import requests

class checkHealth:
    def checkHealthMethod(self,ip):
        res = requests.get('http://' + ip + ':5000/')
        print(res.status_code)
        if res.status_code == 200:
            # print("true")
            return True
        else:
            # print("false")
            return False

# ip = '192.168.3.15'
# c = checkHealth()
# c.checkHealthMethod(ip)
