
# ==============================
# File: processor/performance.py
# ==============================
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests


def measure_performance(url: str, max_resources: int = 40, per_request_timeout: int = 6) -> dict:
    """Medición ligera: descarga HTML y un subconjunto de recursos (img, css, js) con HEAD/GET.
    Calcula tiempo total, tamaño total aproximado y cantidad de requests.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"
        )
    }

    t0 = time.perf_counter()
    total_bytes = 0
    num_requests = 0

    # HTML principal
    r = requests.get(url, headers=headers, timeout=per_request_timeout)
    r.raise_for_status()
    html = r.text
    total_bytes += len(r.content)
    num_requests += 1

    soup = BeautifulSoup(html, "lxml")

    # Recursos: primeras N de img/src, link rel=stylesheet, script src
    candidates = []
    for img in soup.find_all("img", src=True):
        candidates.append(urljoin(r.url, img["src"]))
    for ln in soup.find_all("link", rel=lambda v: v and "stylesheet" in v):
        if ln.get("href"):
            candidates.append(urljoin(r.url, ln["href"]))
    for sc in soup.find_all("script", src=True):
        candidates.append(urljoin(r.url, sc["src"]))

    # Limitar
    candidates = candidates[:max_resources]

    for res_url in candidates:
        try:
            # Intentar HEAD; si no da tamaño, usamos GET con stream corto
            h = requests.head(res_url, headers=headers, timeout=per_request_timeout, allow_redirects=True)
            size = int(h.headers.get("Content-Length", 0)) if h.ok else 0
            if size == 0:
                g = requests.get(res_url, headers=headers, timeout=per_request_timeout)
                if g.ok:
                    size = len(g.content)
            total_bytes += size
            num_requests += 1
        except Exception:
            continue

    elapsed_ms = int((time.perf_counter() - t0) * 1000)
    total_kb = int(total_bytes / 1024)

    return {
        "load_time_ms": elapsed_ms,
        "total_size_kb": total_kb,
        "num_requests": num_requests,
    }

