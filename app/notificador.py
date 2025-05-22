# app/notificador.py

import os
import logging
import urllib.parse
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

    mensagem_automatica = (
        f"Olá, tudo bem? 😊\n"
        f"Sou da equipe E-Vitrine e vi que você demonstrou interesse em nossos serviços. "
        f"Estou aqui para te ajudar! 💬"
    )

    numero_limpo = user_info["numero"].replace("whatsapp:", "")
    texto_codificado = urllib.parse.quote(mensagem_automatica)
    link_whatsapp = f"https://wa.me/{numero_limpo}?text={texto_codificado}"

    mensagem = (
        f"📩 *Novo lead gerado!*\n\n"
        f"📱 Número: {numero_limpo}\n"
        f"📌 Estado: {user_info['estado']}\n"
        f"🎯 Serviço: {user_info['servico']}\n"
        f"🗺️ Rota: {user_info['rota']}\n\n"
        f"👉 Para iniciar a conversa com o cliente, clique no link abaixo:\n"
        f"{link_whatsapp}"
    )

    try:
        client.messages.create(
            from_=TWILIO_NUMBER,
            to=ATENDENTE_NUMBER,
            body=mensagem
        )
    except Exception as e:
        logger.error(f"Erro ao notificar atendente: {e}")
