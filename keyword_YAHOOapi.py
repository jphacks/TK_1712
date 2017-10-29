import requests
import json
# import urllib3
import urllib.request


input_string = 'こんにちは。私の名前はすずきです。'


class GetIsbn:
    """ Get isbn by google book api.
    """

    def useGoogleApi(self, keywords):
        """ Use googleAPI and return list of isbn.
        """
        condition = ''
        # import pdb
        # pdb.set_trace()
        for key in keywords:
            condition = condition + '+' + key
        url = 'https://www.googleapis.com/books/v1/volumes'
        params = {'q': condition}
        data = requests.get(url, params=params).json()

        isbmList = []
        for item in data['items']:
            # 0 means isbn_13, 1 means isbn_10. isbn_13 is better.
            isbmList.append(item['volumeInfo'][
                            'industryIdentifiers'][0]['identifier'])

        return isbmList


class searchBook:
    """ Get info from isbn and keywords by using yahooAPI.
    """

    def yapiIsbn(self, isbn):
        with open('apikey.json', 'r') as f:
            api_data = json.load(f)
        url = 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemSearch'
        appid = api_data['yahoo_api_key']
        params = {'appid': appid, 'isbn': isbn,  'category_id': '10002'}
        data = requests.get(url, params=params).json()
        return data

    def yapiKeywords(self, keywords):
        """ search from keywords by using yahooapi.
            Return list of dictionary. (This dictionary include product name, product description, small image and url.)
        """
        with open('apikey.json', 'r') as f:
            api_data = json.load(f)
        url = 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemSearch'
        appid = api_data['yahoo_api_key']

        condition = ''
        # TODO: keywordの数2個?
        for i in range(2):
            condition = condition + keywords[i] + '+'
        params = {'appid': appid, 'query': condition, 'category_id': '10002'}
        data = requests.get(url, params=params).json()

        # 商品名,商品説明,76×76サイズの画像URL,商品URLのmapを返す
        totalResultsReturned = data['ResultSet']['totalResultsReturned']
        retData = []
        for i in range(int(totalResultsReturned)):
            tmp = {}
            tmp['Name'] = data['ResultSet']['0']['Result'][str(i)]['Name']
            tmp['Description'] = data['ResultSet'][
                '0']['Result'][str(i)]['Description']
            tmp['Image'] = data['ResultSet']['0'][
                'Result'][str(i)]['Image']['Medium']
            tmp['Url'] = data['ResultSet']['0']['Result'][str(i)]['Url']
            tmp['Price'] = data['ResultSet']['0']['Result'][str(i)]['Price']
            tmp['Review'] = data['ResultSet']['0'][
                'Result'][str(i)]['Review']['Rate']
            retData.append(tmp)

        return retData


def sentenceToKeywordsList(input_string):
    with open('apikey.json', 'r') as f:
        api_data = json.load(f)
    apiid = api_data['yahoo_keyword_api_key']
    url = "http://jlp.yahooapis.jp/KeyphraseService/V1/extract"
    # url = "http://example.com/"
    # TODO: keywordの数2個?
    params = {'apiid': apiid, 'sentence': input_string}
    data = requests.get(url, params=params)
    import pdb
    pdb.set_trace()
    # keywords_list = []

    return data


if __name__ == '__main__':
    # keywords = ["harry", "potter"]
    keywords = sentenceToKeywordsList(input_string)

    isbn = GetIsbn()
    shoopingInfo = searchBook()

    isbnList = isbn.useGoogleApi(keywords)
    data = shoopingInfo.yapiKeywords(keywords)
    print(data)
    f = open('json/sample.json', 'w')
    f.write(json.dumps(data, ensure_ascii=False, indent=4))
    f.close()
