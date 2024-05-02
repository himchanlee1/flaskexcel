from flask import Flask, request, jsonify
import json, re, os

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
    # 저장
    datas = name.split('/')
    data = {
        '이름': datas[0],
        '영어이름': datas[1],
        '번호': datas[2],
        '메일': datas[3],
        '비밀번호': datas[4],
        '원내메일': datas[5]
    }
    print(data)
    with open('data.json', 'w') as f:
        json.dump(data, f)

    # 데이터 저장 확인
    with open('data.json', 'r') as f:
        data = json.load(f)
        print(data)
        print('directory', os.listdir(os.getcwd()))

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

@app.route('/gettime', methods=['POST'])
def gettime():
    time = request.get_json().get('action', {}).get('params', {}).get('sys_text', '')
    split_text = time.split('/')
    if len(split_text) < 3:
        response_text = "시간 형식이 올바르지 않습니다."
    else:
        pickup_date, pickup_time, blood_time = split_text
        response_text = f"입력된 time : {pickup_date}, {pickup_time}, {blood_time}"

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

@app.route('/validateData', methods=['POST'])
def validate_data():
    print('validation 시작.')
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
