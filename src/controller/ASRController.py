from stores.whisper import WhisperService
from .AudioPreprocessor import AudioPreprocessor

class ASRController:
    def __init__(self):
        self.whisper = WhisperService()
    
    def transcribe(self, audio_bytes: bytes):
        audio_array, sr = AudioPreprocessor.load_and_resample(audio_bytes)
        text = self.whisper.transcribe(audio_array)
        
        return text
