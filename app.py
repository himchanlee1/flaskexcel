
from flask import Flask, jsonify, request

# Flask 애플리케이션 생성
app = Flask(__name__) 
'''
Q. 안녕하세요, GI/GU team DHL 배송 입력기 입니다, 초기세팅에 필요한 내용 전달 부탁드립니다.
A
이름 :  # 엑셀 H5 부분에 기입
영어이름 : # invoice shippers name (200,745)에 기입
전화번호 : # 엑셀 I5 부분에 기입
네이버 이메일 :  # ID
네이버 비밀번호 : # PW
invoice 받을 원내 이메일 : #himchan1.lee@sbri.co.kr(각자 원내 아이디 입력)
print ('초기 셋팅이 완료 되었습니다, 초기셋팅을 변경하고 싶으시면 "초기셋팅 변경" 이라고 해주세요.)
'''

# 루트 URL에 대한 핸들러 함수
@app.route('/', methods=['GET'])
def hello_world():
    response = {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": "root url입니다. 서버가 돌아가고 있습니다."
                }, 
                "fixedNewText":{
                    "newtext": "자동으로 업로드 됨을 알 수 있습니다."
                }
            }]
        }
    } 
    return jsonify(response)



@app.route('/m', methods=['POST']) # Test
def message():
    print('/message로 넘어왔습니다.')


    response = {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": "초기 설정에 대한 응답 메시지"
                }
            }]
        }
    } 
    return jsonify(response)


@app.route('/getInfo', methods=['POST'])
def getInfo():
    json = request.get_json()
    params = json['action']['params']

    name = params['이름']
    ename = params['영어이름']
    mail = params['메일']
    pw = params['비밀번호']
    hosmail = params['원내메일']

    response = {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": "입력된 값: {}/{}/{}/{}/{}".format(name, ename, mail, pw, hosmail)
                }
            }]
        }
    } 
    return jsonify(response)
 
@app.route('/getName', methods=['POST'])
def getName():
    json = request.get_json()
    param = json['action']['params']
    print('getName 연결됨')
    print(json)
    name = param['sys_text']
    

    # setting JSON에 저장했다고 치고~

    response = {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": "입력된 이름 : {}".format(name)
                }
            }]
        }
    }
    return jsonify(response)

@app.route('/gettime', methods=['POST'])
def gettime():
    json = request.get_json()
    param = json['action']['params']
    print('gettime 연결됨')
    print(json)
    time = param['sys_text'] 
    # '/' 기준으로 문자열을 나누기
    split_text = time.split('/')
    pickup_date = split_text[0]
    pickup_time = split_text[1]
    blood_time = split_text[2]


    # setting JSON에 저장했다고 치고~

    response = {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": "입력된 time : {}".format(time)
                }
            }]
        }
    }
    return jsonify(response)

    from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

def validate_input(data):
    errors = []
    if not data['name'].strip():
        errors.append("이름이 누락되었습니다.")
    if not data['ename'].strip():
        errors.append("영어 이름이 누락되었습니다.")
    if not data['phone'].strip():
        errors.append("전화번호가 누락되었습니다.")
    if not re.match(r"^\S+@\S+\.\S+$", data['mail']):
        errors.append("유효한 이메일 주소가 아닙니다.")
    if not data['password'].strip():
        errors.append("비밀번호가 누락되었습니다.")
    if not re.match(r"^\S+@\S+\.\S+$", data['hosmail']):
        errors.append("유효한 원내 메일 주소가 아닙니다.")
    return errors

@app.route('/validateData', methods=['POST'])
def validate_data():
    # 파일에서 사용자 정보 읽기
    with open('data.json', 'r') as file:
        user_data = json.load(file)

    # 요청에서 전달된 사용자 입력
    input_data = request.get_json()
    name = input_data.get('name', '')
    ename = input_data.get('ename', '')
    phone = input_data.get('phone', '')
    mail = input_data.get('mail', '')
    password = input_data.get('password', '')
    hosmail = input_data.get('hosmail', '')

    # 사용자 입력을 검증
    errors = validate_input({
        'name': name,
        'ename': ename,
        'phone': phone,
        'mail': mail,
        'password': password,
        'hosmail': hosmail
    })

    # 검증 결과 저장
    results = {
        'errors': errors,
        'valid': not errors
    }
    with open('results.json', 'w') as file:
        json.dump(results, file, indent=4)

    # 결과를 사용자에게 반환
    response = {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": "검증 오류: " + ", ".join(errors) if errors else "모든 입력이 정상적으로 검증되었습니다."
                }
            }]
        }
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)




# 애플리케이션 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
