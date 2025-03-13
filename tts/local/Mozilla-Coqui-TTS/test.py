from TTS.api import TTS
import os

# Inicializar TTS con modelo en español
tts = TTS(model_name="tts_models/es/css10/vits", progress_bar=True)

# Texto a sintetizar
text = "Hola que tal me llamo Mateo y hoy seré tu asistente para este laboratorio"

# Ruta para guardar el audio
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.wav")

# Generar audio
tts.tts_to_file(text=text, file_path=output_path)

print(f"Audio generado y guardado en: {output_path}")
