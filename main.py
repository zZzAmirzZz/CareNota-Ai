import os
import shutil
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from ai.pipeline import run_pipeline

load_dotenv()
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API is running 🚀"}


@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):

    if not file.filename.endswith((".wav", ".mp3", ".m4a")):
        return {"error": "Unsupported file format"}

    file_path = f"temp_{uuid.uuid4()}.wav"

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = run_pipeline(file_path)
        return {"result": result}

    except Exception as e:
        return {"error": str(e)}

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)