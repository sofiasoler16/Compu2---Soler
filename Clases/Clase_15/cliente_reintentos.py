import socket
import time
# ejercico 5

# con nc -l 127.0.0.1 9004 (este es el servidor)
# este codigo es el cliente que reintenta conectarse
HOST, PORT = "127.0.0.1", 9004

def try_connect(max_retries=10, base_backoff=0.5): #subi la cantidad de intentos
    for attempt in range(1, max_retries + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(4)  # subi los segundos
                s.connect((HOST, PORT))
                s.sendall(b"ping\n") # esto es la respuesta del servidor diciendo que se conecto al cliente
                data = s.recv(1024)
                return data
        except (socket.timeout, ConnectionRefusedError) as e:
            sleep_s = base_backoff * attempt
            print(f"Intento {attempt} falló ({e}). Reintento en {sleep_s:.1f}s...")
            time.sleep(sleep_s)
    raise TimeoutError("Servidor no disponible tras varios reintentos")

if __name__ == "__main__":
    print(try_connect())