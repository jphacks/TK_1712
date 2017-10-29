#-*- coding: UTF-8 -*-

from goolabs import GoolabsAPI
import pprint
import json


def make_keywords(sentence):
    # gooAPIが発行してくれたAPI ID
    with open('apikey.json', 'r') as f:
        api_data = json.load(f)
    app_id = api_data['keyword_api_key']
    api = GoolabsAPI(app_id)

    # See sample response below.
    # 例としてpythonによるデータ分析入門の中表紙の文字をコピペしたものをbodyとして
    # キーワード抽出してみた。
    # template = u'1.2なぜPythonはデータ分析者におすすめなのか\n私自身を含む多くの人にとって、Pythonという言語は恋に落ちやすい言語です。1991年の登場の時から、\nPythonは、PerlやRubyなどの言語と並び、最も有名な動的プログラミング言語の1つでしたPythonと\nRubyは最近では、多数のWebフレームワーク(たとえば、RubyではRails, PythonではDjango)を使ったWebサイト構築で特に有名です。これらの言語はよくスクリプト言語と呼ばれます。これは、汚くてもすぐに書ける短いプログラム、つまり、スクリプトを書くのに使えるからです。'
    template = sentence
    sample_response = api.keyword(
        title="photo01", body=template, max_num=5)

    # pprintで、整形された状態でprintできる（sample_responseは辞書型のデータ）
    # pprint.pprint(sample_response)

    # max_num個のキーワードをリスト型にして出力。一緒に出てくる数字は重要度を表す？
    keywords_list = sample_response['keywords']

    data = []
    for keyword in keywords_list:
        data.extend(list(keyword.keys()))

    return data    
