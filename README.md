# Сервис Транскрибации Аудио

Этот проект реализует сервис транскрибации аудио, использующий модель [openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) от Hugging Face. Он предоставляет веб-интерфейс Streamlit и API FastAPI для транскрибации аудиофайлов.

## Функциональность

* **Транскрибация Аудио**: Транскрибирует аудиофайлы с использованием модели Whisper.
* **Интерфейс Streamlit**: Предоставляет удобный веб-интерфейс для загрузки и транскрибации аудио.
* **API FastAPI**: Предлагает API-endpoint для программного доступа к сервису транскрибации.
* **Dockerized**: Упакован в Docker-контейнер для легкого развертывания и переносимости.

## Используемые технологии

* **openai/whisper-large-v3-turbo**: модель для преобразования речи в текст.
* **Hugging Face Transformers**: библиотека для применения предварительно обученных моделей.
* **Streamlit**: фреймворк для создания веб-приложений.
* **FastAPI**: веб-фреймворк для передачи данных между сервисами.
* **Docker**: Платформа для контейнеризации приложений.


## Необходимые условия

* [Docker](https://docs.docker.com/get-docker/), установленный в вашей системе.


## Скриншоты

![Screenshot: intarface](pictures/interface.png)

![Screenshot: div Hashing](pictures/import_audio.png)

![Screenshot: List of Hash Functions](pictures/transcribation.png)


## Установка

1. Убедитесь, что Docker и Docker Compose установлены на вашем сервере.
2. Убедитесь, что команда make установлена в системных переменных среды. Если вы еще не установили make, выполните следующие действия:

    * Для Windows: Следуйте инструкциям на этом сайте: https://www.thewindowsclub.com/install-and-run-makefile-on-windows. Обычно это включает в себя установку MinGW или аналогичного инструментария, а затем добавление каталога, содержащего make (обычно C:\MinGW\bin или аналогичный), в системную переменную среды PATH.
    * Для macOS и Linux: make обычно предустановлен или легко устанавливается с помощью диспетчера пакетов вашей системы (например, apt install make на Debian/Ubuntu, brew install make на macOS).


3. Клонируйте репозиторий:
```bash
git clone https://github.com/Alatin-sergey/asr_service.git
cd asr_service
```

4. Убедитесь, что Docker Desktop запущен в вашей системе.

5. Запустите проект, используя make -f makefile. Обратите внимание, что начальное создание Docker-образа может занять до часа из-за загрузки библиотек и обработки тензоров.

```bash
make -f makefile
```

6. Откройте Streamlit-приложение в вашем браузере по адресу http://localhost:8501. Этот порт используется для пользовательского интерфейса. Получите доступ к API FastAPI по адресу http://localhost:8001. Этот порт используется для бэкенд-API.

7. Чтобы остановить makefile, используйте:
```bash
make -f makefile down
```

## Endpoint: /api/transcribe

* Метод: POST

* Описание: Транскрибирует аудиофайл.

* Тело запроса:
    file: Аудиофайл для транскрибации (например, .wav, .mp3).

* Тело ответа:
    json

{
  "transcription": "Транскрибированный текст."
}

* Пример запроса (с использованием curl):
```bash

curl -X POST -F "file=@audio.wav" http://localhost:8000/api/transcribe
```

## Лицензия

См. файл LICENSE для получения подробной информации.

## Благодарности

* В этом проекте используется модель openai/whisper-large-v3-turbo, которая лицензируется в соответствии с ее соответствующей лицензией (см. [LICENSE](LICENSE)).
* Спасибо команде Hugging Face за предоставление библиотеки Transformers.



# Audio Transcription Service

This project implements an audio transcription service using the [openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) model from Hugging Face. It provides both a Streamlit web interface and a FastAPI API for transcribing audio files.

## Features

*   **Audio Transcription:** Transcribes audio files using the Whisper model.
*   **Streamlit Interface:** Provides a user-friendly web interface for uploading and transcribing audio.
*   **FastAPI API:** Offers an API endpoint for programmatic access to the transcription service.
*   **Dockerized:** Packaged in a Docker container for easy deployment and portability.

## Technologies Used

*   [openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo): A powerful speech-to-text model.
*   [Hugging Face Transformers](https://huggingface.co/transformers/): A library for using pre-trained models.
*   [Streamlit](https://streamlit.io/): A framework for building web applications.
*   [FastAPI](https://fastapi.tiangolo.com/): A modern, high-performance web framework.
*   [Docker](https://www.docker.com/): A platform for containerizing applications.

## Prerequisites

*   [Docker](https://docs.docker.com/get-docker/) installed on your system.

## Screenshots

![Screenshot: intarface](pictures/interface.png)

![Screenshot: div Hashing](pictures/import_audio.png)

![Screenshot: List of Hash Functions](pictures/transcribation.png)

## Installation

1.  Make sure Docker and Docker Compose are installed on your server.

2.  Ensure that the `make` command is installed in your system's environment variables.  If you haven't installed `make` yet, follow these instructions:

    *   **For Windows:** Follow the instructions on this website: [https://www.thewindowsclub.com/install-and-run-makefile-on-windows](https://www.thewindowsclub.com/install-and-run-makefile-on-windows).  This usually involves installing MinGW or a similar toolchain, and then adding the directory containing `make` (usually `C:\MinGW\bin` or similar) to your system's `PATH` environment variable.
    *   **For macOS and Linux:** `make` is typically pre-installed or easily installed using your system's package manager (e.g., `apt install make` on Debian/Ubuntu, `brew install make` on macOS).

2.  Clone the repository:

    ```bash
    git clone https://github.com/Alatin-sergey/asr_service.git
    cd asr_service
    ```

3. Ensure that Docker Desktop is running on your system. 

4.  Run the project using `make -f makefile`. Note that the initial Docker image creation may take up to an hour due to library downloads and tensor processing.

    ```bash
    make -f makefile
    ```

5.  Open the Streamlit application in your browser at `http://localhost:8501`. This port is used for the user interface.
    Access the FastAPI API at `http://localhost:8000`. This port is used for the backend API.

6. To stop makefile use:

    ```bash
    make -f makefile down
    ```

### Endpoint: `/api/transcribe`

*   **Method:** `POST`
*   **Description:** Transcribes an audio file.
*   **Request Body:**

    *   `file`: Audio file to transcribe (e.g., `.wav`, `.mp3`).

*   **Response Body:**

    ```json
    {
      "transcription": "The transcribed text."
    }
    ```

*   **Example Request (using `curl`):**

    ```bash
    curl -X POST -F "file=@audio.wav" http://localhost:8000/api/transcribe
    ```

## License

See the [LICENSE](LICENSE) file for details.

## Acknowledgments

*   This project uses the [openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) model, which is licensed under its respective license.
*   Thanks to the Hugging Face team for providing the Transformers library.