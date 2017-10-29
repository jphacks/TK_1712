from base64 import b64encode
from os import makedirs
from os.path import join, basename
from sys import argv
import json
import requests
from goolabs import GoolabsAPI
import pprint

ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
RESULTS_DIR = 'jsons'
makedirs(RESULTS_DIR, exist_ok=True)

# gooAPIが発行してくれたAPI ID
with open('apikey.json', 'r') as f:
    api_data = json.load(f)
app_id = api_data['keyword_api_key']
api = GoolabsAPI(app_id)


def make_image_data_list(image_filenames):
    """
    image_filenames is a list of filename strings
    Returns a list of dicts formatted as the Vision API
        needs them to be
    """
    img_requests = []
    for imgname in image_filenames:
        with open(imgname, 'rb') as f:
            ctxt = b64encode(f.read()).decode()
            img_requests.append({
                'image': {'content': ctxt},
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': 1
                }]
            })
    return img_requests


def make_image_data(image_filenames):
    """Returns the image data lists as bytes"""
    imgdict = make_image_data_list(image_filenames)
    return json.dumps({"requests": imgdict}).encode()


def request_ocr(api_key, image_filenames):
    response = requests.post(ENDPOINT_URL,
                             data=make_image_data(image_filenames),
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
    return response


def target_sentence_to_keywords_list(target_sentence):
    target_sentence = target_sentence.replace('\n', '')
    # print("target_sentence = ", end="")
    # print(target_sentence)

    # key:キーワード、value:関連度合い の辞書を作る
    sample_response = api.keyword(
        title="photo01", body=target_sentence, max_num=5)

    # pprintで、整形された状態でprintできる（sample_responseは辞書型のデータ）
    # print("sample_response = ", end="")
    # pprint.pprint(sample_response)

    # max_num個のキーワードをリスト型にして出力。
    keywords_dic_list = sample_response["keywords"]
    print("keywords_dic_list = ", end="")
    print(keywords_dic_list)


if __name__ == '__main__':

    # google cloud vision のAPIキー
    with open('apikey.json', 'r') as f:
        api_data = json.load(f)
    app_id = api_data['google_cloud_vision_api_key']

    # 画像ファイル読み込み
    image_filenames = argv[1:]

    if not api_key or not image_filenames:
        print("""
            Please supply an api key, then one or more image filenames
            $ python cloudvisreq.py api_key image1.jpg image2.png""")
    else:
        response = request_ocr(api_key, image_filenames)
        if response.status_code != 200 or response.json().get('error'):
            print(response.text)
        else:
            for idx, resp in enumerate(response.json()['responses']):
                # save to JSON file
                imgname = image_filenames[idx]
                jpath = join(RESULTS_DIR, basename(imgname) + '.json')
                with open(jpath, 'w') as f:
                    datatxt = json.dumps(resp, indent=2)
                    print("Wrote", len(datatxt), "bytes to", jpath)
                    f.write(datatxt)

                # print the plaintext to screen for convenience
                print("---------------------------------------------")
                t = resp['textAnnotations'][0]
                print("    Text:")
                print(t['description'])

                target_sentence_to_keywords_list(
                    'Python is a very useful language.')  # ここの引数に本当は t['description'] を代入したい
