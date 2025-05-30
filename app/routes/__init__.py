# app/routes/__init__.py

from flask import Blueprint
from .twilio import twilio_routes
from .webchat import webchat_routes

routes = Blueprint("routes", __name__)
routes.register_blueprint(twilio_routes)
routes.register_blueprint(webchat_routes)
