# app/handlers/menu_handler.py

import logging
from app.menus import menu_principal, menu_cobertura_eventos, menu_md_humanos, menu_md_veterinarios, menu_ia
from app.states import set_state
from app.utils import messages

logger = logging.getLogger(__name__)

def handle(incoming_msg, user_number):
    saudacoes = ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "opa", "oie", "salve", "menu"]
    msg_lower = incoming_msg.lower()
    if any(saudacao in msg_lower for saudacao in saudacoes):
        set_state(user_number, "menu")
        return menu_principal()
    elif incoming_msg == "1":
        set_state(user_number, "cobertura_eventos")
        return menu_cobertura_eventos()
    elif incoming_msg == "2":
        set_state(user_number, "md_humanos")
        return menu_md_humanos()
    elif incoming_msg == "3":
        set_state(user_number, "md_veterinarios")
        return menu_md_veterinarios()
    elif incoming_msg == "4":
        set_state(user_number, "ia")
        return menu_ia()
    else:
        set_state(user_number, "menu")
        return messages.opcao_invalida + menu_principal()
