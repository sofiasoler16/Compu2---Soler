from multiprocessing import Process
import os, time

def tarea():
    time.sleep(10)
    print(f"Proceso hijo ejecutándose. PID: {os.getpid()}")

if __name__ == '__main__':
    print(f"Proceso principal. PID: {os.getpid()}")
    p = Process(target=tarea)

    time.sleep(10)  # 1° espera del padre
    p.start()       # Crea y arranca al hijo (quien también hace sleep 10)
    print("Post start -------------------")

    time.sleep(10)  # 2° espera del padre
    p.join()        # Espera al hijo si aún no terminó
    print("El proceso hijo ha terminado.")
