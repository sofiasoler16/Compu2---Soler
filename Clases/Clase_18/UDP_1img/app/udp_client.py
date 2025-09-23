
import argparse, socket

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--server", required=True, help="host or service name")
    p.add_argument("--port", type=int, required=True)
    p.add_argument("--message", default="ping")
    p.add_argument("--timeout", type=float, default=2.0)
    args = p.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(args.timeout)
        s.sendto(args.message.encode("utf-8"), (args.server, args.port))
        data, _ = s.recvfrom(4096)
        print("Response:", data.decode("utf-8", errors="ignore").strip())

if __name__ == "__main__":
    main()
