import streamlit as st
from app.controllers.video_controller import VideoController

DATASET = "dataset/asl_alphabet"

controller = VideoController(DATASET)

st.title("ASL Word to Video API")
st.write("Enter a word to convert it into ASL sign letters video.")

word = st.text_input("Enter a word")

if st.button("Generate Video"):
    output_path = controller.generate_word_video(word)

    if output_path:
        st.video(output_path)
    else:
        st.error("Failed: No video generated. Check the word or dataset folders.")
