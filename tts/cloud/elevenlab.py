from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import os

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Obtener la ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

audio = client.text_to_speech.convert(
    voice_id="94zOad0g7T7K4oa7zhDq",
    output_format="mp3_44100_128",  # Formato correcto de los soportados por la API
    text="Hola que tal me llamo Mateo y hoy seré tu asistente para este laboratorio",
    model_id="eleven_flash_v2_5",
)

# Convertir el generador a bytes
audio_bytes = b''.join(list(audio))

# Guardar el audio en la misma carpeta
output_path = os.path.join(current_dir, "elevenLabs.mp3")
with open(output_path, "wb") as f:
    f.write(audio_bytes)

print(f"Audio guardado en: {output_path}")