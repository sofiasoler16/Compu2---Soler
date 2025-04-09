#Usando fork cree 2 hijos, uno de ellos espere 2 segundos y diga soy el hijo 2 mi pip es tanto
#que el hijo 2 espere 2 segundos y diga soy el hijo 1 mi pip es tanto
#El padre no espere nada, termina antes que los hijos



import os
import time

def create_child(wait_time, message):
    pid = os.fork()
    if pid == 0:
        # Estamos en el hijo
        time.sleep(wait_time)
        print(f"{message}, mi PID es {os.getpid()}, el PID de mi padre es: {os.getppid()}")
        os._exit(0)  # Terminamos bien el hijo
    # El padre simplemente sigue, no hace nada en esta función

if __name__ == "__main__":
    # Creamos los hijos
    create_child(2, "Soy el hijo 2")  # Este hablará a los 2 segundos
    create_child(4, "Soy el hijo 1")  # Este hablará a los 4 segundos

    # El padre no espera. Solo duerme 1 segundo para que su mensaje se imprima primero.
    time.sleep(1)
    print(f"Soy el padre, mi PID es {os.getpid()}")
    os._exit(0)  # También terminamos el padre bien



# for i in range(2):
#     pid = os.fork()
#     if pid == 0:
#         # Estamos en el hijo
#         if i == 0:
#             time.sleep(2)
#             print("[HIJO 1] Mi PID es", os.getpid(), "Mi padre es", os.getppid())
#         else:
#             time.sleep(4)
#             print("[HIJO 2] Mi PID es", os.getpid(), "Mi padre es", os.getppid())
#         os._exit(0)  # Termina el hijo
#         # Nota: sin esto, el hijo seguiría el ciclo y podría crear más hijos

# # El padre no espera, simplemente termina
# print("[PADRE] Termino mi trabajo, mi PID es", os.getpid())
# os._exit(0)

# pid1 = os.fork() 
# pid2 = os.fork() #Al hacer esto cree 2 procesos, es decir 4 hijos

# if pid1 == 0:
#     time.sleep(2)
#     os.wait()
#     print("[HIJO 1] Mi PID es", os.getpid(), "Mi padre es", os.getppid())


# if pid2 == 0:
#     time.sleep(3)
#     print("[HIJO 2] Mi PID es", os.getpid(), "Mi padre es", os.getppid())

# os._exit(0)
