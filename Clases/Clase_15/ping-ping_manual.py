import socket
# ejercico 7

# TCP --> hay conexion, el flujo esta ordenado, es confiable

# UDP --> no orientado a conexion, el cliente manda un paquete, el servidor recibe
# Cada datagrama viaja por separado, no hay garantia de orden ni de entrega

HOST, PORT = "127.0.0.1", 9006

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"ping", (HOST, PORT))
    data, addr = s.recvfrom(2048)
    print(f"< {data!r} desde {addr}")