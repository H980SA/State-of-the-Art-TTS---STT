# Piper TTS

## Instalación

1. Descargue Piper desde [GitHub](https://github.com/rhasspy/piper/releases)
2. Extraiga los archivos en una ubicación de su elección
3. Descargue un modelo en español desde [aquí](https://huggingface.co/rhasspy/piper-voices/tree/main)
   - Recomendamos el modelo `es_ES-davefx-medium.onnx`
4. Coloque el archivo del modelo en el mismo directorio que el ejecutable de Piper o actualice la ruta en el script

## Uso
1. Asegúrese que Piper esté en su PATH del sistema o modifique la ruta en el script
2. Ejecute el script `test.py` para generar un archivo de audio
3. El archivo de salida se guardará como `output.wav` en la misma carpeta
