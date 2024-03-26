import requests
from urllib.parse import quote, unquote
from bs4 import BeautifulSoup
from bs4.element import Tag

BASE_URL = 'https://lab.incruit.com/editor/spell/spell_ajax.asp'

def string_indexing(response):
    result = []
    idx, unit_idx, flag = 0, 0, 0
    soup = BeautifulSoup(response, 'html.parser')
    
    for unit in soup.descendants:
        if isinstance(unit, Tag) and flag == 0: # grammar error
            flag = 1
            result.append({
                'help': '',
                'orgStr': unit.text.strip(),
                'canWord': [],
                'errorIdx': unit_idx, 
                'correctMethod': 0,
                'start': idx, 
                'end': idx+len(unit.text.strip())
            })
            idx += len(unit.text.strip())
            unit_idx += 1
        elif unit.isspace(): 
            continue
        else:
            if flag:
                flag = 0
                continue
            idx += len(unit.strip())
        idx += 1
        
    # print('string_indexing done', result)
    return result

class_dict = {
    'er-1' : '맞춤법 오류',
    'er-2' : '띄어쓰기 오류',
    'er-3' : '표준어 의심'
}

def ending_indexing(response, result):
    soup = BeautifulSoup(response, 'html.parser')
    li_list = soup.find_all('li')
    for idx in range(len(li_list)):
        result[idx]['correctMethod'] =  class_dict[li_list[idx].get('class')[0]] # er-1 => 맞춤법 오류, er-2 => 띄어쓰기 오류, er-3 => 표준어 의심
        result[idx]['help'] = li_list[idx].find('span').text # front에서 br로 주면 좋은지 확인 후 \n => <br>로 교체
        result[idx]['canWord'].append(li_list[idx].find('button').text.strip())

    # print('ending_indexing done', result)
    return result


def url_encode(text):
    encoded_parts = []
    for char in text:
        if ' ' == char:  # space
            encoded_parts.append('%20')
        elif ord(char) < 128: # english
            encoded_parts.append(char)
        else: # korean
            encoded_parts.append('%u{:04X}'.format(ord(char)))
    result = ''.join(encoded_parts)
    
    # print('url_encode done', result)
    return result


def parse_html(response):
    wrong_text_num = int(response[-1])
    if wrong_text_num == 0:
        return {'result': 0, 'message': 'correct grammar'} # -1 : 서버 에러 0 : 오류 문장 0개 1: 오류 문장 1개 ...
    
    parsed_list = response.split('#^#')
    result = string_indexing(parsed_list[0])
    result = ending_indexing(parsed_list[2], result)
    
    # print('parse_html done', result)
    return result
    
    
def check(val):
    
    data = {
        'md': 'spellerv2',
        'selfintro': url_encode(val)   # escape가 필요한지는 요청 내용에 따라 다름 
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    response = requests.post(BASE_URL, data=data, headers = headers)

    if response.status_code == 200:
        return parse_html(response.text)
    else:
        return {'result': False, 'message': 'Failed to get a valid response from the server.'}
    
    
# print(check("안되 조금 더 살펴보고 틀린게 없는지 보아ㅑ지"))
""" 'help': '의존 명사는 앞의 어미와 띄어 써야 합니다. 또한 문장 성분이 다른 단어나 명사가 덧붙을 때는 각각의 단어를 띄어 씀이 바릅니다.[맞춤법 표준안 42조]\r\n\r\n  (예) 먹은거고 (x) -> 먹은 거고  (o)\r\n      먹은거냐 (x) -> 먹은 거냐  (o)\r\n      할바있다 (x) -> 할 바 있다 (o)\r\n      한셈치다 (x) -> 한 셈 치다 (o)\r\n      온듯도   (x) -> 온 듯도    (o)\r\n      할바를   (x) -> 할 바를    (o)\r\n      할수가   (x) -> 할 수가    (o)\r\n      할테다   (x) -> 할 테다    (o)' """