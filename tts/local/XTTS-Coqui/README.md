# XTTS by Coqui

## Instalación

```bash
pip install TTS
```

## Requisitos de hardware
- GPU con al menos 8GB VRAM (recomendado)
- Al menos 16GB de RAM

## Uso
1. Ejecute el script `test.py` para generar un archivo de audio con el texto de ejemplo.
2. El archivo de salida se guardará como `output.wav` en la misma carpeta.

## Notas adicionales
- La primera vez que ejecute el script, descargará automáticamente el modelo XTTS v2.
- Para clonar una voz, proporcione un archivo de audio de referencia modificando el parámetro `speaker_wav`.
- Si no tiene suficiente potencia de GPU, el proceso será muy lento.
