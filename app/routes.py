# app/routes.py

from flask import Blueprint, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from app.utils.main import handle_message
from app.channels.twilio import send_whatsapp_message
from app.channels.webchat import send_webchat_message

routes = Blueprint("routes", __name__)

@routes.route("/webhook/twilio", methods=["POST"])
def webhook_twilio():
    incoming_msg = request.form.get("Body")
    user_id = request.form.get("From")

    response = handle_message(user_id, incoming_msg, canal="whatsapp")

    twilio_response = MessagingResponse()
    twilio_response.message(response)

    return str(twilio_response), 200

@routes.route("/webhook/webchat", methods=["POST"])
def webhook_webchat():
    data = request.get_json()
    user_id = data["user_id"]
    message = data["message"]

    response = handle_message(user_id, message, canal="webchat")
    send_webchat_message(user_id, response)

    return jsonify({"response": response})
