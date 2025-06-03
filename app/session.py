# app/session.py

user_sessions = {}

def set_response_parts(user_number, parts):
    user_sessions[user_number] = parts

def get_next_part(user_number):
    if user_number in user_sessions and user_sessions[user_number]:
        return user_sessions[user_number].pop(0)
    return None

def has_more_parts(user_number):
    return bool(user_sessions.get(user_number))

def clear_session(user_number):
    if user_number in user_sessions:
        del user_sessions[user_number]
