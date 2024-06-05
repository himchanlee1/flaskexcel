import requests
import uuid
import time, os
import json, random
from PIL import Image
from io import BytesIO

 
api_url = 'https://wl11rjimfa.apigw.ntruss.com/custom/v1/30859/ea5fcbc02c05c115b55bbe64469072ec865b2fb60e1ee0fe60eb45dfb4d7e2c7/general'
secret_key = 'ZlRDYlNTZk5RRlFxWW9hY1RjQkR3dVRjSlFmVE1pQUY='

def extract_numbers(input_string):
    return ''.join([ch for ch in input_string if ch.isdigit()])

def clovaOCR(image_file):
    img_response = requests.get(image_file)
    image = Image.open(BytesIO(img_response.content))

    if not os.path.exists('bill'):
        os.makedirs('bill')

    saved_filename = str(random.randint(0, 99999))
    image_file = 'bill/' + saved_filename + '.jpg'
    image.save(image_file)

    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [('file', open(image_file, 'rb'))]
    headers = {'X-OCR-SECRET': secret_key}

    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    response = json.loads(response.text.encode('utf8'))

    prof = None
    weight = '1.0'
    waybill = []

    counter = 0
    isappend = False

    for result in response['images'][0]['fields']:
        if 'Suk' in result['inferText']:
            prof = 'Young Suk Park'
        elif 'Tae' in result['inferText']:
            prof = 'Seung Tae Kim'
        elif 'Lee' in result['inferText']:
            prof = 'Jeeyun Lee'
        elif 'SeHoon' in result['inferText']:
            prof = 'SeHoon Park'
        elif 'Oh' in result['inferText']:
            prof = 'Joon Oh Park'
        elif 'Hong' in result['inferText']:
            prof = 'Jung Yong Hong'
        
        if prof == None:
            prof = 'Jeeyun Lee'

        if '4.1' in result['inferText']:
            weight = '4.1'

        if 'WAYBILL' == result['inferText']:
            isappend = True
            continue

        if isappend:
            waybill.append(result['inferText'])
            counter += 1

            if counter == 3:
                isappend = False
                counter = 0

    return prof, weight, extract_numbers(waybill[-3] + waybill[-2] + waybill[-1])




def clovaOCR_for_file(image_file):
    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [('file', open(image_file, 'rb'))]
    headers = {'X-OCR-SECRET': secret_key}

    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    response = json.loads(response.text.encode('utf8'))

    prof = None
    weight = '1.0'
    waybill = []

    counter = 0
    isappend = False
    # print(response)
    for result in response['images'][0]['fields']:
        if 'Suk' in result['inferText']:
            prof = 'Young Suk Park'
        elif 'Tae' in result['inferText']:
            prof = 'Seung Tae Kim'
        elif 'Lee' in result['inferText']:
            prof = 'Jeeyun Lee'
        elif 'SeHoon' in result['inferText']:
            prof = 'SeHoon Park'
        elif 'Oh' in result['inferText']:
            prof = 'Joon Oh Park'
        elif 'Hong' in result['inferText']:
            prof = 'Jung Yong Hong'

        if prof == None:
            prof = 'Jeeyun Lee'

        if '4.1' in result['inferText']:
            weight = '4.1'

        if 'WAYBILL' == result['inferText']:
            isappend = True
            continue

        if isappend:
            waybill.append(result['inferText'])
            counter += 1

            if counter == 3:
                isappend = False
                counter = 0

    return prof, weight, extract_numbers(waybill[-3] + waybill[-2] + waybill[-1])



# for img in sorted(os.listdir('test_images/')):
#     if img == '.DS_Store':
#         continue
#     print(img, clovaOCR_for_file('test_images/'+img))

# import os 
# print(os.listdir('test_images'))

# print(clovaOCR_for_file('test_images/28.jpg'))