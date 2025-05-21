# app/handlers/menu_handler.py

import logging
from app.menus import menu_principal, menu_cobertura_eventos, menu_md_humanos, menu_md_veterinarios
from app.states import set_state

logger = logging.getLogger(__name__)

def handle(incoming_msg, user_number):
    saudacoes = ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]
    if incoming_msg.lower() in saudacoes:
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
        resposta = (
            "🤖 Você ativou o modo informativo com inteligência artificial.\n"
            "Sou um chatbot especializado da *E-Vitrine* pronto para tirar suas dúvidas sobre marketing digital.\n\n"
            "Digite sua pergunta ou *VOLTAR* para retornar ao menu."
        )
        return resposta
    else:
        return "❌ Opção inválida.\n\n" + menu_principal()
