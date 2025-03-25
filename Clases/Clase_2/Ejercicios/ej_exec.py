import os

pid = os.fork()

if pid == 0:
    os.execlp("ls", "ls", "-l")  # Reemplaza al hijo con el programa 'ls'
else:
    os.wait()
