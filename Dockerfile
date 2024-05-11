# 베이스 이미지 설정
FROM python:3.10

# 패키지 업데이트 및 libgl1-mesa-glx 설치
RUN apt-get update && \
    apt-get -y install libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# 나머지 작업 진행
