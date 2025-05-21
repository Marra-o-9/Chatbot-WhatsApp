# app/handlers/cobertura_handler.py

import logging
from app.menus import menu_principal, menu_cobertura_eventos, menu_congresso_feiras, menu_speakers, menu_final
from app.states import set_state, set_servico, set_rota

logger = logging.getLogger(__name__)

def handle(incoming_msg, user_number, estado):
    if estado == "cobertura_eventos":
        if incoming_msg == "1":
            set_state(user_number, "congresso_feiras")
            return menu_congresso_feiras()
        elif incoming_msg == "2":
            set_state(user_number, "speakers")
            return menu_speakers()
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "menu")
            return "🔙 Voltando ao menu principal...\n\n" + menu_principal()
        else:
            return "❌ Opção inválida."

    if estado in ["congresso_feiras", "speakers"]:
        rotas = {
            "congresso_feiras": ["Fotos - Congresso & Feiras", "Vídeos - Congresso & Feiras", "Cobertura completa - Congresso & Feiras"],
            "speakers": ["Pré Reels - Speakers", "Cobertura visual - Speakers"]
        }

        opcoes_validas = [str(i + 1) for i in range(len(rotas[estado]))]
        if incoming_msg in opcoes_validas:
            index = int(incoming_msg) - 1
            rota_nome = rotas[estado][index]
            set_servico(user_number, rota_nome)
            set_state(user_number, f"final_{estado}")
            return menu_final(rota_nome)
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "cobertura_eventos")
            if estado == "congresso_feiras":
                return "🔙 Voltando ao menu anterior...\n\n" + menu_congresso_feiras()
            else:
                return "🔙 Voltando ao menu anterior...\n\n" + menu_speakers()
        else:
            return "❌ Opção inválida."

    if estado.startswith("final_") and any(x in estado for x in ["congresso_feiras", "speakers"]):
        contexto = estado.replace("final_", "").replace("_", " ").title()
        if incoming_msg == "1":
            set_rota(user_number, f"{contexto} - WhatsApp - Eventos")
            return "📲 Em breve um consultor entrará em contato via WhatsApp."
        elif incoming_msg == "2":
            set_rota(user_number, f"{contexto} - Ligação - Eventos")
            return "📞 Nossa equipe fará uma ligação comercial para você."
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "cobertura_eventos")
            return "🔙 Voltando ao menu anterior...\n\n" + menu_cobertura_eventos()
        else:
            return "❌ Opção inválida."

    return "❌ Opção inválida."
