import openai
import json

# Clase para utilizar cualquier LLM para procesar un texto
class LLM():
    def __init__(self):
        self.messages = [{"role": "system", "content": "Eres un asistente para negociaciones en el sector financiero."}]
        self.emotions_detected = []
        self.negotiation_terms = {"offer_amount": 0, "payment_plan": "", "success_level": ""}

    def process_functions(self, text):
        user_input = text

        # Si el usuario ingresa 'salir', terminamos la conversación
        if user_input.lower() == "salir":
            print("La conversación ha terminado.")
            return self.generate_report()

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
        return bot_response

    def generate_report(self):
        # Generar un reporte detallado basado en la conversación
        report = {
            "emotions_detected": self.emotions_detected,
            "negotiation_terms": self.negotiation_terms,
            "conversation": self.messages
        }
        return json.dumps(report, indent=4)