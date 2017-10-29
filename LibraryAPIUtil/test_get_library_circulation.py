#!/usr/bin/env python3
from library_api_util import *
import json

# This variable is to decide how many nearest libraries you will look for.
LIBRARY_API_SEARCH_NUM = 5

try:
    with open('apikey.json', 'r') as f:
        api_data = json.load(f)
    book_status_json = LibraryBookStatusJSON();
    params = {
        'appkey' : api_data['library_api_key'],
        'isbn' : '4577002086',
        'systemid' : 'Tokyo_Sumida',
        'format' : 'json',
        'callback' : '',
    }
    data = book_status_json.getLibkey(params)
    print('libkey is the following : ')
    if 'libkey' in data:
        print(data['libkey'])
    else:
        print('\'libkey\' is not on the Library API callback list.')

except json.decoder.JSONDecodeError as e:
    print("JSON Decode Error: {}".format(e))

except:
    print("Unknown Error: ", sys.exc_info()[0])
    raise
