import configparser
import os
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
config_path = os.path.join(BASE_DIR, "config.ini")
build_queue_path = os.path.join(BASE_DIR, "assets/build_queue.json")
buildings_path = os.path.join(BASE_DIR, "assets/buildings.json")
fields_path = os.path.join(BASE_DIR, "assets/fields.json")

config = configparser.ConfigParser()
config.read(config_path)

SERVER_URL = config['USER']['server_url']
USERNAME = config['USER']['email']
PASSWORD = config['USER']['password']
PROXY = {'http': config['USER']['https_proxy'],
         'https': config['USER']['https_proxy']}

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}

HEADERS_LOGIN = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Version': '1644.8',
    'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': 'Bearer undefined',
    'Origin': 'https://ts8.x1.europe.travian.com'
}

HEADERS_API = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Version': '1644.8',
    'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': 'Bearer undefined',
    'Referer': 'https://ts8.x1.europe.travian.com/hero/adventures',
    'Origin': 'https://ts8.x1.europe.travian.com'
}

VILLAGE_URL = SERVER_URL + 'dorf1.php'
TOWN_URL = SERVER_URL + 'dorf2.php'
HERO_URL = SERVER_URL + 'hero.php?t=3'
ADVENTURE_URL = SERVER_URL + 'hero/adventures'
LOGIN_URL = SERVER_URL + 'api/v1/auth/login'
