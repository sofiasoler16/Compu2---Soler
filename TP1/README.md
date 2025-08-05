# Trabajo Práctico: Sistema Concurrente de Análisis Biométrico con Cadena de Bloques Local
Sofía Soler – Universidad de Mendoza – Computación II

## Descripción

Este sistema simula una prueba de esfuerzo en tiempo real. Genera datos biométricos (frecuencia cardíaca, presión arterial y nivel de oxígeno) y los procesa de forma concurrente con múltiples procesos y mecanismos de IPC (FIFO y Queue). Los resultados se validan y almacenan en una cadena de bloques local (`blockchain.json`) para garantizar integridad.

---

## Requisitos

- Python **≥ 3.9**
- Módulos estándar: `multiprocessing`, `os`, `time`, `random`, `hashlib`, `json`, `datetime`, `collections`
- Módulo externo: `numpy`

### Instalar dependencias

```bash
pip install numpy
```

---

## Instrucciones para ejecución

### 1. Ejecutar el sistema principal

```bash
python3 main.py
```

Esto inicia:
- El **proceso generador** (simula datos biométricos cada segundo)
- Tres **procesos analizadores** (uno por tipo de señal)
- El **proceso verificador** (construye los bloques y los guarda)

Se generará un archivo `blockchain.json` con la cadena de bloques local.

### 2. Verificar integridad de la cadena y generar estadísticas

```bash
python3 verificar_cadena.py
```

Esto:
- Verifica que la cadena no esté corrupta (validación de hashes)
- Muestra si hay errores
- Crea un archivo `reporte.txt` con:
  - Cantidad total de bloques
  - Número de bloques con alertas
  - Promedios globales de frecuencia, presión y oxígeno



