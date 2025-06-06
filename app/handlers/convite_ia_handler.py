# app/handlers/convite_ia_handler.py

import logging
from app.menus import menu_principal, menu_ia
from app.states import set_state
from app.utils import messages

logger = logging.getLogger(__name__)

def handle(incoming_msg, user_number, estado):
    sim = ["sim", "s", "ss", "yes"]
    nao = ["não", "nao", "n", "no", "nn"]
    if estado == "convite_ia":
        if incoming_msg.lower() in sim:
            set_state(user_number, "ia")
            return "🎉 Que ótimo!\n\n" + menu_ia()
        elif incoming_msg.lower() in nao:
            set_state(user_number, "menu")
            return "👍 Sem problemas!\n\n" + messages.voltando_menu + menu_principal()
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "menu")
            return messages.voltando_menu + menu_principal()
        else:
            return "❓ Não entendi. Por favor, responda *SIM* ou *NÃO*."
