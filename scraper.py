import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_page(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    articles = soup.select("article.product_pod")

    for article in articles:
        title = article.select_one("h3 a")["title"]
        
        # Strip the weird encoding symbol
        price = article.select_one("p.price_color").text.replace("Â", "").strip()
        
        # Get second class name for rating
        rating_word = article.select_one("p.star-rating")["class"][1]
        rating = RATING_MAP.get(rating_word, 0)
        
        availability = article.select_one("p.availability").text.strip()

        books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
        })

    # Find next page link
    next_btn = soup.select_one("li.next a")
    next_url = BASE_URL + next_btn["href"] if next_btn else None

    return books, next_url

def scrape_books(max_pages=5):
    all_books = []
    url = START_URL
    page = 1

    while url and page <= max_pages:
        print(f"📄 Scraping page {page}...")
        books, url = scrape_page(url)
        all_books.extend(books)
        page += 1

    return all_books