from ai.whisper_model import transcribe_audio
from ai.gemini import reconstruct_arabic, extract_json, safe_json_parse


def run_pipeline(file_path):
    text = transcribe_audio(file_path)

    corrected = reconstruct_arabic(text)

    raw_json = extract_json(corrected)

    final_json = safe_json_parse(raw_json)

    return final_json