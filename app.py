import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "mi_token_secreto_123")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "")
API_URL = "https://graph.facebook.com/v18.0/me/messages"


def send_request(payload):
    response = requests.post(
        API_URL,
        params={"access_token": PAGE_ACCESS_TOKEN},
        headers={"Content-Type": "application/json"},
        json=payload
    )
    print(f"[FB API] Status: {response.status_code} | {response.text}")
    return response


def send_text(recipient_id, text):
    send_request({
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    })


def send_quick_replies(recipient_id, text, opciones):
    quick_replies = [
        {"content_type": "text", "title": op["title"], "payload": op["payload"]}
        for op in opciones
    ]
    send_request({
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {
            "text": text,
            "quick_replies": quick_replies
        }
    })


def send_buttons(recipient_id, text, botones):
    buttons = [
        {"type": "postback", "title": btn["title"], "payload": btn["payload"]}
        for btn in botones
    ]
    send_request({
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons": buttons
                }
            }
        }
    })


def menu_principal(sender_id):
    send_quick_replies(
        sender_id,
        "Hola! Bienvenido a Streaming Free. Que deseas hacer?",
        [
            {"title": "Ver catalogo", "payload": "CATALOGO"},
            {"title": "Precios",      "payload": "PRECIOS"},
            {"title": "Como comprar", "payload": "COMPRAR"},
            {"title": "Garantia",     "payload": "GARANTIA"},
        ]
    )


def menu_catalogo(sender_id):
    send_quick_replies(
        sender_id,
        "Elige una plataforma para ver detalles y precio:",
        [
            {"title": "Netflix",         "payload": "INFO_NETFLIX"},
            {"title": "Disney+",         "payload": "INFO_DISNEY"},
            {"title": "Max (HBO)",       "payload": "INFO_MAX"},
            {"title": "Prime Video",     "payload": "INFO_PRIME"},
            {"title": "Crunchyroll",     "payload": "INFO_CRUNCHYROLL"},
            {"title": "Menu principal",  "payload": "MENU"},
        ]
    )


def info_plataforma(sender_id, plataforma):
    datos = {
        "INFO_NETFLIX":     ("Netflix compartido\n1 pantalla: $3/mes\n2 pantallas: $5/mes\nAcceso inmediato.",     "Comprar Netflix",     "PEDIR_NETFLIX"),
        "INFO_DISNEY":      ("Disney+ compartido\n1 pantalla: $2/mes\nDisney, Marvel, Star Wars y mas.",          "Comprar Disney+",     "PEDIR_DISNEY"),
        "INFO_MAX":         ("Max (HBO) compartido\n1 pantalla: $2.50/mes\nSeries y peliculas exclusivas.",       "Comprar Max",         "PEDIR_MAX"),
        "INFO_PRIME":       ("Prime Video compartido\n1 pantalla: $2/mes\nContenido Amazon original.",            "Comprar Prime",       "PEDIR_PRIME"),
        "INFO_CRUNCHYROLL": ("Crunchyroll compartido\n1 pantalla: $1.50/mes\nTodo el anime disponible.",         "Comprar Crunchyroll", "PEDIR_CRUNCHYROLL"),
    }
    if plataforma in datos:
        texto, boton, payload = datos[plataforma]
        send_buttons(sender_id, texto, [
            {"title": boton,           "payload": payload},
            {"title": "Ver otras",     "payload": "CATALOGO"},
            {"title": "Menu principal","payload": "MENU"},
        ])


def iniciar_compra(sender_id, plataforma):
    nombres = {
        "PEDIR_NETFLIX": "Netflix", "PEDIR_DISNEY": "Disney+",
        "PEDIR_MAX": "Max (HBO)", "PEDIR_PRIME": "Prime Video",
        "PEDIR_CRUNCHYROLL": "Crunchyroll",
    }
    nombre = nombres.get(plataforma, "la plataforma")
    send_text(sender_id, f"Excelente! Para completar tu compra de {nombre}, un asesor te contactara con los datos de pago en breve.")
    send_quick_replies(
        sender_id,
        "Puedo ayudarte con algo mas?",
        [
            {"title": "Ver otras plataformas", "payload": "CATALOGO"},
            {"title": "Menu principal",         "payload": "MENU"},
        ]
    )


def handle_postback(sender_id, payload):
    print(f"[POSTBACK] {sender_id}: {payload}")
    if payload == "MENU":
        menu_principal(sender_id)
    elif payload == "CATALOGO":
        menu_catalogo(sender_id)
    elif payload == "PRECIOS":
        send_buttons(sender_id,
            "Nuestros precios:\nNetflix: desde $3/mes\nDisney+: desde $2/mes\nMax: desde $2.50/mes\nPrime: desde $2/mes\nCrunchyroll: desde $1.50/mes",
            [{"title": "Ver catalogo", "payload": "CATALOGO"}, {"title": "Menu principal", "payload": "MENU"}]
        )
    elif payload == "COMPRAR":
        send_text(sender_id, "Para comprar:\n1. Elige tu plataforma\n2. Te damos datos de pago\n3. Envias comprobante\n4. Recibes tu cuenta en minutos!")
        menu_catalogo(sender_id)
    elif payload == "GARANTIA":
        send_buttons(sender_id,
            "Garantia completa:\nReposicion en menos de 24h si la cuenta falla\nSoporte todos los dias\nClientes satisfechos desde 2022",
            [{"title": "Ver catalogo", "payload": "CATALOGO"}, {"title": "Menu principal", "payload": "MENU"}]
        )
    elif payload.startswith("INFO_"):
        info_plataforma(sender_id, payload)
    elif payload.startswith("PEDIR_"):
        iniciar_compra(sender_id, payload)


def handle_message(sender_id, message):
    if "text" in message:
        texto = message["text"].lower().strip()
        print(f"[MSG] {sender_id}: {texto}")
        saludos = ["hola", "hello", "buenas", "hi", "ey", "hey", "inicio", "start", "menu", "comenzar"]
        if any(s in texto for s in saludos):
            menu_principal(sender_id)
        else:
            send_quick_replies(sender_id, "Usa el menu para navegar:", [
                {"title": "Ver catalogo", "payload": "CATALOGO"},
                {"title": "Precios",      "payload": "PRECIOS"},
                {"title": "Como comprar", "payload": "COMPRAR"},
                {"title": "Garantia",     "payload": "GARANTIA"},
            ])


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                if "postback" in event:
                    handle_postback(sender_id, event["postback"]["payload"])
                elif "message" in event and not event["message"].get("is_echo"):
                    msg = event["message"]
                    if "quick_reply" in msg:
                        handle_postback(sender_id, msg["quick_reply"]["payload"])
                    else:
                        handle_message(sender_id, msg)
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    print("Bot con botones iniciado en http://localhost:5000")
    app.run(port=5000, debug=True)
