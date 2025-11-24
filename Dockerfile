FROM python:3.13-slim-trixie

COPY --from=denoland/deno:bin /deno /usr/local/bin/deno

RUN apt-get update && apt-get -y upgrade && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY check.py /opt/resource/check
COPY in.py /opt/resource/in
