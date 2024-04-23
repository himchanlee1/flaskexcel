from myexcel import update_excel, read_excel, read_pickup_date
from myeasyocr import extract_shipment_info
from myimageedit import imageEdit
from myemail import send_mail
# 이미지와 엑셀 파일 경로를 직접 지정합니다.
image_path = r'bill/waybill.jpg'
file_path = r'bill/코반스 픽업요청서 양식.xlsx'


def getInfo():
    pickup_date = input("픽업 날짜를 YY.MM.DD 형식으로 입력하세요: ")
    ready_time = input("준비된 시간이 오전인가요 오후인가요? (오전/오후로 입력): ")
    blood_collection_date = input("채혈 날짜를 YY.MM.DD 형식으로 입력하세요: ")

    # 나중에 Kakao ChatBot DB에 한번 입력한 아이디, 비번은 저장되도록 설정
     

    return pickup_date, ready_time, blood_collection_date

def getEmailInfo():
    email_id = input('발신자 네이버 이메일 아이디를 입력해주세요: ')
    email_pw = input('발신자 이메일 비밀번호를 입력해주세요: ')
    email_add = input('발신자 이메일 주소를 입력해주세요: ')
    
    send_to_email_add = '{}@naver.com'.format(email_id)

    return email_id, email_pw, email_add, send_to_email_add

# 기본 데이터 입력
pickup_date, ready_time, blood_collection_date = getInfo()

# OCR 정보추출
shipment_weight, waybill_number = extract_shipment_info(image_path)

# 엑셀에 정보 저장!
try:
    update_excel(file_path, waybill_number, shipment_weight, pickup_date, ready_time, blood_collection_date)
    
except Exception as e:
    print(f"에러가 발생했습니다: {e}")

# read_pickup_date로 픽업날짜 호출
billNum, date = read_excel(file_path)

# 이미지 편집
imageEdit(billNum, date)

# 이메일 정보 입력
email_id, email_pw, email_add, send_to_add = getEmailInfo()

# 이메일 전송 (엑셀파일)
send_mail(send_from=email_add, send_to=[send_to_add],
          subject='{} 삼성서울병원 픽업 문의드립니다.'.format(read_pickup_date(file_path=file_path)), message=f'연구 진행 위해 픽업 문의 드립니다.', files=[file_path],
          mtype='html', server='smtp.naver.com', username=email_id, password=email_pw)

print('모든 작업 수행 완료!')