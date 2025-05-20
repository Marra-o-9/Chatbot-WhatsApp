# app/handlers/ia.py

from ..rag import iniciar_rag
from ..states import set_state

qa_chain = iniciar_rag()

def tratar_ia(incoming_msg, user_number):
    if incoming_msg.upper() == "VOLTAR":
        set_state(user_number, "menu")
        from ..menus import menu_principal
        return "🔙 Voltando ao menu principal...\n\n" + menu_principal()

    prompt = (
        "Você é um chatbot inteligente da empresa de marketing digital E-Vitrine. "
        "Responda com clareza e objetividade como um especialista. "
        f"Pergunta do cliente: {incoming_msg}"
    )
    resposta = qa_chain.invoke({"query": prompt})["result"]
    return resposta + "\n\nDigite *VOLTAR* para retornar ao menu."
