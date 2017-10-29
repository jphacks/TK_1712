鈴木担当箇所の説明
### まだかなりゴミコードですごめんなさい

## 環境
- Python3.6.3

## ①画像から文字認識（OCR, 光学的文字認識）（char_recognition_gcp.py）
- google Cloud Vision APIで精度よくできる
- "python char_recognition_gcp.py ***(画像ファイルへのパス)"
- 

## ②キーワード抽出（keyword_goo_API.py）
- gooAPIを使う（https://labs.goo.ne.jp/api/jp/keyword-extraction/）
- 単体で動かすことはできる（keyword_goo_API.py）
	- 何個キーワードを出力するか指定する
	- リスト内辞書でこのように出力できる
		- [{'Python': 0.3385}, {'データ分析入門': 0.3385}, {'NumPy': 0.3133}, {'pandas': 0.3133}, {'Wes McKinney': 0.2881}]

## ①②をマージするとJSONDecodeErrorが...
- api.keyword()の中でbodyに代入する文字列が""ではなく''で囲まれてしまっているのが原因ぽい？
- よくわからず
