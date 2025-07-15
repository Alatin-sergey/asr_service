from abc import ABC
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from dotenv import load_dotenv
from loguru import logger
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
import os
from typing import List

load_dotenv()


class BaseClass(ABC):
    pass


class ASRModel(BaseClass):
    def __init__(
            self, 
            model: str,
            torch_dtype,
            device_map: str = "cpu",
            target_sr: int = 16000,
            max_new_tokens: int = 440,
            temperature: float = 0.0,
            do_sample: bool = False,
    ):
        self.model = model
        self.processor = AutoProcessor.from_pretrained(self.model)
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model,
            torch_dtype = self.torch_dtype,
        ).to(device_map) 
        self.torch_dtype=torch_dtype
        self.sr = target_sr
        self.max_new_tokens = max_new_tokens
        self.do_sample = do_sample
        self.temperature = temperature
        logger.info("Model is downloaded")

    def transcribe_segment(self, segment: List[float]) -> str:
        """
        Транскрибирует один сегмент аудио, используя LLM-сервис.

        Args:
            segment (List[float]): Список чисел с плавающей точкой, представляющий собой фрагмент (чанк) аудиоданных.
        Returns:
            str:  Текст транскрибированного сегмента аудио.
        """
        try:
            input_features = self.processor(
                segment, 
                sampling_rate=self.sr,
                return_tensors="pt").input_features.to(os.getenv("DEVICE"))
            
            generation_kwargs = {
                "max_new_tokens": self.max_new_tokens,
                "do_sample": self.do_sample,
                "temperature": self.temperature,
            }
            
            predicted_ids = self.model.generate(
                input_features,
                **generation_kwargs
            )
            traunscribe_chunk = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        except Exception as e:
            raise
        return traunscribe_chunk
