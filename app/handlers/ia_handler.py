# app/handlers/ia_handler.py

import logging
from app.menus import menu_principal
from app.states import set_state
from app.rag import iniciar_rag

logger = logging.getLogger(__name__)
qa_chain = iniciar_rag()

def handle(incoming_msg, user_number):
    if incoming_msg.upper() == "VOLTAR":
        set_state(user_number, "menu")
        resposta = "🔙 Voltando ao menu principal...\n\n" + menu_principal()
        logger.info(f"[IA] {user_number}: {resposta}")
        return resposta

    prompt = (
        "Você é um chatbot inteligente da empresa de marketing digital E-Vitrine. "
        "Responda com clareza e objetividade como um especialista. "
        f"Pergunta do cliente: {incoming_msg}"
    )
    resposta = "🤖 _*Chatbot E-Vitrine*_: \n\n"
    resposta += qa_chain.invoke({"query": prompt})["result"]
    resposta += "\n\nDigite *VOLTAR* para retornar ao menu."
    logger.info(f"[IA] {user_number}: {resposta}")
    return resposta
