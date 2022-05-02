from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from django.http import JsonResponse
# Create your views here.

# connect to mongodb
try:
    password = 'fcPZp2f4ixQ5QJpj'
    databaseName = 'Api'
    client = MongoClient(f"mongodb+srv://Architrixs:{password}@cluster0.do1dd.mongodb.net/{databaseName}?retryWrites=true&w=majority")
    db = client['Api']

    collection = db['ApiForApi']
    print(collection.find_one())
except ServerSelectionTimeoutError:
    print("Server not found")
    exit()


# main page
class MainPageView(View):
    def get(self, request):
        data = list(collection.aggregate([{'$sample': {'size': 1}}]))[0]
        print(data)
        # return the data
        return render(request, 'index.html', {'api': data})


class RandomDataView(View):
    def get(self, request):
        print(request.GET)
        data = list(collection.aggregate([{'$sample': {'size': 1}}]))[0]
        print(data)
        # return the data
        return JsonResponse(data, status=201, safe=False)
