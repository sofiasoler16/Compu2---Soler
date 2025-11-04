
import socket, sys
ip = sys.argv[1]      #192.168.86.219
port = int(sys.argv[2])
msg = sys.argv[3]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip, port))
    s.sendall(msg.encode("ascii"))
    print("Received:", s.recv(1024).decode("ascii"))
