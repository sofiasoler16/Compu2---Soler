#Aca quiero que el padre termine despues de esperar a 1 hijo

import os
import time

pid1 = os.fork()

if pid1 == 0:
    # Hijo 1
    time.sleep(4)
    print("[HIJO 1] Mi PID es", os.getpid(), "Mi padre es", os.getppid())
    os._exit(0)

# Solo el padre sigue acá
pid2 = os.fork()

if pid2 == 0:
    # Hijo 2
    time.sleep(6)
    print("[HIJO 2] Mi PID es", os.getpid(), "Mi padre es", os.getppid())
    os._exit(0)

# El padre solo espera a Hijo 1
os.waitpid(pid1, 0)

print("[PADRE] Hijo 1 terminó. Mi PID es", os.getpid())
os._exit(0)
