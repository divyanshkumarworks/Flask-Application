from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
print(client)
Users = client["Users"]
Profile = Users["profile"]

@app.route("/users", methods=["POST"])
def create_new_user():
	json = request.json
	id = json["id"]
	name = json["name"]
	email = json["email"]
	password = json["password"]
	if request.method == "POST" and id and name and email and password:
		post = {"_id": id, "name": name, "email": email, "password": password}
		Profile.insert_one(post)
		return jsonify("user created sucessfully")

@app.route("/users")
def users():
	users = Profile.find()
	return dumps(users)

@app.route("/users/<id>")
def search_user(id):
	user = Profile.find_one({"_id": int(id)})
	return dumps(user)

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
	user = Profile.delete_one({"_id": int(id)})
	return jsonify("user deleted sucessfully")

@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
	json = request.json
	id = int(id)
	name = json["name"]
	email = json["email"]
	password = json["password"]
	if request.method == "PUT" and id and name and email and password:
		Profile.update_one({"_id": id}, {"$set":{"name": name, "email": email, "password": password}})
		return jsonify("user updated sucessfully")

if __name__ == "__main__":
	app.run(debug=True)
	

