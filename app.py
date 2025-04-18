import streamlit as st
import requests
import os
import io


FASTAPI_URL = os.environ.get("FASTAPI_URL", "http://localhost:8000")

st.title('Automatic Speech Recognition')

audio_file = st.file_uploader("Import your audio file", type=['mp3', 'wav', 'ogg', 'flac'])



if audio_file is not None:
    st.audio(audio_file, format='audio/' + audio_file.name.split('.')[-1])


    if st.button('Transcribation'):
        try:
            files = {'file': (audio_file.name, audio_file, audio_file.type)}
            print("Files:", files)
            response = requests.post(f"{FASTAPI_URL}/ASR/", files=files)
            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                transcription = response.json()
                st.write("Transcription:")
                st.write(transcription['transcription'])
            else:
                st.error(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to FastAPI: {e}")







