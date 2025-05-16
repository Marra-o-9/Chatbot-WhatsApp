# Importa as bibliotecas necessárias
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Importa menus modularizados
from menus import (
    menu_principal,
    menu_cobertura_eventos,
    menu_congresso_feiras,
    menu_speakers
)

from states import get_state, set_state

# Carrega variáveis de ambiente
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Inicializa aplicação Flask
app = Flask(__name__)

# Indexa documentos para RAG (chatbot informativo)
loader = TextLoader("data/data.txt")
raw_docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = splitter.split_documents(raw_docs)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name=OPENAI_MODEL),
    retriever=retriever
)

# Função para tratar modo IA
def tratar_ia(incoming_msg, user_number):
    if incoming_msg.upper() == "VOLTAR":
        set_state(user_number, "menu")
        return "🔙 Voltando ao menu principal...\n\n" + menu_principal()
    
    prompt = (
        "Você é um chatbot inteligente da empresa de marketing digital E-Vitrine. "
        "Responda com clareza e objetividade como um especialista. "
        f"Pergunta do cliente: {incoming_msg}"
    )
    resposta = qa_chain.run(prompt)
    return resposta + "\n\nDigite *VOLTAR* para retornar ao menu."

# Webhook principal
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    user_number = request.values.get("From", "")
    resp = MessagingResponse()
    msg = resp.message()

    estado = get_state(user_number)

    # IA
    if estado == "ia":
        msg.body(tratar_ia(incoming_msg, user_number))
        return str(resp)

    if estado == "menu":
        if incoming_msg == "1":
            set_state(user_number, "cobertura_eventos")
            msg.body(menu_cobertura_eventos())
        elif incoming_msg == "2":
            msg.body("🩺 Ajudamos médicos a se posicionarem de forma estratégica nas redes sociais. Fale conosco para mais detalhes.")
        elif incoming_msg == "3":
            msg.body("🐾 Oferecemos marketing especializado para clínicas e profissionais da área veterinária.")
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
            msg.body("📸 Realizamos registro fotográfico profissional de congressos e feiras, com foco em destacar sua marca.")
        elif incoming_msg == "2":
            msg.body("🎥 Vídeos dinâmicos e envolventes para redes sociais e divulgação institucional de eventos.")
        elif incoming_msg == "3":
            msg.body("✨ Cobertura completa com fotos, vídeos, reels e edição pronta para publicação.")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "cobertura_eventos")
            msg.body("🔙 Voltando ao menu anterior...\n\n" + menu_cobertura_eventos())
        else:
            msg.body("❌ Opção inválida. Escolha 1, 2 ou 3, ou digite *VOLTAR*.")
        return str(resp)

    if estado == "speakers":
        if incoming_msg == "1":
            msg.body("🎬 Criamos chamadas personalizadas para reels com os speakers do seu evento, otimizadas para engajamento digital.")
        elif incoming_msg == "2":
            msg.body("🎤 Cobrimos a participação de speakers com foco em presença de marca e impacto visual.")
        elif incoming_msg.upper() == "VOLTAR":
            set_state(user_number, "cobertura_eventos")
            msg.body("🔙 Voltando ao menu anterior...\n\n" + menu_cobertura_eventos())
        else:
            msg.body("❌ Opção inválida. Escolha 1 ou 2, ou digite *VOLTAR*.")
        return str(resp)

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
