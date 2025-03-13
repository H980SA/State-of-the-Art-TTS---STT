from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import json
import os
import time
from pydub import AudioSegment

# Suppress verbose logging
SetLogLevel(-1)

# Define paths
model_path = r"C:\php-Course\State-of-the-Art TTS & STT\stt\local\vosk\model\vosk-model-small-es-0.42"
mp3_path = r"C:\php-Course\State-of-the-Art TTS & STT\stt\local\audio.mp3"
wav_path = mp3_path.replace(".mp3", ".wav")

# Check if model exists
if not os.path.exists(model_path):
    print(f"Error: Model not found at {model_path}")
    exit(1)

# Convert MP3 to WAV if needed
if not os.path.exists(wav_path) or os.path.getmtime(mp3_path) > os.path.getmtime(wav_path):
    print("Converting MP3 to WAV...")
    AudioSegment.from_mp3(mp3_path).export(wav_path, format="wav")
    print(f"Converted audio saved to {wav_path}")

# Process audio with timing
start_time = time.time()

print(f"Loading model from {model_path}...")
model = Model(model_path)

# Try to load model with GPU (experimental, may not work)
try:
    # This is an experimental approach - Vosk doesn't officially support GPU acceleration
    # in the Python API directly
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Use first GPU
    print("Attempting GPU acceleration (experimental)")
except:
    print("Using CPU only (standard for Vosk)")

wf = wave.open(wav_path, "rb")
recognizer = KaldiRecognizer(model, wf.getframerate())

print("Processing audio...")
full_text = ""

# Increase batch size for better performance
batch_size = 16000  # Increased from 4000 for better CPU utilization

while True:
    data = wf.readframes(batch_size)
    if len(data) == 0:
        break
    
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        text = result.get("text", "")
        if text:
            print(text)
            full_text += text + " "

final_result = json.loads(recognizer.FinalResult())
final_text = final_result.get("text", "")
if final_text:
    full_text += final_text

end_time = time.time()
print(f"\nProcessing time: {end_time - start_time:.2f} seconds")
print("\nFull transcription:")
print(full_text)