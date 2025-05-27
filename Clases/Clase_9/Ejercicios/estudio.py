import threading
import time
import random

# Sala con 3 lugares disponibles
sala_estudio = threading.Semaphore(3)

def estudiante(nombre):
    print(f"{nombre} quiere entrar a la sala.")
    sala_estudio.acquire()
    print(f"{nombre} ha entrado a la sala 📚")
    time.sleep(random.uniform(1, 3))  # Tiempo de estudio aleatorio
    print(f"{nombre} ha salido de la sala.")
    sala_estudio.release()

# Crear varios hilos (más de 3)
hilos = []
for i in range(6):
    nombre = f"Estudiante-{i+1}"
    hilo = threading.Thread(target=estudiante, args=(nombre,))
    hilos.append(hilo)
    hilo.start()

# Esperamos a que todos terminen
for hilo in hilos:
    hilo.join()

print("Todos los estudiantes terminaron.")