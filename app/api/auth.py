from flask import Blueprint, request, jsonify, session
from marshmallow import ValidationError

from ..models import User
from ..schemas.user import UserRegister, UserLogin

auth_api_bp = Blueprint("api_auth", __name__)

@auth_api_bp.route("/login", methods=["POST"])
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
    return jsonify({"message": "Login succeed"}), 200


@auth_api_bp.route("/register", methods=["POST"])
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

    return jsonify({"message": "User registered, you can login now!"}), 201


