import os

pid = os.fork()

if pid == 0:
    print("[HIJO] Finalizando...")
    os._exit(0)  # Siempre que un hijo termina, debe salir explícitamente
else:
    print("[PADRE] Esperando que termine el hijo...")
    os.wait()
    print("[PADRE] Hijo terminado")
