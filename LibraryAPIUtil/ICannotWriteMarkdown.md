### 服部担当箇所

## 位置情報の取得
緯度経度をGeolocation APIなどで取得する予定です。
python3で叩くのが大変そうです。
多分javascriptで取得することになります。

## 図書館一覧の取得

位置情報から近い順に図書館を表示する。
図書館API (Reference: https://calil.jp/doc/api_ref.html)で取得します。

https://api.calil.jp/libraryに適切なクエリパラメータを渡すとjsonが返ってきます。

APIキーは自分で取りました。このファイルが置いてあるディレクトリの下にapikey.jsonというものを置き、

{
    "library_api_key" : "some api key"
}
とすると、test_library_api_util.pyが動かせるようになります。

API制限は各IPごとに、1時間に1000回リクエストまでらしいので余裕です。

## 本のISBNを受け取り、図書館の貸出状況をリストアップする
本のISBNから図書館APIで検索する。
これも図書館APIで検索します。

https://api.calil.jp/checkにクエリパラメータを渡すと貸出状況がわかります。


## 注意
calilのAPIを使って取得された図書館名などには、かならずcalilのリンクを貼らなきゃいけないようです。
本を取得 : https://calil.jp/book/{ISBN10}
図書館ページを取得 : https://calil.jp/library/{libid}/{図書館の正式名称}
                        or
                     https://calil.jp/library?search?s={システムID}&k={図書館のLibkey}
