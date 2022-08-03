import copy
import json

import login
from scrapping.dorf1 import get_construction_cost, get_actual_resources, scan_fields, scan_buildings, \
    pick_random_lowest_field, pick_random_crop_field, get_checksum, current_construction, gold_club_active, \
    field_under_construction, building_under_construction
from settings import VILLAGE_URL, SERVER_URL, TOWN_URL, build_queue_path
from utils import log, check_if_actual_level_is_lower_than_target


class Building:

    def __init__(self) -> None:
        self.session = login.Login()
        self.actual_resources = {}
        self.build_queue = []

    def field_upgrade(self, v_id: int, slot: int, gid: int) -> None:
        html = self.session.get_html(SERVER_URL + f'build.php?newdid={v_id}?id={slot}&gid={gid}')
        checksum = get_checksum(html)

        payload = {
            "id": slot,
            "gid": gid,
            "action": 'build',
            "checksum": checksum
        }

        try:
            upgrade_html = (VILLAGE_URL + f'?id={slot}&gid={gid}&action=build&checksum={checksum}')
            self.session.request(method='get', url=upgrade_html, data=payload)
            log(f"Upgrading resource field")
        except:
            print("Upgrade did not work")

    def building_update(self, v_id: int, slot: int, gid: int) -> None:
        html = self.session.get_html(SERVER_URL + f'build.php?newdid={v_id}?id={slot}&gid={gid}')
        checksum = get_checksum(html)

        payload = {
            "id": slot,
            "gid": gid,
            "action": 'build',
            "checksum": checksum
        }

        try:
            upgrade_html = (TOWN_URL + f'?id={slot}&gid={gid}&action=build&checksum={checksum}')
            self.session.request(method='get', url=upgrade_html, data=payload)
            log(f"Upgrading building")
        except:
            print("Upgrade did not work")

    def populate_build_queue(self) -> list:
        """
        Read the build_queue file and returns the list of buildings to build up to which level.
        :return:list
        """
        with open(build_queue_path) as f:
            for line in f:
                building_details = line.split(',')
                building = building_details[0].rstrip('\n'), building_details[1].rstrip('\n')
                self.build_queue.append(building)
        return self.build_queue

    def test2(self):
        html = self.session.get_html(TOWN_URL)
        print(scan_buildings(html))

    def upgrade_from_file(self, v_id: int, file_name: str = None) -> None:
        fields_to_upgrade = []
        buildings_to_upgrade = []
        actual_fields = []
        actual_buildings = []
        with open(build_queue_path, 'r') as f:
            build_queue = json.load(f)
        fields_to_upgrade = copy.deepcopy(build_queue['fieldlist'])
        buildings_to_upgrade = copy.deepcopy(build_queue['townlist'])
        while True:
            if fields_to_upgrade == [] and buildings_to_upgrade == []:
                log(f'Both fieldlist and townlist from {build_queue_path} are empty')
                break

            html = self.session.get_html(VILLAGE_URL)
            actual_fields = scan_fields(url=html)
            fields_to_remove = check_if_actual_level_is_lower_than_target(list_1=actual_fields, list_2=fields_to_upgrade)
            if fields_to_remove:
                fields_to_upgrade.remove(fields_to_remove)
            html = self.session.get_html(TOWN_URL)
            actual_buildings = scan_buildings(url=html)
            buildings_to_remove = check_if_actual_level_is_lower_than_target(list_1=actual_buildings, list_2=buildings_to_upgrade)
            if buildings_to_remove:
                buildings_to_upgrade.remove(buildings_to_remove)

            if field_under_construction(html) and building_under_construction(html):
                construction_list = current_construction(html)
                sleeptime = min(construction_list, key=lambda x: x[2])[2]

            if not field_under_construction(html) and building_under_construction(html):
                pass

            if not building_under_construction(html) and field_under_construction(html):
                pass


if __name__ == '__main__':
    test = Building()
    # test.field_upgrade(v_id=21606, slot=6, gid=2)
    # test.building_update(v_id=21606, slot=23, gid=23)
