import requests
from configparser import ConfigParser
from requests.auth import HTTPBasicAuth


class Bert:
    def __init__(self, text, ratio=0.2):
        self.text = text
        self.ratio = ratio
        self.config = ConfigParser()
        self.config.read('config.ini')

    def get_summary(self):
        url = self.config.get('bert', 'url')
        api_key = self.config.get('bert', 'api_key')
        auth = HTTPBasicAuth('API_KEY', api_key)
        summary = requests.post(url=url, params={'ratio': self.ratio}, auth=auth, data=self.text.encode("utf-8"))
        summary = summary.json()['summary']
        return summary


