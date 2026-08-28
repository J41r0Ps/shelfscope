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
    detail_url = BASE_URL + "catalogue/" + article.h3.a["href"].replace("../../../", "").replace("../../", "").replace("../", "")   # This is a bit hacky, but it works for this site. The href is relative and has varying numbers of "../" at the start.

    price_text = article.find("p", class_="price_color").get_text(strip=True)
                 
    availability_text = article.find("p", class_="instock availability").get_text(strip=True)

    # star-rating class looks like: "star-rating Three" -> we want "Three"
    rating_classes = article.find("p", class_="star-rating")["class"]   # Here return a list like ['star-rating', 'Three']
    star_rating_word = rating_classes[1] if len(rating_classes) > 1 else None

    return {
        "title": title,
        "price_raw": price_text,
        "availability_raw": availability_text,
        "star_rating_word": star_rating_word,
        "detail_url": detail_url,
    }

def scrape_all_books(max_pages: int | None = None, delay: float = 0.5) -> list[dict]:
    """
    Walk every catalogue page starting from the homepage, following the "next" link,
    and collect parsed book dicts from every page.

    max_pages: optional cap, useful for quick testing (e.g. max_pages=2).
    delay: seconds to wait between page requests (politeness).
    """
    all_books = []
    page_url = BASE_URL
    page_count = 0

    while page_url:
        soup = get_soup(page_url, delay=delay)
        articles = soup.find_all("article", class_="product_pod")

        for article in articles:
            all_books.append(parse_book_card(article))

        page_count += 1
        print(f"Scraped page {page_count} — {len(articles)} books (total so far: {len(all_books)})")

        if max_pages is not None and page_count >= max_pages:
            break

        # find the "next" link, if any
        next_link = soup.find("li", class_="next")
        if next_link:
            next_href = next_link.a["href"]
            if page_url == BASE_URL:
                # from homepage, href is already "catalogue/page-2.html"
                page_url = BASE_URL + next_href
            else:
                # from inside /catalogue/, href is just "page-3.html"
                page_url = BASE_URL + "catalogue/" + next_href
        else:
            page_url = None

    return all_books