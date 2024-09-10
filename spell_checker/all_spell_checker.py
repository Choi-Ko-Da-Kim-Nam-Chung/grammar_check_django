def adjust_indices_for_escape_characters(text, start, end):
    # 이스케이프 문자가 있는 위치를 기준으로 인덱스를 보정하는 함수
    escape_characters = ['\n', '\t', '\r']

    adjustment = 0  # 이스케이프 문자가 발견될 때마다 추가할 보정 값

    for i, char in enumerate(text):
        if i >= start and i >= end:
            break  # start와 end 모두를 지나면 중단
        if char in escape_characters:
            adjustment += 1  # 이스케이프 문자는 두 칸을 차지하므로 보정 값 추가

    # 인덱스를 보정된 값으로 반환
    return start + adjustment, end + adjustment
