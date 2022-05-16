from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# connect to mongodb
try:
    password = 'fcPZp2f4ixQ5QJpj'
    databaseName = 'Api'
    client = MongoClient(
        f"mongodb+srv://Architrixs:{password}@cluster0.do1dd.mongodb.net/{databaseName}?retryWrites=true&w=majority")
    db = client['Api']

    collection_ApiForApi = db['ApiForApi']
    collection_MetaData = db['MetaData']
    collection_Counter = db['Counter']

except ServerSelectionTimeoutError:
    print("Server not found")
    exit()


def getNextSequence(name):
    newSequence = collection_Counter.find_one_and_update(
        {'name': name},
        {'$inc': {'seq': 1}},
    )
    return newSequence['seq']



