from __future__ import annotations

import struct
import unittest

from rccompiler.coff import build_coff32_resource_object
from rccompiler.model import ResourceRecord
from rccompiler.resource_tree import build_resource_section


class CoffResourceTests(unittest.TestCase):
    def test_coff_header_and_relocations(self):
        records = [
            ResourceRecord(10, 1, 0x0407, b"abc"),
            ResourceRecord(6, 63, 0x0407, b"defgh"),
            ResourceRecord("CUSTOM", "NAME", 0, b"xyz"),
        ]
        section = build_resource_section(records)
        self.assertEqual(len(section.relocation_offsets), 3)
        obj = build_coff32_resource_object(section)

        machine, section_count, timestamp, symptr, symcount, optsize, flags = (
            struct.unpack_from("<HHIIIHH", obj, 0)
        )
        self.assertEqual(machine, 0x014C)
        self.assertEqual(section_count, 1)
        self.assertEqual(timestamp, 0)
        self.assertEqual(symcount, 2)
        self.assertEqual(optsize, 0)
        self.assertGreater(symptr, 60)

        name = struct.unpack_from("<8s", obj, 20)[0].rstrip(b"\x00")
        self.assertEqual(name, b".rsrc")
        raw_size, raw_pointer, reloc_pointer = struct.unpack_from("<III", obj, 36)
        self.assertEqual(raw_size, len(section.data))
        self.assertEqual(raw_pointer, 60)
        self.assertEqual(reloc_pointer, 60 + len(section.data))

        for index, expected_offset in enumerate(section.relocation_offsets):
            offset, symbol_index, relocation_type = struct.unpack_from(
                "<IIH",
                obj,
                reloc_pointer + index * 10,
            )
            self.assertEqual(offset, expected_offset)
            self.assertEqual(symbol_index, 0)
            self.assertEqual(relocation_type, 0x0007)


if __name__ == "__main__":
    unittest.main()
