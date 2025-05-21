# app/handlers/cobertura_handler.py

import logging
from app.menus import menu_cobertura_eventos, menu_congresso_feiras, menu_speakers, menu_final
from app.states import set_state

logger = logging.getLogger(__name__)

def handle(incoming_msg, user_number, estado):
    # Fluxo para o estado cobertura de eventos
    if estado == "cobertura_eventos":
        if incoming_msg == "1":
            set_state(user_number, "congresso_feiras")
            return menu_congresso_feiras()
        elif incoming_msg == "2":
            set_state(user_number, "speakers")
            return menu_speakers()
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "menu")
            return "🔙 Voltando ao menu principal...\n\n" + menu_cobertura_eventos()
        else:
            return "❌ Opção inválida. Escolha 1 ou 2, ou digite *VOLTAR*."

    # Fluxo para congresso/feiras
    if estado == "congresso_feiras":
        rotas = {
            "1": "Fotos - Congresso & Feiras",
            "2": "Vídeos - Congresso & Feiras",
            "3": "Cobertura completa - Congresso & Feiras"
        }
        if incoming_msg in rotas:
            set_state(user_number, "final_congresso_feiras")
            return menu_final(rotas[incoming_msg])
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "cobertura_eventos")
            return "🔙 Voltando ao menu anterior...\n\n" + menu_congresso_feiras()
        else:
            return "❌ Opção inválida. Escolha 1, 2 ou 3, ou digite *VOLTAR*."

    # Fluxo para speakers
    if estado == "speakers":
        rotas = {
            "1": "Pré Reels - Speakers",
            "2": "Cobertura visual - Speakers"
        }
        if incoming_msg in rotas:
            set_state(user_number, "final_speakers")
            return menu_final(rotas[incoming_msg])
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "cobertura_eventos")
            return "🔙 Voltando ao menu anterior...\n\n" + menu_speakers()
        else:
            return "❌ Opção inválida. Escolha 1 ou 2, ou digite *VOLTAR*."

    return "❌ Opção inválida."
