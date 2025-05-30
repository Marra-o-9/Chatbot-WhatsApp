# app/utils/main.py

import logging
from app.handlers import (
    ia_handler,
    menu_handler,
    cobertura_handler,
    md_humanos_handler,
    md_veterinarios_handler,
)
from app.states import get_state

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_message(user_id, incoming_msg, canal="whatsapp"):
    logger.info(f"[{canal.upper()} RECEBIDA] {user_id}: {incoming_msg}")

    estado = get_state(user_id)

    if estado == "ia":
        resposta = ia_handler.handle(incoming_msg, user_id)
    elif estado == "menu":
        resposta = menu_handler.handle(incoming_msg, user_id)
    elif estado in ["cobertura_eventos", "congresso_feiras", "speakers"] or (
        estado.startswith("final_") and any(x in estado for x in ["congresso_feiras", "speakers"])
    ):
        resposta = cobertura_handler.handle(incoming_msg, user_id, estado)
    elif estado in ["md_humanos", "fotos_humanos", "redes_humanos", "eventos_humanos"] or (
        estado.startswith("final_") and "humanos" in estado
    ):
        resposta = md_humanos_handler.handle(incoming_msg, user_id, estado)
    elif estado in ["md_veterinarios", "fotos_veterinarios", "redes_veterinarios", "eventos_veterinarios"] or (
        estado.startswith("final_") and "veterinarios" in estado
    ):
        resposta = md_veterinarios_handler.handle(incoming_msg, user_id, estado)
    else:
        resposta = "❌ Estado não reconhecido."

    logger.info(f"[RESPOSTA {canal.upper()}] {user_id}: {resposta}")
    return resposta
