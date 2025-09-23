#!/usr/bin/env python3
import socketserver, time, os, sys, logging

LOG_DIR = "/app/logs"
PORT = int(os.environ.get("PORT", "9999"))
HOST = os.environ.get("HOST", "0.0.0.0")

class NowUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        msg = (data or b"").decode("utf-8", errors="ignore").strip()
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        logging.info("req from %s msg=%r -> %s", self.client_address, msg, now)
        sock.sendto((now + "\n").encode("utf-8"), self.client_address)

class ReusableUDPServer(socketserver.UDPServer):
    allow_reuse_address = True

def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(os.path.join(LOG_DIR, "time.log")),
                  logging.StreamHandler(sys.stdout)]
    )
    with ReusableUDPServer((HOST, PORT), NowUDPHandler) as srv:
        print(f"[NOW] UDP server listening on {HOST}:{PORT}", flush=True)
        srv.serve_forever()

if __name__ == "__main__":
    main()
