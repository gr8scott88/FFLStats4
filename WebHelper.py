from bs4 import BeautifulSoup
import requests

def build_url(root, *paths):
    url = root
    for path in paths:
        if url.endswith('/'):
            url = url + str(path)
        else:
            url = url + r'/' + str(path)
    return url


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup