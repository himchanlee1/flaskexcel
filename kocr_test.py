import requests
import uuid
import time
import json

# 카카오용으로 남겨두자. 

imgs = ['testimg/1.jpeg', 'testimg/2.jpeg', 'testimg/3.jpeg', 'form/waybill.jpg']
api_url = 'YOUR_API_URL'
secret_key = 'YOUR_SECRET_KEY'

for img in imgs:
    image_file = img

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
    files = [
    ('file', open(image_file,'rb'))
    ]
    headers = {
    'X-OCR-SECRET': secret_key
    }

    response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

    print(response.text.encode('utf8')) 
