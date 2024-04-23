import easyocr
import re

def extract_shipment_info(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    shipment_weight = "0"
    waybill_number = ""

    for bbox, text, prob in results:
        if "Shpt Wght" in text or "kg" in text:
            weight_search = re.search(r'(\d+\.\d+|\d+)\s*kg', text, re.IGNORECASE)
            if weight_search:
                shipment_weight = weight_search.group(1)

        # WAYBILL 텍스트가 포함된 라인에서 숫자 추출
        if "WAYBILL" in text.upper():
            numbers = re.findall(r'\d+', text)
            # 숫자들을 연결하여 WAYBILL 번호 생성
            waybill_candidate = ''.join(numbers)
            # WAYBILL 번호가 일반적으로 10자리임을 확인
            if len(waybill_candidate) == 10:
                waybill_number = waybill_candidate
                break

    if not waybill_number:
        raise ValueError("Waybill 번호를 찾을 수 없습니다.")

    return shipment_weight, waybill_number

# 사용 예:

# image_path = r'C:\Python\bill\waybill.jpg'  # 실제 이미지 경로
# weight, waybill = extract_shipment_info(image_path)
# print("Shipment Weight:", weight)
# print("Waybill Number:", waybill)
