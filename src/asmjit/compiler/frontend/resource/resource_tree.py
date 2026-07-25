from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import struct

from .model import ResourceId, ResourceRecord
from .util import align


@dataclass
class ResourceLeaf:
    record: ResourceRecord
    data_entry_offset: int = 0
    data_offset: int = 0


@dataclass
class ResourceDirectory:
    children: dict[ResourceId, "ResourceDirectory | ResourceLeaf"] = field(default_factory=dict)
    offset: int = 0


@dataclass
class ResourceSection:
    data: bytes
    relocation_offsets: list[int]


def _entry_sort_key(item: tuple[ResourceId, Any]) -> tuple[int, Any]:
    key = item[0]
    if isinstance(key, str):
        return (0, key.casefold())
    return (1, int(key))


def _directory_size(directory: ResourceDirectory) -> int:
    return 16 + len(directory.children) * 8


def build_resource_section(records: list[ResourceRecord]) -> ResourceSection:
    root = ResourceDirectory()

    for record in records:
        type_dir = root.children.setdefault(record.type_id, ResourceDirectory())
        if not isinstance(type_dir, ResourceDirectory):
            raise RuntimeError("resource type tree collision")
        name_dir = type_dir.children.setdefault(record.name_id, ResourceDirectory())
        if not isinstance(name_dir, ResourceDirectory):
            raise RuntimeError("resource name tree collision")
        if record.language in name_dir.children:
            raise RuntimeError(
                f"duplicate resource type={record.type_id!r}, "
                f"name={record.name_id!r}, language={record.language}"
            )
        name_dir.children[record.language] = ResourceLeaf(record)

    directories: list[ResourceDirectory] = []
    leaves: list[ResourceLeaf] = []

    def collect(directory: ResourceDirectory) -> None:
        directories.append(directory)
        for _, child in sorted(directory.children.items(), key=_entry_sort_key):
            if isinstance(child, ResourceDirectory):
                collect(child)
            else:
                leaves.append(child)

    collect(root)

    cursor = 0
    for directory in directories:
        directory.offset = cursor
        cursor += _directory_size(directory)

    # Store every named key exactly once. Offsets are relative to .rsrc.
    name_offsets: dict[str, int] = {}
    for directory in directories:
        for key in directory.children:
            if isinstance(key, str) and key not in name_offsets:
                cursor = align(cursor, 2)
                name_offsets[key] = cursor
                encoded = key.encode("utf-16le")
                cursor += 2 + len(encoded)

    cursor = align(cursor, 4)
    for leaf in leaves:
        leaf.data_entry_offset = cursor
        cursor += 16

    cursor = align(cursor, 4)
    for leaf in leaves:
        cursor = align(cursor, 4)
        leaf.data_offset = cursor
        cursor += len(leaf.record.data)

    output = bytearray(cursor)

    for directory in directories:
        items = sorted(directory.children.items(), key=_entry_sort_key)
        named_count = sum(isinstance(key, str) for key, _ in items)
        id_count = len(items) - named_count
        struct.pack_into(
            "<IIHHHH",
            output,
            directory.offset,
            0,  # Characteristics
            0,  # TimeDateStamp, deterministic
            0,  # MajorVersion
            0,  # MinorVersion
            named_count,
            id_count,
        )
        entry_offset = directory.offset + 16
        for key, child in items:
            if isinstance(key, str):
                name_field = 0x80000000 | name_offsets[key]
            else:
                if not 0 <= int(key) <= 0xFFFF:
                    raise RuntimeError(f"numeric resource identifier out of range: {key}")
                name_field = int(key) & 0xFFFF

            if isinstance(child, ResourceDirectory):
                child_field = 0x80000000 | child.offset
            else:
                child_field = child.data_entry_offset

            struct.pack_into(
                "<II",
                output,
                entry_offset,
                name_field,
                child_field,
            )
            entry_offset += 8

    for name, offset in name_offsets.items():
        encoded = name.encode("utf-16le")
        struct.pack_into("<H", output, offset, len(encoded) // 2)
        output[offset + 2:offset + 2 + len(encoded)] = encoded

    relocations: list[int] = []
    for leaf in leaves:
        # OffsetToData initially contains the section-relative addend. The
        # IMAGE_REL_I386_DIR32NB relocation against .rsrc turns it into an RVA.
        struct.pack_into(
            "<IIII",
            output,
            leaf.data_entry_offset,
            leaf.data_offset,
            len(leaf.record.data),
            leaf.record.codepage & 0xFFFFFFFF,
            0,
        )
        relocations.append(leaf.data_entry_offset)
        start = leaf.data_offset
        output[start:start + len(leaf.record.data)] = leaf.record.data

    return ResourceSection(
        data=bytes(output),
        relocation_offsets=relocations,
    )
