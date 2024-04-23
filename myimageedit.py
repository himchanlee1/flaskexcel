import cv2
from datetime import datetime



def imageEdit(bill, date, img_path='bill/invoice.png'):
    # 이미지를 로드합니다.
    image_path = r'{}'.format(img_path)  # 로드할 이미지의 경로 (invoice)
    image = cv2.imread(image_path)

    # 추가할 텍스트와 좌표
    texts_and_positions = {
        "{}".format(bill): (200, 670),  # House Air Bill #의 좌표
        "{}".format(date): (250, 695),   # Expected Date of delivery의 좌표
        "Him Chan Lee": (200, 745), # Shippers Signature의 좌표
        "SC": (200, 770)            # Shippers Name & Title의 좌표
    }

    # OpenCV에서 사용할 폰트 설정
    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 1  # 텍스트 크기
    font_color = (0, 0, 0)  # 텍스트 색상 (BGR)
    thickness = 1  # 텍스트 두께

    # 각 텍스트와 좌표에 대해 이미지에 텍스트를 추가합니다.
    for text, position in texts_and_positions.items():
        cv2.putText(image, text, position, font, font_scale, font_color, thickness)

    # 현재 날짜와 시간을 포함하는 고유한 파일명을 생성합니다.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # output_path = rf'C:\Python\bill\modified_invoice_{timestamp}.png'
    output_path = rf'bill/modified_invoide_{timestamp}.png'

    # 변경된 이미지를 저장합니다.
    cv2.imwrite(output_path, image)
    print('편집 및 저장 완료.')

# 시험 실행

# from myeasyocr import extract_shipment_info
# from myexcel import main, update_excel, read_excel, format_date

# # image_path = r'C:\Python\bill\waybill.jpg'
# # file_path = r'C:\Python\bill\코반스 픽업요청서 양식.xlsx'

 
# file_path = r'bill/코반스 픽업요청서 양식.xlsx'
# invoice_path = r'bill/invoice.png'

# bill, date = read_excel(file_path=file_path) 
# imageEdit(invoice_path, bill, date)