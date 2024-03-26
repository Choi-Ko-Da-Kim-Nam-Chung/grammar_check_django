from . import busan_spell_checker
from . import saramin_spell_checker
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def busanSpellChecker(request):
    # request.body를 읽어 문자열로 변환합니다.
    body_str = request.body.decode('utf-8')
    result = busan_spell_checker.check(u'안녕하시렵니까')

    # 처리 결과를 JSON으로 반환합니다.
    return HttpResponse(
        json.dumps(result, ensure_ascii=False),
        content_type='application/json',
    )
@csrf_exempt
def saraminSpellChecker(request):
    body_str = request.body.decode('utf-8')
    result = saramin_spell_checker.check(u'안녕하시렵니까')

    return HttpResponse(
        json.dumps(result, ensure_ascii=False),
        content_type='application/json',
    )
