import os
import sys
import select

FIFO_ENTRADA = "canal_in"
FIFO_SALIDA = "canal_out"

# Abrimos FIFOs en modo no bloqueante
fd_entrada = os.open(FIFO_ENTRADA, os.O_RDONLY | os.O_NONBLOCK)
fd_salida = os.open(FIFO_SALIDA, os.O_WRONLY)

print("Chat iniciado. Escribí tu mensaje y presioná Enter. Escribí 'salir' para cerrar.")

while True:
    # select permite saber si hay algo para leer sin bloquear
    rlist, _, _ = select.select([fd_entrada, sys.stdin], [], [])

    for fuente in rlist:
        if fuente == fd_entrada:
            try:
                mensaje = os.read(fd_entrada, 1024).decode()
                if mensaje:
                    print("\nOtro:", mensaje.strip())
                else:
                    print("\n[Fin de comunicación]")
                    os.close(fd_entrada)
                    os.close(fd_salida)
                    exit(0)
            except BlockingIOError:
                pass  # No hay nada para leer

        elif fuente == sys.stdin:
            texto = sys.stdin.readline().strip()
            if texto == "salir":
                os.write(fd_salida, b"*** desconectado ***\n")
                os.close(fd_entrada)
                os.close(fd_salida)
                print("Saliste del chat.")
                exit(0)
            os.write(fd_salida, (texto + '\n').encode())
