# dormir.py
import time
import signal
import sys

def manejar_sigterm(signum, frame):
    print("Proceso recibido SIGTERM. Terminando.")
    sys.exit(0)

signal.signal(signal.SIGINT, manejar_sigterm)

print("Proceso iniciado. Durmiendo 40 segundos...")
while True:pass
print("Proceso terminado.")
