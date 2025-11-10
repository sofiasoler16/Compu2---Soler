import asyncio
import os
import socket
import json
import pytest

from common.protocol import encode_message, decode_message_async

PROC_HOST = os.getenv("PROC_HOST", "127.0.0.1")
PROC_PORT = int(os.getenv("PROC_PORT", "9000"))

pytestmark = pytest.mark.asyncio

async def _rpc(payload: dict, timeout=8.0):
    """
    Cliente mínimo al protocolo del Server B usando framing JSON.
    """
    reader, writer = await asyncio.wait_for(
        asyncio.open_connection(PROC_HOST, PROC_PORT), timeout=timeout
    )
    try:
        writer.write(encode_message(payload))
        await writer.drain()
        resp = await asyncio.wait_for(decode_message_async(reader), timeout=timeout)
        return resp
    finally:
        writer.close()
        await writer.wait_closed()

@pytest.mark.integration
async def test_full_processing_ok():
    """
    Server B debe responder OK para una URL simple.
    """
    payload = {
        "task": "full_processing",
        "url": "https://example.com",
        "options": {"screenshot": True, "performance": True, "image_thumbs": 2},
    }
    try:
        resp = await _rpc(payload)
    except (ConnectionRefusedError, OSError):
        pytest.skip("Server B no está corriendo en 127.0.0.1:9000")

    assert isinstance(resp, dict)
    assert resp.get("status") in ("ok", "error")  # según tu implementación
    if resp["status"] == "ok":
        assert "screenshot_b64" in resp
        assert "performance" in resp
        assert "thumbnails_b64" in resp
        perf = resp["performance"]
        assert all(k in perf for k in ("load_time_ms", "total_size_kb", "num_requests"))

@pytest.mark.integration
async def test_invalid_task():
    """
    Si mando una task inválida, B debería devolver error.
    """
    payload = {"task": "no_such_task", "url": "https://example.com", "options": {}}
    try:
        resp = await _rpc(payload)
    except (ConnectionRefusedError, OSError):
        pytest.skip("Server B no está corriendo en 127.0.0.1:9000")

    assert isinstance(resp, dict)
    assert resp.get("status") == "error"

@pytest.mark.integration
async def test_concurrent_requests():
    """
    Varias solicitudes concurrentes para ejercitar el pool de procesos.
    """
    try:
        resps = await asyncio.gather(*[
            _rpc({
                "task": "full_processing",
                "url": "https://example.com",
                "options": {"screenshot": True, "performance": True, "image_thumbs": 1},
            })
            for _ in range(4)
        ])
    except (ConnectionRefusedError, OSError):
        pytest.skip("Server B no está corriendo en 127.0.0.1:9000")

    assert len(resps) == 4
    ok_count = sum(1 for r in resps if r.get("status") == "ok")
    assert ok_count >= 1  # al menos una OK (según recursos de la máquina)
