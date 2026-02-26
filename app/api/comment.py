from flask import Blueprint, request, jsonify, session, redirect
from marshmallow import ValidationError

from ..models import Comment, Post
from ..schemas.comment import CommentCreate

comment_api_bp = Blueprint("api_comment", __name__)

@comment_api_bp.route("/new", methods=["POST"])
def post_login():
    if not session.get("user", None):
        return redirect("/login")

    if not request.is_json:
        return jsonify({"error": "Expect Content-Type: application/json"}), 422

    comment_data = request.get_json()
    if not comment_data:
        return jsonify({"error": "Data not received"}), 422

    comment_schema = CommentCreate(only={
        "post_id", "parent_id", "content"
    })

    try:
        comment = comment_schema.load(comment_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    if comment.parent_id == 0:
        comment.parent_id = None
    
    if comment.parent_id:
        parent = Comment.query.get(comment.parent_id)

        if not parent:
            return jsonify({"error": "Parent comment not found"}), 404

        # Herdar post do pai
        comment.post_id = parent.post_id

    if not comment.post_id:
        return jsonify({"error": "post_id is required"}), 400

    post = Post.query.get(comment.post_id)

    if not post:
        return jsonify({"error": "Post not found"}), 404


    user_id = session.get("user")
    comment.set_user_id(user_id)

    try:
        comment.insert()
    except Exception as err:
        print(err)
        return jsonify({"error": "There is something wrong"}), 500

    return jsonify({"message": "Comment created"}), 201
