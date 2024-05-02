from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

def validate_input(data):
    errors = []
    if not data.get('name', '').strip():
        errors.append("이름이 누락되었습니다.")
    if not data.get('ename', '').strip():
        errors.append("영어 이름이 누락되었습니다.")
    if not data.get('phone', '').strip():
        errors.append("전화번호가 누락되었습니다.")
    if not re.match(r"^\S+@\S+\.\S+$", data.get('mail', '')):
        errors.append("유효한 이메일 주소가 아닙니다.")
    if not data.get('password', '').strip():
        errors.append("비밀번호가 누락되었습니다.")
    if not re.match(r"^\S+@\S+\.\S+$", data.get('hosmail', '')):
        errors.append("유효한 원내 메일 주소가 아닙니다.")
    return errors

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": "root url입니다. 서버가 돌아가고 있습니다."
                }
            }]
        }
    })

@app.route('/m', methods=['POST'])
def message():
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": "초기 설정에 대한 응답 메시지"
                }
            }]
        }
    })

@app.route('/getInfo', methods=['POST'])
def getInfo():
    params = request.get_json().get('action', {}).get('params', {})
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": f"입력된 값: {params.get('이름', '')}/{params.get('영어이름', '')}/{params.get('메일', '')}/{params.get('비밀번호', '')}/{params.get('원내메일', '')}"
                }
            }]
        }
    })

@app.route('/getName', methods=['POST'])
def getName():
    name = request.get_json().get('action', {}).get('params', {}).get('sys_text', '이름 없음')
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": f"입력된 이름 : {name}"
                }
            }]
        }
    })

@app.route('/validateData', methods=['POST'])
def validate_data():
    input_data = request.get_json()
    errors = validate_input(input_data)
    results = {'errors': errors, 'valid': not errors}

    with open('results.json', 'w') as file:
        json.dump(results, file, indent=4)

    response_text = "검증 오류: " + ", ".join(errors) if errors else "모든 입력이 정상적으로 검증되었습니다."
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": response_text
                }
            }]
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
