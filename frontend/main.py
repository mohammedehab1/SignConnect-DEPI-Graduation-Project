import streamlit as st
import cv2
import requests
import numpy as np
from PIL import Image
from mediapipe_utils import MediaPipeProcessor
import time
import io

st.title('SignConnect')

cooldown = 0.45
flash_duration = 0.35
last_capture_time = 0
flash_until = 0

vote_window = []
VOTE_REQUIRED = 3
CONF_REQUIRED = 0.45
current_text = ""
PROCESS_INTERVAL = 0.5
last_process_time = 0


st.write("ASL")
API_URL = "https://8000-01kb8hcty9d4xc1v0s3m5zz6ya.cloudspaces.litng.ai//stt/predict"

mp_processor = MediaPipeProcessor()
cap = cv2.VideoCapture(0)
frame_window = st.image([])
run_cam = st.button("Start Camera")
placeholder = st.empty()
i=0
while run_cam:
    i+=1
    ret, frame = cap.read()
    if not ret:
        st.error("Camera not detected!")
        break

    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    now = time.time()
    results = mp_processor.process_frame(rgb_frame)

    roi_x1, roi_y1 = 0 // 2, h // 4
    roi_x2, roi_y2 = w // 2, 3 * h // 4
    cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (255,255,255), 2)

    if results:
        if mp_processor.is_hand_in_allowed_area(results, w, h):
            x1, y1, x2, y2 = mp_processor.get_fixed_bbox(results, w, h)
            if now - last_process_time > PROCESS_INTERVAL:

                hand_crop = frame[y1:y2, x1:x2]
                hand_crop_rgb = cv2.cvtColor(hand_crop, cv2.COLOR_BGR2RGB)
                buffer = io.BytesIO()
                np.save(buffer, hand_crop_rgb)
                buffer.seek(0)
                files = {"file": ("frame.npy", buffer.read(), "application/octet-stream")}
                try:
                    res = requests.post(API_URL, files=files, timeout=2).json()
                    pred_text = res.get("added_char") or res.get("predicted") or ""
                    conf = res.get("confidence") or 0
                except:
                    pred_text = "API ERROR"
                    conf = 0

                text = f"{pred_text} | conf:{conf}"
                cv2.putText(frame, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                vote_window.append(pred_text)
                if len(vote_window) > 5:
                    vote_window.pop(0)

                voted = max(set(vote_window), key=vote_window.count)
                vote_count = vote_window.count(voted)

                if vote_count >= VOTE_REQUIRED and conf > CONF_REQUIRED:
                    if now - last_capture_time > cooldown:
                        flash_until = now + flash_duration

                        if voted == "SPACE":
                                current_text += "_"
                        elif voted == "DEL":
                            current_text = current_text[:-1]
                        elif voted == "CLEAR":
                            current_text = ""
                        else:
                            current_text += voted
                        vote_window = []
                        last_capture_time = now
                
                last_process_time = now
            


            cv2.rectangle(frame, (x1, y1), (x2, y2), (255,255,255), 2)

            cv2.putText(frame, f"{pred_text}", (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            if now < flash_until:
                mp_processor.apply_glow(frame, x1, y1, x2, y2)
    else:
        cv2.putText(frame, "NO HAND DETECTED", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.putText(frame, current_text, (10, h - 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (200,0,200), 2)
    placeholder.text_area("Transcription", current_text, height=200, key=f"transcription_{i}")


    frame_window.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


st.write('Upload an audio file to get its transcription.')

uploaded_file = st.file_uploader("Choose an audio file", 
                                 type=["wav", "mp3", "flac", "m4a", "aac", "ogg", "wma"])

ASR_URL = "https://8000-01kb8hcty9d4xc1v0s3m5zz6ya.cloudspaces.litng.ai/asr/transcribe"

if uploaded_file is not None:
    st.audio(uploaded_file)
    audio_bytes = uploaded_file.read()

    if st.button('Transcribe'):
        with st.spinner('Transcribing...'):
            files = {'file': (uploaded_file.name, audio_bytes, uploaded_file.type)}

            response = requests.post(ASR_URL, files=files)

            if response.status_code == 200:
                result = response.json()

                st.success('Transcription completed!')
                st.text_area('Trascription', result.get('transcription', ''), height=200)
            else:
                st.error('Error during transcription. Please try again.' + response.text)
