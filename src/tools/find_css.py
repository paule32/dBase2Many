from pathlib import Path

ROOT = Path(".")

KEYWORDS = [
    "setStyleSheet(",
    "setPalette(",
    "QPalette(",
    ".palette(",
    "setStyle(",
    "QStyleFactory",
    "Fusion",
    "background:",
    "background-color:",
    "color:",
    "QLabel",
    "QPushButton",
    "QLineEdit",
]

for py in ROOT.rglob("*.py"):
    try:
        text = py.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue

    lines = text.splitlines()
    hits = []
    for i, line in enumerate(lines, start=1):
        if any(k in line for k in KEYWORDS):
            hits.append((i, line.strip()))

    if hits:
        print(f"\n=== {py} ===")
        for lineno, line in hits:
            print(f"{lineno:5d}: {line}")
