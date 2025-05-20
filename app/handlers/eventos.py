# app/handlers/eventos.py

from ..menus import menu_fotos_videos, menu_redes, menu_eventos, menu_eventos_principal, menu_final
from ..states import set_state, set_rota


def tratar_eventos(estado, incoming_msg, user_number):
    if estado == "eventos":
        if incoming_msg == "1":
            set_state(user_number, "fotos_eventos")
            return menu_fotos_videos("Eventos")
        elif incoming_msg == "2":
            set_state(user_number, "redes_eventos")
            return menu_redes("Eventos")
        elif incoming_msg == "3":
            set_state(user_number, "eventos_eventos")
            return menu_eventos("Eventos")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "menu")
            from ..menus import menu_principal
            return "🔙 Voltando ao menu anterior...\n\n" + menu_principal()
        else:
            return "❌ Opção inválida."

    elif estado in ["fotos_eventos", "redes_eventos", "eventos_eventos"]:
        rotas = {
            "fotos_eventos": ["Cobertura Fotográfica", "Fotos com Edição Imediata"],
            "redes_eventos": ["Posts + Monitoramento", "Posts + Fotos/Vídeos + Monitoramento"],
            "eventos_eventos": ["Cobertura de Evento", "Cobertura com Edição Imediata"]
        }
        if incoming_msg in ["1", "2"]:
            index = int(incoming_msg) - 1
            rota_nome = rotas[estado][index]
            set_state(user_number, f"final_{estado}")
            return menu_final(f"{rota_nome} - Eventos")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "eventos")
            return "🔙 Voltando ao menu anterior...\n\n" + menu_eventos_principal()
        else:
            return "❌ Opção inválida."

    elif estado.startswith("final_") and "eventos" in estado:
        contexto = estado.replace("final_", "").replace("_eventos", "").replace("_", " ").title()
        if incoming_msg == "1":
            set_rota(user_number, f"{contexto} - WhatsApp - Eventos")
            return "📲 Em breve um consultor entrará em contato via WhatsApp."
        elif incoming_msg == "2":
            set_rota(user_number, f"{contexto} - Ligação - Eventos")
            return "📞 Nossa equipe fará uma ligação comercial para você."
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "eventos")
            return "🔙 Voltando ao menu anterior...\n\n" + menu_eventos_principal()
        else:
            return "❌ Opção inválida."

    return "❌ Opção inválida."
