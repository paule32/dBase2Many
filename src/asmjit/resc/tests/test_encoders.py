from __future__ import annotations

import unittest

from rccompiler.encoders import (
    ResourceEncoder,
    encode_accelerators,
    encode_dialog,
    encode_menu,
    encode_version_info,
)
from rccompiler.model import (
    AcceleratorEntry,
    AcceleratorResource,
    DialogControl,
    DialogFont,
    DialogResource,
    MenuItem,
    MenuResource,
    ResourceOptions,
    SourceLocation,
    StringTable,
    VersionBlock,
    VersionInfo,
    VersionValue,
)


LOC = SourceLocation("test.rc", 1, 0)
OPT = ResourceOptions(language=0x0407)


class EncoderTests(unittest.TestCase):
    def test_stringtable_groups(self):
        encoder = ResourceEncoder()
        records = encoder.encode(type("U", (), {
            "resources": [StringTable({0: "A", 17: "B"}, OPT, LOC)]
        })())
        self.assertEqual([(r.type_id, r.name_id) for r in records], [(6, 1), (6, 2)])

    def test_version_info(self):
        resource = VersionInfo(
            name_id=1,
            options=OPT,
            file_version=(1, 2, 3, 4),
            children=[
                VersionBlock("StringFileInfo", [
                    VersionBlock("040704E4", [
                        VersionValue("FileDescription", ["Test\0"]),
                    ])
                ]),
                VersionBlock("VarFileInfo", [
                    VersionValue("Translation", [0x0407, 1252]),
                ]),
            ],
            location=LOC,
        )
        data = encode_version_info(resource)
        self.assertEqual(int.from_bytes(data[0:2], "little"), len(data))
        self.assertIn("VS_VERSION_INFO".encode("utf-16le"), data)
        self.assertIn("FileDescription".encode("utf-16le"), data)

    def test_menu_accel_dialog(self):
        menu = MenuResource(
            1,
            False,
            [MenuItem("File", popup=True, children=[MenuItem("Exit", 10)])],
            OPT,
            LOC,
        )
        self.assertGreater(len(encode_menu(menu)), 12)

        accel = AcceleratorResource(
            2,
            [AcceleratorEntry(ord("Q"), 10, 0x09)],
            OPT,
            LOC,
        )
        self.assertEqual(len(encode_accelerators(accel)), 8)

        dialog = DialogResource(
            name_id=3,
            extended=True,
            x=0, y=0, width=100, height=50,
            style=0x90C800C0,
            caption="Test",
            font=DialogFont(9, "Segoe UI", 400, 0, 1),
            controls=[
                DialogControl(
                    "PUSHBUTTON", "OK", 1, 0x80,
                    0x50010001, 0, 20, 20, 40, 14,
                )
            ],
            options=OPT,
            location=LOC,
        )
        data = encode_dialog(dialog)
        self.assertEqual(data[0:4], b"\x01\x00\xff\xff")
        self.assertIn("Segoe UI".encode("utf-16le"), data)


if __name__ == "__main__":
    unittest.main()
