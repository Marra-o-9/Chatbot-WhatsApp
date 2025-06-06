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
            set_state(user_number, "menu")
            return messages.opcao_invalida + menu_principal()

    if estado in ["congresso_feiras", "speakers"]:
        rotas = {
            "congresso_feiras": [
                "Cobertura de Eventos -> Congresso & Feiras -> Fotos",
                "Cobertura de Eventos -> Congresso & Feiras -> Vídeos",
                "Cobertura de Eventos -> Congresso & Feiras -> Cobertura de Fotos + Vídeos",
                "Cobertura de Eventos -> Congresso & Feiras -> Gestão de Redes Sociais"
            ],
            "speakers": [
                "Cobertura de Eventos -> Speakers -> Chamada de Pré Release Digital",
                "Cobertura de Eventos -> Speakers -> Cobertura do Speakers no Evento"
            ]
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
            return messages.voltando_anterior + (menu_congresso_feiras() if estado == "congresso_feiras" else menu_speakers())
        else:
            set_state(user_number, "menu")
            return messages.opcao_invalida + menu_principal()

    if estado.startswith("final_") and any(x in estado for x in ["congresso_feiras", "speakers"]):
        if incoming_msg == "1":
            set_rota(user_number, "Atendimento via WhatsApp")
            notificar_atendente(user_number)
            set_state(user_number, "convite_ia")
            return messages.contato_whatsapp(user_number) + messages.convite_ia
        elif incoming_msg == "2":
            set_rota(user_number, "Ligação Comercial")
            notificar_atendente(user_number)
            set_state(user_number, "convite_ia")
            return messages.contato_ligacao(user_number) + messages.convite_ia
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "cobertura_eventos")
            return messages.voltando_anterior + menu_cobertura_eventos()
        else:
            set_state(user_number, "menu")
            return messages.opcao_invalida + menu_principal()

    set_state(user_number, "menu")
    return messages.opcao_invalida + menu_principal()
