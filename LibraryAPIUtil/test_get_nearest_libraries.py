#!/usr/bin/env python3
from library_api_util import *
import json

# This variable is to decide how many nearest libraries you will look for.
LIBRARY_API_SEARCH_NUM = 5

try:
    with open('apikey.json', 'r') as f:
        api_data = json.load(f)
    library_list_json = LibraryListJSON();
    params_1 = {
        'appkey' : api_data['library_api_key'],
        'pref' : '東京都',
        'city' : '千代田区',
        'format' : 'json',
        'callback' : '',
        'limit' : LIBRARY_API_SEARCH_NUM,
    }
    params_2 = {
        'appkey' : api_data['library_api_key'],
        'geocode' : '139.8,35.7',
        'format' : 'json',
        'callback' : '',
        'limit' : LIBRARY_API_SEARCH_NUM,
    }
    data = library_list_json.getLibraryData(params_2)
    print('The nearest library data are the following : ')
    print(data[0])
    print('The nearest 5 libraries data are the following : ')
    for datum in data:
        print(datum)



except json.decoder.JSONDecodeError as e:
    print("JSON Decode Error: {}".format(e))

except:
    print("Unknown Error: ", sys.exc_info()[0])
    raise
