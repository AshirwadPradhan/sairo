import requests
from requests.exceptions import Timeout

class CheckHealth:

    @staticmethod
    def check(ip: str) -> bool:

        try:
            res = requests.get('http://' + ip + '/', timeout=0.5)
            if res.status_code == 200:
                print(res.status_code)
                print(f'{ip} Health: OK...')
                return True
            else:
                print(f'{ip} Health: NOT OK...')
                return False
        except Timeout as e:
            print(f'{ip} Health: NOT OK...')
            return False
