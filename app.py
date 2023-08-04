from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from bson import json_util
import json
import re

client = MongoClient("mongodb+srv://johnybravo2404:%40bcd1234@cluster0.ikxf9ss.mongodb.net/?retryWrites=true&w=majority")
db = client["Users"]
collection = db["profile"]

app = Flask(__name__)
api = Api(app)


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_name(name):
    return bool(name.strip())

def is_valid_password(password):
    return len(password) >= 6

user_parser = reqparse.RequestParser()
user_parser.add_argument("name", type=str, required=True, help="Name is required.")
user_parser.add_argument("email", type=str, required=True, help="Email is required.")
user_parser.add_argument("password", type=str, required=True, help="Password is required.")

class UserResource(Resource):
    
    def get(self, user_id):
        user = collection.find_one({"_id": int(user_id)})
        if user:
            return user, 200
        else:
            return {"message": "User not found"}, 404

    def put(self, user_id):
        user = collection.find_one({"_id": int(user_id)})
        if not user:
            return {"message": "User not found"}, 404

        data = user_parser.parse_args()

        if not is_valid_name(data["name"]):
            return {"message": "Invalid name"}, 400
        if not is_valid_email(data["email"]):
            return {"message": "Invalid email"}, 400
        if not is_valid_password(data["password"]):
            return {"message": "Invalid password (should be at least 6 characters)"}, 400

        existing_user = collection.find_one({"email": data["email"], "id": {"$ne": int(user_id)}})
        if existing_user:
            return {"message": "Email or id already in use"}, 409

        collection.update_one({"_id": int(user_id)}, {"$set": {"email": data["email"], "name": data["name"], "password": data["password"]}})
        data["id"] = user_id
        return data, 200

    def delete(self, user_id):
        result = collection.delete_one({"_id": int(user_id)})
        if result.deleted_count > 0:
            return {"message": "User deleted successfully"}, 200
        else:
            return {"message": "User not found"}, 404

class UsersResource(Resource):
    def get(self):
        user = collection.find({})
        if user:
            return [json.loads(json.dumps(doc, default=str)) for doc in user], 200
        else:
            return {"Users not found"}, 400

    def post(self):
        user_parser.add_argument("id", type=str)
        data = user_parser.parse_args()

        if not is_valid_name(data["name"]):
            return {"message": "Invalid name"}, 400
        if not is_valid_email(data["email"]):
            return {"message": "Invalid email"}, 400
        if not is_valid_password(data["password"]):
            return {"message": "Invalid password (should be at least 6 characters)"}, 400

        existing_user = collection.find_one({"email": data["email"], "id": {"$ne": int(data["id"])}})
        if existing_user:
            return {"message": "Email or id already in use"}, 409

        collection.insert_one({"_id": int(data["id"]), "email": data["email"], "name": data["name"], "password": data["password"]})

        return data, 201

api.add_resource(UserResource, "/users/<string:user_id>")
api.add_resource(UsersResource, "/users")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
	

