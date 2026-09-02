import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# =============================================
# CONFIGURACION - Rellena estos valores
# =============================================
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "mi_token_secreto_123")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "EAATfSZAIxd48BScJlFrNOEASaBpk4txZCmd8ZCblB9ZBEYzLX7EX5mKxKMrdr2xHWUgku5jPvgpdPf9RYYe3yX1ZBKPGFQ9tgupwh66pJ2x1IVtwZCTpQptgaxxM4ThCoqZATko4U1hVMJdFubjOp6DaZClefiRg1oCkgZBkQaMS3si7kGL1Ph6WqVA0Wg61oU7vtWPSGXQZDZD")  # Lo obtienes de Meta for Developers
# =============================================


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
    """Logica principal para responder mensajes."""
    if "text" in message:
        text = message["text"].lower()
        print(f"Mensaje recibido de {sender_id}: {text}")

        # --- Define aqui las respuestas de tu bot ---
        if "hola" in text or "hello" in text:
            send_message(sender_id, "Hola! Soy un bot. En que puedo ayudarte?")
        elif "ayuda" in text or "help" in text:
            send_message(sender_id, "Puedo responder mensajes basicos. Intenta saludarme!")
        elif "adios" in text or "bye" in text:
            send_message(sender_id, "Hasta luego! Fue un placer charlar contigo.")
        else:
            # Respuesta por defecto: eco (repite el mensaje)
            send_message(sender_id, f"Recibi tu mensaje: '{message['text']}'")


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """Facebook verifica el webhook con una solicitud GET."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verificado correctamente!")
        return challenge, 200
    else:
        print("Error de verificacion del webhook.")
        return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def receive_message():
    """Recibe los eventos (mensajes) desde Facebook."""
    data = request.get_json()
    print(f"Evento recibido: {json.dumps(data, indent=2)}")

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]

                # Solo procesamos mensajes de texto (no eventos de lectura, etc.)
                if "message" in event and not event["message"].get("is_echo"):
                    handle_message(sender_id, event["message"])

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    print("Bot de Messenger iniciado en http://localhost:5000")
    app.run(port=5000, debug=True)
