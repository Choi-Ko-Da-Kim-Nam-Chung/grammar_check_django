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
        <dt>택원이</dt>
        <dd>
            <button type="button" class="spellOver" id="tl_errbt_1_0_0" atsrccd="1_0" atsrc="erck_1_0" errtxt="택원이" replacetxt="태권이" onclick="fn_ShowSpellerV2('erck_1_0', '1_0', '1_0_0', '%uD0DD%uC6D0%uC774','%uD0DC%uAD8C%uC774','%uCCA0%uC790%20%uAC80%uC0AC%uB97C%20%uD574%20%uBCF4%uB2C8%20%uC774%20%uC5B4%uC808%uC740%20%uBD84%uC11D%uD560%20%uC218%20%uC5C6%uC73C%uBBC0%uB85C%20%uD2C0%uB9B0%20%uB9D0%uB85C%20%uD310%uB2E8%uD558%uC600%uC2B5%uB2C8%uB2E4.%0D%0A%0D%0A%uD6C4%uBCF4%20%uC5B4%uC808%uC740%20%uC774%20%uCCA0%uC790%uAC80%uC0AC/%uAD50%uC815%uAE30%uC5D0%uC11C%20%uB744%uC5B4%uC4F0%uAE30%2C%20%uBD99%uC5EC%20%uC4F0%uAE30%2C%20%uC74C%uC808%uB300%uCE58%uC640%20%uAC19%uC740%20%uAD50%uC815%uBC29%uBC95%uC5D0%20%uB530%uB77C%20%uC218%uC815%uD55C%20%uACB0%uACFC%uC785%uB2C8%uB2E4.%0D%0A%0D%0A%uD6C4%uBCF4%20%uC5B4%uC808%20%uC911%20%uC120%uD0DD%uD558%uC2DC%uAC70%uB098%20%uC624%uB958%20%uC5B4%uC808%uC744%20%uC218%uC815%uD558%uC5EC%20%uC8FC%uC2ED%uC2DC%uC624.%0D%0A%0D%0A*%20%uB2E8%2C%20%uC0AC%uC804%uC5D0%20%uC5C6%uB294%20%uB2E8%uC5B4%uC774%uAC70%uB098%20%uC0AC%uC6A9%uC790%uAC00%20%uC62C%uBC14%uB974%uB2E4%uACE0%20%uD310%uB2E8%uD55C%20%uC5B4%uC808%uC5D0%20%uB300%uD574%uC11C%uB294%20%uD1B5%uACFC%uD558%uC138%uC694%21%21', 0,1);return false;">태권이</button>
        </dd>
    </dl>
    <div class="cact-helper">
        <div class="cact">
            <h3>직접수정</h3>
            <input type="text" value="" id="tl_txt_1_0" maxlength="30">
            <button type="button" id="tl_errcustombt_1_0" atsrccd="1_0" atsrc="erck_1_0" errtxt="택원이" name="tl_customspellbt" onclick="fn_CustomSpellerV2('erck_1_0', '1_0', '1_0_1', '%uD0DD%uC6D0%uC774','','', '','');return false;">적용</button>
        </div>
        <div class="helper">
            <h3>도움말</h3>
            <span>철자 검사를 해 보니 이 어절은 분석할 수 없으므로 틀린 말로 판단하였습니다.

후보 어절은 이 철자검사/교정기에서 띄어쓰기, 붙여 쓰기, 음절대치와 같은 교정방법에 따라 수정한 결과입니다.

후보 어절 중 선택하시거나 오류 어절을 수정하여 주십시오.

* 단, 사전에 없는 단어이거나 사용자가 올바르다고 판단한 어절에 대해서는 통과하세요!!</span>
        </div>
    </div>
    <button type="button" class="opener">
        <span>열기/닫기</span>
    </button>
</li>
<li class='er-3' id="opener_3_1">
    <dl>
        <dt>반나서</dt>
        <dd>
            <button type="button" class="spellOver" id="tl_errbt_3_1_0" atsrccd="3_1" atsrc="erck_3_1" errtxt="반나서" replacetxt="반라서" onclick="fn_ShowSpellerV2('erck_3_1', '3_1', '3_1_0', '%uBC18%uB098%uC11C','%uBC18%uB77C%uC11C','%uB450%uC74C%uBC95%uCE59%uC740%20%uB2E8%uC5B4%uC758%20%uCCAB%20%uC74C%uC808%uC5D0%uB9CC%20%uC801%uC6A9%uD569%uB2C8%uB2E4.%20%uC544%uB2C8%uBA74%20%uC790%uD310%20%uC704%uCE58%uAC00%20%uBE44%uC2B7%uD558%uC5EC%20%uC798%uBABB%20%uD45C%uAE30%uD558%uC168%uC744%20%uC218%uB3C4%20%uC788%uC2B5%uB2C8%uB2E4.', 1,2);return false;">반라서</button>
        </dd>
    </dl>
    <div class="cact-helper">
        <div class="cact">
            <h3>직접수정</h3>
            <input type="text" value="" id="tl_txt_3_1" maxlength="30">
            <button type="button" id="tl_errcustombt_3_1" atsrccd="3_1" atsrc="erck_3_1" errtxt="반나서" name="tl_customspellbt" onclick="fn_CustomSpellerV2('erck_3_1', '3_1', '3_1_1', '%uBC18%uB098%uC11C','','', '','');return false;">적용</button>
        </div>
        <div class="helper">
            <h3>도움말</h3>
            <span>두음법칙은 단어의 첫 음절에만 적용합니다. 아니면 자판 위치가 비슷하여 잘못 표기하셨을 수도 있습니다.</span>
        </div>
    </div>
    <button type="button" class="opener">
        <span>열기/닫기</span>
    </button>
</li>
<li class='er-3' id="opener_3_2">
    <dl>
        <dt>방가워</dt>
        <dd>
            <button type="button" class="spellOver" id="tl_errbt_3_2_0" atsrccd="3_2" atsrc="erck_3_2" errtxt="방가워" replacetxt="반가워" onclick="fn_ShowSpellerV2('erck_3_2', '3_2', '3_2_0', '%uBC29%uAC00%uC6CC','%uBC18%uAC00%uC6CC','%uC624%uB298%uB0A0%20%uD1B5%uC2E0%uC5D0%uC11C%20%uC790%uC8FC%20%uC4F0%uB294%20%uC740%uC5B4%uC785%uB2C8%uB2E4.', 2,3);return false;">반가워</button>
        </dd>
    </dl>
    <div class="cact-helper">
        <div class="cact">
            <h3>직접수정</h3>
            <input type="text" value="" id="tl_txt_3_2" maxlength="30">
            <button type="button" id="tl_errcustombt_3_2" atsrccd="3_2" atsrc="erck_3_2" errtxt="방가워" name="tl_customspellbt" onclick="fn_CustomSpellerV2('erck_3_2', '3_2', '3_2_1', '%uBC29%uAC00%uC6CC','','', '','');return false;">적용</button>
        </div>
        <div class="helper">
            <h3>도움말</h3>
            <span>오늘날 통신에서 자주 쓰는 은어입니다.</span>
        </div>
    </div>
    <button type="button" class="opener">
        <span>열기/닫기</span>
    </button>
</li>
#^#3"""
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
        result[idx]['canWord'].append(li_list[idx].find('button').text)

    print(result)
    
        
ending_indexing(a, retult)
# result = string_indexing(input_string)
# print(result)
# print("Content inside <em> tags:", result['em_content'])
# print("Content outside <em> tags:", result['non_em_content'])