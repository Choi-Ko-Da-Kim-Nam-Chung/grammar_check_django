# 제 실험용 페이지 입니다.
import requests, re, codecs
from urllib.parse import quote, unquote
from bs4 import BeautifulSoup
from bs4.element import Tag


def string_indexing(input_string):
    result = []
    originText = '띠 어 !쓰 이 ! 얶떡해? 오똑햐'
    print(originText)
    idx, unit_idx, flag = 0, 0, 0
    soup = BeautifulSoup(input_string, 'html.parser')
    for a in soup.descendants:
        print(a)
        if isinstance(a, Tag) and flag == 0: # grammar error
            flag = 1
            result.append({
                'help': '',
                'orgStr': a.text.strip(),
                'candWord': [],
                'errorIdx': unit_idx, 
                'correctMethod': 0,
                'start': idx, 
                'end': idx+len(a.text.strip()) # 끝 인덱스를 idx + 1 해야하나 말아야하나?
            })
            idx += len(a.text.strip())
            print(a.text, idx - len(a.text.strip()), idx)
            unit_idx += 1
            
        else:
            if flag:
                flag = 0
                continue
            if '\n' in a:
                a = re.sub(r'\n', '', a)
            if 0 < idx - 1 and originText[idx-1] != ' ':
                print(originText[idx-1])
                idx -= 1
            idx += len(a.strip())
        idx += 1
    
    return result



input_string = """<em class='er-3' attrtop="" id="erck_3_0" class="replace_spell" onclick="fn_SpellClick('3_0');" style="cursor:pointer">띠 어 !쓰</em> 이 ! �Z떡해? <em class='er-1' attrtop="" id="erck_1_1" class="replace_spell" onclick="fn_SpellClick('1_1');" style="cursor:pointer">오똑햐</em>"""
# 아 니!!!! ! 왜 이 래! ! !!
# print(string_indexing(input_string))
a = """<li class='er-1' id="opener_1_0">
    <dl>
        <dt>이게징짜</dt>
        <dd>
            <button type="button" class="spellOver" id="tl_errbt_1_0_0" atsrccd="1_0" atsrc="erck_1_0" errtxt="이게징짜" replacetxt="이게 진짜" onclick="fn_ShowSpellerV2('erck_1_0', '1_0', '1_0_0', '%uC774%uAC8C%uC9D5%uC9DC','%uC774%uAC8C%20%uC9C4%uC9DC','%uD754%uD788%20%uD1B5%uC2E0%uC5D0%uC11C%20%uB9D0%uC744%20%uD568%uBD80%uB85C%20%uBCC0%uD615%uD558%uAC70%uB098%2C%20%uB744%uC5B4%uC4F0%uAE30%uB97C%20%uBC14%uB974%uAC8C%20%uD558%uC9C0%20%uC54A%uB294%20%uB4F1%20%uC798%uBABB%20%uC0AC%uC6A9%uD558%uB294%20%uACBD%uD5A5%uC774%20%uC788%uC2B5%uB2C8%uB2E4.%20%uBC14%uB978%20%uD45C%uD604%uC744%20%uC0AC%uC6A9%uD574%uC57C%20%uD569%uB2C8%uB2E4.', 0,1);return false;">이게 진짜</button>
            <button type="button" class="spellOver" id="tl_errbt_1_0_1" atsrccd="1_0" atsrc="erck_1_0" errtxt="이게징짜" replacetxt="이게 징징 짜" onclick="fn_ShowSpellerV2('erck_1_0', '1_0', '1_0_1', '%uC774%uAC8C%uC9D5%uC9DC','%uC774%uAC8C%20%uC9D5%uC9D5%20%uC9DC','%uD754%uD788%20%uD1B5%uC2E0%uC5D0%uC11C%20%uB9D0%uC744%20%uD568%uBD80%uB85C%20%uBCC0%uD615%uD558%uAC70%uB098%2C%20%uB744%uC5B4%uC4F0%uAE30%uB97C%20%uBC14%uB974%uAC8C%20%uD558%uC9C0%20%uC54A%uB294%20%uB4F1%20%uC798%uBABB%20%uC0AC%uC6A9%uD558%uB294%20%uACBD%uD5A5%uC774%20%uC788%uC2B5%uB2C8%uB2E4.%20%uBC14%uB978%20%uD45C%uD604%uC744%20%uC0AC%uC6A9%uD574%uC57C%20%uD569%uB2C8%uB2E4.', 0,1);return false;">이게 징징 짜</button>
        </dd>
    </dl>
    <div class="cact-helper">
        <div class="cact">
            <h3>직접수정</h3>
            <input type="text" value="" id="tl_txt_1_0" maxlength="30">
            <button type="button" id="tl_errcustombt_1_0" atsrccd="1_0" atsrc="erck_1_0" errtxt="이게징짜" name="tl_customspellbt" onclick="fn_CustomSpellerV2('erck_1_0', '1_0', '1_0_2', '%uC774%uAC8C%uC9D5%uC9DC','','', '','');return false;">적용</button>
        </div>
        <div class="helper">
            <h3>도움말</h3>
            <span>흔히 통신에서 말을 함부로 변형하거나, 띄어쓰기를 바르게 하지 않는 등 잘못 사용하는 경향이 있습니다. 바른 표현을 사용해야 합니다.</span>
        </div>
    </div>
    <button type="button" class="opener">
        <span>열기/닫기</span>
    </button>
</li>
<li class='er-2' id="opener_2_1">
    <dl>
        <dt>해난건가</dt>
        <dd>
            <button type="button" class="spellOver" id="tl_errbt_2_1_0" atsrccd="2_1" atsrc="erck_2_1" errtxt="해난건가" replacetxt="해난 건가" onclick="fn_ShowSpellerV2('erck_2_1', '2_1', '2_1_0', '%uD574%uB09C%uAC74%uAC00','%uD574%uB09C%20%uAC74%uAC00','%uB744%uC5B4%uC4F0%uAE30%20%uC624%uB958%uC785%uB2C8%uB2E4.%20%uB300%uCE58%uC5B4%uB97C%20%uCC38%uACE0%uD558%uC5EC%20%uB744%uC5B4%20%uC4F0%uB3C4%uB85D%20%uD569%uB2C8%uB2E4.', 1,2);return false;">해난 건가</button>
        </dd>
    </dl>
    <div class="cact-helper">
        <div class="cact">
            <h3>직접수정</h3>
            <input type="text" value="" id="tl_txt_2_1" maxlength="30">
            <button type="button" id="tl_errcustombt_2_1" atsrccd="2_1" atsrc="erck_2_1" errtxt="해난건가" name="tl_customspellbt" onclick="fn_CustomSpellerV2('erck_2_1', '2_1', '2_1_1', '%uD574%uB09C%uAC74%uAC00','','', '','');return false;">적용</button>
        </div>
        <div class="helper">
            <h3>도움말</h3>
            <span>띄어쓰기 오류입니다. 대치어를 참고하여 띄어 쓰도록 합니다.</span>
        </div>
    </div>
    <button type="button" class="opener">
        <span>열기/닫기</span>
    </button>
</li>"""
class_dict = {
    'er-1' : '맞춤법 오류',
    'er-2' : '띄어쓰기 오류',
    'er-3' : '표준어 의심'
}

retult = {'help': '', 'orgStr': '택원이', 'canWord': [], 'errorIdx': 0, 'correctMethod': 0, 'start': 6, 'end': 9}, {'help': '', 'orgStr': '반나서', 'canWord': [], 'errorIdx': 1, 'correctMethod': 0, 'start': 10, 'end': 13}, {'help': '', 'orgStr': '방가워', 'canWord': [], 'errorIdx': 2, 'correctMethod': 0, 'start': 14, 'end': 17}
def ending_indexing(response, result):
    soup = BeautifulSoup(response, 'html.parser')
    li_list = soup.find_all('li')
    for idx in range(len(li_list)):
        result[idx]['correctMethod'] =  class_dict[li_list[idx].get('class')[0]] # er-1 => 맞춤법 오류, er-2 => 띄어쓰기 오류, er-3 => 표준어 의심
        result[idx]['help'] = li_list[idx].find('span').text # front에서 br로 주면 좋은지 확인 후 \n => <br>로 교체
        for i in li_list[idx].find_all('button'): # 대체 문자는 여러 개 될 수 있음
            if i.get('class') and i.get('class')[0] == 'spellOver':
                result[idx]['canWord'].append(i.get('replacetxt'))

    # print(result)
    
        
# ending_indexing(a, retult)
# result = string_indexing(input_string)
# print(result)
# print("Content inside <em> tags:", result['em_content'])
# print("Content outside <em> tags:", result['non_em_content'])

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
    # print(result)
    return result

BASE_URL = 'https://lab.incruit.com/editor/spell/spell_ajax.asp'

def check(val):
    if not val:
        return {'result': False, 'message': 'check your text'}
    
    data = {
        'md': 'spellerv2',
        'selfintro': url_encode(val)   # escape가 필요한지는 요청 내용에 따라 다름 
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    response = requests.post(BASE_URL, data=data, headers = headers)
    print(response.content)
    print()
    if response.status_code == 200:
        print(response.text)
        
originText = '띠 어 !쓰 이 ! 얶떡해? 오똑햐'
print(check(originText))
a = 65533
# print(chr(a))
def url_decode(encoded_text):
    decoded_parts = []
    i = 0
    while i < len(encoded_text):
        if encoded_text[i] == '%':
            if encoded_text[i + 1: i + 3] == '20':  # Decoding '%20' to space
                decoded_parts.append(' ')
                i += 3
            else:  # Decoding '%uXXXX' sequences
                code = int(encoded_text[i + 2: i + 6], 16)  # Extract hex code
                decoded_parts.append(chr(code))  # Convert to character
                i += 6
        else:
            decoded_parts.append(encoded_text[i])
            i += 1

    return ''.join(decoded_parts)
a = '%uB760%20%uC5B4%20!%uC4F0%20%uC774%20!%20%uC5B6%uB5A1%uD574?%20%uC624%uB611%uD590'
# decoded_string = url_decode(a)
# print(decoded_string)
encoded_string = b'\xc0\xcc ! \x9eZ\xb6\xb1\xc7\xd8?'

# Decode the string using Latin-1 encoding
# decoded_string = encoded_string.decode('euc-kr')

# print(decoded_string)