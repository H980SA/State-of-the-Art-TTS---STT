import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

api_key = os.getenv("CARTESIA_API_KEY")

url = "https://api.cartesia.ai/tts/bytes"
payload = {
    "model_id": "sonic-2",
    "transcript": "Hola que tal me llamo Mateo y hoy seré tu asistente para este laboratorio",
    "voice": {
        "model": "id",
        "id": "79743797-2087-422f-8dc7-86f9efca85f1"
    },
    "output_format": {
        "container": "mp3",
        "bit_rate": 128000,
        "sample_rate": 44100
    },
    "language": "en"
}
headers = {
    "Cartesia-Version": "2024-06-10",
    "X-API-Key": api_key,
    "Content-Type": "application/json"
}

# Realizar la solicitud y recibir la respuesta como contenido binario
response = requests.post(url, json=payload, headers=headers)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    # Guardar el contenido de audio en un archivo
    output_file = "output_audio.mp3"  # Cambiado a .mp3 según el formato solicitado
    with open(output_file, "wb") as f:
        f.write(response.content)
    print(f"Audio guardado correctamente en {output_file}")
else:
    print(f"Error: {response.status_code}")
    print(f"Mensaje: {response.text}")