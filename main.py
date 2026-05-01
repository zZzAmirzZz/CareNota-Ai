import os
import uuid
import requests
import shutil
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from ai.pipeline import run_pipeline

os.makedirs('temp', exist_ok=True)

load_dotenv()
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

app = FastAPI()

class AudioRequest(BaseModel):
    audio_url: str

@app.get("/")
def home():
    return {"message": "API is running 🚀"}

@app.post("/process-audio")
async def process_audio(request: AudioRequest):
    audio_url = request.audio_url
    file_path = None

    try:
        response = requests.get(audio_url)
        response.raise_for_status()

        file_path = f"temp/{uuid.uuid4()}.wav"
        with open(file_path, "wb") as buffer:
            buffer.write(response.content)

        result = run_pipeline(file_path)
        return result

    except Exception as e:
        return {"error": str(e)}

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)