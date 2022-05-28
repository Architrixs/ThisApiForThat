import requests
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from django.http import JsonResponse
import json
from .models import ApiModel
import ThisApiForThatThing.util as util

# Create your views here.
baseUrl = "http://localhost:8000"
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
        # return the data
        return render(request, 'index.html', {'api': data})


# section for api calls
class RandomDataCall(View):
    # returns a random document from the collection_ApiForApi
    def get(self, request):
        data = list(collection_ApiForApi.aggregate([{'$sample': {'size': 1}}]))[0]
        # return the data
        return JsonResponse(data, status=201, safe=False)


class TypeDataCall(View):
    # accepts the string as a GET parameter type and filters the data and returns all the data of that type
    def get(self, request, type):
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
        return redirect('crudId', id=oid)

    # post method to save the data
    def post(self, request):
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
        return render(request, 'typeForm.html', {'types': data})

#     update type
    def post(self, request):
        type = request.POST.get('type')
        original_type = request.POST.get('original_type')
        # update all the data with the type
        collection_ApiForApi.update_many({'type': original_type}, {'$set': {'type': type}})
        return redirect('crudTypes')


# make the api call for meta data
class MetaDataCall(View):
    def get(self, request):
        # get all the data from the database, remove the _id field from each and return the data
        data = list(collection_MetaData.find())
        for i in range(len(data)):
            del data[i]['_id']
        return JsonResponse(data, status=201, safe=False)


class CrudPageViewWithMetaData(View):
    def get(self, request):
        data = requests.get(baseUrl + '/api/meta/')
        # prettyfy the json
        data = json.dumps(data.json(), indent=4, sort_keys=True)
        return render(request, 'meta.html', {'data': data})

    def post(self, request):
        typeData = list(collection_ApiForApi.distinct('type'))
        # get total number of types
        totalTypes = len(typeData)
        # get total number of api
        totalApi = collection_ApiForApi.count_documents({})

        # update the data in the database
        temp = list(collection_MetaData.find({'name': 'Types'}))
        collection_MetaData.update_one({'name': 'Types'}, {'$set': {'value': typeData}})
        collection_MetaData.update_one({'name': 'TotalTypes'}, {'$set': {'value': totalTypes}})
        collection_MetaData.update_one({'name': 'Count'}, {'$set': {'value': totalApi}})
        return redirect('crudMeta')


class CrudPageViewWithAuths(View):
    def get(self, request):
        data = list(collection_ApiForApi.distinct('auth'))
        return render(request, 'authForm.html', {'auths': data})

#     update type
    def post(self, request):
        auth = request.POST.get('auth')
        original_auth = request.POST.get('original_auth')
        # update all the data with the auth
        collection_ApiForApi.update_many({'auth': original_auth}, {'$set': {'auth': auth}})
        return redirect('crudAuths')


class AboutPageView(View):
    def get(self, request):
        # get meta data
        data = requests.get(baseUrl + '/api/meta/').json()
        # form a key, value pair from all the dicts in data list
        metaData = {d['name']: d['value'] for d in data}
        return render(request, 'about.html', {'data': metaData})

