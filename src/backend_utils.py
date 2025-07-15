import requests
from loguru import logger
from dotenv import load_dotenv
import os
from fastapi import HTTPException
from typing import List

load_dotenv()


def request_to_llm(audio_file: List[float]) -> List[str]:
    """
    Отправляет аудиоданные в LLM-сервис для транскрибации.
    Args:
        audio_file (List[float]): Список чисел с плавающей точкой, представляющих собой аудиоданные.
    Returns:
        List[str]:  Словарь, содержащий ответ от LLM-сервиса. Ключ `response` содержит результат транскрибации.
    """
    try:
        response = requests.post(
            url=f"http://{os.getenv('LLM_SERVICE', 'llm')}:{os.getenv('LLM_PORT', 8002)}/LLM_service/", 
            json={'audio_file': audio_file},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        logger.exception(f"Ключи словаря {response.json().keys()}")
        return response.json()['response']
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to LLM service: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to LLM service")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
