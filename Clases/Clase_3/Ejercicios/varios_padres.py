#5 padres y cada uno crea a sus hijos, en forma de cascada

import os
import time

print(f"[Nivel 1] PID: {os.getpid()}, PPID: {os.getppid()}")
pid = os.fork()

if pid == 0:
    # Nivel 2
    print(f"[Nivel 2] PID: {os.getpid()}, PPID: {os.getppid()}")
    pid = os.fork()

    if pid == 0:
        # Nivel 3
        print(f"[Nivel 3] PID: {os.getpid()}, PPID: {os.getppid()}")
        pid = os.fork()

        if pid == 0:
            # Nivel 4
            print(f"[Nivel 4] PID: {os.getpid()}, PPID: {os.getppid()}")
            pid = os.fork()

            if pid == 0:
                # Nivel 5 (último)
                print(f"[Nivel 5] PID: {os.getpid()}, PPID: {os.getppid()}")
                time.sleep(1)
                print(f"[Nivel 5] PID: {os.getpid()} finalizando.")
            else:
                time.sleep(2)
                print(f"[Nivel 4] PID: {os.getpid()} finalizando.")
        else:
            time.sleep(2)
            print(f"[Nivel 3] PID: {os.getpid()} finalizando.")
    else:
        time.sleep(2)
        print(f"[Nivel 2] PID: {os.getpid()} finalizando.")
else:
    time.sleep(2)
    print(f"[Nivel 1] PID: {os.getpid()} finalizando.")
