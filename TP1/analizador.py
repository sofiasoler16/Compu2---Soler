import numpy as np
import json
from collections import deque

def proceso_analizador(nombre, fifo_path, tipo_senal, cola_salida=None):
    ventana = deque(maxlen=30)  # Últimos 30 segundos

    with open(fifo_path, 'r') as fifo:
        while True:
            linea = fifo.readline()
            if not linea:
                break  # EOF o error
            try:
                dato = json.loads(linea)
                valor = extraer_valor(dato, tipo_senal)
                ventana.append(valor)
                media = np.mean(ventana)
                desv = np.std(ventana)
                resultado = {
                    "tipo": tipo_senal,
                    "timestamp": dato["timestamp"],
                    "media": round(float(media), 2),
                    "desv": round(float(desv), 2)
                }
                print(f"[{nombre}] {resultado}")
                
                if cola_salida:
                    cola_salida.put(resultado)
                    
            except Exception as e:
                print(f"[{nombre}] Error al procesar:", e)

def extraer_valor(dato, tipo):
    if tipo == "frecuencia":
        return dato["frecuencia"]
    elif tipo == "presion":
        sistolica, diastolica = dato["presion"]
        return (sistolica + diastolica) / 2  # ejemplo de simplificación
    elif tipo == "oxigeno":
        return dato["oxigeno"]
    