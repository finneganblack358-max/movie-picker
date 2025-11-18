from flask import Flask
import os
from dotenv import load_dotenv
from api.config import Config
from api.routes import api
from api.models import db

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback-secret-key")

    db.init_app(app)
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)