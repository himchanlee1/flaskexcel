from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def imageEdit(bill, date, img_path='form/invoice.png'):
    # 이미지를 로드합니다.
    image_path = r'{}'.format(img_path)  # 로드할 이미지의 경로 (invoice)
    image = Image.open(image_path)

    # 텍스트와 좌표 설정
    texts_and_positions = {
        "{}".format(bill): (200, 670),  # House Air Bill #의 좌표
        "{}".format(date): (250, 695),   # Expected Date of delivery의 좌표
        "Him Chan Lee": (200, 745), # Shippers Signature의 좌표
        "SC": (200, 770)            # Shippers Name & Title의 좌표
    }

    # 사용할 폰트와 크기 설정
    # font_path = "arial.ttf"  # 사용할 폰트 파일의 경로
    # font_size = 14
    # font = ImageFont.truetype(font_path, font_size)

    font = ImageFont.load_default()

    # 텍스트와 좌표에 텍스트를 이미지에 추가합니다.
    draw = ImageDraw.Draw(image)
    font_color = (0, 0, 0)  # 텍스트 색상 (RGB)
    for text, position in texts_and_positions.items():
        draw.text(position, text, font=font, fill=font_color)

    # 현재 날짜와 시간을 포함하는 고유한 파일명을 생성합니다.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = rf'bill/modified_invoice_{timestamp}.png'
    print("Invoice Output Path:", output_path)
    # 변경된 이미지를 저장합니다.
    image.save(output_path)
    print('편집 및 저장 완료.')

    return output_path

# 시험 실행
 
# from myexcel import main, update_excel, read_excel, format_date

# # image_path = r'C:\Python\bill\waybill.jpg'
# # file_path = r'C:\Python\bill\코반스 픽업요청서 양식.xlsx'

 
# file_path = r'bill/코반스 픽업요청서 양식.xlsx'
# invoice_path = r'bill/invoice.png'

# bill, date = read_excel(file_path=file_path) 
# imageEdit(invoice_path, bill, date)