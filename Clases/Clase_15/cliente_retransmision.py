import socket
# ejercicio 8

# nc -u -l 127.0.0.1 9007 (este es el servidor)


HOST, PORT = "127.0.0.1", 9007

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s: #crea el socket. Tipo datagrama
    s.settimeout(1.0)
    retries = 5 #lo subi de 3 a 5
    for i in range(1, retries + 1): #bucle de reintentos
        try:
            s.sendto(b"TIME", (HOST, PORT)) #envia el datagrama UDP, hace que se escriba TIME
            data, _ = s.recvfrom(2048) #la respuesta que espera es de 2048 bytes
            print("Respuesta:", data.decode()) #si llega la respuesta, la imprime
            break #si llega la respuesta, sale del bucle
        except socket.timeout: #si no llega la respuesta, entra en el except
            print(f"Timeout intento {i}; reintentando...")
    else:
        print("Sin respuesta tras reintentos")