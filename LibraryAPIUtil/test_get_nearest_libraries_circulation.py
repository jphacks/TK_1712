#!/usr/bin/env python3
from library_api_util import *
import json

# This variable is to decide how many nearest libraries you will look for.

LATITUDE = 35.7
LONGTITUDE = 139.8
ISBN = '4577002086'
LIBRARY_API_SEARCH_NUM = 5

try:
    with open('apikey.json', 'r') as f:
        api_data = json.load(f)
    library_api = LibraryAPI()
    data = library_api.get(api_data, LATITUDE, LONGTITUDE, ISBN, LIBRARY_API_SEARCH_NUM)
    print(data)
    f = open('json/sample2.json', 'w')
    f.write(json.dumps(data, ensure_ascii=False, indent=4))
    f.close()
except json.decoder.JSONDecodeError as e:
    print("JSON Decode Error: {}".format(e))

except:
    print("Unknown Error: ", sys.exc_info()[0])
    raise
