# app/channels/webchat.py

# Para o Webchat, como é backend, normalmente o frontend espera a resposta da rota
# então aqui apenas criamos uma função de placeholder se quiser expandir no futuro

def send_webchat_message(user_id, message):
    # No Webchat, a resposta já é enviada pelo return do Flask (JSON), então essa função pode ser usada para logs, etc.
    print(f"[WEBCHAT RESP] {user_id}: {message}")
