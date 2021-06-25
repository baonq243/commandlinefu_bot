FROM python:3

LABEL org.opencontainers.image.source https://github.com/baonq243/commandlinefu_bot

WORKDIR /app

ADD requirements.txt .

ADD main.py .

RUN pip3 install -r requirements.txt

CMD [ "python", "./main.py" ]