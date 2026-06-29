# ---------------------------------------------------------------------------
# File: pe64.py - writer for pe64
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

# ---------------------------------------------------------------------------
# Windows 10 64-Bit PE executable writer ...
# ---------------------------------------------------------------------------
class PE64Writer:
    IMAGE_BASE     = 0x140000000
    FILE_ALIGNMENT = 0x200
    SECTION_ALIGN  = 0x1000

    def __init__(self, coff):
        self.coff    = coff
        self.imports = CDATA.imports

    @property
    def text(self):
        return self.coff.text
    
    @property
    def code(self):
        return self.coff.code
    
    @property
    def data(self):
        return self.coff.data

    def find_entrypoint(self):
        for sym in self.coff.symbols:
            if sym["name"] in ("test", "main", "_main"):
                return sym["value"]
        raise RuntimeError(tr("entry point not found: main/_main"))

    def align(self, value, alignment):
        return (value + alignment - 1) & ~(alignment - 1)

    def pad_to(self, data, size):
        while len(data) < size:
            data.append(0)
    
    def emit_ret(self):
        self.text.append(0xC3)

    def all_import_functions(self):
        funcs = []
        for dll_name, names in self.imports.items():
            for name in names:
                if name not in funcs:
                    funcs.append(name)
        return funcs

    def build_text_with_import_thunks(self):
        text_image = bytearray(self.text)
        self.import_thunk_offsets = {}

        for name in self.all_import_functions():
            self.import_thunk_offsets[name] = len(text_image)

            # jmp qword [rip + disp32]
            # FF 25 xx xx xx xx
            text_image += b"\xFF\x25\x00\x00\x00\x00"

        return text_image

    def patch_external_call_relocations(self, text_image, text_rva):
        for reloc in self.coff.text_relocations:
            sym = self.coff.symbols[reloc["symbol_index"]]
            name = sym["name"]

            if sym["section"] != 0:
                continue

            if name not in self.import_thunk_offsets:
                raise RuntimeError(f"{tr('external call not imported')}: {name}")

            patch_pos = reloc["offset"]
            thunk_off = self.import_thunk_offsets[name]

            target_rva = text_rva + thunk_off
            next_rva   = text_rva + patch_pos + 4

            rel32 = target_rva - next_rva
            text_image[patch_pos:patch_pos + 4] = int(rel32).to_bytes(4, "little", signed=True)

    def patch_import_thunks(self, text_image, text_rva):
        for name, thunk_off in self.import_thunk_offsets.items():
            if name not in self.import_iat_rvas:
                raise RuntimeError(f"{tr('IAT RVA missing for import')}: {name}")

            iat_rva = self.import_iat_rvas[name]

            thunk_rva = text_rva + thunk_off
            next_rva  = thunk_rva + 6

            disp32 = iat_rva - next_rva

            text_image[thunk_off:thunk_off + 6] = (
                b"\xFF\x25" +
                int(disp32).to_bytes(4, "little", signed=True)
            )

    def symbol_rva(self, sym, text_rva, data_rva):
        if sym["section"] == 1:
            return text_rva + sym["value"]

        if sym["section"] == 2:
            return data_rva + sym["value"]

        raise RuntimeError(f"{tr('unsupported symbol section')}: {sym}")

    def patch_internal_relocations(self, text_image, data_image, text_rva, data_rva):
        # .text Relocations, z.B. lea rcx, [rel str_0]
        for reloc in self.coff.text_relocations:
            sym = self.coff.symbols[reloc["symbol_index"]]

            # externe Imports werden separat über Thunks behandelt
            if sym["section"] == 0:
                continue

            if reloc["type"] == IMAGE_REL_AMD64_REL32:
                patch_pos = reloc["offset"]
                target_rva = self.symbol_rva(sym, text_rva, data_rva)
                next_rva = text_rva + patch_pos + 4

                rel32 = target_rva - next_rva

                text_image[patch_pos:patch_pos + 4] = int(rel32).to_bytes(
                    4,
                    "little",
                    signed=True
                )
            else:
                raise RuntimeError(f"{tr('unsupported text relocation type')}: {reloc['type']}")

        # .data Relocations, z.B. ctx enthält qword-Adresse von int_vars
        for reloc in self.coff.data_relocations:
            sym = self.coff.symbols[reloc["symbol_index"]]

            if reloc["type"] == IMAGE_REL_AMD64_ADDR64:
                patch_pos = reloc["offset"]
                target_va = self.IMAGE_BASE + self.symbol_rva(sym, text_rva, data_rva)

                data_image[patch_pos:patch_pos + 8] = int(target_va).to_bytes(
                    8,
                    "little",
                    signed=False
                )
            else:
                raise RuntimeError(f"{tr('unsupported data relocation type')}: {reloc['type']}")

    def build_import_section(self, idata_rva):
        imports = self.imports
        self.import_iat_rvas = {}

        descriptor_size = 20
        descriptors_size = (len(imports) + 1) * descriptor_size

        data = bytearray(b"\x00" * descriptors_size)

        cursor = descriptors_size
        descriptors = []

        for dll_name, funcs in imports.items():
            ilt_rva = idata_rva + cursor

            ilt_offsets = []
            for func in funcs:
                ilt_offsets.append(cursor)
                data += b"\x00" * 8
                cursor += 8

            data += b"\x00" * 8
            cursor += 8

            iat_rva = idata_rva + cursor

            iat_offsets = []
            for func in funcs:
                iat_offsets.append(cursor)
                self.import_iat_rvas[func] = idata_rva + cursor
                data += b"\x00" * 8
                cursor += 8

            data += b"\x00" * 8
            cursor += 8

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
                struct.pack_into("<Q", data, off, hn_rva)

            for off, hn_rva in zip(iat_offsets, hint_name_rvas):
                struct.pack_into("<Q", data, off, hn_rva)

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

    def write(self, filename):
        dos_header = bytearray(64)
        dos_header[0:2] = b"MZ"
        struct.pack_into("<I", dos_header, 0x3C, 0x80)

        dos_stub = bytearray(0x80 - len(dos_header))

        pe_sig = b"PE\x00\x00"

        number_of_sections      = 3
        size_of_optional_header = 0xF0
        section_header_size     = 40

        file_header = struct.pack(
            "<HHIIIHH",
            0x8664,
            number_of_sections,
            int(time.time()),
            0,
            0,
            size_of_optional_header,
            0x0022
        )

        headers_size = self.align(0x80 + 4 + 20 +
            size_of_optional_header + number_of_sections * section_header_size,
            self.FILE_ALIGNMENT
        )

        text_image          = self.build_text_with_import_thunks()

        text_rva            = self.SECTION_ALIGN
        entry_rva           = text_rva + self.find_entrypoint()

        text_raw            = headers_size
        text_raw_size       = self.align(len(text_image), self.FILE_ALIGNMENT)
        text_virtual_size   = len(text_image)
        
        data_rva            = self.align(text_rva + text_virtual_size, self.SECTION_ALIGN)
        data_raw            = text_raw + text_raw_size
        data_raw_size       = self.align(len(self.data), self.FILE_ALIGNMENT)
        data_virtual_size   = len(self.data)
        
        idata_rva           = self.align(data_rva + data_virtual_size, self.SECTION_ALIGN)
        idata_raw           = data_raw + data_raw_size
        idata               = self.build_import_section(idata_rva)

        data_image          = bytearray(self.data)

        self.patch_internal_relocations(
            text_image,
            data_image,
            text_rva,
            data_rva
        )

        self.patch_external_call_relocations(text_image, text_rva)
        self.patch_import_thunks(text_image, text_rva)
        
        idata_raw_size      = self.align(len(idata), self.FILE_ALIGNMENT)
        idata_virtual_size  = len(idata)
        
        size_of_image = self.align(
            idata_rva + idata_virtual_size,
            self.SECTION_ALIGN
        )

        optional_header     = bytearray()

        optional_header += struct.pack("<H", 0x20B)      # PE32+
        optional_header += struct.pack("<BB", 14, 0)     # linker version
        optional_header += struct.pack("<III",
            text_raw_size, 0, 0
        )

        optional_header += struct.pack("<I", entry_rva)  # AddressOfEntryPoint
        optional_header += struct.pack("<I", text_rva)   # BaseOfCode
        optional_header += struct.pack("<Q", self.IMAGE_BASE)

        optional_header += struct.pack("<II",
            self.SECTION_ALIGN,
            self.FILE_ALIGNMENT
        )

        optional_header += struct.pack("<HHHHHH",
            6, 0,    # OS version
            0, 0,    # Image version
            6, 0     # Subsystem version
        )

        optional_header += struct.pack("<I", 0)          # Win32VersionValue
        optional_header += struct.pack("<I", size_of_image)
        optional_header += struct.pack("<I", headers_size)
        optional_header += struct.pack("<I", 0)          # Checksum

        optional_header += struct.pack("<HH",
            3,       # Windows CUI
            0x8160   # DLL characteristics
        )

        optional_header += struct.pack("<QQQQ",
            0x100000,  # SizeOfStackReserve
            0x1000,    # SizeOfStackCommit
            0x100000,  # SizeOfHeapReserve
            0x1000     # SizeOfHeapCommit
        )

        optional_header += struct.pack("<II",
            0,      # LoaderFlags
            16      # NumberOfRvaAndSizes
        )

        data_directories = bytearray(16 * 8)
        struct.pack_into(
            "<II",
            data_directories,
            1 * 8,        # Import Directory
            idata_rva,
            len(idata)
        )
        
        optional_header += data_directories

        if len(optional_header) != size_of_optional_header:
            raise RuntimeError(len(optional_header))

        text_section_header = struct.pack(
            "<8sIIIIIIHHI",
            b".text\x00\x00\x00",
            text_virtual_size,
            text_rva,
            text_raw_size,
            text_raw,
            0,
            0,
            0,
            0,
            0x60000020
        )

        data_section_header = struct.pack(
            "<8sIIIIIIHHI",
            b".data\x00\x00\x00",
            data_virtual_size,
            data_rva,
            data_raw_size,
            data_raw,
            0,
            0,
            0,
            0,
            0xC0000040
        )
        
        idat_section_header = struct.pack(
            "<8sIIIIIIHHI",
            b".idata\x00\x00",
            idata_virtual_size,
            idata_rva,
            idata_raw_size,
            idata_raw,
            0,
            0,
            0,
            0,
            0xC0000040
        )
        
        image  = bytearray()
        image += dos_header
        image += dos_stub
        
        image += pe_sig
        image += file_header
        image += optional_header
        
        image += text_section_header
        image += data_section_header
        image += idat_section_header

        self.pad_to(image, text_raw)
        
        image += text_image; self.pad_to( image,  text_raw +  text_raw_size )
        image += data_image; self.pad_to( image,  data_raw +  data_raw_size )
        image +=      idata; self.pad_to( image, idata_raw + idata_raw_size )

        with open(filename, "wb") as f:
            f.write(image)
