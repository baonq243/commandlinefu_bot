FROM python:3

LABEL org.opencontainers.image.source https://github.com/baonq243/commandlinefu_bot

RUN mkdir /app

WORKDIR /app

ADD requirements.txt .

ADD main.py .

ADD list_id.txt .

RUN pip3 install -r requirements.txt

CMD [ "python", "./main.py" ]