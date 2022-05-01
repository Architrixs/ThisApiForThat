# Author: Architrixs, 30/04/2022
# Description: Scrapes data from the various sources of free/public APIs and stores it in a MongoDB database
# Usage: python3 ApiDataScraper.py

# import libraries
import requests
import json
import time
import re
import pprint
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

pp = pprint.PrettyPrinter(indent=4)
# api data model
dataModel = {
    "_id": 0,
    "name": "",
    "link": "",
    "description": "",
    "type": "",
    "tryMe": "",
    "auth": "",
    "working": 1,
}

# make a connection to the MongoDB database
password = 'fcPZp2f4ixQ5QJpj'
databaseName = 'Api'
client = MongoClient(f"mongodb+srv://Architrixs:{password}@cluster0.do1dd.mongodb.net/{databaseName}?retryWrites=true&w=majority")

# check if the connection is successful
try:
    client.admin.command('ismaster')
except ServerSelectionTimeoutError:
    print('Server not available')
    exit()

# get the database
dbAPI = client['Api']['ApiForApi']
print(dbAPI.find_one())

# scrape data from the various sources

# ------------------------------------ #
# from 'https://raw.githubusercontent.com/public-apis/public-apis/master/README.md
# ------------------------------------ #

""" 
#DONE count = 1420
# get the list of APIs
url = 'https://raw.githubusercontent.com/public-apis/public-apis/master/README.md'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())
typesExp = re.compile("### (.*)")
nameAndLinkExp = re.compile("\[(.*)\]\((.*)\)")
expresion = re.compile("\| (.*)\|")
types = re.findall(typesExp, soup.prettify())
search = re.findall(expresion, soup.prettify())
print(search[1])
print(types, len(types))
count = 0
index = 1
for api in search[1:]:
    # split using '|'
    # if (api == "Description | Auth | HTTPS | CORS "):
    #     count = count + 1
    data = api.split('|')
    print(api, data)
    # get the name and link
    nameAndLink = nameAndLinkExp.search(data[0])
    if nameAndLink is not None:
        dataModel['_id'] = index
        dataModel['name'] = nameAndLink.group(1)
        dataModel['link'] = nameAndLink.group(2)
        dataModel['description'] = data[1] if len(data) >1 else ""
        dataModel['type'] = types[count]
        dataModel['tryMe'] = nameAndLink.group(2)
        dataModel['auth'] = data[2] if len(data) >2 else ""
        dataModel['working'] = 1
        pp.pprint(dataModel)
        # sleep for a bit
        time.sleep(1)
        dbAPI.insert_one(dataModel)
        index = index + 1
"""

# dbAPI.update_many(
#   {},
#   {"$set": {"working": 1}}
# )

# ------------------------------------ #
# from https://mixedanalytics.com/blog/list-actually-free-open-no-auth-needed-apis/
# ------------------------------------ #

"""
url = 'https://mixedanalytics.com/blog/list-actually-free-open-no-auth-needed-apis/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
#print(soup.prettify())

# get all tr elements
trs = soup.find_all('tr')
print(trs[1].prettify())
print(trs[1].text)
print("name", trs[1].find_all('a')[0].text)
print("link", trs[1].find_all('a')[0].get('href'))
print("description", trs[1].find_all('td')[2].text)
print("tryme", trs[1].find_all('a')[1].text)
index = 1421
for tr in trs[1:]:
    data = tr.find_all('a')
    description = tr.find_all('td')[2].text
    dataModel['_id'] = index
    dataModel['name'] = data[0].text
    dataModel['link'] = data[0].get('href')
    dataModel['description'] = description
    dataModel['type'] = 'Miscellaneous'
    dataModel['tryMe'] = data[1].text
    dataModel['auth'] = 'No'
    dataModel['working'] = 1
    pp.pprint(dataModel)
    # sleep for a bit
    time.sleep(1)
    # check if same name exists
    if dbAPI.find_one({"name": dataModel['name']}) is None:
        dbAPI.insert_one(dataModel)
    else:
        print("already exists", dataModel['name'])
    index = index + 1
"""
remaining_ids = [1421,1422,1423,1423,1424,14251428,1429,1431,1432,1433,1434,1435,1436,1437,1441,1442,1443,1445,1446,1447,1448,1449,1450,1451,1453,1454,1456,1455,1458,1459,1460,1461,1462,1464,1467,1469,1470,1471,1472,1473,1474,1479]
