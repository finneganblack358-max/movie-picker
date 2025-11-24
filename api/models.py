from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
    
class MovieQuote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(500))
    movie = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
