import random
import time
import logging
import os
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
LOG_DIR = os.path.join(BASE_DIR, "logs", "bot.log")


def sleep_random(min_t=2, max_t=3) -> float:
    sleep_time = random.uniform(min_t, max_t)
    time.sleep(sleep_time)
    return sleep_time


def parse_time_to_seconds(t: str) -> int:
    """needs hour:minutes:seconds as paramter, returns time in seconds"""
    timelist = t.split(":")
    seconds = int(timelist[0]) * 60 * 60 + int(timelist[1]) * 60 + int(timelist[2])

    return seconds


def log(text: str):
    logging.basicConfig(format='%(asctime)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p',
                        filename=LOG_DIR,
                        level=logging.INFO, filemode='w')
    logger = logging.getLogger()
    logger.info(text)


def clean_numbers(nb) -> int:
    nb_text = nb
    if nb_text.find(',') or nb_text('.') != -1:
        clean_nb = nb_text.replace(',', '').replace('.', '')
    else:
        clean_nb = nb_text
    return int(clean_nb)
