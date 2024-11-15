# import whisper

# class Transcriber:
#     def __init__(self):
#         # Cargar el modelo Whisper - selecciona el modelo según tus necesidades (ej. 'base', 'small')
#         self.model = whisper.load_model("base")

#     def transcribe(self, audio):
#         try:
#             # Guardar el archivo de audio recibido
#             audio.save("audio.mp3")
            
#             # Transcribir el archivo MP3 directamente
#             result = self.model.transcribe("audio.mp3")
#             return result['text']
#         except Exception as e:
#             return ""
import openai

#Convertir audio en texto
class Transcriber:
    def __init__(self):
        pass
        
    #Siempre guarda y lee del archivo audio.mp3
    #Utiliza whisper en la nube :) puedes cambiarlo por una impl local
    def transcribe(self, audio):
        audio.save("audio.mp3")
        audio_file= open("audio.mp3", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript.text