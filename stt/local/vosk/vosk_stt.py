from vosk import Model, KaldiRecognizer
import wave
import json
import os
from pydub import AudioSegment

# Define paths
model_path = r"C:\php-Course\State-of-the-Art TTS & STT\stt\local\vosk\model\vosk-model-es-0.42"
# Or use the smaller model if you prefer:
# model_path = r"C:\php-Course\State-of-the-Art TTS & STT\stt\local\vosk\model\vosk-model-small-es-0.42"

mp3_path = r"C:\php-Course\State-of-the-Art TTS & STT\stt\local\audio.mp3"
wav_path = mp3_path.replace(".mp3", ".wav")

# Check if model exists
if not os.path.exists(model_path):
    print(f"Error: Model not found at {model_path}")
    exit(1)

# Convert MP3 to WAV (Vosk requires WAV format)
try:
    print("Converting MP3 to WAV...")
    AudioSegment.from_mp3(mp3_path).export(wav_path, format="wav")
    print(f"Converted audio saved to {wav_path}")
except Exception as e:
    print(f"Error converting audio: {e}")
    print("Make sure you have ffmpeg installed and pydub: pip install pydub")
    exit(1)

# Load model and process audio
try:
    print(f"Loading model from {model_path}...")
    model = Model(model_path)
    
    wf = wave.open(wav_path, "rb")
    
    # Create recognizer with the correct sample rate from WAV file
    recognizer = KaldiRecognizer(model, wf.getframerate())
    
    print("Processing audio...")
    full_text = ""
    
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            if text:
                print(text)
                full_text += text + " "
    
    # Get final result
    final_result = json.loads(recognizer.FinalResult())
    final_text = final_result.get("text", "")
    if final_text:
        print(final_text)
        full_text += final_text
    
    print("\nFull transcription:")
    print(full_text)
    
except Exception as e:
    print(f"Error during speech recognition: {e}")