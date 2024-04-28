import easyocr
import re

def extract_shipment_info(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)

    shipment_weight = None
    waybill_number = None
    doctor_name = None

    # OCR 결과를 순회하며 정보 추출
    for bbox, text, prob in results:
        # WAYBILL 번호 추출
        waybill_search = re.search(r'WAYBILL\s(\d{2}\s\d{4}\s\d{4})', text)
        if waybill_search:
            waybill_number = waybill_search.group(1).replace(" ", "")
            continue

        # 무게 추출
        if "kg" in text:
            weight_search = re.search(r'(\d+\.\d+)\s*kg', text)
            if weight_search:
                shipment_weight = weight_search.group(1)
                continue

        # Doctor 이름 추출
        if "Dr:" in text:
            # 'Dr:' 다음에 오는 단어들(이름)을 가져옵니다.
            name_search = re.search(r'Dr:\s+([A-Za-z]+\s[A-Za-z]+)', text)
            if name_search:
                doctor_name = name_search.group(1)
                # 이름 다음에 나오는 'Kim'을 찾아 추가합니다.
                next_index = results.index((bbox, text, prob)) + 1
                if next_index < len(results):
                    next_text = results[next_index][1]
                    if "Kim" in next_text:
                        doctor_name += ' ' + next_text
                continue

    # 결과 확인
    if shipment_weight is None:
        shipment_weight = "Shipment weight not found"

    if waybill_number is None or len(waybill_number) != 10:
        waybill_number = "Waybill number not found or incorrect"

    if doctor_name is None:
        doctor_name = "Doctor's name not found"

    return shipment_weight, waybill_number, doctor_name

# 이미지 파일 경로
image_path = r'C:\Users\admin\Documents\GitHub\flaskexcel\form\waybill.jpg'  # 윈도우 파일 경로

# 추출된 정보 출력
try:
    weight, waybill, doctor_name = extract_shipment_info(image_path)
    print(f"Shipment Weight: {weight} kg")
    print(f"Waybill Number: {waybill}")
    print(f"Doctor's Name: {doctor_name}")
except Exception as e:
    print(e)
