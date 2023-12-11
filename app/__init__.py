from flask import Flask

from app.models import db
from app.routes import init_app


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config['SECRET_KEY']: str = 'your_secret_key'  # Замените на свой секретный ключ
    app.config['SQLALCHEMY_DATABASE_URI']: str = 'postgresql://postgres:123@localhost/flask_app'  # Замените на свои данные
    # app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)
    init_app(app)

    with app.app_context():
        db.create_all()

    return app
