# SignConnect 
SignConnect is an AI-powered communication system designed to seamlessly translate between **Sign Language, Text, and Voice**.
It enables a full multimodal communication loop:

**Sign → Text → Voice → Text → Sign**

The system supports:

- **ASL Sign Recognition**
- **Text-to-Speech (TTS)**
-  **Automatic Speech Recognition (ASR)**
- **Text-to-Sign **

This empowers both **deaf/hard-of-hearing** users and **hearing** users to communicate naturally.

## Features
### 1. Sign → Text (ASL Recognition)
- ResNet-based model trained on ASL alphabet.
- Converts hand gestures into text characters.

### 2. Text → Voice (TTS)
- Generates clear, natural speech from text.
- Language-flexible depending on the TTS engine.

### 3. Voice → Text (ASR)
- Built using Whisper Large-V3.
- We fine-tuned the model on Egyptian Arabic speech.
- Produces accurate transcriptions even with noisy input.

### 4. Text → Sign
- Converts text back into ASL signs or fingerspelling.
- Useful for helping hearing users communicate with sign-language users.

## System Workflow
Sign Language  →  Text  →  Voice  →  Text  →  Sign Language

**1. Sign to Text**
```bash
Camera frame → ResNet Model → Predicted Letter → Text
```
**2. Text to Voice**
```bash
Text → TTS Engine → Audio Output
```
**3. Voice to Text**
```bash
Audio → Preprocessing → Whisper (fine-tuned) → Transcription
```
**4. Text to Sign**
```bash
Text → Sign Rendering Module → ASL Animation / Frames
```
## Project Structure
```bash
.
├── LICENSE
├── README.md
├── asl_video_project/              # ASL recognition project
│   ├── app/                        # ASL API and components
│   ├── asl_alphabet/               # ASL dataset
│   └── tests/
├── frontend/                       # Frontend (Mediapipe utils)
├── src/                            # Main backend system
│   ├── controller/                 # ASR, STT, TTS controllers
│   ├── stores/                     # Whisper, ResNet, TTS models
│   ├── routes/                     # FastAPI endpoints
│   ├── models/                     # API output schemas
│   ├── helpers/                    # Config utilities
│   ├── notebooks/                  # Whisper/TTS training notebooks
│   ├── main.py                     # FastAPI entry point
│   └── data/
└── text_to_sign_app/               # Text-to-sign rendering
```


## API Endpoints (FastAPI)
### 1. Sign Recognition
```http
POST /stt/predict-sign
```

### 2. Text-to-Speech
```http
POST /tts/speak
```

### 3. ASR – Transcribe Speech
```http
POST /asr/transcribe
```
### 4. Text-to-Sign
```http
GET /api/video?letter=<LETTER>
```


## Tech Stack
- Python
- FastAPI
- Whisper Large-V3 (fine-tuned)
- ResNet-18 (ASL)
- PEFT / LoRA
- Mediapipe
- Torch / Transformers

## Purpose

**SignConnect aims to support:**

- Deaf and hard-of-hearing individuals
- Hearing users who want to communicate with them
- Schools and educational tools
- Accessibility applications
- Healthcare, customer service, and public services

By bridging sign, text, and voice, SignConnect makes communication more inclusive and accessible.


<!-- ## Contributers
- [Khaled Zakarya](https://github.com/khaledzakarya) → khaledzzyadaa@gmail.com
- [Khaled Helmy](https://github.com/khalledhelmy) → khalledhellmy@gmail.com
- [Mohamed Ehab](_____) → ____
- [Samer Zaid](_____) → ____ -->