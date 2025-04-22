from time import sleep
import datetime

with open('canal', 'w') as fifo:
    for i in range(3):
        mensaje = f"[{datetime.datetime.now()}] Mensaje {i + 1}\n"
        fifo.write(mensaje)
        print("Productor escribió:", mensaje.strip())
        sleep(2)
