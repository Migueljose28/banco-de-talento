from db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(30), nullable=False)
    senha = db.Column(db.String(255))
    email = db.Column(db.String(50), unique=True, nullable=False)
    telefone = db.Column(db.String(15))
    cpf = db.Column(db.String(11), nullable=False)
    

    def __repr__(self):
        return f"User('{self.nome}', '{self.email}')"