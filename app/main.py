# app/main.py

import logging
from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from .states import get_state
from .handlers import handle_message

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    user_number = request.values.get("From", "")
    logger.info(f"[MENSAGEM RECEBIDA] {user_number}: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    estado = get_state(user_number)
    resposta = handle_message(estado, incoming_msg, user_number)

    msg.body(resposta)
    logger.info(f"[RESPOSTA] {user_number}: {resposta}")
    return str(resp)
