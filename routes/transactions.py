from flask import Blueprint, request, jsonify
import uuid
import datetime
import datetime

transactions_bp = Blueprint("transactions", __name__)
dynamodb_table = None


def init_table(table_ref):
    global dynamodb_table
    dynamodb_table = table_ref


@transactions_bp.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()

    required_fields = ["amount", "category", "type", "description"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    

    transaction_item = {
        "id": str(uuid.uuid4()),  # required partition key
        "amount": data["amount"],
        "category": data["category"],
        "type": data["type"],
        "description": data["description"],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    print(transaction_item)

    
    try:
        dynamodb_table.put_item(Item=transaction_item)
        return jsonify({"message": "Transaction added", "item": transaction_item}), 201
    except Exception as e:
        return jsonify({"message":str(e)}), 500