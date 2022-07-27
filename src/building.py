import login
from scrapping.dorf1 import get_construction_cost, get_actual_resources, scan_fields, scan_buildings, \
    pick_random_lowest_field, pick_random_crop_field, get_checksum, current_construction
from settings import VILLAGE_URL, SERVER_URL, TOWN_URL
from utils import log


class Building:

    def __init__(self) -> None:
        self.session = login.Login()
        self.actual_resources = {}

    def field_upgrade(self, v_id, slot, gid):
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
            response = self.session.request(method='get', url=upgrade_html, data=payload)
            log(f"Upgrading resource field")
            print(response.status_code)
        except:
            print("Upgrade did not work")

    def building_update(self, v_id, slot, gid):
        html = self.session.get_html(SERVER_URL + f'build.php?newdid={v_id}?id={slot}&gid={gid}')

    def test(self):
        html = self.session.get_html(VILLAGE_URL)
        current_construction(html)


if __name__ == '__main__':
    test = Building()
    # test.building_update(v_id=21606, slot=26, gid=15)
