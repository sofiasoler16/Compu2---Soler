import os

#Que hace exec?
#Reemplaza el contenido del proceso actual (usualmente el hijo) con un nuevo programa.
#Ese nuevo programa ocupa toda la memoria del proceso, borrando lo anterior.

pid = os.fork() #Crea un proceso hijo

if pid == 0:
    os.execlp("ls", "ls", "-l")  # Reemplaza al hijo con el programa 'ls'
else:
    os.wait()
