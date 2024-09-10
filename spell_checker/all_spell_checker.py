def adjust_indices_for_escape_characters(text, start, end):
    # 이스케이프 문자가 있는 위치를 기준으로 인덱스를 보정하는 함수
    escape_characters = ['\n', '\t', '\r']

    for i, char in enumerate(text):
        if i >= end:
            break  # start와 end 모두를 지나면 중단
        if char in escape_characters:
            end+=1
            start+=1
            if i >= start:
                return -1, -1

    # 인덱스를 보정된 값으로 반환
    return start, end
