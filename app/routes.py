# app/routes.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
import google.generativeai as genai
from config import API_KEY, MODEL_ID
from app import db
from app.models import Chat
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

# Configure the Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_ID)

@main.route("/", methods=["GET"])
@login_required
def index():
    all_chats = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.id.asc()).all()
    # If user hasn't set their preference, redirect them
    if not current_user.personality_preference:
        return redirect(url_for("preferences.set_preferences"))
    return render_template("index.html", chats=all_chats)

@main.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    all_chats = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.id.asc()).all()
    
    # Tailor the conversation context using the user's personality preference.
    conversation_context = (
        f"You are Raven, a {current_user.personality_preference} girl who gives heartfelt, moody love advice with a twist.\n"
    )
    
    for chat in all_chats:
         conversation_context += f"You: {chat.user_message}\nRaven: {chat.bot_response}\n"
    
    prompt = conversation_context + f"You: {user_message}\nRaven:"
    response = model.generate_content(prompt)
    bot_reply = response.text.strip()
    
    # Ensure that only one "Raven:" is used
    if bot_reply.lower().startswith("raven:"):
        bot_reply = bot_reply[6:].strip()  # Strip the initial "Raven:" prefix
    
    new_chat = Chat(user_message=user_message, bot_response=bot_reply, user_id=current_user.id)
    db.session.add(new_chat)
    db.session.commit()
    
    # Use a suggestion prompt that returns only the three specific questions.
    suggestion_prompt = (
        conversation_context +
        f"You: {user_message}\n" +
        "Now, suggest three follow-up questions related to the conversation flow (one per line), without any additional text:"
    )
    suggestion_response = model.generate_content(suggestion_prompt)
    suggestions_text = suggestion_response.text.strip()
    suggestions = [line.strip() for line in suggestions_text.splitlines() if line.strip()][:3]
    
    return jsonify({"response": bot_reply, "suggestions": suggestions})

@main.route("/simplify", methods=["POST"])
@login_required
def simplify():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    simplify_prompt = f"Rewrite the following text using simpler language and common words: \"{text}\""
    response = model.generate_content(simplify_prompt)
    simplified_text = response.text.strip()
    if simplified_text.lower().startswith("raven:"):
        simplified_text = simplified_text[6:].strip()
    return jsonify({"simplified": simplified_text})

@main.route("/delete_history", methods=["POST"])
@login_required
def delete_history():
    try:
        # Delete all chat records for the current user.
        num_deleted = Chat.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        print(f"Deleted {num_deleted} chat(s) for user {current_user.id}")
        return jsonify({"status": "success", "deleted": num_deleted})
    except Exception as e:
        db.session.rollback()
        print("Error deleting history:", str(e))
        return jsonify({"status": "error", "error": str(e)}), 500
