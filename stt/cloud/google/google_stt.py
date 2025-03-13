import io
from google.cloud import speech

def run_quickstart() -> None:
    # Instancia el cliente de Speech-to-Text
    client = speech.SpeechClient()

    # Ruta del archivo de audio a transcribir
    audio_file = r"C:\php-Course\State-of-the-Art TTS & STT\stt\cloud\audio.mp3"

    # Lee el contenido del archivo de audio
    with io.open(audio_file, "rb") as archivo:
        contenido = archivo.read()

    # Crea el objeto de audio a partir del contenido leído
    audio = speech.RecognitionAudio(content=contenido)

    # Configuración para la transcripción
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=44100,  # Ajusta este valor según la tasa de muestreo real de tu audio
        language_code="es-ES"
    )

    # Detecta el habla en el archivo de audio
    respuesta = client.recognize(config=config, audio=audio)

    # Imprime el resultado de la transcripción
    for resultado in respuesta.results:
        print(f"Transcripción: {resultado.alternatives[0].transcript}")

if __name__ == "__main__":
    run_quickstart()
