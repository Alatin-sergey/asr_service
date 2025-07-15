from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from backend_utils import request_to_llm


class Item(BaseModel):
    chunk: List[float]


app = FastAPI()


@app.post("/get_transcribe/")
async def get_transcribe(file: Item):
    """
    Принимает фрагмент аудио, отправляет его в LLM-сервис для транскрибации и возвращает результат.
    Args:
        file (Item): Объект, содержащий фрагмент аудио для транскрибации.
    Returns:
        Dict[str, str]:  Словарь, содержащий транскрибированный текст в ключе "response".
    """
    return {"response": request_to_llm(file.chunk)}
