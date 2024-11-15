import openai
from flask import Flask, render_template, request, jsonify
import json
from transcriber import Transcriber
from llm import LLM
from tts import TTS

# Cargar llaves del archivo .env
openai.api_key = ''
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

@app.route("/end_call", methods=["POST"])
def end_call():
    try:
        print("Solicitud recibida en /end_call")
        # Utilizar el LLM para generar el informe
        llm = LLM()
        response = llm.process_functions("salir")
        
        # Leer el informe generado
        with open("informe_conversacion.json", "r") as json_file:
            informe = json.load(json_file)
        
        print("Informe generado:", informe)
        return jsonify({"result": "ok", "informe": informe})
    except Exception as e:
        print("Error al generar el informe:", e)
        return jsonify({"result": "error", "message": str(e)})
