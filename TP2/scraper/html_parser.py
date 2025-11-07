
# ==============================
# File: scraper/html_parser.py
# ==============================
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_basic_structure(html: str, base_url: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    # Título
    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    # Links absolutos
    links = []
    for a in soup.find_all("a", href=True):
        try:
            links.append(urljoin(base_url, a.get("href")))
        except Exception:
            continue

    # Headers H1..H6
    structure = {}
    for level in range(1, 7):
        structure[f"h{level}"] = len(soup.find_all(f"h{level}"))

    # Imágenes
    images_count = len(soup.find_all("img"))

    return {
        "title": title,
        "links": links,
        "structure": structure,
        "images_count": images_count,
    }

