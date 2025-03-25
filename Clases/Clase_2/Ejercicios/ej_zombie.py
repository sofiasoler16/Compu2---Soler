import os, time

pid = os.fork()

if pid == 0:
    print("[HIJO] Terminando")
    os._exit(0)
else:
    print("[PADRE] No recolecto al hijo por 15 segundos")
    time.sleep(15)
    os.wait()
