import os
import sys

def main():
    # Crear pipe: devuelve (lectura, escritura)
    read_fd, write_fd = os.pipe()

    pid = os.fork()

    if pid > 0:  # Proceso padre
        os.close(read_fd)  # No va a leer

        # Convertir a objeto archivo para escribir fácilmente
        with os.fdopen(write_fd, 'w') as write_pipe:
            message = input("Padre: Ingresá un mensaje para el hijo: ")
            write_pipe.write(message + "\n")
            write_pipe.flush()
            print("Padre: Mensaje enviado. Esperando que el hijo termine...")
        
        os.waitpid(pid, 0)
        print("Padre: El hijo terminó.")

    else:  # Proceso hijo
        os.close(write_fd)  # No va a escribir

        # Convertir a objeto archivo para leer fácilmente
        with os.fdopen(read_fd) as read_pipe:
            print("Hijo: Esperando mensaje...")
            message = read_pipe.readline().strip()
            print(f"Hijo: Mensaje recibido: '{message}'")
            print(f"Hijo: Procesando el mensaje... → '{message.upper()}'")

        sys.exit(0)

if __name__ == "__main__":
    main()
