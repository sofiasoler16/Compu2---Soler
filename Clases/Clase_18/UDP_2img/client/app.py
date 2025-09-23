#!/usr/bin/env python3
import os, socket, sys

HOST = os.environ.get("SERVER_HOST", "time-server")
PORT = int(os.environ.get("SERVER_PORT", "9999"))
MSG  = os.environ.get("MESSAGE", "time")
TO   = float(os.environ.get("TIMEOUT", "2.0"))

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(TO)
        s.sendto(MSG.encode("utf-8"), (HOST, PORT))
        try:
            data, _ = s.recvfrom(4096)
            print("Response:", data.decode("utf-8", errors="ignore").strip())
        except socket.timeout:
            print("Timeout esperando respuesta", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
