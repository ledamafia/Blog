from blog import db, app
from blog.models import Usuario, Post



with app.app_context():
    db.create_all()