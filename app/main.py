#!/usr/local/python3
# -*- coding: utf-8 -*-

import requests
import telegram
import schedule
import time
import os


def parser_tele(msg):
    for i in list_escape:
        msg = msg.replace(i, "\\{}".format(i))
    return msg


def job():
    try:
        n = 0
        while n < 10000:
            r = requests.get('http://www.commandlinefu.com/commands/browse/sort-by-votes/json/{}'.format(n))
            for i in r.json():
                print(i["id"], i["command"], i["summary"], i["votes"], i["url"])
                with open('list_id.txt', 'r') as r:
                    lines = r.read().splitlines()
                if i["id"] not in lines:
                    with open('list_id.txt', 'a+') as w:
                        w.write(i["id"]+"\n")
                        msg = "_ID_: `{}`, _Vote_: `{}`\n" \
                              "_Command_: `{}`\n" \
                              "_Description_: `{}`\n" \
                              "_URL_: `{}`".format(parser_tele(i["id"]), parser_tele(i["votes"]), parser_tele(i["command"]), parser_tele(i["summary"]), parser_tele(i["url"]))
                        bot.send_message(CHAT_ID, msg, parse_mode=telegram.ParseMode.MARKDOWN_V2)
                    return
            n = n + 25
    except Exception as e:
        print(e)


if __name__ == '__main__':
    TELEGRAM_TOKEN = os.getenv('TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')
    list_escape = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    schedule.every(5).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
