from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
print(client)
Users = client["Users"]
Porfile = Users["profile"]

if __name__ == "__main__":
	app.run(debug=True)
	

