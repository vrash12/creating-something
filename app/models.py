# app/models.py
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    # New column to store personality preference, default is None
    personality_preference = db.Column(db.String(50), nullable=True)
    chats = db.relationship('Chat', backref='user', lazy=True)
    
    def set_password(self, password):
         self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
         return check_password_hash(self.password_hash, password)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
