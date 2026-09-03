import os
import json
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify
from respuestas import RESPUESTAS, RESPUESTA_DEFAULT

app = Flask(__name__)

# =============================================
# CONFIGURACION - Variables de entorno en Render
# =============================================
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "mi_token_secreto_123")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
# =============================================

# Configurar Gemini si hay API key
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    modelo_ia = genai.GenerativeModel("gemini-1.5-flash")
else:
    modelo_ia = None

CONTEXTO_BOT = """
Eres un asistente de ventas de cuentas de streaming compartidas para la tienda "Streaming Free".
Vendes: Netflix, Disney+, Max (HBO), Prime Video y Crunchyroll a precios economicos.
Responde siempre en espanol, de forma breve, amigable y enfocada en ayudar al cliente a comprar.
Si no sabes algo especifico, di que un asesor los contactara pronto.
"""


def buscar_respuesta_fija(texto):
    """Busca si el mensaje coincide con alguna palabra clave del diccionario."""
    texto = texto.lower().strip()
    for palabras_clave, respuesta in RESPUESTAS.items():
        for palabra in palabras_clave:
            if palabra in texto:
                return respuesta
    return None


def preguntar_ia(texto):
    """Usa Gemini como respaldo si no hay respuesta fija."""
    if not modelo_ia:
        return RESPUESTA_DEFAULT
    try:
        prompt = f"{CONTEXTO_BOT}\n\nCliente dice: {texto}"
        respuesta = modelo_ia.generate_content(prompt)
        return respuesta.text
    except Exception as e:
        print(f"Error con Gemini: {e}")
        return RESPUESTA_DEFAULT


def send_message(recipient_id, message_text):
    """Envia un mensaje de texto al usuario."""
    url = "https://graph.facebook.com/v18.0/me/messages"
    headers = {"Content-Type": "application/json"}
    params = {"access_token": PAGE_ACCESS_TOKEN}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(url, headers=headers, params=params, json=payload)
    if response.status_code != 200:
        print(f"Error al enviar mensaje: {response.text}")
    return response


def handle_message(sender_id, message):
    """Logica principal: primero busca respuesta fija, luego usa IA."""
    if "text" in message:
        texto = message["text"]
        print(f"Mensaje de {sender_id}: {texto}")

        # 1. Buscar respuesta fija
        respuesta = buscar_respuesta_fija(texto)

        # 2. Si no hay, usar IA de Gemini
        if not respuesta:
            print("Sin respuesta fija, usando IA...")
            respuesta = preguntar_ia(texto)

        send_message(sender_id, respuesta)


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verificado!")
        return challenge, 200
    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                if "message" in event and not event["message"].get("is_echo"):
                    handle_message(sender_id, event["message"])

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    print("Bot de Streaming iniciado en http://localhost:5000")
    app.run(port=5000, debug=True)
