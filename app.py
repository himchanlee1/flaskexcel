from flask import Flask, request, jsonify
import json, re, os

app = Flask(__name__)
 
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

@app.route('/getInfo', methods=['POST']) # <- 이거 안 쓰는 것 같은데..?
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
    name = request.get_json()['action']['params']['sys_text']
    # 저장
    print(name)
    datas = list(name.split('/'))
    print(datas)
    if len(datas) == 6:
        data = {
            '이름': datas[0],
            '영어이름': datas[1],
            '번호': datas[2],
            '메일': datas[3],
            '비밀번호': datas[4],
            '원내메일': datas[5]
        }
        print(data)
        with open('info.json', 'w') as f:
            json.dump(data, f)

        # 데이터 저장 확인
        with open('info.json', 'r') as f:
            data = json.load(f)
            print(data)
            print('directory', os.listdir(os.getcwd()))
    else:
        name = "입력된 정보의 형식이 올바르지 않습니다."

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": f"입력된 정보 : {name}"
                }
            }]
        }
    })

@app.route('/gettime', methods=['POST'])
def gettime():
    time = request.get_json()['action']['params']['sys_text']
    split_text = time.split('/')
    if len(split_text) < 3:
        response_text = "시간 형식이 올바르지 않습니다."
    else:
        pickup_date, pickup_time, blood_time = split_text
        response_text = f"입력된 time : {pickup_date}, {pickup_time}, {blood_time}"
        
        # 픽업날짜, 픽업시간, 채혈날짜 수정은 data.json의 일부만 수정하면 되기에 아래의 코드를 사용
        with open('data.json', 'r') as f:
            data = json.load(f)
        
        data["픽업날짜"] = pickup_date
        data["픽업시간"] = pickup_time
        data["채혈날짜"] = blood_time

        with open('data.json', 'w') as f:
            json.dump(data, f)

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


# VAL COMPLETE.
def validate_input(data): # info.json의 검증 함수
    errors = []
    if not data.get('이름', '').strip():
        errors.append("이름이 누락되었습니다.")
    if not data.get('영어이름', '').strip():
        errors.append("영어 이름이 누락되었습니다.")
    if not data.get('번호', '').strip():
        errors.append("전화번호가 누락되었습니다.")
    if not re.match(r"^\S+@\S+\.\S+$", data.get('메일', '')):
        errors.append("유효한 이메일 주소가 아닙니다.")
    if not data.get('비밀번호', '').strip():
        errors.append("비밀번호가 누락되었습니다.")
    if not re.match(r"^\S+@\S+\.\S+$", data.get('원내메일', '')):
        errors.append("유효한 원내 메일 주소가 아닙니다.")
    return errors

def validate_data(data): # data.json의 검증 함수
    errors = []
    if not data.get('픽업날짜', '').strip():
        errors.append("픽업날짜가 누락되었습니다.")
    if not data.get('픽업시간', '').strip():
        errors.append("픽업시간이 누락되었습니다.")
    if not data.get('채혈날짜', '').strip():
        errors.append("채혈날짜가 누락되었습니다.")

    if len(data.get('이미지주소', '')) == 0: # 저장된 이미지가 0개이면 오류.
        errors.append('전송된 이미지가 없습니다.')

    return errors

@app.route('/validateData', methods=['POST'])
def validate():
    print('validation 시작.')
    # input_data = request.get_json()['action']['params']['sys_text']
    # print('input_data:', input_data)

    with open('info.json', 'r') as f:
        input_data = json.load(f) 
        errors = validate_input(input_data)
        isValid = {
            'valid': 0
        }
        if len(errors) == 0:
            # 에러가 존재하지 않음. 
            isValid = {
                'valid': 1
            }
        
        with open('data.json', 'r') as f: # data.json도 검사.
            data = json.load(f)
            errors = validate_data(data)
            if len(errors) > 0:
                isValid = {
                    'valid': 0
                }

        with open('validation.json', 'w') as f:
            json.dump(isValid, f)

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
