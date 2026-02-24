from flask import Blueprint, render_template, request, jsonify, flash
from marshmallow import ValidationError

from ..extensions import db
from ..models.post import Post
from ..schemas.user import UserRegister

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

@public_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return {"message": "in development"}

    return render_template("login.html")

@public_bp.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@public_bp.route("/api/auth/register", methods=["POST"])
def auth_register():

    if not request.is_json:
        return jsonify({"error": "É esperado Content-Type: application/json"}), 422

    user_register_data = request.get_json()
    if not user_register_data:
        return jsonify({"error": "Dados não recebidos"}), 422
    
    user_register_schema = UserRegister(only={
        "username", "email", "password", "confirm_password"
    })

    try:
        user = user_register_schema.load(user_register_data)
    except ValidationError as err:
        return jsonify(err.messages), 422   

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as err:
        print(err.messages)
        return jsonify({"error": "There is something wrong"})

    return jsonify({"message": "Usuário cadastrado, você já pode fazer Login!"}), 201


