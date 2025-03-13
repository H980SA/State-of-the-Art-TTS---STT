import subprocess
import os
from pathlib import Path

# Texto a sintetizar
text = "Hola que tal me llamo Mateo y hoy seré tu asistente para este laboratorio"

# Ruta para guardar el archivo de texto y audio
current_dir = Path(__file__).parent.absolute()
output_file = current_dir / "output.wav"

try:
    # Ejecutar Mimic3 con voz en español
    # Asumiendo que mimic3 está instalado y en PATH
    subprocess.run([
        "mimic3",
        "--voice", "es_ES/m-ailabs_mls_10246",
        "--output-file", str(output_file),
        text
    ])
    print(f"Audio generado y guardado en: {output_file}")
except FileNotFoundError:
    print("Error: Mimic3 no está instalado o no está en PATH. Siga las instrucciones en README.md.")
except Exception as e:
    print(f"Error al ejecutar Mimic3: {e}")
