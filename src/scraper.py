import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"


def get_soup(url: str, delay: float = 0.5) -> BeautifulSoup:
    """
    Fetch a URL and return a parsed BeautifulSoup object.
    A small delay is applied before each request to be polite to the server.
    """
    time.sleep(delay)
    response = requests.get(url)
    response.raise_for_status()  # raises an error if the request failed (e.g. 404, 500)
    return BeautifulSoup(response.content, "lxml")