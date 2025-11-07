# ==============================
# File: server_scraping.py
# ==============================
import argparse
import asyncio
import json
import os
from datetime import datetime, timezone
from urllib.parse import urlparse

from aiohttp import web

from scraper.async_http import AsyncHTTPClient
from scraper.html_parser import parse_basic_structure
from scraper.metadata_extractor import extract_meta_tags
from common.serialization import b64_png, utc_timestamp
from common.protocol import encode_message, decode_message_async

# ------------------------------
# Config y argumentos CLI
# ------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        prog="server_scraping.py",
        description="Servidor de Scraping Web Asíncrono",
    )
    parser.add_argument("-i", "--ip", required=True, help="Dirección de escucha (IPv4/IPv6)")
    parser.add_argument("-p", "--port", type=int, required=True, help="Puerto de escucha")
    parser.add_argument("-w", "--workers", type=int, default=4, help="Límite de concurrencia por dominio")
    parser.add_argument("--proc-host", default=os.getenv("PROC_HOST", "127.0.0.1"), help="Host del servidor de procesamiento (B)")

    parser.add_argument("--proc-port", type=int, default=int(os.getenv("PROC_PORT", "9000")), help="Puerto del servidor de procesamiento (B)")

    parser.add_argument("--proc-timeout", type=float, default=25.0, help="Timeout de solicitud a B (segundos)")
    parser.add_argument("--request-timeout", type=float, default=30.0, help="Timeout por página (segundos)")

    parser.add_argument("--processor", help="URL completa del processor, ej: http://127.0.0.1:9000")

    args = parser.parse_args()
    if args.processor:
        from urllib.parse import urlparse
        u = urlparse(args.processor)
        if u.hostname:
            args.proc_host = u.hostname
        if u.port:
            args.proc_port = u.port

    return parser.parse_args()

# ------------------------------
# Comunicación con Servidor B (sockets TCP + framing JSON)
# ------------------------------

async def request_processing_b(host: str, port: int, payload: dict, timeout: float):
    """Envía una solicitud de procesamiento al Servidor B y espera respuesta.
    Devuelve un dict con los campos esperados o levanta excepción si falla.
    """
    reader = writer = None
    try:
        conn_coro = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(conn_coro, timeout=timeout)
        msg = encode_message(payload)
        writer.write(msg)
        await writer.drain()
        # Leer respuesta enquadrada
        response_obj = await asyncio.wait_for(decode_message_async(reader), timeout=timeout)
        return response_obj
    finally:
        if writer is not None:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

# ------------------------------
# Handlers HTTP
# ------------------------------

async def handle_health(request: web.Request):
    return web.json_response({"status": "ok"})

async def handle_scrape(request: web.Request):
    app = request.app
    url = request.query.get("url")
    if not url:
        return web.json_response({"status": "failed", "error": "missing_url"}, status=400)

    # Validación simple de URL
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return web.json_response({"status": "failed", "error": "invalid_url"}, status=400)

    http_client: AsyncHTTPClient = app["http_client"]
    proc_host: str = app["proc_host"]
    proc_port: int = app["proc_port"]
    proc_timeout: float = app["proc_timeout"]
    page_timeout: float = app["request_timeout"]

    try:
        # Descarga HTML asíncrona con límite por dominio y timeout
        html, final_url = await http_client.fetch_html(url, timeout=page_timeout)

        # Parsing de estructura básica y metadatos
        basic = parse_basic_structure(html, base_url=final_url)
        meta = extract_meta_tags(html)

        scraping_data = {
            "title": basic["title"],
            "links": basic["links"],
            "meta_tags": meta,
            "structure": basic["structure"],
            "images_count": basic["images_count"],
        }

        # Preparar solicitud a Servidor B (procesamiento adicional)
        processing_request = {
            "task": "full_processing",
            "url": final_url,
            "options": {
                "screenshot": True,
                "performance": True,
                "image_thumbs": min(3, scraping_data["images_count"])  # pedir hasta 3 thumbs
            },
        }

        processing_data = None
        try:
            resp_b = await request_processing_b(proc_host, proc_port, processing_request, timeout=proc_timeout)
            if isinstance(resp_b, dict) and resp_b.get("status") == "ok":
                processing_data = {
                    "screenshot": resp_b.get("screenshot_b64"),
                    "performance": resp_b.get("performance"),
                    "thumbnails": resp_b.get("thumbnails_b64", []),
                }
            else:
                processing_data = None
        except (asyncio.TimeoutError, ConnectionError, OSError):
            # B no disponible o tardó mucho → devolvemos parcial
            processing_data = None

        status = "success" if processing_data is not None else "partial"
        result = {
            "url": final_url,
            "timestamp": utc_timestamp(),
            "scraping_data": scraping_data,
            "processing_data": processing_data,
            "status": status,
        }
        return web.json_response(result)

    except asyncio.TimeoutError:
        return web.json_response({"status": "failed", "error": "timeout"}, status=504)
    except Exception as e:
        return web.json_response({"status": "failed", "error": str(e)}, status=500)

# ------------------------------
# App Factory
# ------------------------------

async def app_factory(args) -> web.Application:
    app = web.Application()

    # Cliente HTTP asíncrono compartido (con límites por dominio)
    http_client = AsyncHTTPClient(max_per_domain=args.workers)
    await http_client.start()

    app["http_client"] = http_client
    app["proc_host"] = args.proc_host
    app["proc_port"] = args.proc_port
    app["proc_timeout"] = args.proc_timeout
    app["request_timeout"] = args.request_timeout

    app.router.add_get("/health", handle_health)
    app.router.add_get("/scrape", handle_scrape)
    app.router.add_get("/", lambda request: web.json_response(
    {"status": "ok", "endpoints": ["/health", "/scrape?url=<url>"]}
))


    async def on_cleanup(app_):
        await app_["http_client"].close()

    app.on_cleanup.append(on_cleanup)
    return app


def main():
    args = parse_args()
    web.run_app(app_factory(args), host=args.ip, port=args.port)


if __name__ == "__main__":
    main()

# Para ver que devuelve health
# curl http://127.0.0.1:8000/health

# Para ver que devuelve scrape
# curl -v 'http://127.0.0.1:8000/scrape?url=https://www.hola.com/us-es/entretenimiento/20251107866424/miss-universe-2025-candidatas-fuera-competencia/'
# curl -v 'http://127.0.0.1:8000/scrape?url=https://google.com'
