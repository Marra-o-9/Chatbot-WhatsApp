# __init__.py

from flask import Flask
from .main import webhook, home

def create_app():
    app = Flask(__name__)

    app.add_url_rule("/webhook", view_func=webhook, methods=["POST"])
    app.add_url_rule("/", view_func=home, methods=["GET", "HEAD"])

    return app
