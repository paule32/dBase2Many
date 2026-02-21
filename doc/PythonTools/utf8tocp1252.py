from pathlib import Path

# Passe an: wo liegen die generierten hhc/hhk?
roots = [Path("out/de/html"), Path("out/en/html"), Path("out/chm")]

def to_cp1252(p: Path) -> None:
    # Doxygen schreibt meist UTF-8; wir konvertieren nach cp1252 (Windows-1252).
    data = p.read_bytes()
    text = data.decode("utf-8")  # wenn das bei dir mal knallt: errors="replace"
    p.write_bytes(text.encode("cp1252"))

for root in roots:
    if not root.exists():
        continue
    for ext in ("*.hhc", "*.hhk"):
        for f in root.rglob(ext):
            to_cp1252(f)
            print("converted:", f)
