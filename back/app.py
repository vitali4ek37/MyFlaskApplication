import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

client = MongoClient('mongodb://mongo:27017')
db = client['my_database']
collection = db['users']

MANDATORY_FIELDS = ["email", "name"]


@app.route("/users", methods=["POST"])
@cross_origin()
def handle_user_creation():
    user_data = request.json
    missing_fields = [field for field in MANDATORY_FIELDS if field not in user_data]
    if missing_fields:
        return f"Missing mandatory fields: {', '.join(missing_fields)}", 400
    else:
        found_user = collection.find_one({"email": user_data["email"]})
        found_user_json = json.loads(dumps(found_user))

        if found_user_json is not None:
            return "User with provided email already exists", 400

        allowed_fields = ["email", "name", "lastname", "phone_number", "country"]
        filtered_user_data = {}
        for field in user_data:
            if field in allowed_fields:
                filtered_user_data[field] = user_data[field]
                # filtered_user_data.update({field: user_data[field]})
        collection.insert_one(filtered_user_data)
        return "User created successfully", 201


@app.route("/users", methods=["GET"])
@cross_origin()
def get_users():
    allowed_fields = ["email", "name", "lastname", "phone_number", "country"]
    if "email" in request.args and "name" in request.args:
        email = request.args.get("email")
        name = request.args.get("name")
        user = collection.find_one({"name": name, "email": email})
        user_ready = None
        if user is not None:
            user_ready = {key: user[key] for key in user if key in allowed_fields}
            return user_ready
        else:
            return "You should specify a valid search criteria", 400
    elif "email" in request.args:
        email = request.args.get("email")
        user = collection.find_one({"email": email})
        user_ready = None
        if user is not None:
            user_ready = {key: user[key] for key in user if key in allowed_fields}
            return user_ready
        else:
            return "You should specify a valid search criteria", 400
    elif "name" in request.args:
        name = request.args.get("name")
        user = collection.find_one({"name": name})
        user_ready = None
        if user is not None:
            user_ready = {key: user[key] for key in user if key in allowed_fields}
            return user_ready
        else:
            return "You should specify a valid search criteria", 400
    else:
        return "You should specify at least one query parameter", 400


@app.route("/users", methods=["PUT", "PATCH", "UPDATE", "DELETE"])
@cross_origin()
def filter_request_types():
    return 'Method not allowed', 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
