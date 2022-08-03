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


def check_if_actual_level_is_lower_than_target(list_1: list, list_2: list) -> list:
    """
    Verify if the level of the building / field is lower than the target level.
    :param list_1: actual_building
    :param list_2: build_queue
    :return: list of upgrades to remove from to do list
    """
    result = []
    for obj in list_1:
        for to_obj in list_2:
            if obj[1] == to_obj[1] and (obj[2] > to_obj[2] or obj[2] == to_obj[2]):
                result.append(to_obj)
                break
    return result


if __name__ == '__main__':
    list1 = [[1, 2, 4], [2, 5, 10]]
    list2 = [[1, 2, 4], [4, 5, 8]]
    print(min(list1, key=lambda x: x[2])[2])
    # check_if_actual_level_is_lower_than_target(list_1=list1, list_2=list2)
