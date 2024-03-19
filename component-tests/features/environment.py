from pymongo import MongoClient


def before_all(context):
    context.base_url = "http://localhost:5000"
    context.mongo_uri = 'mongodb://localhost:27017'

    # Check that mongodb is up
    context.mongo_client = MongoClient(context.mongo_uri)
    mongo_response = context.mongo_client.admin.command('ping')
    assert mongo_response == {'ok': 1.0}


def after_all(context):
    context.mongo_client.close()
