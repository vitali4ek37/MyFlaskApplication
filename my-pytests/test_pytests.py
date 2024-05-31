import random

import requests
from pymongo import MongoClient

base_url = "http://localhost:5000"
mongo_uri = 'mongodb://localhost:27017'
mongo_client = MongoClient(mongo_uri)
allowed_fields = ["email", "name", "lastname", "phone_number", "country"]


def test_successful_user_creation():
    email = f"test{random.randint(3, 1000)}@vodafone.com"
    request_body = {
        "email": email,
        "name": "John",
        "lastname": "Snow",
        "phone_number": "1234567890",
        "country": "Spain",
        "password": "password"
    }
    headers = {
        'ContentType': 'application/json'
    }
    response = requests.post(url=f"{base_url}/users", json=request_body, headers=headers)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201

    client = mongo_client  # Adjust host and port if needed
    db = client['my_database']
    collection = db['users']
    # Find user with matching email
    user = collection.find_one({"email": email})
    assert user is not None
    for key, value in request_body.items():
        if key in allowed_fields:
            assert value == user[key]
        else:
            assert key not in user.keys()
