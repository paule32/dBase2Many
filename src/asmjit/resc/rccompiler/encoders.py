from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import struct

from .constants import (
    CONTROL_DEFAULTS,
    RESOURCE_TYPE_NAMES,
    RT_ACCELERATOR,
    RT_BITMAP,
    RT_CURSOR,
    RT_DIALOG,
    RT_GROUP_CURSOR,
    RT_GROUP_ICON,
    RT_ICON,
    RT_MENU,
    RT_STRING,
    RT_VERSION,
)
from .model import (
    AcceleratorResource,
    DialogResource,
    FileResource,
    MenuItem,
    MenuResource,
    RawItem,
    RawResource,
    ResourceAst,
    ResourceRecord,
    ResourceUnit,
    StringTable,
    VersionBlock,
    VersionInfo,
    VersionValue,
)
from .util import (
    align,
    encode_dialog_string,
    pad_bytes,
    read_binary,
    utf16z,
)


class ResourceEncodingError(RuntimeError):
    pass


def _language(options) -> int:
    return int(options.language or 0) & 0xFFFF


def encode_raw_items(items: list[RawItem], codepage: int) -> bytes:
    output = bytearray()
    encoding = "utf-8" if codepage == 65001 else f"cp{codepage}"

    for item in items:
        if isinstance(item.value, str):
            if item.wide:
                output.extend(item.value.encode("utf-16le"))
            else:
                try:
                    output.extend(item.value.encode(encoding))
                except (LookupError, UnicodeEncodeError) as exc:
                    raise ResourceEncodingError(
                        f"could not encode raw string using codepage {codepage}: {exc}"
                    ) from exc
        elif item.dword:
            output.extend(struct.pack("<I", int(item.value) & 0xFFFFFFFF))
        else:
            output.extend(struct.pack("<H", int(item.value) & 0xFFFF))
    return bytes(output)


def encode_bitmap_file(data: bytes) -> bytes:
    if len(data) >= 14 and data[:2] == b"BM":
        # RT_BITMAP contains the DIB, without BITMAPFILEHEADER.
        return data[14:]
    return data


def parse_icon_file(data: bytes) -> list[tuple[dict[str, int], bytes]]:
    if len(data) < 6:
        raise ResourceEncodingError("truncated icon file")
    reserved, icon_type, count = struct.unpack_from("<HHH", data, 0)
    if reserved != 0 or icon_type != 1 or count == 0:
        raise ResourceEncodingError("invalid ICO header")
    if 6 + count * 16 > len(data):
        raise ResourceEncodingError("truncated ICO directory")

    result: list[tuple[dict[str, int], bytes]] = []
    for index in range(count):
        offset = 6 + index * 16
        width, height, colors, reserved_byte, planes, bit_count, size, image_offset = (
            struct.unpack_from("<BBBBHHII", data, offset)
        )
        if image_offset + size > len(data):
            raise ResourceEncodingError(f"ICO image {index} exceeds file size")
        result.append(({
            "width": width,
            "height": height,
            "colors": colors,
            "reserved": reserved_byte,
            "planes": planes,
            "bit_count": bit_count,
            "size": size,
        }, data[image_offset:image_offset + size]))
    return result


def parse_cursor_file(data: bytes) -> list[tuple[dict[str, int], bytes]]:
    if len(data) < 6:
        raise ResourceEncodingError("truncated cursor file")
    reserved, cursor_type, count = struct.unpack_from("<HHH", data, 0)
    if reserved != 0 or cursor_type != 2 or count == 0:
        raise ResourceEncodingError("invalid CUR header")
    if 6 + count * 16 > len(data):
        raise ResourceEncodingError("truncated CUR directory")

    result: list[tuple[dict[str, int], bytes]] = []
    for index in range(count):
        offset = 6 + index * 16
        width, height, colors, reserved_byte, hotspot_x, hotspot_y, size, image_offset = (
            struct.unpack_from("<BBBBHHII", data, offset)
        )
        if image_offset + size > len(data):
            raise ResourceEncodingError(f"CUR image {index} exceeds file size")
        image = data[image_offset:image_offset + size]
        planes = 1
        bit_count = 1
        pixel_width = width or 256
        pixel_height = height or 256
        if len(image) >= 16:
            header_size = struct.unpack_from("<I", image, 0)[0]
            if header_size >= 16:
                pixel_width = abs(struct.unpack_from("<i", image, 4)[0])
                dib_height = abs(struct.unpack_from("<i", image, 8)[0])
                pixel_height = max(1, dib_height // 2)
                planes, bit_count = struct.unpack_from("<HH", image, 12)
        result.append(({
            "width": pixel_width,
            "height": pixel_height,
            "colors": colors,
            "reserved": reserved_byte,
            "hotspot_x": hotspot_x,
            "hotspot_y": hotspot_y,
            "planes": planes,
            "bit_count": bit_count,
            "size": size + 4,
        }, struct.pack("<HH", hotspot_x, hotspot_y) + image))
    return result


def encode_group_icon(entries: list[tuple[dict[str, int], int]]) -> bytes:
    output = bytearray(struct.pack("<HHH", 0, 1, len(entries)))
    for meta, resource_id in entries:
        output.extend(struct.pack(
            "<BBBBHHIH",
            meta["width"] & 0xFF,
            meta["height"] & 0xFF,
            meta["colors"] & 0xFF,
            meta["reserved"] & 0xFF,
            meta["planes"] & 0xFFFF,
            meta["bit_count"] & 0xFFFF,
            meta["size"] & 0xFFFFFFFF,
            resource_id & 0xFFFF,
        ))
    return bytes(output)


def encode_group_cursor(entries: list[tuple[dict[str, int], int]]) -> bytes:
    output = bytearray(struct.pack("<HHH", 0, 2, len(entries)))
    for meta, resource_id in entries:
        output.extend(struct.pack(
            "<HHHHIH",
            meta["width"] & 0xFFFF,
            meta["height"] & 0xFFFF,
            meta["planes"] & 0xFFFF,
            meta["bit_count"] & 0xFFFF,
            meta["size"] & 0xFFFFFFFF,
            resource_id & 0xFFFF,
        ))
    return bytes(output)


def encode_string_tables(resource: StringTable) -> list[ResourceRecord]:
    groups: dict[int, list[str]] = {}
    for string_id, text in resource.entries.items():
        block_id = string_id // 16 + 1
        index = string_id % 16
        group = groups.setdefault(block_id, [""] * 16)
        group[index] = text

    records: list[ResourceRecord] = []
    for block_id, strings in sorted(groups.items()):
        data = bytearray()
        for text in strings:
            encoded = text.encode("utf-16le")
            length = len(encoded) // 2
            if length > 0xFFFF:
                raise ResourceEncodingError(
                    f"STRINGTABLE entry in block {block_id} is too long"
                )
            data.extend(struct.pack("<H", length))
            data.extend(encoded)
        records.append(ResourceRecord(
            type_id=RT_STRING,
            name_id=block_id,
            language=_language(resource.options),
            data=bytes(data),
            location=resource.location,
        ))
    return records


def _version_node(
    key: str,
    *,
    value: bytes = b"",
    value_length: int = 0,
    value_type: int = 0,
    children: list[bytes] | None = None,
) -> bytes:
    output = bytearray(b"\x00" * 6)
    output.extend(utf16z(key))
    pad_bytes(output, 4)
    output.extend(value)
    pad_bytes(output, 4)
    for child in children or []:
        output.extend(child)
        pad_bytes(output, 4)
    struct.pack_into(
        "<HHH",
        output,
        0,
        len(output) & 0xFFFF,
        value_length & 0xFFFF,
        value_type & 0xFFFF,
    )
    return bytes(output)


def _encode_version_value(value: VersionValue, parent_key: str) -> bytes:
    if parent_key.upper() == "VARFILEINFO" and value.key.upper() == "TRANSLATION":
        raw = bytearray()
        for item in value.values:
            if isinstance(item, str):
                raise ResourceEncodingError("Translation VALUE must be numeric")
            raw.extend(struct.pack("<H", int(item) & 0xFFFF))
        return _version_node(
            value.key,
            value=bytes(raw),
            value_length=len(raw),
            value_type=0,
        )

    if all(isinstance(item, str) for item in value.values):
        text = "".join(str(item) for item in value.values)
        raw = utf16z(text)
        return _version_node(
            value.key,
            value=raw,
            value_length=len(raw) // 2,
            value_type=1,
        )

    raw = bytearray()
    for item in value.values:
        if isinstance(item, str):
            raw.extend(utf16z(item))
        else:
            raw.extend(struct.pack("<I", int(item) & 0xFFFFFFFF))
    return _version_node(
        value.key,
        value=bytes(raw),
        value_length=len(raw),
        value_type=0,
    )


def _encode_version_block(block: VersionBlock) -> bytes:
    children: list[bytes] = []
    for child in block.children:
        if isinstance(child, VersionBlock):
            children.append(_encode_version_block(child))
        else:
            children.append(_encode_version_value(child, block.key))
    return _version_node(block.key, children=children)


def encode_version_info(resource: VersionInfo) -> bytes:
    fv = resource.file_version
    pv = resource.product_version
    fixed = struct.pack(
        "<13I",
        0xFEEF04BD,
        0x00010000,
        ((fv[0] & 0xFFFF) << 16) | (fv[1] & 0xFFFF),
        ((fv[2] & 0xFFFF) << 16) | (fv[3] & 0xFFFF),
        ((pv[0] & 0xFFFF) << 16) | (pv[1] & 0xFFFF),
        ((pv[2] & 0xFFFF) << 16) | (pv[3] & 0xFFFF),
        resource.file_flags_mask & 0xFFFFFFFF,
        resource.file_flags & 0xFFFFFFFF,
        resource.file_os & 0xFFFFFFFF,
        resource.file_type & 0xFFFFFFFF,
        resource.file_subtype & 0xFFFFFFFF,
        0,
        0,
    )
    children = [
        _encode_version_block(child)
        if isinstance(child, VersionBlock)
        else _encode_version_value(child, "VS_VERSION_INFO")
        for child in resource.children
    ]
    return _version_node(
        "VS_VERSION_INFO",
        value=fixed,
        value_length=len(fixed),
        value_type=0,
        children=children,
    )


def _classic_menu_items(items: list[MenuItem]) -> bytes:
    output = bytearray()
    for index, item in enumerate(items):
        flags = item.flags & 0xFFFF
        if item.popup:
            flags |= 0x0010
        if index == len(items) - 1:
            flags |= 0x0080
        if item.separator:
            flags |= 0x0800

        output.extend(struct.pack("<H", flags))
        if not item.popup:
            output.extend(struct.pack("<H", item.item_id & 0xFFFF))
        output.extend(utf16z("" if item.separator else item.text))
        if item.popup:
            output.extend(_classic_menu_items(item.children))
    return bytes(output)


def _extended_menu_items(items: list[MenuItem]) -> bytes:
    output = bytearray()
    for index, item in enumerate(items):
        pad_bytes(output, 4)
        type_flags = item.type_flags | (0x0800 if item.separator else 0)
        state_flags = item.state_flags
        resource_info = 0
        if item.popup:
            resource_info |= 0x0001
        if index == len(items) - 1:
            resource_info |= 0x0080
        output.extend(struct.pack(
            "<IIIH",
            type_flags & 0xFFFFFFFF,
            state_flags & 0xFFFFFFFF,
            item.item_id & 0xFFFFFFFF,
            resource_info & 0xFFFF,
        ))
        output.extend(utf16z("" if item.separator else item.text))
        pad_bytes(output, 4)
        if item.popup:
            output.extend(struct.pack("<I", item.help_id & 0xFFFFFFFF))
            output.extend(_extended_menu_items(item.children))
    return bytes(output)


def encode_menu(resource: MenuResource) -> bytes:
    if resource.extended:
        return struct.pack("<HHI", 1, 4, 0) + _extended_menu_items(resource.items)
    return struct.pack("<HH", 0, 0) + _classic_menu_items(resource.items)


def encode_accelerators(resource: AcceleratorResource) -> bytes:
    output = bytearray()
    for index, entry in enumerate(resource.entries):
        flags = entry.flags | (0x80 if index == len(resource.entries) - 1 else 0)
        output.extend(struct.pack(
            "<BBHHH",
            flags & 0xFF,
            0,
            entry.key & 0xFFFF,
            entry.command_id & 0xFFFF,
            0,
        ))
    return bytes(output)


def encode_dialog(resource: DialogResource) -> bytes:
    style = resource.style & 0xFFFFFFFF
    if resource.font is not None:
        style |= 0x0040

    output = bytearray()
    if resource.extended:
        output.extend(struct.pack(
            "<HHIIIHhhhh",
            1,
            0xFFFF,
            resource.help_id & 0xFFFFFFFF,
            resource.exstyle & 0xFFFFFFFF,
            style,
            len(resource.controls) & 0xFFFF,
            resource.x,
            resource.y,
            resource.width,
            resource.height,
        ))
    else:
        output.extend(struct.pack(
            "<IIHhhhh",
            style,
            resource.exstyle & 0xFFFFFFFF,
            len(resource.controls) & 0xFFFF,
            resource.x,
            resource.y,
            resource.width,
            resource.height,
        ))

    output.extend(encode_dialog_string(resource.menu))
    output.extend(encode_dialog_string(resource.window_class))
    output.extend(utf16z(resource.caption))

    if resource.font is not None:
        output.extend(struct.pack("<H", resource.font.point_size & 0xFFFF))
        if resource.extended:
            output.extend(struct.pack(
                "<HBB",
                resource.font.weight & 0xFFFF,
                resource.font.italic & 0xFF,
                resource.font.charset & 0xFF,
            ))
        output.extend(utf16z(resource.font.face))

    for control in resource.controls:
        pad_bytes(output, 4)
        if resource.extended:
            output.extend(struct.pack(
                "<IIIhhhhI",
                control.help_id & 0xFFFFFFFF,
                control.exstyle & 0xFFFFFFFF,
                control.style & 0xFFFFFFFF,
                control.x,
                control.y,
                control.width,
                control.height,
                control.control_id & 0xFFFFFFFF,
            ))
        else:
            output.extend(struct.pack(
                "<IIhhhhH",
                control.style & 0xFFFFFFFF,
                control.exstyle & 0xFFFFFFFF,
                control.x,
                control.y,
                control.width,
                control.height,
                control.control_id & 0xFFFF,
            ))
        output.extend(encode_dialog_string(control.class_id))
        output.extend(encode_dialog_string(control.text))
        output.extend(struct.pack("<H", len(control.extra_data) & 0xFFFF))
        output.extend(control.extra_data)
    return bytes(output)


class ResourceEncoder:
    def __init__(self, *, codepage: int = 65001):
        self.codepage = int(codepage)
        self.records: list[ResourceRecord] = []
        self.used_numeric_ids: dict[int, set[int]] = defaultdict(set)

    def allocate_id(self, type_id: int) -> int:
        used = self.used_numeric_ids[type_id]
        candidate = 1
        while candidate in used:
            candidate += 1
        if candidate > 0xFFFF:
            raise ResourceEncodingError(f"resource id space exhausted for type {type_id}")
        used.add(candidate)
        return candidate

    def add(self, record: ResourceRecord) -> None:
        if isinstance(record.name_id, int):
            self.used_numeric_ids[int(record.type_id) if isinstance(record.type_id, int) else -1].add(
                record.name_id
            )
        self.records.append(record)

    def encode(self, unit: ResourceUnit) -> list[ResourceRecord]:
        # Reserve explicit numeric identifiers before allocating ICON/CURSOR ids.
        for resource in unit.resources:
            if hasattr(resource, "name_id") and isinstance(resource.name_id, int):
                type_id = self.ast_type_id(resource)
                if isinstance(type_id, int):
                    self.used_numeric_ids[type_id].add(resource.name_id)

        for resource in unit.resources:
            self.encode_ast(resource)
        self.validate_duplicates()
        return self.records

    def ast_type_id(self, resource: ResourceAst):
        if isinstance(resource, FileResource):
            if isinstance(resource.type_name, int):
                return resource.type_name
            name = resource.type_name.upper()
            if name == "ICON": return RT_GROUP_ICON
            if name == "CURSOR": return RT_GROUP_CURSOR
            return RESOURCE_TYPE_NAMES.get(name, resource.type_name)
        if isinstance(resource, RawResource): return resource.type_id
        if isinstance(resource, StringTable): return RT_STRING
        if isinstance(resource, VersionInfo): return RT_VERSION
        if isinstance(resource, MenuResource): return RT_MENU
        if isinstance(resource, AcceleratorResource): return RT_ACCELERATOR
        if isinstance(resource, DialogResource): return RT_DIALOG
        raise TypeError(type(resource))

    def encode_ast(self, resource: ResourceAst) -> None:
        if isinstance(resource, FileResource):
            self.encode_file(resource)
        elif isinstance(resource, RawResource):
            self.add(ResourceRecord(
                type_id=resource.type_id,
                name_id=resource.name_id,
                language=_language(resource.options),
                data=encode_raw_items(resource.items, self.codepage),
                location=resource.location,
            ))
        elif isinstance(resource, StringTable):
            for record in encode_string_tables(resource):
                self.add(record)
        elif isinstance(resource, VersionInfo):
            self.add(ResourceRecord(
                type_id=RT_VERSION,
                name_id=resource.name_id,
                language=_language(resource.options),
                data=encode_version_info(resource),
                location=resource.location,
            ))
        elif isinstance(resource, MenuResource):
            self.add(ResourceRecord(
                type_id=RT_MENU,
                name_id=resource.name_id,
                language=_language(resource.options),
                data=encode_menu(resource),
                location=resource.location,
            ))
        elif isinstance(resource, AcceleratorResource):
            self.add(ResourceRecord(
                type_id=RT_ACCELERATOR,
                name_id=resource.name_id,
                language=_language(resource.options),
                data=encode_accelerators(resource),
                location=resource.location,
            ))
        elif isinstance(resource, DialogResource):
            self.add(ResourceRecord(
                type_id=RT_DIALOG,
                name_id=resource.name_id,
                language=_language(resource.options),
                data=encode_dialog(resource),
                location=resource.location,
            ))
        else:
            raise TypeError(f"unsupported resource AST: {type(resource).__name__}")

    def encode_file(self, resource: FileResource) -> None:
        data = read_binary(resource.filename)
        language = _language(resource.options)
        type_name = (
            resource.type_name.upper()
            if isinstance(resource.type_name, str)
            else resource.type_name
        )

        if type_name == "BITMAP":
            self.add(ResourceRecord(
                type_id=RT_BITMAP,
                name_id=resource.name_id,
                language=language,
                data=encode_bitmap_file(data),
                location=resource.location,
            ))
            return

        if type_name == "ICON":
            group_entries: list[tuple[dict[str, int], int]] = []
            for meta, image in parse_icon_file(data):
                image_id = self.allocate_id(RT_ICON)
                self.add(ResourceRecord(
                    type_id=RT_ICON,
                    name_id=image_id,
                    language=language,
                    data=image,
                    location=resource.location,
                ))
                group_entries.append((meta, image_id))
            self.add(ResourceRecord(
                type_id=RT_GROUP_ICON,
                name_id=resource.name_id,
                language=language,
                data=encode_group_icon(group_entries),
                location=resource.location,
            ))
            return

        if type_name == "CURSOR":
            group_entries = []
            for meta, image in parse_cursor_file(data):
                image_id = self.allocate_id(RT_CURSOR)
                self.add(ResourceRecord(
                    type_id=RT_CURSOR,
                    name_id=image_id,
                    language=language,
                    data=image,
                    location=resource.location,
                ))
                group_entries.append((meta, image_id))
            self.add(ResourceRecord(
                type_id=RT_GROUP_CURSOR,
                name_id=resource.name_id,
                language=language,
                data=encode_group_cursor(group_entries),
                location=resource.location,
            ))
            return

        type_id = (
            RESOURCE_TYPE_NAMES.get(type_name, type_name)
            if isinstance(type_name, str)
            else type_name
        )
        self.add(ResourceRecord(
            type_id=type_id,
            name_id=resource.name_id,
            language=language,
            data=data,
            location=resource.location,
        ))

    def validate_duplicates(self) -> None:
        seen: set[tuple[object, object, int]] = set()
        for record in self.records:
            key = (record.type_id, record.name_id, record.language)
            if key in seen:
                raise ResourceEncodingError(
                    f"duplicate resource type={record.type_id!r} "
                    f"name={record.name_id!r} language={record.language}"
                )
            seen.add(key)
