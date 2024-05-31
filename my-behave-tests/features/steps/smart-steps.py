import json
import random
import requests
from behave import given, when, then
from pymongo import MongoClient
from bson.json_util import dumps


@given(u'a Create User request')
def step_impl(context):
    context.email = f"test{random.randint(3, 1000)}@vodafone.com"
    context.request_body = {
        "email": context.email,
        "name": "John",
        "lastname": "Snow",
        "phone_number": "1234567890",
        "country": "Spain",
        "password": "password"
    }

    context.headers = {
        'ContentType': 'application/json'
    }


@when(u'request is sent')
def step_impl(context):
    response = requests.post(url=f"{context.base_url}/users", json=context.request_body, headers=context.headers)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201


@then(u'new user appears in the database')
def step_impl(context):
    client = context.mongo_client  # Adjust host and port if needed
    db = client['my_database']
    collection = db['users']
    # Find user with matching email
    user = collection.find_one({"email": context.email})
    if user:
        print(f"User with email '{context.email}' found!")
    else:
        print(f"User with email '{context.email}' not found.")
    assert user is not None


@then(u'can be obtained by API')
def step_impl(context):
    params = {
        "email": context.email
    }
    response = requests.get(url=f"{context.base_url}/users", params=params)
    assert response.status_code == 200
    assert response.json()['email'] == context.email
