# Mimic3

## Instalación

```bash
pip install mycroft-mimic3-tts[all]
```
mimic3 --download-voice es_ES/carlfm_low

## Descarga de voces
Para descargar la voz en español:
```bash
mimic3-download es_ES/m-ailabs_mls_10246
```

## Uso
1. Ejecute el script `test.py` para generar un archivo de audio
2. El archivo de salida se guardará como `output.wav` en la misma carpeta

## Voces disponibles
Para listar todas las voces disponibles:
```bash
mimic3-voices
```

## Servidor web (opcional)
Mimic3 también puede ejecutarse como servidor web:
```bash
mimic3-server
```
Esto permite enviar solicitudes TTS a través de HTTP.
