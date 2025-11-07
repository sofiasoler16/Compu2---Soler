
# ==============================
# File: scraper/metadata_extractor.py
# ==============================
from bs4 import BeautifulSoup


def extract_meta_tags(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    out = {"description": None, "keywords": None}

    # Meta description & keywords
    desc = soup.find("meta", attrs={"name": "description"})
    if desc and desc.get("content"):
        out["description"] = desc.get("content").strip()

    keys = soup.find("meta", attrs={"name": "keywords"})
    if keys and keys.get("content"):
        out["keywords"] = keys.get("content").strip()

    # Open Graph
    og = {}
    for tag in soup.find_all("meta"):
        prop = tag.get("property") or tag.get("name")
        if prop and prop.startswith("og:") and tag.get("content"):
            og[prop] = tag.get("content").strip()
    if og:
        out.update(og)

    return out

