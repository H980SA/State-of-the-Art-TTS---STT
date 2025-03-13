import os
import requests
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

class GoogleTTS:
    """
    A class for Google Text-to-Speech using the REST API with API key
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the Google TTS with API key
        
        Args:
            api_key (str): Google API key, defaults to one from environment variables
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.base_url = "https://texttospeech.googleapis.com/v1/text:synthesize"
    
    def synthesize(self, text, language_code="es-ES", voice_name="es-ES-Neural2-A", 
                   audio_encoding="MP3", speaking_rate=1.0, pitch=0):
        """
        Synthesize speech from text using Google Cloud Text-to-Speech
        
        Args:
            text (str): Text to convert to speech
            language_code (str): Language code for the voice
            voice_name (str): Voice name to use
            audio_encoding (str): Format for the output audio (MP3, LINEAR16, etc.)
            speaking_rate (float): Speed of speech (0.25 to 4.0)
            pitch (int): Voice pitch (-20 to 20)
            
        Returns:
            bytes: Audio data in the specified format or None if error
        """
        if not self.api_key:
            print("API key not available")
            return None
            
        try:
            # Prepare request payload
            payload = {
                "input": {"text": text},
                "voice": {
                    "languageCode": language_code,
                    "name": voice_name
                },
                "audioConfig": {
                    "audioEncoding": audio_encoding,
                    "speakingRate": speaking_rate,
                    "pitch": pitch
                }
            }
            
            # Make API request
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                json=payload
            )
            
            # Check if request was successful
            if response.status_code == 200:
                audio_content = base64.b64decode(response.json()["audioContent"])
                return audio_content
            else:
                print(f"Error from Google TTS API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error synthesizing speech: {e}")
            return None
    
    def synthesize_to_file(self, text, output_file, language_code="es-ES", 
                           voice_name="es-ES-Chirp-HD-D", audio_encoding="MP3",
                           speaking_rate=1.0, pitch=0):
        """
        Synthesize speech and save to file
        
        Args:
            text (str): Text to convert to speech
            output_file (str): Path to save the audio file
            language_code (str): Language code for the voice
            voice_name (str): Voice name to use
            audio_encoding (str): Format for the output audio (MP3, LINEAR16, etc.)
            speaking_rate (float): Speed of speech (0.25 to 4.0)
            pitch (int): Voice pitch (-20 to 20)
            
        Returns:
            bool: True if successful, False otherwise
        """
        audio_content = self.synthesize(text, language_code, voice_name, 
                                        audio_encoding, speaking_rate, pitch)
        
        if audio_content:
            try:
                with open(output_file, "wb") as out:
                    out.write(audio_content)
                return True
            except Exception as e:
                print(f"Error writing audio to file: {e}")
                return False
        return False
    
    def list_voices(self, language_code=None):
        """
        List available voices, optionally filtered by language code
        
        Args:
            language_code (str): Optional language code to filter voices
            
        Returns:
            list: List of available voice names or empty list if error
        """
        if not self.api_key:
            print("API key not available")
            return []
            
        try:
            url = f"https://texttospeech.googleapis.com/v1/voices?key={self.api_key}"
            if language_code:
                url += f"&languageCode={language_code}"
                
            response = requests.get(url)
            
            if response.status_code == 200:
                voices = []
                for voice in response.json().get("voices", []):
                    for language_code in voice.get("languageCodes", []):
                        voices.append({
                            'name': voice.get("name"),
                            'language_code': language_code,
                            'ssml_gender': voice.get("ssmlGender")
                        })
                return voices
            else:
                print(f"Error from Google TTS API: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"Error listing voices: {e}")
            return []


# Example usage
if __name__ == "__main__":
    tts = GoogleTTS()
    
    # Example 1: Convert text to speech and save to file
    text = "Hola que tal me llamo Mateo y hoy seré tu asistente para este laboratorio"
    output_file = "google.mp3"
    
    if tts.synthesize_to_file(text, output_file):
        print(f"Audio guardado en {output_file}")
    else:
        print("Error al generar el audio")
    
    # # Example 2: List available voices
    # print("\nVoces disponibles en español:")
    # voices = tts.list_voices(language_code="es")
    # for voice in voices[:20]:  # Show first 5 voices
    #     print(f"{voice['name']} ({voice['language_code']}) - {voice['ssml_gender']}")
