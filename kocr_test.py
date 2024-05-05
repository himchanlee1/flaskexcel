import cv2
import imutils # <- 이걸 제대로 된 가공을 하는게 아니라면 필요가 없지 않나?
from imutils.perspective import four_point_transform
import pytesseract

import matplotlib.pyplot as plt

url = 'form/waybill.jpg'
original_img = cv2.imread(url)

# cv2.imshow("original image", original_img)

image = original_img.copy()
image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
edged = cv2.Canny(blurred, 75, 200)

# cv2.imshow("gray", gray)
# cv2.imshow("blurred", blurred)
# cv2.imshow("edged", edged)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

receiptCnt = None
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02*peri, True)

    if len(approx) == 4:
        receiptCnt = approx
        break 
if receiptCnt is None:
    raise Exception(("Could not find outline"))

output = image.copy()
cv2.drawContours(output, [receiptCnt], -1, (255, 0, 0), 3)

ratio = original_img.shape[1] / float(image.shape[1])
receipt = four_point_transform(original_img, receiptCnt.reshape(4, 2) * ratio)
# cv2.imshow("Receipt", receipt)
 

options = r'--psm 1 --oem 4'
# text = pytesseract.image_to_string(cv2.cvtColor(receipt, cv2.COLOR_BGR2RGB), config=options)
tex2 = pytesseract.image_to_string(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB), config=options)

# for n in range(1, 14):
#     options = "--psm {}".format(n)
#     print("<<{}>>".format(options))
#     try:
#         print(pytesseract.image_to_string(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB), config=options))
#     except:
#         continue

print(tex2)