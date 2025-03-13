from flask import Blueprint, jsonify, request
from backend.extensions import mongo
from bson.objectid import ObjectId

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def get_users():
    users = mongo.db.users.find()
    user_list = [{"_id": str(user["_id"]), "name": user["name"], "email": user["email"]} for user in users]
    return jsonify(user_list), 200

@users_bp.route("/", methods=["POST"])
def add_user():
    data = request.json
    if not data or "name" not in data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    user_id = mongo.db.users.insert_one({
        "name": data["name"], 
        "email": data["email"], 
        "password_hash": data["password"]
    }).inserted_id

    return jsonify({"message": "User added", "id": str(user_id)}), 201
