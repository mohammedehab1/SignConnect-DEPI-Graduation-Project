from fastapi import FastAPI
from routes import asr_router, stt_router,tts_router,api
from helpers.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(asr_router)
app.include_router(stt_router)
app.include_router(tts_router, prefix="/tts", tags=["TTS"])
app.include_router(api)
