from flask import Blueprint, request, jsonify, session, redirect
from marshmallow import ValidationError

from ..models import Post
from ..schemas.post import PostCreate

post_api_bp = Blueprint("api_post", __name__)

@post_api_bp.route("/new", methods=["POST"])
def post_login():
    if not session.get("user", None):
        return redirect("/login")

    if not request.is_json:
        return jsonify({"error": "Expect Content-Type: application/json"}), 422

    post_data = request.get_json()
    if not post_data:
        return jsonify({"error": "Data not received"}), 422

    post_schema = PostCreate(only={
        "title", "content", "type"
    })

    try:
        post = post_schema.load(post_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    user_id = session.get("user")
    post.set_user_id(user_id)

    try:
        post.insert()
    except Exception as err:
        print(err)
        return jsonify({"error": "There is something wrong"}), 500

    return jsonify({"message": "Post created"}), 201
