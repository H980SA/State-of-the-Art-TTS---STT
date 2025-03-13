import os
import subprocess
from pathlib import Path

# Texto a sintetizar
text = "Hola que tal me llamo Mateo y hoy seré tu asistente para este laboratorio"

# Ruta para guardar el archivo de texto y audio
current_dir = Path(__file__).parent.absolute()
text_file = current_dir / "input.txt"
output_file = current_dir / "output.wav"

# Guardar el texto en un archivo
with open(text_file, "w", encoding="utf-8") as f:
    f.write(text)

# Ejecutar Piper
try:
    # Asumiendo que piper está instalado y en PATH
    # Usando modelo es_ES-davefx-medium
    subprocess.run([
        "piper",
        "--model", "es_ES-davefx-medium.onnx",
        "--output_file", str(output_file),
        str(text_file)
    ])
    print(f"Audio generado y guardado en: {output_file}")
except FileNotFoundError:
    print("Error: Piper no está instalado o no está en PATH. Siga las instrucciones en README.md.")
except Exception as e:
    print(f"Error al ejecutar Piper: {e}")
