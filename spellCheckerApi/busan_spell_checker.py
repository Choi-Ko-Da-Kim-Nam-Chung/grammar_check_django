import re
import requests
import json

# 수정된 부분: `base_url`을 부산대학교 맞춤법 검사기 URL로 설정
base_url = 'http://speller.cs.pusan.ac.kr/results'

def check(text):
    if isinstance(text, list):
        result = []
        for item in text:
            checked = check(item)
            result.append(checked)
        return result

    if len(text) > 500:
        # 여기서는 체크할 수 있는 글자 수 제한을 설정합니다.
        return {'result': False, 'message': 'Text exceeds the maximum allowed length.'}

    payload = {
        'text1': text
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(base_url, data=payload, headers=headers)

    if response.status_code == 200:
        data = parse_response(response.text)
        # 여기서 `parse_response`는 응답 텍스트를 처리하고 필요한 데이터를 추출하는 함수입니다.
        # 이 함수는 두 번째 코드에서 `parseJSON` 함수의 로직을 참고하여 구현해야 합니다.
        return data
    else:
        return {'result': False, 'message': 'Failed to get a valid response from the server.'}

def parse_response(response_text):
    # Since `extract_data_from_html` already returns a Python object, we don't need to parse it again.
    data = extract_data_from_html(response_text)
    
    if not data:
        return None  # or handle the error as appropriate

    # 결과를 저장할 리스트를 초기화합니다.
    results = []
    
    # `errInfo` 배열을 순회하면서 각 오류에 대한 정보를 추출합니다.
    for error_info in data[0]['errInfo']:
        error_details = {
            'help': error_info['help'],  # 오류를 해결하기 위한 도움말
            'orgStr': error_info['orgStr'],  # 오류가 발생한 원래 문자열
            'candWord': error_info['candWord'].split('|'),  # 교정 제안
            'errorIdx': error_info['errorIdx'],  # 오류 인덱스
            'correctMethod': error_info['correctMethod'],  # 교정 방법
            'start': error_info['start'],  # 오류가 시작되는 위치
            'end': error_info['end'],  # 오류가 끝나는 위치
        }
        results.append(error_details)
    
    return results

def extract_data_from_html(html_content):
    # `data` 변수에 할당된 JSON 데이터를 찾기 위한 정규 표현식
    pattern = re.compile(r'data\s*=\s*(\[{.*?}\]);', re.DOTALL)
    
    # 정규 표현식을 사용하여 HTML에서 JSON 문자열을 찾습니다.
    match = pattern.search(html_content)
    if match:
        json_data = match.group(1)
        try:
            # JSON 문자열을 파싱하여 Python 객체로 변환합니다.
            data = json.loads(json_data)
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No data found")
        return None