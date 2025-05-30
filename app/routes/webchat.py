# app/routes/webchat.py

from flask import Blueprint, request, jsonify
from app.utils.main import handle_message
from app.channels.webchat import send_webchat_message

webchat_routes = Blueprint("webchat_routes", __name__)

@webchat_routes.route("/webhook/webchat", methods=["POST"])
def webhook_webchat():
    data = request.get_json()
    user_id = data["user_id"]
    message = data["message"]

    response = handle_message(user_id, message, canal="webchat")
    send_webchat_message(user_id, response)

    return jsonify({"response": response})
