import hashlib
import json
from datetime import datetime
from collections import defaultdict

def calcular_hash(prev_hash, datos, timestamp):
    contenido = prev_hash + json.dumps(datos, sort_keys=True) + timestamp
    return hashlib.sha256(contenido.encode()).hexdigest()

def guardar_cadena(cadena):
    with open("blockchain.json", "w") as f:
        json.dump(cadena, f, indent=2)


def proceso_verificador(q_frecuencia, q_presion, q_oxigeno):
    cadena = []
    bloques_pendientes = defaultdict(dict)

    for _ in range(60):  # 60 segundos esperados
        # Recibir un dato por cada queue
        for q in [(q_frecuencia, "frecuencia"), (q_presion, "presion"), (q_oxigeno, "oxigeno")]:
            queue, tipo = q
            resultado = queue.get()
            timestamp = resultado["timestamp"]
            bloques_pendientes[timestamp][tipo] = resultado

        # Verificar si ya tenemos los 3 datos para un timestamp
        completados = [ts for ts, valores in bloques_pendientes.items() if len(valores) == 3]

        for ts in sorted(completados):
            datos = bloques_pendientes.pop(ts)
            alerta = (
                datos["frecuencia"]["media"] >= 200 or
                datos["oxigeno"]["media"] < 90 or
                datos["presion"]["media"] >= 200  # usamos promedio de sistólica y diastólica por simplicidad
            )

            prev_hash = cadena[-1]["hash"] if cadena else "0"*64
            bloque = {
                "timestamp": ts,
                "datos": datos,
                "alerta": alerta,
                "prev_hash": prev_hash,
                "hash": calcular_hash(prev_hash, datos, ts)
            }

            cadena.append(bloque)
            print(f"[Bloque {len(cadena)}] Hash: {bloque['hash']} | Alerta: {alerta}")
            guardar_cadena(cadena)