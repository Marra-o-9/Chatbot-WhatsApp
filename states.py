# states.py

# Dicionário global para armazenar os estados dos usuários
user_states = {}

def get_state(user_id):
    """
    Retorna o estado atual do usuário.
    Se o usuário não estiver registrado, assume estado 'menu'.
    """
    return user_states.get(user_id, "menu")

def set_state(user_id, state):
    """
    Atualiza o estado atual do usuário.
    """
    user_states[user_id] = state
