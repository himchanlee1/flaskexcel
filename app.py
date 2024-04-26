
from flask import Flask, jsonify, request

# Flask 애플리케이션 생성
app = Flask(__name__) 
'''
Q. 안녕하세요, GI/GU team DHL 배송 입력기 입니다, 초기세팅에 필요한 내용 전달 부탁드립니다.
A
이름 :  # 엑셀 H5 부분에 기입
영어이름 : # invoice shippers name (200,745)에 기입
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
 

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
