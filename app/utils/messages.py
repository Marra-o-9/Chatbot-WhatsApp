# app/utils/messages.py

from app.states import get_user_info

def contato_whatsapp(numero):
    user_info = get_user_info(numero)
    servico = user_info.get("servico") if user_info else "Não registrado"
    return f"🎯 *Serviço escolhido:* {servico}\n\n📲 Aguarde, um consultor entrará em contato via WhatsApp.\n\n"

def contato_ligacao(numero):
    user_info = get_user_info(numero)
    servico = user_info.get("servico") if user_info else "Não registrado"
    return f"🎯 *Serviço escolhido:* {servico}\n\n📞 Aguarde, nossa equipe fará uma ligação comercial para você.\n\n"

opcao_invalida = "❓ Não entendi.\n\n"
voltando_menu = "🔙 Voltando ao menu principal...\n\n"
voltando_anterior = "🔙 Voltando ao menu anterior...\n\n"
convite_ia = "🤖 Quer conhecer nosso Chatbot com Inteligência Artificial? Responda *SIM* ou *NÃO*"
