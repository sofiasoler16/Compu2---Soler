# tests/conftest.py
import sys
from pathlib import Path

# Agrega el directorio raíz del proyecto (TP2/) al PYTHONPATH.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
