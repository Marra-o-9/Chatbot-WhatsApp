# app/handlers/md_veterinarios_handler.py

import logging
from app.menus import menu_principal, menu_md_veterinarios, menu_fotos_videos, menu_redes, menu_eventos, menu_final
from app.states import set_state, set_rota, set_servico
from app.notificador import notificar_atendente
from app.utils import messages

logger = logging.getLogger(__name__)

def handle(incoming_msg, user_number, estado):
    if estado == "md_veterinarios":
        if incoming_msg == "1":
            set_state(user_number, "fotos_veterinarios")
            return menu_fotos_videos("Médicos Veterinários")
        elif incoming_msg == "2":
            set_state(user_number, "redes_veterinarios")
            return menu_redes("Médicos Veterinários")
        elif incoming_msg == "3":
            set_state(user_number, "eventos_veterinarios")
            return menu_eventos("Médicos Veterinários")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "menu")
            return messages.voltando_menu + menu_principal()
        else:
            set_state(user_number, "menu")
            return messages.opcao_invalida + menu_principal()

    if estado in ["fotos_veterinarios", "redes_veterinarios", "eventos_veterinarios"]:
        rotas = {
            "fotos_veterinarios": ["Autoridade Veterinária", "Consultório Veterinário"],
            "redes_veterinarios": ["Posts + Monitoramento", "Posts + Fotos/Vídeos + Monitoramento"],
            "eventos_veterinarios": ["Cobertura de Evento", "Cobertura com Edição Imediata"]
        }
        if incoming_msg in ["1", "2"]:
            index = int(incoming_msg) - 1
            rota_nome = rotas[estado][index]
            set_servico(user_number, rota_nome)
            set_state(user_number, f"final_{estado}")
            return menu_final(f"{rota_nome} - Médicos Veterinários")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "md_veterinarios")
            return messages.voltando_anterior + menu_md_veterinarios()
        else:
            set_state(user_number, "menu")
            return messages.opcao_invalida + menu_principal()

    if estado.startswith("final_") and "veterinarios" in estado:
        contexto = estado.replace("final_", "").replace("_veterinarios", "").replace("_", " ").title()
        if incoming_msg == "1":
            set_rota(user_number, f"Médicos Veterinários - {contexto} - WhatsApp")
            notificar_atendente(user_number)
            set_state(user_number, "convite_ia")
            return messages.contato_whatsapp + messages.convite_ia
        elif incoming_msg == "2":
            set_rota(user_number, f"Médicos Veterinários - {contexto} - Ligação")
            notificar_atendente(user_number)
            set_state(user_number, "convite_ia")
            return messages.contato_ligacao + messages.convite_ia
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "md_veterinarios")
            return messages.voltando_anterior + menu_md_veterinarios()
        else:
            set_state(user_number, "menu")
            return messages.opcao_invalida + menu_principal()

    set_state(user_number, "menu")
    return messages.opcao_invalida + menu_principal()
