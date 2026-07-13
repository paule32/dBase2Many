# ---------------------------------------------------------------------------
# File: pe32.py - writer for pe32
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

from compiler.common.constants import *
from compiler.writer.nt32      import *

import struct
import os
from dataclasses import dataclass

def double_to_bits(value):
    return struct.unpack(
        "<Q",
        struct.pack("<d", float(value))
    )[0]

# ---------------------------------------------------------------------------
# members used to include external coff32 .a rchive files into the exe image:
# ---------------------------------------------------------------------------
class ArMember:
    def __init__(self, name, data, offset=0):
        self.name = name
        self.data = data
        self.offset = offset

        self.loaded = False
        self.defined_symbols = []

class ArArchiveReader:
    MAGIC = b"!<arch>\n"

    def __init__(self, filename=None):
        self.filename = filename
        self.members = []
        self.long_names = b""
        self.symbol_index = {}

    @classmethod
    def read(cls, filename):
        ar = cls(filename)

        with open(filename, "rb") as f:
            data = f.read()

        if not data.startswith(cls.MAGIC):
            raise RuntimeError(f"not an ar archive: {filename}")

        pos = len(cls.MAGIC)

        while pos + 60 <= len(data):
            header = data[pos:pos + 60]
            member_offset = pos
            pos += 60

            raw_name = header[0:16].decode("ascii", errors="replace")
            raw_size = header[48:58].decode("ascii", errors="replace").strip()

            if not raw_size:
                break

            size = int(raw_size)

            member_data = data[pos:pos + size]
            pos += size

            if pos & 1:
                pos += 1

            name = ar.decode_member_name(raw_name)

            if name == "//":
                ar.long_names = member_data
                continue

            if name == "/":
                continue

            member = ArMember(
                name=name,
                data=member_data,
                offset=member_offset
            )

            ar.members.append(member)

        return ar

    def decode_member_name(self, raw_name):
        name = raw_name.strip()

        if name == "/":
            return "/"

        if name == "//":
            return "//"

        if name.startswith("/") and name[1:].isdigit():
            return self.get_long_name(int(name[1:]))

        if name.endswith("/"):
            name = name[:-1]

        return name

    def get_long_name(self, offset):
        if not self.long_names:
            return f"/{offset}"

        end = self.long_names.find(b"\n", offset)

        if end < 0:
            end = len(self.long_names)

        name = self.long_names[offset:end]
        name = name.rstrip(b"/")
        name = name.rstrip(b"\r\n")

        return name.decode("ascii", errors="replace")

    def build_symbol_index(self, coff_reader_class):
        self.symbol_index.clear()

        for member in self.members:
            try:
                coff = coff_reader_class.from_bytes(member.data)
            except Exception:
                continue

            symbols = coff.get_defined_symbols()

            member.defined_symbols = symbols

            for sym in symbols:
                self.symbol_index.setdefault(sym, []).append(member)

    def find_members_for_symbol(self, symbol):
        return self.symbol_index.get(symbol, [])

# ---------------------------------------------------------------------------
# members used to include external coff32 .o bject files into exe image link:
# ---------------------------------------------------------------------------
class Coff32Relocation:
    def __init__(self, virtual_address, symbol_index, rel_type):
        self.virtual_address = virtual_address
        self.symbol_index = symbol_index
        self.type = rel_type

class Coff32Object:
    def __init__(self):
        self.sections        = []
        self.symbols         = {}
        self.relocations     = []
        self.raw_symbols     = []
        self.string_table    = b""
    
    def get_defined_symbols(self):
        result = []

        for sym in self.symbols.values():
            if not sym.name:
                continue
             
            if sym.section_number > 0:
                result.append(sym.name)

        return result

    def get_undefined_symbols(self):
        result = []

        for sym in self.symbols.values():
            if not sym.name:
                continue

            if sym.section_number == 0:
                result.append(sym.name)

        return result

class Coff32Section:
    def __init__(self, name, data, characteristics):
        self.name            = name
        self.data            = bytearray(data)
        self.characteristics = characteristics
        self.relocations     = []
        self.output_section  = None
        self.output_offset   = 0
        self.rva             = 0

class Coff32Symbol:
    def __init__(self, name, section_number, value, storage_class):
        self.name            = name
        self.section_number  = section_number
        self.value           = value
        self.storage_class   = storage_class
        self.resolved_rva    = None

# ---------------------------------------------------------------------------
# Windows NT 3.5 PE COFF object/code reader
# ---------------------------------------------------------------------------
class Coff32Reader:
    def __init__(self, filename):
        self.filename     = filename
        self.data         = None
        self.obj          = Coff32Object()
        self.string_table = b""

    @classmethod
    def from_bytes(cls, data):
        reader = cls(None)
        reader.data = data

        reader.read_header()
        reader.read_sections()
        reader.read_symbols()

        return reader.obj
    
    def read(self):
        with open(self.filename, "rb") as f:
            self.data = f.read()

        self.read_header()
        self.read_sections()
        self.read_symbols()

        return self.obj

    def read_header(self):
        (
            self.machine,
            self.number_of_sections,
            self.time_date_stamp,
            self.pointer_to_symbol_table,
            self.number_of_symbols,
            self.size_of_optional_header,
            self.characteristics
        ) = struct.unpack_from("<HHLLLHH", self.data, 0)

        if self.machine != 0x014C:
            raise RuntimeError("not a COFF32 i386 object file")

        if self.size_of_optional_header != 0:
            raise RuntimeError("COFF object should not have optional header")

    def section_name(self, raw):
        raw = raw.rstrip(b"\x00")
        return raw.decode("ascii", errors="replace")

    def read_sections(self):
        offset = 20

        for i in range(self.number_of_sections):
            (
                raw_name,
                virtual_size,
                virtual_address,
                size_of_raw_data,
                pointer_to_raw_data,
                pointer_to_relocations,
                pointer_to_linenumbers,
                number_of_relocations,
                number_of_linenumbers,
                characteristics
            ) = struct.unpack_from("<8sLLLLLLHHL", self.data, offset)

            name = self.section_name(raw_name)

            section_data = b""
            if size_of_raw_data:
                section_data = self.data[
                    pointer_to_raw_data:
                    pointer_to_raw_data + size_of_raw_data
                ]

            sec = Coff32Section(name, section_data, characteristics)

            for r in range(number_of_relocations):
                roff = pointer_to_relocations + r * 10

                (
                    virtual_address,
                    symbol_index,
                    rel_type
                ) = struct.unpack_from("<LLH", self.data, roff)

                sec.relocations.append(
                    Coff32Relocation(
                        virtual_address,
                        symbol_index,
                        rel_type
                    )
                )

            self.obj.sections.append(sec)
            offset += 40

    def get_string_from_table(self, offset):
        start = offset
        end = self.string_table.find(b"\x00", start)

        if end < 0:
            end = len(self.string_table)

        return self.string_table[start:end].decode("ascii", errors="replace")

    def symbol_name(self, raw_name):
        first4, second4 = struct.unpack("<LL", raw_name)

        if first4 == 0:
            return self.get_string_from_table(second4)

        return raw_name.rstrip(b"\x00").decode("ascii", errors="replace")

    def read_symbols(self):
        symtab = self.pointer_to_symbol_table
        strtab_offset = symtab + self.number_of_symbols * 18

        if strtab_offset + 4 <= len(self.data):
            size = struct.unpack_from("<L", self.data, strtab_offset)[0]
            self.string_table = self.data[strtab_offset:strtab_offset + size]
        else:
            self.string_table = b"\x04\x00\x00\x00"

        i = 0

        while i < self.number_of_symbols:
            off = symtab + i * 18

            raw_name = self.data[off:off + 8]

            (
                value,
                section_number,
                symbol_type,
                storage_class,
                number_of_aux_symbols
            ) = struct.unpack_from("<LhHBB", self.data, off + 8)

            name = self.symbol_name(raw_name)

            sym = Coff32Symbol(
                name,
                section_number,
                value,
                storage_class
            )

            self.obj.raw_symbols.append(sym)

            if name:
                self.obj.symbols[name] = sym

            for _ in range(number_of_aux_symbols):
                i += 1
                self.obj.raw_symbols.append(None)

            i += 1

# ---------------------------------------------------------------------------
# Export description used by the PE32 image writer.
# ---------------------------------------------------------------------------
@dataclass
class PE32Export:
    name: str
    target_label: str
    ordinal: int | None = None

# ---------------------------------------------------------------------------
# Windows NT 3.5 PE COFF object/code writer
# ---------------------------------------------------------------------------
class PE32Writer:
    def __init__(self):
        self.regs = {
            "eax": 0,
            "ecx": 1,
            "edx": 2,
            "ebx": 3,
            "esp": 4,
            "ebp": 5,
            "esi": 6,
            "edi": 7,
        }
        
        self.text = bytearray()
        self.data = bytearray()

        self.labels = {}
        self.fixups = []

        self.symbols = []
        self.text_relocations = []
        self.data_relocations = []

        self.string_table = bytearray()
        self.string_offsets = {}
        
        self.image_kind = "exe"
        self.image_name = None

        self.exports: list[PE32Export] = []

        # Optionaler DLL-Einstiegspunkt.
        # None bedeutet AddressOfEntryPoint = 0.
        self.dll_entry_label: str | None = None
        
        # search path's:
        #self.link_object_files  = []
        #self.link_archive_files = []
        
        #self.library_paths      = ["."]
        #self.object_paths       = ["."]

        # external .o bject file's
        self.coff_objects       = []
        
        # external .a rchive file's
        self.archive_files      = []
        self.archives           = []
    
    def map_reg32(self, reg):
        reg_map = {
            "rax" : "eax", "eax": "eax",
            "rbx" : "ebx", "ebx": "ebx",
            "rcx" : "ecx", "ecx": "ecx",
            "rdx" : "edx", "edx": "edx",
            "rbp" : "ebp", "ebp": "ebp",
            "rsp" : "esp", "esp": "esp",
            "rsi" : "esi", "esi": "esi",
            "rdi" : "edi", "edi": "edi",
            
            "r8"  : "ecx",
            "r8d" : "ecx",
            "r9"  : "edx",
            "r9d" : "edx",

            "r10" : "edi",
            "r10d": "edi",
            "r11" : "ebx",
            "r11d": "ebx",
            
            "r12" : "esi",
        }
        
        if reg not in reg_map:
            raise RuntimeError(f"{tr('unsupported NT32 register')}: {reg}")
        
        return reg_map[reg]
    
    def archive_name_candidates(self, name):
        name = self.normalize_link_path(name)

        directory = os.path.dirname(name)
        base      = os.path.basename(name)

        root, ext = os.path.splitext(base)

        candidates = []

        def add_candidate(filename):
            full = os.path.join(directory, filename) if directory else filename

            if full not in candidates:
                candidates.append(full)

        if ext:
            add_candidate(base)

            if not root.startswith("lib"):
                add_candidate("lib" + root + ext)
        else:
            add_candidate(base + ".a")

            if base.startswith("lib"):
                add_candidate(base + ".a")
            else:
                add_candidate("lib" + base + ".a")

        return candidates
    
    def resolve_link_archive_name(self, name):
        name       = self.normalize_link_path(name)
        candidates = self.archive_name_candidates(name)

        # absolute oder mit Pfad
        if os.path.isabs(name) or os.path.dirname(name):
            for candidate in candidates:
                if os.path.exists(candidate):
                    return candidate

            raise RuntimeError(
                "archive file not found: " + ", ".join(candidates)
            )

        # Suchpfade
        for path in CDATA.link_library_paths:
            for candidate in candidates:
                full = os.path.join(path, candidate)

                if os.path.exists(full):
                    return full

        raise RuntimeError(
            "archive file not found: " + ", ".join(candidates)
        )

    def resolve_archive_objects(self):
        self.load_archives()

        changed = True

        while changed:
            changed = False

            unresolved = self.collect_unresolved_symbols()

            if not unresolved:
                break

            for archive in self.archives:
                for symbol in list(unresolved):
                    members = archive.find_members_for_symbol(symbol)

                    for member in members:
                        if member.loaded:
                            continue

                        obj = Coff32Reader.from_bytes(member.data)

                        self.add_coff_object(obj)

                        member.loaded = True
                        changed = True
    
    def normalize_link_path(self, name):
        name = name.strip()

        if (
            (name.startswith("'") and name.endswith("'")) or
            (name.startswith('"') and name.endswith('"'))
        ):
            name = name[1:-1]

        name = name.replace("\\", os.sep).replace("/", os.sep)

        return os.path.normpath(name)

    def add_object_search_path(self, path):
        path = self.normalize_link_path(path)

        if path not in CDATA.link_object_paths:
            CDATA.link_object_paths.append(path)

    def add_library_search_path(self, path):
        path = self.normalize_link_path(path)

        if path not in CDATA.link_library_paths:
            CDATA.link_library_paths.append(path)

    def add_link_object(self, name):
        filename = self.resolve_link_object_name(name)

        if filename not in CDATA.link_object_files:
            CDATA.link_object_files.append(filename)

    def add_link_archive(self, name):
        filename = self.resolve_link_archive_name(name)

        if filename not in CDATA.link_archive_files:
            CDATA.link_archive_files.append(filename)
            self.add_archive_file(filename)
    
    def add_archive_file(self, filename):
        self.archive_files.append(filename)

    def add_coff_object(self, source):
        if isinstance(source, Coff32Object):
            obj = source
        else:
            obj = Coff32Reader(source).read()

        self.coff_objects.append(obj)
        return obj
    
    def resolve_link_object_name(self, name):
        name      = self.normalize_link_path(name)
        root, ext = os.path.splitext(name)

        if not ext:
            name = name + ".o"

        # absolute oder explizite Pfadangabe
        if os.path.isabs(name) or os.path.dirname(name):
            if os.path.exists(name):
                return name

            raise RuntimeError(f"object file not found: {name}")

        # Suchpfade
        for path in CDATA.link_object_paths:
            candidate = os.path.join(path, name)

            if os.path.exists(candidate):
                return candidate

        raise RuntimeError(f"object file not found: {name}")
    
    def load_archives(self):
        self.archives = []

        for filename in self.archive_files:
            ar = ArArchiveReader.read(filename)
            ar.build_symbol_index(Coff32Reader)
            self.archives.append(ar)
    
    def section_rva(self, name):
        if name == ".text":
            return self.text_rva

        if name in [".data", ".rdata"]:
            return self.data_rva

        raise RuntimeError(f"unknown output section: {name}")
        
    def include_coff_objects(self):
        for obj in self.coff_objects:
            for sec in obj.sections:
                if sec.name == ".text":
                    sec.output_section = ".text"
                    sec.output_offset  = len(self.text)
                    self.text         += sec.data
                
                elif sec.name in [".data", ".rdata"]:
                    sec.output_section = ".data"
                    sec.output_offset  = len(self.data)
                    self.data         += sec.data
                
                elif sec.name == ".bss":
                    sec.output_section = ".bss"
                    sec.output_offset  = self.bss_size
                    self.bss_size     += len(sec.data)
    
    def add_symbol_alias(self, alias_name, target_name):
        target_index = self.find_symbol_index(target_name)

        if target_index is None:
            raise RuntimeError(f"alias target symbol not found: {target_name}")

        target = self.symbols[target_index]

        if self.find_symbol_index(alias_name) is None:
            self.add_symbol(
                name=alias_name,
                value=target["value"],
                section_number=target["section"]
            )
    
    def collect_defined_symbols(self):
        defined = set()

        for obj in self.coff_objects:
            for sym in obj.get_defined_symbols():
                defined.add(sym)

        for sym in self.symbols:
            if isinstance(sym, dict):
                if sym.get("section", 0) > 0:
                    defined.add(sym.get("name"))

        return defined
    
    def collect_unresolved_symbols(self):
        defined = self.collect_defined_symbols()
        unresolved = set()

        for obj in self.coff_objects:
            for sym in obj.get_undefined_symbols():
                if sym not in defined:
                    unresolved.add(sym)

        for sym in self.symbols:
            if isinstance(sym, dict):
                name = sym.get("name")
                section = sym.get("section", 0)

                if section == 0 and name not in defined:
                    unresolved.add(name)

        return unresolved
    
    def begin_function(self, name, local_size=0, public=True):
        offset = len(self.text)

        self.bind_label(name)

        if self.find_symbol_index(name) is None:
            self.add_symbol(
                name=name,
                value=offset,
                section_number=1
            )

        # Für NT32 erst schlicht:
        # push ebp
        # mov  ebp, esp
        self.emit_push_reg32("ebp")
        self.emit_mov_reg_reg32("ebp", "esp")

        if local_size:
            self.emit_sub_reg_imm32("esp", local_size)

        return offset
    
    def end_function(self):
        self.emit_mov_reg_reg32("esp", "ebp")
        self.emit_pop_reg32("ebp")
        self.emit_ret()

    @property
    def is_dll(self) -> bool:
        return self.image_kind == "dll"

    def configure_dll(
        self,
        filename: str,
        entry_label: str | None = None
    ) -> None:
        filename  = os.path.abspath (filename)
        root, ext = os.path.splitext(filename)

        if ext.lower() != ".dll":
            filename = root + ".dll"
        
        self.image_kind = "dll"
        self.image_name = os.path.basename(filename)
        self.dll_entry_label = entry_label

    def add_export(
        self,
        name: str,
        target_label: str,
        ordinal: int | None = None
    ) -> None:
        if not name:
            raise ValueError("export name must not be empty")

        if ordinal is not None and ordinal < 1:
            raise ValueError("export ordinal must be >= 1")

        for item in self.exports:
            if item.name == name:
                raise ValueError(f"duplicate export name: {name}")

            if (
                ordinal is not None and
                item.ordinal is not None and
                item.ordinal == ordinal
            ):
                raise ValueError(
                    f"duplicate export ordinal: {ordinal}"
                )

        self.exports.append(
            PE32Export(
                name=name,
                target_label=target_label,
                ordinal=ordinal
            )
        )

    def _reg_id(self, reg):
        if reg not in self.regs:
            raise RuntimeError(f"{tr('unsupported 32-bit register')}: {reg}")
        return self.regs[reg]

    def bind_label(self, name):
        self.labels[name] = len(self.text)
        
        idx = self.find_symbol_index(name)
        if idx is None:
            self.add_symbol(name, len(self.text), section_number=1)
        else:
            self.symbols[idx]["value"] = len(self.text)
            self.symbols[idx]["section"] = 1

        pending = [
            f for f in self.fixups
            if f["label"] == name
        ]

        for fix in pending:
            self.patch_rel32(
                fix["patch_pos"],
                self.labels[name]
            )

        self.fixups = [
            f for f in self.fixups
            if f["label"] != name
        ]

    def patch_rel32(self, patch_pos, target_pos):
        rel = target_pos - (patch_pos + 4)
        self.text[patch_pos:patch_pos + 4] = int(rel).to_bytes(
            4,
            "little",
            signed=True
        )

    def emit_push_imm32(self, value):
        self.text.append(0x68)
        self.text += int(value).to_bytes(4, "little", signed=True)
        
    def emit_mov_data_label_r8(self, label, reg8):
        if reg8.lower() != "al":
            raise ValueError("emit_mov_data_label_r8 supports only AL")

        # Byte/Word vorerst über 32-bit Store ablegen.
        # Da Byte/Word in .data klein angelegt sind, besser unten add_data_i32 nutzen.
        self.emit_mov_data_label_r32(label, "eax")

    def emit_mov_data_label_r16(self, label, reg16):
        if reg16.lower() != "ax":
            raise ValueError("emit_mov_data_label_r16 supports only AX")

        self.emit_mov_data_label_r32(label, "eax")

    def emit_movsd_data_label_xmm0_store(self, label):
        self.emit_lea_reg_data_label("edx", label)
        self.emit_movsd_store32("edx", 0, "xmm0")

    def emit_push_reg32(self, reg):
        reg_id = self._reg_id(reg)
        self.text.append(0x50 + reg_id)

    def emit_pop_reg32(self, reg):
        reg_id = self._reg_id(reg)
        self.text.append(0x58 + reg_id)

    def emit_mov_reg_imm32(self, reg, value):
        reg_id = self._reg_id(reg)
        self.text.append(0xB8 + reg_id)
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_xor_reg_reg(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        self.text.append(0x31)
        self.text.append(0xC0 | (src_id << 3) | dst_id)

    def emit_ret(self):
        self.text.append(0xC3)

    def emit_ret_imm16(self, stack_bytes):
        stack_bytes = int(stack_bytes)

        if not 0 <= stack_bytes <= 0xFFFF:
            raise ValueError("RET stack size must fit into uint16")

        self.text.append(0xC2)
        self.text += stack_bytes.to_bytes(2, "little", signed=False)

    def emit_call_label(self, label):
        self.text.append(0xE8)

        patch_pos = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        if label in self.labels:
            self.patch_rel32(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })
    
    def emit_movapd32(self, dst, src):
        dst_id = self._xmm_id(dst)
        src_id = self._xmm_id(src)

        # movapd xmm, xmm
        self.text += b"\x66\x0F\x28"
        self.text.append(0xC0 | (dst_id << 3) | src_id)
    
    def emit_jmp(self, label):
        self.text.append(0xE9)

        patch_pos = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        if label in self.labels:
            self.patch_rel32(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })

    def emit_mov_byte_ptr_reg8(self, base, offset, src):
        reg32 = {
            "eax": 0,
            "ecx": 1,
            "edx": 2,
            "ebx": 3,
            "esp": 4,
            "ebp": 5,
            "esi": 6,
            "edi": 7,
        }

        reg8 = {
            "al": 0,
            "cl": 1,
            "dl": 2,
            "bl": 3,
        }

        if base not in reg32:
            raise RuntimeError(f"unsupported base register: {base}")

        if src not in reg8:
            raise RuntimeError(f"unsupported 8-bit src register: {src}")

        # mov byte ptr [base+offset], src
        self.text += b"\x88"

        if offset == 0 and base != "ebp":
            self.text.append(0x00 | (reg8[src] << 3) | reg32[base])
        elif -128 <= int(offset) <= 127:
            self.text.append(0x40 | (reg8[src] << 3) | reg32[base])
            self.text.append(int(offset) & 0xFF)
        else:
            self.text.append(0x80 | (reg8[src] << 3) | reg32[base])
            self.text += int(offset).to_bytes(4, "little", signed=True)

    def emit_movzx_r32_byte_ptr(self, dst, base, offset=0):
        reg = {
            "eax": 0,
            "ecx": 1,
            "edx": 2,
            "ebx": 3,
            "esp": 4,
            "ebp": 5,
            "esi": 6,
            "edi": 7,
        }

        if dst not in reg:
            raise RuntimeError(f"unsupported dst register: {dst}")

        if base not in reg:
            raise RuntimeError(f"unsupported base register: {base}")

        # movzx r32, byte ptr [base+disp]
        self.text += b"\x0F\xB6"

        if offset == 0 and base != "ebp":
            self.text.append(0x00 | (reg[dst] << 3) | reg[base])
        elif -128 <= int(offset) <= 127:
            self.text.append(0x40 | (reg[dst] << 3) | reg[base])
            self.text.append(int(offset) & 0xFF)
        else:
            self.text.append(0x80 | (reg[dst] << 3) | reg[base])
            self.text += int(offset).to_bytes(4, "little", signed=True)

    def emit_jcc(self, cc, label):
        opcodes = {
            "je":  b"\x0F\x84",
            "jne": b"\x0F\x85",
            "jl":  b"\x0F\x8C",
            "jle": b"\x0F\x8E",
            "jg":  b"\x0F\x8F",
            "jge": b"\x0F\x8D",

            "jb":  b"\x0F\x82",
            "jbe": b"\x0F\x86",
            "ja":  b"\x0F\x87",
            "jae": b"\x0F\x83",
        }

        if cc not in opcodes:
            raise RuntimeError(f"{tr('unsupported PE32 condition jump')}: {cc}")

        self.text += opcodes[cc]

        patch_pos = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        if label in self.labels:
            self.patch_rel32(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })

    def emit_jcc(self, cc, label):
        opcodes = {
            "je":  b"\x0F\x84",
            "jne": b"\x0F\x85",
            "jl":  b"\x0F\x8C",
            "jle": b"\x0F\x8E",
            "jg":  b"\x0F\x8F",
            "jge": b"\x0F\x8D",

            "jb":  b"\x0F\x82",
            "jbe": b"\x0F\x86",
            "ja":  b"\x0F\x87",
            "jae": b"\x0F\x83",
        }

        if cc not in opcodes:
            raise RuntimeError(f"{tr('unsupported PE32 condition jump')}: {cc}")

        self.text += opcodes[cc]

        patch_pos = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        if label in self.labels:
            self.patch_rel32(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })


    def emit_jb(self, label):  self.emit_jcc("jb", label)
    def emit_jbe(self, label): self.emit_jcc("jbe", label)
    def emit_ja(self, label):  self.emit_jcc("ja", label)
    def emit_jae(self, label): self.emit_jcc("jae", label)

    def emit_je (self, label): self.emit_jcc("je",  label)
    def emit_jne(self, label): self.emit_jcc("jne", label)
    def emit_jl (self, label): self.emit_jcc("jl",  label)
    def emit_jle(self, label): self.emit_jcc("jle", label)
    def emit_jg (self, label): self.emit_jcc("jg",  label)
    def emit_jge(self, label): self.emit_jcc("jge", label)
    
    def emit_call_external(self, symbol_name):
        #if symbol_name in self.labels:
        #    return self.emit_call_label(symbol_name)
        if symbol_name == "_main":
            return self.emit_call_label(symbol_name)
        
        if symbol_name in ["rax", "eax", "rbx", "ebx", "rcx", "ecx", "rdx", "edx"]:
            raise RuntimeError(f"{tr('register passed to emit_call_external')}: {symbol_name}")
        
        sym_index = self.find_or_add_external(symbol_name)

        self.text.append(0xE8)          # call rel32
        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_REL32
        })

    def add_symbol(self, name, value, section_number=1):
        self.symbols.append({
            "name": name,
            "value": value,
            "section": section_number,
            "type": 0x20,
            "storage": IMAGE_SYM_CLASS_EXTERNAL,
            "aux": 0
        })

    def add_external_symbol(self, name):
        index = len(self.symbols)

        self.symbols.append({
            "name": name,
            "value": 0,
            "section": 0,
            "type": 0,
            "storage": IMAGE_SYM_CLASS_EXTERNAL,
            "aux": 0
        })

        return index

    def find_or_add_symbol(self, name):
        index = self.find_symbol_index(name)

        if index is None:
            raise RuntimeError(f"{tr('Symbol not defined')}: {name}")

        return index

    def find_or_add_external(self, name):
        for index, sym in enumerate(self.symbols):
            if sym["name"] == name:
                return index

        return self.add_external_symbol(name)

    def add_data_string(self, name, text):
        offset = len(self.data)
        self.data += text.encode("ascii", errors="replace") + b"\x00"

        self.add_symbol(
            name=name,
            value=offset,
            section_number=2
        )

        return offset

    def add_data_i32(self, name, value=0):
        return self.add_data_bytes(
            name,
            int(value).to_bytes(4, "little", signed=True),
            alignment=4
        )

    def add_data_zeros(self, name, size, alignment=4):
        return self.add_data_bytes(
            name,
            b"\x00" * size,
            alignment=alignment
        )

    def align_data(self, alignment):
        while len(self.data) % alignment != 0:
            self.data.append(0)

    def add_data_bytes(self, name, data_bytes, alignment=1):
        self.align_data(alignment)

        offset = len(self.data)
        self.data += data_bytes

        self.add_symbol(
            name=name,
            value=offset,
            section_number=2
        )

        return offset
    
    def emit_mov_reg_reg32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        # mov r/m32, r32
        self.text.append(0x89)
        self.text.append(0xC0 | (src_id << 3) | dst_id)
    
    def emit_sub_reg_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        # sub r/m32, imm32
        self.text.append(0x81)
        self.text.append(0xE8 | reg_id)
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_sub_reg_reg32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        # sub r/m32, r32
        self.text.append(0x29)
        self.text.append(0xC0 | (src_id << 3) | dst_id)

    def emit_add_reg_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        # add r/m32, imm32
        self.text.append(0x81)
        self.text.append(0xC0 | reg_id)
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_add_reg_reg32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        # add r/m32, r32
        self.text.append(0x01)
        self.text.append(0xC0 | (src_id << 3) | dst_id)

    def find_symbol_index(self, name):
        for index, sym in enumerate(self.symbols):
            if sym["name"] == name:
                return index

        return None

    def emit_ucomisd32(self, left, right):
        left_id  = self._xmm_id(left)
        right_id = self._xmm_id(right)

        # 66 0F 2E /r
        self.text += b"\x66\x0F\x2E"
        self.text.append(0xC0 | (left_id << 3) | right_id)
    
    def emit_mov_reg_data_label32(self, reg, label):
        reg_id    = self._reg_id(reg)
        sym_index = self.find_or_add_symbol(label)

        # mov r32, imm32
        self.text.append(0xB8 + reg_id)

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_DIR32
        })

    def _emit_modrm_mem32(self, reg_id, base_id, offset=0):
        rm = base_id & 7

        needs_sib  = rm == 4          # esp
        needs_disp = rm == 5 and offset == 0  # ebp braucht disp8=0

        if offset == 0 and not needs_disp:
            mod = 0x00
        elif -128 <= offset <= 127:
            mod = 0x40
        else:
            mod = 0x80

        if needs_disp:
            mod = 0x40
            offset = 0

        if needs_sib:
            self.text.append(mod | ((reg_id & 7) << 3) | 0x04)
            self.text.append(0x24)  # scale=0,index=none,base=esp
        else:
            self.text.append(mod | ((reg_id & 7) << 3) | rm)

        if mod == 0x40:
            self.text.append(offset & 0xFF)
        elif mod == 0x80:
            self.text += int(offset).to_bytes(4, "little", signed=True)
    
    def emit_mov_mem_reg32(self, base, offset, src):
        base_id = self._reg_id(base)
        src_id  = self._reg_id(src)

        self.text.append(0x89)  # mov r/m32, r32
        self._emit_modrm_mem32(src_id, base_id, offset)
    
    def emit_mov_mem_reg32(self, base, offset, src):
        base_id = self._reg_id(base)
        src_id  = self._reg_id(src)

        self.text.append(0x89)
        self._emit_modrm_mem32(src_id, base_id, offset)
    
    def emit_mov_reg_mem32(self, dst, base, offset=0):
        dst_id  = self._reg_id(dst)
        base_id = self._reg_id(base)

        self.text.append(0x8B)  # mov r32, r/m32
        self._emit_modrm_mem32(dst_id, base_id, offset)
    
    def emit_mov_data_label_r32(self, label, src):
        src_id    = self._reg_id(src)
        sym_index = self.find_or_add_symbol(label)

        # mov r/m32, r32
        # absoluter Speicherzugriff: [imm32]
        self.text.append(0x89)
        self.text.append(0x05 | ((src_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_DIR32
        })
    
    def emit_mov_r32_data_label(self, dst, label):
        return self.emit_mov_reg_data_label32(dst, label)
    
    def emit_imul_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        # imul r32, r/m32
        self.text += b"\x0F\xAF"
        self.text.append(0xC0 | (dst_id << 3) | src_id)

    def emit_imul_r32_r32_imm32(self, dst, src, value):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        # imul r32, r/m32, imm32
        self.text.append(0x69)
        self.text.append(0xC0 | (dst_id << 3) | src_id)
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_imul(self, dst, src, value=None):
        if value is None:
            self.emit_imul_r32_r32(dst, src)
        else:
            self.emit_imul_r32_r32_imm32(dst, src, value)
    
    def emit_cdq(self):
        # CDQ: EDX:EAX vorbereiten für IDIV
        self.text.append(0x99)

    def emit_idiv_r32(self, reg):
        reg_id = self._reg_id(reg)

        # idiv r/m32
        self.text.append(0xF7)
        self.text.append(0xF8 | reg_id)
    
    def emit_cmp_reg_reg32(self, left, right):
        left_id  = self._reg_id(left)
        right_id = self._reg_id(right)

        # cmp r/m32, r32
        self.text.append(0x39)
        self.text.append(0xC0 | (right_id << 3) | left_id)

    def emit_cmp_reg_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        # cmp r/m32, imm32
        self.text.append(0x81)
        self.text.append(0xF8 | reg_id)
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_setne(self, reg):
        if reg != "al":
            raise RuntimeError(tr("PE32Writer.emit_setne currently supports only al"))

        # setne al
        self.text += b"\x0F\x95\xC0"
    
    def emit_movzx(self, dst, src, comment=""):
        self.writer.emit_movzx_r32_r8(
            self.map_reg32(dst),
            self.map_reg8(src)
        )

    def emit_movzx_r32_r8(self, dst, src):
        dst_id = self._reg_id(dst)

        reg8 = {
            "al": 0,
            "cl": 1,
            "dl": 2,
            "bl": 3,
        }

        if src not in reg8:
            raise RuntimeError(f"{tr('unsupported 8-bit source register')}: {src}")

        # movzx r32, r/m8
        self.text += b"\x0F\xB6"
        self.text.append(0xC0 | (dst_id << 3) | reg8[src])
    
    def emit_mov_r64_data_label(self, dst, label):
        # NT32: r64-Aufruf vom gemeinsamen Generator auf r32 abbilden
        return self.emit_mov_r32_data_label(
            self._map_reg64_to_32(dst),
            label
        )

    def emit_mov_data_label_r64(self, label, src):
        # NT32: Pointer/String/Object-Handles sind 32-bit
        return self.emit_mov_data_label_r32(
            label,
            self._map_reg64_to_32(src)
        )

    def _map_reg64_to_32(self, reg):
        reg_map = {
            "rax": "eax",
            "rbx": "ebx",
            "rcx": "ecx",
            "rdx": "edx",
            "rsi": "esi",
            "rdi": "edi",
            "rbp": "ebp",
            "rsp": "esp",
        }

        return reg_map.get(reg, reg)
    
    def emit_test_reg_reg32(self, reg1, reg2):
        r1 = self._reg_id(reg1)
        r2 = self._reg_id(reg2)

        # test r/m32, r32
        self.text.append(0x85)
        self.text.append(0xC0 | (r2 << 3) | r1)
    
    def emit_call_reg32(self, reg):
        reg_id = self._reg_id(reg)

        # call r/m32
        self.text.append(0xFF)
        self.text.append(0xD0 | reg_id)
    
    def emit_push_data_label32(self, label):
        sym_index = self.find_or_add_symbol(label)

        self.text.append(0x68)  # push imm32

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_DIR32
        })
    
    def emit_fstp_qword_ptr_esp(self):
        # fstp qword [esp]
        self.text += b"\xDD\x1C\x24"
    
    def emit_movsd_qword_ptr_esp_xmm0(self):
        # movsd qword [esp], xmm0
        self.text += b"\xF2\x0F\x11\x04\x24"
    
    def add_data_double(self, name, value):
        bits = double_to_bits(value)
        return self.add_data_bytes(
            name,
            int(bits).to_bytes(8, "little", signed=False),
            alignment=8
        )

    def emit_movsd_xmm0_data_label32(self, label):
        sym_index = self.find_or_add_symbol(label)

        # movsd xmm0, qword ptr [imm32]
        self.text += b"\xF2\x0F\x10\x05"

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_DIR32
        })
    
    def _xmm_id(self, reg):
        xmm = {
            "xmm0": 0,
            "xmm1": 1,
            "xmm2": 2,
            "xmm3": 3,
            "xmm4": 4,
            "xmm5": 5,
            "xmm6": 6,
            "xmm7": 7,
        }
        if reg not in xmm:
            raise RuntimeError(f"{tr('unsupported NT32 xmm register')}: {reg}")
        return xmm[reg]

    def emit_movsd_store32(self, base, offset, src):
        src_id = self._xmm_id(src)
        self.text += b"\xF2\x0F\x11"
        self._emit_modrm_mem32(src_id, self._reg_id(base), offset)

    def emit_movsd_load32(self, dst, base, offset=0):
        dst_id = self._xmm_id(dst)
        self.text += b"\xF2\x0F\x10"
        self._emit_modrm_mem32(dst_id, self._reg_id(base), offset)
    
    def emit_cvtsi2sd32(self, dst, src):
        dst_id = self._xmm_id(dst)
        src_id = self._reg_id(src)

        # cvtsi2sd xmm, r/m32
        self.text += b"\xF2\x0F\x2A"
        self.text.append(0xC0 | (dst_id << 3) | src_id)

    def emit_sse2_xmm_xmm32(self, opcode, dst, src):
        dst_id = self._xmm_id(dst)
        src_id = self._xmm_id(src)

        # addsd/subsd/mulsd/divsd xmm, xmm
        self.text += b"\xF2\x0F"
        self.text.append(opcode)
        self.text.append(0xC0 | (dst_id << 3) | src_id)

    def emit_mov_reg_from_data_label32(self, reg, label):
        reg_id    = self._reg_id(reg)
        sym_index = self.find_or_add_symbol(label)

        # mov r32, dword ptr [imm32]
        self.text.append(0x8B)
        self.text.append(0x05 | (reg_id << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_DIR32
        })

    def emit_lea_reg_data_label(self, reg, label):
        # NT32: Adresse eines Datenlabels in Register laden
        # mov reg, imm32 + DIR32 relocation
        self.emit_mov_reg_data_label32(reg, label)

    def add_data_i32_symbol_ref(self, target_symbol):
        sym_index = self.find_or_add_symbol(target_symbol)
        offset = len(self.data)
        self.data += b"\x00\x00\x00\x00"

        self.data_relocations.append({
            "offset": offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_DIR32
        })

        return offset

    def emit_setcc_r8(self, opcode, reg):
        reg8 = {
            "al": 0,
            "cl": 1,
            "dl": 2,
            "bl": 3,
        }

        reg = reg.lower()

        if reg not in reg8:
            raise RuntimeError(
                f"unsupported 8-bit SETcc register: {reg}"
            )

        # SETcc r/m8:
        # 0F opcode /0
        self.text += b"\x0F"
        self.text.append(opcode)
        self.text.append(0xC0 | reg8[reg])


    def emit_sete (self, reg): self.emit_setcc_r8(0x94, reg)
    def emit_setne(self, reg): self.emit_setcc_r8(0x95, reg)
    def emit_setl (self, reg): self.emit_setcc_r8(0x9C, reg)
    def emit_setge(self, reg): self.emit_setcc_r8(0x9D, reg)
    def emit_setle(self, reg): self.emit_setcc_r8(0x9E, reg)
    def emit_setg (self, reg): self.emit_setcc_r8(0x9F, reg)

    #def has_symbol(self, name):
    #    for sym in self.symbols:
    #        if sym.name == name:
    #            return True
    #    return False
    
    def has_symbol(self, name):
        for sym in self.symbols:
            if isinstance(sym, dict):
                if sym.get("name") == name:
                    return True
            else:
                if getattr(sym, "name", None) == name:
                    return True
        return False

    def add_data_label(self, name):
        if self.find_symbol_index(name) is not None:
            raise RuntimeError(
                f"Duplicate data label: {name}"
            )

        self.add_symbol(
            name=name,
            value=len(self.data),
            section_number=2
        )
    
    def ensure_data_symbol_block(self, name, size):
        if not self.has_symbol(name):
            self.add_data_bytes(name, b"\x00" * size, alignment=4)
        
    def add_jit_context32(self, name="ctx"):
        #self.ensure_data_symbol_block("int_vars",    4 * max( 1, self.required_int_slots))
        #self.ensure_data_symbol_block("double_vars", 8 * max( 1, self.required_double_slots))
        #self.ensure_data_symbol_block("string_vars", 4 * max( 1, self.required_string_slots))
        #self.ensure_data_symbol_block("record_vars",     max(16, self.required_record_bytes))
        #self.ensure_data_symbol_block("arrays_vars",     max(16, self.required_array_bytes))
        #self.ensure_data_symbol_block("pointr_vars", 4 * max( 1, self.required_pointer_slots))
        
        self.ensure_data_symbol_block("int_vars", 16)
        self.ensure_data_symbol_block("double_vars", 16)
        self.ensure_data_symbol_block("string_vars", 16)
        self.ensure_data_symbol_block("record_vars", 64)
        self.ensure_data_symbol_block("arrays_vars", 64)
        self.ensure_data_symbol_block("pointr_vars", 16)

        self.align_data(4)
        ctx_offset = len(self.data)

        self.add_symbol(
            name=name,
            value=ctx_offset,
            section_number=2
        )

        self.add_data_i32_symbol_ref("int_vars")
        self.add_data_i32_symbol_ref("double_vars")
        self.add_data_i32_symbol_ref("string_vars")
        self.add_data_i32_symbol_ref("record_vars")
        self.add_data_i32_symbol_ref("arrays_vars")
        self.add_data_i32_symbol_ref("pointr_vars")

        self.data += b"\x00" * 4   # print_int_tmp
        self.data += b"\x00" * 8   # print_double_tmp

        return ctx_offset

    def pointer_slot_size(self):
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            return 4
        return 8

    def _coff_encode_symbol_name(
        self,
        name,
        string_data,
        string_offsets
    ):
        """
        Kodiert einen COFF-Symbolnamen.

        Namen mit maximal 8 Bytes werden direkt im Symbol-Eintrag
        gespeichert. Laengere Namen werden in der COFF-Stringtabelle
        abgelegt.
        """
        encoded_name = str(name).encode(
            "ascii",
            errors="replace"
        )

        if len(encoded_name) <= 8:
            return encoded_name.ljust(8, b"\x00")

        if name not in string_offsets:
            # COFF-Offsets beziehen sich auf den Anfang der Stringtabelle.
            # Die ersten vier Bytes enthalten deren Gesamtgroesse.
            string_offsets[name] = 4 + len(string_data)
            string_data += encoded_name + b"\x00"

        return struct.pack(
            "<II",
            0,
            string_offsets[name]
        )

    def build_object_image(self):
        """
        Erzeugt eine reine Microsoft COFF32-i386-Objektdatei.

        Enthalten:
            - IMAGE_FILE_HEADER
            - .text-Section
            - .data-Section
            - Relocation-Tabellen
            - Symboltabelle
            - Stringtabelle

        Nicht enthalten:
            - DOS-MZ-Header
            - PE-Signatur
            - Optional Header
            - Import-Tabelle
            - Programmeinstieg
        """
        IMAGE_FILE_MACHINE_I386 = 0x014C

        IMAGE_SCN_CNT_CODE             = 0x00000020
        IMAGE_SCN_CNT_INITIALIZED_DATA = 0x00000040

        IMAGE_SCN_ALIGN_4BYTES         = 0x00300000
        IMAGE_SCN_ALIGN_16BYTES        = 0x00500000

        IMAGE_SCN_MEM_EXECUTE          = 0x20000000
        IMAGE_SCN_MEM_READ             = 0x40000000
        IMAGE_SCN_MEM_WRITE            = 0x80000000

        text_characteristics = (
            IMAGE_SCN_CNT_CODE
            | IMAGE_SCN_ALIGN_16BYTES
            | IMAGE_SCN_MEM_EXECUTE
            | IMAGE_SCN_MEM_READ
        )

        data_characteristics = (
            IMAGE_SCN_CNT_INITIALIZED_DATA
            | IMAGE_SCN_ALIGN_4BYTES
            | IMAGE_SCN_MEM_READ
            | IMAGE_SCN_MEM_WRITE
        )

        # Interne Vorwaertsreferenzen muessen vor dem Schreiben
        # vollstaendig aufgeloest sein.
        if self.fixups:
            unresolved_labels = sorted({
                fixup["label"]
                for fixup in self.fixups
            })

            raise RuntimeError(
                "unresolved internal COFF labels: "
                + ", ".join(unresolved_labels)
            )

        if len(self.text_relocations) > 0xFFFF:
            raise RuntimeError(
                "too many .text relocations for COFF32"
            )

        if len(self.data_relocations) > 0xFFFF:
            raise RuntimeError(
                "too many .data relocations for COFF32"
            )

        sections = [
            {
                "name": b".text\x00\x00\x00",
                "data": bytes(self.text),
                "relocations": self.text_relocations,
                "characteristics": text_characteristics
            },
            {
                "name": b".data\x00\x00\x00",
                "data": bytes(self.data),
                "relocations": self.data_relocations,
                "characteristics": data_characteristics
            }
        ]

        number_of_sections = len(sections)

        file_header_size    = 20
        section_header_size = 40

        cursor = (
            file_header_size
            + number_of_sections * section_header_size
        )

        # Datei-Offsets der Sektionsdaten und Relocations bestimmen.
        for section in sections:
            section_data = section["data"]
            relocations  = section["relocations"]

            if section_data:
                section["raw_pointer"] = cursor
                cursor += len(section_data)
            else:
                section["raw_pointer"] = 0

            if relocations:
                section["reloc_pointer"] = cursor
                cursor += len(relocations) * 10
            else:
                section["reloc_pointer"] = 0

        pointer_to_symbol_table = cursor

        # Symbol- und Stringtabelle erzeugen.
        symbol_table   = bytearray()
        string_data    = bytearray()
        string_offsets = {}

        for symbol in self.symbols:
            symbol_name = symbol["name"]

            encoded_name = self._coff_encode_symbol_name(
                symbol_name,
                string_data,
                string_offsets
            )

            value = int(
                symbol.get("value", 0)
            )

            section_number = int(
                symbol.get("section", 0)
            )

            symbol_type = int(
                symbol.get("type", 0)
            )

            storage_class = int(
                symbol.get(
                    "storage",
                    IMAGE_SYM_CLASS_EXTERNAL
                )
            )

            number_of_aux_symbols = int(
                symbol.get("aux", 0)
            )

            if number_of_aux_symbols != 0:
                raise RuntimeError(
                    "COFF auxiliary symbols are not supported yet: "
                    + str(symbol_name)
                )

            symbol_table += encoded_name
            symbol_table += struct.pack(
                "<IhHBB",
                value,
                section_number,
                symbol_type,
                storage_class,
                number_of_aux_symbols
            )

        number_of_symbols = len(self.symbols)

        # Die ersten vier Bytes der COFF-Stringtabelle enthalten
        # deren Gesamtgroesse einschliesslich des Laengenfeldes.
        string_table = (
            struct.pack(
                "<I",
                4 + len(string_data)
            )
            + string_data
        )

        # Reiner COFF-File-Header: kein Optional Header.
        file_header = struct.pack(
            "<HHIIIHH",
            IMAGE_FILE_MACHINE_I386,
            number_of_sections,
            0,                          # TimeDateStamp
            pointer_to_symbol_table,
            number_of_symbols,
            0,                          # SizeOfOptionalHeader
            0                           # Characteristics
        )

        section_headers = bytearray()

        for section in sections:
            section_headers += struct.pack(
                "<8sIIIIIIHHI",
                section["name"],
                0,                          # PhysicalAddress / VirtualSize
                0,                          # VirtualAddress
                len(section["data"]),       # SizeOfRawData
                section["raw_pointer"],     # PointerToRawData
                section["reloc_pointer"],   # PointerToRelocations
                0,                          # PointerToLinenumbers
                len(section["relocations"]),
                0,                          # NumberOfLinenumbers
                section["characteristics"]
            )

        image = bytearray()
        image += file_header
        image += section_headers

        for section in sections:
            image += section["data"]

            for relocation in section["relocations"]:
                image += struct.pack(
                    "<IIH",
                    int(relocation["offset"]),
                    int(relocation["symbol_index"]),
                    int(relocation["type"])
                )

        image += symbol_table
        image += string_table

        return image

    def write_object(self, filename):
        """Schreibt eine reine COFF32-i386-Objektdatei."""
        output_path = os.path.abspath(filename)
        output_dir  = os.path.dirname(output_path)

        if output_dir:
            os.makedirs(
                output_dir,
                exist_ok=True
            )

        image = self.build_object_image()

        with open(output_path, "wb") as stream:
            stream.write(image)

        # Selbsttest mit dem bereits vorhandenen Reader.
        obj = Coff32Reader(output_path).read()

        if not obj.sections:
            raise RuntimeError(
                "written COFF32 object contains no sections"
            )

        return output_path

    def write(self, filename):
        #self.add_coff_object("math.o")
        #self.add_archive_file("libmath.a")
        #self.add_archive_file("libruntime.a")
        
        # {$link foo.o}
        for obj in CDATA.link_object_files:
            self.add_coff_object(obj)
        
        # {$linklib libfoo.a}
        for lib in CDATA.link_archive_files:
            self.add_link_archive(lib)
        
        # 1. Archive nach offenen Symbolen durchsuchen
        self.resolve_archive_objects()
        
        # 2. Alle gefundenen .o-Objekte einfügen
        self.include_coff_objects()

        NT32Writer(self).write(filename)
