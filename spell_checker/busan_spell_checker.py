import re
import requests
import json
from spell_checker.all_spell_checker import adjust_indices_for_escape_characters


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
        data = parse_response(response.text, text)
        # 여기서 `parse_response`는 응답 텍스트를 처리하고 필요한 데이터를 추출하는 함수입니다.
        # 이 함수는 두 번째 코드에서 `parseJSON` 함수의 로직을 참고하여 구현해야 합니다.
        return data
    else:
        return {'result': False, 'message': 'Failed to get a valid response from the server.'}

def parse_response(response_text, original_text):
    data = extract_data_from_html(response_text)

    if not data:
        return None

    results = []

    for error_info in data[0]['errInfo']:
        # 오류의 원래 start, end 인덱스
        start = error_info['start']
        end = error_info['end']

        # 이스케이프 문자로 인한 인덱스 보정
        adjusted_start, adjusted_end = adjust_indices_for_escape_characters(original_text, start, end)
        
        if adjusted_start == -1 and adjusted_end == -1:
            continue
        
        error_details = {
            'help': error_info['help'],  # 오류를 해결하기 위한 도움말
            'orgStr': error_info['orgStr'],  # 오류가 발생한 원래 문자열
            'candWord': error_info['candWord'].split('|'),  # 교정 제안
            'errorIdx': error_info['errorIdx'],  # 오류 인덱스
            'correctMethod': error_info['correctMethod'],  # 교정 방법
            'start': adjusted_start,  # 보정된 start 인덱스
            'end': adjusted_end,  # 보정된 end 인덱스
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