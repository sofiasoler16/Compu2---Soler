
# ==============================
# File: common/serialization.py
# ==============================
import base64
from datetime import datetime, timezone


def b64_png(png_bytes: bytes) -> str:
    return base64.b64encode(png_bytes).decode("ascii")


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

