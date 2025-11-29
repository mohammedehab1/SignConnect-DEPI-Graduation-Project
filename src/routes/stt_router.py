from fastapi import FastAPI, File, UploadFile , APIRouter
from controller import Resnet
import io
from PIL import Image
import numpy as np
from models import STTOutput

stt_router = APIRouter(prefix="/stt")
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "stores", "STT", "Resnet", "best_resnet18_asl7_15.pth")

model = Resnet(model_path=MODEL_PATH)

@stt_router.post("/predict" ,response_model=STTOutput)
async def predict(file: UploadFile = File(...)):
    data = await file.read()
    frame = np.load(io.BytesIO(data), allow_pickle=False)
    pred, conf = model.predict(frame)
    return STTOutput(predicted=pred, confidence=conf, added_char=pred)
