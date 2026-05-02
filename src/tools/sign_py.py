# sign py file

from cryptography.hazmat.primitives import serialization

with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=b"1234"
    )

with open("meinmodul.py", "rb") as f:
    data = f.read()

signature = private_key.sign(data)

with open("meinmodul.py.sig", "wb") as f:
    f.write(signature)
