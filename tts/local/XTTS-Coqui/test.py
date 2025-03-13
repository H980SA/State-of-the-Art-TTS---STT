import os
from TTS.api import TTS
import torch

# Verificar disponibilidad de GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Usando dispositivo: {device}")

try:
    # Inicializar TTS con modelo XTTS v2
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    # Texto a sintetizar
    text = "Hola que tal me llamo Mateo y hoy seré tu asistente para este laboratorio"

    # Ruta para guardar el audio
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.wav")

    # Generar audio (utilizando una voz en español)
    tts.tts_to_file(
        text=text,
        file_path=output_path,
        speaker_wav=None,  # Si tienes un archivo de voz de referencia, puedes especificarlo aquí
        language="es"
    )

    print(f"Audio generado y guardado en: {output_path}")
    
except Exception as e:
    print(f"Error al generar audio: {e}")
    print("Asegúrese de tener suficiente RAM y potencia de GPU para XTTS v2")
