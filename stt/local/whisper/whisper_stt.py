import whisper
import torch
import time

# Check if GPU is available
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
    device = "cuda"
else:
    print("GPU not available, using CPU")
    device = "cpu"

start_time = time.time()

# Load model with device specification
model = whisper.load_model("turbo", device=device)

# Transcribe audio
result = model.transcribe(r"C:\php-Course\State-of-the-Art TTS & STT\stt\local\audio.mp3", language="es")

end_time = time.time()
print(f"Processing time: {end_time - start_time:.2f} seconds")
print(result["text"])