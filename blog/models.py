from blog import db, login_manager
from flask_login import UserMixin
from datetime import datetime




@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='autor', lazy=True)
    foto_perfil = db.Column(db.String, default='default.jpg')  # Caminho para a foto de perfil
    temas = db.Column(db.String, nullable=False, default='Não informado')

    def contar_post(self):
        return len(self.posts)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tema = db.Column(db.String(100), nullable=False)