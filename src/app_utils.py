import librosa
from loguru import logger
import requests
import os
from dotenv import load_dotenv
import io
from typing import List
from streamlit.runtime.uploaded_file_manager import UploadedFile

load_dotenv()


def request_to_backend(
        audio: UploadedFile,
        chunk_size_sec: int = 30,
) -> List[str]:
    """
    Отправляет аудиофайл по чанкам на backend для транскрибации.
    Args:
        audio: Объект, предоставляющий доступ к содержимому аудиофайла (объект UploadedFile из Streamlit).
        chunk_size_sec (int): Размер чанка (фрагмента) аудио в секундах.  По умолчанию 30 секунд.
    Returns:
        List[str]: Список строк, представляющих собой транскрипцию каждого чанка.
    """
    file_bytes = None
    file_bytes = io.BytesIO(audio.read())
    audio, original_sr = librosa.load(file_bytes, sr=None)
    audio_file = resample_audio(audio, original_sr)
    audio_list = audio_file.tolist()
    chunk_length = chunk_size_sec * int(os.getenv("TARGET_SR"))
    res_text = []
    for i, chunk in enumerate([audio_list[i:i + chunk_length] for i in range(0, len(audio_list), chunk_length)]):
        logger.info(f"Chunk number:{i}")
        response = requests.post(
            url=f"http://{os.getenv('BACKEND_SERVICE', 'backend')}:{os.getenv('BACKEND_PORT', 8001)}/get_transcribe/",
            json={"chunk": chunk},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        res_text.append(response.json()["response"])
    logger.info(f"results{res_text}")
    return res_text


def resample_audio(
        audio, 
        orig_sr, 
        target_sr: int = 16000
) -> List[float]:
    """Передискретизирует аудиосигнал.
    Args:
        audio (np.ndarray): Массив NumPy с аудиоданными.
        orig_sr (int): Исходная частота дискретизации.
        target_sr (int): Целевая частота дискретизации (по умолчанию 16000).

    Returns:
        np.ndarray: Передискретизированный аудиосигнал.
    """
    target_sr = int(os.getenv('TARGET_SR'))
    if orig_sr != target_sr:
        audio_resampled = librosa.resample(audio, orig_sr=orig_sr, target_sr=target_sr)
        return audio_resampled
    else:
        return audio
