# 사용할 Python 이미지 선택
FROM python:3.9-slim

# 환경변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gevent  # gevent 설치

# 프로젝트 코드 복사
COPY . /app/

# static 파일 수집
RUN python manage.py collectstatic --noinput

# 애플리케이션 서버 실행 (gunicorn 설정 업데이트)
CMD ["gunicorn", "--workers", "4", "--worker-class", "gevent", "--bind", "0.0.0.0:8000", "spellchecker.wsgi:application"]