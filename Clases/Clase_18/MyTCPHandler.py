import socketserver, threading

class MyTCPHandler(socketserver.StreamRequestHandler):
    # StreamRequestHandler te da rfile/wfile tipo archivo
    def handle(self):
        line = self.rfile.readline().strip()   # lee una línea (bloquea hasta \n)
        print(f"{self.client_address[0]} wrote:")
        print(line)
        self.wfile.write(line.upper() + b"\n") # responde en MAYÚSCULAS

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True     # liberar rápido el puerto al reiniciar
    daemon_threads = True          # hilos “daemon”

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999   # <<< CLAVE: 0.0.0.0 escucha en todas las interfaces
    with ThreadedTCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"TCP server escuchando en {HOST}:{PORT}")
        server.serve_forever()