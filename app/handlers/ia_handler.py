# app/handlers/ia_handler.py

import logging
from app.menus import menu_principal
from app.states import set_state
from app.rag import iniciar_rag
from app.utils import messages
from app import session

logger = logging.getLogger(__name__)
qa_chain = iniciar_rag()

MAX_CHARACTERS = 1500

def split_message(message, max_length):
    return [message[i:i+max_length] for i in range(0, len(message), max_length)]

def handle(incoming_msg, user_number):
    incoming_msg = incoming_msg.strip().upper()

    if incoming_msg == "VOLTAR":
        set_state(user_number, "menu")
        session.clear_session(user_number)
        resposta = messages.voltando_menu + menu_principal()
        logger.info(f"[IA] {user_number}: {resposta}")
        return resposta

    if incoming_msg == "CONTINUAR":
        next_part = session.get_next_part(user_number)
        if next_part:
            next_part = "➡️ *Continuação:*\n\n" + next_part
            if not session.has_more_parts(user_number):
                session.clear_session(user_number)
                next_part += "\n\n✅ Fim da resposta.\n\nDigite sua pergunta ou *VOLTAR* para retornar ao menu."
            else:
                next_part += "\n\n➡️ Digite *CONTINUAR* para mais ou *VOLTAR* para retornar ao menu."
            logger.info(f"[IA-Continue] {user_number}: {next_part}")
            return next_part

    # Nova pergunta ao chatbot
    prompt = (
        "Você é um chatbot inteligente da empresa de marketing digital E-Vitrine. "
        "Responda com clareza e objetividade como um especialista. "
        f"Pergunta do cliente: {incoming_msg}"
    )

    resposta_ia = qa_chain.invoke({"query": prompt})["result"]

    resposta_completa = "🤖 _*Chatbot E-Vitrine*_: \n\n" + resposta_ia
    partes = split_message(resposta_completa, MAX_CHARACTERS)

    # Se só tiver uma parte, envia tudo
    if len(partes) == 1:
        resposta = partes[0] + "\n\nDigite sua pergunta ou *VOLTAR* para retornar ao menu."
        logger.info(f"[IA] {user_number}: {resposta}")
        return resposta

    # Mais de uma parte, armazena o restante
    session.set_response_parts(user_number, partes[1:])
    resposta = partes[0] + "\n\n➡️ Digite *CONTINUAR* para mais ou *VOLTAR* para retornar ao menu."

    logger.info(f"[IA] {user_number}: {resposta}")
    return resposta
