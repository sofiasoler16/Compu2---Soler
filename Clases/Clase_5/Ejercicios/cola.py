
from multiprocessing import Process, Queue


def productor(queue):
    for num in range(0, 20, 2):  # 0, 2, 4, 6, 8, 10, 12, 14, 16, 18
        print(f"[Productor] Enviando: {num}")
        queue.put(num)
    queue.put("FIN")  # Señal de fin

def consumidor(queue):
    while True:
        num = queue.get()
        if num == "FIN":
            print("[Consumidor] Fin de la comunicación")
            break
        print(f"[Consumidor] Recibí {num} - Su doble es: {num*2}")

if __name__ == '__main__':
    q = Queue()

    p1 = Process(target=productor, args=(q,))
    p2 = Process(target=consumidor, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
