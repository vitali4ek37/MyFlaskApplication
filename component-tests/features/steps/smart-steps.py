import random
import requests
from behave import given, when, then


@given(u'a Create User request')
def step_impl(context):
    context.email = f"test{random.randint(3, 1000)}@vodafone.com"
    context.request_body = {
        "username": "test",
        "password": "password",
        "email": context.email,
        "name": "John",
        "lastname": "Snow",
        "phone": "1234567890"
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
    search_email = context.email
    # Find user with matching email
    user = collection.find_one({"email": search_email})
    if user:
        print(f"User with email '{search_email}' found!")
    else:
        print(f"User with email '{search_email}' not found.")
    assert user is not None


@then(u'can be obtained by API')
def step_impl(context):
    params = {
        "emails": context.email
    }
    response = requests.get(url=f"{context.base_url}/users", params=params)
    assert response.status_code == 200
    assert response.json()[0]['email'] == context.email

    params = {
        "name": "John"
    }
    response = requests.get(url=f"{context.base_url}/users", params=params)
    assert response.status_code == 200
    assert response.json()[0]['name'] == 'John'
