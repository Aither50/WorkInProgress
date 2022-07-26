import re
from pprint import pprint

from bs4 import BeautifulSoup

from utils import parse_time_to_seconds


def get_adventure_balance(url: str) -> int:
    dorf_parser = BeautifulSoup(url, 'html.parser')
    hero_portrait_adv_btn = dorf_parser.find('a', {'href': '/hero/adventures'})
    adventure_balance = int(hero_portrait_adv_btn.find('div', {'class': 'content'}).text)
    if not adventure_balance:
        return 0
    return adventure_balance


def get_adventure_id(url: str) -> str:
    dorf_parser = BeautifulSoup(url, 'html.parser')
    adventure_list = dorf_parser.find(string='"adventures":[{"mapId":')
    pprint(dorf_parser)


def check_hero_health(url: str, health: int) -> bool:
    dorf_parser = BeautifulSoup(url, 'html.parser')
    hero_portrait_health_btn = dorf_parser.find('svg', {'class': 'health'})
    hero_health = hero_portrait_health_btn.find('title').text.replace("%", "")
    hero_health = int(re.findall(r'(\d+)', hero_health)[0])
    return hero_health > health


def check_hero_availability(url: str) -> bool:
    dorf_parser = BeautifulSoup(url, 'html.parser')
    hero_portrait_status_btn = dorf_parser.find('div', {'class': 'heroStatus'})
    hero_status = hero_portrait_status_btn.find('i')['class'][0]
    if hero_status != 'heroHome':
        return False
    return True


def check_adventure_time(url: str) -> int:
    dorf_parser = BeautifulSoup(url, 'html.parser')
    sentence = dorf_parser.find('a', {'class': 'heroImageButton'})['title']
    time = re.search('Arrival in (.+?) at', sentence).group(1)
    return parse_time_to_seconds(time) + 10
