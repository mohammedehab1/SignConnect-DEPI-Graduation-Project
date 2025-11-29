from pydantic import BaseModel

class STTOutput(BaseModel):
    predicted: str
    confidence: float
    added_char: str