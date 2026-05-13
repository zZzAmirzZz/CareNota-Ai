import whisper

model = whisper.load_model("base")

def transcribe_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    
    result = model.transcribe(file_path, language="ar", task="transcribe")
    return result["text"]