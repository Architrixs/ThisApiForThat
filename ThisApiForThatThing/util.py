from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from django.conf import settings
import django
import os
import hashlib
import hmac
# connect to mongodb
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ApiForApi.settings')
    if settings:
        password = settings.PASSWORD
        databaseName = settings.NAME
        client = MongoClient(
            f"mongodb+srv://Architrixs:{password}@cluster0.do1dd.mongodb.net/{databaseName}?retryWrites=true&w=majority")
        db = client['Api']

        collection_ApiForApi = db['ApiForApi']
        collection_MetaData = db['MetaData']
        collection_Counter = db['Counter']

except ServerSelectionTimeoutError:
    print("Server not found")
    exit()


def getNextSequence(name: str):
    """
    Get the next sequence for the given collection. Generates next _Id.
    """
    newSequence = collection_Counter.find_one_and_update(
        {'name': name},
        {'$inc': {'seq': 1}},
    )
    return newSequence['seq']


def hash_new_password(password: str):
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.
    """
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt, pw_hash


def is_correct_password(salt: bytes, pw_hash: bytes, password: str) -> bool:
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    return hmac.compare_digest(
        pw_hash,
        hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    )

