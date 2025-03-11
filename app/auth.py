# app/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)

            # Redirect to preferences page if the user hasn't selected one yet
            if not user.personality_preference:
                return redirect(url_for('preferences.set_preferences'))

            return redirect(url_for('main.index'))
        else:
            flash('Please check your login details and try again.')
    
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('auth.signup'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        # Redirect to preferences page immediately after signup
        return redirect(url_for('preferences.set_preferences'))
    
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
