#!/usr/local/python3
# -*- coding: utf-8 -*-

import requests
import telegram
import schedule
import time
import os
import datetime
import logging
from logging.handlers import RotatingFileHandler


logging.basicConfig(filename="running.log", level=logging.INFO, format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")
logger = logging.getLogger('my_bot')
handler = RotatingFileHandler('running.log', maxBytes=500000, backupCount=5)
logger.addHandler(handler)


def parser_tele(msg):
    for i in list_escape:
        msg = msg.replace(i, "\\{}".format(i))
    return msg


def get_command():
    try:
        n = 0
        while n < 10000:
            r = requests.get('http://www.commandlinefu.com/commands/browse/sort-by-votes/json/{}'.format(n))
            for i in r.json():
                with open('list_id.txt', 'r') as r:
                    lines = r.read().splitlines()
                if i["id"] not in lines:
                    with open('list_id.txt', 'a+') as w:
                        w.write(i["id"] + "\n")
                        msg = "*{}* (_Vote_: `{}`)\n" \
                              "\n`{}`\n" \
                              "\n{}".format(parser_tele(i["summary"]), parser_tele(i["votes"]),
                                            parser_tele(i["command"]), parser_tele(i["url"]))
                        logger.info(i["summary"], i["votes"], i["command"], i["url"])
                        bot.send_message(CHAT_ID, msg, parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                         disable_web_page_preview=True)
                    return
            n = n + 25
    except Exception as e:
        logger.error(e)
        print(e)


def job():
    try:
        today = datetime.datetime.today().weekday()
        timenow = datetime.datetime.now().time()
        start = datetime.time(8, 0, 0)
        end1 = datetime.time(20, 0, 0)
        if today in range(0, 4):
            if start <= timenow <= end1:
                get_command()
            else:
                print("De yen cho tao ngu")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    TELEGRAM_TOKEN = os.getenv('TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')
    list_escape = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    job()
    schedule.every(10).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
