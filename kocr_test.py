import keras_ocr
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


pipeline = keras_ocr.pipeline.Pipeline()

images = [
    keras_ocr.tools.read(url) for url in [
        'form/waybill.jpg'
    ]
]

prediction_groups = pipeline.recognize(images)

for predictions in prediction_groups:
    for p in predictions:
        print(p[0])