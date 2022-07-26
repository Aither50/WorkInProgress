import login
from scrapping.hero import get_adventure_balance, check_hero_availability, check_hero_health, get_adventure_id
from settings import VILLAGE_URL, SERVER_URL, ADVENTURE_URL


class Adventure:
    """Class to send the hero on adventure"""

    def __init__(self) -> None:
        self.session = login.Login()

    def start_adventure(self, health: int = 30) -> None:
        html = self.session.get_html(VILLAGE_URL)
        if check_hero_health(html, health) and check_hero_availability(html) and get_adventure_balance(html) > 0:
            self.send_hero_on_first_adventure()

    def send_hero_on_first_adventure(self):
        html = self.session.get_html(ADVENTURE_URL)
        get_adventure_id(html)


if __name__ == '__main__':
    test = Adventure()
    test.send_hero_on_first_adventure()
