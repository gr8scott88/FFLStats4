import requests
from bs4 import BeautifulSoup


class Webpage:
    def __init__(self, url):
        page = requests.get(url)
        self.soup = BeautifulSoup(page.content, 'html.parser')

    def save(self):
        pass


