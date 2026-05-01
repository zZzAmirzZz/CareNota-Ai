import os
import uuid
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from ai.pipeline import run_pipeline
from dotenv import load_dotenv
load_dotenv()

load_dotenv()


os.makedirs("temp", exist_ok=True)

app = FastAPI()


class AudioRequest(BaseModel):
    audio_url: str


@app.get("/")
def home():
    return {"message": "API is running 🚀"}


@app.post("/process-audio")
async def process_audio(request: AudioRequest):
    file_path = None

    try:
        response = requests.get(request.audio_url, timeout=15)
        response.raise_for_status()

        # validate file type
        content_type = response.headers.get("Content-Type", "")
        if "audio" not in content_type:
            return {"error": f"Invalid file type: {content_type}"}

        file_path = f"temp/{uuid.uuid4()}.wav"

        with open(file_path, "wb") as f:
            f.write(response.content)

        result = run_pipeline(file_path)
        return result

    except Exception as e:
        return {"error": str(e)}

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)