from __future__ import annotations

from pathlib import Path
import codecs
import struct


def align(value: int, alignment: int) -> int:
    return (value + alignment - 1) & ~(alignment - 1)


def pad_bytes(data: bytearray, alignment: int) -> None:
    data.extend(b"\x00" * ((-len(data)) % alignment))


def parse_integer_literal(text: str) -> tuple[int, bool]:
    raw = text.strip()
    suffix = ""

    while raw and raw[-1] in "uUlL":
        suffix = raw[-1] + suffix
        raw = raw[:-1]

    if raw.lower().startswith("0x"):
        value = int(raw[2:], 16)
    elif raw.lower().startswith("0o"):
        value = int(raw[2:], 8)
    elif len(raw) > 1 and raw.startswith("0") and raw.isdigit():
        value = int(raw, 8)
    else:
        value = int(raw, 10)

    return value, "l" in suffix.lower()


def decode_rc_string(token_text: str) -> tuple[str, bool]:
    wide = len(token_text) >= 2 and token_text[0] in "lL" and token_text[1] == '"'
    quoted = token_text[1:] if wide else token_text

    if len(quoted) < 2 or quoted[0] != '"' or quoted[-1] != '"':
        raise ValueError(f"invalid RC string literal: {token_text!r}")

    body = quoted[1:-1]
    result: list[str] = []
    i = 0

    escapes = {
        "a": "\a",
        "b": "\b",
        "f": "\f",
        "n": "\n",
        "r": "\r",
        "t": "\t",
        "v": "\v",
        "\\": "\\",
        '"': '"',
        "'": "'",
        "?": "?",
    }

    while i < len(body):
        ch = body[i]
        i += 1

        if ch != "\\" or i >= len(body):
            result.append(ch)
            continue

        esc = body[i]
        i += 1

        if esc in escapes:
            result.append(escapes[esc])
            continue

        if esc in "xX":
            start = i
            while i < len(body) and body[i] in "0123456789abcdefABCDEF":
                i += 1
            if i == start:
                result.append("x")
            else:
                result.append(chr(int(body[start:i], 16)))
            continue

        if esc in "01234567":
            digits = esc
            for _ in range(2):
                if i < len(body) and body[i] in "01234567":
                    digits += body[i]
                    i += 1
                else:
                    break
            result.append(chr(int(digits, 8)))
            continue

        # RC accepts escaped characters permissively.
        result.append(esc)

    return "".join(result), wide


def utf16z(text: str) -> bytes:
    return text.encode("utf-16le") + b"\x00\x00"


def encode_dialog_string(value: int | str | None) -> bytes:
    if value is None or value == "":
        return b"\x00\x00"

    if isinstance(value, int):
        return struct.pack("<HH", 0xFFFF, value & 0xFFFF)

    return utf16z(value)


def read_binary(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise RuntimeError(f"could not read resource file {path}: {exc}") from exc
