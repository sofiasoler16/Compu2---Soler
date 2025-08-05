from multiprocessing import Process, Queue

from generador import FIFO_FRECUENCIA, FIFO_PRESION, FIFO_OXIGENO, proceso_generador
from generador import crear_fifos
from analizador import proceso_analizador
from verificador import proceso_verificador

if __name__ == "__main__":
    crear_fifos()

    q_frec = Queue()
    q_pres = Queue()
    q_oxi = Queue()

    procesos = [
        Process(target=proceso_analizador, args=("Frecuencia", FIFO_FRECUENCIA, "frecuencia", q_frec)),
        Process(target=proceso_analizador, args=("Presion", FIFO_PRESION, "presion", q_pres)),
        Process(target=proceso_analizador, args=("Oxigeno", FIFO_OXIGENO, "oxigeno", q_oxi)),
        Process(target=proceso_generador),
        Process(target=proceso_verificador, args=(q_frec, q_pres, q_oxi))
    ]

    for p in procesos:
        p.start()

    for p in procesos:
        p.join()




