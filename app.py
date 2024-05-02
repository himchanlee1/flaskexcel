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

@app.route('/', methods=['GET'])
def hello_world():
    response = {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": "root url입니다. 서버가 돌아가고 있습니다."
                }
            }]
        }
    } 
    return jsonify(response)

@app.route('/m', methods=['POST'])
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
    params = request.get_json()['action']['params']
    response = {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": "입력된 값: {}/{}/{}/{}/{}".format(
                        params['이름'], params['영어이름'], params['메일'], params['비밀번호'], params['원내메일'])
                }
            }]
        }
    } 
    return jsonify(response)

@app.route('/getName', methods=['POST'])
def getName():
    name = request.get_json()['action']['params']['sys_text']
    print('getName 연결됨:', name)
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

@app.route('/validateData', methods=['POST'])
def validate_data():
    try:
        with open('data.json', 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {'name': '', 'ename': '', 'phone': '', 'mail': '', 'password': '', 'hosmail': ''}

    input_data = request.get_json()
    errors = validate_input(input_data)

    results = {'errors': errors, 'valid': not errors}
    with open('results.json', 'w') as file:
        json.dump(results, file, indent=4)

    response_text = "검증 오류: " + ", ".join(errors) if errors else "모든 입력이 정상적으로 검증되었습니다."
    response = {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": response_text
                }
            }]
        }
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
