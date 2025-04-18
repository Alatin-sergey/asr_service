from fastapi import FastAPI, File, UploadFile, HTTPException
import logging
import io

from utils.ASR import ASRModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

asr = ASRModel() 

@app.post("/ASR/")
async def transcribe_audio(file: UploadFile = File(...)) -> dict[str, str]: 
    try:
        logger.info("Функция transcribe_audio вызвана")
        logger.info(f"Имя файла: {file.filename}")
        logger.info(f"Тип контента: {file.content_type}")
        contents = await file.read() 
        logger.info(f"Размер файла: {len(contents)}")

        audio, sr = asr.import_audio(io.BytesIO(contents)) 
        segments = asr.split_audio(audio)
        transcription = asr.transcribe_segments(segments)
        return {"transcription": transcription}

    except ValueError as e:
        logger.error(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Exception: {e}") 
        raise HTTPException(status_code=500, detail=str(e))