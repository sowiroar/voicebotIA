import openai
from flask import Flask, render_template, request, jsonify
import json
from transcriber import Transcriber
from llm import LLM
from tts import TTS

# #Cargar llaves del archivo .env
openai.api_key = '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'
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("recorder.html")

@app.route("/audio", methods=["POST"])
def audio():
    try:
        # Obtener audio grabado y transcribirlo
        audio = request.files.get("audio")
        text = Transcriber().transcribe(audio)
        
        # Utilizar el LLM para generar un análisis detallado
        llm = LLM()
        response = llm.process_functions(text)
        
        # Procesar la respuesta del LLM
        if response:
            tts = TTS()
            print(response)
            tts_file = tts.process(response)
            return jsonify({"result": "ok", "text": response, "file": tts_file})
        else:
            final_response = "No se pudo generar un análisis detallado."
            tts = TTS()
            tts_file = tts.process(final_response)
            return jsonify({"result": "ok", "text": final_response, "file": tts_file})
    except Exception as e:
        return jsonify({"result": "error", "message": str(e)})
