from pydantic import BaseModel

class ASROutput(BaseModel):
    transcription: str