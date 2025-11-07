
# ==============================
# File: processor/image_processor.py
# ==============================
from io import BytesIO
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from PIL import Image


def build_thumbnails(url: str, limit: int = 3, max_image_bytes: int = 3_000_000, thumb_px: int = 256) -> List[str]:
    """Descarga hasta `limit` imágenes de la página y devuelve thumbnails en base64 PNG."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    imgs = []
    for img in soup.find_all("img", src=True):
        full = urljoin(resp.url, img["src"])
        imgs.append(full)
    imgs = imgs[:limit]

    out_b64 = []
    from common.serialization import b64_png

    for u in imgs:
        try:
            r = requests.get(u, headers=headers, timeout=10)
            if not r.ok:
                continue
            if len(r.content) > max_image_bytes:
                continue
            im = Image.open(BytesIO(r.content))
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGB")
            im.thumbnail((thumb_px, thumb_px))
            buf = BytesIO()
            im.save(buf, format="PNG")
            out_b64.append(b64_png(buf.getvalue()))
        except Exception:
            continue

    return out_b64

