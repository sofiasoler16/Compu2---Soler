import threading
import time

# Semáforo con 1 permiso (solo un hilo puede acceder a la vez)
semaforo_impresora = threading.Semaphore(1)

def usar_impresora(nombre_hilo):
    print(f"{nombre_hilo} quiere usar la impresora...")
    semaforo_impresora.acquire()  # Pide acceso
    print(f"{nombre_hilo} está usando la impresora 🖨️")
    time.sleep(2)  # Simula tiempo de uso
    print(f"{nombre_hilo} terminó de usar la impresora.")
    semaforo_impresora.release()  # Libera el recurso

# Crear varios hilos
hilos = []
for i in range(3):
    nombre = f"Hilo-{i+1}"
    hilo = threading.Thread(target=usar_impresora, args=(nombre,))
    hilos.append(hilo)
    hilo.start()

# Esperamos a que todos terminen
for hilo in hilos:
    hilo.join()

print("Todos los hilos terminaron.")