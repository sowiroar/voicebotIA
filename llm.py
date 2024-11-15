import openai
import json
from transformers import pipeline

# Cargar el modelo de análisis de sentimientos en español usando transformers
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Base de datos sintética de clientes
clientes = [
    {
        "ID_Cliente": "C001",
        "Nombre_Cliente": "Juan Pérez",
        "Fecha_Nacimiento": "1985-07-12",
        "Número_Documento": "12345678",
        "Teléfono_Contacto": "+5491155550001",
        "Correo_Electrónico": "juan.perez@example.com",
        "Monto_Deuda": 1500.00,
        "Fecha_Vencimiento": "2023-12-15",
        "Estado_Cuenta": "En mora",
        "Historial_Pagos": [{"fecha": "2023-09-10", "monto": 200}]
    },
    {
        "ID_Cliente": "C002",
        "Nombre_Cliente": "María González",
        "Fecha_Nacimiento": "1992-03-25",
        "Número_Documento": "87654321",
        "Teléfono_Contacto": "+5491155550002",
        "Correo_Electrónico": "maria.gonzalez@example.com",
        "Monto_Deuda": 2500.00,
        "Fecha_Vencimiento": "2023-10-20",
        "Estado_Cuenta": "Pendiente",
        "Historial_Pagos": [{"fecha": "2023-08-20", "monto": 300}]
    },
    {
        "ID_Cliente": "C003",
        "Nombre_Cliente": "Carlos Ramírez",
        "Fecha_Nacimiento": "1978-11-05",
        "Número_Documento": "11223344",
        "Teléfono_Contacto": "+5491155550003",
        "Correo_Electrónico": "carlos.ramirez@example.com",
        "Monto_Deuda": 1000.00,
        "Fecha_Vencimiento": "2023-11-10",
        "Estado_Cuenta": "Pagada",
        "Historial_Pagos": [{"fecha": "2023-07-15", "monto": 500}]
    }
]

# Clase para utilizar cualquier LLM para procesar un texto
class LLM():
    def __init__(self):
        self.messages = [{"role": "system", "content": "Eres un asistente para negociaciones en el sector financiero."}]
        self.emotions_detected = []
        self.negotiation_terms = {"offer_amount": 0, "payment_plan": "", "success_level": ""}
        self.cliente_actual = None
        self.acuerdo_negociado = False

    def buscar_cliente(self, nombre):
        for cliente in clientes:
            if cliente["Nombre_Cliente"].lower() == nombre.lower():
                return cliente
        return None

    def analizar_emociones(self, respuesta):
        resultado = sentiment_analyzer(respuesta)[0]
        sentimiento = "positivo" if resultado["label"] == "5 stars" else "negativo"
        emociones_detectadas = ["alegría"] if sentimiento == "positivo" else ["enojo"]
        return {"emociones": emociones_detectadas, "sentimiento": sentimiento, "score": resultado["score"]}

    def generar_informe(self):
        # Análisis de emociones y sentimientos en todos los mensajes
        analisis_emociones = self.analizar_emociones(" ".join([msg['content'] for msg in self.messages if msg['role'] == "user"]))

        # Calcular el número total de palabras y tokens
        total_palabras = sum(len(msg['content'].split()) for msg in self.messages if msg['role'] == "user")
        total_tokens = total_palabras  # Aproximación de tokens

        # Cálculo de costos
        costo_entrada = 0.15 * total_tokens / 1_000_000
        costo_salida = 0.60 * total_tokens / 1_000_000
        costo_total = costo_entrada + costo_salida

        # Crear el informe en formato diccionario
        informe = {
            "Sentimiento_Detectado": analisis_emociones["sentimiento"],
            "Emociones_Dominantes": analisis_emociones["emociones"],
            "Indicador_Negociacion": "100/100" if self.acuerdo_negociado else "0/100",
            "Costos_Estimados": {
                "Total_Palabras": total_palabras,
                "Total_Tokens": total_tokens,
                "Costo_Total": costo_total
            },
            "Cliente": self.cliente_actual
        }

        # Guardar el informe en un archivo JSON
        with open("informe_conversacion.json", "w") as json_file:
            json.dump(informe, json_file, indent=4)
        print("Informe guardado como informe_conversacion.json")
        print(informe)

    def process_functions(self, text):
        user_input = text

        # Si el usuario ingresa 'salir', terminamos la conversación
        if user_input.lower() == "salir":
            print("La conversación ha terminado.")
            self.generar_informe()
            return "Informe generado y guardado como JSON."

        # Intentar identificar al cliente si no se ha hecho aún
        if self.cliente_actual is None:
            palabras = user_input.lower().split()
            for palabra in palabras:
                self.cliente_actual = self.buscar_cliente(palabra.capitalize())
                if self.cliente_actual:
                    print(f"Cliente identificado: {self.cliente_actual['Nombre_Cliente']}. Monto de la deuda: ${self.cliente_actual['Monto_Deuda']}.")
                    break

        # Agregar el mensaje del usuario a la conversación
        self.messages.append({"role": "user", "content": user_input})

        # Llamada a la API para obtener la respuesta del chatbot
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=self.messages,
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            tools=[{
                "type": "function",
                "function": {
                    "name": "handle_call",
                    "description": "Eres un chatbot que simula una llamada de un cliente en el contexto de una negociación de pago en el sector financiero. Deberás ser capaz de comprender el contexto de la conversación, gestionar las emociones del cliente y negociar un acuerdo de pago. Al finalizar cada llamada, deberás generar un análisis detallado que incluya los sentimientos y emociones detectados durante la conversación, el nivel de éxito de la negociación y los costos asociados al acuerdo alcanzado.",
                    "parameters": {
                        "type": "object",
                        "required": [
                            "call_context",
                            "customer_emotions",
                            "negotiation_terms"
                        ],
                        "properties": {
                            "call_context": {
                                "type": "object",
                                "properties": {
                                    "customer_id": {"type": "string"},
                                    "inquiry_type": {"type": "string"}
                                },
                                "additionalProperties": False,
                                "required": ["customer_id", "inquiry_type"]
                            },
                            "customer_emotions": {
                                "type": "array",
                                "items": {"type": "string", "enum": ["happy", "angry", "frustrated", "confused", "satisfied"]}
                            },
                            "negotiation_terms": {
                                "type": "object",
                                "properties": {
                                    "offer_amount": {"type": "number"},
                                    "payment_plan": {"type": "string"},
                                    "success_level": {"type": "string"}
                                },
                                "additionalProperties": False,
                                "required": ["offer_amount", "payment_plan", "success_level"]
                            }
                        },
                        "additionalProperties": False
                    }
                }
            }],
            parallel_tool_calls=True,
            response_format={"type": "text"}
        )

        # Obtener y mostrar la respuesta del chatbot
        bot_response = response['choices'][0]['message']['content']
        self.messages.append({"role": "assistant", "content": bot_response})

        # Verificar si el bot ha hecho una oferta de pago
        if "ofrecemos un plan de pago" in bot_response.lower():
            self.acuerdo_negociado = True

        return bot_response