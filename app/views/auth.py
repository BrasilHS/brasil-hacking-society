from flask import Blueprint, render_template, session, redirect

auth_view_bp = Blueprint("auth", __name__)

@auth_view_bp.route("/login", methods=["GET"])
def login():
    if session.get("user", None):
        return redirect("/")
    return render_template("auth/login.html")

@auth_view_bp.route("/register", methods=["GET"])
def register():
    if session.get("user", None):
        return redirect("/")
    return render_template("auth/register.html")

@auth_view_bp.route("/logout", methods=["GET"])
def logout():
    if session.get("user", None):
        session.pop("user")
    return redirect("/")

