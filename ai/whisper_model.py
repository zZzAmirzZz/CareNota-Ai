import whisper

model = whisper.load_model("base")

def transcribe_audio(file_path):
    result = model.transcribe(file_path, language="ar", task="transcribe")
    return result["text"]