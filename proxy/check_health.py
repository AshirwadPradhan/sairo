import requests

class checkHealth:
    def checkHealthMethod(self,ip):
        res = requests.get(ip)
        print(res.status_code)
        if res.status_code == 200:
            print("true")
            return True
        else:
            print("false")
            return False

# ip = 'http://192.168.3.15:5000/'
# c = checkHealth()
# c.checkHealthMethod(ip)
