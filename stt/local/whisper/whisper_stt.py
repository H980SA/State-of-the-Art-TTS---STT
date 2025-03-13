import whisper

model = whisper.load_model("large-v3-turbo")  # Options: tiny, base, small, medium, large
result = model.transcribe(r"C:\php-Course\State-of-the-Art TTS & STT\stt\local\audio.mp3", language="es")
print(result["text"])