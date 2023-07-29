# Flask-Application

## About
This project demonstrates a simple Flask application that integrates with MongoDB to provide a RESTful API for performing CRUD (Create, Read, Update, Delete) operations on a collection of resources.

## ✨ Demo

![Demo](https://github.com/divyanshkumarworks/Flask-Application/assets/134360630/0e91c1e4-2183-4f03-b1e3-1e757187b116)


## Getting Started: 🚀

### Prerequisites 📋
Before running the application, ensure you have the following installed:

- Python (version 3.6 or higher)
- Flask (version 2.0.0 or higher)
- pymongo (version 3.11.4 or higher)
- MongoDB (version 4.4 or higher)

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Installation
1. Clone this repository
 ```bash
 https://github.com/divyanshkumarworks/Flask-Application.git
 ```
2. go inside clone folder
 ```bash
 cd Flask-Application
```
3. Create a Virtual Environment
 ```bash
 python -m venv venv
 ```
4. Activate the environment
 ```bash
 source /venv/bin/activate
 ``` 
5. install all dependencies:
```bash
python -m pip install -r requirements.txt
```

6. Run the Flask application.
```bash
python app.py
```
The application will be accessible at http://localhost:5000.

**Note**: This project need a ```Mongodb atlas``` account for accessing the database. you can create your MongoDB atlas account in official MongoDB website here: [https://www.mongodb.com/basics/mongodb-atlas-tutorial](https://www.mongodb.com/basics/mongodb-atlas-tutorial)

## API Endpoints

The following API endpoints are available:

1. `POST /users` Create a new user. (Request body should contain the resource data in JSON format.)
2. `GET /users` Fetch all users from the database.
3. `GET /users/<id>` Fetch a specific user by its unique identifier (ID).
4. `DELETE /users/<id>` Delete a user with the specified ID.
5. `PUT /users/<id>` Update an existing user identified by its ID. (Request body should contain the updated resource data in JSON format.)

## Acknowledgments
Special thanks to the Flask and MongoDB communities for their excellent documentation and resources.

If you have any questions or issues, please feel free to open an issue on the repository. Happy coding!
