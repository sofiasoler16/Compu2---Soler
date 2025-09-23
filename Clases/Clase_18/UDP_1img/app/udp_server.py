
import argparse, socketserver, time, os, logging, sys

LOG_DIR = "/var/log/udp"

class EchoUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        msg = data.decode("utf-8", errors="ignore").strip()
        logging.info("ECHO from %s: %r", self.client_address, msg)
        sock.sendto(msg.upper().encode("utf-8"), self.client_address)

class NowUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        msg = data.decode("utf-8", errors="ignore").strip()
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        logging.info("NOW from %s (req=%r) -> %s", self.client_address, msg, now)
        sock.sendto(f"{now}\n".encode("utf-8"), self.client_address)

class ReusableUDPServer(socketserver.UDPServer):
    allow_reuse_address = True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["echo","now"], required=True)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=9007)
    args = parser.parse_args()

    os.makedirs(LOG_DIR, exist_ok=True)
    logfile = os.path.join(LOG_DIR, f"{args.mode}.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(logfile),
            logging.StreamHandler(sys.stdout),
        ],
    )

    handler = EchoUDPHandler if args.mode == "echo" else NowUDPHandler
    with ReusableUDPServer((args.host, args.port), handler) as server:
        print(f"[{args.mode.upper()}] UDP server listening on {args.host}:{args.port}")
        server.serve_forever()

if __name__ == "__main__":
    main()
