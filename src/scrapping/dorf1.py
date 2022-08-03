import json
import random
import re
from pprint import pprint

from bs4 import BeautifulSoup

from settings import buildings_path, fields_path


def get_construction_cost(url: str) -> dict:
    dorf_parser = BeautifulSoup(url, 'html.parser')
    lumber_cost = dorf_parser.find_all('span', {'class': 'value value'})[0].text
    clay_cost = dorf_parser.find_all('span', {'class': 'value value'})[1].text
    iron_cost = dorf_parser.find_all('span', {'class': 'value value'})[2].text
    crop_cost = dorf_parser.find_all('span', {'class': 'value value'})[3].text
    free_crop_cost = dorf_parser.find_all('span', {'class': 'value value'})[4].text
    construction_cost = {'lumber': int(lumber_cost),
                         'clay': int(clay_cost),
                         'iron': int(iron_cost),
                         'crop': int(crop_cost),
                         'freeCrop': int(free_crop_cost),
                         }
    return construction_cost


def get_actual_resources(url: str) -> dict:
    dorf_parser = BeautifulSoup(url, 'html.parser')
    lumber = dorf_parser.find('div', {'id': 'l1'}).text.replace('\u202d', '').replace('\u202c', '')
    clay = dorf_parser.find('div', {'id': 'l2'}).text.replace('\u202d', '').replace('\u202c', '')
    iron = dorf_parser.find('div', {'id': 'l3'}).text.replace('\u202d', '').replace('\u202c', '')
    crop = dorf_parser.find('div', {'id': 'l4'}).text.replace('\u202d', '').replace('\u202c', '')
    free_crop = dorf_parser.find('div', {'id': 'stockBarFreeCrop'}).text.replace('\u202d', '').replace('\u202c', '')
    resources = {'lumber': int(lumber),
                 'clay': int(clay),
                 'iron': int(iron),
                 'crop': int(crop),
                 'freeCrop': free_crop,
                 }
    return resources


def scan_fields(url: str) -> list:
    """
    Creates list of lists of resource fields and returns it. Each element in tile list is an int.
    \n gid = Field type
    (1: Wood ; 2: Clay ; 3: Iron ; 4: Crop)
    \n buildingSlot = field position on the grid
    \n level = Field level

    :param url: dorf1
    :return: [[gid#, buildingSlot#, level#]]
    """

    dorf_parser = BeautifulSoup(url, 'html.parser')
    fields = []
    for i in range(1, 19):
        field = dorf_parser.find('a', {'class': 'buildingSlot' + str(i)})['class']
        del field[0:3]
        field = [s.replace('buildingSlot', '') for s in field]
        field = [s.replace('level', '') for s in field]
        field = [s.replace('gid', '') for s in field]
        field = [int(item) for item in field]
        fields.append(field)
    with open(fields_path, 'w') as f:
        json.dump(fields_path, f, indent=4)
    return fields


def scan_buildings(url: str) -> list:
    """
    Creates list of lists of buildings and returns it. Each element in tile list is an int.
    \n aid = Building position on the grid
    \n gid = Building type
    \n level = Building level
    \n name = Building name

    :param url: dorf2
    :return: [[aid#, gid#, level#, name]]
    """

    dorf_parser = BeautifulSoup(url, 'html.parser')
    buildings = []
    aid = dorf_parser.find('div', {'data-aid': '19'})['data-aid']
    pprint(aid)
    for i in range(19, 41):
        building = []
        aid = dorf_parser.find('div', {'data-aid': str(i)})['data-aid']
        gid = dorf_parser.find('div', {'data-aid': str(i)})['data-gid']
        if gid != '0':
            level = dorf_parser.find('div', {'data-aid': str(i)}).find('a')['data-level']
            name = dorf_parser.find('div', {'data-aid': str(i)})['data-name']
        else:
            level = '0'
            name = ''
        building.append(int(aid))
        building.append(int(gid))
        building.append(int(level))
        building.append(name)
        buildings.append(building)
    with open(buildings_path, 'w') as f:
        json.dump(buildings, f, indent=4)
    return buildings


def pick_random_lowest_field(url: str) -> tuple:
    """
    Pick randomly the lowest field and returns the gid and buildingSlot.

    :param url: dorf1
    :return: (gid#, buildingSlot#)
    """
    fields = scan_fields(url)
    lowest_level = min(fields, key=lambda x: x[2])[2]
    lowest_fields = filter(lambda l: l[2] == lowest_level, fields)
    lowest_fields_list = list(lowest_fields)
    random_lowest_field = random.choice(lowest_fields_list)
    return random_lowest_field[0], random_lowest_field[1]


def pick_random_crop_field(url: str) -> tuple:
    """
    Pick randomly the lowest crop field and returns the gid and buildingSlot.

    :param url: VILLAGE_URL
    :return: (gid#, buildingSlot#)
    """
    fields = scan_fields(url)
    crop_fields = list(filter(lambda l: l[0] == 4, fields))
    lowest_level = min(crop_fields, key=lambda x: x[2])[2]
    lowest_crop_fields = filter(lambda l: l[2] == lowest_level, crop_fields)
    lowest_crop_fields_list = list(lowest_crop_fields)
    random_lowest_field = random.choice(lowest_crop_fields_list)
    return random_lowest_field[0], random_lowest_field[1]


def get_checksum(url: str) -> str:
    """
    Return the checksum of a field to upgrade it.

    :param url: field page
    :return: checksum
    """
    field_parser = BeautifulSoup(url, 'html.parser')
    upgrade_btn = field_parser.find('div', {'class': 'section1'}).find('button')['onclick']
    checksum = re.search("checksum=(.*)'", upgrade_btn).group(1)
    return checksum


def current_construction(url: str) -> list:
    """
    Creates a list of tuples specifying what is currently being constructed in village.
    :param url: dorf
    :return:[(Name of construction, level#, seconds remaining), ...]
    """
    dorf_parser = BeautifulSoup(url, 'html.parser')
    under_construction = []
    try:
        building_list = dorf_parser.find('div', {'class': 'buildingList'}).find_all('li')
        for building in building_list:
            div_name = building.find('div', {'class': 'name'})
            name = div_name.contents[0].strip()
            span_level = building.find('span', {'class': 'lvl'})
            level = int(re.findall(r' (\d+)', span_level.text)[0])
            time = building.find('span', {'class': 'timer'})['value']
            under_construction.append((name, level, time))
        return under_construction
    except:
        return under_construction


def field_under_construction(url: str) -> bool:
    """
    Check if a field is in being built. If yes returns True, if not False.
    :param url: dorf
    :return: True or False
    """
    resource_labels = ('Clay P', 'Woodcu', 'Iron M', 'Cropland')
    under_construction = current_construction(url)

    if len(under_construction) == 0:
        return False
    for construction in under_construction:
        for r in resource_labels:
            if construction[0] == r:
                return True
    return False


def building_under_construction(url: str) -> bool:
    """
    Check if a building is in being built. If yes returns True, if not False.
    :param url: dorf
    :return: True or False
    """
    resource_labels = ('Clay P', 'Woodcu', 'Iron M', 'Cropland')
    under_construction = current_construction(url)

    if len(under_construction) == 0:
        return False
    if len(under_construction) == 2:
        return True
    for construction in under_construction:
        for r in resource_labels:
            if construction[0] == r:
                return False
    return True


def plus_acount_active(url: str) -> bool:
    """
    Check is Travian plus is activated on the account.
    :param url: dorf
    :return: True or False
    """
    dorf_parser = BeautifulSoup(url, 'html.parser')
    link_list = dorf_parser.find('div', {'id': 'sidebarBoxLinklist'})
    link_list_btn = link_list.find('div', {'class': 'buttonsWrapper'}).find('a')['class']
    if 'gold' in link_list_btn:
        return False
    return True


def gold_club_active(url: str) -> bool:
    """
    Check is Gold Club is activated on the account.
    :param url: Rally Point page
    :return: True or False
    """
    rally_point_parser = BeautifulSoup(url, 'html.parser')
    header = rally_point_parser.find('div', {'class': 'scrollingContainer'})
    farm_list_btn = header.find('div', {'class': 'favorKey99'}).find('a')['title']
    if 'For this feature you need the Gold club activated' in farm_list_btn:
        return False
    return True
