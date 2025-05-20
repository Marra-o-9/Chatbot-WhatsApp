# app/handlers/__init__.py

from flask import Flask
from .main import webhook

def create_app():
    app = Flask(__name__)

    app.add_url_rule("/webhook", view_func=webhook, methods=["POST"])

    return app
