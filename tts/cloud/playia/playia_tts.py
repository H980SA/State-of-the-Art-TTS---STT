import requests
import json
from dotenv import load_dotenv
load_dotenv()
import os

url = "https://api.play.ht/api/v2/voices"

headers = {
    "accept": "application/json",
    "AUTHORIZATION": "{}".format(os.getenv("PLAYAI_SECRET_KEY")),
    "X-USER-ID": "{}".format(os.getenv("PLAYAI_USER_ID")),
}

response = requests.get(url, headers=headers)

# Procesa la respuesta como JSON
if response.status_code == 200:
    voices = response.json()
    print(f"Total de voces disponibles: {len(voices)}")
    
    # Muestra las primeras 5 voces como ejemplo
    print("\nPrimeras 5 voces:")
    for i, voice in enumerate(voices[:20]):
        print(f"{i+1}. Nombre: {voice.get('name', 'N/A')}, ID: {voice.get('id', 'N/A')}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)