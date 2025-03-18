import sys
import getopt

def main(argv):
    nombre = ""
    edad = 0

    try:
        # Definir los argumentos esperados
        opts, args = getopt.getopt(argv, "n:e:", ["nombre=", "edad="])
    except getopt.GetoptError:
        print("Uso: getopt_demo.py -n <nombre> -e <edad>")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-n", "--nombre"):
            nombre = arg
        elif opt in ("-e", "--edad"):
            edad = int(arg)  # Convertir edad a número

    print(f"Nombre: {nombre}, Edad: {edad}")

if __name__ == "__main__":
    main(sys.argv[1:])
