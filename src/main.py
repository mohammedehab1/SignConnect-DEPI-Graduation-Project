from fastapi import FastAPI
from routes.asr_router import asr_router
from helpers.config import settings

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.include_router(asr_router, 
                   prefix="/asr", 
                   tags=["ASR"])

@app.get('/')
def root():
    return {
        "message": f"{settings.APP_NAME} is running!"
    }
