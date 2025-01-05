from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi database
    db.init_app(app)

    # Daftarkan Blueprint
    from app.routes import routes
    app.register_blueprint(routes)

    return app
