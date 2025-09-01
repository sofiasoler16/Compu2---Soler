# client_interactivo.py
import socket, sys, select

HOST, PORT = "127.0.0.1", 9008

with socket.create_connection((HOST, PORT)) as s:
    s.setblocking(False)
    print(f"Conectado a {HOST}:{PORT}. Escribí y Enter. Ctrl-D para dejar de ENVIAR.")
    while True:
        r, _, _ = select.select([s, sys.stdin], [], [])
        if s in r:
            data = s.recv(4096)
            if not data:
                print("\n<peer cerró la conexión>")
                break
            sys.stdout.write(data.decode("utf-8", errors="replace"))
            sys.stdout.flush()
        if sys.stdin in r:
            line = sys.stdin.readline()
            if line == "":               # Ctrl-D en stdin
                s.shutdown(socket.SHUT_WR)
            else:
                s.sendall(line.encode("utf-8"))
