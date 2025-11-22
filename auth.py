from flask import Blueprint, request, jsonify
from models import create_user, get_user_by_email
from flask_jwt_extended import create_access_token
import datetime

auths = Blueprint('auth', __name__)

@auths.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not (name and email and password):
        return jsonify({"success": False, "message": "Missing fields"}), 400

    if get_user_by_email(email):
        return jsonify({"success": False, "message": "User exists"}), 400

    user = create_user(name, email, password)
    user['_id'] = str(user['_id'])
    return jsonify({"success": True, "user": user}), 201

@auths.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not (email and password):
        return jsonify({"success": False, "message": "Missing fields"}), 400

    user = get_user_by_email(email)
    if not user:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    if user["password"] != password:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=str(user["_id"]),
        expires_delta=datetime.timedelta(days=7)
    )

    return jsonify({
        "success": True,
        "token": access_token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
    }), 200
