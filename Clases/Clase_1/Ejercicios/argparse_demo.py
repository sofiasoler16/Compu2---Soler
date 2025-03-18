import argparse

def main():
    parser = argparse.ArgumentParser(description="Script que recibe un nombre y una edad")
    
    # Definir argumentos
    parser.add_argument("-n", "--nombre", required=True, help="Nombre de la persona")
    parser.add_argument("-e", "--edad", type=int, required=True, help="Edad de la persona")
    
    args = parser.parse_args()

    print(f"Nombre: {args.nombre}, Edad: {args.edad}")

if __name__ == "__main__":
    main()
