import os
import json
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# CARREGA VARIAVEIS DE AMBIENTE DO ARQUIVO .env
load_dotenv()

# CONFIGURACOES GERAIS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

# INICIALIZA APLICACAO
app = Flask(__name__)

# INDEXACAO DOS DOCUMENTOS COM FAISS
loader = TextLoader("data.txt")  # seu arquivo de conhecimento
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

# ROTA PARA RECEBER MENSAGENS DO TWILIO
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "")
    user_number = request.values.get("From", "")

    # Lógica de resposta
    resposta = qa_chain.run(incoming_msg)

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(resposta)

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
