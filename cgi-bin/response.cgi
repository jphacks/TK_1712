#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi, cgitb, sys, json
sys.path.append('getIsbnAndInfo')
sys.path.append('LibraryAPIUtil')
from getIsbnAndInfo import GetIsbn
from getIsbnAndInfo import searchBook
from library_api_util import LibraryAPI

cgitb.enable()

form = cgi.FieldStorage()
text = form.getfirst("text")
filepath = form.getfirst("filepath")
latitude = form.getfirst("latitude")
longtitude = form.getfirst("lontitude")
if (latitude is None):
    latitude = 35.7
if (longtitude is None):
    longtitude = 139.8
print(latitude)
print(longtitude)
sequence_list = []

# keywords = ["harry", "potter"]
keywords = getkeywords.make_keywords_from_photo()

with open('json/keywords.json', 'w') as f:
    f.write(json.dumps(keywords, ensure_ascii=False, indent=4))

isbn = GetIsbn()
shoopingInfo = searchBook()

isbnList = isbn.useGoogleApi(keywords)
if (len(isbnList) <= 0):
    isbnList = ['4577002086'] + isbnList
data = shoopingInfo.yapiKeywords(keywords)
print(isbnList)

with open('json/sample.json', 'w') as f:
    f.write(json.dumps(data, ensure_ascii=False, indent=4))

with open('apikey.json', 'r') as f:
    api_data = json.load(f)
library_api = LibraryAPI()
data = library_api.get(api_data, float(latitude), float(longtitude), isbnList[0], 5)

with open('json/sample2.json', 'w') as f:
    f.write(json.dumps(data, ensure_ascii=False, indent=4))

print('Content-type: text/html\nAccess-Control-Allow-Origin: *\n')
#print('{} {}'.format(latitude, longtitude))
print(form)
