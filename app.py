import json
from flask import Flask, request
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
client = MongoClient('mongodb://mongo:27017')
db = client['my_database']
collection = db['users']

MANDATORY_FIELDS = ["email", "name", "lastname"]


@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        if "emails" in request.args:
            emails = request.args.getlist("emails")
            users = collection.find({"email": {"$in": emails}})
            return json.loads(dumps(users))
        elif "name" in request.args:
            name = request.args.get("name")
            users = collection.find({"name": name})
            return json.loads(dumps(users))
        else:
            users = collection.find()
            json_obj = json.loads(dumps(users))
            return json_obj
    elif request.method == 'POST':
        user_data = request.json
        missing_fields = [field for field in MANDATORY_FIELDS if field not in user_data]
        if missing_fields:
            return f"Missing mandatory fields: {', '.join(missing_fields)}", 400
        collection.insert_one(user_data)
        return 'User created successfully!', 201
    return 'Method not allowed', 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
