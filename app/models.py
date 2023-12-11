from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db: SQLAlchemy = SQLAlchemy()


# Модель пользователя
class User(UserMixin, db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(50), unique=True, nullable=False)
    password: str = db.Column(db.String(255), nullable=False)


# Модель записи
class Entry(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(100), nullable=False)
    content: str = db.Column(db.Text, nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))
