
import pytesseract
import cv2
import numpy as np

kernel = np.ones((5, 5), np.uint8)
path = 'form/waybill.jpg'
image = cv2.imread(path)
image = cv2.resize(image, None, fx=2, fy=2)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

morph = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

text = pytesseract.image_to_string(morph, lang='kor+eng')
text = text.split('\n')
for t in text:
    print(t)