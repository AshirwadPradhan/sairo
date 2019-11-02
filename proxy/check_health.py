import requests

class CheckHealth:

    @staticmethod
    def check(ip: str) -> bool:

        res = requests.get('http://' + ip + ':5000/')
        print(res.status_code)
        if res.status_code == 200:
            print(f'{ip} Health: OK...')
            return True
        else:
            print(f'{ip} Health: NOT OK...')
            return False
