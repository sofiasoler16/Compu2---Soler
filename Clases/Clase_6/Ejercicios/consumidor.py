with open('canal', 'r') as fifo:
    while True:
        linea = fifo.readline()
        if not linea:
            break
        print("Consumidor leyó:", linea.strip())
