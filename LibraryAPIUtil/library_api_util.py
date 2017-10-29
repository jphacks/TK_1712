#!/usr/bin/env python3
import sys
import urllib.request
import json

class LibraryAPI:
    """
## INPUT
        latitude : geometry parameter (ex 137)
        longtitude : geometry parameter (ex 35)
        isbn : 10 or 13 digit number (ex 4577002086)
        library_search_num : how many library result you want to get (ex 5)
## OUTPUT
        Library circulation status will be returned
    """
    def get(self, api_data, latitude, longtitude, isbn, library_search_num):
        str_ = str(longtitude) + ',' + str(latitude)
        params = {
            'appkey' : api_data['library_api_key'],
            'geocode' : str_,
            'format' : 'json',
            'callback' : '',
            'limit' : library_search_num,
        }
        library_list_json = LibraryListJSON();
        library_list = library_list_json.getLibraryData(params)

        result = []
        for i in range(0, int(library_search_num)):
            params = {
                'appkey' : api_data['library_api_key'],
                'isbn' : str(isbn),
                'systemid' : library_list[i]['systemid'],
                'format' : 'json',
                'callback' : '',
            }
            book_status_json = LibraryBookStatusJSON()
            book_status = book_status_json.getLibkey(params)
            library_list[i].update(book_status)
            result.append(library_list[i])
        return result

class LibraryListJSON:
    m_base_url = 'https://api.calil.jp/library'
    """
## INPUT
        'params' should have 'appkey' field or 'pref' field or 'systemid' field
        Attitude and Longtitude will be used.
        example 1: 
            params_1 = {
                'appkey' : api_data['library_api_key'],
                'pref' : '東京都',
                'city' : '千代田区',
                'format' : json,
                'callback' : '',
                'limit' : 5,
            }
            params_2 = {
                'appkey' : api_data['library_api_key'],
                'geocode' : '139.8,35.7',
                'format' : json,
                'callback' : '',
                'limit' : 5,
            }
## OUTPUT
        Library(this means book library) list will be returned.
        Elements are sort by distance.
        Each Element has a dictionary(This is the Python3 'dictionary' format),
        which has 'systemid', 'distance', and so on.
    """
    def getLibraryData(self, query_params):
        query =  urllib.parse.urlencode(query_params)
        url = self.m_base_url + '?' + query
        print(url)
        with urllib.request.urlopen(url) as res:
            raw_text = res.read().decode('utf-8')
            data = json.loads(raw_text)
        return data

class LibraryBookStatusJSON:
    m_base_url = 'https://api.calil.jp/check'
    """
## INPUT
        'params' should have 'appkey' field and 'isbn' field and 'sytemid' field
        Attitude and Longtitude will be used.
        example 1: 
            params = {
                'appkey' : api_data['library_api_key'],
                'isbn' : '4577002086',
                'systemid' : 'Tokyo_Sumida',
                'format' : json,
                'callback' : '',
            }
## OUTPUT
        Library(this means book library) dictionary(this means Python3 'dictionary' format) will be returned.
        Return value will have 'libkey' list value, which is to check whether you can rent a book at the library.
    """
    def getLibkey(self, query_params):
        query =  urllib.parse.urlencode(query_params)
        url = self.m_base_url + '?' + query
        success = 1
        while success == 1:
            with urllib.request.urlopen(url) as res:
                raw_text = res.read().decode('utf-8')
                raw_text = raw_text.lstrip('(').rstrip(');')
                raw_text = '[' + raw_text + ']'
                data = json.loads(raw_text)
                success = data[0]['continue']
        return data[0]['books'][query_params['isbn']][query_params['systemid']]
