from base64 import b64encode
from os import makedirs
from os.path import join, basename
from sys import argv
import json
import requests

import keyword_goo_API as kg

ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
RESULTS_DIR = 'jsons'
makedirs(RESULTS_DIR, exist_ok=True)


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

def sentence_recog(image_path):
    # google cloud vision のAPI
    with open('apikey.json', 'r') as f:
        api_data = json.load(f)
    api_key = api_data['google_cloud_vision_api_key']

    # 画像ファイルの読み込み（TODO: ここで、ユーザーがアップロードした画像を代入する）
    image_filenames = image_path

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
                # print("    Bounding Polygon:")
                # print(t['boundingPoly'])
                print("    Text:")
                target_sentence = t['description'].replace('\n', '')
                return target_sentence

def make_keywords_from_photo():
    path = ['../Photo2Keywords/photos/python_data_analysis_camera.jpeg']
    sentence = sentence_recog(path)
    keywords_list = kg.make_keywords(sentence)
    return keywords_list
