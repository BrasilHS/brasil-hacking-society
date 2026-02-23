from flask import Blueprint, render_template
from ..models.post import Post

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
