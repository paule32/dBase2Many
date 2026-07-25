from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import struct

from .resource_tree import ResourceSection

IMAGE_FILE_MACHINE_I386 = 0x014C
IMAGE_FILE_32BIT_MACHINE = 0x0100

IMAGE_SCN_CNT_INITIALIZED_DATA = 0x00000040
IMAGE_SCN_ALIGN_4BYTES = 0x00300000
IMAGE_SCN_MEM_READ = 0x40000000

IMAGE_SYM_CLASS_STATIC = 3
IMAGE_REL_I386_DIR32NB = 0x0007


@dataclass
class CoffBuildInfo:
    filename: Path
    section_size: int
    relocation_count: int
    file_size: int


def build_coff32_resource_object(section: ResourceSection) -> bytes:
    if len(section.relocation_offsets) > 0xFFFF:
        raise RuntimeError(
            "too many .rsrc relocations for a standard COFF section"
        )

    file_header_size = 20
    section_header_size = 40
    raw_pointer = file_header_size + section_header_size
    raw_data = section.data
    relocation_pointer = raw_pointer + len(raw_data)
    relocations = bytearray()

    # Symbol index zero is the .rsrc section symbol.
    for offset in section.relocation_offsets:
        if not 0 <= offset <= len(raw_data) - 4:
            raise RuntimeError(f"invalid .rsrc relocation offset: {offset}")
        relocations.extend(struct.pack(
            "<IIH",
            offset,
            0,
            IMAGE_REL_I386_DIR32NB,
        ))

    symbol_table_pointer = relocation_pointer + len(relocations)
    symbol_count = 2  # section symbol + one auxiliary section definition

    file_header = struct.pack(
        "<HHIIIHH",
        IMAGE_FILE_MACHINE_I386,
        1,
        0,  # deterministic timestamp
        symbol_table_pointer,
        symbol_count,
        0,
        IMAGE_FILE_32BIT_MACHINE,
    )

    characteristics = (
        IMAGE_SCN_CNT_INITIALIZED_DATA
        | IMAGE_SCN_ALIGN_4BYTES
        | IMAGE_SCN_MEM_READ
    )
    section_header = struct.pack(
        "<8sIIIIIIHHI",
        b".rsrc\x00\x00\x00",
        0,  # PhysicalAddress / VirtualSize in object files
        0,  # VirtualAddress
        len(raw_data),
        raw_pointer,
        relocation_pointer if relocations else 0,
        0,  # line numbers
        len(section.relocation_offsets),
        0,
        characteristics,
    )

    section_symbol = struct.pack(
        "<8sIhHBB",
        b".rsrc\x00\x00\x00",
        0,
        1,
        0,
        IMAGE_SYM_CLASS_STATIC,
        1,
    )

    # IMAGE_AUX_SYMBOL.Section definition.
    section_aux = struct.pack(
        "<IHHIhB3s",
        len(raw_data),
        len(section.relocation_offsets),
        0,
        0,
        0,
        0,
        b"\x00\x00\x00",
    )

    string_table = struct.pack("<I", 4)

    result = bytearray()
    result.extend(file_header)
    result.extend(section_header)
    result.extend(raw_data)
    result.extend(relocations)
    result.extend(section_symbol)
    result.extend(section_aux)
    result.extend(string_table)
    return bytes(result)


def write_coff32_resource_object(
    filename: str | Path,
    section: ResourceSection,
) -> CoffBuildInfo:
    path = Path(filename).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    data = build_coff32_resource_object(section)
    path.write_bytes(data)
    return CoffBuildInfo(
        filename=path,
        section_size=len(section.data),
        relocation_count=len(section.relocation_offsets),
        file_size=len(data),
    )
