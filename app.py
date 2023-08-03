from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import re

# Connect to MongoDB Atlas using the connection string
client = MongoClient("mongodb+srv://johnybravo2404:%40bcd1234@cluster0.ikxf9ss.mongodb.net/?retryWrites=true&w=majority")
db = client["Users"]
collection = db["profile"]

app = Flask(__name__)
api = Api(app)

# Custom validation functions for email, name, and password

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_name(name):
    return bool(name.strip())

def is_valid_password(password):
    return len(password) >= 6

# Request parser for handling incoming data
user_parser = reqparse.RequestParser()
user_parser.add_argument("id", type=str)
user_parser.add_argument("name", type=str, required=True, help="Name is required.")
user_parser.add_argument("email", type=str, required=True, help="Email is required.")
user_parser.add_argument("password", type=str, required=True, help="Password is required.")

# User resource
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = collection.find_one({"_id": int(user_id)})
            if user:
                return user, 200
            else:
                return {"message": "User not found"}, 404
        else:
            users = list(collection.find({}, {"_id": 0}))
            return users, 200

    def post(self):
        data = user_parser.parse_args()

        # Validate data
        if not is_valid_name(data["name"]):
            return {"message": "Invalid name"}, 400
        if not is_valid_email(data["email"]):
            return {"message": "Invalid email"}, 400
        if not is_valid_password(data["password"]):
            return {"message": "Invalid password (should be at least 6 characters)"}, 400

        # Check if the id is already in use
        existing_user = collection.find_one({"email": data["email"], "id": {"$ne": int(data["id"])}})
        if existing_user:
            return {"message": "Email or id already in use"}, 409

        # Generate a unique ID for the new user
        collection.insert_one({"_id": int(data["id"]), "email": data["email"], "name": data["name"], "password": data["password"]})

        return data, 201

    def put(self, user_id):
        user = collection.find_one({"_id": int(user_id)})
        if not user:
            return {"message": "User not found"}, 404

        data = user_parser.parse_args()

        # Validate data
        if not is_valid_name(data["name"]):
            return {"message": "Invalid name"}, 400
        if not is_valid_email(data["email"]):
            return {"message": "Invalid email"}, 400
        if not is_valid_password(data["password"]):
            return {"message": "Invalid password (should be at least 6 characters)"}, 400

        # Check if the updated email is already in use by another user
        existing_user = collection.find_one({"email": data["email"], "id": {"$ne": int(user_id)}})
        if existing_user:
            return {"message": "Email or id already in use"}, 409

        # Update the user in the database
        collection.update_one({"id": int(user_id)}, {"$set": data})
        data["id"] = user_id
        return data, 200

    def delete(self, user_id):
        result = collection.delete_one({"id": int(user_id)})
        if result.deleted_count > 0:
            return {"message": "User deleted successfully"}, 200
        else:
            return {"message": "User not found"}, 404

# Add the User resource to the API
api.add_resource(UserResource, "/users", "/users/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True)
	

