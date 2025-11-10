import argparse
import socket
import socketserver
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from common.protocol import (
    encode_message,
    decode_message_async, 
)
from common.protocol import decode_message_sync, send_message_sync

from processor.screenshot import take_screenshot_png
from processor.performance import measure_performance
from processor.image_processor import build_thumbnails


class ProcessingTCPHandler(socketserver.BaseRequestHandler):
    
    executor: ProcessPoolExecutor = None  

    def handle(self):
        sock: socket.socket = self.request
        try:
            req = decode_message_sync(sock)
            print(f"[B] Recibida tarea: {req}", flush=True)

        except Exception as e:
            # Si no pudimos decodificar, respondemos error simple
            resp = {"status": "error", "message": f"bad_request: {e}"}
            try:
                send_message_sync(sock, resp)
            except Exception:
                pass
            return

        task = (req or {}).get("task")
        url = (req or {}).get("url")
        options = (req or {}).get("options", {})

        if task != "full_processing":
            # devolver error explícito para tasks desconocidas
            send_message_sync(sock, {"status": "error", "error": f"unknown_task:{task}"})
            return

        if not url:
            send_message_sync(sock, {"status": "error", "error": "missing_url"})
            return

        fut = self.executor.submit(process_request, url, options)
        try:
            result = fut.result(timeout=60)  # seguridad en el handler
        except Exception as e:
            result = {"status": "error", "message": str(e)}

        try:
            send_message_sync(sock, result)
        except Exception:
            pass


def process_request(url: str, options: dict) -> dict:
    """Corre en un PROCESO del pool. Hace screenshot, performance e imágenes."""
    screenshot_png_b64 = None
    performance = None
    thumbs_b64 = []

    # Screenshot
    if options.get("screenshot", True):
        try:
            png_bytes = take_screenshot_png(url, viewport=(1280, 800), timeout=15)
            if png_bytes:
                from common.serialization import b64_png
                screenshot_png_b64 = b64_png(png_bytes)
        except Exception:
            screenshot_png_b64 = None

    # Performance
    if options.get("performance", True):
        try:
            performance = measure_performance(url, max_resources=40, per_request_timeout=6)
        except Exception:
            performance = {"load_time_ms": None, "total_size_kb": None, "num_requests": None}

    # Thumbnails
    n_thumbs = int(options.get("image_thumbs", 0) or 0)
    if n_thumbs > 0:
        try:
            thumbs_b64 = build_thumbnails(url, limit=n_thumbs, max_image_bytes=3_000_000, thumb_px=256)
        except Exception:
            thumbs_b64 = []

    return {
        "status": "ok",
        "screenshot_b64": screenshot_png_b64,
        "performance": performance,
        "thumbnails_b64": thumbs_b64,
    }


def parse_args():
    parser = argparse.ArgumentParser(
        prog="server_processing.py",
        description="Servidor de Procesamiento Distribuido",
    )
    parser.add_argument("-i", "--ip", required=True, help="Dirección de escucha")
    parser.add_argument("-p", "--port", type=int, required=True, help="Puerto de escucha")
    parser.add_argument("-n", "--processes", type=int, default=os.cpu_count() or 2,
                        help="Número de procesos en el pool (default: CPU count)")
    return parser.parse_args()


class ReusableTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    args = parse_args()

    with ProcessPoolExecutor(max_workers=args.processes) as executor:
        ProcessingTCPHandler.executor = executor
        with ReusableTCPServer((args.ip, args.port), ProcessingTCPHandler) as server:
            host, port = server.server_address
            print(f"Processing Server listening on {host}:{port} (proc workers={args.processes})")
            try:
                server.serve_forever(poll_interval=0.5)
            except KeyboardInterrupt:
                print("Shutting down...")


if __name__ == "__main__":
    main()

