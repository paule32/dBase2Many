# ---------------------------------------------------------------------------
# File: nt32.py - writer for Windows NT 3.5 32 bit
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

from compiler.common.types     import *
from compiler.common.locale    import *

from compiler.backend.coff32   import Coff32Backend

import time
import struct

# ---------------------------------------------------------------------------
# Windows NT 3.5 32-Bit PE executable writer ...
# ---------------------------------------------------------------------------
class NT32Writer:
    EXE_IMAGE_BASE = 0x00400000
    DLL_IMAGE_BASE = 0x10000000

    FILE_ALIGNMENT = 0x200
    SECTION_ALIGN  = 0x1000

    IMAGE_FILE_RELOCS_STRIPPED         = 0x0001
    IMAGE_FILE_EXECUTABLE_IMAGE        = 0x0002
    IMAGE_FILE_LINE_NUMS_STRIPPED      = 0x0004
    IMAGE_FILE_LOCAL_SYMS_STRIPPED     = 0x0008
    IMAGE_FILE_32BIT_MACHINE           = 0x0100
    IMAGE_FILE_DLL                     = 0x2000

    IMAGE_DIRECTORY_ENTRY_EXPORT = 0
    IMAGE_DIRECTORY_ENTRY_IMPORT = 1

    def __init__(self, coff):
        self.coff    = coff
        self.imports = CDATA.imports

        self.is_dll = bool(getattr(coff, "is_dll", False))
        self.IMAGE_BASE = (
            self.DLL_IMAGE_BASE
            if self.is_dll
            else self.EXE_IMAGE_BASE
        )

        self.text_rva = 0
        self.data_rva = 0
        
    @property
    def text(self): return self.coff.text

    @property
    def data(self): return self.coff.data

    def align(self, value, alignment):
        return (value + alignment - 1) & ~(alignment - 1)

    def pad_to(self, data, size):
        while len(data) < size:
            data.append(0)

    def find_entrypoint(self):
        for sym in self.coff.symbols:
            if sym["name"] in ["_start"]:  #("test", "main", "_main"):
                return sym["value"]
        raise RuntimeError(tr("entry point not found: _start/main/_main"))

    def resolve_label_rva(self, label_name):
        """Resolve a Pascal/COFF symbol to an RVA in the final PE image."""
        if not label_name:
            raise RuntimeError("empty PE label name")

        external = getattr(self.coff, "external_symbols", {})
        if label_name in external:
            return external[label_name]

        for sym in self.coff.symbols:
            if sym.get("name") != label_name:
                continue

            if sym.get("section") == 1:
                return self.text_rva + sym.get("value", 0)

            if sym.get("section") == 2:
                return self.data_rva + sym.get("value", 0)

        if label_name in getattr(self.coff, "labels", {}):
            return self.text_rva + self.coff.labels[label_name]

        raise RuntimeError(
            f"PE label/symbol not found: {label_name}"
        )


    def build_text_with_import_thunks(self):
        text_image = bytearray(self.text)
        self.import_thunk_offsets = {}

        for internal_name in self.all_import_functions():
            if not isinstance(internal_name, str):
                raise RuntimeError(
                    "internal import symbol is not a string: "
                    + repr(internal_name)
                )

            if internal_name in self.import_thunk_offsets:
                continue

            self.import_thunk_offsets[
                internal_name
            ] = len(text_image)

            # jmp dword ptr [absolute IAT address]
            #
            # FF 25 xx xx xx xx
            text_image += (
                b"\xFF\x25"
                b"\x00\x00\x00\x00"
            )

        return text_image

    #Liefert den internen COFF-Symbolnamen.
    #
    #Dieser Name wird verwendet für:
    #
    #  - COFF-Relocations
    #  - Import-Thunks
    #  - import_iat_rvas
    #  - collect_used_external_symbols()
    #
    #Unterstützte Formate:
    #
    #    "_jit_print_text"
    #
    #    ("_jit_print_text", 12)
    #
    #    {
    #        "symbol": "__dllimp_0_libfoo_fuzz",
    #        "name": "fuzz"
    #    }
    #
    #    {
    #        "symbol": "__dllimp_0_libfoo_fuzz",
    #        "name": "fuzz",
    #        "ordinal": 12
    #    }
    def import_internal_name(self, func):
        if isinstance(func, dict):
            name = (
                func.get("symbol")
                or func.get("internal_name")
                or func.get("name")
            )

            if not name:
                raise RuntimeError(
                    "DLL import dictionary has no "
                    "'symbol', 'internal_name' or 'name'"
                )

            if not isinstance(name, str):
                raise RuntimeError(
                    "DLL import internal symbol must be a string: "
                    + repr(name)
                )

            return name

        if isinstance(func, tuple):
            if not func:
                raise RuntimeError(
                    "empty DLL import tuple"
                )

            name = func[0]

            if not isinstance(name, str):
                raise RuntimeError(
                    "DLL import tuple symbol must be a string: "
                    + repr(name)
                )

            return name

        if isinstance(func, str):
            return func

        if isinstance(func, int):
            # Ein reiner Ordinalimport hat sonst keinen Namen für
            # COFF-Relocations. Bevorzugt sollte dafür ein dict oder
            # Tuple mit internem Symbol verwendet werden.
            return f"__ordinal_import_{func}"

        raise RuntimeError(
            "unsupported DLL import descriptor: "
            + repr(func)
        )

    #Liefert den tatsächlichen Namen, der in die PE-Importtabelle
    #geschrieben wird.
    #
    #Beispiel:
    #
    #    Pascal-Name:      Foo
    #    internes Symbol:  __dllimp_0_libfoo_fuzz
    #    DLL-Exportname:   fuzz
    def import_external_name(self, func):
        if isinstance(func, dict):
            name = (
                func.get("name")
                or func.get("import_name")
                or func.get("symbol")
            )

            if name is None:
                return None

            if not isinstance(name, str):
                raise RuntimeError(
                    "DLL import external name must be a string: "
                    + repr(name)
                )

            return name

        if isinstance(func, tuple):
            # Das bisherige Tuple-Format ist:
            #
            #     (internal_name, ordinal)
            #
            # Daher wird bei einem Ordinalimport kein Name benötigt.
            return func[0]

        if isinstance(func, str):
            return func

        if isinstance(func, int):
            return None

        raise RuntimeError(
            "unsupported DLL import descriptor: "
            + repr(func)
        )

    # Liefert die Ordinalnummer oder None bei Import-by-name.
    def import_ordinal(self, func):
        if isinstance(func, dict):
            ordinal = func.get("ordinal")

            if ordinal is None:
                return None

            ordinal = int(ordinal)

            if not 1 <= ordinal <= 0xFFFF:
                raise RuntimeError(
                    f"invalid DLL import ordinal: {ordinal}"
                )

            return ordinal

        if isinstance(func, tuple):
            if len(func) < 2:
                return None

            ordinal = int(func[1])

            if not 1 <= ordinal <= 0xFFFF:
                raise RuntimeError(
                    f"invalid DLL import ordinal: {ordinal}"
                )

            return ordinal

        if isinstance(func, int):
            if not 1 <= func <= 0xFFFF:
                raise RuntimeError(
                    f"invalid DLL import ordinal: {func}"
                )

            return func

        return None

    #Erzeugt den ILT/IAT-Wert für einen Ordinalimport.
    #
    #Bei Import-by-name wird None geliefert; der Aufrufer erzeugt
    #dann einen IMAGE_IMPORT_BY_NAME-Eintrag.
    def import_lookup_value(
        self,
        func,
        idata_rva=None,
        cursor=None
    ):
        IMAGE_ORDINAL_FLAG32 = 0x80000000

        ordinal = self.import_ordinal(func)

        if ordinal is None:
            return None

        return (
            IMAGE_ORDINAL_FLAG32
            | (ordinal & 0xFFFF)
        )


    #Liefert alle internen Import-Symbolnamen.
    #
    #Wichtig: Hier dürfen niemals die Dictionary-Objekte selbst
    #zurückgegeben werden, weil sie später als Dictionary-Schlüssel
    #verwendet werden.
    def all_import_functions(self):
        result = []
        seen   = set()

        for dll_name, funcs in self.imports.items():
            for func in funcs:
                internal_name = self.import_internal_name(
                    func
                )

                if internal_name in seen:
                    continue

                seen.add(internal_name)
                result.append(internal_name)

        return result

    def import_external_name(self, func):
        if isinstance(func, dict):
            return func.get(
                "name",
                func["symbol"]
            )

        if isinstance(func, tuple):
            return func[0]

        if isinstance(func, int):
            return None

        return func

    def import_ordinal(self, func):
        if isinstance(func, dict):
            return func.get("ordinal")

        if isinstance(func, tuple):
            return func[1]

        if isinstance(func, int):
            return func

        return None


    def build_import_section_by_name(self, idata_rva):
        self.import_iat_rvas = {}

        descriptor_size  = 20
        descriptors_size = (len(self.imports) + 1) * descriptor_size

        data = bytearray(b"\x00" * descriptors_size)
        cursor = descriptors_size
        descriptors = []

        for dll_name, funcs in self.imports.items():
            ilt_rva = idata_rva + cursor
            ilt_offsets = []

            for func in funcs:
                ilt_offsets.append(cursor)
                data += b"\x00" * 4
                cursor += 4

            data += b"\x00" * 4
            cursor += 4

            iat_rva = idata_rva + cursor
            iat_offsets = []

            for func in funcs:
                iat_offsets.append(cursor)
                self.import_iat_rvas[func] = idata_rva + cursor
                data += b"\x00" * 4
                cursor += 4

            data += b"\x00" * 4
            cursor += 4

            hint_name_rvas = []

            for func in funcs:
                hint_name_rva = idata_rva + cursor
                hint_name_rvas.append(hint_name_rva)

                data += struct.pack("<H", 0)
                data += func.encode("ascii") + b"\x00"
                cursor = len(data)

            dll_name_rva = idata_rva + cursor
            data += dll_name.encode("ascii") + b"\x00"
            cursor = len(data)

            for off, hn_rva in zip(ilt_offsets, hint_name_rvas):
                struct.pack_into("<I", data, off, hn_rva)

            for off, hn_rva in zip(iat_offsets, hint_name_rvas):
                struct.pack_into("<I", data, off, hn_rva)

            descriptors.append((ilt_rva, dll_name_rva, iat_rva))

        for index, (ilt_rva, dll_name_rva, iat_rva) in enumerate(descriptors):
            struct.pack_into(
                "<IIIII",
                data,
                index * descriptor_size,
                ilt_rva,
                0,
                0,
                dll_name_rva,
                iat_rva
            )

        return data

    def collect_used_external_symbols(self):
        """Collect real Windows imports used by primary code and linked .o files.

        Symbols defined by the main Pascal stream or by any linked COFF object
        are internal link targets. Only still-undefined symbols must be resolved
        through the PE import table.
        """
        used = set()
        defined = self.coff.collect_defined_symbols()

        # Relocations emitted directly by the Pascal generator.
        for reloc in self.coff.text_relocations:
            sym = self.coff.symbols[reloc["symbol_index"]]

            if sym["section"] == 0 and sym["name"] not in defined:
                used.add(sym["name"])

        for reloc in self.coff.data_relocations:
            sym = self.coff.symbols[reloc["symbol_index"]]

            if sym["section"] == 0 and sym["name"] not in defined:
                used.add(sym["name"])

        # Relocations contained in linked Pascal-unit/native COFF objects.
        for obj in self.coff.coff_objects:
            for section in obj.sections:
                for reloc in section.relocations:
                    symbol = obj.raw_symbols[reloc.symbol_index]

                    if symbol is None:
                        raise RuntimeError(
                            "COFF relocation references AUX symbol"
                        )

                    if (
                        symbol.section_number == 0
                        and symbol.name not in defined
                    ):
                        used.add(symbol.name)

        return used

    def filtered_imports(self):
        used = self.collect_used_external_symbols()

        result = {}

        for dll_name, funcs in self.imports.items():
            selected = []

            for func in funcs:
                internal_name = self.import_internal_name(func)

                if internal_name in used:
                    selected.append(func)

            if selected:
                result[dll_name] = selected

        return result

    def build_import_section_by_ord(self, idata_rva):
        """
        Erzeugt die PE32-Importsection.

        Unterstützt:

          - Import-by-name
          - Import-by-ordinal
          - internen Symbolalias
          - abweichenden DLL-Exportnamen

        Importbeschreibung:

            "MessageBoxA"

        oder:

            {
                "symbol": "__dllimp_0_libfoo_fuzz",
                "name": "fuzz"
            }

        oder:

            {
                "symbol": "__dllimp_1_libfoo_ord12",
                "ordinal": 12
            }
        """
        self.import_iat_rvas = {}

        descriptor_size = 20

        descriptors_size = (
            len(self.imports) + 1
        ) * descriptor_size

        data = bytearray(
            b"\x00" * descriptors_size
        )

        cursor = descriptors_size
        descriptors = []

        for dll_name, funcs in self.imports.items():
            if not isinstance(dll_name, str):
                raise RuntimeError(
                    "DLL name must be a string: "
                    + repr(dll_name)
                )

            # ----------------------------------------------------------
            # Import Lookup Table
            # ----------------------------------------------------------
            ilt_rva = idata_rva + cursor
            ilt_offsets = []

            for func in funcs:
                ilt_offsets.append(cursor)

                data += b"\x00\x00\x00\x00"
                cursor += 4

            # Nullterminator der ILT
            data += b"\x00\x00\x00\x00"
            cursor += 4

            # ----------------------------------------------------------
            # Import Address Table
            # ----------------------------------------------------------
            iat_rva = idata_rva + cursor
            iat_offsets = []

            for func in funcs:
                internal_name = self.import_internal_name(
                    func
                )

                iat_offsets.append(cursor)

                self.import_iat_rvas[
                    internal_name
                ] = idata_rva + cursor

                data += b"\x00\x00\x00\x00"
                cursor += 4

            # Nullterminator der IAT
            data += b"\x00\x00\x00\x00"
            cursor += 4

            # ----------------------------------------------------------
            # Import-by-name- oder Import-by-ordinal-Werte
            # ----------------------------------------------------------
            lookup_values = []

            for func in funcs:
                ordinal_value = self.import_lookup_value(
                    func,
                    idata_rva,
                    cursor
                )

                if ordinal_value is not None:
                    lookup_values.append(
                        ordinal_value
                    )
                    continue

                external_name = self.import_external_name(
                    func
                )

                if not external_name:
                    raise RuntimeError(
                        "DLL name import has no external name: "
                        + repr(func)
                    )

                try:
                    encoded_name = external_name.encode(
                        "ascii"
                    )
                except UnicodeEncodeError as exc:
                    raise RuntimeError(
                        "DLL import name must be ASCII: "
                        + external_name
                    ) from exc

                # IMAGE_IMPORT_BY_NAME:
                #
                # WORD Hint
                # BYTE Name[]
                # BYTE Null
                hint_name_rva = idata_rva + cursor

                lookup_values.append(
                    hint_name_rva
                )

                data += struct.pack("<H", 0)
                data += encoded_name
                data += b"\x00"

                # IMAGE_IMPORT_BY_NAME-Einträge sollten auf einer
                # geraden Adresse beginnen.
                if len(data) & 1:
                    data += b"\x00"

                cursor = len(data)

            # ----------------------------------------------------------
            # DLL-Name
            # ----------------------------------------------------------
            dll_name_rva = idata_rva + cursor

            try:
                encoded_dll_name = dll_name.encode(
                    "ascii"
                )
            except UnicodeEncodeError as exc:
                raise RuntimeError(
                    "DLL filename must be ASCII: "
                    + dll_name
                ) from exc

            data += encoded_dll_name
            data += b"\x00"

            cursor = len(data)

            # Für den nächsten Block auf DWORD ausrichten.
            while cursor & 3:
                data += b"\x00"
                cursor += 1

            # ----------------------------------------------------------
            # ILT und IAT patchen
            # ----------------------------------------------------------
            for offset, value in zip(
                ilt_offsets,
                lookup_values
            ):
                struct.pack_into(
                    "<I",
                    data,
                    offset,
                    value
                )

            for offset, value in zip(
                iat_offsets,
                lookup_values
            ):
                struct.pack_into(
                    "<I",
                    data,
                    offset,
                    value
                )

            descriptors.append(
                (
                    ilt_rva,
                    dll_name_rva,
                    iat_rva
                )
            )

        # --------------------------------------------------------------
        # IMAGE_IMPORT_DESCRIPTOR-Einträge
        # --------------------------------------------------------------
        for index, descriptor in enumerate(descriptors):
            (
                ilt_rva,
                dll_name_rva,
                iat_rva
            ) = descriptor

            struct.pack_into(
                "<IIIII",
                data,
                index * descriptor_size,

                ilt_rva,       # OriginalFirstThunk
                0,             # TimeDateStamp
                0,             # ForwarderChain
                dll_name_rva,  # Name
                iat_rva        # FirstThunk
            )

        # Der letzte, bereits reservierte Descriptor bleibt komplett 0.
        return data
    
    def patch_import_thunks(self, text_image):
        for internal_name, thunk_offset in (
            self.import_thunk_offsets.items()
        ):
            if internal_name not in self.import_iat_rvas:
                raise RuntimeError(
                    "no IAT entry for imported symbol: "
                    + internal_name
                )

            iat_rva = self.import_iat_rvas[
                internal_name
            ]

            iat_va = self.IMAGE_BASE + iat_rva

            # FF 25 imm32
            #
            # jmp dword ptr [iat_va]
            text_image[
                thunk_offset:
                thunk_offset + 6
            ] = (
                b"\xFF\x25"
                + int(iat_va).to_bytes(
                    4,
                    "little",
                    signed=False
                )
            )

    def symbol_rva(self, sym, text_rva, data_rva):
        if sym["section"] == 1:
            return text_rva + sym["value"]
        if sym["section"] == 2:
            return data_rva + sym["value"]
        raise RuntimeError(f"{tr('unsupported symbol section')}: {sym}")

    def patch_internal_relocations(
        self,
        text_image,
        data_image,
        text_rva,
        data_rva
    ):
        """Patch relocations resolved by this image or linked COFF objects."""
        for reloc in self.coff.text_relocations:
            sym = self.coff.symbols[reloc["symbol_index"]]
            name = sym["name"]

            if sym["section"] == 0:
                # Undefined in the primary stream, but possibly supplied by
                # an included Pascal-unit object. register_coff_symbols() has
                # already populated external_symbols at this point.
                target_rva = self.coff.external_symbols.get(name)

                if target_rva is None:
                    continue
            else:
                target_rva = self.symbol_rva(
                    sym,
                    text_rva,
                    data_rva
                )

            patch_pos = reloc["offset"]

            if reloc["type"] == IMAGE_REL_I386_REL32:
                next_rva = text_rva + patch_pos + 4
                rel32 = target_rva - next_rva

                text_image[patch_pos:patch_pos + 4] = int(
                    rel32
                ).to_bytes(4, "little", signed=True)

            elif reloc["type"] == IMAGE_REL_I386_DIR32:
                target_va = self.IMAGE_BASE + target_rva

                text_image[patch_pos:patch_pos + 4] = int(
                    target_va
                ).to_bytes(4, "little", signed=False)

            else:
                raise RuntimeError(
                    f"unsupported text relocation type: {reloc['type']}"
                )

        for reloc in self.coff.data_relocations:
            sym = self.coff.symbols[reloc["symbol_index"]]
            name = sym["name"]

            if sym["section"] == 0:
                target_rva = self.coff.external_symbols.get(name)

                if target_rva is None:
                    raise RuntimeError(
                        f"unresolved COFF data symbol: {name}"
                    )
            else:
                target_rva = self.symbol_rva(
                    sym,
                    text_rva,
                    data_rva
                )

            patch_pos = reloc["offset"]

            if reloc["type"] == IMAGE_REL_I386_DIR32:
                target_va = self.IMAGE_BASE + target_rva

                data_image[patch_pos:patch_pos + 4] = int(
                    target_va
                ).to_bytes(4, "little", signed=False)
            else:
                raise RuntimeError(
                    f"unsupported data relocation type: {reloc['type']}"
                )

    def patch_external_call_relocations(self, text_image, text_rva):
        for reloc in self.coff.text_relocations:
            sym = self.coff.symbols[reloc["symbol_index"]]

            if sym["section"] != 0:
                continue

            name = sym["name"]

            # The symbol was supplied by a linked .o file and has already
            # been patched by patch_internal_relocations().
            if name in self.coff.external_symbols:
                continue

            if name not in self.import_thunk_offsets:
                raise RuntimeError(
                    f"external call not imported: {name}"
                )

            patch_pos = reloc["offset"]
            thunk_off = self.import_thunk_offsets[name]

            target_rva = text_rva + thunk_off
            next_rva   = text_rva + patch_pos + 4
            rel32      = target_rva - next_rva

            text_image[patch_pos:patch_pos + 4] = int(
                rel32
            ).to_bytes(4, "little", signed=True)

    def validate_imports_complete(self):
        used = self.collect_used_external_symbols()

        known = set()
        for dll_name, funcs in self.imports.items():
            for func in funcs:
                known.add(self.import_internal_name(func))

        missing = used - known

        if missing:
            raise RuntimeError(
                "external symbols not listed in imports: " +
                ", ".join(sorted(missing))
            )
    
    def register_coff_symbols(self, text_rva, data_rva):
        self.coff.external_symbols = {}

        self.coff.external_symbols.update(
            self.build_pascal_symbol_rvas(text_rva, data_rva)
        )

        for obj in self.coff.coff_objects:
            for name, sym in obj.symbols.items():
                if sym is None:
                    continue

                if sym.section_number <= 0:
                    continue

                sec = obj.sections[sym.section_number - 1]

                if sec.output_section == ".text":
                    base_rva = text_rva
                elif sec.output_section in [".data", ".rdata", ".bss"]:
                    base_rva = data_rva
                else:
                    raise RuntimeError(f"unknown COFF output section: {sec.output_section}")

                sym.resolved_rva = base_rva + sec.output_offset + sym.value
                self.coff.external_symbols[name] = sym.resolved_rva

    def build_pascal_symbol_rvas(self, text_rva, data_rva):
        result = {}

        for sym in self.coff.symbols:
            name = sym["name"]

            if sym["section"] == 1:
                rva = text_rva + sym["value"]
            elif sym["section"] == 2:
                rva = data_rva + sym["value"]
            else:
                continue

            result[name] = rva

            if not name.startswith("_"):
                result["_" + name] = rva

            if name.startswith("_"):
                result[name[1:]] = rva

        return result
    
    def linked_object_symbol_rva(
        self,
        obj,
        symbol,
        text_rva,
        data_rva
    ):
        """Resolve a symbol defined in the same linked COFF object.

        Local labels such as str_0 can occur in more than one unit. Resolving
        them through the global name dictionary would make an earlier unit
        accidentally reference the identically named symbol of a later unit.
        """
        if symbol.section_number <= 0:
            return None

        section = obj.sections[symbol.section_number - 1]

        if section.output_section == ".text":
            base_rva = text_rva
        elif section.output_section in (".data", ".rdata", ".bss"):
            base_rva = data_rva
        else:
            raise RuntimeError(
                "unknown COFF output section: "
                + str(section.output_section)
            )

        return base_rva + section.output_offset + symbol.value

    def patch_coff_relocations(
        self,
        text_image,
        data_image,
        text_rva,
        data_rva
    ):
        """Patch relocations located inside linked COFF32 object files.

        Targets can be:
          * symbols defined by the main Pascal object,
          * symbols defined by another linked object,
          * Windows imports reached through a generated import thunk.
        """
        for obj in self.coff.coff_objects:
            for section in obj.sections:
                if not section.output_section:
                    continue

                if section.output_section == ".text":
                    buffer = text_image
                    section_rva = text_rva

                elif section.output_section in (
                    ".data",
                    ".rdata",
                    ".bss"
                ):
                    buffer = data_image
                    section_rva = data_rva

                else:
                    raise RuntimeError(
                        "unknown COFF output section: "
                        + str(section.output_section)
                    )

                for relocation in section.relocations:
                    symbol = obj.raw_symbols[
                        relocation.symbol_index
                    ]

                    if symbol is None:
                        raise RuntimeError(
                            "COFF relocation references AUX symbol"
                        )

                    name = symbol.name
                    patch_offset = (
                        section.output_offset
                        + relocation.virtual_address
                    )

                    # --------------------------------------------------
                    # A symbol defined in this same object must be resolved
                    # from that object's section. Names such as str_0 are
                    # intentionally not globally unique.
                    # --------------------------------------------------
                    if symbol.section_number > 0:
                        target_rva = self.linked_object_symbol_rva(
                            obj,
                            symbol,
                            text_rva,
                            data_rva
                        )

                    # --------------------------------------------------
                    # Undefined in this object, but defined by the main
                    # Pascal stream or another linked object.
                    # --------------------------------------------------
                    elif name in self.coff.external_symbols:
                        target_rva = self.coff.external_symbols[name]

                    # --------------------------------------------------
                    # Imported function used by a linked .o file.
                    # A REL32 call targets the JMP thunk in .text.
                    # --------------------------------------------------
                    elif (
                        relocation.type == IMAGE_REL_I386_REL32
                        and name in self.import_thunk_offsets
                    ):
                        target_rva = (
                            text_rva
                            + self.import_thunk_offsets[name]
                        )

                    else:
                        raise RuntimeError(
                            "unresolved COFF symbol: " + name
                        )

                    if relocation.type == IMAGE_REL_I386_REL32:
                        source_rva = section_rva + patch_offset
                        value = target_rva - (source_rva + 4)

                        buffer[
                            patch_offset:patch_offset + 4
                        ] = int(value).to_bytes(
                            4,
                            "little",
                            signed=True
                        )

                    elif relocation.type == IMAGE_REL_I386_DIR32:
                        value = self.IMAGE_BASE + target_rva

                        buffer[
                            patch_offset:patch_offset + 4
                        ] = int(value).to_bytes(
                            4,
                            "little",
                            signed=False
                        )

                    else:
                        raise RuntimeError(
                            "unsupported COFF relocation type: "
                            f"{relocation.type:04X}"
                        )

    def _export_value(self, item, name, default=None):
        if isinstance(item, dict):
            return item.get(name, default)
        return getattr(item, name, default)

    def build_export_section(self, section_rva):
        exports = list(getattr(self.coff, "exports", []))

        if not exports:
            return bytearray()

        used_ordinals = {
            self._export_value(item, "ordinal")
            for item in exports
            if self._export_value(item, "ordinal") is not None
        }

        next_ordinal = 1
        resolved = []

        for item in exports:
            name = self._export_value(item, "name")
            target_label = self._export_value(item, "target_label")
            ordinal = self._export_value(item, "ordinal")

            if not name:
                raise RuntimeError("DLL export has no name")

            if not target_label:
                raise RuntimeError(
                    f"DLL export {name} has no target label"
                )

            if ordinal is None:
                while next_ordinal in used_ordinals:
                    next_ordinal += 1

                ordinal = next_ordinal
                used_ordinals.add(ordinal)
                next_ordinal += 1

            resolved.append({
                "name": str(name),
                "target_label": str(target_label),
                "ordinal": int(ordinal),
            })

        ordinal_base = min(item["ordinal"] for item in resolved)
        max_ordinal  = max(item["ordinal"] for item in resolved)
        function_count = max_ordinal - ordinal_base + 1

        named_exports = sorted(
            resolved,
            key=lambda item: item["name"].encode("ascii")
        )

        data = bytearray(40)

        dll_name = (
            getattr(self.coff, "image_name", None)
            or "output.dll"
        )
        dll_name = str(dll_name).replace("\\", "/").split("/")[-1]

        dll_name_offset = len(data)
        data += dll_name.encode("ascii", errors="replace") + b"\x00"

        while len(data) & 3:
            data.append(0)

        eat_offset = len(data)
        data += b"\x00" * (function_count * 4)

        name_pointer_offset = len(data)
        data += b"\x00" * (len(named_exports) * 4)

        ordinal_table_offset = len(data)
        data += b"\x00" * (len(named_exports) * 2)

        export_name_offsets = []

        for item in named_exports:
            try:
                encoded = item["name"].encode("ascii")
            except UnicodeEncodeError as exc:
                raise RuntimeError(
                    f"DLL export name is not ASCII: {item['name']}"
                ) from exc

            export_name_offsets.append(len(data))
            data += encoded + b"\x00"

        for item in resolved:
            eat_index = item["ordinal"] - ordinal_base
            target_rva = self.resolve_label_rva(
                item["target_label"]
            )

            struct.pack_into(
                "<I",
                data,
                eat_offset + eat_index * 4,
                target_rva
            )

        for index, item in enumerate(named_exports):
            eat_index = item["ordinal"] - ordinal_base

            struct.pack_into(
                "<I",
                data,
                name_pointer_offset + index * 4,
                section_rva + export_name_offsets[index]
            )

            struct.pack_into(
                "<H",
                data,
                ordinal_table_offset + index * 2,
                eat_index
            )

        struct.pack_into(
            "<IIHHIIIIIII",
            data,
            0,
            0,                              # Characteristics
            int(time.time()),               # TimeDateStamp
            0,                              # MajorVersion
            0,                              # MinorVersion
            section_rva + dll_name_offset,  # Name
            ordinal_base,                   # Base
            function_count,                 # NumberOfFunctions
            len(named_exports),             # NumberOfNames
            section_rva + eat_offset,       # AddressOfFunctions
            section_rva + name_pointer_offset,
            section_rva + ordinal_table_offset
        )

        return data

    def write(self, filename):
        if CDATA.debug_mode:
            print(
            "NT32Writer.write called:",
            "DLL" if self.is_dll else "EXE",
            filename
            )

        if self.is_dll:
            if not getattr(self.coff, "image_name", None):
                self.coff.image_name = filename
        else:
            Coff32Backend(self.coff).emit_program_entry()

        # All local labels must be bound before the PE image is laid out.
        if self.coff.fixups:
            unresolved = [
                f"{fixup['label']} at text+0x{fixup['patch_pos']:08X}"
                for fixup in self.coff.fixups
            ]

            raise RuntimeError(
                "unresolved local labels before PE link:\n"
                + "\n".join(unresolved)
            )

        self.validate_imports_complete()
        self.imports = self.filtered_imports()

        dos_header = bytearray(64)
        dos_header[0:2] = b"MZ"
        struct.pack_into("<I", dos_header, 0x3C, 0x80)

        dos_stub = bytearray(0x80 - len(dos_header))
        pe_sig = b"PE\x00\x00"

        has_exports = self.is_dll and bool(
            getattr(self.coff, "exports", [])
        )

        number_of_sections = 4 if has_exports else 3
        size_of_optional_header = 0xE0
        section_header_size = 40

        characteristics = (
            self.IMAGE_FILE_RELOCS_STRIPPED |
            self.IMAGE_FILE_EXECUTABLE_IMAGE |
            self.IMAGE_FILE_LINE_NUMS_STRIPPED |
            self.IMAGE_FILE_LOCAL_SYMS_STRIPPED |
            self.IMAGE_FILE_32BIT_MACHINE
        )

        if self.is_dll:
            characteristics |= self.IMAGE_FILE_DLL

        file_header = struct.pack(
            "<HHIIIHH",
            0x014C,
            number_of_sections,
            int(time.time()),
            0,
            0,
            size_of_optional_header,
            characteristics
        )

        headers_size = self.align(
            0x80 + 4 + 20 + size_of_optional_header +
            number_of_sections * section_header_size,
            self.FILE_ALIGNMENT
        )

        text_image = self.build_text_with_import_thunks()

        self.text_rva = self.SECTION_ALIGN
        text_rva = self.text_rva

        text_raw = headers_size
        text_virtual_size = max(1, len(text_image))
        text_raw_size = self.align(
            text_virtual_size,
            self.FILE_ALIGNMENT
        )

        self.data_rva = self.align(
            text_rva + text_virtual_size,
            self.SECTION_ALIGN
        )
        data_rva = self.data_rva

        data_raw = text_raw + text_raw_size
        data_image = bytearray(self.data)
        data_virtual_size = max(1, len(data_image))
        data_raw_size = self.align(
            data_virtual_size,
            self.FILE_ALIGNMENT
        )

        idata_rva = self.align(
            data_rva + data_virtual_size,
            self.SECTION_ALIGN
        )
        idata_raw = data_raw + data_raw_size
        idata = self.build_import_section_by_ord(idata_rva)
        idata_virtual_size = max(1, len(idata))
        idata_raw_size = self.align(
            idata_virtual_size,
            self.FILE_ALIGNMENT
        )

        # All Pascal and linked-object symbols now receive their final RVA.
        self.register_coff_symbols(text_rva, data_rva)

        self.patch_coff_relocations(
            text_image,
            data_image,
            text_rva,
            data_rva
        )
        self.patch_internal_relocations(
            text_image,
            data_image,
            text_rva,
            data_rva
        )
        self.patch_external_call_relocations(
            text_image,
            text_rva
        )
        self.patch_import_thunks(text_image)

        edata = bytearray()
        edata_rva = 0
        edata_raw = 0
        edata_virtual_size = 0
        edata_raw_size = 0

        if has_exports:
            edata_rva = self.align(
                idata_rva + idata_virtual_size,
                self.SECTION_ALIGN
            )
            edata_raw = idata_raw + idata_raw_size
            edata = self.build_export_section(edata_rva)
            edata_virtual_size = len(edata)
            edata_raw_size = self.align(
                edata_virtual_size,
                self.FILE_ALIGNMENT
            )

        if self.is_dll:
            entry_label = getattr(
                self.coff,
                "dll_entry_label",
                None
            )
            entry_rva = (
                self.resolve_label_rva(entry_label)
                if entry_label
                else 0
            )
        else:
            entry_rva = text_rva + self.find_entrypoint()

        if has_exports:
            image_end_rva = edata_rva + edata_virtual_size
        else:
            image_end_rva = idata_rva + idata_virtual_size

        size_of_image = self.align(
            image_end_rva,
            self.SECTION_ALIGN
        )

        initialized_data_size = (
            data_raw_size +
            idata_raw_size +
            edata_raw_size
        )

        optional_header = bytearray()
        optional_header += struct.pack("<H", 0x10B)
        optional_header += struct.pack("<BB", 6, 0)
        optional_header += struct.pack(
            "<III",
            text_raw_size,
            initialized_data_size,
            0
        )
        optional_header += struct.pack("<I", entry_rva)
        optional_header += struct.pack("<I", text_rva)
        optional_header += struct.pack("<I", data_rva)
        optional_header += struct.pack("<I", self.IMAGE_BASE)
        optional_header += struct.pack(
            "<II",
            self.SECTION_ALIGN,
            self.FILE_ALIGNMENT
        )

        optional_header += struct.pack(
            "<HHHHHH",
            3, 50,
            0, 0,
            3, 50
        )

        optional_header += struct.pack("<I", 0)
        optional_header += struct.pack("<I", size_of_image)
        optional_header += struct.pack("<I", headers_size)
        optional_header += struct.pack("<I", 0)

        # Subsystem is largely irrelevant for a DLL. Keep console for
        # compatibility with the existing NT32 runtime.
        optional_header += struct.pack("<HH", 3, 0)

        optional_header += struct.pack(
            "<IIIIII",
            0x100000,
            0x1000,
            0x100000,
            0x1000,
            0,
            16
        )

        data_directories = bytearray(16 * 8)

        if has_exports:
            struct.pack_into(
                "<II",
                data_directories,
                self.IMAGE_DIRECTORY_ENTRY_EXPORT * 8,
                edata_rva,
                len(edata)
            )

        struct.pack_into(
            "<II",
            data_directories,
            self.IMAGE_DIRECTORY_ENTRY_IMPORT * 8,
            idata_rva,
            len(idata)
        )

        optional_header += data_directories

        if len(optional_header) != size_of_optional_header:
            raise RuntimeError(
                f"{tr('optional header size')}: "
                f"{len(optional_header)}"
            )

        text_section_header = struct.pack(
            "<8sIIIIIIHHI",
            b".text\x00\x00\x00",
            text_virtual_size,
            text_rva,
            text_raw_size,
            text_raw,
            0, 0, 0, 0,
            0x60000020
        )

        data_section_header = struct.pack(
            "<8sIIIIIIHHI",
            b".data\x00\x00\x00",
            data_virtual_size,
            data_rva,
            data_raw_size,
            data_raw,
            0, 0, 0, 0,
            0xC0000040
        )

        idata_section_header = struct.pack(
            "<8sIIIIIIHHI",
            b".idata\x00\x00",
            idata_virtual_size,
            idata_rva,
            idata_raw_size,
            idata_raw,
            0, 0, 0, 0,
            0xC0000040
        )

        section_headers = bytearray()
        section_headers += text_section_header
        section_headers += data_section_header
        section_headers += idata_section_header

        if has_exports:
            section_headers += struct.pack(
                "<8sIIIIIIHHI",
                b".edata\x00\x00",
                edata_virtual_size,
                edata_rva,
                edata_raw_size,
                edata_raw,
                0, 0, 0, 0,
                0x40000040
            )

        image = bytearray()
        image += dos_header
        image += dos_stub
        image += pe_sig
        image += file_header
        image += optional_header
        image += section_headers

        self.pad_to(image, text_raw)

        image += text_image
        self.pad_to(image, text_raw + text_raw_size)

        image += data_image
        self.pad_to(image, data_raw + data_raw_size)

        image += idata
        self.pad_to(image, idata_raw + idata_raw_size)

        if has_exports:
            image += edata
            self.pad_to(image, edata_raw + edata_raw_size)

        with open(filename, "wb") as stream:
            stream.write(image)

