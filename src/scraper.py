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

def parse_book_card(article) -> dict:
    """
    Extract the fields we care about from one <article class="product_pod"> tag.
    """
    title = article.h3.a["title"]
    detail_url = BASE_URL + "catalogue/" + article.h3.a["href"].replace("../../../", "").replace("../../", "").replace("../", "")

    price_text = article.find("p", class_="price_color").get_text(strip=True)

    availability_text = article.find("p", class_="instock availability").get_text(strip=True)

    # star-rating class looks like: "star-rating Three" -> we want "Three"
    rating_classes = article.find("p", class_="star-rating")["class"]
    star_rating_word = rating_classes[1] if len(rating_classes) > 1 else None

    return {
        "title": title,
        "price_raw": price_text,
        "availability_raw": availability_text,
        "star_rating_word": star_rating_word,
        "detail_url": detail_url,
    }