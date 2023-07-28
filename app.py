from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/Users"
mongo = PyMongo(app)

@app.route("/users", methods=["POST"])
def create_new_user():
	json = request.json
	id = json["id"]
	if mongo.db.profile.find_one({"_id": int(id)}):
		return jsonify("user id already exists")
	else:
		name = json["name"]
		email = json["email"]
		password = json["password"]
		if request.method == "POST" and id and name and email and password:
			post = {"_id": int(id) , "name": name, "email": email, "password": password}
			mongo.db.profile.insert_one(post)
			return jsonify("user created sucessfully")
		else:
			resp = jsonify({"message": "not found"})
			resp.status_code = 404
			return resp

@app.route("/users")
def users():
	users = mongo.db.profile.find()
	return dumps(users)

@app.route("/users/<id>")
def search_user(id):
	user = mongo.db.profile.find_one({"_id": int(id)})
	if user:
		return dumps(user)
	else:
		resp = jsonify({"message": "user not found"})
		resp.status_code = 404
		return resp

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
	if mongo.db.profile.find_one({"_id": int(id)}):
		mongo.db.profile.delete_one({"_id": int(id)})
		resp = jsonify("user deleted sucessfully")
		return resp
	else:
		resp = jsonify({"message": "user not found"})
		resp.status_code = 404
		return resp


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
	json = request.json
	name = json["name"]
	email = json["email"]
	password = json["password"]
	if mongo.db.profile.find_one({"_id": int(id)}) and request.method == "PUT" and id and name and email and password:
		mongo.db.profile.update_one({"_id": int(id)}, {"$set":{"name": name, "email": email, "password": password}})
		return jsonify("user updated sucessfully")

	else:
		resp = jsonify({"message": "user id not found"})
		resp.status_code = 404
		return resp

if __name__ == "__main__":
	app.run(debug=True)
	

