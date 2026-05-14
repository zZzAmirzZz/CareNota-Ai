import uuid
import os
from pydub import AudioSegment
from pydub.effects import normalize

def preprocess_audio(input_path, output_path=None):

    os.makedirs("temp", exist_ok=True)

    if output_path is None:
        output_path = f"temp/{uuid.uuid4()}.wav"

    audio = AudioSegment.from_file(input_path)

    audio = (
        audio
        .set_frame_rate(16000)
        .set_channels(1)
        .set_sample_width(2)
    )

    audio = normalize(audio)

    audio.export(output_path, format="wav")

    return output_path