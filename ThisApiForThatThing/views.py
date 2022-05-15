from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from django.http import JsonResponse
# import models
from .models import ApiModel

# Create your views here.

# connect to mongodb
try:
    password = 'fcPZp2f4ixQ5QJpj'
    databaseName = 'Api'
    client = MongoClient(
        f"mongodb+srv://Architrixs:{password}@cluster0.do1dd.mongodb.net/{databaseName}?retryWrites=true&w=majority")
    db = client['Api']

    collection_ApiForApi = db['ApiForApi']
    collection_MetaData = db['MetaData']
except ServerSelectionTimeoutError:
    print("Server not found")
    exit()


# section for webpage
# main page
class MainPageView(View):
    def get(self, request):
        data = list(collection_ApiForApi.aggregate([{'$sample': {'size': 1}}]))[0]
        print(data)
        # return the data
        return render(request, 'index.html', {'api': data})


# section for api calls
class RandomDataCall(View):
    # returns a random document from the collection_ApiForApi
    def get(self, request):
        data = list(collection_ApiForApi.aggregate([{'$sample': {'size': 1}}]))[0]
        print(data)
        # return the data
        return JsonResponse(data, status=201, safe=False)


class TypeDataCall(View):
    # accepts the string as a GET parameter type and filters the data and returns all the data of that type
    def get(self, request, type):
        print(request.GET)
        data = list(collection_ApiForApi.aggregate([{'$match': {'type': type}}]))
        return JsonResponse(data, status=201, safe=False)


class AllTypes(View):
    # returns all the unique types in data
    def get(self, request):
        # data = list(collection_ApiForApi.distinct('type'))
        data = collection_MetaData.find_one({'name': 'Types'})['value']
        return JsonResponse(data, status=201, safe=False)


class CrudPageViewWithId(View):
    def get(self, request, id) -> HttpResponse:
        oid = id
        data = collection_ApiForApi.find_one({'_id': oid})
        return render(request, 'crud.html', context={'data': data, 'id': oid})


# section for modifying data for admin
class CrudPageView(View):
    # takes 'id' input from page and returns the data with that id
    # here we can modify the data and save it to the database
    def get(self, request):
        # get the id from the page
        oid = 1
        if request.GET.get('id') is not None:
            oid = int(request.GET.get('id'))
        data = collection_ApiForApi.find_one({'_id': oid})
        print(data, oid, id, request)
        # return render(request, 'crud.html', {'data': data, 'id': oid})
        return redirect('crudId', id=oid)

    # post method to save the data
    def post(self, request, id=1):
        # TODO: save the data to the database
        # get the next id from the database
        oid = collection_ApiForApi.find().sort('_id', -1).limit(1)[0]['_id'] + 1
        # get the data from the page
        data = request.POST
        # save the data to the database according to the ApiModel
        ApiModel(oid, data['type'], data['name'], data['description'], data['link'], data['method'], data['parameters'],
                 data['response'], data['status']).save()


class CrudPageViewWithTypes(View):
    def get(self, request):
        # get type from the page
        # get the data from the database
        data = list(collection_ApiForApi.distinct('type'))
        print(data)
        return render(request, 'typeForm.html', {'types': data})

#     update type
    def post(self, request, type):
        data = request.POST
        print(data)
        # update all the data with the type
        collection_ApiForApi.update_many({'type': type}, {'$set': {'type': data['type']}})
        return redirect('crudType', type=data['type'])


# make the api call for meta data
class MetaDataCall(View):
    def get(self, request):
        # get all the data from the database, remove the _id field from each and return the data
        data = list(collection_MetaData.find())
        for i in range(len(data)):
            del data[i]['_id']
        return JsonResponse(data, status=201, safe=False)
