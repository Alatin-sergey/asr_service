from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
import librosa
import torch
import io
import streamlit as st
import os
import uuid
import time
import tempfile

class ASRModel:
    def __init__(self):
        self.model_name = "openai/whisper-large-v3-turbo"
        self.cache_dir = os.path.abspath("./.cache")
        self.load_model()
        
        self.temp_dir = os.path.join(os.getcwd(), ".temp")
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        print(f"Using temporary directory: {self.temp_dir}")
        tempfile.tempdir = self.temp_dir

        self.sr = 16000
        os.makedirs(self.cache_dir, exist_ok=True) 
        
 
    def load_model(self):
        device = 'cpu'
        processor_path = os.path.join(self.cache_dir, "processor")
        start_time = time.time()
        if not os.path.exists(processor_path):
            st.write("Загрузка processor...")
            self.processor = AutoProcessor.from_pretrained(self.model_name, cache_dir=self.cache_dir)
            self.processor.save_pretrained(processor_path) #Сохраняем, чтобы не загружать каждый раз
        else:
            self.processor = AutoProcessor.from_pretrained(processor_path)

        # 2. Загрузка model
        model_path = os.path.join(self.cache_dir, "model")
        if not os.path.exists(model_path):
            st.write("Загрузка model...")
            self.model = AutoModelForSpeechSeq2Seq.from_pretrained(self.model_name, cache_dir=self.cache_dir).to(device)
            self.model.save_pretrained(model_path) #Сохраняем, чтобы не загружать каждый раз
        else:
            self.model = AutoModelForSpeechSeq2Seq.from_pretrained(model_path).to(device) 
        end_time = time.time()
        print(f"Время загрузки модели (из кэша): {end_time - start_time:.2f} секунд")

    def import_audio(self, audio_file: io.BytesIO):
        try:
            # Генерируем случайное имя файла
            temp_file_name = str(uuid.uuid4()) + ".wav"
            temp_file_path = os.path.join(self.temp_dir, temp_file_name)

            # Проверяем, что audio_file не пустой
            if not audio_file.getbuffer().nbytes:
                raise ValueError("Audio file is empty")

            # Записываем данные во временный файл
            with open(temp_file_path, "wb") as f:
                f.write(audio_file.read())

            # Загружаем аудио из временного файла
            audio, sr = librosa.load(temp_file_path, sr=self.sr)

            # Удаляем временный файл
            os.remove(temp_file_path)

            return audio, sr

        except Exception as e:
            raise ValueError(f"Ошибка при импорте аудио: {e}")
        

    def split_audio(self, audio, segment_length_sec=30):
        """Разбивает аудио на сегменты заданной длины."""
        segment_length_samples = segment_length_sec * self.sr
        segments = []
        start = 0
        while start < len(audio):
            end = min(start + segment_length_samples, len(audio))
            segments.append(audio[start:end])
            start = end
        return segments
    
    def transcribe_segments(self, segments):
        transcription = []

        for i, segment in enumerate(segments):
            try:
                input_features = self.processor(segment, sampling_rate=self.sr, return_tensors="pt").to('cpu')
                
                self.model.generation_config.forced_decoder_ids = None

                with torch.no_grad():
                    # Передаем max_length
                    predicted_ids = self.model.generate(input_features.input_features)

                transcription.append(self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0])
            except Exception as e:
                raise

        return ''.join(transcription)