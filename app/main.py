# app/main.py

import logging
from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from .handlers import ia_handler, menu_handler, cobertura_handler, md_humanos_handler, md_veterinarios_handler
from app.states import get_state

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def enviar_resposta(msg_obj, user_number, texto):
    logger.info(f"[RESPOSTA] {user_number}: {texto}")
    msg_obj.body(texto)

def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    user_number = request.values.get("From", "")
    logger.info(f"[MENSAGEM RECEBIDA] {user_number}: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    estado = get_state(user_number)

    # Dispatch para o handler apropriado com base no estado
    if estado == "ia":
        resposta = ia_handler.handle(incoming_msg, user_number)
    elif estado == "menu":
        resposta = menu_handler.handle(incoming_msg, user_number)
    elif estado in ["cobertura_eventos", "congresso_feiras", "speakers"] or (estado.startswith("final_") and any(x in estado for x in ["congresso_feiras", "speakers"])):
        resposta = cobertura_handler.handle(incoming_msg, user_number, estado)
    elif estado in ["md_humanos", "fotos_humanos", "redes_humanos", "eventos_humanos"] or (estado.startswith("final_") and "humanos" in estado):
        resposta = md_humanos_handler.handle(incoming_msg, user_number, estado)
    elif estado in ["md_veterinarios", "fotos_veterinarios", "redes_veterinarios", "eventos_veterinarios"] or (estado.startswith("final_") and "veterinarios" in estado):
        resposta = md_veterinarios_handler.handle(incoming_msg, user_number, estado)
    else:
        resposta = "❌ Estado não reconhecido."

    enviar_resposta(msg, user_number, resposta)
    return str(resp)
