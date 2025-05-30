# app/channels/twilio.py

from twilio.rest import Client
import os

# Configure essas variáveis com suas credenciais do Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to, message):
    client.messages.create(
        body=message,
        from_=f"whatsapp:{TWILIO_NUMBER}",
        to=to
    )
