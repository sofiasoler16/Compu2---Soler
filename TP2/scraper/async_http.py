
# ==============================
# File: scraper/async_http.py
# ==============================
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Tuple
from urllib.parse import urlparse, urljoin

import aiohttp

class AsyncHTTPClient:
    def __init__(self, max_per_domain: int = 4, user_agent: str | None = None):
        self._session: aiohttp.ClientSession | None = None
        self._domain_semaphores: Dict[str, asyncio.Semaphore] = {}
        self._max_per_domain = max(1, int(max_per_domain))
        self._user_agent = user_agent or (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"
        )

    async def start(self):
        timeout = aiohttp.ClientTimeout(total=None, sock_connect=15, sock_read=25)
        self._session = aiohttp.ClientSession(timeout=timeout, headers={
            "User-Agent": self._user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })

    async def close(self):
        if self._session:
            await self._session.close()
            self._session = None

    def _sem_for_domain(self, url: str) -> asyncio.Semaphore:
        netloc = urlparse(url).netloc
        if netloc not in self._domain_semaphores:
            self._domain_semaphores[netloc] = asyncio.Semaphore(self._max_per_domain)
        return self._domain_semaphores[netloc]

    @asynccontextmanager
    async def _guard_domain(self, url: str):
        sem = self._sem_for_domain(url)
        await sem.acquire()
        try:
            yield
        finally:
            sem.release()

    async def fetch_html(self, url: str, *, timeout: float = 30.0) -> Tuple[str, str]:
        """Devuelve (html_text, final_url). Sigue redirects. Respeta límite por dominio."""
        if not self._session:
            raise RuntimeError("AsyncHTTPClient no inicializado. Llama a start().")
        async with self._guard_domain(url):
            async with self._session.get(url, allow_redirects=True, timeout=timeout) as resp:
                resp.raise_for_status()
                text = await resp.text(errors="ignore")
                return text, str(resp.url)

