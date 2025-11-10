import re
import unicodedata
import hashlib
from urllib.parse import urlparse

_SLUG_RE = re.compile(r"[^a-z0-9]+")
_DASH_RE = re.compile(r"-{2,}")

def _slugify(text: str, max_len: int = 40) -> str:
    """
    Normaliza y convierte a un slug en minúsculas [a-z0-9-].
    """
    if not text:
        return ""
    # NFKD para separar acentos y caracteres especiales
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = _SLUG_RE.sub("-", text)
    text = _DASH_RE.sub("-", text).strip("-")
    if max_len and len(text) > max_len:
        text = text[:max_len].rstrip("-")
    return text or "x"

def _domain_core(hostname: str) -> str:
    if not hostname:
        return "site"
    hostname = hostname.lower()
    if hostname.startswith("www."): #quita www
        hostname = hostname[4:]
    parts = hostname.split(".")
    if len(parts) >= 2:
        core = parts[-2]   # 'google' de 'www.google.com'
    else:
        core = parts[0]
    return _slugify(core, max_len=30)

def _path_hint(path: str) -> str:
    # Usa el primer segmento del path como hint
    if not path or path == "/":
        return ""
    seg = path.strip("/").split("/", 1)[0]
    return _slugify(seg, max_len=30)

def base_from_url(url: str) -> str:
    # Genera un 'base' amigable a partir de la URL
    try:
        u = urlparse(url)
    except Exception:
        return "task"
    core = _domain_core(u.hostname or "")
    hint = _path_hint(u.path or "")
    base = f"{core}-{hint}" if hint else core
    return base or "task"

class FriendlyIdRegistry:

    def __init__(self, max_per_base: int = 9999):
        self._counters = {}          # base -> next_int (arranca en 1)
        self._by_friendly = {}       # friendly_id -> uuid
        self._by_uuid = {}           # uuid -> friendly_id
        self._max_per_base = max_per_base

    def next_for(self, url: str, task_uuid: str) -> str:
        # Genera y persiste un friendly_id para el uuid dado.
        base = base_from_url(url)
        n = self._counters.get(base, 1)
        friendly = f"{base}{n}"

        # Si por algún motivo ya existe, probá siguientes n
        while friendly in self._by_friendly:
            n += 1
            if n > self._max_per_base:
                # fallback con sufijo hash corto
                h = hashlib.sha1(task_uuid.encode("utf-8")).hexdigest()[:4]
                friendly = f"{base}-{h}"
                break
            friendly = f"{base}{n}"

        # Persistir
        self._counters[base] = n + 1 if n <= self._max_per_base else n
        self._by_friendly[friendly] = task_uuid
        self._by_uuid[task_uuid] = friendly
        return friendly

    def resolve_friendly(self, friendly_id: str) -> str | None:
        # friendly_id -> uuid (o None si no existe).
        return self._by_friendly.get(friendly_id)

    def resolve_uuid(self, task_uuid: str) -> str | None:
        # uuid -> friendly_id (o None si no existe).
        return self._by_uuid.get(task_uuid)
