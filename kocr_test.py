import requests
import uuid
import time
import json, random
from PIL import Image
from io import BytesIO
# 카카오용으로 남겨두자. 

# imgs = ['testimg/1.jpeg', 'testimg/2.jpeg', 'testimg/3.jpeg', 'form/waybill.jpg']
api_url = 'https://wl11rjimfa.apigw.ntruss.com/custom/v1/30859/ea5fcbc02c05c115b55bbe64469072ec865b2fb60e1ee0fe60eb45dfb4d7e2c7/general'
secret_key = 'ZlRDYlNTZk5RRlFxWW9hY1RjQkR3dVRjSlFmVE1pQUY='


def clovaOCR(image_file):
    image_file = image_file

    img_response = requests.get(image_file)
    image = Image.open(BytesIO(img_response.content))
    saved_filename = str(random.randint(0, 99999))
    image_file = 'bill/'+saved_filename+'.jpeg'
    image.save(image_file)

    request_json = {
        'images': [
            {
                'format': 'jpeg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
    ('file', open(image_file,'rb'))
    ]
    headers = {
    'X-OCR-SECRET': secret_key
    }

    response = requests.request("POST", api_url, headers=headers, data = payload, files = files)
    response = json.loads(response.text.encode('utf8'))

    '''
    Young Suk Park
    Seung Tae Kim
    Jung Yong Hong
    Jeeyun Lee
    SeHoon Park
    Joon Oh Park
    '''
    prof = None
    weight = 1.0
    waybill = []

    counter = 0
    isappend = False

    for result in response['images'][0]['fields']:
        
        if 'Young' in result['inferText']:
            prof = 'Young Suk Park'
        elif 'Seung' in result['inferText']:
            prof = 'Seung Tae Kim' 
        elif 'Jeeyun' in result['inferText']:
            prof = 'Jeeyun Lee'
        elif 'SeHoon' in result['inferText']:
            prof = 'SeHoon Park'
        elif 'Joon' in result['inferText']:
            prof = 'Joon Oh Park'     
        
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

    return prof, weight, waybill[-3]+waybill[-2]+waybill[-1]
 