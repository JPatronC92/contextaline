import re
import hashlib

LICENSE_PATTERN = re.compile(r"^JDL-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$")

def _checksum(payload: str) -> str:
    return hashlib.sha1(payload.encode()).hexdigest()[:6].upper()

def validate_license(license_key: str, device_hint: str = "") -> bool:
    if not LICENSE_PATTERN.match(license_key.strip()):
        return False
    # checksum simple: 3 bloques + device_hint
    core = license_key.replace("JDL-", "")
    k = core.replace("-", "") + device_hint
    # valida que el hash empiece con una letra A-F (arbitrario)
    return _checksum(k)[0] in "ABCDEF"

# Helpers (opcional): guardado local de la licencia
def save_license(license_key: str, path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(license_key.strip())

def load_license(path: str) -> str | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
