# Morikawa
きたなくてごめんなさい。typoもきっとたくさんある。。。  
とりあえず、画像からisbnを取り出す、yahoo aoi にて情報を持ってくる、ができます。  
主にgetIsbnAndInfo.pyを見てもらえれば良いです。  
mainの中を見てもらえると良いかと思います...


``` python:getIsbnAndInfo.py  
if __name__ == '__main__':
    keywords = getkeywords.make_keywords_from_photo()

    isbn = GetIsbn()
    shoopingInfo = searchBook()

    isbnList = isbn.useGoogleApi(keywords)
    data = shoopingInfo.yapiKeywords(keywords)
    print(data)
```

(もとの画像に関してはchar_recognition_gcpをいじってあげる必要ありだが今は固定してます。)

## isbn を持ってくる
> keywords = getkeywords.make_keywords_from_photo()

りさちゃんの書いてくれたコードによりキーワードのリストを得ている。  
ex)  
['Python', 'Ruby', 'データ分析者', 'Perl', '動的プログラミング言語']


> isbnList = isbn.useGoogleApi(keywords)

isbnListにはisbn13のリストが入っている。 ちなみにisbn10にすることも簡単にできる。コード中のコメント参照。  
ex)  
['9784798048161', '9784873113647', '477415654X', '4774161632', '475611895X', '4621066080', '4774178942', '4873111870', '9784798143354', '4873117437']  
ゆえにisbnのリストが欲しい時はこの関数を使えばよい

## yahooAPIを使い情報を持ってくる
> data = shoopingInfo.yapiKeywords(keywords)

yahooから持ってきた銃砲が入っている。
商品の名前(Name),説明(Description), 画像URL(Image), 商品URL(Url)の情報が入っている。  
辞書のリストになってます。jsonとかで返すべきかも??あと、他にも欲しい情報があれば。  

ex)  
[{'Name': '関数プログラミング実践入門 簡潔で、正しいコードを書くために WEB+DB\u3000PRESS\u3000plusシリーズ / 大川徳之  〔本〕', 'Description': '発売日:2016年09月24日 / ジャンル:建築・理工 / フォーマット:本 / 出版社:技術評論社 / 発売国:日本 / ISBN:9784774183909 / アーティストキーワード:大川徳之   内容詳細:プログラミングの考え方が見えてくる！言語の壁を越えて活かせるスタイル。Ｈａｓｋｅｌｌプロダクトの開発者が見極めたシンプルで、使える基本。言語／開発環境最新スペック対応。目次:第０章\u3000“入門”関数プログラミング―「関数」の世界/ 第１章\u3000“比較で見えてくる”関数プログラミング―Ｃ／Ｃ＋＋、Ｊａｖａ、ＪａｖａＳｃｒｉｐｔ、Ｒｕｂｙ、Ｐｙｔｈｏｎ、そしてＨａｓｋｅｌｌ/ 第２章\u3000型と値―「型」は、すべての基本である/ 第３章\u3000関数―関数適用、関数合成、関数定義、再帰関数、高階関数/ 第４章\u3000評価戦略―遅延・・・', 'Image': 'https://item-shopping.c.yimg.jp/i/c/hmv_7337943', 'Url': 'https://store.shopping.yahoo.co.jp/hmv/7337943.html'}, ...]
