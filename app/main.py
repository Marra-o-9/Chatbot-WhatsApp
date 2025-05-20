# main.py

import logging
from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from .menus import *
from .states import get_state, set_state, set_rota
from .rag import iniciar_rag

# Configurar logger para o Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

qa_chain = iniciar_rag()

def tratar_ia(incoming_msg, user_number):
    if incoming_msg.upper() == "VOLTAR":
        set_state(user_number, "menu")
        resposta = "🔙 Voltando ao menu principal...\n\n" + menu_principal()
        logger.info(f"[RESPOSTA] {user_number}: {resposta}")
        return resposta

    prompt = (
        "Você é um chatbot inteligente da empresa de marketing digital E-Vitrine. "
        "Responda com clareza e objetividade como um especialista. "
        f"Pergunta do cliente: {incoming_msg}"
    )
    resposta = qa_chain.invoke({"query": prompt})["result"]
    resposta += "\n\nDigite *VOLTAR* para retornar ao menu."
    logger.info(f"[RESPOSTA] {user_number}: {resposta}")
    return resposta

def enviar_resposta(msg_obj, user_number, texto):
    logger.info(f"[RESPOSTA] {user_number}: {texto}")
    msg_obj.body(texto)

def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    user_number = request.values.get("From", "")
    logger.info(f"[MENSAGEM RECEBIDA] {user_number}: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    estado = get_state(user_number)

    if estado == "ia":
        resposta = tratar_ia(incoming_msg, user_number)
        enviar_resposta(msg, user_number, resposta)
        return str(resp)

    if estado == "menu":
        saudacoes = ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]
        if incoming_msg.lower() in saudacoes:
            enviar_resposta(msg, user_number, menu_principal())
        elif incoming_msg == "1":
            set_state(user_number, "cobertura_eventos")
            enviar_resposta(msg, user_number, menu_cobertura_eventos())
        elif incoming_msg == "2":
            set_state(user_number, "md_humanos")
            enviar_resposta(msg, user_number, menu_md_humanos())
        elif incoming_msg == "3":
            set_state(user_number, "md_veterinarios")
            enviar_resposta(msg, user_number, menu_md_veterinarios())
        elif incoming_msg == "4":
            set_state(user_number, "ia")
            resposta = (
                "🤖 Você ativou o modo informativo com inteligência artificial.\n"
                "Sou um chatbot especializado da *E-Vitrine* pronto para tirar suas dúvidas sobre marketing digital.\n\n"
                "Digite sua pergunta ou *VOLTAR* para retornar ao menu."
            )
            enviar_resposta(msg, user_number, resposta)
        else:
            enviar_resposta(msg, user_number, "❌ Opção inválida.\n\n" + menu_principal())
        return str(resp)

    # Cobertura de eventos
    if estado == "cobertura_eventos":
        if incoming_msg == "1":
            set_state(user_number, "congresso_feiras")
            enviar_resposta(msg, user_number, menu_congresso_feiras())
        elif incoming_msg == "2":
            set_state(user_number, "speakers")
            enviar_resposta(msg, user_number, menu_speakers())
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "menu")
            enviar_resposta(msg, user_number, "🔙 Voltando ao menu principal...\n\n" + menu_principal())
        else:
            enviar_resposta(msg, user_number, "❌ Opção inválida. Escolha 1 ou 2, ou digite *VOLTAR*.")
        return str(resp)

    if estado == "congresso_feiras":
        if incoming_msg == "1":
            set_rota(user_number, "Fotos - Congresso & Feiras")
            enviar_resposta(msg, user_number, "📸 Fotos profissionais de congressos e feiras para destacar sua marca.")
        elif incoming_msg == "2":
            set_rota(user_number, "Vídeos - Congresso & Feiras")
            enviar_resposta(msg, user_number, "🎥 Vídeos envolventes para redes sociais e divulgação.")
        elif incoming_msg == "3":
            set_rota(user_number, "Cobertura completa - Congresso & Feiras")
            enviar_resposta(msg, user_number, "✨ Cobertura completa com fotos, vídeos, reels e edição.")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "cobertura_eventos")
            enviar_resposta(msg, user_number, "🔙 Voltando ao menu anterior...\n\n" + menu_cobertura_eventos())
        else:
            enviar_resposta(msg, user_number, "❌ Opção inválida. Escolha 1, 2 ou 3, ou digite *VOLTAR*.")
        return str(resp)

    if estado == "speakers":
        if incoming_msg == "1":
            set_rota(user_number, "Pré Reels - Speakers")
            enviar_resposta(msg, user_number, "🎬 Chamadas personalizadas para reels com speakers.")
        elif incoming_msg == "2":
            set_rota(user_number, "Cobertura visual - Speakers")
            enviar_resposta(msg, user_number, "🎤 Cobertura com foco em presença de marca e impacto visual.")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "cobertura_eventos")
            enviar_resposta(msg, user_number, "🔙 Voltando ao menu anterior...\n\n" + menu_cobertura_eventos())
        else:
            enviar_resposta(msg, user_number, "❌ Opção inválida. Escolha 1 ou 2, ou digite *VOLTAR*.")
        return str(resp)

    # Marketing Digital para Médicos Humanos
    if estado == "md_humanos":
        if incoming_msg == "1":
            set_state(user_number, "fotos_humanos")
            enviar_resposta(msg, user_number, menu_fotos_videos("Médicos Humanos"))
        elif incoming_msg == "2":
            set_state(user_number, "redes_humanos")
            enviar_resposta(msg, user_number, menu_redes("Médicos Humanos"))
        elif incoming_msg == "3":
            set_state(user_number, "eventos_humanos")
            enviar_resposta(msg, user_number, menu_eventos("Médicos Humanos"))
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "menu")
            enviar_resposta(msg, user_number, menu_principal())
        else:
            enviar_resposta(msg, user_number, "❌ Opção inválida.")
        return str(resp)

    if estado in ["fotos_humanos", "redes_humanos", "eventos_humanos"]:
        rotas = {
            "fotos_humanos": ["Autoridade Médica", "Consultório Médico"],
            "redes_humanos": ["Posts + Monitoramento", "Posts + Fotos/Vídeos + Monitoramento"],
            "eventos_humanos": ["Cobertura de Evento", "Cobertura com Edição Imediata"]
        }
        if incoming_msg in ["1", "2"]:
            index = int(incoming_msg) - 1
            rota_nome = rotas[estado][index]
            set_state(user_number, f"final_{estado}")
            enviar_resposta(msg, user_number, menu_final(f"{rota_nome} - Médicos Humanos"))
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "md_humanos")
            enviar_resposta(msg, user_number, menu_md_humanos())
        else:
            enviar_resposta(msg, user_number, "❌ Opção inválida.")
        return str(resp)

    if estado.startswith("final_") and "humanos" in estado:
        contexto = estado.replace("final_", "").replace("_humanos", "").replace("_", " ").title()
        if incoming_msg == "1":
            set_rota(user_number, f"{contexto} - WhatsApp - Médicos Humanos")
            enviar_resposta(msg, user_number, "📲 Em breve um consultor entrará em contato via WhatsApp.")
        elif incoming_msg == "2":
            set_rota(user_number, f"{contexto} - Ligação - Médicos Humanos")
            enviar_resposta(msg, user_number, "📞 Nossa equipe fará uma ligação comercial para você.")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "md_humanos")
            enviar_resposta(msg, user_number, menu_md_humanos())
        else:
            enviar_resposta(msg, user_number, "❌ Opção inválida.")
        return str(resp)

    # Marketing Digital para Médicos Veterinários
    if estado == "md_veterinarios":
        if incoming_msg == "1":
            set_state(user_number, "fotos_veterinarios")
            enviar_resposta(msg, user_number, menu_fotos_videos("Médicos Veterinários"))
        elif incoming_msg == "2":
            set_state(user_number, "redes_veterinarios")
            enviar_resposta(msg, user_number, menu_redes("Médicos Veterinários"))
        elif incoming_msg == "3":
            set_state(user_number, "eventos_veterinarios")
            enviar_resposta(msg, user_number, menu_eventos("Médicos Veterinários"))
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "menu")
            enviar_resposta(msg, user_number, menu_principal())
        else:
            enviar_resposta(msg, user_number, "❌ Opção inválida.")
        return str(resp)

    if estado in ["fotos_veterinarios", "redes_veterinarios", "eventos_veterinarios"]:
        rotas = {
            "fotos_veterinarios": ["Autoridade Veterinária", "Consultório Veterinário"],
            "redes_veterinarios": ["Posts + Monitoramento", "Posts + Fotos/Vídeos + Monitoramento"],
            "eventos_veterinarios": ["Cobertura de Evento", "Cobertura com Edição Imediata"]
        }
        if incoming_msg in ["1", "2"]:
            index = int(incoming_msg) - 1
            rota_nome = rotas[estado][index]
            set_state(user_number, f"final_{estado}")
            enviar_resposta(msg, user_number, menu_final(f"{rota_nome} - Médicos Veterinários"))
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "md_veterinarios")
            enviar_resposta(msg, user_number, menu_md_veterinarios())
        else:
            enviar_resposta(msg, user_number, "❌ Opção inválida.")
        return str(resp)

    if estado.startswith("final_") and "veterinarios" in estado:
        contexto = estado.replace("final_", "").replace("_veterinarios", "").replace("_", " ").title()
        if incoming_msg == "1":
            set_rota(user_number, f"{contexto} - WhatsApp - Médicos Veterinários")
            enviar_resposta(msg, user_number, "📲 Em breve um consultor entrará em contato via WhatsApp.")
        elif incoming_msg == "2":
            set_rota(user_number, f"{contexto} - Ligação - Médicos Veterinários")
            enviar_resposta(msg, user_number, "📞 Nossa equipe fará uma ligação comercial para você.")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "md_veterinarios")
            enviar_resposta(msg, user_number, menu_md_veterinarios())
        else:
            enviar_resposta(msg, user_number, "❌ Opção inválida.")
        return str(resp)

    return str(resp)
