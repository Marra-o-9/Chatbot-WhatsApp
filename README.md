# Chatbot com RAG para WhatsApp

Este projeto é um chatbot híbrido que integra respostas geradas por IA com base em conhecimento pré-carregado (RAG - Retrieval-Augmented Generation). Ele se conecta ao WhatsApp via Twilio e utiliza a API da OpenAI com LangChain para processar as interações.

## Funcionalidades

- Integração com WhatsApp via Twilio.
- Recuperação de informações com LangChain + FAISS.
- Uso de modelo via OpenAI.
- Base de conhecimento personalizável.
- Deploy pronto para Render.

## Requisitos

- Python 3.9+
- Conta na OpenAI
- Conta no Twilio (com Sandbox WhatsApp ativado)
- [Ngrok](https://ngrok.com/) (para testes locais)

## Como rodar localmente

1. Clone o projeto:

   ```bash
   git clone https://github.com/Marra-o-9/Chatbot-WhatsApp.git
   cd Chatbot-WhatsApp
   ```

2. Crie e ative um ambiente virtual:

   - Linux/macOS:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Crie o arquivo `.env` na raiz do projeto:

   ```
   OPENAI_API_KEY=sua-chave-aqui
   OPENAI_MODEL=seu-modelo-aqui
   ```

5. Coloque seu arquivo de base de conhecimento em `data/base_conhecimento.txt`.

6. Execute a aplicação localmente:

   ```bash
   python chatbot_evitrine.py
   ```

7. Em outro terminal, rode o ngrok:

   ```bash
   ngrok http 5000
   ```

   Copie o link gerado (ex: `https://abcd1234.ngrok.io`) e configure no painel do Twilio como webhook.

## Deploy no Render

Este projeto já possui um arquivo `render.yaml`. Basta conectar este repositório ao [Render](https://render.com/) e configurar a variável de ambiente `OPENAI_API_KEY` no painel.

## Observações

- O arquivo `.env` e os dados sensíveis não devem ser versionados.
- O arquivo de base de conhecimento deve estar presente no deploy para que o chatbot funcione corretamente.
