from flask import Blueprint, jsonify, request
from backend.extensions import mongo
from bson.objectid import ObjectId

transactions_bp = Blueprint("transactions", __name__)



@transactions_bp.route("/", methods=["GET"])
def get_transactions():
    transactions = mongo.db.transactions.find()
    transacion_list = [{"_id": str(t["_id"]), "user_id": str(t["user_id"]),
                        "category_id": str(t["category_id"]),"amount": t["amount"], "description": t.get("description", ""), "date": t["date"]} for t in transactions]
    return jsonify(transacion_list), 200


@transactions_bp.route("/", methods=["POST"])
def add_transaction():
    data = request.json
    if not data or "user_id" not in data or "category_id" not in data or "amount" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    transaction_id = mongo.db.transactions.insert_one({
        "user_id": ObjectId(data["user_id"]), 
        "category_id": ObjectId(data["category_id"]),
        "amount": data["amount"],
        "description": data.get("description", ""),
        "date": data["data"]
    }).inserted_id

    return jsonify({"message": "Transaction added", "id": str(transaction_id)}), 201
        