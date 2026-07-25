from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeAlias

ResourceId: TypeAlias = int | str


@dataclass
class SourceLocation:
    filename: str
    line: int
    column: int = 0


@dataclass
class ResourceOptions:
    language: int | None = None
    characteristics: int = 0
    version: int = 0
    memory_flags: set[str] = field(default_factory=set)


@dataclass
class ResourceRecord:
    type_id: ResourceId
    name_id: ResourceId
    language: int
    data: bytes
    codepage: int = 0
    location: SourceLocation | None = None


@dataclass
class RawItem:
    value: int | str
    wide: bool = False
    dword: bool = False


@dataclass
class FileResource:
    name_id: ResourceId
    type_name: ResourceId
    filename: Path
    options: ResourceOptions
    location: SourceLocation


@dataclass
class RawResource:
    name_id: ResourceId
    type_id: ResourceId
    items: list[RawItem]
    options: ResourceOptions
    location: SourceLocation


@dataclass
class StringTable:
    entries: dict[int, str]
    options: ResourceOptions
    location: SourceLocation


@dataclass
class VersionValue:
    key: str
    values: list[int | str]


@dataclass
class VersionBlock:
    key: str
    children: list["VersionBlock | VersionValue"] = field(default_factory=list)


@dataclass
class VersionInfo:
    name_id: ResourceId
    options: ResourceOptions
    file_version: tuple[int, int, int, int] = (0, 0, 0, 0)
    product_version: tuple[int, int, int, int] = (0, 0, 0, 0)
    file_flags_mask: int = 0x3F
    file_flags: int = 0
    file_os: int = 0x00040004
    file_type: int = 1
    file_subtype: int = 0
    children: list[VersionBlock | VersionValue] = field(default_factory=list)
    location: SourceLocation | None = None


@dataclass
class MenuItem:
    text: str = ""
    item_id: int = 0
    flags: int = 0
    type_flags: int = 0
    state_flags: int = 0
    help_id: int = 0
    popup: bool = False
    separator: bool = False
    children: list["MenuItem"] = field(default_factory=list)


@dataclass
class MenuResource:
    name_id: ResourceId
    extended: bool
    items: list[MenuItem]
    options: ResourceOptions
    location: SourceLocation


@dataclass
class AcceleratorEntry:
    key: int
    command_id: int
    flags: int


@dataclass
class AcceleratorResource:
    name_id: ResourceId
    entries: list[AcceleratorEntry]
    options: ResourceOptions
    location: SourceLocation


@dataclass
class DialogFont:
    point_size: int
    face: str
    weight: int = 0
    italic: int = 0
    charset: int = 1


@dataclass
class DialogControl:
    kind: str
    text: ResourceId | str
    control_id: int
    class_id: ResourceId
    style: int
    exstyle: int
    x: int
    y: int
    width: int
    height: int
    help_id: int = 0
    extra_data: bytes = b""


@dataclass
class DialogResource:
    name_id: ResourceId
    extended: bool
    x: int
    y: int
    width: int
    height: int
    style: int = 0
    exstyle: int = 0
    caption: str = ""
    menu: ResourceId | None = None
    window_class: ResourceId | None = None
    font: DialogFont | None = None
    help_id: int = 0
    controls: list[DialogControl] = field(default_factory=list)
    options: ResourceOptions = field(default_factory=ResourceOptions)
    location: SourceLocation | None = None


ResourceAst: TypeAlias = (
    FileResource
    | RawResource
    | StringTable
    | VersionInfo
    | MenuResource
    | AcceleratorResource
    | DialogResource
)


@dataclass
class ResourceUnit:
    resources: list[ResourceAst] = field(default_factory=list)
    default_language: int = 0
