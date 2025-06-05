# app/session.py

user_sessions = {}

def set_response_parts(user_number, parts):
    if user_number not in user_sessions:
        user_sessions[user_number] = {"parts": [], "history": []}
    user_sessions[user_number]["parts"] = parts

def get_next_part(user_number):
    if user_number in user_sessions and user_sessions[user_number]["parts"]:
        return user_sessions[user_number]["parts"].pop(0)
    return None

def has_more_parts(user_number):
    return bool(user_sessions.get(user_number, {}).get("parts"))

def clear_session(user_number):
    if user_number in user_sessions:
        del user_sessions[user_number]

def add_history(user_number, role, message):
    if user_number not in user_sessions:
        user_sessions[user_number] = {"parts": [], "history": []}
    user_sessions[user_number]["history"].append({"role": role, "message": message})

def get_history(user_number):
    return user_sessions.get(user_number, {}).get("history", [])
