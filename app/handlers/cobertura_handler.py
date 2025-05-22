# app/handlers/cobertura_handler.py

import logging
from app.menus import menu_principal, menu_cobertura_eventos, menu_congresso_feiras, menu_speakers, menu_final
from app.states import set_state, set_servico, set_rota
from app.notificador import notificar_atendente
from app.utils import messages

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
            return messages.voltando_menu + menu_principal()
        else:
            return messages.opcao_invalida

    if estado in ["congresso_feiras", "speakers"]:
        rotas = {
            "congresso_feiras": ["Fotos - Congresso & Feiras", "Vídeos - Congresso & Feiras", "Cobertura completa - Congresso & Feiras"],
            "speakers": ["Pré Release - Speakers", "Cobertura visual - Speakers"]
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
                return messages.voltando_anterior + menu_congresso_feiras()
            else:
                return messages.voltando_anterior + menu_speakers()
        else:
            return messages.opcao_invalida

    if estado.startswith("final_") and any(x in estado for x in ["congresso_feiras", "speakers"]):
        contexto = estado.replace("final_", "").replace("_", " ").title()
        if incoming_msg == "1":
            set_rota(user_number, f"Eventos - {contexto} - WhatsApp")
            notificar_atendente(user_number)
            set_state(user_number, "menu")
            return messages.contato_whatsapp + messages.voltando_menu + menu_principal()
        elif incoming_msg == "2":
            set_rota(user_number, f"Eventos - {contexto} - Ligação")
            notificar_atendente(user_number)
            set_state(user_number, "menu")
            return messages.contato_ligacao + messages.voltando_menu + menu_principal()
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "cobertura_eventos")
            return messages.voltando_anterior + menu_cobertura_eventos()
        else:
            return messages.opcao_invalida

    return messages.opcao_invalida
