from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
print(client)
Users = client["Users"]
Porfile = Users["profile"]

@app.route("/users", methods=["POST"])
def create_new_user():
	json = request.json
	id = json["id"]
	name = json["name"]
	email = json["email"]
	password = json["password"]
	if request.method == "POST" and id and name and email and password:
		post = {"_id": id, "name": name, "email": email, "password": password}
		Porfile.insert_one(post)
		return jsonify("user created sucessfully")


if __name__ == "__main__":
	app.run(debug=True)
	

