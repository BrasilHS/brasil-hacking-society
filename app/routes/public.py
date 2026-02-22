from flask import Blueprint, render_template
from ..models.post import Post

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts)