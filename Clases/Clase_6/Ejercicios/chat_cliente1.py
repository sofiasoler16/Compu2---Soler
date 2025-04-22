import threading

def leer():
    with open("canal_out", "r") as fifo_out:
        while True:
            msg = fifo_out.readline()
            if not msg:
                break
            print("Servidor:", msg.strip())

def escribir():
    with open("canal_in", "w") as fifo_in:
        while True:
            texto = input("Yo: ")
            fifo_in.write(texto + '\n')
            fifo_in.flush()

# Hilos para lectura y escritura simultánea
threading.Thread(target=leer, daemon=True).start()
escribir()
