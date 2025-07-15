import streamlit as st
from loguru import logger
from app_utils import request_to_backend


st.title("Автоматическая транскрибация аудио")
st.write("Выберете аудиофайл")

audiofile = st.file_uploader(
    label="Добавьте файл",
    type=["mp3", "wav", "ogg", "flac"]
)

if audiofile is not None:
    st.audio(audiofile, format="audio/" + audiofile.name.split(".")[-1])
    if st.button("Транскрибция"):
        with st.spinner("Выполнение запроса..."):
            try:
                logger.info(f"Тип файла {type(audiofile)}")
                transcribe = request_to_backend(audiofile)
                st.write("Транскрибция")
                st.write(' '.join(transcribe))
            except Exception as e:
                logger.info(f"Error: {e}")
