import os
import json, time, random
from datetime import datetime

FIFO_FRECUENCIA = "/tmp/fifo_frecuencia"
FIFO_PRESION    = "/tmp/fifo_presion"
FIFO_OXIGENO    = "/tmp/fifo_oxigeno"


def crear_fifos():
    for fifo in [FIFO_FRECUENCIA, FIFO_PRESION, FIFO_OXIGENO]:
        if not os.path.exists(fifo):
            os.mkfifo(fifo)


def generar_datos():
    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "frecuencia": random.randint(60, 180),
        "presion": [random.randint(110, 180), random.randint(70, 110)],
        "oxigeno": random.randint(90, 100)
    }

def proceso_generador():
    crear_fifos()
    with open(FIFO_FRECUENCIA, 'w') as f1, open(FIFO_PRESION, 'w') as f2, open(FIFO_OXIGENO, 'w') as f3:
        for _ in range(60):
            dato = generar_datos()
            json_str = json.dumps(dato)
            f1.write(json_str + '\n')
            f1.flush()
            f2.write(json_str + '\n')
            f2.flush()
            f3.write(json_str + '\n')
            f3.flush()
            print("Generado:", dato)
            time.sleep(1)