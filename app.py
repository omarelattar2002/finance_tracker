from dotenv import load_dotenv
from flask import Flask, jsonify, request
import os
import boto3
from routes.transactions import transactions_bp, init_table

load_dotenv()

aws_access_key = os.environ["aws_access_key"]
aws_secret_access_key = os.environ["aws_secret_access_key"]

session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name="us-east-1"
)

dynamodb = session.resource("dynamodb")
table = dynamodb.Table("finance_tracker")
init_table(table)

app = Flask(__name__)

from routes.transactions import transactions_bp
app.register_blueprint(transactions_bp)

@app.route("/")
def home():
    data = table.scan()
    return jsonify(data["Items"])




if __name__ == "__main__":
    app.run(debug=True)
