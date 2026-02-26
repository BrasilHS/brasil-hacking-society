from flask import Blueprint, render_template, session, redirect, request, url_for

from ..models import Post, Comment

post_view_bp = Blueprint("post_view", __name__)

@post_view_bp.route("/writeup/new", methods=["GET"])
def new_writeup():
    if not session.get("user", None):
        return redirect("/login")
    
    return render_template("posts/create.html", type="writeup")

@post_view_bp.route("/question/new", methods=["GET"])
def new_question():
    if not session.get("user", None):
        return redirect("/login")
    
    return render_template("posts/create.html", type="question")

@post_view_bp.route("/<id>")
def show_post(id):
    post = Post.query.filter_by(id=id).first()
    return render_template("posts/show.html", post=post)

