# app/handlers/md_humanos.py

from ..menus import menu_fotos_videos, menu_redes, menu_eventos, menu_md_humanos, menu_final
from ..states import set_state, set_rota


def tratar_humanos(estado, incoming_msg, user_number):
    if estado == "md_humanos":
        if incoming_msg == "1":
            set_state(user_number, "fotos_humanos")
            return menu_fotos_videos("Médicos Humanos")
        elif incoming_msg == "2":
            set_state(user_number, "redes_humanos")
            return menu_redes("Médicos Humanos")
        elif incoming_msg == "3":
            set_state(user_number, "eventos_humanos")
            return menu_eventos("Médicos Humanos")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "menu")
            from ..menus import menu_principal
            return "🔙 Voltando ao menu anterior...\n\n" + menu_principal()
        else:
            return "❌ Opção inválida."

    elif estado in ["fotos_humanos", "redes_humanos", "eventos_humanos"]:
        rotas = {
            "fotos_humanos": ["Autoridade Médica", "Consultório Médico"],
            "redes_humanos": ["Posts + Monitoramento", "Posts + Fotos/Vídeos + Monitoramento"],
            "eventos_humanos": ["Cobertura de Evento", "Cobertura com Edição Imediata"]
        }
        if incoming_msg in ["1", "2"]:
            index = int(incoming_msg) - 1
            rota_nome = rotas[estado][index]
            set_state(user_number, f"final_{estado}")
            return menu_final(f"{rota_nome} - Médicos Humanos")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "md_humanos")
            return "🔙 Voltando ao menu anterior...\n\n" + menu_md_humanos()
        else:
            return "❌ Opção inválida."

    elif estado.startswith("final_") and "humanos" in estado:
        contexto = estado.replace("final_", "").replace("_humanos", "").replace("_", " ").title()
        if incoming_msg == "1":
            set_rota(user_number, f"{contexto} - WhatsApp - Médicos Humanos")
            return "📲 Em breve um consultor entrará em contato via WhatsApp."
        elif incoming_msg == "2":
            set_rota(user_number, f"{contexto} - Ligação - Médicos Humanos")
            return "📞 Nossa equipe fará uma ligação comercial para você."
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "md_humanos")
            return "🔙 Voltando ao menu anterior...\n\n" + menu_md_humanos()
        else:
            return "❌ Opção inválida."

    return "❌ Opção inválida."
