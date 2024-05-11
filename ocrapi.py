import requests, json
API_KEY = 'bbfb2373b588957'

def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': API_KEY,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()


# Use examples:
imgs = ['testimg/1.jpeg', 'testimg/2.jpeg', 'testimg/3.jpeg', 'form/waybill.jpg']

# 이거 url되는 아래 함수로 수정해라. 
def myocrapi(img): 
    print('-----------{}------'.format(img))
    test_file = ocr_space_file(filename=img, language='eng')
    obj = json.loads(test_file)['ParsedResults'][0]['ParsedText']
    # print(obj)
    # print('@@@@@@@@@@@@@@@@@@@@@@@@')

    prof = None
    weight = None
    bill = None

    for text in obj.split('\n'):
        if ('Dr ' in text) or ('Or ' in text) or ('Dr.' in text) or ('Or.' in text):
            # print(text)
            prof = text
        elif 'kg' in text:
            # print(text)
            weight = text
        elif ('WAYBILL' in text) and ('DOC' not in text):
            # print(text)
            bill = text
    return prof, weight, bill
        
for i in imgs:
    print(myocrapi(i))


# test_url = ocr_space_url(url='http://i.imgur.com/31d5L5y.jpg')