import socket

def main():
    HOST, PORT = "127.0.0.1", 8000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world\n")
        data = s.recv(4096)
        print(f"< {data!r}")

if __name__ == "__main__":
    main()