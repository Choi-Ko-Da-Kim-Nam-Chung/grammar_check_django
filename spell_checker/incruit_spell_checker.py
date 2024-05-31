import requests, re
from bs4 import BeautifulSoup
from bs4.element import Tag

BASE_URL = 'https://lab.incruit.com/editor/spell/spell_ajax.asp'

def string_indexing(response, originText, space_num):
    # print(response)
    result = []
    idx, unit_idx, flag = space_num, 0, 0
    soup = BeautifulSoup(response, 'html.parser')
    # originText 비교해가며 인덱싱 해야함.
    for unit in soup.descendants:
        
        if unit == ' ':
            continue
        if isinstance(unit, Tag) and flag == 0: # grammar error
            if unit.name == 'br':
                continue
            flag = 1
            result.append({
                'orgStr': unit.text.strip(),
                'candWord': [],
                'errorIdx': unit_idx, 
                'correctMethod': 0,
                'help': '',
                'start': idx, 
                'end': idx+len(unit.text.strip())
            })
            # print(unit.text + "!끝!" + str(len(unit.text.strip())) +' '+ str(len(unit.text)) + ' '+str(idx) + ' ' + str(idx + len(unit.text.strip())))
            
            idx += len(unit.text.strip())
            unit_idx += 1
            
            
        else:
            if flag:
            # 2번 나오기 때문에 이미 위에서 처리했으면 flag = 1
                flag = 0
                continue
            if '\n' in unit:
            # 엔터가 있으면 공백으로 바꿔줌
                unit = re.sub(r'\n', '', unit)
            if 0 < idx - 1 and originText[idx-1] != ' ':
                idx -= 1
            # 중간에 올바른 맞춤법을 갖고있는 문자열 더해주기
            # print(unit.text, len(unit.text), str(len(unit.strip())) + ' '+str(idx) + ' ' + str(idx + len(unit.strip())), "pass")
            idx += len(unit.strip())
            if unit[-1] != ' ':
                idx -= 1
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
        for i in li_list[idx].find_all('button'): # 대체 문자는 여러 개 될 수 있음
            if i.get('class') and i.get('class')[0] == 'spellOver':
                result[idx]['candWord'].append(i.get('replacetxt'))

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


def parse_html(response, originText, space_num):
    wrong_text_num = int(response[-1])
    if wrong_text_num == 0:
        # 틀린 문장이 없으면 빈 리스트 반환
        return [] #{'result': 0, 'message': 'correct grammar'} # -1 : 서버 에러 0 : 오류 문장 0개 1: 오류 문장 1개 ...
    
    parsed_list = response.split('#^#')
    result = string_indexing(parsed_list[0], originText, space_num)
    result = ending_indexing(parsed_list[2], result)
    
    # print('parse_html done', result)
    return result
    
    
def check(val):
    val = val['text']
    if not val:
        return []
    
    # 맨 앞에 공백이 있으면 incruit에서 자동으로 제거 후 반환함.
    space_num = len(val) - len(val.lstrip())
    data = {
        'md': 'spellerv2',
        'selfintro': url_encode(val)   # escape가 필요한지는 요청 내용에 따라 다름 
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    response = requests.post(BASE_URL, data=data, headers = headers)

    if response.status_code == 200:
        return parse_html(response.text, val, space_num)
    else:
        # 에러시 빈 리스트 반환
        return []
'''{
'result': False, 
'message': 'Failed to get a valid response from the server.'
}'''
    
    
# print(check("안되 조금 더 살펴보고 틀린게 없는지 보아ㅑ지"))
""" 'help': '의존 명사는 앞의 어미와 띄어 써야 합니다. 또한 문장 성분이 다른 단어나 명사가 덧붙을 때는 각각의 단어를 띄어 씀이 바릅니다.[맞춤법 표준안 42조]\r\n\r\n  (예) 먹은거고 (x) -> 먹은 거고  (o)\r\n      먹은거냐 (x) -> 먹은 거냐  (o)\r\n      할바있다 (x) -> 할 바 있다 (o)\r\n      한셈치다 (x) -> 한 셈 치다 (o)\r\n      온듯도   (x) -> 온 듯도    (o)\r\n      할바를   (x) -> 할 바를    (o)\r\n      할수가   (x) -> 할 수가    (o)\r\n      할테다   (x) -> 할 테다    (o)' """