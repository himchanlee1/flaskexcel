from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def imageEdit(bill, date, img_path, ename):
    # 이미지를 로드합니다.
    image_path = r'{}'.format(img_path)  # 로드할 이미지의 경로
    image = Image.open(image_path)

    
    month = date[3:5]
    m = None
    if month == '01':
        m = 'JAN'
    elif month == '02':
        m = 'FEB'
    elif month == '03':
        m = 'MAR'
    elif month == '04':
        m = 'APR'
    elif month == '05':
        m = 'MAY'
    elif month == '06':
        m = 'JUN'
    elif month == '07':
        m = 'JUL'
    elif month == '08':
        m = 'AUG'
    elif month == '09':
        m = 'SEP'
    elif month == '10':
        m = 'OCT'
    elif month == '11':
        m = 'NOV'
    elif month == '12':
        m = 'DEC'
    newdate = date[:2]+m+"20"+date[-2:]

    # 텍스트와 좌표 설정
    texts_and_positions = {
        "{}".format(bill): (360, 1050),  # House Air Bill #의 좌표
        "{}".format(date): (390, 1090),   # Expected Date of delivery의 좌표
        "{}".format(ename): (370, 1180), # Shippers Signature의 좌표
        "SC": (370, 1230)            # Shippers Name & Title의 좌표
    }

    font = ImageFont.truetype("arial.ttf", 20)

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
