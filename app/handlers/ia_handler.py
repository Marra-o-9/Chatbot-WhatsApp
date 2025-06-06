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
    incoming_msg = incoming_msg.strip()

    if incoming_msg.upper() == "VOLTAR":
        set_state(user_number, "menu")
        session.clear_session(user_number)
        resposta = messages.voltando_menu + menu_principal()
        logger.info(f"[IA] {user_number}: {resposta}")
        return resposta

    if incoming_msg.upper() == "CONTINUAR":
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

    # ✅ Recupera histórico e adiciona ao prompt
    history = session.get_history(user_number)
    contexto = ""
    for h in history[-5:]:  # Limita a 5 interações mais recentes para não explodir o tamanho
        contexto += f"{h['role'].capitalize()}: {h['message']}\n"

    prompt = (
        "Você é um chatbot inteligente da empresa de marketing digital E-Vitrine, especializado em três áreas: "
        "1) marketing digital, 2) medicina humana e 3) medicina veterinária. "
        "Responda sempre com clareza, objetividade e como um especialista. "
        "Se não encontrar informações exatas na sua base de dados, use seu conhecimento geral e explique de forma simples. "
        "Você pode responder perguntas sobre saúde, doenças, bem-estar, estratégias de marketing, presença online e captação de pacientes ou clientes."
        "Você pode responder perguntas relacionadas a qualquer um destes temas."
    )

    if contexto:
        prompt += f"Contexto anterior:\n{contexto}\n"

    prompt += f"Pergunta do cliente: {incoming_msg}"

    resposta_ia = qa_chain.invoke({"query": prompt})["result"]

    # ✅ Atualiza histórico
    session.add_history(user_number, "usuário", incoming_msg)
    session.add_history(user_number, "chatbot", resposta_ia)

    resposta_completa = "🤖 _*Chatbot E-Vitrine:*_ \n\n" + resposta_ia
    partes = split_message(resposta_completa, MAX_CHARACTERS)

    if len(partes) == 1:
        resposta = partes[0] + "\n\nDigite sua pergunta ou *VOLTAR* para retornar ao menu."
        logger.info(f"[IA] {user_number}: {resposta}")
        return resposta

    session.set_response_parts(user_number, partes[1:])
    resposta = partes[0] + "\n\n➡️ Digite *CONTINUAR* para mais ou *VOLTAR* para retornar ao menu."

    logger.info(f"[IA] {user_number}: {resposta}")
    return resposta
