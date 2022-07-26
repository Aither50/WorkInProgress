import json
import requests
import time

from settings import USERNAME, PASSWORD, SERVER_URL, VILLAGE_URL, LOGIN_URL, HEADERS_LOGIN, HEADERS, HEADERS_API
from utils import log, sleep_random

REQUEST_MAX_TRIES = 2


class Login:
    """Class to handle connection and interaction with the server"""

    def __init__(self) -> None:
        self.session = self.new_session()
        self.server = SERVER_URL
        self.login_url = LOGIN_URL
        self.logged_in = False

        self.timeout = 5.0
        self.relogin_delay = 0.33
        self.reconnections = 1
        self.html_obsolescence_time = 1.0
        self.html_sources = dict()

        self.game_version = None

    @staticmethod
    def get_session() -> object:
        print('Creation of a session')
        return requests.session()

    def new_session(self) -> object:
        if getattr(self, 'session', None):
            self.session.close()
        self.session = self.get_session()
        self.session.headers = HEADERS
        return self.session

    def request(self, method: str, url: str, data=None, params=None) -> requests.Response:

        if params is None:
            params = {}
        if data is None:
            data = {}
        response = None

        try:
            log(f'Send {method.upper()} request to url: {url}')
            if method == 'get':
                sleep_random()
                response = self.session.get(url, params=params, headers=HEADERS)
            elif method == 'post':
                sleep_random()
                response = self.session.post(url, params=params, data=data, headers=HEADERS)
        except:
            log(f'Net problem, cant fetch the URL {url}')

        if not response:
            raise ValueError('response must be not None')

        return response

    def get(self, url: str, data=None, params=None) -> requests.Response:
        """ Sends a GET request to the server """
        if data is None:
            data = {}
        if params is None:
            params = {}
        return self.request('get', url, data, params)

    def post(self, url: str, data=None, params=None) -> requests.Response:
        """ Sends a POST request to the server """
        if data is None:
            data = {}
        if params is None:
            params = {}
        return self.request('post', url, data, params)

    def send_request(self, url: str, data=None, params=None) -> requests.Response:
        """Send a GET request if no data, otherwise send a POST request"""
        if data is None:
            data = {}
        if params is None:
            params = {}
        if not len(data):
            response = self.get(url, data=data, params=params)
        else:
            response = self.post(url, data=data, params=params)
        return response

    def login(self, url: str = VILLAGE_URL, email: str = USERNAME, password: str = PASSWORD) -> bool:

        log(f"Start Login to server {url}")

        payload = {
            "mobileOptimizations": False,
            "name": email,
            "password": password,
            "w": "1920:1080",
        }

        # Sending the first request (POST) to retrieve the JSON token

        log(f"Sending POST login request on {LOGIN_URL}")
        response = self.session.post(url=LOGIN_URL, headers=HEADERS_LOGIN, data=json.dumps(payload))

        if response.status_code != 200:
            log('Login failed')
            return False

        token = str(response.json()['nonce'])

        # Sending the second request (POST) to authenticate on the server

        url = SERVER_URL + 'api/v1/auth/' + token
        response = self.session.post(url)

        if response.status_code != 200:
            log('Login failed')
            return False

        # Sending the thrid request (GET) to load village page and make sure the connection went through
        log(f"Sending GET request on {VILLAGE_URL}")
        html = self.session.get(VILLAGE_URL, headers=HEADERS).text

        if 'playerName' in html:
            self.logged_in = True
            log(f'Login success')
            return True
        else:
            self.logged_in = False
            log(f'Login failed')

    def __call__(self):
        if not self.login():
            print("Can\'t login. Something is wrong.")

    def load_html(self, url: str, params=None, data=None) -> str:
        if params is None:
            params = {}
        if data is None:
            data = {}
        if not self.logged_in:
            if not self.login():
                log('Can\'t login. Something is wrong.')
                print("Can\'t login. Something is wrong.")
        html = self.send_request(url, data=data, params=params).text
        if 'playerName' not in html:
            self.logged_in = False
            log('Suddenly logged off')
            for i in range(self.reconnections):
                if self.login():
                    html = self.send_request(url, data=data, params=params).text
                    return html
                else:
                    log('Could not relogin %d time' % (self.reconnections - i))
                    time.sleep(self.relogin_delay)
        return html

    def get_html(self, url: str, params=None, data=None) -> str:

        """Load the page"""

        if params is None:
            params = {}
        if data is None:
            data = {}
        key = (url, hash(tuple(sorted(params.items()))))

        if key in self.html_sources:
            html, load_time = self.html_sources[key]
            if time.time() - load_time < self.html_obsolescence_time:
                log(f"{url} : no obsolescence html")
                return html

        load_time = time.time()
        html = self.load_html(url, params=params, data=data)
        self.html_sources[key] = (html, load_time)

        return html

    ####################################################################################################################

    def request_api(self, method: str, url: str, data=None, params=None) -> requests.Response:

        if params is None:
            params = {}
        if data is None:
            data = {}
        response = None

        print("url = " + url)

        try:
            log(f'Send {method.upper()} API request to url: {url}')
            if method == 'get':
                sleep_random()
                response = self.session.get(url, params=params, headers=HEADERS_API)
            elif method == 'post':
                sleep_random()
                response = self.session.post(url, params=params, data=json.dumps(data), headers=HEADERS_API)
        except:
            log(f'Net problem, cant fetch the URL {url}')

        if not response:
            raise ValueError('response must be not None')

        return response

    def get_api(self, url: str, data=None, params=None) -> requests.Response:
        """ Sends a GET request to the server """
        if data is None:
            data = {}
        if params is None:
            params = {}
        return self.request_api('get', url, data, params)

    def post_api(self, url: str, data=None, params=None) -> requests.Response:
        """ Sends a POST request to the server """
        if data is None:
            data = {}
        if params is None:
            params = {}

        return self.request_api('post', url, data, params)

    def send_request_api(self, url: str, data=None, params=None) -> requests.Response:
        """Send a GET request if no data, otherwise send a POST request"""
        if data is None:
            data = {}
        if params is None:
            params = {}
        if not len(data):
            # Force POST request
            response = self.post_api(url, data=data, params=params)
        else:
            response = self.post_api(url, data=data, params=params)
        return response

    def load_api(self, url: str, params=None, data=None) -> str:
        if params is None:
            params = {}
        if data is None:
            data = {}
        if not self.logged_in:
            if not self.login():
                log('Can\'t login. Something is wrong.')
                print("Can\'t login. Something is wrong.")
        html = self.send_request_api(url, data=data, params=params).text
        if 'playerName' not in html:
            self.logged_in = False
            log('Suddenly logged off')
            for i in range(self.reconnections):
                if self.login():
                    html = self.send_request_api(url, data=data, params=params).text
                    return html
                else:
                    log('Could not relogin %d time' % (self.reconnections - i))
                    time.sleep(self.relogin_delay)
        return html

    def get_api(self, url: str, params=None, data=None) -> str:

        """Load the page"""

        if params is None:
            params = {}
        if data is None:
            data = {}
        key = (url, hash(tuple(sorted(params.items()))))

        if key in self.html_sources:
            html, load_time = self.html_sources[key]
            if time.time() - load_time < self.html_obsolescence_time:
                log(f"{url} : no obsolescence html")
                return html

        load_time = time.time()
        html = self.load_api(url, params=params, data=data)
        self.html_sources[key] = (html, load_time)

        return html


if __name__ == '__main__':
    test = Login()
    test.login()
