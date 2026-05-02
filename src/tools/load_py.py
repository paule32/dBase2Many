import types
import requests

from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


MODULE_URL = "https://example.com/meinmodul.py"
SIGNATURE_URL = "https://example.com/meinmodul.py.sig"


with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())


code_bytes = requests.get(MODULE_URL, timeout=10).content
sig_bytes = requests.get(SIGNATURE_URL, timeout=10).content


try:
    public_key.verify(sig_bytes, code_bytes)
except InvalidSignature:
    raise RuntimeError("Signatur ungültig! Modul wird nicht ausgeführt.")


module = types.ModuleType("meinmodul")
exec(code_bytes.decode("utf-8"), module.__dict__)


module.meine_funktion()
