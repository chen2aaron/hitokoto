import os
import sys
import argparse
import logging
from time import sleep, time
from logging.config import fileConfig

import requests

from database import db_session
from models import Hitokoto


fileConfig('logging_config.ini')
logger = logging.getLogger()

url = 'http://api.hitokoto.us/rand'
START_TIME = time()


def hitokoto_script(delay):
    resp = requests.get(url)
    sleep(delay)

    data = resp.json()
    if db_session.query(Hitokoto).get(data['id']):
        logger.warning('This data already exists: %s %s' % (data['id'], data['hitokoto']))
        return False
    hitokoto = Hitokoto(**data)
    db_session.add(hitokoto)
    db_session.commit()
    logger.warning('This data insert success: %s %s' % (data['id'], data['hitokoto']))
    return True


def show_progress_bar(progress, start_time, msg):
    """
    Well, it's a fancy progress bar, it looks like this:
    Msg:        50.0% [=========================>                          ]      in 0.9s
    :param progress: range 0 to 100
    :param start_time: looks like time.time()
    :param msg: message to show
    :return:
    """
    screen_width = os.get_terminal_size().columns // 10 * 10 - 40
    bar_width = int(progress * screen_width / 100)
    progress_bar = (msg + ": " + " " * 10)[:9] + \
                   (" " * 4 + str(int(progress)) + "%")[-6:] + \
                   (" [" + bar_width * "=" + ">" + " " * int(screen_width - bar_width) + "]") + \
                   ("      in " + str(round(time() - start_time, 1)) + "s")
    sys.stdout.write(progress_bar + "\r")
    sys.stdout.flush()


def main(cycle, delay):
    count = 0
    while cycle > count:
        created = hitokoto_script(delay)
        if created:
            show_progress_bar(((count + 1) * 100 // cycle), START_TIME, "Insert")
        else:
            show_progress_bar(((count + 1) * 100 // cycle), START_TIME, "Exists")
        count += 1


def parse_arguments():
    parser = argparse.ArgumentParser(prog="app", description="hitokoto script")
    parser.add_argument("-c", help="cycle number", type=int)
    parser.add_argument("-d", help="request delay second, default 0.3s", type=float, default=0.3)
    if not parser.parse_args().c:
        logger.warning("Missing arguments: cycle.\nUsage: python app.py -h")
        exit()
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.c, args.d)
