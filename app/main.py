# main.py

from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from .menus import *
from .states import get_state, set_state
from .rag import iniciar_rag

qa_chain = iniciar_rag()

def tratar_ia(incoming_msg, user_number):
    if incoming_msg.upper() == "VOLTAR":
        set_state(user_number, "menu")
        return "🔙 Voltando ao menu principal...\n\n" + menu_principal()

    prompt = (
        "Você é um chatbot inteligente da empresa de marketing digital E-Vitrine. "
        "Responda com clareza e objetividade como um especialista. "
        f"Pergunta do cliente: {incoming_msg}"
    )
    resposta = qa_chain.invoke({"query": prompt})
    return resposta["result"] + "\n\nDigite *VOLTAR* para retornar ao menu."

def home():
    return "🚀 E-Vitrine Chatbot API Online", 200

def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    user_number = request.values.get("From", "")
    resp = MessagingResponse()
    msg = resp.message()

    estado = get_state(user_number)

    if estado == "ia":
        msg.body(tratar_ia(incoming_msg, user_number))
        return str(resp)

    if estado == "menu":
        saudacoes = ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]
        if incoming_msg.lower() in saudacoes:
            msg.body(menu_principal())
        elif incoming_msg == "1":
            set_state(user_number, "cobertura_eventos")
            msg.body(menu_cobertura_eventos())
        elif incoming_msg == "2":
            msg.body("🩺 Ajudamos médicos a se posicionarem de forma estratégica nas redes sociais.")
        elif incoming_msg == "3":
            msg.body("🐾 Oferecemos marketing especializado para clínicas veterinárias.")
        elif incoming_msg == "4":
            set_state(user_number, "ia")
            msg.body(
                "🤖 Você ativou o modo informativo com inteligência artificial.\n"
                "Sou um chatbot especializado da *E-Vitrine* pronto para tirar suas dúvidas sobre marketing digital.\n\n"
                "Digite sua pergunta ou *VOLTAR* para retornar ao menu."
            )
        else:
            msg.body("❌ Opção inválida.\n\n" + menu_principal())
        return str(resp)

    if estado == "cobertura_eventos":
        if incoming_msg == "1":
            set_state(user_number, "congresso_feiras")
            msg.body(menu_congresso_feiras())
        elif incoming_msg == "2":
            set_state(user_number, "speakers")
            msg.body(menu_speakers())
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "menu")
            msg.body("🔙 Voltando ao menu principal...\n\n" + menu_principal())
        else:
            msg.body("❌ Opção inválida. Escolha 1 ou 2, ou digite *VOLTAR*.")
        return str(resp)

    if estado == "congresso_feiras":
        if incoming_msg == "1":
            msg.body("📸 Fotos profissionais de congressos e feiras para destacar sua marca.")
        elif incoming_msg == "2":
            msg.body("🎥 Vídeos envolventes para redes sociais e divulgação.")
        elif incoming_msg == "3":
            msg.body("✨ Cobertura completa com fotos, vídeos, reels e edição.")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "cobertura_eventos")
            msg.body("🔙 Voltando ao menu anterior...\n\n" + menu_cobertura_eventos())
        else:
            msg.body("❌ Opção inválida. Escolha 1, 2 ou 3, ou digite *VOLTAR*.")
        return str(resp)

    if estado == "speakers":
        if incoming_msg == "1":
            msg.body("🎬 Chamadas personalizadas para reels com speakers.")
        elif incoming_msg == "2":
            msg.body("🎤 Cobertura com foco em presença de marca e impacto visual.")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "cobertura_eventos")
            msg.body("🔙 Voltando ao menu anterior...\n\n" + menu_cobertura_eventos())
        else:
            msg.body("❌ Opção inválida. Escolha 1 ou 2, ou digite *VOLTAR*.")
        return str(resp)

    return str(resp)
