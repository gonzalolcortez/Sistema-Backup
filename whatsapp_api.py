import os
import logging
import requests


TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")

logger = logging.getLogger(__name__)


def enviar_whatsapp(numero, mensaje):
    """Send a WhatsApp message via the Meta WhatsApp Cloud API.

    Args:
        numero: Destination phone number in E.164 format (e.g. '5491123456789').
        mensaje: Plain-text body of the message.

    Returns:
        The JSON response from the API, or None if credentials are missing or on error.
    """
    if not TOKEN or not PHONE_ID:
        logger.warning("[WhatsApp] WHATSAPP_TOKEN o WHATSAPP_PHONE_ID no configurados. Mensaje no enviado.")
        return None

    url = f"https://graph.facebook.com/v22.0/{PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }
    body = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {
            "body": mensaje,
        },
    }

    try:
        response = requests.post(url, json=body, headers=headers, timeout=10)
        data = response.json()
        message_id = data.get("messages", [{}])[0].get("id", "N/A") if response.ok else "N/A"
        logger.info("[WhatsApp] Respuesta de la API: status=%s, message_id=%s", response.status_code, message_id)
        response.raise_for_status()
        return data
    except requests.exceptions.RequestException as e:
        logger.error("[WhatsApp] Error al enviar mensaje: %s", e)
        return None
