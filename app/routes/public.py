from flask import Blueprint, render_template, request, jsonify
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

@public_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        user_register_data = request.form.to_dict()  
        if not user_register_data:
            return jsonify({"error": "no data provided"}), 422
        
        user_register_schema = UserRegister(only={
            "username", "email", "password", "confirm_password"
        })

        try:
            user = user_register_schema.load(user_register_data)
        except ValidationError as err:
            return jsonify(err.messages), 422
        
        print(user)

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "user created"}), 201
    
    return render_template("register.html")

