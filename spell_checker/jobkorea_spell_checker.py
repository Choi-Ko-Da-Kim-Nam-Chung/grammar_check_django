import re
import requests
import json

base_url = 'https://www.jobkorea.co.kr/Service/User/Tool/SpellCheckExecute'

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
        'tBox': text
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.jobkorea.co.kr',
        'Referer': 'https://www.jobkorea.co.kr/service/user/tool/spellcheck?TS_XML=3',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    response = requests.post(base_url, data=payload, headers=headers)

    if response.status_code == 200:
        data = parse_response(response.text, text)
        return data
    else:
        return { 'result': False, 'message': 'Failed to get a valid response from the server.' }

def parse_response(response_text, text):
    # Since `extract_data_from_html` already returns a Python object, we don't need to parse it again.
    data = json.loads(response_text)
    results = []

    # `errInfo` 배열을 순회하면서 각 오류에 대한 정보를 추출합니다.

    current_idx = 0

    if 'WordCandidateList' in data:
        for error_info in data['WordCandidateList']:
            correct_method_value = calculate_correct_method(error_info['helpMessage'])

            start_idx = calculate_idx(error_info['errorWord'], current_idx, text)
            end_idx = start_idx + len(error_info['errorWord'])
            error_details = {
                'help': error_info['helpMessage'],  # 오류를 해결하기 위한 도움말
                'orgStr': error_info['errorWord'],  # 오류가 발생한 원래 문자열
                'candWord': remove_html(error_info['candidateWord']),  # 교정 제안
                'errorIdx': start_idx,  # 오류 인덱스
                'correctMethod': correct_method_value,  # 교정 방법
                'start': start_idx,  # 오류가 시작되는 위치
                'end': end_idx,  # 오류가 끝나는 위치
            }
            results.append(error_details)
            current_idx = end_idx

    return results
def remove_html(html_str):
    # HTML 태그를 제거하고 결과물을 리스트로 변환합니다.
    texts = re.findall(r'>[^<]+<', html_str)
    # 각 텍스트에서 앞뒤의 '>'와 '<'를 제거합니다.
    cleaned_texts = [text[1:-1] for text in texts]
    return cleaned_texts

def calculate_idx(error_str, current_idx, text):
    start_idx = text.find(error_str, current_idx)
    return start_idx

def calculate_correct_method(str):
    if '틀린 말' in str: return 1
    elif '붙' in str or '띄' in str: return 2
    else: return 1