import os

#Que hace fork?
#clona el proceso actual, creando un proceso hijo idéntico pero con su propio espacio de memoria.
#La función devuelve dos veces:

#En el padre, retorna el PID del hijo.
#En el hijo, retorna 0.


pid = os.fork()

if pid == 0:
    print("[HIJO] Mi PID es", os.getpid(), "Mi padre es", os.getppid())
else:
    print("[PADRE] Mi PID es", os.getpid(), "Creé un hijo con PID", pid)
