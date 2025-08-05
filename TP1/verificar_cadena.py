import hashlib
import json

def calcular_hash(prev_hash, datos, timestamp):
    contenido = prev_hash + json.dumps(datos, sort_keys=True) + timestamp
    return hashlib.sha256(contenido.encode()).hexdigest()

def verificar_cadena():
    with open("blockchain.json", "r") as f:
        cadena = json.load(f)

    errores = []
    for i in range(1, len(cadena)):
        bloque_actual = cadena[i]
        bloque_anterior = cadena[i - 1]

        # Verificar hash previo
        if bloque_actual["prev_hash"] != bloque_anterior["hash"]:
            errores.append((i, "prev_hash incorrecto"))

        # Recalcular hash
        hash_esperado = calcular_hash(
            bloque_actual["prev_hash"],
            bloque_actual["datos"],
            bloque_actual["timestamp"]
        )

        if bloque_actual["hash"] != hash_esperado:
            errores.append((i, "hash inválido"))

    if not errores:
        print("✅ La cadena es válida.")
    else:
        print("❌ Errores encontrados en la cadena:")
        for i, mensaje in errores:
            print(f"  Bloque {i}: {mensaje}")

def generar_reporte():
    with open("blockchain.json", "r") as f:
        cadena = json.load(f)

    total_bloques = len(cadena)
    alertas = 0
    suma_frec = suma_pres = suma_oxi = 0

    for bloque in cadena:
        if bloque["alerta"]:
            alertas += 1
        suma_frec += bloque["datos"]["frecuencia"]["media"]
        suma_pres += bloque["datos"]["presion"]["media"]
        suma_oxi += bloque["datos"]["oxigeno"]["media"]

    promedio_frec = round(suma_frec / total_bloques, 2)
    promedio_pres = round(suma_pres / total_bloques, 2)
    promedio_oxi = round(suma_oxi / total_bloques, 2)

    with open("reporte.txt", "w") as f:
        f.write(f"Cantidad total de bloques: {total_bloques}\n")
        f.write(f"Bloques con alerta: {alertas}\n")
        f.write(f"Promedio de frecuencia: {promedio_frec}\n")
        f.write(f"Promedio de presión: {promedio_pres}\n")
        f.write(f"Promedio de oxígeno: {promedio_oxi}\n")

    print("📄 Se generó el reporte.txt con éxito.")

# Llamar ambas funciones
if __name__ == "__main__":
    verificar_cadena()
    generar_reporte()

