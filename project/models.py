import json
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    
    def to_json(self):
        return {'id': self.id, 'nome': self.nome, 'email': self.email}

class Images(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100), unique=True)
    image = db.Column(db.LargeBinary)
    resume = db.Column(db.String(1000))

    
    def to_json(self):
        return {'id': self.id, 'nome': self.name, 'image': self.image, 'resume': self.resume}
    