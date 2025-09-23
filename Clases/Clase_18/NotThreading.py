#!/usr/bin/env python3
import socketserver
import os

class ProcessTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).decode("ascii")
        pid = os.getpid()
        response = f"{pid}: {data}"
        self.request.sendall(response.encode("ascii"))

class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    allow_reuse_address = True  # liberar rápido el puerto al reiniciar
    # opcional: limitar procesos hijos
    # max_children = 64

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999   # <<< clave para aceptar conexiones externas
    with ForkedTCPServer((HOST, PORT), ProcessTCPRequestHandler) as server:
        print(f"Servidor corriendo en {HOST}:{PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nDeteniendo…")
