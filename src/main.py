from fastapi import FastAPI
from routes import stt_router
from helpers.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(asr_router)
app.include_router(stt_router)

@app.get('/')
def root():
    return {
        "message": f"{settings.APP_NAME} is running!"
    }
