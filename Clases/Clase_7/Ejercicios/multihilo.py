import threading
import signal
import os
import time

# Evento para coordinar hilos
evento = threading.Event()

def handler(signum, frame):
    print(f"[Main] Señal {signum} recibida, activando evento.")
    evento.set()

def worker():
    print(f"[Hilo {threading.current_thread().name}] Esperando evento...")
    evento.wait()
    print(f"[Hilo {threading.current_thread().name}] ¡Evento recibido! Continuando...")

if __name__ == "__main__":
    signal.signal(signal.SIGUSR1, handler)

    for i in range(3):
        threading.Thread(target=worker, name=f"Hilo-{i}").start()

    print(f"[Main] PID: {os.getpid()} - Enviar SIGUSR1 para activar los hilos")

    while True:
        time.sleep(1)
