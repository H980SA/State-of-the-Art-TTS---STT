import os
import time
from faster_whisper import WhisperModel

model_size = "large-v3"

# Try loading the model with retries
max_retries = 3
retry_delay = 5  # seconds

for attempt in range(max_retries):
    try:
        print(f"Attempt {attempt+1}/{max_retries} to load model...")
        # Run on GPU with FP16
        model = WhisperModel(model_size, device="cuda", compute_type="float16")
        break  # Success, exit loop
    except Exception as e:
        print(f"Error loading model: {e}")
        if attempt < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries exceeded. Try using a smaller model ('small', 'medium' or 'base').")
            model_size = "medium"
            print(f"Falling back to {model_size} model...")
            model = WhisperModel(model_size, device="cuda", compute_type="float16")

segments, info = model.transcribe("audio.mp3", beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))