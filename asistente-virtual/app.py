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