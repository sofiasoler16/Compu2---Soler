import threading

def leer():
    with open("canal_in", "r") as fifo_in:
        while True:
            msg = fifo_in.readline()
            if not msg:
                break
            print("Cliente:", msg.strip())

def escribir():
    with open("canal_out", "w") as fifo_out:
        while True:
            texto = input("Yo: ")
            fifo_out.write(texto + '\n')
            fifo_out.flush()

threading.Thread(target=leer, daemon=True).start()
escribir()
