FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY check.py /opt/resource/check
COPY in.py /opt/resource/in
