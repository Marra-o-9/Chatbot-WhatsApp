# app/routes/twilio.py

from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from app.utils.main import handle_message

twilio_routes = Blueprint("twilio_routes", __name__)

@twilio_routes.route("/webhook/twilio", methods=["POST"])
def webhook_twilio():
    incoming_msg = request.form.get("Body")
    user_id = request.form.get("From")

    response = handle_message(user_id, incoming_msg, canal="whatsapp")

    twilio_response = MessagingResponse()
    twilio_response.message(response)

    return str(twilio_response), 200
