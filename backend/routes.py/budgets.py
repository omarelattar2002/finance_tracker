from flask import Blueprint, jsonify, request
from backend.extensions import mongo
from bson.objectid import ObjectId

budgets_bp = Blueprint("budgets", __name__)

@budgets_bp.route("/", methods=["GET"])
def get_budgets():
    budgets = mongo.db.budgets.find()
    budget_list = [{"_id": str(b["_id"]), "user_id": str(b["user_id"]), "category_id": str(b["category_id"]),
                    "limit_amt": b["limit_amt"], "start_date": b["start_date"], "end_date": b["end_date"]} for b in budgets]
    return jsonify(budget_list), 200

@budgets_bp.route("/", methods=["POST"])
def add_budget():
    data = request.json
    if not data or "user_id" not in data or "category_id" not in data or "limit_amt" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    budget_id = mongo.db.budgets.insert_one({
        "user_id": ObjectId(data["user_id"]),
        "category_id": ObjectId(data["category_id"]),
        "limit_amt": data["limit_amt"],
        "start_date": data["start_date"],
        "end_date": data["end_date"]
    }).inserted_id

    return jsonify({"message": "Budget added", "id": str(budget_id)}), 201
