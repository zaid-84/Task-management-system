import os

from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.services.scheduler_service import start_scheduler
from app.routes.task_routes import task_bp
from app.routes.user_routes import user_bp



def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    

    CORS(
    app,
    origins=[Config.FRONTEND_URL],
    supports_credentials=True
    )

    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)

    start_scheduler()

    @app.route("/")
    def home():
        return {
            "message": "Task Management API is running"
        }

    return app