import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Procesar archivos de entrada y salida")
    parser.add_argument("-i", "--input", required=True, help="Archivo de entrada")
    parser.add_argument("-o", "--output", required=True, help="Archivo de salida")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: El archivo de entrada '{args.input}' no existe.")
        exit(1)

    print(f"Procesando archivo: {args.input} → {args.output}")

if __name__ == "__main__":
    main()