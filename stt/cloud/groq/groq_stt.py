
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq()
filename = r"C:\php-Course\State-of-the-Art TTS & STT\stt\cloud\audio.mp3"

with open(filename, "rb") as file:
    transcription = client.audio.transcriptions.create(
      file=(filename, file.read()),
      model="whisper-large-v3-turbo",
      response_format="verbose_json",
    )
    print(transcription.text)
      