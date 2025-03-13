from dotenv import load_dotenv
from io import BytesIO
import os
from elevenlabs.client import ElevenLabs

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

# Define the path to the audio file
audio_path = r"C:/php-Course/State-of-the-Art TTS & STT/stt/cloud/audio.mp3"

# Open the file in binary mode and read its contents
with open(audio_path, "rb") as audio_file:
    audio_data = BytesIO(audio_file.read())

transcription = client.speech_to_text.convert(
    file=audio_data,
    model_id="scribe_v1", # Model to use, for now only "scribe_v1" is supported
    tag_audio_events=True, # Tag audio events like laughter, applause, etc.
    language_code="es", # Language of the audio file. If set to None, the model will detect the language automatically.
    diarize=True, # Whether to annotate who is speaking
)

print(transcription.text)

