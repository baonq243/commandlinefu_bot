FROM python:3.9.6-slim-buster

LABEL org.opencontainers.image.source https://github.com/baonq243/commandlinefu_bot

RUN mkdir /app

WORKDIR /app

ADD ./app .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" ]