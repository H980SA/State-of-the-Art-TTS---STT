#!/usr/bin/env python
# Copyright 2024 Google LLC

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from google.cloud import texttospeech
import os
import asyncio
import re
import pyaudio
import queue
import threading
import time

# Cargar variables de entorno
load_dotenv()

# Configuración del modelo GPT-4
model = ChatOpenAI(model="gpt-4o-mini-2024-07-18")
template = "Eres un asistente que guiará al estudiante en el laboratorio de materiales y quiero que hables del siguiente tema :{topic}, sé lo más coloquial posible sin usar ** o ## o -"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", template), ("user", "{topic}")]
)
parser = StrOutputParser()
chain = prompt_template | model | parser

# Configuración de Google TTS
client = texttospeech.TextToSpeechClient()

# Colas para comunicación entre hilos
text_queue = queue.Queue(maxsize=10)
audio_queue = queue.Queue(maxsize=10)

# Configuración de audio
p = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 24000

def tts_worker():
    """Hilo para síntesis de TTS"""
    while True:
        text_chunk = text_queue.get()
        if text_chunk is None:
            audio_queue.put(None)
            break
        
        try:
            input_text = texttospeech.SynthesisInput(text=text_chunk)
            voice = texttospeech.VoiceSelectionParams(
                language_code="es-ES",
                name="es-ES-Neural2-A"
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                sample_rate_hertz=RATE
            )
            
            response = client.synthesize_speech(
                input=input_text,
                voice=voice,
                audio_config=audio_config
            )
            
            if response.audio_content:
                # Dividir el audio en chunks más pequeños para reproducción suave
                chunk_size = 4096
                for i in range(0, len(response.audio_content), chunk_size):
                    audio_chunk = response.audio_content[i:i+chunk_size]
                    audio_queue.put(audio_chunk)
        
        except Exception as e:
            print(f"Error en TTS: {str(e)}")
        
        text_queue.task_done()

def audio_worker():
    """Hilo para reproducción continua de audio"""
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        output=True,
        start=False
    )
    stream.start_stream()
    
    while True:
        audio_chunk = audio_queue.get()
        if audio_chunk is None:
            break
        
        try:
            stream.write(audio_chunk)
        except Exception as e:
            print(f"Error en audio: {str(e)}")
        
        audio_queue.task_done()
    
    stream.stop_stream()
    stream.close()

async def stream_joke_and_tts(topic, min_words=4):
    """Genera el chiste y coordina los hilos"""
    print(f"\nGenerando broma sobre {topic}...")
    
    # Iniciar hilos
    tts_thread = threading.Thread(target=tts_worker, daemon=True)
    audio_thread = threading.Thread(target=audio_worker, daemon=True)
    tts_thread.start()
    audio_thread.start()
    
    buffer = ""
    try:
        async for event in chain.astream_events({"topic": topic}):
            if event["event"] == "on_chat_model_stream":
                new_text = event["data"]["chunk"].content
                print(new_text, end="", flush=True)
                buffer += new_text
                
                if len(buffer.split()) >= min_words and is_sentence_boundary(buffer):
                    # Enviar chunk al hilo de TTS
                    text_queue.put(buffer)
                    buffer = ""
        
        # Procesar buffer residual
        if buffer.strip():
            text_queue.put(buffer)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        # Señales de terminación
        text_queue.put(None)
        text_queue.join()
        audio_queue.join()
        
        # Esperar a que termine la cola de audio
        while not audio_queue.empty():
            time.sleep(0.1)

def is_sentence_boundary(text):
    """Detecta límites naturales de oración"""
    return bool(re.search(r'[.!?;:,]\s*$', text))

if __name__ == "__main__":
    try:
        topic = input("Introduce un tema del laboratorio: ")
        asyncio.run(stream_joke_and_tts(topic))
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario")
    finally:
        p.terminate()