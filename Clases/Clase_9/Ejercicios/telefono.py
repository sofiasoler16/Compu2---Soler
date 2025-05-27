from multiprocessing import Process, BoundedSemaphore
import time
import random

MAX_CABINAS = 3
cabinas = BoundedSemaphore(MAX_CABINAS)

def get_connection_cabina(persona_id):
    """ Intenta ocupar una cabina. """
    cabinas.acquire()
    print(f"Persona {persona_id} (Cabina): Ha ocupado una cabina.")

def release_connection_cabina(persona_id):
    """ Libera una cabina """
    print(f"Persona {persona_id} (Cabina): Ha liberado la cabina.")
    cabinas.release()

def use_resource_cabina(persona_id):
    """ Simula el uso de una cabina telefónica. """
    cabina_ocupada = False
    try:
        get_connection_cabina(persona_id)
        cabina_ocupada = True
        tiempo_llamada = random.uniform(1, 5)
        print(f"Persona {persona_id} (Cabina): Hablando por {tiempo_llamada:.2f} minutos.")
        time.sleep(tiempo_llamada)

        release_connection_cabina(persona_id)
        cabina_ocupada = False

        print(f"Persona {persona_id} (Cabina): ERROR SIMULADO - intentando liberar de nuevo.")
        release_connection_cabina(persona_id)  # Esto lanza ValueError

    except ValueError:
        print(f"Persona {persona_id} (Cabina): ¡ERROR! Se intentó liberar una cabina no ocupada.")
    except Exception as e:
        print(f"Persona {persona_id} (Cabina): Error inesperado: {e}")
    finally:
        if cabina_ocupada:
            try:
                release_connection_cabina(persona_id)
                print(f"Persona {persona_id} (Cabina): Cabina liberada en finally.")
            except ValueError:
                print(f"Persona {persona_id} (Cabina): Error al liberar en finally (ya se había liberado).")

if __name__ == '__main__':
    personas = []

    for i in range(6):  # 6 personas compiten por 3 cabinas
        p = Process(target=use_resource_cabina, args=(i,))
        personas.append(p)
        p.start()

    for p in personas:
        p.join()

    print("Fin de llamadas.")