from fastapi import APIRouter, File, UploadFile
from controller import ASRController
from models import ASROutput

asr_router = APIRouter( 
                   prefix="/asr", 
                   tags=["ASR"]
                   )
asr_controller = ASRController()

@asr_router.post("/transcribe", response_model=ASROutput)
async def transcribe_audio(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    text = asr_controller.transcribe(audio_bytes)
    return ASROutput(transcription=text)