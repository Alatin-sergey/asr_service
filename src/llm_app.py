from fastapi import FastAPI
from dotenv import load_dotenv
from loguru import logger
from local_llm import ASRModel
from pydantic import BaseModel
from typing import List
import os
import torch

load_dotenv()

app = FastAPI()
asr = ASRModel(
    model=os.getenv("MODEL", "openai/whisper-large-v3-turbo"),
    torch_dtype=torch.float32 if os.getenv("TORCH_DTYPE") == "FLOAT32" else torch.float16,
    device_map = os.getenv("DEVICE"),
    target_sr = int(os.getenv("TARGET_SR")),
)


class AudioData(BaseModel):
    audio_file: List[float]


@app.post("/LLM_service/")
def llm_transcribe(audio: AudioData):
    """
    Транскрибирует аудиоданные, используя LLM-сервис.
    Args:
        audio (AudioData): Объект, содержащий аудиоданные для транскрибации.
    Returns:
        Dict[str, str]:  Словарь, содержащий результат транскрибации.
                           В случае успеха: `{"response": "<текст_транскрибации>"}`.
                           В случае ошибки: `{"error": "<описание_ошибки>"}`.
    """
    try:
        transcription = asr.transcribe_segment(audio.audio_file)
        # transcription = model.generate(audio.audio_file)
        return {"response": transcription}
    except Exception as e:
        logger.exception(f"Error during transcription: {e}")
        return {"error": str(e)}
