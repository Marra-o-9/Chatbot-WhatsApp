from flask import Flask

def create_app():
    app = Flask(__name__)

    from .main import webhook
    app.add_url_rule("/webhook", view_func=webhook, methods=["POST"])

    return app
