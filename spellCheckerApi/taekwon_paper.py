# 제 실험용 페이지 입니다.
import requests, re, codecs
from urllib.parse import quote, unquote
from bs4 import BeautifulSoup
from bs4.element import Tag


def string_indexing(input_string):
    result = []
    idx, unit_idx, flag = 0, 0, 0
    soup = BeautifulSoup(input_string, 'html.parser')
    for a in soup.descendants:
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
            unit_idx += 1
        elif a.isspace(): 
            continue
        else:
            
            if flag:
                flag = 0
                continue
            idx += len(a.strip())
        idx += 1
    
    return result


    


input_string = """안녕? 나 <em class='er-1' attrtop="" id="erck_1_0" class="replace_spell" onclick="fn_SpellClick('1_0');" style="cursor:pointer">택원이</em>
<em class='er-3' attrtop="" id="erck_3_1" class="replace_spell" onclick="fn_SpellClick('3_1');" style="cursor:pointer">반나서</em>
<em class='er-3' attrtop="" id="erck_3_2" class="replace_spell" onclick="fn_SpellClick('3_2');" style="cursor:pointer">방가워</em>
하하 내일 봐#^#"""
"""
<p id="spellingAlltest" class="text_edit_area" style="display:none">
    안녕? 나 <em class='er-1' attrtop="" id="erck_1_0" class="replace_spell" onclick="fn_SpellClick('1_0');" style="cursor:pointer">태권이</em>
    <em class='er-3' attrtop="" id="erck_3_1" class="replace_spell" onclick="fn_SpellClick('3_1');" style="cursor:pointer">반라서</em>
    <em class='er-3' attrtop="" id="erck_3_2" class="replace_spell" onclick="fn_SpellClick('3_2');" style="cursor:pointer">반가워</em>
    하하 내일 봐
</p>
#^#
"""
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
    
        
ending_indexing(a, retult)
# result = string_indexing(input_string)
# print(result)
# print("Content inside <em> tags:", result['em_content'])
# print("Content outside <em> tags:", result['non_em_content'])