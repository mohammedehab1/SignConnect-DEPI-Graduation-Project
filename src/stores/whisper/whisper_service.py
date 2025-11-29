import torch
from transformers import WhisperProcessor, AutoModelForSpeechSeq2Seq
from peft import PeftModel
from helpers.config import settings
import os

class WhisperService:
    def __init__(self):
        BASE_MODEL = settings.BASE_MODEL
        LORA_REPO = settings.HF_REPO  
        HF_CACHE_DIR = settings.HF_CACHE_DIR

        os.makedirs(HF_CACHE_DIR, exist_ok=True)

        self.processor = WhisperProcessor.from_pretrained(
            BASE_MODEL,
            token=settings.HF_TOKEN,
            cache_dir=HF_CACHE_DIR
        )

        base_model = AutoModelForSpeechSeq2Seq.from_pretrained(
            BASE_MODEL,
            cache_dir=HF_CACHE_DIR,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )


        self.model = PeftModel.from_pretrained(
            base_model,
            LORA_REPO,
            token=settings.HF_TOKEN,
            cache_dir=HF_CACHE_DIR
        )

        self.model.eval()

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)

    def transcribe(self, audio_array):
        inputs = self.processor(
            audio_array,
            sampling_rate=16000,
            return_tensors="pt"
        ).input_features

        inputs = inputs.to(self.device)

        if self.model.dtype == torch.float16:
            inputs = inputs.half()
        else:
            inputs = inputs.float()

        with torch.no_grad():
            predicted_ids = self.model.generate(inputs)

        text = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return text