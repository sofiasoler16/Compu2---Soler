from multiprocessing import Process, Queue
import time
import random

def productor(queue, id_productor):
    for i in range(3):
        num = random.randint(1, 100)
        print(f"[Productor {id_productor}] Enviando: {num}")
        queue.put(num)
        time.sleep(random.random())
    queue.put("FIN")

def consumidor(queue, id_consumidor):
    while True:
        num = queue.get()
        if num == "FIN":
            print(f"[Consumidor {id_consumidor}] Terminando")
            queue.put("FIN")  # Para avisar a otros consumidores
            break
        print(f"[Consumidor {id_consumidor}] Recibí {num} - Su doble es: {num*2}")

if __name__ == '__main__':
    q = Queue()

    productores = [Process(target=productor, args=(q, i)) for i in range(2)]
    consumidores = [Process(target=consumidor, args=(q, i)) for i in range(2)]

    for p in productores + consumidores:
        p.start()

    for p in productores + consumidores:
        p.join()
