# app/preferences.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db

preferences = Blueprint('preferences', __name__)

@preferences.route("/preferences", methods=["GET", "POST"])
@login_required
def set_preferences():
    if request.method == "POST":
        # Get the selected personality from the form
        personality = request.form.get("personality")
        if not personality:
            flash("Please select a personality preference.")
            return redirect(url_for("preferences.set_preferences"))
        
        # Save the preference to the current user
        current_user.personality_preference = personality
        db.session.commit()
        return redirect(url_for("main.index"))
    
    return render_template("preferences.html")
