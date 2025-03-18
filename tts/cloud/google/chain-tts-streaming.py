#!/usr/bin/env python
# Copyright 2024 Google LLC

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from google.cloud import texttospeech
import os
import asyncio
import itertools
import time
import re

# Cargar las variables de entorno
load_dotenv()

# Configuración del modelo GPT-4 de LangChain con el prompt de comediante
model = ChatOpenAI(model="gpt-4o-mini-2024-07-18")
template = "eres un comediante y di algo gracioso sobre {topic}, sé lo más coloquial posible sin uso de ** o ## o -"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", template), ("user", "{topic}")]
)
parser = StrOutputParser()
chain = prompt_template | model | parser

# Configuración del cliente de Google Cloud TTS
client = texttospeech.TextToSpeechClient()

# Configuración de la voz para el TTS
streaming_config = texttospeech.StreamingSynthesizeConfig(
    voice=texttospeech.VoiceSelectionParams(name="es-ES-Neural2-A", language_code="es-ES")
)

# Función que guarda el audio generado por TTS
async def save_audio_to_file(audio_content, filename):
    """Guarda el contenido de audio en un archivo .mp3"""
    with open(filename, "wb") as out:
        out.write(audio_content)
    print(f"\nAudio guardado como {filename}")

# Función para determinar si el texto termina en un límite natural
def is_sentence_boundary(text):
    """Determina si el texto termina en un límite de oración."""
    return bool(re.search(r'[.!?;:,]\s*$', text))

# Función que envía las respuestas del modelo a Google TTS
async def send_to_tts(text_chunk):
    """Envía un fragmento de texto al servicio de TTS de Google."""
    try:
        # Crear la solicitud de entrada con el texto
        input_request = texttospeech.SynthesisInput(text=text_chunk)
        
        # Crear la solicitud de configuración de voz
        voice = texttospeech.VoiceSelectionParams(name="es-ES-Neural2-A", language_code="es-ES")
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        # Realizar la solicitud de síntesis
        response = client.synthesize_speech(input=input_request, voice=voice, audio_config=audio_config)
        
        # Guardar el audio en un archivo
        filename = f"audio_{int(time.time())}.mp3"
        await save_audio_to_file(response.audio_content, filename)
    except Exception as e:
        print(f"\nError en TTS: {str(e)}")

# Función principal que genera un "stream" de texto con buffering y lo envía a TTS
async def stream_joke_and_tts(topic, min_words=4):
    """
    Genera un chiste sobre un tema y lo sintetiza con voz usando buffering.
    
    Args:
        topic: El tema sobre el que generar el contenido
        min_words: Mínimo de palabras antes de enviar a TTS (default: 4)
    """
    print(f"Generando una broma sobre {topic} con mínimo {min_words} palabras por fragmento...\n")
    
    # Buffer para acumular texto
    buffer = ""
    
    try:
        # Procesar el stream
        async for event in chain.astream_events({"topic": topic}):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                # Obtener el nuevo fragmento de texto
                new_text = event["data"]["chunk"].content
                buffer += new_text
                
                # Contar palabras en el buffer
                current_words = len(buffer.split())
                
                # Mostrar el progreso
                print(new_text, end="", flush=True)
                
                # Procesar si tenemos suficientes palabras o hay un límite natural de oración
                if current_words >= min_words and (is_sentence_boundary(buffer) or current_words >= min_words*2):
                    print(f"\n[Enviando {current_words} palabras a TTS]: {buffer}")
                    
                    # Enviar a TTS
                    await send_to_tts(buffer)
                    
                    # Reiniciar buffer
                    buffer = ""
        
        # Procesar cualquier texto restante en el buffer
        if buffer.strip():
            print(f"\n[Enviando {len(buffer.split())} palabras restantes a TTS]: {buffer}")
            await send_to_tts(buffer)
            
    except Exception as e:
        print(f"\nError: {str(e)}")
    
    print("\nProcesamiento completado")

# Ejecutar el código
if __name__ == "__main__":
    try:
        topic = input("Introduce un tema para la broma: ")
        min_words = input("Mínimo de palabras por fragmento (default 4): ")
        min_words = int(min_words) if min_words.isdigit() else 4
        
        asyncio.run(stream_joke_and_tts(topic, min_words))
    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario")