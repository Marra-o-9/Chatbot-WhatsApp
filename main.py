# Importa as bibliotecas necessárias
import os
import logging
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Inicializa aplicação Flask
app = Flask(__name__)

# Indexa documentos para RAG (chatbot informativo)
try:
    loader = TextLoader("data/data.txt")
    raw_docs = loader.load()
    logger.info("✅ Database carregada com sucesso")
except Exception as e:
    logger.error(f"❌ Erro ao carregar data.txt: {e}")
    raw_docs = []

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = splitter.split_documents(raw_docs)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

# Define cadeia de perguntas e respostas com recuperação
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name=OPENAI_MODEL),
    retriever=retriever
)

# Armazena estado por número de telefone
user_states = {}

# Mensagem do menu principal
def menu_principal():
    return (
        "👋 Olá! Seja bem-vindo à *E-Vitrine*, sua parceira em marketing digital.\n\n"
        "Escolha uma das opções para continuar:\n"
        "1️⃣ - Cobertura de eventos\n"
        "2️⃣ - Marketing digital para médicos\n"
        "3️⃣ - Marketing digital para segmento veterinário\n"
        "4️⃣ - Chatbot especializado com IA\n\n"
        "Digite o número da opção desejada."
    )

# Rota para verificar se o servidor está funcionando
@app.route("/", methods=["GET"])
def index():
    return "Webhook para Twilio WhatsApp está funcionando!"

# Rota para receber mensagens do Twilio
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Log dos dados recebidos
        logger.info(f"Dados recebidos: {request.values}")
        
        incoming_msg = request.values.get("Body", "").strip()
        user_number = request.values.get("From", "")
        
        logger.info(f"Mensagem recebida: '{incoming_msg}' de {user_number}")
        
        resp = MessagingResponse()
        msg = resp.message()

        # Inicializa estado do usuário se ainda não existir
        if user_number not in user_states:
            user_states[user_number] = "menu"
            logger.info(f"Novo usuário: {user_number}")

        estado = user_states[user_number]
        logger.info(f"Estado atual do usuário: {estado}")

        # Lógica do modo informativo com IA
        if estado == "ia":
            if incoming_msg.upper() == "VOLTAR":
                user_states[user_number] = "menu"
                msg.body("🔙 Voltando ao menu principal...\n\n" + menu_principal())
                logger.info("Usuário voltou ao menu principal")
            else:
                # Inclui contexto no prompt
                pergunta_com_contexto = (
                    f"Você é um chatbot inteligente da empresa de marketing digital E-Vitrine. "
                    f"Responda com clareza e objetividade como um especialista. "
                    f"Pergunta do cliente: {incoming_msg}"
                )
                logger.info(f"Enviando pergunta para IA: {pergunta_com_contexto[:50]}...")
                try:
                    resposta = qa_chain.run(pergunta_com_contexto)
                    logger.info(f"Resposta da IA recebida: {resposta[:50]}...")
                    msg.body(resposta + "\n\nDigite *VOLTAR* para retornar ao menu.")
                except Exception as e:
                    logger.error(f"Erro ao processar resposta da IA: {e}")
                    msg.body("Desculpe, tive um problema ao processar sua pergunta. Por favor, tente novamente ou digite *VOLTAR* para retornar ao menu.")
        
        # Lógica do menu principal e submenus
        elif estado == "menu":
            if incoming_msg == "1":
                user_states[user_number] = "cobertura_eventos"
                msg.body(
                    "🎤 *Cobertura de eventos*\n\n"
                    "Escolha uma das opções:\n"
                    "1️⃣ - Congresso & Feiras\n"
                    "2️⃣ - Speakers\n\n"
                    "Digite o número da opção ou *VOLTAR* para retornar."
                )
            elif incoming_msg == "2":
                msg.body("🩺 Ajudamos médicos a se posicionarem de forma estratégica nas redes sociais. Fale conosco para mais detalhes.")
            elif incoming_msg == "3":
                msg.body("🐾 Oferecemos marketing especializado para clínicas e profissionais da área veterinária.")
            elif incoming_msg == "4":
                user_states[user_number] = "ia"
                msg.body(
                    "🤖 Você ativou o modo informativo com inteligência artificial.\n"
                    "Sou um chatbot especializado da *E-Vitrine* pronto para tirar suas dúvidas sobre marketing digital.\n\n"
                    "Digite sua pergunta ou *VOLTAR* para retornar ao menu."
                )
            else:
                msg.body("❌ Opção inválida. Por favor, escolha uma das opções abaixo:\n\n" + menu_principal())
        
        # Lógica para submenu: cobertura de eventos
        elif estado == "cobertura_eventos":
            if incoming_msg == "1":
                user_states[user_number] = "congresso_feiras"
                msg.body(
                    "🏛️ *Congresso & Feiras*\n\n"
                    "1️⃣ - Fotos\n"
                    "2️⃣ - Vídeos\n"
                    "3️⃣ - Cobertura completa\n\n"
                    "Digite o número da opção ou *VOLTAR* para retornar."
                )
            elif incoming_msg == "2":
                user_states[user_number] = "speakers"
                msg.body(
                    "🎤 *Speakers no evento*\n\n"
                    "1️⃣ - Chamada de Pré Reels Digital\n"
                    "2️⃣ - Cobertura do Speakers no Evento\n\n"
                    "Digite o número da opção ou *VOLTAR* para retornar."
                )
            elif incoming_msg.upper() == "VOLTAR":
                user_states[user_number] = "menu"
                msg.body("🔙 Voltando ao menu principal...\n\n" + menu_principal())
            else:
                msg.body("❌ Opção inválida. Escolha 1 ou 2, ou digite *VOLTAR*.")
        
        # Lógica para submenu: congresso & feiras
        elif estado == "congresso_feiras":
            if incoming_msg == "1":
                msg.body("📸 Realizamos registro fotográfico profissional de congressos e feiras, com foco em destacar sua marca.")
            elif incoming_msg == "2":
                msg.body("🎥 Vídeos dinâmicos e envolventes para redes sociais e divulgação institucional de eventos.")
            elif incoming_msg == "3":
                msg.body("✨ Cobertura completa com fotos, vídeos, reels e edição pronta para publicação.")
            elif incoming_msg.upper() == "VOLTAR":
                user_states[user_number] = "cobertura_eventos"
                msg.body("🔙 Voltando ao menu anterior...\n\n1 - Congresso & Feiras\n2 - Speakers")
            else:
                msg.body("❌ Opção inválida. Escolha 1, 2 ou 3, ou digite *VOLTAR*.")
        
        # Lógica para submenu: speakers
        elif estado == "speakers":
            if incoming_msg == "1":
                msg.body("🎬 Criamos chamadas personalizadas para reels com os speakers do seu evento, otimizadas para engajamento digital.")
            elif incoming_msg == "2":
                msg.body("🎤 Cobrimos a participação de speakers com foco em presença de marca e impacto visual.")
            elif incoming_msg.upper() == "VOLTAR":
                user_states[user_number] = "cobertura_eventos"
                msg.body("🔙 Voltando ao menu anterior...\n\n1 - Congresso & Feiras\n2 - Speakers")
            else:
                msg.body("❌ Opção inválida. Escolha 1 ou 2, ou digite *VOLTAR*.")
        
        # Log da resposta
        logger.info(f"Resposta enviada: {msg.body}")
        
        # Garantir que a resposta seja retornada corretamente
        response = Response(str(resp), mimetype="application/xml")
        logger.info(f"Resposta XML: {str(resp)}")
        return response
        
    except Exception as e:
        logger.error(f"Erro no webhook: {e}", exc_info=True)
        # Retornar uma resposta mesmo em caso de erro
        error_resp = MessagingResponse()
        error_resp.message("Desculpe, ocorreu um erro no processamento da sua mensagem. Por favor, tente novamente.")
        return Response(str(error_resp), mimetype="application/xml")

# Rota para teste de webhook
@app.route("/test", methods=["GET"])
def test_webhook():
    resp = MessagingResponse()
    resp.message("Este é um teste do webhook. Se você está vendo esta mensagem, o webhook está funcionando corretamente!")
    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    # Usar a porta definida pelo ambiente ou 5000 como padrão
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Iniciando servidor na porta {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
