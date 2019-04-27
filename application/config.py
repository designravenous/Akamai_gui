from akamai.edgegrid import EdgeGridAuth
import requests

class Akamai_credentials:
    def __init__(self, datetime):
        self.datetime = datetime
    def Akamai_report(self):
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token='xxxxxxxxxxxxxxxxxxx',
            client_secret='xxxxxxxxxxxxxxxxxxx',
            access_token='xxxxxxxxxxxxxxxxxxx'
        )
        baseurl = 'https://xxxxxxxxxxxxxxxxxxx.luna.akamaiapis.net/'
        credentials_list = [s, baseurl]
        return credentials_list
    def Akamai_zone_read(self):
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token='xxxxxxxxxxxxxxxxxxx',
            client_secret='xxxxxxxxxxxxxxxxxxx',
            access_token='xxxxxxxxxxxxxxxxxxx'
        )
        baseurl = 'https://xxxxxxxxxxxxxxxxxxx.luna.akamaiapis.net/'
        credentials_list = [s, baseurl]
        return credentials_list
