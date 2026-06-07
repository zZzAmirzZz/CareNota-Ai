import os
import uuid
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from ai.pipeline import run_pipeline

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
        async with httpx.AsyncClient() as client:
            response = await client.get(request.audio_url, timeout=15)

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("audio"):
            return {"error": f"Invalid file type: {content_type}"}

        if len(response.content) > 10 * 1024 * 1024:
            return {"error": "File too large"}

        file_path = f"temp/{uuid.uuid4()}.wav"

        with open(file_path, "wb") as f:
            f.write(response.content)

        print("Running pipeline...")
        result = run_pipeline(file_path)

        return result

    except Exception as e:
        return {"error": str(e)}

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)