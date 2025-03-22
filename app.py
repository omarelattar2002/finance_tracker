from dotenv import load_dotenv
from flask import Flask, jsonify
from pymongo import MongoClient
import os
import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from boto3.dynamodb.conditions import Key



load_dotenv()
aws_access_key = os.environ["aws_access_key"]
aws_secret_access_key = os.environ["aws_secret_access_key"]
session = boto3.Session(aws_access_key_id = aws_access_key, aws_secret_access_key = aws_secret_access_key, region_name="us-east-1")
dynamodb = session.resource("dynamodb")
app = Flask(__name__)



table = dynamodb.Table("table_test")


# def dynamo_to_python(dynamo_objects: list) -> list:
#     deserializer = TypeDeserializer()
#     return [
#         {k: deserializer.deserialize(v) for k, v in item.items()}
#         for item in dynamo_objects if isinstance(item, dict) and item
#     ]

@app.route("/")
def home():
    data = table.scan()
    json_data = (data["Items"])
    return json_data


if __name__ == "__main__":
    app.run(debug=True)
