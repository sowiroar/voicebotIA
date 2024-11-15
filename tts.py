import os
import requests

# Texto a voz. Esta impl utiliza ElevenLabs
class TTS():
    def __init__(self):
        self.key = 'sk_4037a10fcbc06e8e1e8653ff8cb804c84fc85a078bffcd53'
    
    def process(self, text):
        CHUNK_SIZE = 1024
        # Utiliza la voz clonada con el ID proporcionado
        # url = "https://api.elevenlabs.io/v1/text-to-speech/BxN7zlH0BixwSekY7lQm"
        url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.key
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.55
            }
        }

        # Nombre de archivo constante
        file_name = "response.mp3"
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open("static/" + file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
            return file_name
        else:
            raise Exception(f"Error in TTS API call: {response.status_code} - {response.text}")