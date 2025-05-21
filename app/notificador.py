# app/notificador.py

import os
import logging
from twilio.rest import Client
from app.states import get_user_info

logger = logging.getLogger(__name__)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
ATENDENTE_NUMBER = os.getenv("ATENDENTE_NUMBER")

def notificar_atendente(user_number):
    user_info = get_user_info(user_number)
    if not user_info:
        logger.warning(f"Não foi possível obter dados do cliente {user_number} para notificar atendente.")
        return

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    mensagem = (
        f"📩 *Novo lead gerado!*\n\n"
        f"📱 Número: {user_info['numero']}\n"
        f"📌 Estado: {user_info['estado']}\n"
        f"🎯 Serviço: {user_info['servico']}\n"
        f"🗺️ Rota: {user_info['rota']}"
    )

    try:
        client.messages.create(
            from_=TWILIO_NUMBER,
            to=ATENDENTE_NUMBER,
            body=mensagem
        )
    except Exception as e:
        logger.error(f"Erro ao notificar atendente: {e}")

