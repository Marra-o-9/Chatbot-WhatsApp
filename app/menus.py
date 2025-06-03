# app/menus.py

def menu_principal():
    return (
        "👋 Olá! Seja bem-vindo à *E-Vitrine*, sua parceira em marketing digital.\n\n"
        "Escolha uma das opções para continuar:\n"
        "1️⃣ - Cobertura de Eventos\n"
        "2️⃣ - Marketing Digital para Médicos\n"
        "3️⃣ - Marketing Digital para Segmento Veterinário\n"
        "4️⃣ - Chatbot Especializado com IA\n\n"
        "Digite o número da opção desejada."
    )

def menu_cobertura_eventos():
    return (
        "🎤 *Cobertura de eventos*\n\n"
        "Escolha uma das opções:\n"
        "1️⃣ - Congresso & Feiras\n"
        "2️⃣ - Speakers\n\n"
        "Digite o número da opção ou *VOLTAR* para retornar."
    )

def menu_congresso_feiras():
    return (
        "🏛️ *Congresso & Feiras*\n\n"
        "1️⃣ - Fotos\n"
        "2️⃣ - Vídeos\n"
        "3️⃣ - Cobertura completa\n\n"
        "Digite o número da opção ou *VOLTAR* para retornar."
    )

def menu_speakers():
    return (
        "🎤 *Speakers no evento*\n\n"
        "1️⃣ - Chamada de Pré Release Digital\n"
        "2️⃣ - Cobertura do Speakers no Evento\n\n"
        "Digite o número da opção ou *VOLTAR* para retornar."
    )

def menu_md_humanos():
    return (
        "🩺 *Marketing Digital para Médicos Humanos*\n\n"
        "1️⃣ - Captação de Fotos e Vídeos\n"
        "2️⃣ - Acompanhamento das Redes Sociais\n"
        "3️⃣ - Cobertura de Evento\n\n"
        "Digite o número da opção ou *VOLTAR* para retornar."
    )

def menu_md_veterinarios():
    return (
        "🐾 *Marketing Digital para Médicos Veterinários*\n\n"
        "1️⃣ - Captação de Fotos e Vídeos\n"
        "2️⃣ - Acompanhamento das Redes Sociais\n"
        "3️⃣ - Cobertura de Evento\n\n"
        "Digite o número da opção ou *VOLTAR* para retornar."
    )

def menu_fotos_videos(tipo):
    return (
        f"📸 *Captação de Fotos e Vídeos - {tipo}*\n\n"
        "1️⃣ - Fotos e Vídeos para sua autoridade\n"
        "2️⃣ - Fotos e Vídeos para consultório e/ou estrutura\n\n"
        "Digite o número da opção ou *VOLTAR* para retornar."
    )

def menu_redes(tipo):
    return (
        f"📱 *Acompanhamento das Redes Sociais - {tipo}*\n\n"
        "1️⃣ - Posts Estáticos + Monitoramento\n"
        "2️⃣ - Posts Estáticos + Fotos/Vídeos + Monitoramento\n\n"
        "Digite o número da opção ou *VOLTAR* para retornar."
    )

def menu_eventos(tipo):
    return (
        f"🎉 *Cobertura de Evento - {tipo}*\n\n"
        "1️⃣ - Cobertura com Fotos e Vídeos\n"
        "2️⃣ - Cobertura com entrega imediata\n\n"
        "Digite o número da opção ou *VOLTAR* para retornar."
    )

def menu_final(rota):
    return (
        f"📌 *{rota}*\n\n"
        "1️⃣ - Atendimento via WhatsApp\n"
        "2️⃣ - Ligação Comercial\n\n"
        "Digite o número da opção ou *VOLTAR* para retornar."
    )

def menu_ia():
    return (
        "🤖 Você ativou o modo informativo com inteligência artificial.\n"
        "Sou um chatbot especializado da *E-Vitrine* pronto para tirar suas dúvidas sobre marketing digital.\n\n"
        "Digite sua pergunta ou *VOLTAR* para retornar ao menu."
    )