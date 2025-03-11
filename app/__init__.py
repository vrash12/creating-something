# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY
    
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate here
    login_manager.init_app(app)
    
    from app.models import User, Chat
    
    @login_manager.user_loader
    def load_user(user_id):
         return User.query.get(int(user_id))
    
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.preferences import preferences as preferences_blueprint
    app.register_blueprint(preferences_blueprint)
    
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
