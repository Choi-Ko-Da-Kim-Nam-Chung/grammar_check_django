from django.shortcuts import render
from . import spell_checker, incruit_api
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def busanSpellChecker(request):
    # request.body를 읽어 문자열로 변환합니다.
    body_str = request.body.decode('utf-8')
    result = spell_checker.check(body_str)

    # 처리 결과를 JSON으로 반환합니다.
    return HttpResponse(
        json.dumps(result),
        content_type='application/json',
    )

@csrf_exempt
def incruitSpellChecker(request):
    # request.body를 읽어 문자열로 변환합니다.
    body_str = request.body.decode('utf-8')
    result = incruit_api.check(body_str)

    # 처리 결과를 JSON으로 반환합니다.
    return HttpResponse(
        json.dumps(result),
        content_type='application/json',
    )
