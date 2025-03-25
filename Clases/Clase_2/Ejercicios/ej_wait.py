import os

#Que hace wait?
#Sirve para que el proceso padre espere a que el hijo termine, 
#recoja su estado de salida, y libere correctamente los recursos del sistema operativo.

#💡 Si no lo hacés, el hijo puede quedar como zombi (ya lo vamos a ver).

pid = os.fork()

if pid == 0:
    print("[HIJO] Finalizando...")
    os._exit(0)  # Siempre que un hijo termina, debe salir explícitamente
else:
    print("[PADRE] Esperando que termine el hijo...")
    os.wait()
    print("[PADRE] Hijo terminado")
