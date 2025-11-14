from flask import Flask
from api.routes import api
from api.models import db
from api.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(api)

    print(app.url_map)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)