import os
import sys
import time

def stage1(write_pipe):
    with os.fdopen(write_pipe, 'w') as pipe:
        print("Stage 1: Generando números...")
        for i in range(1, 11):
            pipe.write(f"{i}\n")
            pipe.flush()
            print(f"Stage 1: Envió {i}")
            time.sleep(0.3)

def stage2(read_pipe, write_pipe):
    with os.fdopen(read_pipe) as in_pipe, os.fdopen(write_pipe, 'w') as out_pipe:
        print("Stage 2: Calculando cuadrados...")
        for line in in_pipe:
            num = int(line.strip())
            cuadrado = num ** 2
            out_pipe.write(f"{cuadrado}\n")
            out_pipe.flush()
            print(f"Stage 2: Recibió {num}, envió {cuadrado}")
            time.sleep(0.3)

def stage3(read_pipe):
    with os.fdopen(read_pipe) as pipe:
        total = 0
        print("Stage 3: Sumando cuadrados...")
        for line in pipe:
            num = int(line.strip())
            total += num
            print(f"Stage 3: Recibió {num}, suma parcial = {total}")
            time.sleep(0.3)
        print(f"Stage 3: Resultado final = {total}")

def main():
    # Crear pipe A (Stage 1 → Stage 2) y pipe B (Stage 2 → Stage 3)
    a_r, a_w = os.pipe()
    b_r, b_w = os.pipe()

    pid1 = os.fork()
    if pid1 == 0:
        os.close(a_r)
        os.close(b_r)
        os.close(b_w)
        stage1(a_w)
        sys.exit(0)

    pid2 = os.fork()
    if pid2 == 0:
        os.close(a_w)
        os.close(b_r)
        stage2(a_r, b_w)
        sys.exit(0)

    # Proceso principal ejecuta Stage 3
    os.close(a_r)
    os.close(a_w)
    os.close(b_w)
    stage3(b_r)

    os.waitpid(pid1, 0)
    os.waitpid(pid2, 0)
    print("Pipeline completado.")

if __name__ == "__main__":
    main()
