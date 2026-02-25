from flask import Blueprint, render_template, request, jsonify, session, redirect
from sqlalchemy import select
from marshmallow import ValidationError

from ..extensions import db
from ..models import Post, User
from ..schemas.user import UserRegister, UserLogin

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    # posts = [
    #     {
    #         "id": 1,
    #         "title": "Espero que esteja gostando da exploração",
    #         "content": "Por acaso você está tentando achar secrets nos commits passados? (já pode descer um commit haha). Talvez apenas curiosidade? não sei, enfim, tenha uma boa experiência e obrigado pela dedicação!",
    #         "created_at": "23/02/2026 01:38:23",
    #         "author": "Some Guy",
    #         "votes": 351,
    #         "comment_quantity": 34
    #     }
    # ]
    return render_template("index.html", posts=posts)

@public_bp.route("/login", methods=["GET"])
def login():
    if session.get("user", None):
        return redirect("/")
    return render_template("login.html")

@public_bp.route("/api/auth/login", methods=["POST"])
def auth_login():
    if not request.is_json:
        return jsonify({"error": "Expect Content-Type: application/json"}), 422

    user_login_data = request.get_json()
    if not user_login_data:
        return jsonify({"error": "Data not received"}), 422

    user_login_schema = UserLogin(only={
        "username", "password"
    })

    try:
        user = user_login_schema.load(user_login_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    try:
        user_exists = User.query.filter_by(username=user["username"]).first()
        
        if not user_exists:
            return jsonify({"error": "Invalid login credentials"}), 422
        
        if not user_exists.check_password(user["password"]):
            return jsonify({"error": "Invalid login credentials"}), 422

    except Exception as err:
        print(err)
        return jsonify({"error": "There is something wrong"}), 500
    
    session["user"] = user_exists.id
    return jsonify({"message": "success"}), 200

@public_bp.route("/register", methods=["GET"])
def register():
    if session.get("user", None):
        return redirect("/")
    return render_template("register.html")

@public_bp.route("/api/auth/register", methods=["POST"])
def auth_register():

    if not request.is_json:
        return jsonify({"error": "Expect Content-Type: application/json"}), 422

    user_register_data = request.get_json()
    if not user_register_data:
        return jsonify({"error": "Data not received"}), 422
    
    user_register_schema = UserRegister(only={
        "username", "email", "password", "confirm_password"
    })

    try:
        user = user_register_schema.load(user_register_data)
    except ValidationError as err:
        return jsonify(err.messages), 422   

    try:
        user.insert()
    except Exception as err:
        print(err)
        return jsonify({"error": "There is something wrong"}), 500

    return jsonify({"message": "Usuário cadastrado, você já pode fazer Login!"}), 201


@public_bp.route("/logout", methods=["GET"])
def logout():
    if session.get("user", None):
        session.pop("user")
    return redirect("/")
