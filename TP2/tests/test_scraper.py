import asyncio
import types
import uuid
import pytest
from types import SimpleNamespace
from aiohttp import web
from aiohttp.test_utils import TestServer, TestClient
import server_scraping

pytestmark = pytest.mark.asyncio

# ---------- Helpers ----------
async def _start_app():
    # Armamos args como los espera app_factory
    args = SimpleNamespace(
        ip="127.0.0.1",
        port=0,  #TestServer elige puerto
        workers=2,
        proc_host="127.0.0.1",
        proc_port=9000,
        proc_timeout=45.0,    
        request_timeout=45.0, 
        processor=None,
    )
    app = await server_scraping.app_factory(args)
    return app

# ---------- Tests ----------

async def test_scrape_success_with_processing(monkeypatch):
    """
    /scrape con B respondiendo OK → status: success y processing_data completo.
    """
    # Mock del request_processing_b para no depender del server B real
    async def fake_request_processing_b(host, port, payload, timeout):
        return {
            "status": "ok",
            "screenshot_b64": "iVBOR...",   # base64 fake
            "performance": {"load_time_ms": 123, "total_size_kb": 456, "num_requests": 7},
            "thumbnails_b64": ["dGVzdDE=", "dGVzdDI="],
        }
    monkeypatch.setattr(server_scraping, "request_processing_b", fake_request_processing_b)

    app = await _start_app()
    async with TestServer(app) as ts, TestClient(ts) as client:
        resp = await client.get("/scrape", params={"url": "https://example.com"})
        assert resp.status == 200
        data = await resp.json()
        assert data["status"] == "success"
        assert "scraping_data" in data
        assert "processing_data" in data
        assert data["processing_data"]["performance"]["num_requests"] == 7
        # shape estable
        assert "title" in data["scraping_data"]
        assert "links" in data["scraping_data"]
        assert "meta_tags" in data["scraping_data"]
        assert "structure" in data["scraping_data"]
        assert "images_count" in data["scraping_data"]

async def test_scrape_invalid_url():
    """
    URL inválida → 400.
    """
    app = await _start_app()
    async with TestServer(app) as ts, TestClient(ts) as client:
        resp = await client.get("/scrape", params={"url": "ftp://bad"})
        assert resp.status == 400
        data = await resp.json()
        assert data["error"] == "invalid_url"

async def test_scrape_processing_timeout(monkeypatch):
    """
    Si B timeoutea/cae → status: partial y processing_data None (o shape parcial si lo ajustaste).
    """
    async def fake_timeout(*args, **kwargs):
        raise asyncio.TimeoutError()
    monkeypatch.setattr(server_scraping, "request_processing_b", fake_timeout)

    app = await _start_app()
    async with TestServer(app) as ts, TestClient(ts) as client:
        resp = await client.get("/scrape", params={"url": "https://example.com"})
        assert resp.status == 200
        data = await resp.json()
        assert data["status"] == "partial"
        assert data["processing_data"] is None or data["processing_data"]["performance"] is None

async def test_queue_flow_with_friendly_ids(monkeypatch):
    """
    /scrape_cola → devuelve task_id + friendly_id; /status y /result funcionan.
    """
    async def fake_request_processing_b(host, port, payload, timeout):
        return {
            "status": "ok",
            "screenshot_b64": "iVBOR...",
            "performance": {"load_time_ms": 99, "total_size_kb": 111, "num_requests": 3},
            "thumbnails_b64": [],
        }
    monkeypatch.setattr(server_scraping, "request_processing_b", fake_request_processing_b)

    app = await _start_app()
    async with TestServer(app) as ts, TestClient(ts) as client:
        # Encolar
        r1 = await client.get("/scrape_cola", params={"url": "https://google.com"})
        assert r1.status == 200
        j = await r1.json()
        assert "task_id" in j
        assert "friendly_id" in j
        friendly = j["friendly_id"]
        assert friendly.startswith("google")  # depende de tu amigable.py

        # Polling de estado
        for _ in range(30):  # hasta ~3s con sleeps
            rs = await client.get(f"/status/{friendly}")
            js = await rs.json()
            if js["status"] == "completed":
                break
            await asyncio.sleep(0.1)
        assert js["status"] == "completed"

        # Obtener resultado con friendly_id
        rr = await client.get(f"/result/{friendly}")
        jr = await rr.json()
        assert jr["status"] == "success"
        assert jr["friendly_id"] == friendly
        assert "scraping_data" in jr
        assert "processing_data" in jr
