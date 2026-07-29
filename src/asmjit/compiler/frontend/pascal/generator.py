# ---------------------------------------------------------------------------
# File: generator.py - Pascal Compiler
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

import os
import sys
import re
import json

from pathlib     import Path
from dataclasses import dataclass, field
from antlr4      import *

from compiler.frontend.pascal.preprocessor   import PascalPreprocessor
from compiler.frontend.dllimports            import *

from parsers.pascal.PascalLexer          import PascalLexer
from parsers.pascal.PascalParser         import PascalParser
from parsers.pascal.PascalParserVisitor  import PascalParserVisitor

from compiler.common.error     import *
from compiler.common.types     import *
from compiler.common.constants import *

from compiler.writer.nt32 import *
from compiler.writer.pe32 import *
from compiler.writer.pe64 import *

from compiler.writer.pe64coff  import *

from compiler.common.constants import (
    LIBDBASE2MANY32_IMPORT_ORDINALS
)

# ---------------------------------------------------------------------------
# NT32 descriptor used for Pascal ``array of const``.
#
# Layout (12 bytes):
#   +0  kind       (uint32)
#   +4  value_low  (uint32)
#   +8  value_high (uint32)
# ---------------------------------------------------------------------------
JIT_VARIANT_EMPTY   = 0
JIT_VARIANT_INTEGER = 1
JIT_VARIANT_BOOLEAN = 2
JIT_VARIANT_CHAR    = 3
JIT_VARIANT_STRING  = 4
JIT_VARIANT_DOUBLE  = 5
JIT_VARIANT_POINTER = 6

JIT_VARIANT_ARG_SIZE    = 12
JIT_VARIANT_KIND_OFFSET = 0
JIT_VARIANT_LOW_OFFSET  = 4
JIT_VARIANT_HIGH_OFFSET = 8

class PropertyInfo:
    def __init__(self, name, ptype, visibility, read_name=None, write_name=None):
        self.name       = name
        self.ptype      = ptype
        self.visibility = visibility
        self.read_name  = read_name
        self.write_name = write_name

def normalize_unit_name(
    unit_name
):
    return (
        str(unit_name)
        .strip()
        .lower()
        .replace(".", "_")
    )


def pui_search_directories(
    source_file
):
    """
    Liefert alle Verzeichnisse, in denen PUI-Dateien gesucht werden.
    """

    directories = []
    seen = set()

    def add_directory(path):
        if not path:
            return

        try:
            path = os.fspath(path)
        except TypeError:
            return

        path = path.strip()

        if not path:
            return

        path = os.path.abspath(
            os.path.expandvars(
                os.path.expanduser(path)
            )
        )

        if not os.path.isdir(path):
            return

        key = os.path.normcase(
            os.path.normpath(path)
        )

        if key in seen:
            return

        seen.add(key)
        directories.append(path)

    def add_file_parent(filename):
        if not filename:
            return

        try:
            filename = os.fspath(filename)
        except TypeError:
            return

        filename = filename.strip()

        if not filename:
            return

        add_directory(
            os.path.dirname(
                os.path.abspath(filename)
            )
        )

    # Verzeichnis der aktuell kompilierten Quelldatei.
    if source_file:
        add_file_parent(source_file)

    # Aktuelles Arbeitsverzeichnis.
    add_directory(
        os.getcwd()
    )

    # Explizites Ausgabeverzeichnis.
    output_directory = getattr(
        CDATA,
        "output_dir",
        None
    )

    add_directory(
        output_directory
    )

    # Konventionelles Projekt-Ausgabeverzeichnis.
    add_directory(
        os.path.join(
            os.getcwd(),
            "testout"
        )
    )

    # Verzeichnisse bekannter Ausgabedateien.
    for attribute_name in (
        "obj_file",
        "object_file",
        "pui_file",
        "exe_file",
        "dll_file",
        "asm_file",
        "output_file"
    ):
        add_file_parent(
            getattr(
                CDATA,
                attribute_name,
                None
            )
        )

    # Unit- und Include-Pfade.
    for attribute_name in (
        "UnitPaths",
        "IncludePaths"
    ):
        paths = getattr(
            CDATA,
            attribute_name,
            []
        ) or []

        for path in paths:
            add_directory(path)

    # Explizite Unit-Dateien oder Unit-Verzeichnisse.
    for item in getattr(
        CDATA,
        "UnitFiles",
        []
    ) or []:
        try:
            item_path = os.path.abspath(
                os.fspath(item)
            )
        except TypeError:
            continue

        if os.path.isdir(item_path):
            add_directory(item_path)

        elif os.path.isfile(item_path):
            add_directory(
                os.path.dirname(item_path)
            )

    return directories


def find_unit_pui_for_preprocessor(
    unit_name,
    source_file
):
    """
    Sucht die PUI einer Unit, bevor Lexer und Parser gestartet werden.
    """

    unit_name = str(
        unit_name
    ).strip()

    normalized_name = normalize_unit_name(
        unit_name
    )

    last_part = unit_name.split(".")[-1]

    candidate_names = []

    def add_candidate(name):
        if name and name not in candidate_names:
            candidate_names.append(name)

    add_candidate(
        unit_name + ".pui"
    )

    add_candidate(
        unit_name.lower() + ".pui"
    )

    add_candidate(
        normalized_name + ".pui"
    )

    add_candidate(
        normalized_name.lower() + ".pui"
    )

    add_candidate(
        last_part + ".pui"
    )

    add_candidate(
        last_part.lower() + ".pui"
    )

    search_directories = pui_search_directories(
        source_file
    )

    # Schneller Weg über bekannte Dateinamen.
    for directory in search_directories:
        for candidate_name in candidate_names:
            candidate = os.path.abspath(
                os.path.join(
                    directory,
                    candidate_name
                )
            )

            if os.path.isfile(candidate):
                return candidate

    # Fallback: alle PUI-Dateien öffnen und Unit-Namen prüfen.
    for directory in search_directories:
        try:
            entries = os.listdir(
                directory
            )
        except OSError:
            continue

        for entry in entries:
            if not entry.lower().endswith(".pui"):
                continue

            candidate = os.path.abspath(
                os.path.join(
                    directory,
                    entry
                )
            )

            try:
                with open(
                    candidate,
                    "r",
                    encoding="utf-8"
                ) as stream:
                    data = json.load(
                        stream
                    )

            except (
                OSError,
                ValueError,
                TypeError
            ):
                continue

            unit_info = data.get(
                "unit",
                {}
            )

            if not isinstance(
                unit_info,
                dict
            ):
                continue

            stored_name = unit_info.get(
                "normalized_name"
            )

            if not stored_name:
                stored_name = normalize_unit_name(
                    unit_info.get(
                        "name",
                        ""
                    )
                )

            if (
                str(stored_name).lower()
                == normalized_name.lower()
            ):
                return candidate

    return None


def load_pui_data(
    pui_filename
):
    try:
        with open(
            pui_filename,
            "r",
            encoding="utf-8"
        ) as stream:
            data = json.load(
                stream
            )

    except OSError as exc:
        raise PascalPreprocessorError(
            f"could not read PUI file "
            f"{pui_filename}: {exc}"
        ) from None

    except (
        ValueError,
        TypeError
    ) as exc:
        raise PascalPreprocessorError(
            f"invalid PUI file "
            f"{pui_filename}: {exc}"
        ) from None

    if not isinstance(
        data,
        dict
    ):
        raise PascalPreprocessorError(
            f"invalid PUI root object: "
            f"{pui_filename}"
        )

    return data


def merge_imported_macro(
    result,
    owners,
    macro_name,
    macro_value,
    unit_name
):
    """
    Fügt ein PUI-Makro ein und erkennt Namenskonflikte.
    """

    name = str(
        macro_name
    ).strip().upper()

    if not name:
        raise PascalPreprocessorError(
            f"empty macro name in unit "
            f"{unit_name}"
        )

    if name in result:
        old_value = result[name]

        # Identische Definitionen sind unproblematisch.
        if old_value == macro_value:
            return

        old_owner = owners.get(
            name,
            "<unknown>"
        )

        raise PascalPreprocessorError(
            f"conflicting imported macro {name}: "
            f"{old_owner} defines {old_value!r}, "
            f"{unit_name} defines {macro_value!r}"
        )

    result[name] = macro_value
    owners[name] = unit_name


def collect_pui_macros_recursive(
    unit_name,
    source_file,
    result,
    owners,
    visited,
    loading
):
    """
    Lädt Makros einer PUI und ihrer öffentlichen Interface-Abhängigkeiten.
    """

    unit_key = normalize_unit_name(
        unit_name
    )

    if unit_key in visited:
        return

    if unit_key in loading:
        chain = " -> ".join(
            list(loading) + [unit_key]
        )

        raise PascalPreprocessorError(
            f"circular PUI macro dependency: "
            f"{chain}"
        )

    pui_filename = find_unit_pui_for_preprocessor(
        unit_name,
        source_file
    )

    if pui_filename is None:
        # Die normale Unit-Auflösung erzeugt später eine genauere
        # Meldung. Hier wird die Unit zunächst übersprungen.
        return

    loading.add(
        unit_key
    )

    try:
        data = load_pui_data(
            pui_filename
        )

        # Nur öffentliche Interface-Abhängigkeiten rekursiv exportieren.
        #
        # Implementation-Units sind private Abhängigkeiten und sollen
        # ihre Makros nicht an Benutzer dieser Unit weiterreichen.
        uses_info = data.get(
            "uses",
            {}
        )

        if isinstance(
            uses_info,
            dict
        ):
            dependencies = uses_info.get(
                "interface",
                []
            ) or []
        else:
            dependencies = []

        for dependency in dependencies:
            collect_pui_macros_recursive(
                unit_name=dependency,
                source_file=source_file,
                result=result,
                owners=owners,
                visited=visited,
                loading=loading
            )

        macros = data.get(
            "macros",
            {}
        )

        if macros is None:
            macros = {}

        if not isinstance(
            macros,
            dict
        ):
            raise PascalPreprocessorError(
                f"invalid macros section in "
                f"{pui_filename}"
            )

        for macro_name, macro_value in macros.items():
            merge_imported_macro(
                result=result,
                owners=owners,
                macro_name=macro_name,
                macro_value=macro_value,
                unit_name=unit_name
            )

        visited.add(
            unit_key
        )

    finally:
        loading.discard(
            unit_key
        )

# ---------------------------------------------------------------------------
# Liest einfache Pascal-USES-Klauseln vor dem eigentlichen Parser.
#
# Unterstützt beispielsweise:
#
#    uses System.Types;
#    uses System.Types, VCL.Windows;
# ---------------------------------------------------------------------------
def extract_uses_units(source_text):
    units = []

    matches = re.finditer(
        r"\buses\b(.*?);",
        source_text,
        re.IGNORECASE | re.DOTALL
    )

    for match in matches:
        content = match.group(1)

        for item in content.split(","):
            item = item.strip()

            if not item:
                continue

            # Unterstützung für:
            #
            #     UnitName in 'datei.pas'
            item = re.split(
                r"\s+in\s+",
                item,
                maxsplit=1,
                flags=re.IGNORECASE
            )[0].strip()

            if re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_.]*",
                item
            ):
                units.append(item)

    return units
    
# ----------------------------------------------------------------------
# Sammelt alle Makros aus den PUIs der direkt verwendeten Units.
# Dieser Schritt muss vor PascalPreprocessor.process() erfolgen.
# ----------------------------------------------------------------------
def collect_used_unit_macros(
    raw_source,
    source_file
):
    result = {}
    owners = {}
    visited = set()
    loading = set()

    unit_names = extract_uses_units(
        raw_source
    )

    for unit_name in unit_names:
        collect_pui_macros_recursive(
            unit_name=unit_name,
            source_file=source_file,
            result=result,
            owners=owners,
            visited=visited,
            loading=loading
        )

    return result
    
# ---------------------------------------------------------------------------
# the transpiler generator for Pascal->Assembly
# ---------------------------------------------------------------------------
class AsmJitGenerator(PascalParserVisitor):
    def __init__(self, backend=None):
        self.backend = backend or AsmJitBackend()   # default backend
        self.lines   = self.backend.lines
        
        self.subrange_types     = {}
        self.vars               = {}
        self.next_slot          = 0
        self.program_name       = "Program"
        self.var_types          = {}
        self.cpp_print_lines    = []
        
        self.source_file       = None
        self.source_dir        = None
        
        self.loaded_units      = {}
        self.loaded_puis       = {}
        self.loading_units     = set()
        self.unit_init_labels  = []
        self.current_unit      = None
        
        self.vars               = {}
        self.var_types          = {}

        self.int_slots          = {}
        self.double_slots       = {}

        self.next_int_slot      = 0
        self.next_double_slot   = 0
        self.next_string_slot   = 0
        self.next_record_slot   = 0
        self.next_arrays_slot   = 0
        self.next_pointr_slot   = 0
        
        self.label_id           = 0
        
        self.string_literals    = []
        self.double_literals    = []
        
        self.procedures         = {}
        self.functions          = {}
        self.constants          = {}
        self.variables          = []
        self.enums              = {}
        self.records            = {}
        self.arrays             = {}
        self.classes            = {}
        self.pui_class_units    = {}
        
        self.current_class  = None
        self.current_method = None
        
        self.type_aliases       = {}
        self.pointer_types      = {}
        
        self.scope_stack        = []
        
        self.local_var_stack    = []
        self.local_const_stack  = []
        self.exit_label_stack   = []
        self.try_except_stack   = []
        
        self.break_label_stack    = []
        self.continue_label_stack = []

        self.asm_label_mappings = []
        
        self.current_function   = None
        self.current_proc_params= {}
        
        self.next_variant_array_id = 0
        self.next_const_array_id   = 0
        self.pending_open_array_actual = None
        
        self.section_text = []
        self.section_data = []
        
        self.constants["true"] = {
            "name": "True",
            "type": "boolean",
            "value": 1
        }

        self.constants["false"] = {
            "name": "False",
            "type": "boolean",
            "value": 0
        }
        
        self.dll_import_symbols = {}
        self.next_dll_import_id = 0

        # ------------------------------------------------------------------
        # Root-Modul und PUI-Verwaltung
        # ------------------------------------------------------------------
        self.source_file_depth = 0

        self.root_module_kind = None
        self.root_unit_name   = None

        self.root_link_objects   = []
        self.root_link_archives  = []
        self.root_resource_files = []
        
        # COFF-Dateien, die physisch in die erzeugte Unit-.o-Datei
        # übernommen werden sollen.
        self.root_embedded_objects = []

        self.pending_pui = None
        self.collect_pui_interface = False

        self.asm_file               = CDATA.asm_file
        self.emit_local_string_data = True
        
        # Makros, die direkt in der aktuell kompilierten Unit
        # durch {$DEFINE ...} festgelegt wurden.
        self.unit_source_macros = {}
        
        self.module_kind        = "program"
        self.module_kind_value  = 1
        
        self.exports = []
    
    def format_error(self, filename, err):
        template = ERROR_MAP.get(err.code, err.code)
        message  = template.format(**err.params)
        
        return f"{err.code}: {os.path.basename(filename)} {err.line}:{err.column} {message}"

    def is_pointer_type(
        self,
        type_name,
        include_nil=False
    ):
        if type_name is None:
            return False

        current = type_name

        visited = set()

        while isinstance(
            current,
            str
        ):
            key = current.lower()

            if key in visited:
                break

            visited.add(key)

            if include_nil and key == "nil":
                return True

            if key in (
                "pointer",
                "pchar",
                "pansichar"
            ):
                return True

            if key.startswith("^"):
                return True

            resolved = self.resolve_type(
                current
            )

            if (
                resolved is None
                or resolved == current
            ):
                break

            current = resolved

        return False

    def is_char_pointer_type(self, type_name):
        """
        True for PChar/PAnsiChar and aliases that resolve to ^Char.
        """
        resolved_type = self.resolve_type(
            type_name
        )

        if resolved_type in (
            "pchar",
            "pansichar"
        ):
            return True

        if (
            isinstance(
                resolved_type,
                str
            )
            and resolved_type.startswith("^")
        ):
            pointed_type = self.resolve_type(
                resolved_type[1:]
            )

            return pointed_type == "char"

        return False

    def is_packed_runtime_library(self, dll_name):
        if not getattr(
            CDATA,
            "packed_runtime",
            False
        ):
            return False

        normalized = os.path.basename(
            str(dll_name).strip()
        ).lower()

        packed_libraries = getattr(
            CDATA,
            "packed_runtime_libraries",
            None
        )

        if packed_libraries is None:
            packed_libraries = {
                #"libruntime_mini.dll",
                "libruntime_all.dll",
                "libdbase2many.32.dll",
            }

        packed_libraries = {
            os.path.basename(
                str(name).strip()
            ).lower()
            for name in packed_libraries
        }

        return normalized in packed_libraries

    def class_is_descendant(
        self,
        actual_type,
        expected_type
    ):
        actual = self.resolve_type(actual_type)
        expected = self.resolve_type(expected_type)

        if actual == expected:
            return True

        current = actual

        while current in self.classes:
            current = self.classes[current].parent

            if current == expected:
                return True

            if current is None:
                break

        return False

    def is_class_type(self, type_name):
        resolved = self.resolve_type(type_name)

        return (
            isinstance(resolved, str)
            and resolved in self.classes
        )

    def is_nil_type(self, type_name):
        return self.resolve_type(type_name) in (
            "nil",
            "^nil"
        )

    def class_assignment_compatible(
        self,
        actual_type,
        expected_type
    ):
        actual = self.resolve_type(actual_type)
        expected = self.resolve_type(expected_type)

        if self.is_nil_type(actual):
            return True

        if not (
            self.is_class_type(actual)
            and self.is_class_type(expected)
        ):
            return False

        return self.class_is_descendant(
            actual,
            expected
        )

    def pointer_assignment_compatible(
        self,
        actual_type,
        expected_type
    ):
        actual = self.resolve_type(actual_type)
        expected = self.resolve_type(expected_type)

        if self.is_nil_type(actual):
            return True

        if not self.is_pointer_type(
            expected,
            include_nil=False
        ):
            return False

        if self.is_pointer_type(
            actual,
            include_nil=False
        ):
            return True

        # An untyped Pointer may hold an object address. Typed pointers
        # still require an explicit cast for a class reference.
        return (
            expected == "pointer"
            and self.is_class_type(actual)
        )
    

    def external_import_name(
        self,
        spec_ctx
    ):
        accessor = getattr(
            spec_ctx,
            "externalNameClause",
            None
        )

        if accessor is None:
            return None

        clause = accessor()

        if clause is None:
            return None

        token = clause.STRING()

        if token is None:
            return None

        value = self.pascal_token_string(
            token
        )

        if not value:
            raise CompileError(
                spec_ctx,
                "E0019",
                text="external import name must not be empty"
            )

        return value


    def external_import_ordinal(
        self,
        spec_ctx
    ):
        accessor = getattr(
            spec_ctx,
            "externalOrdinalClause",
            None
        )

        if accessor is None:
            return None

        clause = accessor()

        if clause is None:
            return None

        token = clause.NUMBER()

        if token is None:
            raise CompileError(
                spec_ctx,
                "E0019",
                text="external ordinal has no numeric value"
            )

        try:
            ordinal = int(
                token.getText(),
                10
            )
        except ValueError:
            raise CompileError(
                spec_ctx,
                "E0019",
                text=(
                    "invalid external ordinal: "
                    + token.getText()
                )
            ) from None

        if not 1 <= ordinal <= 0xFFFF:
            raise CompileError(
                spec_ctx,
                "E0019",
                text=(
                    f"external ordinal {ordinal} "
                    "must be in range 1..65535"
                )
            )

        return ordinal

    def class_metadata_symbol(
        self,
        class_name,
        kind
    ):
        scope_name = (
            self.current_unit
            if self.current_unit
            else self.program_name
        )

        safe_scope = re.sub(
            r"[^A-Za-z0-9_]",
            "_",
            str(scope_name).lower()
        )

        safe_class = re.sub(
            r"[^A-Za-z0-9_]",
            "_",
            str(class_name).lower()
        )

        return (
            f"__{kind}_{safe_scope}_{safe_class}"
        )

    def configure_class_vmt_metadata(
        self,
        ctx,
        class_key,
        vmt_symbol=None,
        class_name_symbol=None
    ):
        """
        VMT-Layout NT32:

            +0   Parent
            +4   ClassName
            +8   InstanceSize
            +12  Init
            +16  Finalize
            +20  Destroy
            +24  erste normale virtuelle Methode
        """
        cls = self.classes[
            class_key
        ]

        cls.vmt_symbol = (
            vmt_symbol
            or self.class_metadata_symbol(
                cls.name,
                "vmt"
            )
        )

        cls.class_name_symbol = (
            class_name_symbol
            or self.class_metadata_symbol(
                cls.name,
                "classname"
            )
        )

        parent_cls = (
            self.classes.get(
                cls.parent
            )
            if cls.parent
            else None
        )

        slots = list(
            getattr(
                parent_cls,
                "vmt_slots",
                []
            )
            if parent_cls is not None
            else []
        )

        destroy_method = (
            getattr(
                parent_cls,
                "vmt_destroy",
                None
            )
            if parent_cls is not None
            else None
        )

        def signature_key(method):
            return (
                str(method.name).lower(),
                self.method_signature(
                    method.params
                )
            )

        slot_indexes = {
            signature_key(method): index
            for index, method in enumerate(
                slots
            )
        }

        for overloads in cls.methods.values():
            for method in overloads:
                if method.owner != class_key:
                    continue

                is_virtual = bool(
                    getattr(
                        method,
                        "is_virtual",
                        False
                    )
                )

                is_override = bool(
                    getattr(
                        method,
                        "is_override",
                        False
                    )
                )

                if method.kind == "destructor":
                    if is_override:
                        if destroy_method is None:
                            raise CompileError(
                                ctx,
                                "E0019",
                                text=(
                                    f"{cls.name}.{method.name} "
                                    "uses override but the parent "
                                    "has no virtual destructor"
                                )
                            )

                        is_virtual = True

                    if is_virtual:
                        method.is_virtual = True
                        method.vmt_offset = 20
                        destroy_method = method
                    else:
                        method.is_virtual = False
                        method.vmt_offset = None

                    continue

                key = signature_key(
                    method
                )

                inherited_index = (
                    slot_indexes.get(
                        key
                    )
                )

                if is_override:
                    if inherited_index is None:
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                f"{cls.name}.{method.name} "
                                "uses override but no matching "
                                "virtual parent method exists"
                            )
                        )

                    is_virtual = True

                if not is_virtual:
                    method.is_virtual = False
                    method.vmt_offset = None
                    continue

                method.is_virtual = True

                if inherited_index is not None:
                    method.vmt_offset = (
                        24
                        + inherited_index * 4
                    )

                    slots[
                        inherited_index
                    ] = method

                else:
                    method.vmt_offset = (
                        24
                        + len(slots) * 4
                    )

                    slot_indexes[
                        key
                    ] = len(slots)

                    slots.append(
                        method
                    )

        cls.vmt_destroy = destroy_method
        cls.vmt_slots = slots

    def emit_class_vmt_data(
        self,
        class_name
    ):
        if not hasattr(
            self,
            "emitted_class_vmts"
        ):
            self.emitted_class_vmts = set()

        cls = self.classes[
            class_name.lower()
        ]

        # Der Cache darf nur dann als Treffer gelten, wenn das COFF-Symbol
        # im aktuell verwendeten Writer wirklich vorhanden ist. Das ist
        # wichtig, wenn ein Generator/Writer während mehrerer Unit-Schritte
        # erneut verwendet wird.
        if (
            cls.vmt_symbol in self.emitted_class_vmts
            and self.writer.find_symbol_index(
                cls.vmt_symbol
            ) is not None
        ):
            return

        self.emitted_class_vmts.discard(
            cls.vmt_symbol
        )

        self.emitted_class_vmts.add(
            cls.vmt_symbol
        )

        self.writer.add_data_string(
            cls.class_name_symbol,
            cls.name
        )

        # Eine VMT besteht aus zusammenhängenden 32-Bit-Slots.
        #
        # add_data_string() richtet das Ende nicht automatisch aus.
        # Ohne dieses Alignment könnte die VMT beispielsweise bei
        # 0x402005 beginnen. add_data_u32() fügt später Padding ein,
        # wodurch die fest definierten Offsets +8, +20 und +24 nicht
        # mehr stimmen.
        self.writer.align_data(
            4
        )

        vmt_start = len(
            self.writer.data
        )

        self.writer.add_data_label(
            cls.vmt_symbol
        )

        # +0 Parent
        if cls.parent:
            parent_cls = self.classes[
                cls.parent
            ]

            self.writer.add_data_i32_symbol_ref(
                parent_cls.vmt_symbol
            )
        else:
            self.writer.add_data_u32(
                0
            )

        # +4 ClassName
        self.writer.add_data_i32_symbol_ref(
            cls.class_name_symbol
        )

        # +8 InstanceSize
        self.writer.add_data_u32(
            cls.size
        )

        # +12 Init
        self.writer.add_data_u32(
            0
        )

        # +16 Finalize
        self.writer.add_data_u32(
            0
        )

        # +20 Destroy
        if cls.vmt_destroy is not None:
            target = (
                cls.vmt_destroy.label
                or cls.vmt_destroy.mangled
            )

            self.writer.add_data_i32_symbol_ref(
                target
            )
        else:
            self.writer.add_data_u32(
                0
            )

        # +24 virtuelle Slots
        for method in cls.vmt_slots:
            target = (
                method.label
                or method.mangled
            )

            self.writer.add_data_i32_symbol_ref(
                target
            )

        expected_vmt_size = (
            24
            + len(cls.vmt_slots) * 4
        )

        actual_vmt_size = (
            len(self.writer.data)
            - vmt_start
        )

        if actual_vmt_size != expected_vmt_size:
            raise RuntimeError(
                f"invalid VMT layout for {cls.name}: "
                f"expected {expected_vmt_size} bytes, "
                f"got {actual_vmt_size} bytes"
            )

    def ensure_class_vmt_reference(
        self,
        ctx,
        class_name
    ):
        class_key = str(
            class_name
        ).lower()

        cls = self.classes[
            class_key
        ]

        symbol = cls.vmt_symbol

        if self.writer.find_symbol_index(
            symbol
        ) is None:
            if class_key in self.pui_class_units:
                # Die VMT gehört zu einer bereits kompilierten Unit.
                # Ihr COFF-Objekt wird über die PUI eingebunden; hier wird
                # deshalb nur ein undefiniertes externes Symbol für die
                # DIR32-Relocation benötigt.
                add_external = getattr(
                    self.writer,
                    "find_or_add_external",
                    None
                )

                if add_external is None:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "backend cannot reference external "
                            f"class VMT: {symbol}"
                        )
                    )

                add_external(
                    symbol
                )
            else:
                # Lokale Klassen besitzen ihre VMT in der aktuellen
                # Objektdatei. Falls der Deklarationsdurchlauf das Symbol
                # nicht mehr im Writer hinterlassen hat, wird es hier vor
                # dem ersten Konstruktorzugriff zuverlässig erzeugt.
                self.emit_class_vmt_data(
                    class_name
                )

        if self.writer.find_symbol_index(
            symbol
        ) is None:
            raise RuntimeError(
                "class VMT symbol was not registered: "
                + symbol
            )

        return symbol

    def method_directive_flags(
        self,
        declaration_ctx
    ):
        result = {
            "virtual": False,
            "override": False
        }

        directive_list = (
            declaration_ctx.methodDirectiveList()
            if hasattr(
                declaration_ctx,
                "methodDirectiveList"
            )
            else None
        )

        if directive_list is None:
            return result

        for directive in directive_list.methodDirective():
            value = directive.getText().lower()

            if value == "virtual":
                result["virtual"] = True

            elif value == "override":
                result["override"] = True

        return result

    def find_unit_file(self, ctx, unit_name):
        unit_name = str(unit_name).strip()

        if not unit_name:
            raise CompileError(
                ctx,
                "E0019",
                text="empty unit name"
            )

        dotted_name = unit_name

        namespace_path = unit_name.replace(
            ".",
            os.sep
        )

        candidates = [
            dotted_name + ".pas",
            dotted_name + ".pp",

            dotted_name.lower() + ".pas",
            dotted_name.lower() + ".pp",

            namespace_path + ".pas",
            namespace_path + ".pp",

            namespace_path.lower() + ".pas",
            namespace_path.lower() + ".pp"
        ]

        # Doppelte Einträge entfernen
        candidates = list(
            dict.fromkeys(candidates)
        )

        search_dirs = []
        seen_dirs = set()

        def add_directory(path):
            if not path:
                return

            try:
                path = os.fspath(path)
            except TypeError:
                return

            path = path.strip()

            if not path:
                return

            path = os.path.abspath(
                os.path.expandvars(
                    os.path.expanduser(path)
                )
            )

            if not os.path.isdir(path):
                return

            key = os.path.normcase(
                os.path.normpath(path)
            )

            if key in seen_dirs:
                return

            seen_dirs.add(key)
            search_dirs.append(path)

        # Verzeichnis der aktuellen Quelldatei
        add_directory(
            self.source_dir
        )

        if self.source_file:
            add_directory(
                os.path.dirname(
                    os.path.abspath(
                        self.source_file
                    )
                )
            )

        # Aktuelles Arbeitsverzeichnis
        add_directory(
            os.getcwd()
        )

        # -Fu- und Include-Pfade
        for attribute_name in (
            "UnitPaths",
            "IncludePaths"
        ):
            paths = getattr(
                CDATA,
                attribute_name,
                []
            ) or []

            for path in paths:
                add_directory(path)

        # Explizit eingetragene Unit-Dateien
        for item in getattr(
            CDATA,
            "UnitFiles",
            []
        ) or []:
            try:
                item_path = os.path.abspath(
                    os.fspath(item)
                )
            except TypeError:
                continue

            if os.path.isfile(item_path):
                base_name = os.path.splitext(
                    os.path.basename(item_path)
                )[0]

                normalized_base = (
                    base_name
                    .lower()
                    .replace("_", ".")
                )

                normalized_unit = (
                    unit_name
                    .lower()
                    .replace("_", ".")
                )

                if normalized_base == normalized_unit:
                    return item_path

            elif os.path.isdir(item_path):
                add_directory(item_path)

        # Datei suchen
        for directory in search_dirs:
            for candidate in candidates:
                filename = os.path.abspath(
                    os.path.join(
                        directory,
                        candidate
                    )
                )

                if os.path.isfile(filename):
                    return filename

        searched = os.pathsep.join(
            search_dirs
        )

        raise CompileError(
            ctx,
            "E0019",
            text=(
                f"unit source {unit_name} not found; "
                f"searched: {searched}"
            )
        )
    
    def format_method_signature(self, params):
        if not params:
            return "()"

        types = []

        for p in params:
            typ = p["type"]

            if isinstance(typ, dict):
                if typ.get("kind") == "open_array":
                    element_type = self.resolve_type(
                        typ["element_type"]
                    )

                    types.append(
                        f"array of {element_type}"
                    )
                    continue

            types.append(
                str(self.resolve_type(typ))
            )

        return "(" + ", ".join(types) + ")"
    
    def infer_subrange_storage(self, min_value, max_value):
        if min_value > max_value:
            raise ValueError(
                f"invalid subrange: {min_value}..{max_value}"
            )

        signed = min_value < 0

        if signed:
            if -128 <= min_value and max_value <= 127:
                return 1, True

            if -32768 <= min_value and max_value <= 32767:
                return 2, True

            if -2147483648 <= min_value and max_value <= 2147483647:
                return 4, True

        else:
            if max_value <= 0xFF:
                return 1, False

            if max_value <= 0xFFFF:
                return 2, False

            if max_value <= 0xFFFFFFFF:
                return 4, False

        raise ValueError(
            f"subrange does not fit into 32 bits: "
            f"{min_value}..{max_value}"
        )

    def subrange_info(self, typ):
        if not isinstance(typ, str):
            return None

        return self.subrange_types.get(
            typ.lower()
        )

    def scalar_base_type(self, typ):
        info = self.subrange_info(typ)

        if info is not None:
            return info.base_type

        return self.resolve_type(typ)

    def function_abi_return_type(self, type_name):
        return_type = self.resolve_type(type_name)

        # Klassenvariablen enthalten Objektzeiger.
        if return_type in self.classes:
            return "pointer"

        if self.is_pointer_type(return_type, include_nil=False):
            return "pointer"

        if self.subrange_info(return_type) is not None:
            return "integer"

        return return_type

    def function_result_storage_type(
        self,
        declared_type
    ):
        """
        Bestimmt den lokalen Speichertyp der impliziten Result-Variable.

        Kleine skalare Typen werden absichtlich in einem 32-Bit-Slot
        gespeichert, weil NT32 sie über EAX zurückgibt und die vorhandenen
        Store-Emitter 32-Bit-Zugriffe erzeugen.
        """
        resolved_type = self.resolve_type(
            declared_type
        )

        abi_type = self.function_abi_return_type(
            resolved_type
        )

        if abi_type in (
            "integer",
            "boolean",
            "char"
        ):
            return "integer"

        return resolved_type

    def declare_subrange_type(
        self,
        ctx,
        name,
        min_value,
        max_value
    ):
        key = name.lower()

        if (
            key in self.type_aliases
            or key in self.subrange_types
            or key in self.records
            or key in self.arrays
            or key in self.classes
            or key in self.enums
        ):
            raise CompileError(
                ctx,
                "E0002",
                name=name
            )

        try:
            size, signed = self.infer_subrange_storage(
                min_value,
                max_value
            )
        except ValueError as exc:
            raise CompileError(
                ctx,
                "E0019",
                text=str(exc)
            )

        self.subrange_types[key] = SubrangeTypeInfo(
            name=name,
            base_type="integer",
            min_value=min_value,
            max_value=max_value,
            size=size,
            signed=signed
        )

    def parse_signed_integer(self, ctx):
        text = ctx.getText()

        try:
            return int(text, 10)
        except ValueError:
            raise CompileError(
                ctx,
                "E0019",
                text=f"invalid integer constant: {text}"
            )
    
    def pascal_token_string(self, token):
        text = token.getText()

        if len(text) < 2:
            return ""

        quote = text[0]

        if quote not in ("'", '"') or text[-1] != quote:
            raise ValueError(f"invalid Pascal string token: {text}")

        value = text[1:-1]

        if quote == "'":
            value = value.replace("''", "'")
        else:
            value = value.replace('""', '"')

        return value
    
    def find_known_dll_import_ordinal(
        self,
        dll_name,
        import_name
    ):
        """
        Liefert die stabile Ordinalnummer eines bekannten Runtime-Exports.

        Unterstützt sowohl den C-Namen:

            _jit_malloc

        als auch den dekorierten i386-COFF-Namen:

            __jit_malloc
        """
        if not dll_name or not import_name:
            return None

        normalized_dll = os.path.basename(
            str(dll_name).strip()
        ).lower()

        if normalized_dll != "libruntime_mini2.dll":
            return None

        name = str(
            import_name
        ).strip()

        candidates = [
            name
        ]

        # MinGW32 dekoriert einen C-Namen mit einem zusätzlichen
        # führenden Unterstrich.
        if name.startswith("__"):
            candidates.append(
                name[1:]
            )

        elif not name.startswith("_"):
            candidates.append(
                "_" + name
            )

        for candidate in candidates:
            ordinal = (
                LIBDBASE2MANY32_IMPORT_ORDINALS.get(
                    candidate
                )
            )

            if ordinal is not None:
                return int(
                    ordinal
                )

        return None


    def find_known_dll_import_name(
        self,
        dll_name,
        ordinal
    ):
        """
        Rückwärtsauflösung für PUI-Einträge, die nur eine Ordinalnummer
        enthalten. Sie wird für den gepackten Runtime-Thunkpfad benötigt.
        """
        if not dll_name or ordinal is None:
            return None

        normalized_dll = os.path.basename(
            str(dll_name).strip()
        ).lower()

        if normalized_dll != "libruntime_mini3.dll":
            return None

        wanted_ordinal = int(
            ordinal
        )

        for import_name, import_ordinal in (
            LIBDBASE2MANY32_IMPORT_ORDINALS.items()
        ):
            if int(import_ordinal) == wanted_ordinal:
                return str(
                    import_name
                )

        return None

    def make_dll_import_symbol(self, dll_name, import_name):
        key = (
            dll_name.lower(),
            import_name
        )

        old_symbol = self.dll_import_symbols.get(key)

        if old_symbol:
            return old_symbol

        safe_dll = re.sub(
            r"[^A-Za-z0-9_]",
            "_",
            dll_name
        )

        safe_name = re.sub(
            r"[^A-Za-z0-9_]",
            "_",
            import_name
        )

        symbol = (
            f"__dllimp_{self.next_dll_import_id}_"
            f"{safe_dll}_{safe_name}"
        )

        self.next_dll_import_id += 1
        self.dll_import_symbols[key] = symbol

        return symbol

    def register_local_external_routine(
        self,
        ctx,
        kind,
        name,
        params,
        return_type,
        convention
    ):
        key = name.lower()

        # Für C/MinGW32 wird ein führender Unterstrich verwendet.
        symbol = name

        if (
            CDATA.args_target in (
                "nt35",
                "winnt",
                "win32"
            )
            and not symbol.startswith("_")
        ):
            symbol = "_" + symbol

        metadata = {
            "name": name,
            "scoped_name": name,
            "label": None,
            "mangled": symbol,
            "symbol": symbol,
            "params": params,
            "return_type": return_type,
            "calling_convention": convention,
            "external": True,
            "external_kind": "coff",
            "dll": None,
            "import_name": None,
            "ordinal": None,
        }

        if kind == "function":
            self.functions[key] = metadata
        else:
            self.procedures[key] = metadata

        return None

    def decorate_local_external_symbol(
        self,
        name,
        convention,
        parameter_bytes=0
    ):
        symbol = name

        # Der Pascal-Name enthält bereits den gewünschten Unterstrich.
        if symbol.startswith("_"):
            return symbol

        if CDATA.args_target not in (
            "nt35",
            "winnt",
            "win32"
        ):
            return symbol

        if convention == "stdcall":
            return (
                "_"
                + symbol
                + "@"
                + str(parameter_bytes)
            )

        return "_" + symbol

    def normalize_calling_convention(
        self,
        ctx,
        convention
    ):
        """
        Normalisiert die Aufrufkonvention eines Routine-Headers.

        Unterstützt sowohl Textwerte als auch ANTLR-Kontexte und ist
        dadurch unabhängig davon, ob die aktuelle Parser-Version einen
        callingConvention()-Accessor erzeugt.
        """
        if convention is None:
            return "cdecl"

        if hasattr(
            convention,
            "getText"
        ):
            convention = convention.getText()

        convention_text = str(
            convention
        ).strip().lower()

        match = re.search(
            r"(?<![a-z0-9_])"
            r"(cdecl|stdcall|pascal|c)"
            r"(?![a-z0-9_])",
            convention_text
        )

        if match is not None:
            convention_text = match.group(1)

        if convention_text == "c":
            convention_text = "cdecl"

        if not convention_text:
            convention_text = "cdecl"

        if convention_text not in (
            "cdecl",
            "stdcall",
            "pascal"
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "unsupported calling convention: "
                    + convention_text
                )
            )

        return convention_text

    def validate_class_methods(
        self,
        ctx
    ):
        for class_key, cls in self.classes.items():
            for method_name, overloads in cls.methods.items():
                for method in overloads:

                    # Geerbte Methode gehört nicht zu dieser Klasse.
                    if getattr(
                        method,
                        "owner",
                        None
                    ) != class_key:
                        continue

                    if not getattr(
                        method,
                        "implemented",
                        False
                    ):
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                f"{tr('class')} {cls.name} "
                                f"{tr('method')} "
                                f"{method.name}"
                                f"{self.format_method_signature(method.params)} "
                                f"{tr('is declared but not implemented')}"
                            )
                        )

    def register_external_routine(
        self,
        ctx,
        kind,
        name,
        params,
        return_type,
        spec_ctx,
        convention="cdecl"
    ):
        if CDATA.args_target not in (
            "nt35",
            "winnt",
            "win32"
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "DLL imports are currently "
                    "supported only for NT32"
                )
            )

        # Die Aufrufkonvention gehört in der aktuellen Grammar zum
        # Routine-Header, nicht zum ExternalRoutineDirectiveContext.
        convention = self.normalize_calling_convention(
            ctx,
            convention
        )

        library_accessor = getattr(
            spec_ctx,
            "externalLibrary",
            None
        )

        library_ctx = (
            library_accessor()
            if library_accessor is not None
            else None
        )

        if library_ctx is None:
            return self.register_local_external_routine(
                ctx         = ctx,
                kind        = kind,
                name        = name,
                params      = params,
                return_type = return_type,
                convention  = convention
            )

        dll_name = self.resolve_external_library(
            ctx,
            library_ctx
        )

        if not dll_name:
            raise CompileError(
                ctx,
                "E0019",
                text="DLL name must not be empty"
            )

        dll_name = os.path.basename(
            dll_name
        )

        if not os.path.splitext(dll_name)[1]:
            dll_name += ".dll"

        # ----------------------------------------------------------
        # Expliziter Importname und explizites Ordinal aus dem
        # Pascal-Quelltext.
        # ----------------------------------------------------------
        import_name = self.external_import_name(
            spec_ctx
        )

        ordinal = self.external_import_ordinal(
            spec_ctx
        )

        # ----------------------------------------------------------
        # Weder NAME noch ORDINAL angegeben:
        # bisheriges Verhalten beibehalten und einen Namen erzeugen.
        # ----------------------------------------------------------
        if import_name is None and ordinal is None:
            import_name = self.fpc_mangle_external_routine(
                name,
                params
            )

        # ----------------------------------------------------------
        # Wenn kein explizites Ordinal im Pascal-Code steht, darf
        # weiterhin die bekannte Ordinaltabelle verwendet werden.
        # ----------------------------------------------------------
        if ordinal is None and import_name is not None:
            ordinal = self.find_known_dll_import_ordinal(
                dll_name,
                import_name
            )

        if import_name is None and ordinal is None:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "DLL import requires a name "
                    "or an ordinal"
                )
            )

        # make_dll_import_symbol() benötigt einen String.
        # Bei einem reinen Ordinalimport wird deshalb ein interner,
        # rein synthetischer Schlüssel erzeugt.
        symbol_identity = (
            import_name
            if import_name is not None
            else (
                f"ordinal_{ordinal}_"
                f"{name}"
            )
        )

        internal_symbol = self.make_dll_import_symbol(
            dll_name,
            symbol_identity
        )

        import_item = {
            "symbol": internal_symbol
        }

        if import_name is not None:
            import_item["name"] = import_name

        if ordinal is not None:
            import_item["ordinal"] = int(
                ordinal
            )

        dll_imports = CDATA.imports.setdefault(
            dll_name,
            []
        )

        already_registered = any(
            isinstance(item, dict)
            and item.get("symbol") == internal_symbol
            and item.get("name") == import_name
            and item.get("ordinal") == import_item.get("ordinal")
            for item in dll_imports
        )

        if not already_registered:
            dll_imports.append(
                import_item
            )

        # Eine Unit-Objektdatei enthält Relocations auf das interne
        # Symbol (zum Beispiel __dllimp_3_...). Diese Zuordnung muss
        # deshalb in der PUI erhalten bleiben und beim späteren Linken
        # des Hauptprogramms wiederhergestellt werden.
        if (
            self.root_module_kind == "unit"
            and self.pending_pui is not None
        ):
            self.pui_add_dll_import(
                dll_name,
                import_item
            )

        info = {
            "name": name,
            "scoped_name": self.unit_scoped_name(
                name
            ),

            "symbol": internal_symbol,
            "mangled": internal_symbol,

            "dll": dll_name,
            "import_name": import_name,
            "ordinal": ordinal,

            "calling_convention": convention,
            "params": params,

            "return_type": (
                self.resolve_type(return_type)
                if return_type is not None
                else None
            ),

            "external": True,
            "dll_import": True,
            "pui": False
        }

        key = name.lower()

        if kind == "function":
            if key in self.functions:
                raise CompileError(
                    ctx,
                    "E0002",
                    name=name
                )

            self.functions[key] = info

        elif kind == "procedure":
            if key in self.procedures:
                raise CompileError(
                    ctx,
                    "E0002",
                    name=name
                )

            self.procedures[key] = info

        else:
            raise RuntimeError(
                "invalid external routine kind: "
                + str(kind)
            )

        # --------------------------------------------------------------
        # Öffentliche externe Routinen auch als Pascal-Symbol in die
        # PUI schreiben.
        #
        # Die imports-Sektion beschreibt den PE-Import.
        # Die symbols-Sektion beschreibt die Pascal-Signatur.
        # --------------------------------------------------------------
        if (self.collect_pui_interface
            and self.pending_pui is not None
        ):
            if kind == "function":
                pui_section = "functions"
            elif kind == "procedure":
                pui_section = "procedures"
            else:
                raise RuntimeError(
                    "invalid external routine kind: "
                    + str(kind)
                )

            pui_item = {
                "name": name,

                "scoped_name": info[
                    "scoped_name"
                ],

                # Wichtig: dasselbe synthetische COFF-Symbol verwenden,
                # das auch in pending_pui["imports"] gespeichert wird.
                "symbol": internal_symbol,

                "params": self.pui_param_data(
                    params
                ),

                "calling_convention": convention,

                "external": True,
                "dll_import": True,

                "dll": dll_name,
                "import_name": import_name,
                "ordinal": ordinal
            }

            if kind == "function":
                pui_item["return_type"] = (
                    info["return_type"]
                )

            self.pui_add_symbol(
                pui_section,
                pui_item
            )

        return info
    
    def fpc_mangle_external_routine(
        self,
        name,
        params=None
    ):
        params = params or []

        routine_name = str(name).upper()
        param_suffix = self.fpc_mangle_params(params)

        return f"_{routine_name}{param_suffix}"
    
    def current_except_label(self):
        if not self.try_except_stack:
            return None
        return self.try_except_stack[-1]["except_label"]
    
    def is_double(self, typ):
        return typ.lower() == "double"

    def is_integer(self, typ):
        return typ.lower() == "integer"
    
    def push_const_scope(self):
        self.local_const_stack.append({})

    def pop_const_scope(self):
        self.local_const_stack.pop()

    def current_const_scope(self):
        if not self.local_const_stack:
            return None
        return self.local_const_stack[-1]

    def push_local_scope(self):
        self.local_var_stack.append({
            "vars": {},
            "next_offset": 0
        })

    def pop_local_scope(self):
        self.local_var_stack.pop()

    def current_local_scope(self):
        if not self.local_var_stack:
            return None
        return self.local_var_stack[-1]

    def class_instance_size(self, ctx, class_type):
        key = class_type.lower()

        if key not in self.classes:
            raise CompileError(ctx, "E0004", name=class_type)

        return self.classes[key].size
    
    def normalized_param_type(self, param):
        typ = param["type"]
        if isinstance(typ, dict):
            if typ.get("kind") == "open_array":
                element_type = self.resolve_type(
                    typ["element_type"]
                )
                return (
                    "open_array",
                    element_type
                )
        return self.resolve_type(typ)

    def method_signature(self, params):
        return tuple(
            self.normalized_param_type(p)
            for p in params
        )
    
    def sizeof_dos_pointed_type(self, ctx, ptr_type):
        ptr_type = self.resolve_type(ptr_type)

        if not isinstance(ptr_type, str) or not ptr_type.startswith("^"):
            raise CompileError(ctx, "E0005", got=ptr_type, expected="pointer")

        base_type = self.resolve_type(ptr_type[1:])

        if base_type == "integer":
            return 2

        if base_type == "boolean":
            return 2

        if base_type in self.records:
            # Achtung: Record-Felder sind aktuell noch 4/8 Byte aus Win64-Sicht.
            # Für DOS später besser type_size_dos bauen.
            return self.records[base_type].size

        raise CompileError(
            ctx,
            "E0019",
            text=f"DOS New() unsupported pointed type: {base_type}"
        )
    
    def type_size(self, ctx, typ):
        range_info = self.subrange_info(typ)

        if range_info is not None:
            return range_info.size

        typ = self.resolve_type(typ)

        if self.is_pointer_type(
            typ,
            include_nil=False
        ):
            return self.pointer_slot_size()

        if isinstance(typ, dict):
            if typ.get("kind") == "array":
                return typ["size"]

        if isinstance(typ, str) and typ in self.records: return self.records[typ].size
        if isinstance(typ, str) and typ in self.arrays:  return self.arrays[typ].size
        if isinstance(typ, str) and typ in self.classes: return self.pointer_slot_size()
        
        if typ == "char":    return 1
        if typ == "boolean": return 4
        if typ == "integer": return 4
        if typ == "double":  return 8
        if typ == "string":  return self.pointer_slot_size()

        raise CompileError(
            ctx,
            "E0004",
            name=typ
        )

    def add_data_bytes(
        self,
        name,
        data,
        alignment=1
    ):
        writer = getattr(
            self,
            "writer",
            None
        )

        if (
            writer is not None
            and hasattr(
                writer,
                "add_data_bytes"
            )
        ):
            return writer.add_data_bytes(
                name,
                data,
                alignment=alignment
            )

        coff = getattr(
            self,
            "coff",
            None
        )

        if (
            coff is not None
            and hasattr(
                coff,
                "add_data_bytes"
            )
        ):
            return coff.add_data_bytes(
                name,
                data,
                alignment=alignment
            )

        raise RuntimeError(
            "active writer cannot emit raw data bytes"
        )

    def add_data_u8(self, name, value=0):
        return self.add_data_bytes(
            name,
            bytes([value & 0xFF]),
            alignment=1
        )

    def add_data_u16(self, name, value=0):
        return self.add_data_bytes(
            name,
            int(value).to_bytes(
                2,
                "little",
                signed=False
            ),
            alignment=2
        )

    def validate_subrange_constant(
        self,
        ctx,
        declared_type,
        value
    ):
        info = self.subrange_info(
            declared_type
        )

        if info is None:
            return

        if not (
            info.min_value
            <= value
            <= info.max_value
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"value {value} is outside "
                    f"{info.name} range "
                    f"{info.min_value}..{info.max_value}"
                )
            )

    def emit_subrange_check(
        self,
        ctx,
        declared_type,
        value_reg="eax"
    ):
        info = self.subrange_info(declared_type)

        if info is None:
            return

        fail_label = self.new_named_label("subrange_fail")
        done_label = self.new_named_label("subrange_ok")

        self.emit_cmp(value_reg, info.min_value)
        self.emit_jl(fail_label)

        self.emit_cmp(value_reg, info.max_value)
        self.emit_jg(fail_label)
        
        self.emit_jmp(done_label)

        self.emit_bind_label(fail_label)

        self.emit_soft_runtime_error(
            f"Range check error: value for "
            f"{info.name} must be in "
            f"{info.min_value}..{info.max_value}"
        )

        self.emit_bind_label(done_label)

    def expression_variable_ref(self, ctx, expr):
        if expr is None:
            raise CompileError(ctx, "E0005", got="empty", expected="single variable")

        refs = []

        def walk(node):
            if node is None:
                return

            if isinstance(node, PascalParser.VariableRefContext):
                refs.append(node)
                return

            if hasattr(node, "children") and node.children:
                for child in node.children:
                    walk(child)

        walk(expr)

        if len(refs) != 1:
            raise CompileError(
                ctx,
                "E0005",
                got=expr.getText(),
                expected="single variable"
            )

        if refs[0].getText() != expr.getText():
            raise CompileError(
                ctx,
                "E0005",
                got=expr.getText(),
                expected="single variable"
            )

        return refs[0]
    
    def actual_param_variable_ref(self, ctx, arg):
        return self.expression_variable_ref(
            ctx,
            arg.expr()
        )
    
    def declare_record(
        self,
        ctx,
        name,
        fields,
        packed=False
    ):
        key = name.lower()

        if key in self.records:
            raise CompileError(
                ctx,
                "E0002",
                name=name
            )

        offset = 0
        record_fields = {}

        # Das bisherige dBase2Many-Record-ABI legt Felder bereits
        # lückenlos hintereinander. PACKED macht dieses Layout nun
        # ausdrücklich sichtbar und transportiert die Information
        # zusätzlich über die PUI.
        for field_name, field_type in fields:
            field_key = field_name.lower()

            if field_key in record_fields:
                raise CompileError(
                    ctx,
                    "E0002",
                    name=field_name
                )

            resolved_type = self.resolve_type(
                field_type
            )

            size = self.type_size(
                ctx,
                resolved_type
            )

            record_fields[field_key] = RecordFieldInfo(
                name=field_name,
                type=resolved_type,
                offset=offset,
                size=size
            )

            offset += size

        self.records[key] = RecordInfo(
            name=name,
            fields=record_fields,
            size=offset,
            packed=bool(packed),
            alignment=1
        )

    def declare_class(
        self,
        ctx,
        name,
        fields,
        methods,
        properties=None,
        parent_name=None
    ):
        key = name.lower()

        if properties is None:
            properties = {}

        parent_key = None

        # Versteckter VMT-Pointer an Offset 0.
        parent_size = self.pointer_slot_size()

        parent_fields = {}
        parent_methods = {}

        if parent_name:
            parent_key = parent_name.lower()

            if parent_key not in self.classes:
                raise CompileError(
                    ctx,
                    "E0004",
                    name=parent_name
                )

            parent_cls = self.classes[
                parent_key
            ]

            parent_size = max(
                int(parent_cls.size),
                self.pointer_slot_size()
            )

            parent_fields = dict(
                parent_cls.fields
            )

            for method_name, overloads in (
                parent_cls.methods.items()
            ):
                parent_methods[
                    method_name
                ] = list(
                    overloads
                )

        if key in self.classes:
            raise CompileError(
                ctx,
                "E0002",
                name=name
            )

        offset = parent_size
        class_fields = dict(
            parent_fields
        )

        for (
            field_name,
            field_type,
            visibility
        ) in fields:
            field_key = field_name.lower()
            resolved_type = self.resolve_type(
                field_type
            )

            size = self.type_size(
                ctx,
                resolved_type
            )

            class_fields[
                field_key
            ] = RecordFieldInfo(
                name=field_name,
                type=resolved_type,
                offset=offset,
                size=size,
                visibility=visibility
            )

            offset += size

        class_methods = dict(
            parent_methods
        )

        for method_data in methods:
            method_key = (
                method_data["name"].lower()
            )

            info = ClassMethodInfo(
                name=method_data["name"],
                kind=method_data["kind"],
                label=method_data["label"],
                params=method_data.get(
                    "params",
                    []
                ),
                owner=key,
                return_type=method_data.get(
                    "return_type"
                ),
                implemented=False,
                mangled=method_data.get(
                    "mangled"
                ),
                visibility=method_data.get(
                    "visibility",
                    "public"
                )
            )

            info.is_virtual = bool(
                method_data.get(
                    "virtual",
                    False
                )
            )

            info.is_override = bool(
                method_data.get(
                    "override",
                    False
                )
            )

            info.vmt_offset = None

            class_methods.setdefault(
                method_key,
                []
            )

            signature = self.method_signature(
                info.params
            )

            class_methods[
                method_key
            ] = [
                old_method
                for old_method in class_methods[
                    method_key
                ]
                if self.method_signature(
                    old_method.params
                ) != signature
            ]

            class_methods[
                method_key
            ].append(
                info
            )

        if "create" not in class_methods:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"class {name} requires "
                    "constructor Create"
                )
            )

        if "destroy" not in class_methods:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"class {name} requires "
                    "destructor Destroy"
                )
            )

        class_properties = dict(
            properties
        )

        if parent_name:
            parent_properties = getattr(
                parent_cls,
                "properties",
                {}
            )

            class_properties = dict(
                parent_properties
            )

            class_properties.update(
                properties
            )

        self.classes[
            key
        ] = ClassInfo(
            name=name,
            fields=class_fields,
            methods=class_methods,
            properties=class_properties,
            size=max(
                int(offset),
                self.pointer_slot_size()
            ),
            parent=parent_key
        )

        self.configure_class_vmt_metadata(
            ctx,
            key
        )

        if CDATA.debug_mode:
            cls = self.classes[
                key
            ]

            print(
                "DECLARE CLASS:",
                name,
                "size=",
                cls.size,
                "vmt=",
                cls.vmt_symbol
            )

            print(
                "FIELDS:",
                list(
                    class_fields.keys()
                )
            )

    def normalize_bool_eax(self):
        self.emit_cmp   (REG_EAX, 0)
        self.emit_setne (REG_AL)
        self.emit_movzx (REG_EAX, REG_AL)
    
    def normalize_unit_name(self, unit_name):
        return unit_name.lower().replace(".", "_")

    def unit_scoped_name(self, name):
        if self.current_unit:
            return self.normalize_unit_name(self.current_unit) + "_" + name

        return name
    
    def qualified_ident_text(self, ctx):
        return ctx.getText()
    
    def declare_array(self, ctx, name, index_min, index_max, element_type, init_values=None, dimensions=None):
        key = name.lower()

        if key in self.arrays:
            raise CompileError(ctx, "E0002", name=name)

        resolved_type = self.resolve_type(element_type)
        element_size  = self.type_size(ctx, resolved_type)
        
        if isinstance(resolved_type, str) and resolved_type in self.arrays:
            nested_array = self.arrays[resolved_type]

            if dimensions is None:
                dimensions = [
                    {
                        "min": index_min,
                        "max": index_max
                    }
                ]

            dimensions    = dimensions + nested_array.dimensions
            resolved_type = nested_array.element_type
        
        count = index_max - index_min + 1

        if count <= 0:
            raise CompileError(ctx, "E0005", got=str(index_max), expected=f">= {index_min}")

        if init_values is None:
            init_values = []

        if len(init_values) > count:
            raise CompileError(ctx, "E0005", got=str(len(init_values)), expected=f"max {count}")
        
        if dimensions is None:
            dimensions = [
                {
                    "min": index_min,
                    "max": index_max
                }
            ]

        if resolved_type == "char":
            element_size = 1
        
        elif resolved_type == "boolean":
            element_size = 4
            
        elif resolved_type == "integer":
            element_size = 4

        elif resolved_type == "double":
            element_size = 8

        elif resolved_type == "string":
            element_size = self.pointer_slot_size()

        elif self.is_pointer_type(
            resolved_type,
            include_nil=False
        ):
            element_size = self.pointer_slot_size()

        elif isinstance(resolved_type, str) and resolved_type in self.records:
            element_size = self.records[resolved_type].size

        elif isinstance(resolved_type, str) and resolved_type in self.classes:
            element_size = self.pointer_slot_size()

        else:
            raise CompileError(ctx, "E0004", name=resolved_type)

        count = 1
        for dim in dimensions:
            count *= dim["max"] - dim["min"] + 1
    
        self.arrays[key] = ArrayInfo(
            name            = name,
            index_min       = index_min,
            index_max       = index_max,
            element_type    = resolved_type,
            element_size    = element_size,
            size            = count * element_size,
            init_values     = init_values,
            dimensions      = dimensions
        )
    
    def declare_array_type(self, name, dimensions, element_type):
        element_type = self.resolve_type(element_type)

        # Array von Array erkennen
        if isinstance(element_type, dict) and element_type.get("kind") == "array":
            full_dimensions = dimensions + element_type["dimensions"]
            base_type = element_type["base_type"]
        else:
            full_dimensions = dimensions
            base_type = element_type

        self.types[name.lower()] = {
            "kind": "array",
            "name": name,
            "dimensions": full_dimensions,
            "base_type": base_type
        }
    
    def const_array_symbol(
        self,
        name
    ):
        """
        Erzeugt ein eindeutiges internes COFF-Symbol für ein
        typisiertes konstantes Array.

        Lokale Konstanten verschiedener Routinen dürfen denselben
        Pascal-Namen besitzen. Der Scope ist deshalb Bestandteil des
        Symbols.
        """
        scope_parts = []

        if self.current_unit:
            scope_parts.append(
                str(self.current_unit)
            )
        elif self.program_name:
            scope_parts.append(
                str(self.program_name)
            )

        scope_parts.extend(
            str(item)
            for item in self.scope_stack
        )

        scope_parts.append(
            str(name)
        )

        safe_name = re.sub(
            r"[^A-Za-z0-9_]",
            "_",
            "_".join(scope_parts)
        ).lower()

        symbol = (
            f"__const_array_{safe_name}_"
            f"{self.next_const_array_id}"
        )

        self.next_const_array_id += 1

        return symbol


    def encode_const_array_data(
        self,
        ctx,
        element_type,
        init_values
    ):
        """
        Kodiert die Werte eines typisierten konstanten Arrays für
        die COFF-Datensektion.
        """
        resolved_type = self.resolve_type(
            element_type
        )

        range_info = self.subrange_info(
            resolved_type
        )

        payload = bytearray()

        if resolved_type == "char":
            for value in init_values:
                numeric_value = int(value)

                if not 0 <= numeric_value <= 0xFF:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=str(numeric_value),
                        expected="AnsiChar 0..255"
                    )

                payload.append(
                    numeric_value
                )

            return bytes(payload), 1

        if resolved_type == "boolean":
            for value in init_values:
                payload.extend(
                    (1 if value else 0).to_bytes(
                        4,
                        "little",
                        signed=False
                    )
                )

            return bytes(payload), 4

        if (
            resolved_type == "integer"
            or (
                range_info is not None
                and range_info.base_type == "integer"
            )
        ):
            element_size = (
                int(range_info.size)
                if range_info is not None
                else 4
            )

            bit_count = element_size * 8
            mask = (1 << bit_count) - 1

            for value in init_values:
                numeric_value = int(value)

                if range_info is not None:
                    self.validate_subrange_constant(
                        ctx,
                        resolved_type,
                        numeric_value
                    )

                payload.extend(
                    (numeric_value & mask).to_bytes(
                        element_size,
                        "little",
                        signed=False
                    )
                )

            return (
                bytes(payload),
                min(
                    max(element_size, 1),
                    4
                )
            )

        if resolved_type == "double":
            for value in init_values:
                bits = int(
                    double_to_bits(
                        float(value)
                    )
                )

                payload.extend(
                    bits.to_bytes(
                        8,
                        "little",
                        signed=False
                    )
                )

            return bytes(payload), 8

        raise CompileError(
            ctx,
            "E0019",
            text=(
                "constant array data emission is not "
                f"implemented for {resolved_type}"
            )
        )


    def declare_const_array(
        self,
        ctx,
        name,
        dimensions,
        element_type,
        init_values
    ):
        """
        Registriert ein typisiertes konstantes Array im aktuellen
        Konstanten-Scope und schreibt dessen Inhalt in die COFF-
        Datensektion.
        """
        key = name.lower()

        scope = self.current_const_scope()

        if scope is not None:
            if key in scope:
                raise CompileError(
                    ctx,
                    "E0002",
                    name=name
                )

            local_scope = self.current_local_scope()

            if (
                local_scope is not None
                and key in local_scope["vars"]
            ):
                raise CompileError(
                    ctx,
                    "E0002",
                    name=name
                )

            target_table = scope

        else:
            if (
                key in self.constants
                or key in self.vars
            ):
                raise CompileError(
                    ctx,
                    "E0002",
                    name=name
                )

            target_table = self.constants

        if not dimensions:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"constant array {name} has no dimensions"
                )
            )

        resolved_type = self.resolve_type(
            element_type
        )

        element_size = self.type_size(
            ctx,
            resolved_type
        )

        element_count = 1

        for dimension in dimensions:
            count = (
                int(dimension["max"])
                - int(dimension["min"])
                + 1
            )

            if count <= 0:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"invalid constant array dimension "
                        f"for {name}"
                    )
                )

            element_count *= count

        if len(init_values) != element_count:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(init_values)),
                expected=str(element_count)
            )

        first_dimension = dimensions[0]

        array_info = ArrayInfo(
            name=name,
            index_min=int(
                first_dimension["min"]
            ),
            index_max=int(
                first_dimension["max"]
            ),
            element_type=resolved_type,
            element_size=int(element_size),
            size=element_count * int(element_size),
            init_values=list(init_values),
            dimensions=list(dimensions)
        )

        symbol = self.const_array_symbol(
            name
        )

        payload, alignment = self.encode_const_array_data(
            ctx,
            resolved_type,
            init_values
        )

        if CDATA.args_target not in (
            "nt35",
            "winnt",
            "win32",
            "win64"
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "typed constant arrays are currently "
                    "implemented only for COFF targets"
                )
            )

        self.writer.align_data(
            alignment
        )

        self.writer.add_data_label(
            symbol
        )

        self.writer.data.extend(
            payload
        )

        target_table[key] = {
            "name": name,
            "kind": "array",
            "type": "const_array",
            "element_type": resolved_type,
            "array_info": array_info,
            "symbol": symbol,
            "value": tuple(init_values)
        }

        return target_table[key]


    def emit_load_const_array_element(
        self,
        ctx,
        name,
        const_info,
        index_exprs
    ):
        """
        Lädt ein Element eines typisierten konstanten Arrays.

        NT32-Ergebnis:
            Integer/Boolean/Char -> EAX
            Double               -> XMM0
        """
        array_info = const_info.get(
            "array_info"
        )

        symbol = const_info.get(
            "symbol"
        )

        if array_info is None or not symbol:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"invalid constant array metadata: "
                    f"{name}"
                )
            )

        if not isinstance(
            index_exprs,
            list
        ):
            index_exprs = [
                index_exprs
            ]

        dimensions = list(
            array_info.dimensions
        )

        if len(index_exprs) != len(dimensions):
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(index_exprs)),
                expected=str(len(dimensions))
            )

        # Eindimensionale konstante Arrays werden ohne den allgemeinen
        # EBX-Akkumulator berechnet. Komplexe Indexausdrücke wie
        #
        #     (CRC shr 12) and $0F
        #
        # dürfen EBX intern verwenden, ohne dadurch den Index zu
        # verfälschen.
        if len(dimensions) == 1:
            index_type = self.visit(
                index_exprs[0]
            )

            if self.scalar_base_type(
                index_type
            ) != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=index_type,
                    expected="integer"
                )

            dimension = dimensions[0]

            minimum = int(
                dimension["min"]
            )

            maximum = int(
                dimension["max"]
            )

            fail_label = self.new_named_label(
                "const_array_bounds_fail"
            )

            ok_label = self.new_named_label(
                "const_array_bounds_ok"
            )

            self.emit_cmp(
                "eax",
                minimum
            )

            self.emit_jl(
                fail_label
            )

            self.emit_cmp(
                "eax",
                maximum
            )

            self.emit_jg(
                fail_label
            )

            self.emit_jmp(
                ok_label
            )

            self.emit_bind_label(
                fail_label
            )

            self.emit_soft_runtime_error(
                f"Array bounds error: {name} index out of range "
                f"allowed range {minimum}..{maximum}"
            )

            self.emit_bind_label(
                ok_label
            )

            if minimum != 0:
                self.emit_sub(
                    "eax",
                    minimum
                )

        else:
            self.emit_multi_array_index_offset(
                ctx,
                name,
                array_info,
                index_exprs
            )

        # EAX = linearer Index
        if array_info.element_size != 1:
            self.emit_imul(
                "eax",
                "eax",
                array_info.element_size
            )

        is_nt32 = CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        )

        if is_nt32:
            self.emit_mov(
                "edx",
                "eax",
                comment="constant array byte offset"
            )

            self.writer.emit_lea_reg_data_label(
                "eax",
                symbol
            )

            self.emit_add(
                "eax",
                "edx",
                comment=f"{name} element address"
            )

            address_reg = "eax"

        else:
            self.emit_movsxd(
                "r11",
                "eax"
            )

            self.writer.emit_lea_reg_data_label(
                "rax",
                symbol
            )

            self.emit_add(
                "rax",
                "r11",
                comment=f"{name} element address"
            )

            address_reg = "rax"

        element_type = self.resolve_type(
            array_info.element_type
        )

        range_info = self.subrange_info(
            element_type
        )

        if element_type == "char":
            self.backend.writer.emit_movzx_r32_byte_ptr(
                "eax",
                address_reg,
                0
            )

            return "char"

        if element_type == "boolean":
            self.emit_mov_dword_ptr(
                "eax",
                address_reg,
                0,
                comment=f"load {name} element"
            )

            self.emit_and(
                "eax",
                1
            )

            return "boolean"

        if (
            element_type == "integer"
            or (
                range_info is not None
                and range_info.base_type == "integer"
            )
        ):
            element_size = (
                int(range_info.size)
                if range_info is not None
                else 4
            )

            if element_size == 1:
                self.backend.writer.emit_movzx_r32_byte_ptr(
                    "eax",
                    address_reg,
                    0
                )

            elif element_size == 2:
                # Der vorhandene Writer besitzt bereits den stabilen
                # DWord-Ladepfad. Anschließend werden die oberen Bits
                # entfernt.
                self.emit_mov_dword_ptr(
                    "eax",
                    address_reg,
                    0,
                    comment=f"load {name} word element"
                )

                self.emit_and(
                    "eax",
                    0xFFFF
                )

            elif element_size == 4:
                self.emit_mov_dword_ptr(
                    "eax",
                    address_reg,
                    0,
                    comment=f"load {name} integer element"
                )

            else:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"unsupported integer element size "
                        f"{element_size} for {name}"
                    )
                )

            return "integer"

        if element_type == "double":
            self.emit_movsd_load(
                "xmm0",
                address_reg,
                0,
                comment=f"load {name} element"
            )

            return "double"

        raise CompileError(
            ctx,
            "E0014",
            var_type=element_type
        )


    def declare_const(self, ctx, name, value, typ):
        key = name.lower()

        scope = self.current_const_scope()

        if scope is not None:
            if key in scope:
                raise CompileError(ctx, "E0002", name=name)

            scope[key] = {
                "name": name,
                "type": typ.lower(),
                "value": value
            }
            return

        if key in self.constants:
            raise CompileError(ctx, "E0002", name=name)

        self.constants[key] = {
            "name": name,
            "type": typ,
            "value": value
        }
    
    def declare_type_alias(self, ctx, name, target_type):
        key = name.lower()

        if key in self.type_aliases:
            raise CompileError(ctx, "E0002", name=name)

        self.type_aliases[key] = target_type.lower()
    
    def declare_local_var(self, ctx, name, vtype):
        scope = self.current_local_scope()

        if scope is None:
            self.declare_var(ctx, name, vtype)
            return

        key = name.lower()

        if key in scope["vars"]:
            raise CompileError(ctx, "E0002", name=name)

        declared_type = str(vtype).strip().lower()
        range_info = self.subrange_info(declared_type)

        if range_info is not None:
            # Bestehende Ausdruckspfade verwenden intern Integer. Der
            # deklarierte Typ und die tatsächliche Speicherbreite bleiben
            # für Range-Checks und Stores separat erhalten.
            typ = range_info.base_type
            size = int(range_info.size)
        else:
            typ = self.resolve_type(declared_type)

            if typ in ("integer", "boolean"):
                if CDATA.args_target in ("dos", "dos16"):
                    size = 2
                elif CDATA.args_target in ("nt35", "winnt", "win32"):
                    size = 4
                else:
                    size = 8

            elif typ == "char":
                size = 1

            elif typ == "double":
                size = 8

            elif typ == "string":
                if CDATA.args_target in ("dos", "dos16"):
                    size = 4
                else:
                    size = self.pointer_slot_size()

            elif (
                typ == "pointer"
                or self.is_pointer_type(typ, include_nil=False)
                or (
                    isinstance(typ, str)
                    and typ in self.classes
                )
            ):
                size = self.pointer_slot_size()

            elif isinstance(typ, str) and typ in self.records:
                size = int(self.records[typ].size)

            elif isinstance(typ, str) and typ in self.arrays:
                array_info = self.arrays[typ]

                if getattr(array_info, "is_dynamic", False):
                    size = self.pointer_slot_size()
                else:
                    size = int(array_info.size)

            elif isinstance(typ, str) and typ in self.enums:
                typ = "integer"

                if CDATA.args_target in ("dos", "dos16"):
                    size = 2
                elif CDATA.args_target in ("nt35", "winnt", "win32"):
                    size = 4
                else:
                    size = 8

            else:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=typ,
                    expected=(
                        "integer/boolean/char/double/string/"
                        "pointer/record/array/enum"
                    )
                )

        scope["next_offset"] += size
        offset = -scope["next_offset"]

        scope["vars"][key] = {
            "name": name,
            "type": typ,
            "declared_type": declared_type,
            "offset": offset,
            "size": size
        }

    def declare_var(self, ctx, name, vtype):
        key = name.lower()
        #typ = self.resolve_type(vtype)
        
        declared_type = vtype.lower()
        range_info = self.subrange_info(declared_type)
        
        if range_info is not None:
            typ  = range_info.base_type
            size = range_info.size
        else:
            typ  = self.resolve_type(vtype)
            size = self.type_size(ctx, typ)
        
        if key in self.vars:
            raise CompileError(ctx, "E0002", name=name)
        
        symbol = None
        
        use_direct_coff_globals = (
            hasattr(self, "coff")
            and self.backend.name == CDATA.args_backend
        )
        
        if typ == "char":
            slot = self.next_int_slot
            self.next_int_slot += 1

            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                symbol = f"_var_{name}"

                if self.coff.find_symbol_index(symbol) is None:
                    self.coff.add_data_zeros(
                        symbol,
                        1,
                        alignment=1
                    )
        
        elif typ == "integer":
            slot = self.next_int_slot
            self.next_int_slot += 1
            
            if CDATA.args_target in ["dos", "dos16"]:
                symbol = f"_var_{name}"
                self.backend.writer.add_dword_var(symbol)
            else:
                #if use_direct_coff_globals:
                symbol = f"_var_{name}"
                self.coff.add_data_i32(symbol)
        
        elif typ == "double":
            slot = self.next_double_slot
            self.next_double_slot += 1

            # NT32 verwendet direkte COFF-Datensymbole.
            #
            # Nicht von backend.name abhängig machen, weil bei einem
            # DualBackend der Name nicht mit CDATA.args_backend
            # übereinstimmen muss.
            if CDATA.args_target in (
                "nt35",
                "winnt",
                "win32"
            ):
                symbol = f"_var_{name}"

                if self.coff.find_symbol_index(symbol) is None:
                    self.coff.add_data_double(
                        symbol,
                        0.0
                    )

            elif use_direct_coff_globals:
                symbol = f"_var_{name}"

                if self.coff.find_symbol_index(symbol) is None:
                    self.coff.add_data_double(
                        symbol,
                        0.0
                    )
        
        elif typ == "string":
            slot = self.next_string_slot
            self.next_string_slot += 1

            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                symbol = f"_var_{name}"
                if self.coff.find_symbol_index(symbol) is None:
                    self.coff.add_data_i32(symbol, 0)

            elif use_direct_coff_globals:
                symbol = f"_var_{name}"
                self.coff.add_data_qword(symbol)
        
        elif isinstance(typ, str) and typ in self.records:
            slot = self.next_record_slot
            self.next_record_slot += self.records[typ].size

            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                symbol = f"_var_{name}"
                if self.coff.find_symbol_index(symbol) is None:
                    self.coff.add_data_zeros(
                        symbol,
                        self.records[typ].size,
                        alignment=4
                    )
        
        elif isinstance(typ, str) and typ in self.arrays:
            array_info = self.arrays[typ]

            if getattr(array_info, "is_dynamic", False):
                slot = self.next_pointr_slot
                self.next_pointr_slot += 1

                if CDATA.args_target in ["nt35", "winnt", "win32"]:
                    symbol = f"_var_{name}"
                    if self.coff.find_symbol_index(symbol) is None:
                        self.coff.add_data_i32(symbol, 0)
            else:
                slot = self.next_arrays_slot
                self.next_arrays_slot += array_info.size

                if CDATA.args_target in ["nt35", "winnt", "win32"]:
                    symbol = f"_var_{name}"
                    if self.coff.find_symbol_index(symbol) is None:
                        self.coff.add_data_zeros(symbol, array_info.size, alignment=4)
        
        elif isinstance(typ, str) and typ in self.classes:
            slot = self.next_pointr_slot
            self.next_pointr_slot += 1

            if CDATA.args_target in ["dos", "dos16"]:
                symbol = f"_var_{name}"
                self.backend.writer.add_dword_var(symbol)

            elif CDATA.args_target in ["nt35", "winnt", "win32"]:
                symbol = f"_var_{name}"

                if self.coff.find_symbol_index(symbol) is None:
                    self.coff.add_data_i32(symbol, 0)

            elif use_direct_coff_globals:
                symbol = f"_var_{name}"
                self.coff.add_data_qword(symbol)

        elif self.is_pointer_type(
            typ,
            include_nil=False
        ):
            slot = self.next_pointr_slot
            self.next_pointr_slot += 1
            
            if CDATA.args_target in ["dos", "dos16"]:
                symbol = f"_var_{name}"
                self.backend.writer.add_dword_var(symbol)

            elif CDATA.args_target in ["nt35", "winnt", "win32"]:
                symbol = f"_var_{name}"

                if self.coff.find_symbol_index(symbol) is None:
                    self.coff.add_data_i32(
                        symbol,
                        0
                    )

            elif use_direct_coff_globals:
                symbol = f"_var_{name}"
                self.coff.add_data_qword(symbol)
            
        else:
            raise CompileError(ctx, "E0004", name=vtype)
        
        self.vars[key] = {
            "name": name,

            # Für bestehende Operationen:
            "type": typ,

            # Für Größen- und Bereichsprüfung:
            "declared_type": declared_type,

            "size": size,
            "slot": slot
        }
        
        if symbol is not None:
            self.vars[key]["symbol"] = symbol
            
        self.var_types[key] = typ

    def identifier_exists(self, name):
        if name in self.enums:
            return True

        if name in self.type_aliases:
            return True

        if name in self.constants:
            return True

        if name in self.variables:
            return True

        if hasattr(self, "functions") and name in self.functions:
            return True

        if hasattr(self, "procedures") and name in self.procedures:
            return True

        return False

    def declare_enum(self, ctx, name, values):
        key = name.lower()

        if key in self.enums:
            raise CompileError(ctx, "E0016", name=name)

        enum_values = {}

        for value_name, value_int in values:
            value_key = value_name.lower()

            if value_key in enum_values:
                raise CompileError(ctx, "E0017", value_name=value_name)

            enum_values[value_key] = value_int
            self.declare_const(ctx, value_name, value_int, "integer")

        self.enums[key] = EnumInfo(name, enum_values)
        self.declare_type_alias(ctx, name, "integer")
    
    def resolve_class_field_path(self, ctx, parts):
        if len(parts) < 2:
            raise CompileError(
                ctx,
                "E0019",
                text="class field path has no member"
            )

        var_name = parts[0]

        (   source_kind,
            var_info,
            class_type
        ) = self.resolve_named_storage(
            ctx,
            var_name
        )

        if class_type not in self.classes:
            raise CompileError(
                ctx,
                "E0005",
                got=class_type,
                expected="class"
            )

        current_type = class_type
        resolved = []

        for index, member_name in enumerate(
            parts[1:]
        ):
            if current_type in self.classes:
                fields = self.classes[
                    current_type
                ].fields
            elif current_type in self.records:
                fields = self.records[
                    current_type
                ].fields
            else:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=current_type,
                    expected="class/record"
                )

            member_key = member_name.lower()

            if member_key not in fields:
                raise CompileError(
                    ctx,
                    "E0001",
                    name=".".join(
                        parts[:index + 2]
                    )
                )

            member = fields[
                member_key
            ]
            member_type = self.resolve_type(
                member.type
            )

            resolved.append((
                member,
                member_type
            ))

            if index + 1 < len(parts[1:]):
                if (
                    member_type not in self.classes
                    and member_type not in self.records
                ):
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=member_type,
                        expected="class/record"
                    )

                current_type = member_type

        return (
            var_info,
            resolved
        )

    def emit_class_member_address(
        self,
        ctx,
        parts
    ):
        var_info, resolved = self.resolve_class_field_path(
            ctx,
            parts
        )

        is_nt32 = CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        )
        address_reg = "eax" if is_nt32 else "rax"

        self.emit_load_object_var(
            ctx,
            parts[0],
            var_info
        )
        self.emit_nil_pointer_check(
            parts[0]
        )

        for index, (member, member_type) in enumerate(
            resolved[:-1]
        ):
            path = ".".join(
                parts[:index + 2]
            )

            if member_type in self.classes:
                if is_nt32:
                    self.emit_mov_dword_ptr(
                        "eax",
                        "eax",
                        member.offset,
                        comment=path
                    )
                else:
                    self.emit_mov_qword_ptr(
                        "rax",
                        "rax",
                        member.offset,
                        comment=path
                    )

                self.emit_nil_pointer_check(
                    path
                )
                continue

            if member_type in self.records:
                if member.offset:
                    self.emit_add(
                        address_reg,
                        member.offset,
                        comment=path
                    )
                continue

            raise CompileError(
                ctx,
                "E0005",
                got=member_type,
                expected="class/record"
            )

        field, field_type = resolved[-1]

        return (
            field,
            field_type
        )
    
    def resolve_record_path(self, ctx, parts):
        var_name = parts[0]
        (
            source_kind,
            var_info,
            current_type
        ) = self.resolve_named_storage(
            ctx,
            var_name
        )

        if current_type not in self.records:
            raise CompileError(ctx, "E0005", got=current_type, expected="record")

        # The base address is selected separately for local variables,
        # formal parameters and globals. This value therefore contains
        # only offsets inside the record, never a global record slot.
        offset = 0
        field = None

        for field_name in parts[1:]:
            record = self.records[current_type]
            field_key = field_name.lower()

            if field_key not in record.fields:
                raise CompileError(ctx, "E0001", name=".".join(parts))

            field = record.fields[field_key]
            offset += field.offset
            current_type = self.resolve_type(
                field.type
            )

            if field_name != parts[-1]:
                if current_type not in self.records:
                    raise CompileError(ctx, "E0005", got=current_type, expected="record")

        return (
            source_kind,
            var_info,
            offset,
            field
        )

    def emit_record_base_address(
        self,
        ctx,
        name,
        source_kind,
        info,
        address_reg
    ):
        """
        Load the address of a record variable without losing the value
        currently held in EAX/RAX.

        In particular, a VAR record parameter contains the address of the
        caller's record in its stack slot. A local record lives inline in the
        current frame and a global NT32 record has its own COFF data symbol.
        """
        is_nt32 = CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        )

        if source_kind == "local":
            self.emit_lea_byte(
                address_reg,
                "ebp" if is_nt32 else "rbp",
                info["offset"],
                comment=f"{name} record address"
            )
            return

        if source_kind == "param":
            offset = info.get(
                "stack_offset"
            )

            if offset is None:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=f"parameter {name} has no stack offset"
                )

            if info.get("is_var", False):
                if is_nt32:
                    self.emit_mov_dword_ptr(
                        address_reg,
                        "ebp",
                        offset,
                        comment=f"var record parameter {name}"
                    )
                else:
                    self.emit_mov_qword_ptr(
                        address_reg,
                        "rbp",
                        offset,
                        comment=f"var record parameter {name}"
                    )
            else:
                self.emit_lea_byte(
                    address_reg,
                    "ebp" if is_nt32 else "rbp",
                    offset,
                    comment=f"record parameter {name}"
                )

            return

        if source_kind == "global":
            if is_nt32:
                symbol = (
                    info.get("symbol")
                    or f"_var_{info['name']}"
                )

                info["symbol"] = symbol

                self.writer.emit_lea_reg_data_label(
                    address_reg,
                    symbol
                )
                return

            self.emit_mov_qword(
                address_reg,
                "r12",
                "record_vars"
            )

            slot = int(
                info.get("slot", 0)
            )

            if slot:
                self.emit_add(
                    address_reg,
                    slot,
                    comment=f"{name} record slot"
                )

            return

        raise CompileError(
            ctx,
            "E0019",
            text=(
                f"unknown record storage kind for "
                f"{name}: {source_kind}"
            )
        )

    def pascal_import_type(self, typ):
        typ = self.resolve_type(typ)

        if typ == "integer":
            return "Integer"

        if typ == "double":
            return "Double"

        if typ == "string":
            return "AnsiString"

        if self.is_pointer_type(
            typ,
            include_nil=False
        ):
            return "Pointer"

        return str(typ)

    def render_asm_export_thunks(self):
        out  = []
        seen = set()

        for item in self.exports:
            mangled = item["mangled"]

            if mangled in seen:
                continue
            seen.add(mangled)

            # normale Funktionen sind bereits direkt gemappt:
            # _ADD$INTEGER$INTEGER:
            if item.get("kind") == "function":
                continue

            # Prozeduren später genauso behandeln, wenn sie direkt gemappt sind
            if item.get("kind") == "procedure":
                continue

            if item.get("kind") != "class_method":
                continue

            class_name  = item["class_name"].lower()
            method_name = item["method_name"].lower()

            cls = self.classes[class_name]
            overloads = cls.methods[method_name]

            method = self.find_export_method_overload(
                None,
                overloads,
                [
                    self.resolve_type(p["type"])
                    for p in item.get("params", [])
                ]
            )

            target = method.label

            # Sicherheitsbremse gegen Selbstaufruf
            if target == mangled:
                continue

            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append(f'{ASM_OUT_PH}"{mangled}:" << std::endl;')
                out.append(f'{ASM_OUT_PH}"    call {target}" << std::endl;')
                out.append(f'{ASM_OUT_PH}"    ret" << std::endl << std::endl;')
            elif CDATA.BackEnd.current == BACKEND_NASM:
                out.append(f'{mangled}:')
                out.append(f'    call {target}')
                out.append(f'    ret')

        return "\n".join(out)

    def render_import_params(self, params):
        if not params:
            return ""

        parts = []

        for p in params:
            prefix = "var " if p.get("is_var", False) else ""
            parts.append(
                f"{prefix}{p['name']}: {self.pascal_import_type(p['type'])}"
            )

        return "; ".join(parts)

    def render_call_args(self, params):
        return ", ".join(p["name"] for p in params)

    def render_external_decl(self, item):
        params = self.render_import_params(item.get("params", []))
        lines = []

        if item.get("return_type"):
            ret = self.pascal_import_type(item["return_type"])

            if params:
                lines.append(
                    f"function {item['name']}({params}): {ret}; "
                    f"external DLL_NAME name '{item['mangled']}';"
                )
            else:
                lines.append(
                    f"function {item['name']}: {ret}; "
                    f"external DLL_NAME name '{item['mangled']}';"
                )
        else:
            if params:
                lines.append(
                    f"procedure {item['name']}({params}); "
                    f"external DLL_NAME name '{item['mangled']}';"
                )
            else:
                lines.append(
                    f"procedure {item['name']}; "
                    f"external DLL_NAME name '{item['mangled']}';"
                )

        return lines

    def render_class_external_decl(self, item, handle_type):
        lines = []

        raw_name = item["export_name"]
        params   = list(item.get("params", []))
        mk       = item["method_kind"].lower()

        if mk == "constructor":
            params_text = self.render_import_params(params)

            if params_text:
                lines.append(
                    f"function {raw_name}({params_text}): {handle_type}; "
                    f"external DLL_NAME name '{item['mangled']}';"
                )
            else:
                lines.append(
                    f"function {raw_name}: {handle_type}; "
                    f"external DLL_NAME name '{item['mangled']}';"
                )

            return lines

        if mk == "destructor":
            lines.append(
                f"procedure {raw_name}(Self: {handle_type}); "
                f"external DLL_NAME name '{item['mangled']}';"
            )
            return lines

        params_text = self.render_import_params(params)

        if params_text:
            params_text = "Self: " + handle_type + "; " + params_text
        else:
            params_text = "Self: " + handle_type

        if item.get("return_type"):
            ret = self.pascal_import_type(item["return_type"])
            lines.append(
                f"function {raw_name}({params_text}): {ret}; "
                f"external DLL_NAME name '{item['mangled']}';"
            )
        else:
            lines.append(
                f"procedure {raw_name}({params_text}); "
                f"external DLL_NAME name '{item['mangled']}';"
            )

        return lines

    def render_fpc_import_unit(self):
        lib_name  = self.program_name.lower()
        unit_name = "import_" + lib_name
        dll_name  = lib_name + ".dll"

        class_exports = {}
        normal_exports = []

        for item in self.exports:
            if item.get("kind") == "class_method":
                class_exports.setdefault(item["class_name"], [])
                class_exports[item["class_name"]].append(item)
            else:
                normal_exports.append(item)

        lines = []
        lines.append("{$mode objfpc}{$H+}")
        lines.append(f"unit {unit_name};")
        lines.append("")
        lines.append("interface")
        lines.append("")
        lines.append("const")
        lines.append(f"  DLL_NAME = '{dll_name}';")
        lines.append("")

        # normale Funktionen / Prozeduren
        for item in normal_exports:
            lines.extend(self.render_external_decl(item))
            lines.append("")

        # rohe Klassen-Imports
        for class_name, methods in class_exports.items():
            handle_type = class_name + "Handle"

            lines.append("type")
            lines.append(f"  {handle_type} = Pointer;")
            lines.append("")

            for item in methods:
                lines.extend(self.render_class_external_decl(item, handle_type))
                lines.append("")

        # Wrapper-Klassen
        if class_exports:
            lines.append("type")

        for class_name, methods in class_exports.items():
            handle_type = class_name + "Handle"

            lines.append(f"  {class_name} = class")
            lines.append("  private")
            lines.append(f"    FHandle: {handle_type};")
            lines.append("  public")

            for item in methods:
                mk = item["method_kind"].lower()

                if mk == "constructor":
                    params = self.render_import_params(item.get("params", []))
                    
                    if params:
                        lines.append(f"    constructor Create({params});")
                    else:
                        lines.append("    constructor Create;")
                
                elif mk == "destructor":
                    lines.append("    destructor Destroy; override;")
                
                elif mk == "function":
                    params = self.render_import_params(item.get("params", []))
                    ret = self.pascal_import_type(item["return_type"])

                    if params:
                        lines.append(f"    function {item['method_name']}({params}): {ret};")
                    else:
                        lines.append(f"    function {item['method_name']}: {ret};")

                elif mk == "procedure":
                    params = self.render_import_params(item.get("params", []))

                    if params:
                        lines.append(f"    procedure {item['method_name']}({params});")
                    else:
                        lines.append(f"    procedure {item['method_name']};")

            lines.append("  end;")
            lines.append("")

        lines.append("implementation")
        lines.append("")

        # Wrapper-Implementierungen
        for class_name, methods in class_exports.items():
            handle_type = class_name + "Handle"

            for item in methods:
                mk = item["method_kind"].lower()
                method_name = item["method_name"]
                export_name = item["export_name"]

                if mk == "constructor":
                    params = self.render_import_params(item.get("params", []))
                    call_args = self.render_call_args(item.get("params", []))

                    if params:
                        lines.append(f"constructor {class_name}.Create({params});")
                    else:
                        lines.append(f"constructor {class_name}.Create;")

                    lines.append("begin")
                    lines.append("  inherited Create;")

                    if call_args:
                        lines.append(f"  FHandle := {export_name}({call_args});")
                    else:
                        lines.append(f"  FHandle := {export_name};")

                    lines.append("end;")
                    lines.append("")

                elif mk == "destructor":
                    lines.append(f"destructor {class_name}.Destroy;")
                    lines.append("begin")
                    lines.append("  if FHandle <> nil then")
                    lines.append("  begin")
                    lines.append(f"    {export_name}(FHandle);")
                    lines.append("    FHandle := nil;")
                    lines.append("  end;")
                    lines.append("")
                    lines.append("  inherited Destroy;")
                    lines.append("end;")
                    lines.append("")

                elif mk == "function":
                    params = self.render_import_params(item.get("params", []))
                    ret = self.pascal_import_type(item["return_type"])
                    call_args = self.render_call_args(item.get("params", []))

                    if params:
                        lines.append(f"function {class_name}.{method_name}({params}): {ret};")
                    else:
                        lines.append(f"function {class_name}.{method_name}: {ret};")

                    lines.append("begin")

                    if call_args:
                        lines.append(f"  Result := {export_name}(FHandle, {call_args});")
                    else:
                        lines.append(f"  Result := {export_name}(FHandle);")

                    lines.append("end;")
                    lines.append("")

                elif mk == "procedure":
                    params = self.render_import_params(item.get("params", []))
                    call_args = self.render_call_args(item.get("params", []))

                    if params:
                        lines.append(f"procedure {class_name}.{method_name}({params});")
                    else:
                        lines.append(f"procedure {class_name}.{method_name};")

                    lines.append("begin")

                    if call_args:
                        lines.append(f"  {export_name}(FHandle, {call_args});")
                    else:
                        lines.append(f"  {export_name}(FHandle);")

                    lines.append("end;")
                    lines.append("")

        lines.append("begin")
        lines.append("end.")
        lines.append("")

        return "\n".join(lines)

    def write_fpc_import_unit(self):
        if self.module_kind != "library":
            return

        if not self.exports:
            return
        
        # todo !!!
        self.output_dir = "testout"
        
        imports_dir = os.path.join(
            self.output_dir,
            "imports"
        )
        
        os.makedirs(imports_dir, exist_ok=True)
        
        lib_name = self.program_name.lower()
        filename = os.path.join(
            imports_dir,
            f"import_{lib_name}.pas"
        )
        
        # todo !!!
        #print("WRITE IMPORT UNIT:", filename)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.render_fpc_import_unit())

    def emit_load_pointer_reference(
        self,
        ctx,
        name,
        info
    ):
        source_kind = info.get(
            "source_kind"
        )

        if source_kind == "local":
            return self.emit_load_local_var(
                ctx,
                name,
                info
            )

        if source_kind == "param":
            return self.emit_load_param(
                ctx,
                name
            )

        if source_kind == "global":
            return self.emit_load_var(
                name,
                info
            )

        raise CompileError(
            ctx,
            "E0019",
            text=(
                f"unknown pointer source for {name}"
            )
        )
    
    def resolve_pointer_record_path(
        self,
        ctx,
        parts
    ):
        ptr_name = parts[0]
        ptr_key = ptr_name.lower()

        ptr_info = self.find_local_var(
            ptr_name
        )

        source_kind = None

        if ptr_info is not None:
            source_kind = "local"

        if ptr_info is None:
            ptr_info = self.find_param(
                ptr_name
            )

            if ptr_info is not None:
                source_kind = "param"

        if ptr_info is None:
            ptr_info = self.vars.get(
                ptr_key
            )

            if ptr_info is not None:
                source_kind = "global"

        if ptr_info is None:
            raise CompileError(
                ctx,
                "E0001",
                name=ptr_name
            )

        ptr_type = self.resolve_type(
            ptr_info["type"]
        )

        if (
            not isinstance(ptr_type, str)
            or not ptr_type.startswith("^")
        ):
            raise CompileError(
                ctx,
                "E0005",
                got=ptr_type,
                expected="pointer"
            )

        record_type = self.resolve_type(
            ptr_type[1:]
        )

        if record_type not in self.records:
            raise CompileError(
                ctx,
                "E0005",
                got=record_type,
                expected="record"
            )

        offset = 0
        field = None
        current_type = record_type

        for index, field_name in enumerate(
            parts[1:]
        ):
            if current_type not in self.records:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=current_type,
                    expected="record"
                )

            record = self.records[
                current_type
            ]

            field_key = field_name.lower()

            if field_key not in record.fields:
                raise CompileError(
                    ctx,
                    "E0001",
                    name=".".join(parts)
                )

            field = record.fields[
                field_key
            ]

            offset += field.offset

            current_type = self.resolve_type(
                field.type
            )

            is_last = (
                index
                == len(parts[1:]) - 1
            )

            if not is_last:
                if (
                    isinstance(current_type, str)
                    and current_type.startswith("^")
                ):
                    current_type = (
                        current_type[1:]
                    )

                if current_type not in self.records:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=current_type,
                        expected="record"
                    )

        result_info = dict(
            ptr_info
        )

        result_info["source_kind"] = (
            source_kind
        )

        result_info["is_local"] = (
            source_kind == "local"
        )

        result_info["is_param"] = (
            source_kind == "param"
        )

        result_info["is_global"] = (
            source_kind == "global"
        )

        result_info["type"] = (
            ptr_type
        )

        return (
            result_info,
            offset,
            field
        )
    
    def resolve_array_record_field(self, ctx, var_name, index_expr_ctx, field_parts):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
            
        var_info, array_info = self.get_array_info(ctx, var_name)

        element_type = array_info.element_type

        if element_type not in self.records:
            raise CompileError(ctx, "E0005", got=element_type, expected="record array")

        # Index berechnen
        #index_type = self.visit(index_expr_ctx)
        index_type = self.visit(index_exprs[0])

        if index_type != "integer":
            raise CompileError(ctx, "E0005", got=index_type, expected="integer")

        if not getattr(array_info, "is_dynamic", False):
            self.emit_array_bounds_check(ctx, var_name, array_info)

        if array_info.index_min != 0:
            self.emit_sub(REG_EAX, array_info.index_min)

        self.emit_imul(REG_EAX, REG_EAX, array_info.element_size)
        self.emit_add (REG_EAX, var_info["slot"])

        # Array-Basis holen
        self.emit_mov_qword("r11", "r12", "arrays_vars")
        self.emit_movsxd(REG_RAX, REG_EAX)
        self.emit_add("r11", REG_RAX)

        # Jetzt zeigt R11 auf points[index]
        current_type = element_type
        field = None
        field_offset = 0

        for field_name in field_parts:
            record = self.records[current_type]
            field_key = field_name.lower()

            if field_key not in record.fields:
                raise CompileError(ctx, "E0001", name=field_name)

            field = record.fields[field_key]
            field_offset += field.offset
            current_type = field.type

            if field_name != field_parts[-1]:
                if current_type not in self.records:
                    raise CompileError(ctx, "E0005", got=current_type, expected="record")

        if field_offset != 0:
            self.emit_add("r11", field_offset)

        return field
    
    def resolve_type(
        self,
        type_name
    ):
        if not isinstance(
            type_name,
            str
        ):
            return type_name

        current = type_name.strip().lower()

        if not current:
            return current

        visited = set()

        while True:
            if current in visited:
                raise RuntimeError(
                    f"circular type alias detected: "
                    f"{type_name}"
                )

            visited.add(
                current
            )

            # ------------------------------------------------------
            # Pointertyp
            #
            # Beispiele:
            #
            #   ^Byte
            #   ^MyByte
            #   ^^Integer
            # ------------------------------------------------------
            if current.startswith("^"):
                base_type = current[1:]

                resolved_base = self.resolve_type(
                    base_type
                )

                # Ein Alias kann selbst bereits ein Pointer sein.
                #
                #   PByte  = ^Byte
                #   PPByte = ^PByte
                if (
                    isinstance(resolved_base, str)
                    and resolved_base.startswith("^")
                ):
                    return "^" + resolved_base

                return "^" + str(
                    resolved_base
                )

            # ------------------------------------------------------
            # Normaler Typalias
            # ------------------------------------------------------
            alias_target = self.type_aliases.get(
                current
            )

            if alias_target is not None:
                current = str(
                    alias_target
                ).strip().lower()

                continue

            # ------------------------------------------------------
            # Bekannte direkte Typen
            # ------------------------------------------------------
            if current == "boolean":
                return "boolean"

            if current in self.enums:
                return "integer"

            if current in self.subrange_types:
                return current

            if current in self.records:
                return current

            if current in self.arrays:
                return current

            if current in self.classes:
                return current

            return current
        
    def unit_search_directories(self):
        directories = []
        seen = set()

        def add(path, base_directory=None):
            if not path:
                return

            try:
                raw_path = os.fspath(path)
            except TypeError:
                return

            raw_path = raw_path.strip()

            if not raw_path:
                return

            if base_directory and not os.path.isabs(raw_path):
                raw_path = os.path.join(base_directory, raw_path)

            absolute_path = os.path.abspath(raw_path)
            key = os.path.normcase(os.path.normpath(absolute_path))

            if key in seen:
                return

            if os.path.isdir(absolute_path):
                seen.add(key)
                directories.append(absolute_path)

        def add_parent(filename):
            if not filename:
                return

            try:
                filename = os.fspath(filename)
            except TypeError:
                return

            filename = filename.strip()

            if not filename:
                return

            absolute_filename = os.path.abspath(filename)
            add(os.path.dirname(absolute_filename))

        source_directory = self.source_dir

        if not source_directory and self.source_file:
            source_directory = os.path.dirname(
                os.path.abspath(self.source_file)
            )

        current_directory = os.getcwd()

        # Source and current working directory.
        add(source_directory)
        add(current_directory)

        # Explicit compiler output directory.  Relative output directories
        # are checked relative to both cwd and the source directory.
        output_directory = getattr(CDATA, "output_dir", None)

        add(output_directory, current_directory)
        add(output_directory, source_directory)

        # Conventional project output directory used by pas2asmjit.py.
        add("testout", current_directory)
        add("testout", source_directory)

        # Derive directories from known output filenames.  Different driver
        # versions use different attribute names, so inspect all common ones.
        for attribute_name in (
            "obj_file",
            "object_file",
            "pui_file",
            "exe_file",
            "dll_file",
            "asm_file",
            "output_file"
        ):
            add_parent(getattr(CDATA, attribute_name, None))

        # Include/unit/object/library search paths.
        for attribute_name in (
            "IncludePaths",
            "UnitPaths",
            "link_object_paths",
            "link_library_paths"
        ):
            for path in getattr(CDATA, attribute_name, []) or []:
                add(path, current_directory)
                add(path, source_directory)

        # Explicit unit files or directories.
        for item in getattr(CDATA, "UnitFiles", []) or []:
            try:
                item_path = os.path.abspath(os.fspath(item))
            except TypeError:
                continue

            if os.path.isdir(item_path):
                add(item_path)
            elif os.path.isfile(item_path):
                add(os.path.dirname(item_path))

        # Already configured link objects can also reveal the unit output
        # directory even when no separate output_dir option exists.
        for item in getattr(CDATA, "link_object_files", []) or []:
            add_parent(item)

        return directories

    def find_unit_pui_file(self, ctx, unit_name, required=True):
        """Find the PUI belonging to *unit_name* without loading Pascal source."""
        normalized = self.normalize_unit_name(unit_name)
        last_part  = unit_name.split(".")[-1]

        candidate_names = []

        def add_candidate(name):
            if name and name not in candidate_names:
                candidate_names.append(name)

        add_candidate(unit_name + ".pui")
        add_candidate(unit_name.lower() + ".pui")
        add_candidate(normalized + ".pui")
        add_candidate(normalized.lower() + ".pui")
        add_candidate(last_part + ".pui")
        add_candidate(last_part.lower() + ".pui")

        search_dirs = self.unit_search_directories()

        # Fast path: conventional filenames.
        for directory in search_dirs:
            for filename in candidate_names:
                path = os.path.abspath(os.path.join(directory, filename))

                if os.path.isfile(path):
                    return path

        # Fallback: inspect PUI headers. This also supports a source filename
        # that differs from the qualified Pascal unit name.
        wanted = normalized.lower()

        for directory in search_dirs:
            try:
                entries = os.listdir(directory)
            except OSError:
                continue

            for filename in entries:
                if not filename.lower().endswith(".pui"):
                    continue

                path = os.path.join(directory, filename)

                try:
                    with open(path, "r", encoding="utf-8") as stream:
                        data = json.load(stream)
                except (OSError, ValueError, TypeError):
                    continue

                pui_unit = data.get("unit", {})
                pui_name = pui_unit.get("normalized_name")

                if not pui_name:
                    pui_name = self.normalize_unit_name(
                        pui_unit.get("name", "")
                    )

                if str(pui_name).lower() == wanted:
                    return os.path.abspath(path)

        if required:
            searched = ", ".join(search_dirs)

            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"compiled unit interface not found: {unit_name}.pui; "
                    f"searched: {searched}"
                )
            )

        return None

    def validate_unit_pui(self, ctx, unit_name, pui_path, data):
        if data.get("format") != "dBase2Many Pascal Unit Interface":
            raise CompileError(
                ctx,
                "E0019",
                text=f"invalid PUI format: {pui_path}"
            )

        if int(data.get("version", 0)) != 1:
            raise CompileError(
                ctx,
                "E0019",
                text=f"unsupported PUI version in {pui_path}"
            )

        pui_unit = data.get("unit", {})
        stored_name = pui_unit.get("name", "")

        if (
            self.normalize_unit_name(stored_name)
            != self.normalize_unit_name(unit_name)
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"PUI unit mismatch: requested {unit_name}, "
                    f"found {stored_name}"
                )
            )

        target = data.get("target", {})
        current_target = CDATA.args_target.lower()

        nt32_targets = {"nt35", "winnt", "win32"}
        pui_target = str(target.get("target", "")).lower()

        if current_target in nt32_targets:
            compatible = (
                pui_target in nt32_targets
                and target.get("object_format") == "coff32"
                and target.get("machine") == "i386"
                and int(target.get("pointer_size", 0)) == 4
                and target.get("calling_convention") == "cdecl"
            )
        else:
            compatible = pui_target == current_target

        if not compatible:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"PUI target is incompatible with {current_target}: "
                    f"{pui_path}"
                )
            )

    def add_pui_link_object(self, filename):
        filename = os.path.abspath(filename)
        wanted   = os.path.normcase(os.path.normpath(filename))

        for old in CDATA.link_object_files:
            old_abs = os.path.abspath(os.fspath(old))
            old_key = os.path.normcase(os.path.normpath(old_abs))

            if old_key == wanted:
                return

        CDATA.link_object_files.append(filename)

    def add_pui_link_archive(self, filename):
        filename = os.path.abspath(filename)
        wanted   = os.path.normcase(os.path.normpath(filename))

        for old in CDATA.link_archive_files:
            old_abs = os.path.abspath(os.fspath(old))
            old_key = os.path.normcase(os.path.normpath(old_abs))

            if old_key == wanted:
                return

        CDATA.link_archive_files.append(filename)

    def add_pui_resource_file(self, filename):
        filename = os.path.abspath(filename)
        wanted   = os.path.normcase(os.path.normpath(filename))

        resource_files = getattr(
            CDATA,
            "link_resource_files",
            None
        )

        if resource_files is None:
            resource_files = []
            CDATA.link_resource_files = resource_files

        for old in resource_files:
            old_abs = os.path.abspath(os.fspath(old))
            old_key = os.path.normcase(os.path.normpath(old_abs))

            if old_key == wanted:
                return

        resource_files.append(filename)

    def resolve_pui_path(self, pui_directory, filename):
        filename = os.fspath(filename)

        if os.path.isabs(filename):
            return os.path.normpath(filename)

        return os.path.normpath(
            os.path.join(pui_directory, filename)
        )

    def register_pui_classes(self, ctx, unit_name, class_items):
        if not class_items:
            return

        pending = {}

        for class_item in class_items:
            if not isinstance(class_item, dict):
                continue

            class_name = str(
                class_item.get("name", "")
            ).strip()

            if not class_name:
                continue

            pending[class_name.lower()] = class_item

        while pending:
            progress = False

            for class_key, class_item in list(pending.items()):
                class_name = str(
                    class_item["name"]
                ).strip()

                parent_name = class_item.get("parent")
                parent_key = None

                if parent_name:
                    parent_key = str(parent_name).lower()

                    if (
                        parent_key not in self.classes
                        and parent_key in pending
                    ):
                        continue

                    if parent_key not in self.classes:
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                f"PUI class {class_name} references "
                                f"unknown parent class {parent_name}"
                            )
                        )

                if class_key in self.classes:
                    old_unit = self.pui_class_units.get(class_key)

                    if old_unit == unit_name:
                        del pending[class_key]
                        progress = True
                        continue

                    raise CompileError(
                        ctx,
                        "E0002",
                        name=class_name
                    )

                fields = {}

                for field_item in class_item.get("fields", []):
                    if not isinstance(field_item, dict):
                        continue

                    field_name = str(
                        field_item.get("name", "")
                    ).strip()

                    if not field_name:
                        continue

                    field_type = self.resolve_type(
                        field_item.get("type", "")
                    )

                    fields[field_name.lower()] = RecordFieldInfo(
                        name=field_name,
                        type=field_type,
                        offset=int(field_item.get("offset", 0)),
                        size=int(
                            field_item.get(
                                "size",
                                self.pointer_slot_size()
                            )
                        ),
                        visibility=field_item.get(
                            "visibility",
                            "public"
                        )
                    )

                methods = {}

                if parent_key is not None:
                    parent_cls = self.classes[
                        parent_key
                    ]

                    for inherited_name, inherited_overloads in (
                        parent_cls.methods.items()
                    ):
                        methods[inherited_name] = list(
                            inherited_overloads
                        )

                for method_item in class_item.get("methods", []):
                    if not isinstance(method_item, dict):
                        continue

                    method_name = str(
                        method_item.get("name", "")
                    ).strip()

                    symbol = str(
                        method_item.get("symbol", "")
                    ).strip()

                    if not method_name or not symbol:
                        continue

                    params = []

                    for param in method_item.get("params", []):
                        params.append({
                            "name": param.get("name", ""),
                            "type": self.resolve_type(
                                param.get("type", "")
                            ),
                            "is_var": bool(
                                param.get("is_var", False)
                            )
                        })

                    return_type = method_item.get("return_type")

                    if return_type:
                        return_type = self.resolve_type(return_type)

                    method = ClassMethodInfo(
                        name=method_name,
                        kind=method_item.get("kind", "procedure"),
                        label=None,
                        params=params,
                        owner=class_key,
                        return_type=return_type,
                        implemented=True,
                        mangled=symbol,
                        visibility=method_item.get(
                            "visibility",
                            "public"
                        )
                    )

                    method.is_virtual = bool(
                        method_item.get(
                            "is_virtual",
                            False
                        )
                    )

                    method.is_override = bool(
                        method_item.get(
                            "is_override",
                            False
                        )
                    )

                    method.vmt_offset = (
                        int(
                            method_item[
                                "vmt_offset"
                            ]
                        )
                        if method_item.get(
                            "vmt_offset"
                        ) is not None
                        else None
                    )

                    method_key = (
                        method_name.lower()
                    )

                    methods.setdefault(
                        method_key,
                        []
                    )

                    signature = self.method_signature(
                        method.params
                    )

                    methods[method_key] = [
                        old_method
                        for old_method in methods[
                            method_key
                        ]
                        if self.method_signature(
                            old_method.params
                        ) != signature
                    ]

                    methods[
                        method_key
                    ].append(
                        method
                    )

                properties = {}

                for prop_item in class_item.get("properties", []):
                    if not isinstance(prop_item, dict):
                        continue

                    prop_name = str(
                        prop_item.get("name", "")
                    ).strip()

                    if not prop_name:
                        continue

                    properties[prop_name.lower()] = PropertyInfo(
                        name=prop_name,
                        ptype=self.resolve_type(
                            prop_item.get("type", "")
                        ),
                        visibility=prop_item.get(
                            "visibility",
                            "public"
                        ),
                        read_name=prop_item.get("read"),
                        write_name=prop_item.get("write")
                    )

                class_info = ClassInfo(
                    name=class_name,
                    fields=fields,
                    methods=methods,
                    properties=properties,
                    size=int(class_item.get("size", 0)),
                    parent=parent_key
                )

                self.classes[
                    class_key
                ] = class_info

                self.configure_class_vmt_metadata(
                    ctx,
                    class_key,
                    vmt_symbol=class_item.get(
                        "vmt_symbol"
                    ),
                    class_name_symbol=class_item.get(
                        "class_name_symbol"
                    )
                )

                self.pui_class_units[
                    class_key
                ] = unit_name

                del pending[class_key]
                progress = True

            if not progress:
                unresolved = ", ".join(
                    sorted(
                        item.get("name", key)
                        for key, item in pending.items()
                    )
                )

                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "could not resolve PUI class inheritance: "
                        + unresolved
                    )
                )

    def emit_class_method_call(
        self,
        method,
        comment=""
    ):
        local_label = getattr(method, "label",   None)
        mangled     = getattr(method, "mangled", None)

        target = (
            local_label
            if local_label is not None
            else mangled
        )

        if not target:
            raise RuntimeError(
                "class method has no call target: "
                + str(
                    getattr(
                        method,
                        "name",
                        "<unknown>"
                    )
                )
            )

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            if getattr(method, "is_virtual", False):
                vmt_offset = getattr(
                    method,
                    "vmt_offset",
                    None
                )

                if vmt_offset is None:
                    raise RuntimeError(
                        "virtual method has no VMT offset: "
                        + method.name
                    )

                # Self liegt oben auf dem Stack.
                self.writer.emit_mov_reg_mem32("edx", "esp", 0)
                # ECX = Self^.VMT
                self.writer.emit_mov_reg_mem32("ecx", "edx", 0)
                # ECX = VMT-Slot
                self.writer.emit_mov_reg_mem32("ecx", "ecx", vmt_offset)
                self.writer.emit_call_reg32   ("ecx")

                return

            self.writer.emit_call_external(target)
            return

        if local_label is None:
            raise RuntimeError(tr("PUI class imports currently require COFF32"))

        self.emit_call_lbl(local_label, comment=comment)

    def register_pui_routines(self, ctx, unit_name, data):
        symbols = data.get("symbols", {})
        unit_prefix = self.normalize_unit_name(unit_name)

        for item in symbols.get("functions", []):
            name   = item["name"]
            symbol = item["symbol"]
            params = list(item.get("params", []))

            info = {
                "name": name,
                "scoped_name": item.get(
                    "scoped_name",
                    unit_prefix + "_" + name
                ),
                "return_type": self.resolve_type(
                    item["return_type"]
                ),
                
                "label": None,
                "symbol": symbol,
                "mangled": symbol,
                "params": params,
                
                "calling_convention": (
                    self.normalize_calling_convention(
                        ctx,
                        item.get(
                            "calling_convention",
                            "cdecl"
                        )
                    )
                ),
                
                "external": True,
                "external_kind": (
                    "dll"
                    if item.get("dll_import", False)
                    else "coff"
                ),
                
                "dll_import": bool(
                    item.get("dll_import", False)
                ),

                "dll": item.get("dll"),
                "import_name": item.get("import_name"),
                "ordinal": item.get("ordinal"),
                
                "unit": unit_name,
                "pui": True
            }

            scoped_key = info["scoped_name"].lower()
            self.functions[scoped_key] = info

            # Preserve the first unqualified symbol. A future qualified-name
            # resolver can select the scoped entry when two units export the
            # same Pascal identifier.
            self.functions.setdefault(name.lower(), info)

        for item in symbols.get("procedures", []):
            name   = item["name"]
            symbol = item["symbol"]
            params = list(item.get("params", []))

            info = {
                "name": name,
                "scoped_name": item.get(
                    "scoped_name",
                    unit_prefix + "_" + name
                ),
                
                "label": None,
                "symbol": symbol,
                "mangled": symbol,
                "params": params,
                
                "calling_convention": (
                    self.normalize_calling_convention(
                        ctx,
                        item.get(
                            "calling_convention",
                            "cdecl"
                        )
                    )
                ),
                
                "external": True,
                "external_kind": (
                    "dll"
                    if item.get("dll_import", False)
                    else "coff"
                ),

                "dll_import": bool(
                    item.get("dll_import", False)
                ),
                
                "dll": item.get("dll"),
                "import_name": item.get("import_name"),
                "ordinal": item.get("ordinal"),
                
                "unit": unit_name,
                "pui": True
            }

            scoped_key = info["scoped_name"].lower()
            self.procedures[scoped_key] = info
            self.procedures.setdefault(name.lower(), info)

        classes = symbols.get("classes") or []
        self.register_pui_classes(
            ctx,
            unit_name,
            classes
        )

    def local_routine_calling_convention(
        self,
        ctx
    ):
        """
        Liest die Aufrufkonvention aus dem Routine-Header.

        Unterstützt sowohl:

            routineCallingConvention.callingConvention()

        als auch Parser-Versionen, bei denen der äußere Kontext direkt
        den Text "cdecl", "stdcall" oder "pascal" enthält.
        """
        accessor = getattr(
            ctx,
            "routineCallingConvention",
            None
        )

        if accessor is None:
            return "cdecl"

        directive = accessor()

        if directive is None:
            return "cdecl"

        convention_accessor = getattr(
            directive,
            "callingConvention",
            None
        )

        if convention_accessor is not None:
            convention_ctx = convention_accessor()

            if convention_ctx is not None:
                return self.normalize_calling_convention(
                    ctx,
                    convention_ctx
                )

        return self.normalize_calling_convention(
            ctx,
            directive
        )

    def register_pui_imports(
        self,
        ctx,
        unit_name,
        data
    ):
        imports = data.get(
            "imports",
            {}
        )

        if imports is None:
            imports = {}

        if not isinstance(
            imports,
            dict
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"invalid imports section in "
                    f"{unit_name}.pui"
                )
            )

        for raw_dll_name, raw_items in imports.items():
            dll_name = os.path.basename(
                str(raw_dll_name).strip()
            )

            if not dll_name:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"empty DLL name in "
                        f"{unit_name}.pui"
                    )
                )

            if not isinstance(
                raw_items,
                list
            ):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"invalid import list for "
                        f"{dll_name} in {unit_name}.pui"
                    )
                )

            use_runtime_thunks = (
                self.is_packed_runtime_library(
                    dll_name
                )
            )

            # Vorhandenen DLL-Key unabhängig von Groß-/Kleinschreibung
            # wiederverwenden.
            target_dll_name = None

            for existing_dll_name in CDATA.imports:
                if (
                    str(existing_dll_name).lower()
                    == dll_name.lower()
                ):
                    target_dll_name = existing_dll_name
                    break

            if target_dll_name is None:
                target_dll_name = dll_name

            target_items = None

            if not use_runtime_thunks:
                target_items = CDATA.imports.setdefault(
                    target_dll_name,
                    []
                )

            for raw_item in raw_items:
                if not isinstance(
                    raw_item,
                    dict
                ):
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            f"invalid import entry for "
                            f"{dll_name} in {unit_name}.pui"
                        )
                    )

                symbol = raw_item.get(
                    "symbol"
                )

                import_name = raw_item.get(
                    "name"
                )

                ordinal = raw_item.get(
                    "ordinal"
                )

                if not isinstance(
                    symbol,
                    str
                ) or not symbol:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "DLL import without internal symbol "
                            f"in {unit_name}.pui"
                        )
                    )

                if (
                    not isinstance(
                        import_name,
                        str
                    )
                    or not import_name
                ):
                    import_name = None

                if ordinal is None:
                    ordinal = self.find_known_dll_import_ordinal(
                        dll_name,
                        import_name
                    )

                if (
                    import_name is None
                    and ordinal is None
                ):
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            f"DLL import {symbol} has neither "
                            f"name nor ordinal in {unit_name}.pui"
                        )
                    )

                # --------------------------------------------------
                # Gepackte Runtime:
                #
                # Kein PE-Import wird erzeugt. Stattdessen verweist das
                # COFF-Symbol auf den internen Runtime-Thunk.
                # --------------------------------------------------
                if use_runtime_thunks:
                    thunk_name = import_name

                    if thunk_name is None:
                        thunk_name = (
                            self.find_known_dll_import_name(
                                dll_name,
                                ordinal
                            )
                        )

                    if thunk_name is None:
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                f"packed runtime import {symbol} "
                                "has no resolvable thunk name "
                                f"in {unit_name}.pui"
                            )
                        )

                    writer = self.backend.writer

                    if not hasattr(
                        writer,
                        "add_runtime_symbol_alias"
                    ):
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                "backend does not support "
                                "runtime symbol aliases"
                            )
                        )

                    writer.add_runtime_symbol_alias(
                        symbol,
                        thunk_name
                    )

                    key = (
                        dll_name.lower(),
                        thunk_name
                    )

                    self.dll_import_symbols.setdefault(
                        key,
                        symbol
                    )

                    match = re.match(
                        r"^__dllimp_(\d+)_",
                        symbol
                    )

                    if match:
                        self.next_dll_import_id = max(
                            self.next_dll_import_id,
                            int(match.group(1)) + 1
                        )

                    continue

                item = {
                    "symbol": symbol
                }

                if import_name is not None:
                    item["name"] = import_name

                if ordinal is not None:
                    item["ordinal"] = int(
                        ordinal
                    )

                # Dasselbe interne Symbol darf nicht auf zwei
                # verschiedene DLL-Exporte zeigen.
                for (
                    existing_dll,
                    existing_items
                ) in CDATA.imports.items():
                    for existing_item in existing_items:
                        if (
                            isinstance(
                                existing_item,
                                dict
                            )
                            and existing_item.get(
                                "symbol"
                            ) == symbol
                            and (
                                str(existing_dll).lower()
                                != str(target_dll_name).lower()
                                or existing_item.get("name")
                                != item.get("name")
                                or existing_item.get("ordinal")
                                != item.get("ordinal")
                            )
                        ):
                            raise CompileError(
                                ctx,
                                "E0019",
                                text=(
                                    "conflicting imported COFF symbol "
                                    f"{symbol} while loading "
                                    f"{unit_name}.pui"
                                )
                            )

                already_registered = any(
                    isinstance(
                        existing_item,
                        dict
                    )
                    and existing_item.get("symbol")
                    == symbol
                    and existing_item.get("name")
                    == item.get("name")
                    and existing_item.get("ordinal")
                    == item.get("ordinal")
                    for existing_item in target_items
                )

                if not already_registered:
                    target_items.append(
                        item
                    )

                if import_name is not None:
                    key = (
                        dll_name.lower(),
                        import_name
                    )

                    self.dll_import_symbols.setdefault(
                        key,
                        symbol
                    )

                match = re.match(
                    r"^__dllimp_(\d+)_",
                    symbol
                )

                if match:
                    self.next_dll_import_id = max(
                        self.next_dll_import_id,
                        int(match.group(1)) + 1
                    )

    def add_unit_initializer(self, symbol, external=False):
        if not symbol:
            return

        for item in self.unit_init_labels:
            if isinstance(item, dict):
                old_symbol = item.get("symbol")
            else:
                old_symbol = item

            if old_symbol == symbol:
                return

        self.unit_init_labels.append({
            "symbol": symbol,
            "external": bool(external)
        })

    def emit_unit_initializers(self):
        """Emit unit initialization calls in dependency order.

        Internal initializers are normal labels in the current code stream.
        Initializers loaded from a PUI are external COFF symbols and must
        therefore create a relocation instead of a local-label fixup.
        """
        for item in self.unit_init_labels:
            if isinstance(item, dict):
                symbol   = item["symbol"]
                external = bool(item.get("external", False))
            else:
                symbol   = item
                external = False

            if external:
                if CDATA.args_target in ("nt35", "winnt", "win32"):
                    self.writer.emit_call_external(symbol)
                else:
                    self.emit_call(symbol, comment="external unit init")
            else:
                self.emit_call_lbl(symbol, comment="internal unit init")

    def emit_registered_routine_call(self, routine, comment=""):
        """Call a local routine label or a symbol imported through a PUI."""
        if routine.get("external", False):
            symbol = routine.get("symbol") or routine.get("mangled")

            if not symbol:
                raise RuntimeError(
                    "external routine has no COFF symbol: "
                    + str(routine.get("name"))
                )

            if CDATA.args_target in ("nt35", "winnt", "win32"):
                self.writer.emit_call_external(symbol)
            else:
                self.emit_call(symbol, comment=comment)
            return

        label = routine.get("label")

        if not label:
            raise RuntimeError(
                "internal routine has no label: "
                + str(routine.get("name"))
            )

        self.emit_call_lbl(label, comment=comment)

    def load_pui_unit(self, ctx, unit_name, pui_path):
        unit_key = self.normalize_unit_name(unit_name)

        if unit_key in self.loaded_units:
            return

        if unit_key in self.loading_units:
            raise CompileError(
                ctx,
                "E0019",
                text=f"circular unit reference detected: {unit_name}"
            )

        self.loading_units.add(unit_key)

        try:
            with open(pui_path, "r", encoding="utf-8") as stream:
                data = json.load(stream)

            self.validate_unit_pui(
                ctx,
                unit_name,
                pui_path,
                data
            )

            # Dependencies are loaded first. This gives the correct Pascal
            # initialization order and adds all transitive object files.
            uses = data.get("uses", {})

            dependencies = []

            for section_name in ("interface", "implementation"):
                for dependency in uses.get(section_name, []):
                    if dependency not in dependencies:
                        dependencies.append(dependency)

            for dependency in dependencies:
                self.load_unit(ctx, dependency)

            pui_directory = os.path.dirname(os.path.abspath(pui_path))

            object_name = data.get("object", {}).get("file")

            if not object_name:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=f"PUI does not name an object file: {pui_path}"
                )

            object_path = self.resolve_pui_path(
                pui_directory,
                object_name
            )

            if not os.path.isfile(object_path):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=f"unit object file not found: {object_path}"
                )

            self.add_pui_link_object(object_path)

            link = data.get("link", {})

            for object_name in link.get("objects", []):
                path = self.resolve_pui_path(
                    pui_directory,
                    object_name
                )

                if not os.path.isfile(path):
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=f"PUI linked object file not found: {path}"
                    )

                self.add_pui_link_object(path)

            for archive_name in link.get("archives", []):
                path = self.resolve_pui_path(
                    pui_directory,
                    archive_name
                )

                if not os.path.isfile(path):
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=f"PUI linked archive not found: {path}"
                    )

                self.add_pui_link_archive(path)

            for resource_name in link.get("resources", []):
                path = self.resolve_pui_path(
                    pui_directory,
                    resource_name
                )

                if not os.path.isfile(path):
                    # Eine PUI darf einen unveränderten {$R}-Dateinamen
                    # enthalten. Beim späteren Link werden daher zusätzlich
                    # die mit -Fo angegebenen Objektpfade durchsucht.
                    for search_directory in (
                        getattr(
                            CDATA,
                            "link_object_paths",
                            []
                        )
                        or []
                    ):
                        candidate = os.path.abspath(
                            os.path.join(
                                search_directory,
                                os.fspath(resource_name)
                            )
                        )

                        if os.path.isfile(candidate):
                            path = candidate
                            break

                if not os.path.isfile(path):
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "PUI resource file not found: "
                            + str(resource_name)
                        )
                    )

                self.add_pui_resource_file(path)

            self.register_pui_types(
                ctx,
                unit_name,
                data
            )

            self.register_pui_constants(
                ctx,
                unit_name,
                data
            )

            # Die eingebundene Unit-.o-Datei kann Relocations auf
            # synthetische DLL-Import-Symbole enthalten. Diese müssen
            # vor dem finalen PE-Link wieder in CDATA.imports stehen.
            self.register_pui_imports(
                ctx,
                unit_name,
                data
            )

            self.register_pui_routines(
                ctx,
                unit_name,
                data
            )

            init_symbol = data.get(
                "initialization",
                {}
            ).get("symbol")

            self.add_unit_initializer(
                init_symbol,
                external=True
            )

            self.loaded_puis[unit_key] = data
            self.loaded_units[unit_key] = {
                "kind": "pui",
                "pui": os.path.abspath(pui_path),
                "object": object_path
            }

        finally:
            self.loading_units.discard(unit_key)

    def load_unit_source(self, ctx, unit_name):
        """Legacy source-unit loading; disabled unless explicitly requested."""
        unit_key = self.normalize_unit_name(unit_name)

        if unit_key in self.loaded_units:
            return

        if unit_key in self.loading_units:
            raise CompileError(
                ctx,
                "E0019",
                text=f"circular unit reference detected: {unit_name}"
            )

        unit_file = self.find_unit_file(ctx, unit_name)
        self.loading_units.add(unit_key)

        old_source_file = self.source_file
        old_source_dir  = self.source_dir
        old_unit        = self.current_unit

        try:
            with open(unit_file, "r", encoding="utf-8") as stream:
                raw_text = stream.read()

            pp = PascalPreprocessor(
                defines=getattr(CDATA, "Defines", [])
            )
            text = pp.process(raw_text)

            self.source_file  = unit_file
            self.source_dir   = os.path.dirname(unit_file)
            self.current_unit = unit_key

            stream = InputStream(text)
            lexer  = PascalLexer(stream)
            tokens = CommonTokenStream(lexer)
            parser = PascalParser(tokens)
            tree   = parser.sourceFile()

            if parser.getNumberOfSyntaxErrors() > 0:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=f"syntax error in unit {unit_name}"
                )

            self.visit(tree)

            self.loaded_units[unit_key] = {
                "kind": "source",
                "source": unit_file
            }

        finally:
            self.current_unit = old_unit
            self.source_file  = old_source_file
            self.source_dir   = old_source_dir
            self.loading_units.discard(unit_key)

    def load_unit(self, ctx, unit_name):
        """
        Load a compiled unit interface.

        By default source files are not parsed here. This prevents the unit
        implementation from being emitted a second time into the program.
        """
        unit_key = self.normalize_unit_name(unit_name)

        if unit_key in self.loaded_units:
            return

        pui_path = self.find_unit_pui_file(
            ctx,
            unit_name,
            required=False
        )

        if pui_path:
            self.load_pui_unit(
                ctx,
                unit_name,
                pui_path
            )
            return

        if getattr(CDATA, "allow_source_units", False):
            self.load_unit_source(ctx, unit_name)
            return

        searched = ", ".join(
            self.unit_search_directories()
        )

        raise CompileError(
            ctx,
            "E0019",
            text=(
                f"compiled unit interface not found: {unit_name}.pui; "
                f"searched: {searched}; "
                f"compile the unit first or enable CDATA.allow_source_units"
            )
        )

    def find_current_class_field(self, name):
        if self.current_class is None:
            return None

        cls = self.classes[self.current_class]
        key = name.lower()

        if key not in cls.fields:
            return None

        return cls.fields[key]
    
    def find_export_method_overload(self, ctx, overloads, wanted_types):
        for method in overloads:
            method_types = [
                self.resolve_type(p["type"])
                for p in method.params
            ]

            if method_types == wanted_types:
                return method

        raise CompileError(
            ctx,
            "E0019",
            text=f"export overload not found"
        )
    
    def export_wrapper_suffix(self, params):
        if not params:
            return ""

        return "_" + "_".join(
            self.pascal_import_type(p["type"])
            for p in params
        ).replace(" ", "")

    def find_export_function_overload(self, name, wanted_types):
        key = name.lower()

        if key not in self.functions:
            return None

        func = self.functions[key]

        func_types = [
            self.resolve_type(p["type"])
            for p in func.get("params", [])
        ]

        if func_types == wanted_types:
            return func

        return None
    
    def find_const(self, name):
        key = name.lower()

        for scope in reversed(self.local_const_stack):
            if key in scope:
                return scope[key]

        if key in self.constants:
            return self.constants[key]

        return None
    
    def find_function(self, name):
        for i in range(len(self.scope_stack), -1, -1):
            scoped = "_".join(self.scope_stack[:i] + [name])
            key = scoped.lower()
            if key in self.functions:
                return self.functions[key]
        return None
    
    def find_procedure(self, name):
        for i in range(len(self.scope_stack), -1, -1):
            scoped = "_".join(self.scope_stack[:i] + [name])
            key = scoped.lower()
            if key in self.procedures:
                return self.procedures[key]
        return self.procedures.get(name.lower())
    
    def find_param(self, name):
        key = name.lower()

        if key in self.current_proc_params:
            return self.current_proc_params[key]

        return None
    
    def find_local_var(self, name):
        key = name.lower()

        for scope in reversed(self.local_var_stack):
            if key in scope["vars"]:
                return scope["vars"][key]

        return None
    
    def find_class_method_export(self, qualified_name):
        parts = qualified_name.split(".")

        if len(parts) != 2:
            return None

        class_name  = parts[0]
        method_name = parts[1]

        cls = self.classes.get(class_name.lower())

        if not cls:
            return None

        for m in cls.methods:
            if m.name.lower() == method_name.lower():
                return cls, m

        return None
    
    def find_class_method_overload(self, ctx, cls, method_name, actual_types):
        key = method_name.lower()
        
        if key not in cls.methods:
            raise CompileError(
                ctx,
                "E0019",
                text=f"class {cls.name} has no method {method_name}"
            )
        
        candidates = cls.methods[key]
        
        for method in candidates:
            params = method.params
            
            if len(params) != len(actual_types):
                continue
            
            ok = True
            
            for p, actual_type in zip(params, actual_types):
                formal_type = self.resolve_type(p["type"])
                
                if formal_type != actual_type:
                    ok = False
                    break
            
            if ok:
                return method
        
        raise CompileError(
            ctx,
            "E0019",
            text = f"no matching overload for {cls.name}.{method_name}"
        )
    
    def find_class_method_recursive(self, ctx, class_name, method_name, actual_types):
        if isinstance(class_name, ClassInfo):
            class_key = class_name.name.lower()
        else:
            class_key = class_name.lower()
        
        if class_key not in self.classes:
            raise CompileError(ctx, "E0004", name=class_name)
        
        cls = self.classes[class_key]
        method_key = method_name.lower()
        
        if method_key in cls.methods:
            for method in cls.methods[method_key]:
                params = method.params
                
                if len(params) != len(actual_types):
                    continue
                
                ok = True
                
                for p, actual_type in zip(params, actual_types):
                    formal_type = self.resolve_type(p["type"])
                    
                    if formal_type != actual_type:
                        ok = False
                        break
                
                if ok:
                    return method, cls
        
        if cls.parent:
            return self.find_class_method_recursive(
                ctx,
                cls.parent,
                method_name,
                actual_types
            )
        
        raise CompileError(
            ctx,
            "E0019",
            text=f"no matching inherited overload for {class_name}.{method_name}"
        )
    
    def get_record_field(self, ctx, var_name, field_name):
        var_key   = var_name.lower()
        field_key = field_name.lower()

        if var_key not in self.vars:
            raise CompileError(ctx, "E0001", name=var_name)

        var_info = self.vars[var_key]
        record_type = var_info["type"]

        if record_type not in self.records:
            raise CompileError(ctx, "E0005", got=record_type, expected="record")

        record = self.records[record_type]

        if field_key not in record.fields:
            raise CompileError(ctx, "E0001", name=f"{var_name}.{field_name}")

        return var_info, record.fields[field_key]
    
    def get_array_info(self, ctx, var_name):
        key = var_name.lower()

        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=var_name)

        var_info = self.vars[key]
        array_type = var_info["type"]

        if array_type not in self.arrays:
            raise CompileError(ctx, "E0005", got=array_type, expected="array")

        return var_info, self.arrays[array_type]
        
    def collect_formal_params(self, ctx):
        params = []

        formal_param_list = ctx.formalParamList()

        if formal_param_list is None:
            return params

        for formal_ctx in formal_param_list.formalParam():
            modifier = None

            if (
                hasattr(formal_ctx, "paramModifier")
                and formal_ctx.paramModifier() is not None
            ):
                modifier = (
                    formal_ctx
                    .paramModifier()
                    .getText()
                    .lower()
                )

            param_type_ctx = formal_ctx.paramType()

            if param_type_ctx is None:
                raise CompileError(
                    formal_ctx,
                    "E0019",
                    text=(
                        "formal parameter has no type: "
                        + formal_ctx.getText()
                    )
                )

            open_array_ctx = None

            if hasattr(
                param_type_ctx,
                "openArrayType"
            ):
                open_array_ctx = (
                    param_type_ctx.openArrayType()
                )

            is_open_array = (
                open_array_ctx is not None
            )

            is_variant_open_array = False
            element_type = None

            if is_open_array:
                const_token = None

                if hasattr(
                    open_array_ctx,
                    "CONST"
                ):
                    const_token = (
                        open_array_ctx.CONST()
                    )

                if const_token is not None:
                    typ = "open_array:const"
                    element_type = "const"
                    is_variant_open_array = True

                else:
                    type_name_ctx = (
                        open_array_ctx.typeName()
                    )

                    if type_name_ctx is None:
                        raise CompileError(
                            formal_ctx,
                            "E0019",
                            text=(
                                "open array requires an "
                                "element type or const"
                            )
                        )

                    element_type = self.resolve_type(
                        type_name_ctx.getText()
                    )

                    typ = (
                        f"open_array:{element_type}"
                    )

            else:
                type_name_ctx = (
                    param_type_ctx.typeName()
                )

                if type_name_ctx is None:
                    raise CompileError(
                        formal_ctx,
                        "E0019",
                        text=(
                            "unsupported formal parameter type: "
                            + param_type_ctx.getText()
                        )
                    )

                typ = self.resolve_type(
                    type_name_ctx.getText()
                )

            ident_list_ctx = (
                formal_ctx.identList()
            )

            if ident_list_ctx is None:
                raise CompileError(
                    formal_ctx,
                    "E0019",
                    text="formal parameter has no name"
                )

            for ident in ident_list_ctx.IDENT():
                params.append({
                    "name": ident.getText(),
                    "type": typ,

                    "modifier": modifier,
                    "is_var": modifier == "var",
                    "is_const": (
                        modifier == "const"
                        or is_variant_open_array
                    ),

                    "is_open_array": is_open_array,

                    "is_variant_open_array": (
                        is_variant_open_array
                    ),

                    "element_type": element_type
                })

        return params
    
    def scoped_name(self, name):
        if self.scope_stack:
            return "_".join(self.scope_stack + [name])
        return name

    def variable_ref_has_caret(self, ref):
        return any(self.suffix_is_caret(suffix) for suffix in ref.variableSuffix())
    
    def add_asm_label_mapping(self, asmjit_label, target_label):
        self.asm_label_mappings.append({
            "asmjit": asmjit_label,
            "target": target_label
        })
    
    def fpc_mangle_type(self, typ):
        typ = self.resolve_type(typ)

        if typ == "integer":
            return "INTEGER"

        if typ == "double":
            return "DOUBLE"

        if typ == "string":
            return "ANSISTRING"

        if self.is_pointer_type(
            typ,
            include_nil=False
        ):
            return "POINTER"

        return str(typ).upper()

    def fpc_mangle_params(self, params):
        if not params:
            return ""

        return "".join(
            "$" + self.fpc_mangle_type(p["type"])
            for p in params
        )

    def fpc_mangle_unit(self, unit_name):
        return self.normalize_unit_name(unit_name).upper()

    def fpc_mangle_routine(self, name, params=None, unit_name=None):
        params = params or []

        routine = name.upper()
        suffix  = self.fpc_mangle_params(params)

        if unit_name:
            unit = self.fpc_mangle_unit(unit_name)
            return f"_{unit}$$_{routine}{suffix}"

        if self.current_unit:
            unit = self.fpc_mangle_unit(self.current_unit)
            return f"_{unit}$$_{routine}{suffix}"

        return f"_{routine}{suffix}"

    def fpc_mangle_class_method(self, class_name, method_name, params=None, unit_name=None):
        params = params or []

        cls    = class_name.upper()
        method = method_name.upper()
        suffix = self.fpc_mangle_params(params)

        if unit_name:
            unit = self.fpc_mangle_unit(unit_name)
            return f"_{unit}$$_$$_{cls}_$$_{method}{suffix}"

        if self.current_unit:
            unit = self.fpc_mangle_unit(self.current_unit)
            return f"_{unit}$$_$$_{cls}_$$_{method}{suffix}"

        return f"_$$_{cls}_$$_{method}{suffix}"
    
    def emit_class_constructor_call(self, ctx, class_name, method_name):
        class_key = class_name.lower()
        
        if class_key not in self.classes:
            raise CompileError(ctx, "E0004", name=class_name)
        
        cls  = self.classes[class_key]
        args = self.function_call_args(ctx)
        
        actual_types = []
        
        if CDATA.args_target in ["dos", "dos16"]:
            # Argumente auswerten und auf DOS-Stack legen.
            # Reihenfolge: reversed, damit Parameter 1 später bei [bp+4] liegt.
            actual_types = []

            for arg in reversed(args):
                arg_type = self.visit(arg)
                actual_types.insert(0, arg_type)

                if arg_type == "integer":
                    self.backend.writer.emit_push_reg16("ax")

                elif arg_type == "string":
                    # DOS String: DX = Offset, Segment ignorieren/0
                    self.backend.writer.emit_push_reg16("dx")

                elif self.is_pointer_type(
                    arg_type,
                    include_nil=False
                ):
                    # Far Pointer: AX=Offset, DX=Segment
                    self.backend.writer.emit_push_reg16("dx")
                    self.backend.writer.emit_push_reg16("ax")

                else:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=f"unsupported DOS constructor argument type {arg_type}"
                    )

            method, owner_cls = self.find_class_method_recursive(
                ctx,
                cls,
                method_name,
                actual_types
            )

            size = self.class_instance_size(ctx, class_name)

            self.backend.writer.emit_mov_reg16_imm16("ax", size)
            self.backend.writer.emit_heap_alloc()

            fail_label = f"__class_new_fail_{len(self.backend.writer.code)}"
            done_label = f"__class_new_done_{len(self.backend.writer.code)}"

            self.backend.writer.emit_cmp_reg16_imm16("dx", 0)
            self.backend.writer.emit_je(fail_label)

            # Self retten
            self.backend.writer.emit_push_reg16("dx")
            self.backend.writer.emit_push_reg16("ax")

            # Constructor bekommt Self in AX/DX
            self.backend.writer.emit_call_label(method.label)

            # Self zurückholen
            self.backend.writer.emit_pop_reg16("ax")
            self.backend.writer.emit_pop_reg16("dx")

            # Constructor-Parameter vom Stack entfernen
            stack_cleanup = 0
            for typ in actual_types:
                if self.is_pointer_type(
                    typ,
                    include_nil=False
                ):
                    stack_cleanup += 4
                else:
                    stack_cleanup += 2

            if stack_cleanup:
                self.backend.writer.emit_add_sp_imm16(stack_cleanup)

            self.backend.writer.emit_jmp(done_label)

            self.backend.writer.bind_label(fail_label)

            msg_label = "__msg_out_of_memory"
            self.backend.writer.add_dos_string(msg_label, "Out of memory")
            self.backend.writer.emit_mov_dx_label(msg_label)
            self.backend.writer.emit_print_string_current_dx()
            self.backend.writer.emit_print_newline()
            self.backend.writer.emit_exit(1)

            self.backend.writer.bind_label(done_label)

            return class_key
        
        elif CDATA.args_target in ["nt35", "winnt", "win32"]:
            actual_types = []

            # ESI muss unterhalb sämtlicher Konstruktorargumente liegen.
            self.emit_push(
                "esi",
                comment="preserve ESI across constructor expression"
            )

            # Konstruktorargumente von rechts nach links auswerten.
            for arg in reversed(args):
                arg_type = self.visit(
                    arg
                )

                actual_types.insert(
                    0,
                    arg_type
                )

                scalar_type = self.scalar_base_type(
                    arg_type
                )

                if (
                    scalar_type == "integer"
                    or arg_type in (
                        "char",
                        "boolean"
                    )
                ):
                    self.emit_push(
                        "eax",
                        comment="constructor ordinal argument"
                    )

                elif arg_type == "string":
                    self.emit_push(
                        "eax",
                        comment="constructor string argument"
                    )

                elif self.is_pointer_type(
                    arg_type,
                    include_nil=False
                ):
                    self.emit_push(
                        "eax",
                        comment="constructor pointer argument"
                    )

                elif arg_type in self.classes:
                    self.emit_push(
                        "eax",
                        comment="constructor object argument"
                    )

                else:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "unsupported NT32 constructor "
                            f"argument type {arg_type}"
                        )
                    )

            method, owner_cls = self.find_class_method_recursive(
                ctx,
                cls,
                method_name,
                actual_types
            )

            size = max(
                int(cls.size),
                self.pointer_slot_size()
            )

            if CDATA.debug_mode:
                print(
                    "CTOR ALLOC:",
                    class_name,
                    "size=",
                    size
                )

            # --------------------------------------------------------------
            # Objekt reservieren
            # --------------------------------------------------------------
            self.backend.writer.emit_push_imm32(
                size
            )

            self.emit_call(
                "_jit_new_memory"
            )

            self.backend.emit_cleanup_stack(
                4
            )

            # Kein:
            #
            #   lea esi, ctx
            #
            # ESI wird am Ende vom Stack restauriert.

            ok_label = self.new_named_label(
                "class_alloc_ok"
            )

            self.emit_test(
                "eax",
                "eax"
            )

            self.emit_jnz(
                ok_label
            )

            self.emit_call(
                "_jit_error_out_of_memory"
            )

            self.emit_bind_label(
                ok_label
            )

            # --------------------------------------------------------------
            # VMT eintragen
            # --------------------------------------------------------------
            vmt_symbol = (
                self.ensure_class_vmt_reference(
                    ctx,
                    class_name
                )
            )

            self.writer.emit_lea_reg_data_label(
                "edx",
                vmt_symbol
            )

            self.emit_mov_dword_ptr_store(
                "eax",
                0,
                "edx",
                comment=f"{class_name} VMT"
            )

            # --------------------------------------------------------------
            # Ergebnis über den Konstruktoraufruf retten
            # --------------------------------------------------------------
            tmp_symbol = "__ctor_result_tmp"

            if self.coff.find_symbol_index(
                tmp_symbol
            ) is None:
                self.coff.add_data_i32(
                    tmp_symbol,
                    0
                )

            self.coff.emit_mov_data_label_r32(
                tmp_symbol,
                "eax"
            )

            # Aufruflayout:
            #
            # [esp+4]  = Self
            # [esp+8]  = Parameter 1
            # ...
            self.emit_push(
                "eax",
                comment="constructor Self"
            )

            self.emit_class_method_call(
                method,
                comment=(
                    f"{class_name}.{method.name}"
                )
            )

            self.backend.emit_cleanup_stack(
                (len(args) + 1) * 4
            )

            # Neues Objekt wieder nach EAX laden.
            self.coff.emit_mov_reg_from_data_label32(
                "eax",
                tmp_symbol
            )

            # Ursprünglichen ESI-Wert restaurieren.
            self.emit_pop(
                "esi",
                comment="restore ESI after constructor expression"
            )

            return class_key
            
        else:
            # Argumente auswerten und pushen
            for arg in reversed(args):
                arg_type = self.visit(arg)
                actual_types.insert(0, arg_type)
                
                if arg_type == "integer":
                    self.emit_movsxd(REG_RAX, REG_EAX)
                    self.emit_push(REG_RAX, comment='ctor integer arg')
                
                elif arg_type == "string":
                    self.emit_push(REG_RAX, comment='ctor string arg')
                
                elif self.is_pointer_type(
                    arg_type,
                    include_nil=False
                ):
                    self.emit_push(REG_RAX, comment='ctor pointer arg')
                else:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=f"unsupported constructor argument type {arg_type}"
                    )
            method, owner_cls = self.find_class_method_recursive(
                ctx,
                cls,
                method_name,
                actual_types
            )
            
            size = cls.size
        
            self.emit_mov("rcx", size)
            self.emit_mov_imm("rax", "&_jit_new_memory")
            self.emit_call("rax")
            
            param_regs = ["rdx", "r8", "r9"]
            
            # Self zuerst setzen, aber NICHT sofort pushen
            self.emit_mov("rcx", "rax", comment="self") # "a.mov(x86::rcx, x86::rax); // Self")
            
            # Constructor-Parameter aus dem temporären Stack holen
            for index in range(len(args)):
                self.emit_pop(f"{param_regs[index]}", comment="ctor arg {index + 1}")
                #self.emit(f"a.pop(x86::{param_regs[index]});")
            
            # Self über den Call retten
            self.emit_push("rcx", comment="save constructor result object")
            
            self.emit_sub("rsp", 32)
            self.emit_class_method_call(
                method,
                comment=f"{class_name}.{method.name}"
            )
            self.emit_add("rsp", 32)
            self.emit_pop("rax", comment = "constructor result")
            
            return class_key
    
    def resolve_external_library(
        self,
        ctx,
        library_ctx
    ):
        string_token = (
            library_ctx.STRING()
            if hasattr(
                library_ctx,
                "STRING"
            )
            else None
        )

        if string_token is not None:
            return self.pascal_token_string(
                string_token
            )

        ident_token = (
            library_ctx.IDENT()
            if hasattr(
                library_ctx,
                "IDENT"
            )
            else None
        )

        if ident_token is None:
            raise CompileError(
                ctx,
                "E0019",
                text="external library name is missing"
            )

        const_name = ident_token.getText()

        const_info = self.find_const(
            const_name
        )

        if const_info is None:
            raise CompileError(
                ctx,
                "E0001",
                name=const_name
            )

        if const_info.get("type") != "string":
            raise CompileError(
                ctx,
                "E0005",
                got=const_info.get(
                    "type",
                    "<unknown>"
                ),
                expected="string constant"
            )

        dll_name = const_info.get(
            "value"
        )

        if not isinstance(
            dll_name,
            str
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"external library constant "
                    f"{const_name} is not a string"
                )
            )

        return dll_name
    
    def resolve_object_reference(
        self,
        ctx,
        obj_name
    ):
        local_info = self.find_local_var(obj_name)

        if local_info is not None:
            class_type = self.resolve_type(
                local_info["type"]
            )

            if class_type not in self.classes:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=class_type,
                    expected="class"
                )

            return (
                "local",
                local_info,
                class_type
            )

        param_info = self.find_param(
            obj_name
        )

        if param_info is not None:
            class_type = self.resolve_type(
                param_info["type"]
            )

            if class_type not in self.classes:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=class_type,
                    expected="class"
                )

            return (
                "param",
                param_info,
                class_type
            )

        field = self.find_current_class_field(
            obj_name
        )

        if field is not None:
            class_type = self.resolve_type(
                field.type
            )

            if class_type not in self.classes:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=class_type,
                    expected="class"
                )

            return (
                "self_field",
                field,
                class_type
            )

        key = obj_name.lower()

        if key not in self.vars:
            raise CompileError(
                ctx,
                "E0001",
                name=obj_name
            )

        global_info = self.vars[key]
        class_type  = self.resolve_type(global_info["type"])

        if class_type not in self.classes:
            raise CompileError(
                ctx,
                "E0005",
                got=class_type,
                expected="class"
            )

        return (
            "global",
            global_info,
            class_type
        )

    def emit_load_object_reference(
        self,
        ctx,
        obj_name,
        source_kind,
        info,
        class_type
    ):
        if source_kind == "local":
            offset = info["offset"]

            if CDATA.args_target in (
                "nt35",
                "winnt",
                "win32"
            ):
                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    offset,
                    comment=f"local object {obj_name}"
                )
            else:
                self.emit_mov_qword_ptr(
                    "rax",
                    "rbp",
                    offset,
                    comment=f"local object {obj_name}"
                )

            return class_type

        if source_kind == "param":
            result_type = self.emit_load_param(
                ctx,
                obj_name
            )

            if result_type is None:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"could not load object parameter "
                        f"{obj_name}"
                    )
                )

            return class_type

        if source_kind == "self_field":
            if CDATA.args_target in ("nt35", "winnt", "win32"):
                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    -4,
                    comment="Self"
                )

                self.emit_mov_dword_ptr(
                    "eax",
                    "eax",
                    info.offset,
                    comment=f"Self.{obj_name}"
                )

            else:
                self.emit_mov_qword_ptr(
                    "rax",
                    "rbp",
                    -8,
                    comment="Self"
                )

                self.emit_mov_qword_ptr(
                    "rax",
                    "rax",
                    info.offset,
                    comment=f"Self.{obj_name}"
                )

            return class_type

        self.emit_load_object_var(
            ctx,
            obj_name,
            info
        )

        return class_type

    def emit_object_method_call(
        self,
        ctx,
        obj_name,
        method_name,
        actuals=None,
        require_function=False
    ):
        """
        Erzeugt einen Aufruf der Form:

            Obj.Method(...)
            Obj.FunctionMethod

        NT32-ABI:
            Argumente rechts nach links
            danach Self
        """
        if actuals is None:
            actuals = []

        (
            source_kind,
            obj_info,
            class_type
        ) = self.resolve_object_reference(
            ctx,
            obj_name
        )

        actual_types = []

        # ==========================================================
        # NT32 / Win32
        # ==========================================================
        if CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        ):
            arg_bytes = 0

            # cdecl: rechts nach links.
            for arg_index, arg in enumerate(
                reversed(actuals)
            ):
                arg_type = self.resolve_type(
                    self.visit_actual_param_expr(
                        arg
                    )
                )

                actual_types.insert(
                    0,
                    arg_type
                )

                if arg_type in (
                    "integer",
                    "boolean",
                    "char",
                    "string"
                ):
                    self.emit_push(
                        "eax",
                        comment=(
                            f"{obj_name}.{method_name} "
                            f"argument"
                        )
                    )

                    arg_bytes += 4
                    continue

                if self.is_pointer_type(
                    arg_type
                ):
                    self.emit_push(
                        "eax",
                        comment=(
                            f"{obj_name}.{method_name} "
                            f"pointer argument"
                        )
                    )

                    arg_bytes += 4
                    continue

                if arg_type == "double":
                    self.emit_sub(
                        "esp",
                        8,
                        comment=(
                            f"{obj_name}.{method_name} "
                            f"double argument"
                        )
                    )

                    self.emit_movsd_store(
                        "esp",
                        0,
                        "xmm0"
                    )

                    arg_bytes += 8
                    continue

                raise CompileError(
                    ctx,
                    "E0005",
                    got=arg_type,
                    expected=(
                        "integer/boolean/char/string/"
                        "double/pointer/class"
                    )
                )

            method, owner_cls = (
                self.find_class_method_recursive(
                    ctx,
                    class_type,
                    method_name,
                    actual_types
                )
            )

            if (
                require_function
                and method.kind != "function"
            ):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"{owner_cls.name}.{method.name} "
                        f"is not a function"
                    )
                )

            self.emit_load_object_reference(
                ctx,
                obj_name,
                source_kind,
                obj_info,
                class_type
            )

            self.emit_nil_pointer_check(
                obj_name
            )

            # Self liegt absichtlich zuletzt/oben auf dem Stack.
            # emit_class_method_call() benötigt das für VMT-Aufrufe.
            self.emit_push(
                "eax",
                comment=f"{obj_name} Self"
            )

            self.emit_class_method_call(
                method,
                comment=(
                    f"{owner_cls.name}."
                    f"{method.name}"
                )
            )

            self.backend.emit_cleanup_stack(
                arg_bytes + 4
            )

            if (
                self.coff.find_symbol_index(
                    "ctx"
                )
                is not None
            ):
                self.writer.emit_lea_reg_data_label(
                    "esi",
                    "ctx"
                )

            if method.kind == "function":
                return self.resolve_type(
                    method.return_type
                )

            return None

        # ==========================================================
        # Win64 – momentan bis zu drei skalare Methodenparameter.
        # ==========================================================
        if len(actuals) > 3:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "Win64 object method calls currently "
                    "support at most three parameters"
                )
            )

        for arg in reversed(actuals):
            arg_type = self.resolve_type(
                self.visit_actual_param_expr(
                    arg
                )
            )

            actual_types.insert(
                0,
                arg_type
            )

            if (
                arg_type in (
                    "integer",
                    "boolean",
                    "char",
                    "string"
                )
                or self.is_pointer_type(
                    arg_type
                )
            ):
                self.emit_push(
                    "rax",
                    comment=(
                        f"{obj_name}.{method_name} "
                        f"argument"
                    )
                )
                continue

            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "unsupported Win64 object method "
                    f"argument type: {arg_type}"
                )
            )

        method, owner_cls = (
            self.find_class_method_recursive(
                ctx,
                class_type,
                method_name,
                actual_types
            )
        )

        if (
            require_function
            and method.kind != "function"
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"{owner_cls.name}.{method.name} "
                    f"is not a function"
                )
            )

        self.emit_load_object_reference(
            ctx,
            obj_name,
            source_kind,
            obj_info,
            class_type
        )

        self.emit_nil_pointer_check(
            obj_name
        )

        self.emit_mov(
            "rcx",
            "rax",
            comment=f"{obj_name} Self"
        )

        param_regs = [
            "rdx",
            "r8",
            "r9"
        ]

        for index in range(
            len(actuals)
        ):
            self.emit_pop(
                param_regs[index],
                comment=(
                    f"{obj_name}.{method_name} "
                    f"argument {index + 1}"
                )
            )

        self.emit_sub(
            "rsp",
            32,
            comment="method shadow space"
        )

        self.emit_class_method_call(
            method,
            comment=(
                f"{owner_cls.name}."
                f"{method.name}"
            )
        )

        self.emit_add(
            "rsp",
            32,
            comment="remove method shadow space"
        )

        if method.kind == "function":
            return self.resolve_type(
                method.return_type
            )

        return None

    def emit_class_free_call(self, ctx, obj_name):
        (
            source_kind,
            info,
            class_type
        ) = self.resolve_object_reference(
            ctx,
            obj_name
        )

        if class_type not in self.classes:
            raise CompileError(
                ctx,
                "E0005",
                got=class_type,
                expected="class"
            )

        cls = self.classes[class_type]

        # Auch einen geerbten Destruktor finden.
        method, owner_cls = self.find_class_method_recursive(
            ctx,
            class_type,
            "Destroy",
            []
        )

        # ==========================================================
        # DOS16
        # ==========================================================
        if CDATA.args_target in ("dos", "dos16"):
            # Die derzeitige DOS-Implementierung arbeitet mit
            # globalen Far-Pointer-Symbolen.
            if source_kind != "global":
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "DOS16 class Free currently supports "
                        "global object variables only"
                    )
                )

            symbol = info.get("symbol")

            if not symbol:
                symbol = f"_var_{info['name']}"
                info["symbol"] = symbol

            null_label = self.new_named_label(
                "free_nil"
            )

            # AX = Offset
            # DX = Segment
            self.backend.emit_load_far_pointer_var(
                symbol
            )

            # nil-Prüfung entsprechend dem bestehenden
            # Far-Pointer-Modell.
            self.backend.writer.emit_cmp_reg16_imm16(
                "dx",
                0
            )
            self.backend.writer.emit_je(
                null_label
            )

            self.backend.writer.emit_cmp_reg16_imm16(
                "ax",
                0
            )
            self.backend.writer.emit_je(
                null_label
            )

            # Objektzeiger über den Destruktoraufruf retten.
            self.backend.writer.emit_push_reg16(
                "dx"
            )
            self.backend.writer.emit_push_reg16(
                "ax"
            )

            # Self liegt in AX:DX.
            self.backend.writer.emit_call_label(
                method.label
            )

            self.backend.writer.emit_pop_reg16(
                "ax"
            )
            self.backend.writer.emit_pop_reg16(
                "dx"
            )

            # Speicher freigeben und Variable auf nil setzen.
            self.backend.emit_dispose_pointer_far(
                symbol
            )

            self.emit_bind_label(
                null_label
            )

            return None

        # ==========================================================
        # NT32 / Win32
        # ==========================================================
        if CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        ):
            null_label = self.new_named_label(
                "free_nil"
            )

            # Unterstützt:
            #
            #   lokale Objektvariable
            #   Objektparameter
            #   Feld von Self
            #   globale Objektvariable
            #
            # Ergebnis: EAX = Objektzeiger
            self.emit_load_object_reference(
                ctx,
                obj_name,
                source_kind,
                info,
                class_type
            )

            self.emit_test(
                "eax",
                "eax"
            )

            self.emit_jz(
                null_label
            )

            # Objektzeiger unterhalb des Destructor-Self-Arguments
            # auf dem Stack retten.
            self.emit_push(
                "eax",
                comment="save object for dispose"
            )

            self.emit_push(
                "eax",
                comment="Destructor Self"
            )

            # emit_class_method_call() berücksichtigt auch virtuelle
            # Destruktoren und den VMT-Slot.
            self.emit_class_method_call(
                method,
                comment=(
                    f"{owner_cls.name}."
                    f"{method.name}"
                )
            )

            # Destructor-Self entfernen.
            self.backend.emit_cleanup_stack(
                4
            )

            # Geretteten Objektzeiger wiederherstellen.
            self.emit_pop(
                "eax",
                comment="restore object for dispose"
            )

            self.emit_push(
                "eax",
                comment="object for dispose"
            )

            self.emit_call(
                "_jit_dispose_memory"
            )

            self.backend.emit_cleanup_stack(
                4
            )

            # ------------------------------------------------------
            # Ursprüngliche Referenz auf nil setzen
            # ------------------------------------------------------
            if source_kind == "self_field":
                self.emit_xor(
                    "ebx",
                    "ebx"
                )

                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    -4,
                    comment="Self"
                )

                self.emit_mov_dword_ptr_store(
                    "eax",
                    info.offset,
                    "ebx",
                    comment=f"Self.{obj_name} := nil"
                )

            elif source_kind in (
                "local",
                "global"
            ):
                self.emit_xor(
                    "eax",
                    "eax"
                )

                self.emit_store_named_value(
                    ctx,
                    obj_name,
                    source_kind,
                    info,
                    "nil"
                )

            elif source_kind == "param":
                # Bei einem var-Parameter kann auch die Variable
                # des Aufrufers auf nil gesetzt werden.
                if info.get("is_var", False):
                    self.emit_xor(
                        "eax",
                        "eax"
                    )

                    self.emit_store_named_value(
                        ctx,
                        obj_name,
                        source_kind,
                        info,
                        "nil"
                    )

            self.emit_bind_label(
                null_label
            )

            return None

        # ==========================================================
        # Win64
        # ==========================================================
        null_label = self.new_named_label(
            "free_nil"
        )

        # Ergebnis: RAX = Objektzeiger
        self.emit_load_object_reference(
            ctx,
            obj_name,
            source_kind,
            info,
            class_type
        )

        self.emit_test(
            "rax",
            "rax"
        )

        self.emit_jz(
            null_label
        )

        # Objektzeiger über den Destruktoraufruf retten.
        self.emit_push(
            "rax",
            comment="save object for dispose"
        )

        self.emit_mov(
            "rcx",
            "rax",
            comment="Destructor Self"
        )

        self.emit_sub(
            "rsp",
            32,
            comment="destructor shadow space"
        )

        self.emit_class_method_call(
            method,
            comment=(
                f"{owner_cls.name}."
                f"{method.name}"
            )
        )

        self.emit_add(
            "rsp",
            32,
            comment="remove destructor shadow space"
        )

        # RCX = Zeiger für _jit_dispose_memory().
        self.emit_pop(
            "rcx",
            comment="object for dispose"
        )

        self.emit_sub(
            "rsp",
            32,
            comment="dispose shadow space"
        )

        self.emit_mov_imm(
            "rax",
            "&_jit_dispose_memory"
        )

        self.emit_call(
            "rax"
        )

        self.emit_add(
            "rsp",
            32,
            comment="remove dispose shadow space"
        )

        # ----------------------------------------------------------
        # Ursprüngliche Referenz auf nil setzen
        # ----------------------------------------------------------
        if source_kind == "self_field":
            self.emit_xor(
                "r11",
                "r11"
            )

            self.emit_mov_qword_ptr(
                "rax",
                "rbp",
                -8,
                comment="Self"
            )

            self.emit_mov_qword_ptr_store(
                "rax",
                info.offset,
                "r11",
                comment=f"Self.{obj_name} := nil"
            )

        elif source_kind in (
            "local",
            "global"
        ):
            self.emit_xor(
                "rax",
                "rax"
            )

            self.emit_store_named_value(
                ctx,
                obj_name,
                source_kind,
                info,
                "nil"
            )

        elif source_kind == "param":
            if info.get("is_var", False):
                self.emit_xor(
                    "rax",
                    "rax"
                )

                self.emit_store_named_value(
                    ctx,
                    obj_name,
                    source_kind,
                    info,
                    "nil"
                )

        self.emit_bind_label(
            null_label
        )

        return None
    
    def emit_sete(self, reg, comment=""):
        self.backend.emit_sete(reg, comment)

    def emit_setne(self, reg, comment=""):
        self.backend.emit_setne(reg, comment)

    def emit_setl(self, reg, comment=""):
        self.backend.emit_setl(reg, comment)

    def emit_setle(self, reg, comment=""):
        self.backend.emit_setle(reg, comment)

    def emit_setg(self, reg, comment=""):
        self.backend.emit_setg(reg, comment)

    def emit_setge(self, reg, comment=""):
        self.backend.emit_setge(reg, comment)

    def emit_soft_runtime_error(self, message):
        except_label = self.current_except_label()
        label = self.get_or_add_runtime_error_string(message)
        #label = self.add_string_literal(message)

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            if except_label is None:
                self.backend.emit_push_data_label32(label)
                self.emit_call("_jit_error_runtime")
                self.backend.emit_cleanup_stack(4)
                return

            frame = self.try_except_stack[-1]
            esp_symbol = frame.get("esp_symbol")

            if esp_symbol:
                self.writer.emit_mov_reg_from_data_label32("esp", esp_symbol)

            self.writer.emit_lea_reg_data_label("esi", "ctx")
            self.emit_jmp(except_label)
            return

        if except_label is None:
            self.emit_mov_imm("rcx", label)
            self.emit_mov_imm("rax", "&_jit_error_runtime")
            self.emit_call("rax")
            return

        self.emit_mov("rcx", "r12", comment="ctx")
        self.emit_mov_imm("rdx", label)
        self.emit_mov_imm("rax", "&_jit_set_exception")
        self.emit_call("rax")
        self.emit_jmp(except_label)
    
    def emit_nil_pointer_check(self, ptr_name):
        ok_label = self.new_named_label("ptr_not_nil")
        
        if CDATA.args_target in ["dos", "dos16"]:
            # DOS Far Pointer: DX = Segment, AX = Offset
            self.emit_test("rdx", "rdx")
        elif CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_test("eax", "eax")
        else:
            self.emit_test("rax", "rax")

        self.emit_jnz(ok_label)
        self.emit_soft_runtime_error(f"Nil pointer error: {ptr_name}")
        self.emit_bind_label(ok_label)
    
    def emit_builtin_debug_break(self):
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_call("_jit_debug_break")

            # Runtime-Aufrufe dürfen den Generator-Kontext nicht dauerhaft verlieren
            if self.coff.find_symbol_index("ctx") is not None:
                self.writer.emit_lea_reg_data_label("esi", "ctx")

            return None

        self.emit_mov_imm("rax", "&_jit_debug_break")
        self.emit_call("rax")
        return None
    
    def emit_builtin_readln(self, ctx):
        actuals = []

        if ctx.actualParamList():
            actuals = list(ctx.actualParamList().actualParam())

        if len(actuals) != 1:
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected="1")

        ref = self.actual_param_variable_ref(ctx, actuals[0])
        name = ref.IDENT().getText()

        info = self.find_local_var(name)
        is_local = info is not None

        if info is None:
            info = self.var_info(ctx, name)

        typ = self.resolve_type(info["type"])

        if typ == "integer":
            self.emit_mov_imm("rax", "&_jit_read_int")
            self.emit_call("rax")

            if is_local:
                self.emit_store_local_var(ctx, name, "integer")
            else:
                self.emit_store_var(ctx, name, info)

            return None

        if typ == "string":
            self.emit_mov_imm("rax", "&_jit_read_string")
            self.emit_call("rax")

            if is_local:
                self.emit_store_local_var(ctx, name, "string")
            else:
                self.emit_store_var(ctx, name, info)

            return None

        raise CompileError(
            ctx,
            "E0005",
            got=typ,
            expected="integer/string"
        )
    
    def emit_builtin_assigned(self, ctx):
        args = self.function_call_args(ctx)

        if len(args) != 1:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="1"
            )

        expr_type = self.resolve_type(
            self.visit(args[0])
        )

        is_pointer = self.is_pointer_type(
            expr_type,
            include_nil=True
        )

        is_class = (
            isinstance(expr_type, str)
            and expr_type in self.classes
        )

        if not (is_pointer or is_class):
            raise CompileError(
                ctx,
                "E0005",
                got=expr_type,
                expected="pointer/class"
            )

        self.emit_test(REG_RAX, REG_RAX)
        self.emit_setne(REG_AL)
        self.emit_movzx(REG_EAX, REG_AL)

        return "integer"
    
    def emit_builtin_new(self, ctx):
        actuals = []

        if CDATA.args_target in ["dos", "dos16"]:
            args = self.function_call_args(ctx)

            if len(args) != 1:
                raise CompileError(ctx, "E0005", got=str(len(args)), expected="1")

            ptr_name = args[0].getText()
            info = self.var_info(ctx, ptr_name)

            ptr_type = self.resolve_type(info["type"])
            size = self.sizeof_dos_pointed_type(ctx, ptr_type)

            symbol = info.get("symbol")
            if not symbol:
                symbol = f"_var_{info['name']}"
                info["symbol"] = symbol

            self.backend.emit_new_pointer_far(symbol, size)
            return None

        if ctx.actualParamList():
            actuals = list(ctx.actualParamList().actualParam())

        if len(actuals) != 1:
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected="1")

        ref = self.actual_param_variable_ref(ctx, actuals[0])

        name = ref.IDENT().getText()
        info = self.find_local_var(name)
        is_local = info is not None

        if info is None:
            info = self.var_info(ctx, name)

        ptr_type = self.resolve_type(info["type"])

        if not isinstance(ptr_type, str) or not ptr_type.startswith("^"):
            raise CompileError(ctx, "E0005", got=ptr_type, expected="pointer")

        base_type = ptr_type[1:]
        size = self.type_size(ctx, base_type)

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.backend.writer.emit_push_imm32(size)
            self.emit_call("_jit_new_memory")
            self.backend.emit_cleanup_stack(4)
            
            # wichtig: Runtime-Call kann ESI verändert haben
            if self.coff.find_symbol_index("ctx") is not None:
                self.writer.emit_lea_reg_data_label("esi", "ctx")
            
            if is_local:
                self.emit_store_local_var(ctx, name, ptr_type)
            else:
                self.emit_store_var(ctx, name, info)
                
            return None
        else:
            self.emit_mov("rcx", size)
            self.emit_mov_imm("rax", "&_jit_new_memory")
            self.emit_call("rax")

            if is_local:
                self.emit_store_local_var(ctx, name, ptr_type)
            else:
                self.emit_store_var(ctx, name, info)

            return None
    
    def restore_nt32_context_after_runtime_call(self):
        """Lädt ESI nach einem Runtime-Aufruf erneut mit &ctx."""
        if CDATA.args_target not in (
            "nt35",
            "winnt",
            "win32"
        ):
            return

        if self.coff.find_symbol_index("ctx") is not None:
            self.writer.emit_lea_reg_data_label(
                "esi",
                "ctx"
            )

    def emit_builtin_paramcount(self, ctx):
        """
        Pascal:

            ParamCount
            ParamCount()

        Liefert die Anzahl der Argumente ohne ParamStr(0).
        """
        args = self.function_call_args(ctx)

        if args:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="0"
            )

        if CDATA.args_target not in (
            "nt35",
            "winnt",
            "win32"
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "ParamCount is currently implemented "
                    "only for NT32"
                )
            )

        self.emit_call(
            "_jit_param_count"
        )

        self.restore_nt32_context_after_runtime_call()
        return "integer"

    

    def emit_builtin_paramstr(self, ctx):
        """
        Pascal:

            ParamStr(Index)

        ParamStr(0) liefert den Programmnamen. Ein ungültiger Index
        liefert einen leeren dynamischen String.
        """
        args = self.function_call_args(ctx)

        if len(args) != 1:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="1"
            )

        if CDATA.args_target not in (
            "nt35",
            "winnt",
            "win32"
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "ParamStr is currently implemented "
                    "only for NT32"
                )
            )

        index_type = self.visit(
            args[0]
        )

        if index_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=index_type,
                expected="integer"
            )

        # const char* _jit_param_str_cstr(int index)
        self.emit_push(
            "eax",
            comment="ParamStr index"
        )

        self.emit_call(
            "_jit_param_str_cstr"
        )

        self.backend.emit_cleanup_stack(
            4
        )

        # EAX ist ein stabiler C-String. Für Pascal muss daraus ein
        # dynamischer String im vorhandenen Runtime-Format werden.
        self.emit_push(
            "eax",
            comment="ParamStr c-string"
        )

        self.emit_call(
            "_jit_dynstring_from_cstr"
        )

        self.backend.emit_cleanup_stack(
            4
        )

        self.restore_nt32_context_after_runtime_call()
        return "string"

    def emit_builtin_commandline(self, ctx):
        """
        Pascal:

            CommandLine
            CommandLine()

        Liefert die unveränderte vollständige ANSI-Kommandozeile.
        """
        args = self.function_call_args(ctx)

        if args:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="0"
            )

        if CDATA.args_target not in (
            "nt35",
            "winnt",
            "win32"
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "CommandLine is currently implemented "
                    "only for NT32"
                )
            )

        self.emit_call(
            "_jit_command_line_cstr"
        )

        self.emit_push(
            "eax",
            comment="command line c-string"
        )

        self.emit_call(
            "_jit_dynstring_from_cstr"
        )

        self.backend.emit_cleanup_stack(
            4
        )

        self.restore_nt32_context_after_runtime_call()
        return "string"

    def emit_builtin_length(self, ctx):
        actuals = []

        if ctx.argumentList():
            actuals = list(ctx.argumentList().expr())

        if len(actuals) != 1:
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected="1")

        arg_ctx = actuals[0]
        name = arg_ctx.getText()

        # dynamisches Array: Length(A)
        try:
            var_info = self.var_info(ctx, name)
            var_type = var_info["type"]

            if isinstance(var_type, str) and var_type in self.arrays:
                array_info = self.arrays[var_type]

                if getattr(array_info, "is_dynamic", False):
                    self.emit_load_var(name, var_info)      # eax = data pointer

                    done_label = self.new_named_label("dyn_len_done")
                    nil_label  = self.new_named_label("dyn_len_nil")

                    self.emit_test("eax", "eax")
                    self.emit_jz(nil_label)

                    # Header liegt direkt vor data pointer:
                    # [data - 12] = length
                    self.emit_sub("eax", 12)
                    self.emit_mov_reg_dword("eax", "eax")
                    self.emit_jmp(done_label)

                    self.emit_bind_label(nil_label)
                    self.emit_mov("eax", 0)

                    self.emit_bind_label(done_label)
                    return "integer"

        except Exception:
            pass

        # String wie bisher
        expr_type = self.visit(arg_ctx)

        if expr_type != "string":
            raise CompileError(ctx, "E0005", got=expr_type, expected="string")

        self.emit_mov("rcx", "rax")
        self.emit_mov_imm("rax", "&_jit_dynstring_length")
        self.emit_call("rax")

        return "integer"
    
    def emit_builtin_setlength(self, ctx):
        actuals = []

        if ctx.actualParamList():
            actuals = list(ctx.actualParamList().actualParam())

        if len(actuals) != 2:
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected="2")

        target_ctx = actuals[0].expr()
        length_ctx = actuals[1].expr()

        name = target_ctx.getText()

        local_var = self.find_local_var(name)

        if local_var:
            var_type = local_var["type"]
        else:
            var_info = self.var_info(ctx, name)
            var_type = var_info["type"]

        if var_type == "string":
            self.emit_builtin_string_setlength(ctx, name, length_ctx)
            return None

        if isinstance(var_type, str) and var_type in self.arrays:
            array_info = self.arrays[var_type]

            if getattr(array_info, "is_dynamic", False):
                self.emit_builtin_array_setlength(ctx, name, length_ctx)
                return None

        raise CompileError(
            ctx,
            "E0014",
            var_type="SetLength only supports dynamic arrays and strings"
        )
    
    def function_call_args(self, ctx):
        if hasattr(ctx, "actualParamList") and ctx.actualParamList():
            return list(ctx.actualParamList().actualParam())

        if hasattr(ctx, "argumentList") and ctx.argumentList():
            return list(ctx.argumentList().expr())

        if hasattr(ctx, "expr"):
            exprs = ctx.expr()
            if isinstance(exprs, list):
                return list(exprs)
            if exprs:
                return [exprs]

        return []
        
    # ----------------------------------------
    # rcx = Quellstring
    # rdx = Startposition
    # r8  = Anzahl
    # rax = neuer DynString
    # ----------------------------------------
    def emit_builtin_copy(self, ctx):
        args = self.function_call_args(ctx)

        if len(args) != 3:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="3"
            )

        # ---------------------------------------------------------
        # NT32 / Win32
        #
        # Runtime:
        # char* _jit_dynstring_copy(
        #     char* src,
        #     int   start,
        #     int   count
        # );
        #
        # cdecl:
        # push count
        # push start
        # push src
        # call
        # ---------------------------------------------------------
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            source_type = self.visit(args[0])

            if source_type != "string":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=source_type,
                    expected="string"
                )

            self.emit_push("eax", comment="Copy source")

            start_type = self.visit(args[1])

            if start_type != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=start_type,
                    expected="integer"
                )

            self.emit_push("eax", comment="Copy start")

            count_type = self.visit(args[2])

            if count_type != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=count_type,
                    expected="integer"
                )

            self.emit_push("eax", comment="Copy count")

            # Temporäre Werte zurückholen
            self.emit_pop("ecx", comment="Copy count")
            self.emit_pop("edx", comment="Copy start")
            self.emit_pop("eax", comment="Copy source")

            # cdecl: Argumente rechts nach links
            self.emit_push("ecx", comment="count")
            self.emit_push("edx", comment="start")
            self.emit_push("eax", comment="source")

            self.emit_call("_jit_dynstring_copy")
            self.backend.emit_cleanup_stack(12)

            # Runtime-Call darf den Kontext nicht dauerhaft verlieren
            if self.coff.find_symbol_index("ctx") is not None:
                self.writer.emit_lea_reg_data_label("esi", "ctx")

            # EAX = neuer String-Datenpointer
            return "string"

        # ---------------------------------------------------------
        # Win64
        # ---------------------------------------------------------
        source_type = self.visit(args[0])

        if source_type != "string":
            raise CompileError(
                ctx,
                "E0005",
                got=source_type,
                expected="string"
            )

        self.emit_push("rax", comment="Copy source")

        start_type = self.visit(args[1])

        if start_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=start_type,
                expected="integer"
            )

        self.emit_movsxd("rax", "eax")
        self.emit_push("rax", comment="Copy start")

        count_type = self.visit(args[2])

        if count_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=count_type,
                expected="integer"
            )

        self.emit_movsxd("rax", "eax")
        self.emit_push("rax", comment="Copy count")

        # Windows-x64:
        # RCX = source
        # RDX = start
        # R8  = count
        self.emit_pop("r8",  comment="Copy count")
        self.emit_pop("rdx", comment="Copy start")
        self.emit_pop("rcx", comment="Copy source")

        self.emit_sub("rsp", 32)
        self.emit_mov_imm("rax", "&_jit_dynstring_copy")
        self.emit_call("rax")
        self.emit_add("rsp", 32)

        return "string"
    
    # ----------------------------------------
    # rcx = Suchstring
    # rdx = Quellstring
    # eax = Position oder 0
    # ----------------------------------------
    def emit_builtin_pos(self, ctx):
        args = self.function_call_args(ctx)

        if len(args) != 2:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="2"
            )

        # ---------------------------------------------------------
        # NT32 / Win32
        #
        # Runtime:
        # int _jit_dynstring_pos(
        #     char* needle,
        #     char* haystack
        # );
        #
        # cdecl:
        # push haystack
        # push needle
        # ---------------------------------------------------------
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            needle_type = self.visit(args[0])

            if needle_type != "string":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=needle_type,
                    expected="string"
                )

            self.emit_push("eax", comment="Pos needle")

            haystack_type = self.visit(args[1])

            if haystack_type != "string":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=haystack_type,
                    expected="string"
                )

            self.emit_push("eax", comment="Pos haystack")

            # Temporäre Werte holen
            self.emit_pop("edx", comment="Pos haystack")
            self.emit_pop("eax", comment="Pos needle")

            # cdecl: rechts nach links
            self.emit_push("edx", comment="haystack")
            self.emit_push("eax", comment="needle")

            self.emit_call("_jit_dynstring_pos")
            self.backend.emit_cleanup_stack(8)

            if self.coff.find_symbol_index("ctx") is not None:
                self.writer.emit_lea_reg_data_label("esi", "ctx")

            # EAX = Position oder 0
            return "integer"

        # ---------------------------------------------------------
        # Win64
        # ---------------------------------------------------------
        needle_type = self.visit(args[0])

        if needle_type != "string":
            raise CompileError(
                ctx,
                "E0005",
                got=needle_type,
                expected="string"
            )

        self.emit_push("rax", comment="Pos needle")

        haystack_type = self.visit(args[1])

        if haystack_type != "string":
            raise CompileError(
                ctx,
                "E0005",
                got=haystack_type,
                expected="string"
            )

        self.emit_push("rax", comment="Pos haystack")

        self.emit_pop("rdx", comment="Pos haystack")
        self.emit_pop("rcx", comment="Pos needle")

        self.emit_sub("rsp", 32)
        self.emit_mov_imm("rax", "&_jit_dynstring_pos")
        self.emit_call("rax")
        self.emit_add("rsp", 32)

        return "integer"
    
    def emit_builtin_func(self, ctx, func):
        args = self.function_call_args(ctx)

        if len(args) != 2:
            raise CompileError(ctx, "E0005", got=str(len(args)), expected="2")

        t1 = self.visit(args[0])
        if t1 != "string":
            raise CompileError(ctx, "E0005", got=t1, expected="string")

        self.emit_push("rax", comment="string")

        t2 = self.visit(args[1])
        if t2 != "integer":
            raise CompileError(ctx, "E0005", got=t2, expected="integer")

        self.emit_push("rax", comment="length")

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_pop("ebx")      # length
            self.emit_pop("eax")      # string

            # cdecl: rechts nach links pushen
            self.emit_push("ebx")     # len
            self.emit_push("eax")     # string

            self.emit_call(f"_jit_{func}")
            self.backend.emit_cleanup_stack(8)

            # Runtime-Call kann ESI/context zerstören
            self.writer.emit_lea_reg_data_label("esi", "ctx")

        else:
            self.emit_pop("rdx")      # length
            self.emit_pop("rcx")      # string

            self.emit_sub("rsp", 32)
            self.emit_mov_imm("rax", f"&_jit_{func}")
            self.emit_call("rax")
            self.emit_add("rsp", 32)

        return "string"
    
    def emit_builtin_disk_func(self, ctx, runtime_name):
        args = self.function_call_args(ctx)

        if len(args) != 1:
            raise CompileError(ctx, "E0005", got=str(len(args)), expected="1")

        t1 = self.visit(args[0])

        if t1 not in ("char", "string"):
            raise CompileError(ctx, "E0005", got=t1, expected="char/string")

        self.emit_push("rax", comment="drive")

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_pop("eax")

            self.emit_push("eax")
            self.emit_call(runtime_name)
            self.emit("add esp, 4")

        return "string"
    
    def emit_builtin_blake2(self, ctx): return self.emit_builtin_func(ctx, "blake2" )
    def emit_builtin_blake3(self, ctx): return self.emit_builtin_func(ctx, "blake3" )
    def emit_builtin_crc16 (self, ctx): return self.emit_builtin_func(ctx, "crc16"  )
    def emit_builtin_crc32 (self, ctx): return self.emit_builtin_func(ctx, "crc32"  )
    def emit_builtin_crc32c(self, ctx): return self.emit_builtin_func(ctx, "crc32c" )
    def emit_builtin_crc64 (self, ctx): return self.emit_builtin_func(ctx, "crc64"  )
    def emit_builtin_md5   (self, ctx): return self.emit_builtin_func(ctx, "md5"    )
    def emit_builtin_sha1  (self, ctx): return self.emit_builtin_func(ctx, "sha1"   )
    def emit_builtin_sha3  (self, ctx): return self.emit_builtin_func(ctx, "sha3"   )
    def emit_builtin_sha224(self, ctx): return self.emit_builtin_func(ctx, "sha224" )
    def emit_builtin_sha256(self, ctx): return self.emit_builtin_func(ctx, "sha256" )
    def emit_builtin_sha384(self, ctx): return self.emit_builtin_func(ctx, "sha384" )
    def emit_builtin_sha512(self, ctx): return self.emit_builtin_func(ctx, "sha512" )

    def emit_builtin_diskfree       (self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_free")
    def emit_builtin_disktotal      (self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_total")
    def emit_builtin_disklabel      (self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_label")
    def emit_builtin_diskserial     (self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_serial")
    def emit_builtin_diskfilesystem (self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_filesystem")
    def emit_builtin_disktype       (self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_type")
    def emit_builtin_diskshare      (self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_share")
    def emit_builtin_diskused       (self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_used")
    def emit_builtin_diskexists     (self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_exists")
    def emit_builtin_diskready      (self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_ready")
    def emit_builtin_diskiscdrom    (self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_is_cdrom")
    def emit_builtin_diskisnetwork  (self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_is_network")
    def emit_builtin_diskisremovable(self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_is_removable")
    def emit_builtin_diskisfixed    (self, ctx): return self.emit_builtin_disk_func(ctx, "_jit_disk_is_fixed")

    
    def add_double_literal(self, value):
        value_text = str(value)

        safe = (
            value_text
            .replace(".", "_")
            .replace("-", "minus_")
        )

        name = f"dbl_{safe}_{len(self.double_literals)}"
        self.double_literals.append((name, value_text))
        return name
    
    def emit_builtin_dispose(self, ctx):
        actuals = []

        if CDATA.args_target in ("dos", "dos16"):
            args = self.function_call_args(ctx)

            if len(args) != 1:
                raise CompileError(ctx, "E0005", got=str(len(args)), expected="1")

            ptr_name = args[0].getText()
            info = self.var_info(ctx, ptr_name)

            ptr_type = self.resolve_type(info["type"])
            if not isinstance(ptr_type, str) or not ptr_type.startswith("^"):
                raise CompileError(ctx, "E0005", got=ptr_type, expected="pointer")

            symbol = info.get("symbol")
            if not symbol:
                symbol = f"_var_{info['name']}"
                info["symbol"] = symbol

            self.backend.emit_dispose_pointer_far(symbol)
            return None

        if ctx.actualParamList():
            actuals = list(ctx.actualParamList().actualParam())

        if len(actuals) != 1:
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected="1")

        ref = self.actual_param_variable_ref(ctx, actuals[0])

        name = ref.IDENT().getText()

        info = self.find_local_var(name)
        if info is None:
            info = self.var_info(ctx, name)

        ptr_type = self.resolve_type(info["type"])

        if not isinstance(ptr_type, str) or not ptr_type.startswith("^"):
            raise CompileError(ctx, "E0005", got=ptr_type, expected="pointer")

        is_local = self.find_local_var(name) is not None

        if is_local:
            self.emit_load_local_var(ctx, name, info)
        else:
            self.emit_load_var(name, info)

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_push("eax")
            self.emit_call("_jit_dispose_memory")
            self.backend.emit_cleanup_stack(4)

            self.emit_xor("eax", "eax")

            if is_local:
                self.emit_store_local_var(ctx, name, ptr_type)
            else:
                self.emit_store_var(ctx, name, info)

            return None

        else:
            self.emit_mov("rcx", "rax")
            self.emit_mov_imm("rax", "&_jit_dispose_memory")
            self.emit_call("rax")

            self.emit_xor("rax", "rax")

            if is_local:
                self.emit_store_local_var(ctx, name, ptr_type)
            else:
                self.emit_store_var(ctx, name, info)

            return None

    def emit_builtin_array_setlength(self, ctx, name, length_ctx):
        var_info = self.var_info(ctx, name)
        array_info = self.arrays[var_info["type"]]

        # length berechnen
        self.visit(length_ctx)

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            # length sichern
            self.emit_push("eax", comment="length")

            # old array pointer laden -> eax
            self.emit_load_var(name, var_info)

            # old pointer sichern
            self.emit_push("eax", comment="old array pointer")

            # Werte zurückholen
            self.emit_pop("edx")      # old pointer
            self.emit_pop("ecx")      # length

            # cdecl: rechts nach links
            # _jit_dynarray_setlength(old_ptr, length, element_size)
            self.backend.writer.emit_push_imm32(array_info.element_size)
            self.emit_push("ecx", comment="length")
            self.emit_push("edx", comment="old array pointer")

            self.emit_call("_jit_dynarray_setlength")
            self.backend.emit_cleanup_stack(12)

            self.writer.emit_lea_reg_data_label("esi", "ctx")

            self.emit_store_var(ctx, name, var_info)
            return None

        # Win64 wie bisher
        self.emit_movsxd("rdx", "eax")
        self.emit_mov("r8", array_info.element_size)

        self.emit_load_var(name, var_info)
        self.emit_mov("rcx", "rax")

        self.emit_mov_imm("rax", "&_jit_dynarray_setlength")
        self.emit_call("rax")

        self.emit_store_var(ctx, name, var_info)
    
    def emit_multi_array_index_offset(self, ctx, var_name, array_info, index_exprs):
        dims = array_info.dimensions

        if len(index_exprs) != len(dims):
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(index_exprs)),
                expected=str(len(dims))
            )

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_mov("ebx", 0, comment="linear array index")
        else:
            self.emit_xor("ebx", "ebx", comment="linear array index")

        for i, expr in enumerate(index_exprs):
            index_type = self.visit(expr)

            if index_type != "integer":
                raise CompileError(ctx, "E0005", got=index_type, expected="integer")

            dim = dims[i]

            self.emit_array_bounds_check_dimension(
                ctx,
                var_name,
                dim["min"],
                dim["max"]
            )

            if dim["min"] != 0:
                self.emit_sub("eax", dim["min"])

            factor = 1
            for next_dim in dims[i + 1:]:
                factor *= next_dim["max"] - next_dim["min"] + 1

            if factor != 1:
                self.emit_imul("eax", "eax", factor)

            self.emit_add("ebx", "eax")

        #self.emit_mov("eax", "ebx", comment='final linear index')
        self.emit_mov_eax_ebx()

    def get_or_add_runtime_error_string(self, text):
        if not hasattr(self, "runtime_error_strings"):
            self.runtime_error_strings = {}

        if text in self.runtime_error_strings:
            return self.runtime_error_strings[text]

        label = self.add_string_literal(text)
        self.runtime_error_strings[text] = label
        return label

    def emit_array_bounds_check_dimension(self, ctx, var_name, min_value, max_value):
        ok_label    = self.new_named_label("array_bounds_ok")
        fail_label  = self.new_named_label("array_bounds_fail")
        is_nt32 = CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        )

        if is_nt32:
            # EBX is the multidimensional linear-index accumulator, so
            # preserve the current dimension index on the stack.
            self.emit_push(
                "eax",
                comment="save dimension index"
            )

            self.emit_cmp("eax", min_value)
            self.emit_jl(fail_label)
            self.emit_cmp("eax", max_value)
            self.emit_jg(fail_label)
            self.emit_jmp(ok_label)

            self.emit_bind_label(fail_label)
            msg = (
                f"Array bounds error: {var_name} index out of range "
                f"allowed range {min_value}..{max_value}"
            )

            self.emit_soft_runtime_error(msg)

            self.emit_bind_label(ok_label)
            self.emit_pop(
                "eax",
                comment="restore dimension index"
            )
            return

        array_label = self.add_string_literal(
            var_name
        )

        self.emit_mov(
            "r10d",
            "eax",
            comment="save dimension index"
        )
        self.emit_cmp("eax", min_value)
        self.emit_jl(fail_label)
        self.emit_cmp("eax", max_value)
        self.emit_jg(fail_label)
        self.emit_jmp(ok_label)

        self.emit_bind_label(fail_label)
        self.emit_mov_imm("rcx", array_label)
        self.emit_mov("edx", "r10d")
        self.emit_mov("r8d", min_value)
        self.emit_mov("r9d", max_value)
        self.emit_mov_imm("rax", "&_jit_error_array_bounds")
        self.emit_call("rax")

        self.emit_bind_label(ok_label)
        self.emit_mov(
            "eax",
            "r10d",
            comment="restore dimension index"
        )

    def emit_array_bounds_check_for_dimension(self, dim):
        min_value = dim["min"]
        max_value = dim["max"]

        self.emit_push("rax")

        self.emit_cmp("eax", min_value)
        self.emit_jl("error_array_bounds")

        self.emit_cmp("eax", max_value)
        self.emit_jg("error_array_bounds")

        self.emit_pop("rax")
    
    def emit_address_of_routine(self, ctx, name):
        routine = self.find_function(name)

        if routine is None:
            routine = self.find_procedure(
                name
            )

        if routine is None:
            return None

        target = (
            routine.get("label")
            or routine.get("mangled")
            or routine.get("symbol")
        )

        if not target:
            raise CompileError(
                ctx,
                "E0019",
                text=f"routine {name} has no addressable symbol"
            )

        if CDATA.args_target not in (
            "nt35",
            "winnt",
            "win32"
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "routine addresses are currently implemented "
                    "only for NT32"
                )
            )

        # Despite its historical name this writer operation emits an
        # absolute IMAGE_REL_I386_DIR32 relocation. The referenced COFF
        # symbol may therefore live in .text as well as in .data.
        self.writer.emit_lea_reg_data_label(
            "eax",
            target
        )

        return "pointer"

    def addressable_name_type(
        self,
        ctx,
        name
    ):
        info = self.find_local_var(name)

        if info is not None:
            return self.resolve_type(
                info["type"]
            )

        field = self.find_current_class_field(name)

        if field is not None:
            return self.resolve_type(
                field.type
            )

        info = self.var_info(
            ctx,
            name
        )

        return self.resolve_type(
            info["type"]
        )
    
    def emit_address_of_var(self, ctx, name):
        is_nt32 = CDATA.args_target in ["nt35", "winnt", "win32"]

        REG_A   = "eax" if is_nt32 else "rax"
        REG_BP  = "ebp" if is_nt32 else "rbp"

        local_var = self.find_local_var(name)

        if local_var:
            typ    = self.resolve_type(local_var["type"])
            offset = local_var["offset"]

            if typ == "integer":
                self.emit_lea_dword(REG_A, REG_BP, offset, comment=f"@{name}")
                return "^integer"

            if typ == "double":
                self.emit_lea_qword(REG_A, REG_BP, offset, comment=f"@{name}")
                return "^double"

            if typ == "string":
                self.emit_lea_qword(REG_A, REG_BP, offset, comment=f"@{name}")
                return "^string"

            if self.is_pointer_type(
                typ,
                include_nil=False
            ):
                self.emit_lea_qword(REG_A, REG_BP, offset, comment=f"@{name}")
                return "^" + typ

            if isinstance(typ, str) and typ in self.records:
                self.emit_lea_byte(REG_A, REG_BP, offset, comment=f"@{name}")
                return "^" + typ

            if isinstance(typ, str) and typ in self.arrays:
                self.emit_lea_byte(REG_A, REG_BP, offset, comment=f"@{name}")
                return "^" + typ

            raise CompileError(ctx, "E0014", var_type=typ)

        # Feld des impliziten Self-Objekts:
        #
        #     RegisterClassA(FWinClass)
        #
        self_field = self.find_current_class_field(
            name
        )

        if self_field is not None:
            target = self.emit_self_member_address(
                ctx,
                [name]
            )

            if target is None:
                raise CompileError(
                    ctx,
                    "E0001",
                    name=name
                )

            field, field_type = target

            if field.offset:
                self.emit_add(
                    REG_A,
                    field.offset,
                    comment=f"@Self.{name}"
                )

            return "^" + field_type

        key = name.lower()

        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=name)

        info = self.vars[key]
        typ  = self.resolve_type(info["type"])
        slot = info["slot"]

        # -------------------------------------------------
        # NT32: globale Variablen liegen direkt als COFF-
        # Daten-Symbol vor: _var_name.
        # @name bedeutet: Adresse dieses Symbols laden.
        # -------------------------------------------------
        if is_nt32:
            symbol = info.get("symbol")

            if not symbol:
                symbol = f"_var_{info['name']}"
                info["symbol"] = symbol

            if self.coff.find_symbol_index(symbol) is None:
                if typ == "integer":
                    self.coff.add_data_i32(symbol, 0)

                elif typ == "double":
                    self.coff.add_data_double(symbol, 0.0)

                elif typ == "string":
                    self.coff.add_data_i32(symbol, 0)

                elif self.is_pointer_type(
                    typ,
                    include_nil=False
                ):
                    self.coff.add_data_i32(symbol, 0)

                elif isinstance(typ, str) and typ in self.records:
                    self.coff.add_data_zeros(symbol, self.records[typ].size, alignment=4)

                elif isinstance(typ, str) and typ in self.arrays:
                    self.coff.add_data_zeros(symbol, self.arrays[typ].size, alignment=4)

                else:
                    raise CompileError(ctx, "E0014", var_type=typ)

            self.writer.emit_lea_reg_data_label("eax", symbol)

            if typ == "integer":
                return "^integer"

            if typ == "double":
                return "^double"

            if typ == "string":
                return "^string"

            if self.is_pointer_type(
                typ,
                include_nil=False
            ):
                return "^" + typ

            if isinstance(typ, str) and typ in self.records:
                return "^" + typ

            if isinstance(typ, str) and typ in self.arrays:
                return "^" + typ

            raise CompileError(ctx, "E0014", var_type=typ)

        # -------------------------------------------------
        # Win64: bisheriger JitContext-Pfad über r12
        # -------------------------------------------------
        if typ == "integer":
            self.emit_mov_qword("rax", "r12", "int_vars")
            self.emit_add("rax", slot * self.pointer_slot_size(), comment=f"@{name}")
            return "^integer"

        if typ == "double":
            self.emit_mov_qword("rax", "r12", "double_vars")
            self.emit_add("rax", slot * self.pointer_slot_size(), comment=f"@{name}")
            return "^double"

        if typ == "string":
            self.emit_mov_qword("rax", "r12", "string_vars")
            self.emit_add("rax", slot * self.pointer_slot_size(), comment=f"@{name}")
            return "^string"

        if self.is_pointer_type(
            typ,
            include_nil=False
        ):
            self.emit_mov_qword("rax", "r12", "pointr_vars")
            self.emit_add("rax", slot * self.pointer_slot_size(), comment=f"@{name}")
            return "^" + typ

        if isinstance(typ, str) and typ in self.records:
            self.emit_mov_qword("rax", "r12", "record_vars")
            self.emit_add("rax", slot, comment=f"@{name}")
            return "^" + typ

        if isinstance(typ, str) and typ in self.arrays:
            self.emit_mov_qword("rax", "r12", "arrays_vars")
            self.emit_add("rax", slot, comment=f"@{name}")
            return "^" + typ

        raise CompileError(ctx, "E0014", var_type=typ)
    
    def emit_array_bounds_check(self, ctx, var_name, array_info):
        ok_label    = self.new_named_label("array_bounds_ok")
        fail_label  = self.new_named_label("array_bounds_fail")
        array_label = self.add_string_literal(var_name)

        # Originalindex in EBX sichern
        self.emit_mov("ebx", "eax", comment = "save array index")

        self.emit_cmp("eax", array_info.index_min)
        self.emit_jl(fail_label)

        self.emit_cmp("eax", array_info.index_max)
        self.emit_jg(fail_label)

        self.emit_jmp(ok_label)

        self.emit_bind_label(fail_label)
        self.emit_mov_imm("rcx", array_label)
        self.emit_mov("edx", "ebx")
        self.emit_mov("r8d", array_info.index_min)
        self.emit_mov("r9d", array_info.index_max)
        self.emit_mov_imm("rax", "&_jit_error_array_bounds")
        self.emit_call("rax")

        self.emit_bind_label(ok_label)

        # Index wiederherstellen
        self.emit_mov("eax", "ebx", comment='restore array index')
    
    def emit_load_self_field(self, ctx, name):
        if self.find_current_class_field(name) is None:
            return None

        return self.emit_load_self_member_path(
            ctx,
            [name]
        )
    
    def emit_load_object_var(self, ctx, name, info):
        if self.find_local_var(name) is not None:
            return self.emit_load_local_var(
                ctx,
                name,
                info
            )

        if self.find_param(name) is not None:
            return self.emit_load_param(
                ctx,
                name
            )
        
        if CDATA.args_target in ["dos", "dos16"]:
            symbol = info.get("symbol")

            if not symbol:
                symbol = f"_var_{info['name']}"
                info["symbol"] = symbol

            self.backend.emit_load_far_pointer_var(symbol)
            return info["type"]
        
        # NT32 / Win32: Objektpointer ist 32-bit!
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            symbol = info.get("symbol")

            if not symbol:
                symbol = f"_var_{info['name']}"
                info["symbol"] = symbol

            self.coff.emit_mov_reg_from_data_label32("eax", symbol)
            return info["type"]

        if hasattr(self, "coff") and "symbol" in info:
            self.coff.emit_mov_r64_data_label("rax", info["symbol"])
            return info["type"]

        slot = info["slot"]
        self.emit_mov_qword("rax", "r12", "pointr_vars")
        self.emit_mov_qword_ptr("rax","rax",
            slot * self.pointer_slot_size(),
            comment=f"object {name}"
        )

        return info["type"]
    
    def emit_load_string_char(self, ctx, name, index_exprs):
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]

        if len(index_exprs) != 1:
            raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            # Index berechnen -> eax
            index_type = self.visit(index_exprs[0])
            if index_type != "integer":
                raise CompileError(ctx, "E0005", got=index_type, expected="integer")

            # ecx = Pascal index
            self.emit_mov("ecx", "eax", comment="pascal string index")

            # Header laden -> eax
            var_info = self.var_info(ctx, name)
            self.emit_load_var(name, var_info)

            # edx = DynStringHeader*
            self.emit_mov("edx", "eax", comment="string header")

            ok_not_nil = self.new_named_label("string_not_nil")
            fail_label = self.new_named_label("string_index_fail")
            ok_label   = self.new_named_label("string_index_ok")

            self.emit_test("edx", "edx")
            self.emit_jnz(ok_not_nil)
            self.emit_call("_jit_error_string_range")

            self.emit_bind_label(ok_not_nil)

            # eax = header->length
            self.emit_mov_dword_ptr("eax", "edx", 8, comment="string length")

            # index < 1 ?
            self.emit_cmp("ecx", 1)
            self.emit_jl(fail_label)

            # index > length ?
            self.emit_cmp("ecx", "eax")
            self.emit_jg(fail_label)

            self.emit_jmp(ok_label)

            self.emit_bind_label(fail_label)
            self.emit_call("_jit_error_string_range")

            self.emit_bind_label(ok_label)

            # ecx = index - 1
            self.emit_sub("ecx", 1)

            # edi = header->data
            self.emit_mov_dword_ptr("edi", "edx", 12, comment="string data")

            # edi = data + index - 1
            self.emit_add("edi", "ecx", comment="string char address")

            # eax = byte ptr [edi]
            self.backend.writer.emit_movzx_r32_byte_ptr("eax", "edi", 0)

            return "char"

        else:
            self.emit_movsxd("r11", "r10d")
            self.emit_add("r11", "rax")
            self.emit_movzx("eax", "byte_ptr(r11)")
        
        return "char"
    
    def resolve_class_property(self, class_name, prop_name):
        cls = self.classes[class_name.lower()]
        props = getattr(cls, "properties", {})
        return props.get(prop_name.lower())
    
    def emit_load_class_property(self, ctx, parts):
        obj_name  = parts[0]
        prop_name = parts[1]

        (
            source_kind,
            var_info,
            class_type
        ) = self.resolve_named_storage(
            ctx,
            obj_name
        )

        if class_type not in self.classes:
            return None

        cls = self.classes[class_type]
        prop = self.resolve_class_property(class_type, prop_name)

        if prop is None:
            return None

        if prop.read_name is None:
            raise CompileError(ctx, "E0006")

        read_name = prop.read_name
        read_key  = read_name.lower()

        # property Value read FValue;
        if read_key in cls.fields:
            return self.emit_load_class_field(ctx, [obj_name, read_name])

        # property Value read GetValue;
        method, owner_cls = self.find_class_method_recursive(
            ctx,
            class_type,
            read_name,
            []
        )

        self.emit_load_object_var(ctx, obj_name, var_info)
        self.emit_nil_pointer_check(obj_name)

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_push("eax", comment="Self")
            self.emit_class_method_call(
                method,
                comment=f"{owner_cls.name}.{method.name}"
            )
            self.backend.emit_cleanup_stack(4)
            self.writer.emit_lea_reg_data_label("esi", "ctx")
            return self.resolve_type(method.return_type)

        self.emit_mov("rcx", "rax", comment="Self")
        self.emit_sub("rsp", 32)
        self.emit_call_lbl(method.label)
        self.emit_add("rsp", 32)

        return self.resolve_type(method.return_type)
    
    def emit_load_class_field(self, ctx, parts):
        field, field_type = self.emit_class_member_address(
            ctx,
            parts
        )

        path = ".".join(parts)
        range_info = self.subrange_info(
            field_type
        )
        is_nt32 = CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        )
        address_reg = "eax" if is_nt32 else "rax"

        if (
            range_info is not None
            and self.scalar_base_type(field_type) == "integer"
        ):
            if range_info.size == 1:
                self.backend.writer.emit_movzx_r32_byte_ptr(
                    "eax",
                    address_reg,
                    field.offset
                )
            elif range_info.size == 2:
                self.backend.writer.emit_movzx_r32_word_ptr(
                    "eax",
                    address_reg,
                    field.offset
                )
            elif range_info.size == 4:
                self.emit_mov_dword_ptr(
                    "eax",
                    address_reg,
                    field.offset,
                    comment=path
                )
            else:
                raise CompileError(
                    ctx,
                    "E0014",
                    var_type=field_type
                )

            return field_type

        if field_type in ("integer", "boolean"):
            self.emit_mov_dword_ptr(
                "eax",
                address_reg,
                field.offset,
                comment=path
            )

            if field_type == "boolean":
                self.emit_and("eax", 1)

            return field_type

        if field_type == "char":
            self.backend.writer.emit_movzx_r32_byte_ptr(
                "eax",
                address_reg,
                field.offset
            )
            return "char"

        if field_type == "double":
            self.emit_movsd_load(
                "xmm0",
                address_reg,
                field.offset,
                comment=path
            )
            return "double"

        if (
            field_type == "string"
            or self.is_class_type(field_type)
            or self.is_pointer_type(
                field_type,
                include_nil=False
            )
        ):
            if is_nt32:
                self.emit_mov_dword_ptr(
                    "eax",
                    "eax",
                    field.offset,
                    comment=path
                )
            else:
                self.emit_mov_qword_ptr(
                    "rax",
                    "rax",
                    field.offset,
                    comment=path
                )

            return field_type

        raise CompileError(
            ctx,
            "E0014",
            var_type=field_type
        )
    
    def emit_load_const(self, ctx, name):
        c = self.find_const(name)

        if not c:
            raise CompileError(ctx, "E0001", name=name)

        typ = c["type"]
        val = c["value"]

        if typ == "boolean":
            self.emit_mov("eax", val)
            return "boolean"
            
        if typ == "integer":
            self.emit_mov("eax", val)
            return "integer"

        if typ == "double":
            return self.emit_load_double_literal(val)

        if typ == "string":
            label = self.add_string_literal(val)
            self.emit_mov_imm("rax", label)
            return "string"

        raise CompileError(ctx, "E0014", var_type=typ)
    
    def emit_load_double_literal(self, value):
        value_text = str(value)
        label = self.add_double_literal(value_text)

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            if self.coff.find_symbol_index(label) is None:
                self.coff.add_data_double(label, float(value_text))
            self.backend.writer.emit_movsd_xmm0_data_label32(label)
            return "double"

        self.emit_mov_imm("rax", double_to_bits(float(value_text)))
        self.emit_movq("xmm0", "rax")
        return "double"
    
    def context_contains_caret(self, ctx):
        if ctx is None:
            return False

        symbol = getattr(ctx, "symbol", None)

        if symbol is not None:
            token_text = getattr(symbol, "text", None)
            token_type = getattr(symbol, "type", None)
            caret_type = getattr(PascalParser, "CARET", None)

            if token_text == "^":
                return True

            if caret_type is not None and token_type == caret_type:
                return True

            return False

        for child in getattr(ctx, "children", None) or []:
            if self.context_contains_caret(child):
                return True

        return False
        
    def context_contains_dot(self, ctx):
        if ctx is None:
            return False

        symbol = getattr(ctx, "symbol", None)

        if symbol is not None:
            token_text = getattr(symbol, "text", None)
            token_type = getattr(symbol, "type", None)
            caret_type = getattr(PascalParser, "DOT", None)

            if token_text == ".":
                return True

            if caret_type is not None and token_type == caret_type:
                return True

            return False

        for child in getattr(ctx, "children", None) or []:
            if self.context_contains_dot(child):
                return True

        return False
    
    def emit_load_string_var_to_rax(self, ctx, name):
        var_info = self.var_info(ctx, name)
        slot = var_info["slot"]

        self.emit_mov_qword("rax", "r12", "string_vars")
        self.emit_mov_qword_ptr("rax", "rax", slot * self.pointer_slot_size())
    
    def emit_load_pointer_var_to_rax(
        self,
        ctx,
        name,
        info=None
    ):
        if info is None:
            (
                source_kind,
                info,
                pointer_type
            ) = self.resolve_named_storage(
                ctx,
                name
            )
        else:
            pointer_type = self.resolve_type(
                info["type"]
            )

            if self.find_local_var(name) is not None:
                source_kind = "local"
            elif self.find_param(name) is not None:
                source_kind = "param"
            else:
                source_kind = "global"

        if not self.is_pointer_type(
            pointer_type,
            include_nil=False
        ):
            raise CompileError(
                ctx,
                "E0005",
                got=pointer_type,
                expected="pointer"
            )

        return self.emit_load_named_value(
            ctx,
            name,
            source_kind,
            info
        )

    def emit_load_pointer_deref(self, ctx, name):
        info = self.find_local_var(name)
        source_kind = None

        if info is not None:
            source_kind = "local"

        if info is None:
            info = self.find_param(name)
            if info is not None:
                source_kind = "param"

        if info is None:
            info = self.vars.get(name.lower())
            if info is not None:
                source_kind = "global"

        if info is None:
            raise CompileError(ctx, "E0001", name=name)

        ptr_type = self.resolve_type(info["type"])

        if not self.is_pointer_type(ptr_type, include_nil=False):
            raise CompileError(
                ctx,
                "E0005",
                got=ptr_type,
                expected="pointer"
            )

        if source_kind == "local":
            self.emit_load_local_var(ctx, name, info)
        elif source_kind == "param":
            self.emit_load_param(ctx, name)
        else:
            self.emit_load_var(name, info)

        self.emit_nil_pointer_check(name)

        if ptr_type in ("pchar", "pansichar"):
            base_type = "char"
        elif ptr_type == "pointer":
            base_type = "pointer"
        else:
            base_type = self.resolve_type(ptr_type[1:])

        range_info = self.subrange_info(base_type)
        is_nt32 = CDATA.args_target in ("nt35", "winnt", "win32")
        address_reg = "eax" if is_nt32 else "rax"

        if range_info is not None and range_info.base_type == "integer":
            if range_info.size == 1:
                self.backend.writer.emit_movzx_r32_byte_ptr(
                    "eax",
                    address_reg,
                    0
                )
            else:
                self.emit_mov_dword_ptr(
                    "eax",
                    address_reg,
                    0,
                    comment=f"{name}^"
                )

                if not range_info.signed and range_info.size == 2:
                    self.emit_and("eax", 0xFFFF)

            return "integer"

        if base_type == "integer":
            self.emit_mov_dword_ptr("eax", address_reg, 0, comment=f"{name}^")
            return "integer"

        if base_type == "boolean":
            self.emit_mov_dword_ptr("eax", address_reg, 0, comment=f"{name}^")
            self.emit_and("eax", 1)
            return "boolean"

        if base_type == "char":
            self.backend.writer.emit_movzx_r32_byte_ptr(
                "eax",
                address_reg,
                0
            )
            return "char"

        if base_type == "double":
            self.emit_movsd_load("xmm0", address_reg, 0, comment=f"{name}^")
            return "double"

        if base_type == "string":
            if is_nt32:
                self.emit_mov_dword_ptr("eax", "eax", 0, comment=f"{name}^")
            else:
                self.emit_mov_qword_ptr("rax", "rax", 0, comment=f"{name}^")
            return "string"

        if self.is_pointer_type(base_type, include_nil=False):
            if is_nt32:
                self.emit_mov_dword_ptr("eax", "eax", 0, comment=f"{name}^")
            else:
                self.emit_mov_qword_ptr("rax", "rax", 0, comment=f"{name}^")
            return base_type

        if isinstance(base_type, str) and base_type in self.records:
            return base_type

        raise CompileError(ctx, "E0014", var_type=base_type)

    def emit_load_param(self, ctx, name):
        param = self.find_param(name)

        if param is None:
            raise CompileError(ctx, "E0001", name=name)

        declared_type = str(
            param.get("declared_type", param["type"])
        ).strip().lower()

        typ = self.resolve_type(param["type"])
        offset = param.get("stack_offset")

        if offset is None:
            raise CompileError(
                ctx,
                "E0019",
                text=f"parameter {name} has no stack offset"
            )

        is_var = bool(param.get("is_var", False))
        range_info = self.subrange_info(typ)
        scalar_type = self.scalar_base_type(typ)

        if CDATA.args_target in ("nt35", "winnt", "win32"):
            if is_var:
                self.emit_mov_dword_ptr(
                    "ebx",
                    "ebp",
                    offset,
                    comment=f"var parameter address {name}"
                )

                if range_info is not None and scalar_type == "integer":
                    self.emit_mov_dword_ptr(
                        "eax",
                        "ebx",
                        0,
                        comment=f"var subrange parameter {name}: {typ}"
                    )

                    if not range_info.signed:
                        if range_info.size == 1:
                            self.emit_and("eax", 0xFF)
                        elif range_info.size == 2:
                            self.emit_and("eax", 0xFFFF)

                    return "integer"

                if typ == "integer":
                    self.emit_mov_dword_ptr("eax", "ebx", 0)
                    return "integer"

                if typ == "boolean":
                    self.emit_mov_dword_ptr("eax", "ebx", 0)
                    self.emit_and("eax", 1)
                    return "boolean"

                if typ == "char":
                    self.backend.writer.emit_movzx_r32_byte_ptr(
                        "eax",
                        "ebx",
                        0
                    )
                    return "char"

                if typ == "string":
                    self.emit_mov_dword_ptr("eax", "ebx", 0)
                    return "string"

                if typ == "double":
                    self.emit_movsd_load("xmm0", "ebx", 0)
                    return "double"

                if self.is_pointer_type(typ, include_nil=False):
                    self.emit_mov_dword_ptr("eax", "ebx", 0)
                    return typ

                if isinstance(typ, str) and typ in self.classes:
                    self.emit_mov_dword_ptr("eax", "ebx", 0)
                    return typ

                raise CompileError(ctx, "E0014", var_type=typ)

            if range_info is not None and scalar_type == "integer":
                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    offset,
                    comment=f"subrange parameter {name}: {typ}"
                )

                if not range_info.signed:
                    if range_info.size == 1:
                        self.emit_and("eax", 0xFF)
                    elif range_info.size == 2:
                        self.emit_and("eax", 0xFFFF)

                return "integer"

            if typ == "integer":
                self.emit_mov_dword_ptr("eax", "ebp", offset)
                return "integer"

            if typ == "boolean":
                self.emit_mov_dword_ptr("eax", "ebp", offset)
                self.emit_and("eax", 1)
                return "boolean"

            if typ == "char":
                self.emit_mov_dword_ptr("eax", "ebp", offset)
                self.emit_and("eax", 0xFF)
                return "char"

            if typ == "string":
                self.emit_mov_dword_ptr("eax", "ebp", offset)
                return "string"

            if typ == "double":
                self.emit_movsd_load("xmm0", "ebp", offset)
                return "double"

            if self.is_pointer_type(typ, include_nil=False):
                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    offset,
                    comment=f"pointer parameter {name}"
                )
                return typ

            if isinstance(typ, str) and typ in self.classes:
                self.emit_mov_dword_ptr("eax", "ebp", offset)
                return typ

            raise CompileError(ctx, "E0014", var_type=typ)

        if CDATA.args_target in ("dos", "dos16"):
            if is_var:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "DOS VAR parameter loading is not implemented "
                        f"for {declared_type}"
                    )
                )

            if typ == "integer" or (
                range_info is not None
                and scalar_type == "integer"
            ):
                self.backend.writer.emit_mov_reg16_mem16_base_disp(
                    "ax",
                    "bp",
                    offset
                )
                return "integer"

            if self.is_pointer_type(typ, include_nil=False):
                self.backend.writer.emit_mov_reg16_mem16_base_disp(
                    "ax",
                    "bp",
                    offset
                )
                self.backend.writer.emit_mov_reg16_mem16_base_disp(
                    "dx",
                    "bp",
                    offset + 2
                )
                return typ

            raise CompileError(ctx, "E0014", var_type=typ)

        if is_var:
            self.emit_mov_qword_ptr(
                "r11",
                "rbp",
                offset,
                comment=f"var parameter address {name}"
            )

            if typ == "integer" or (
                range_info is not None
                and scalar_type == "integer"
            ):
                self.emit_mov_dword_ptr("eax", "r11", 0)
                return "integer"

            if typ == "boolean":
                self.emit_mov_dword_ptr("eax", "r11", 0)
                self.emit_and("eax", 1)
                return "boolean"

            if typ == "char":
                self.emit_mov_dword_ptr("eax", "r11", 0)
                self.emit_and("eax", 0xFF)
                return "char"

            if typ == "string":
                self.emit_mov_qword_ptr("rax", "r11", 0)
                return "string"

            if typ == "double":
                self.emit_movsd_load("xmm0", "r11", 0)
                return "double"

            if self.is_pointer_type(typ, include_nil=False):
                self.emit_mov_qword_ptr("rax", "r11", 0)
                return typ

            if isinstance(typ, str) and typ in self.classes:
                self.emit_mov_qword_ptr("rax", "r11", 0)
                return typ

            raise CompileError(ctx, "E0014", var_type=typ)

        if typ == "integer" or (
            range_info is not None
            and scalar_type == "integer"
        ):
            self.emit_mov_dword_ptr("eax", "rbp", offset)
            return "integer"

        if typ == "boolean":
            self.emit_mov_dword_ptr("eax", "rbp", offset)
            self.emit_and("eax", 1)
            return "boolean"

        if typ == "char":
            self.emit_mov_dword_ptr("eax", "rbp", offset)
            self.emit_and("eax", 0xFF)
            return "char"

        if typ == "string":
            self.emit_mov_qword_ptr("rax", "rbp", offset)
            return "string"

        if typ == "double":
            self.emit_movsd_load("xmm0", "rbp", offset)
            return "double"

        if self.is_pointer_type(typ, include_nil=False):
            self.emit_mov_qword_ptr("rax", "rbp", offset)
            return typ

        if isinstance(typ, str) and typ in self.classes:
            self.emit_mov_qword_ptr("rax", "rbp", offset)
            return typ

        raise CompileError(ctx, "E0014", var_type=typ)

    def emit_load_record_field(self, ctx, parts):
        (
            source_kind,
            info,
            field_offset,
            field
        ) = self.resolve_record_path(
            ctx,
            parts
        )

        path = ".".join(parts)
        is_nt32 = CDATA.args_target in ["nt35", "winnt", "win32"]
        field_type = self.resolve_type(
            field.type
        )
        address_reg = (
            "edx"
            if is_nt32
            else "r11"
        )

        self.emit_record_base_address(
            ctx,
            parts[0],
            source_kind,
            info,
            address_reg
        )

        if field_type in ("integer", "boolean"):
            self.emit_mov_dword_ptr(
                "eax",
                address_reg,
                field_offset,
                comment=path
            )

            if field_type == "boolean":
                self.emit_and("eax", 1)
                return "boolean"

            return "integer"

        if field_type == "char":
            self.backend.writer.emit_movzx_r32_byte_ptr(
                "eax",
                address_reg,
                field_offset
            )
            return "char"

        if field_type == "double":
            self.emit_movsd_load(
                "xmm0",
                address_reg,
                field_offset,
                comment=path
            )
            return "double"

        if (
            field_type == "string"
            or field_type in self.classes
            or self.is_pointer_type(
                field_type,
                include_nil=False
            )
        ):
            if is_nt32:
                self.emit_mov_dword_ptr(
                    "eax",
                    address_reg,
                    field_offset,
                    comment=path
                )
            else:
                self.emit_mov_qword_ptr(
                    "rax",
                    address_reg,
                    field_offset,
                    comment=path
                )

            return field_type

        if field_type in self.records:
            if is_nt32:
                self.emit_mov(
                    "eax",
                    address_reg,
                    comment=path + " address"
                )
            else:
                self.emit_mov(
                    "rax",
                    address_reg,
                    comment=path + " address"
                )

            if field_offset:
                self.emit_add(
                    "eax" if is_nt32 else "rax",
                    field_offset,
                    comment=path
                )

            return field_type

        raise CompileError(
            ctx,
            "E0014",
            var_type=field_type
        )
    
    def emit_load_pointer_record_field(
        self,
        ctx,
        parts
    ):
        if not parts or len(parts) < 2:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "pointer record field access "
                    "requires pointer and field"
                )
            )

        ptr_name = parts[0]
        ptr_key = ptr_name.lower()

        # ----------------------------------------------------------
        # Pointerquelle bestimmen:
        #
        #   lokale Variable
        #   formaler Parameter
        #   globale Variable
        # ----------------------------------------------------------
        ptr_info = self.find_local_var(
            ptr_name
        )

        source_kind = None

        if ptr_info is not None:
            source_kind = "local"

        if ptr_info is None:
            ptr_info = self.find_param(
                ptr_name
            )

            if ptr_info is not None:
                source_kind = "param"

        if ptr_info is None:
            ptr_info = self.vars.get(
                ptr_key
            )

            if ptr_info is not None:
                source_kind = "global"

        if ptr_info is None:
            raise CompileError(
                ctx,
                "E0001",
                name=ptr_name
            )

        # ----------------------------------------------------------
        # Pointertyp prüfen
        # ----------------------------------------------------------
        ptr_type = self.resolve_type(
            ptr_info["type"]
        )

        if (
            not isinstance(ptr_type, str)
            or not ptr_type.startswith("^")
        ):
            raise CompileError(
                ctx,
                "E0005",
                got=ptr_type,
                expected="pointer"
            )

        current_type = self.resolve_type(
            ptr_type[1:]
        )

        if current_type not in self.records:
            raise CompileError(
                ctx,
                "E0005",
                got=current_type,
                expected="record"
            )

        is_nt32 = (
            CDATA.args_target
            in (
                "nt35",
                "winnt",
                "win32"
            )
        )

        address_reg = (
            "eax"
            if is_nt32
            else "rax"
        )

        # ----------------------------------------------------------
        # Pointerwert laden
        # ----------------------------------------------------------
        if source_kind == "local":
            self.emit_load_local_var(
                ctx,
                ptr_name,
                ptr_info
            )

        elif source_kind == "param":
            self.emit_load_param(
                ctx,
                ptr_name
            )

        elif source_kind == "global":
            self.emit_load_var(
                ptr_name,
                ptr_info
            )

        else:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"unknown pointer source: "
                    f"{ptr_name}"
                )
            )

        self.emit_nil_pointer_check(
            ptr_name
        )

        field_names = parts[1:]

        # ----------------------------------------------------------
        # Feldpfad abarbeiten
        # ----------------------------------------------------------
        for index, field_name in enumerate(
            field_names
        ):
            if current_type not in self.records:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=current_type,
                    expected="record"
                )

            record = self.records[
                current_type
            ]

            field_key = field_name.lower()

            if field_key not in record.fields:
                raise CompileError(
                    ctx,
                    "E0001",
                    name=".".join(parts)
                )

            field = record.fields[
                field_key
            ]

            field_type = self.resolve_type(
                field.type
            )

            is_last = (
                index
                == len(field_names) - 1
            )

            path = ".".join(
                parts[:index + 2]
            )

            # ======================================================
            # Letztes Feld: tatsächlichen Wert laden
            # ======================================================
            if is_last:
                # --------------------------------------------------
                # Integer-Subrange (Byte, Word, DWord, ...)
                # --------------------------------------------------
                range_info = self.subrange_info(field_type)

                if range_info is not None and range_info.base_type == "integer":
                    field_size = int(getattr(field, "size", range_info.size))

                    if field_size == 1:
                        self.backend.writer.emit_movzx_r32_byte_ptr(
                            "eax",
                            address_reg,
                            field.offset
                        )
                    else:
                        self.emit_mov_dword_ptr(
                            "eax",
                            address_reg,
                            field.offset,
                            comment=path
                        )

                        if not range_info.signed and field_size == 2:
                            self.emit_and("eax", 0xFFFF)

                    return "integer"

                # --------------------------------------------------
                # Integer
                # --------------------------------------------------
                if field_type == "integer":
                    self.emit_mov_dword_ptr(
                        "eax",
                        address_reg,
                        field.offset,
                        comment=path
                    )

                    return "integer"

                # --------------------------------------------------
                # Boolean
                # --------------------------------------------------
                if field_type == "boolean":
                    self.emit_mov_dword_ptr(
                        "eax",
                        address_reg,
                        field.offset,
                        comment=path
                    )

                    self.emit_and(
                        "eax",
                        1
                    )

                    return "boolean"

                # --------------------------------------------------
                # Char / AnsiChar
                # --------------------------------------------------
                if field_type == "char":
                    self.backend.writer.emit_movzx_r32_byte_ptr(
                        "eax",
                        address_reg,
                        field.offset
                    )

                    return "char"

                # --------------------------------------------------
                # Double
                # --------------------------------------------------
                if field_type == "double":
                    self.emit_movsd_load(
                        "xmm0",
                        address_reg,
                        field.offset,
                        comment=path
                    )

                    return "double"

                # --------------------------------------------------
                # String
                # --------------------------------------------------
                if field_type == "string":
                    if is_nt32:
                        self.emit_mov_dword_ptr(
                            "eax",
                            "eax",
                            field.offset,
                            comment=path
                        )
                    else:
                        self.emit_mov_qword_ptr(
                            "rax",
                            "rax",
                            field.offset,
                            comment=path
                        )

                    return "string"

                # --------------------------------------------------
                # Pointerfeld
                # --------------------------------------------------
                if self.is_pointer_type(
                    field_type,
                    include_nil=False
                ):
                    if is_nt32:
                        self.emit_mov_dword_ptr(
                            "eax",
                            "eax",
                            field.offset,
                            comment=path
                        )
                    else:
                        self.emit_mov_qword_ptr(
                            "rax",
                            "rax",
                            field.offset,
                            comment=path
                        )

                    return field_type

                # --------------------------------------------------
                # Klassenfeld: ebenfalls Pointer
                # --------------------------------------------------
                if (
                    isinstance(field_type, str)
                    and field_type in self.classes
                ):
                    if is_nt32:
                        self.emit_mov_dword_ptr(
                            "eax",
                            "eax",
                            field.offset,
                            comment=path
                        )
                    else:
                        self.emit_mov_qword_ptr(
                            "rax",
                            "rax",
                            field.offset,
                            comment=path
                        )

                    return field_type

                # --------------------------------------------------
                # Eingebetteter Record:
                # Adresse dieses Records zurückgeben
                # --------------------------------------------------
                if (
                    isinstance(field_type, str)
                    and field_type in self.records
                ):
                    if field.offset != 0:
                        self.emit_add(
                            address_reg,
                            field.offset,
                            comment=path
                        )

                    return field_type

                raise CompileError(
                    ctx,
                    "E0014",
                    var_type=field_type
                )

            # ======================================================
            # Noch nicht letztes Feld:
            # Adresse für den nächsten Zugriff berechnen
            # ======================================================

            # ------------------------------------------------------
            # Eingebetteter Record:
            #
            #   P^.Inner.Value
            #
            # P zeigt auf Outer.
            # Inner liegt direkt innerhalb von Outer.
            # ------------------------------------------------------
            if field_type in self.records:
                if field.offset != 0:
                    self.emit_add(
                        address_reg,
                        field.offset,
                        comment=path
                    )

                current_type = field_type
                continue

            # ------------------------------------------------------
            # Pointer auf nächsten Record:
            #
            #   P^.Next^.Value
            #
            # Das Pointerfeld muss geladen und geprüft werden.
            # ------------------------------------------------------
            if self.is_pointer_type(
                field_type,
                include_nil=False
            ):
                pointed_type = self.resolve_type(
                    field_type[1:]
                )

                if pointed_type not in self.records:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=pointed_type,
                        expected="record"
                    )

                if is_nt32:
                    self.emit_mov_dword_ptr(
                        "eax",
                        "eax",
                        field.offset,
                        comment=path
                    )
                else:
                    self.emit_mov_qword_ptr(
                        "rax",
                        "rax",
                        field.offset,
                        comment=path
                    )

                self.emit_nil_pointer_check(
                    path
                )

                current_type = pointed_type
                continue

            raise CompileError(
                ctx,
                "E0005",
                got=field_type,
                expected="record/pointer"
            )

        raise CompileError(
            ctx,
            "E0019",
            text=(
                "pointer record field path "
                "could not be resolved"
            )
        )
    
    def emit_load_local_var(self, ctx, name, info):
        var = self.find_local_var(name)

        if not var:
            raise CompileError(ctx, "E0012", name=name)

        typ    = self.resolve_type(var["type"])
        offset = var["offset"]

        if typ in ("integer", "boolean"):
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_mov_dword_ptr("eax", "ebp", offset, comment=f"local {name}")
            else:
                self.emit_mov_dword_ptr("eax", "rbp", offset, comment=f"local {name}")

            if typ == "boolean":
                self.emit_and("eax", 1)

            return typ

        if typ == "char":
            self.backend.writer.emit_movzx_r32_byte_ptr(
                "eax",
                "ebp" if CDATA.args_target in ("nt35", "winnt", "win32") else "rbp",
                offset
            )
            return "char"

        if typ == "string":
            if CDATA.args_target in ["dos", "dos16"]:
                # DX = Offset, DS bleibt unverändert
                self.backend.writer.emit_mov_reg16_mem16_base_disp("dx", "bp", offset)
                return "string"

            if CDATA.args_target in ("nt35", "winnt", "win32"):
                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    offset,
                    comment=f"local string {name}"
                )
            else:
                self.emit_mov_qword_ptr(
                    "rax",
                    "rbp",
                    offset,
                    comment=f"local string {name}"
                )

            return "string"

        if self.is_pointer_type(typ, include_nil=False):
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_mov_dword_ptr("eax", "ebp", offset, comment=f"local pointer {name}")
            else:
                self.emit_mov_qword_ptr("rax", "rbp", offset, comment=f"local pointer {name}")

            return typ

        # Lokale Klassenvariable enthält einen Objektzeiger.
        if self.is_class_type(typ):
            if CDATA.args_target in ("nt35", "winnt", "win32"):
                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    offset,
                    comment=f"local object {name}"
                )
            else:
                self.emit_mov_qword_ptr(
                    "rax",
                    "rbp",
                    offset,
                    comment=f"local object {name}"
                )
            return typ

        raise CompileError(ctx, "E0011", typ=typ)

    def emit_nt32_string_index_checked_data_ptr(self, ctx, name, index_exprs):
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]

        if len(index_exprs) != 1:
            raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

        range_error = self.new_named_label("string_range_ok")

        # Index berechnen -> eax
        index_type = self.visit(index_exprs[0])

        if index_type != "integer":
            raise CompileError(ctx, "E0005", got=index_type, expected="integer")

        # ecx = Pascal-Index
        self.emit_mov("ecx", "eax")

        # String-Header laden -> eax
        var_info = self.var_info(ctx, name)
        self.emit_load_var(name, var_info)

        # edx = DynStringHeader*
        self.emit_mov("edx", "eax")

        # nil?
        self.emit_cmp("edx", 0)
        self.emit_je("_jit_error_string_range")

        # Länge laden: [header + 8]
        self.emit_mov_dword_ptr("eax", "edx", 8, comment="string length")

        # index < 1 ?
        self.emit_cmp("ecx", 1)
        self.emit_jl("_jit_error_string_range")

        # index > length ?
        self.emit_cmp("ecx", "eax")
        self.emit_jg("_jit_error_string_range")

        # ecx = index - 1
        self.emit_sub("ecx", 1)

        # data pointer laden: [header + 12]
        self.emit_mov_dword_ptr("edx", "edx", 12, comment="string data")

        # edx = &data[index - 1]
        self.emit_add("edx", "ecx")

        return "edx"

    def emit_builtin_string_setlength(self, ctx, name, length_ctx):
        var_info = self.var_info(ctx, name)

        # new_length berechnen -> eax
        length_type = self.visit(length_ctx)

        if length_type != "integer":
            raise CompileError(ctx, "E0005", got=length_type, expected="integer")

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            # new_length sichern
            self.emit_push("eax", comment="new length")

            # old string pointer laden -> eax
            self.emit_load_var(name, var_info)

            # old_data sichern
            self.emit_push("eax", comment="old string pointer")

            # Werte zurückholen
            self.emit_pop("edx")      # old_data
            self.emit_pop("ecx")      # new_length

            # cdecl: _jit_dynstring_setlength(old_data, new_length)
            # rechts nach links:
            self.emit_push("ecx", comment="new length")
            self.emit_push("edx", comment="old string pointer")

            self.emit_call("_jit_dynstring_setlength")
            self.backend.emit_cleanup_stack(8)

            # Runtime-Call kann ESI/ctx zerstören
            self.writer.emit_lea_reg_data_label("esi", "ctx")

            # eax = neuer string pointer
            self.emit_store_var(ctx, name, var_info)
            return None

        # Win64
        self.emit_movsxd("rdx", "eax")      # new_length

        self.emit_load_var(name, var_info)  # old_data -> rax
        self.emit_mov("rcx", "rax")         # old_data

        self.emit_mov_imm("rax", "&_jit_dynstring_setlength")
        self.emit_call("rax")

        self.emit_store_var(ctx, name, var_info)
        return None
    
    def resolve_self_member_path(
        self,
        ctx,
        parts
    ):
        """
        Resolve an implicit Self member path.

        Examples:

            FAppForm
            FAppForm.WndClass
            FAppForm.WndClass.style

        Class-valued fields contain an object pointer. Record-valued fields
        are stored inline in their containing class or record.
        """
        if self.current_class is None or not parts:
            return None

        current_type = self.current_class
        result = []

        for index, member_name in enumerate(parts):
            if current_type in self.classes:
                fields = self.classes[current_type].fields

            elif current_type in self.records:
                fields = self.records[current_type].fields

            else:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=current_type,
                    expected="class/record"
                )

            member_key = member_name.lower()

            if member_key not in fields:
                # A missing first member means that this is not an
                # implicit Self path. Missing nested members are real
                # compiler errors and must not fall through to var_info().
                if index == 0:
                    return None

                raise CompileError(
                    ctx,
                    "E0001",
                    name=".".join(parts[:index + 1])
                )

            field = fields[member_key]
            field_type = self.resolve_type(field.type)

            result.append((
                field,
                field_type
            ))

            if index + 1 < len(parts):
                if (
                    field_type not in self.classes
                    and field_type not in self.records
                ):
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=field_type,
                        expected="class/record"
                    )

                current_type = field_type

        return result


    def emit_self_member_address(
        self,
        ctx,
        parts
    ):
        """
        Load the address of the container of the last member into EAX/RAX.

        The returned field offset is relative to that address.
        """
        resolved = self.resolve_self_member_path(
            ctx,
            parts
        )

        if resolved is None:
            return None

        is_nt32 = (
            CDATA.args_target
            in (
                "nt35",
                "winnt",
                "win32"
            )
        )

        if is_nt32:
            self.emit_mov_dword_ptr(
                "eax",
                "ebp",
                -4,
                comment="Self"
            )
        else:
            self.emit_mov_qword_ptr(
                "rax",
                "rbp",
                -8,
                comment="Self"
            )

        # Every member except the last one selects the container of the
        # following member.
        for index, (field, field_type) in enumerate(resolved[:-1]):
            path = ".".join(parts[:index + 1])

            if field_type in self.classes:
                # A class field contains a pointer to another object.
                if is_nt32:
                    self.emit_mov_dword_ptr(
                        "eax",
                        "eax",
                        field.offset,
                        comment=path
                    )
                else:
                    self.emit_mov_qword_ptr(
                        "rax",
                        "rax",
                        field.offset,
                        comment=path
                    )

                self.emit_nil_pointer_check(
                    path
                )
                continue

            if field_type in self.records:
                # Records are embedded inline.
                if field.offset:
                    self.emit_add(
                        "eax" if is_nt32 else "rax",
                        field.offset,
                        comment=path
                    )
                continue

            raise CompileError(
                ctx,
                "E0005",
                got=field_type,
                expected="class/record"
            )

        final_field, final_type = resolved[-1]

        return (
            final_field,
            final_type
        )


    def emit_load_self_member_path(
        self,
        ctx,
        parts
    ):
        target = self.emit_self_member_address(
            ctx,
            parts
        )

        if target is None:
            return None

        field, field_type = target
        path = "Self." + ".".join(parts)

        is_nt32 = (
            CDATA.args_target
            in (
                "nt35",
                "winnt",
                "win32"
            )
        )

        address_reg = (
            "eax"
            if is_nt32
            else "rax"
        )

        range_info = self.subrange_info(
            field_type
        )

        if (
            range_info is not None
            and self.scalar_base_type(field_type) == "integer"
        ):
            if range_info.size == 1:
                self.backend.writer.emit_movzx_r32_byte_ptr(
                    "eax",
                    address_reg,
                    field.offset
                )

            elif range_info.size == 2:
                self.backend.writer.emit_movzx_r32_word_ptr(
                    "eax",
                    address_reg,
                    field.offset
                )

            elif range_info.size == 4:
                self.emit_mov_dword_ptr(
                    "eax",
                    address_reg,
                    field.offset,
                    comment=path
                )

            else:
                raise CompileError(
                    ctx,
                    "E0013",
                    var_type=field_type
                )

            return field_type

        if field_type in (
            "integer",
            "boolean"
        ):
            self.emit_mov_dword_ptr(
                "eax",
                address_reg,
                field.offset,
                comment=path
            )

            if field_type == "boolean":
                self.emit_and(
                    "eax",
                    1
                )

            return field_type

        if field_type == "char":
            self.backend.writer.emit_movzx_r32_byte_ptr(
                "eax",
                address_reg,
                field.offset
            )
            return "char"

        if field_type == "double":
            self.emit_movsd_load(
                "xmm0",
                address_reg,
                field.offset,
                comment=path
            )
            return "double"

        if (
            field_type == "string"
            or field_type in self.classes
            or self.is_pointer_type(
                field_type,
                include_nil=False
            )
        ):
            if is_nt32:
                self.emit_mov_dword_ptr(
                    "eax",
                    "eax",
                    field.offset,
                    comment=path
                )
            else:
                self.emit_mov_qword_ptr(
                    "rax",
                    "rax",
                    field.offset,
                    comment=path
                )

            return field_type

        if field_type in self.records:
            # The value of an inline record is represented by its address.
            if field.offset:
                self.emit_add(
                    address_reg,
                    field.offset,
                    comment=path
                )

            return field_type

        raise CompileError(
            ctx,
            "E0013",
            var_type=field_type
        )


    def emit_store_self_member_path(
        self,
        ctx,
        parts,
        expr_type
    ):
        resolved = self.resolve_self_member_path(
            ctx,
            parts
        )

        if resolved is None:
            return False

        field, field_type = resolved[-1]
        value_type = self.resolve_type(
            expr_type
        )

        range_info = self.subrange_info(
            field_type
        )

        if (
            range_info is not None
            and self.scalar_base_type(field_type) == "integer"
        ):
            if self.scalar_base_type(value_type) != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected=field_type
                )

            self.emit_subrange_check(
                ctx,
                field_type,
                value_reg="eax"
            )

        elif field_type == "double" and value_type == "integer":
            self.emit_cvtsi2sd(
                "xmm0",
                "eax"
            )
            value_type = "double"

        elif field_type == "boolean":
            if value_type not in (
                "boolean",
                "integer"
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected="boolean"
                )

            self.emit_and(
                "eax",
                1
            )
            value_type = "boolean"

        elif field_type in self.classes:
            if not self.class_assignment_compatible(
                value_type,
                field_type
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected=field_type
                )

        elif self.is_pointer_type(
            field_type,
            include_nil=False
        ):
            if not self.pointer_assignment_compatible(
                value_type,
                field_type
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected=field_type
                )

        elif field_type != value_type:
            raise CompileError(
                ctx,
                "E0005",
                got=value_type,
                expected=field_type
            )

        is_nt32 = (
            CDATA.args_target
            in (
                "nt35",
                "winnt",
                "win32"
            )
        )

        stack_reg = (
            "esp"
            if is_nt32
            else "rsp"
        )

        # Preserve the right-hand value before EAX/RAX is reused for the
        # Self/member address.
        if field_type == "double":
            self.emit_sub(
                stack_reg,
                8,
                comment="save nested Self field double"
            )

            self.emit_movsd_store(
                stack_reg,
                0,
                "xmm0"
            )
        else:
            self.emit_push(
                "eax" if is_nt32 else "rax",
                comment="save nested Self field value"
            )

        target = self.emit_self_member_address(
            ctx,
            parts
        )

        if target is None:
            return False

        field, field_type = target
        address_reg = (
            "eax"
            if is_nt32
            else "rax"
        )

        path = "Self." + ".".join(parts)

        if field_type == "double":
            self.emit_movsd_load(
                "xmm0",
                stack_reg,
                0
            )

            self.emit_add(
                stack_reg,
                8,
                comment="restore nested Self field double"
            )

            self.emit_movsd_store(
                address_reg,
                field.offset,
                "xmm0",
                comment=path + " :="
            )
            return True

        value_reg = (
            "ebx"
            if is_nt32
            else "r11"
        )

        self.emit_pop(
            value_reg,
            comment="restore nested Self field value"
        )

        range_info = self.subrange_info(
            field_type
        )

        if (
            range_info is not None
            and self.scalar_base_type(field_type) == "integer"
        ):
            if range_info.size == 1:
                self.emit_mov_byte_ptr_store(
                    address_reg,
                    field.offset,
                    "bl" if is_nt32 else "r11b",
                    comment=path + " :="
                )

            elif range_info.size == 2:
                self.emit_mov_word_ptr_store(
                    address_reg,
                    field.offset,
                    "bx" if is_nt32 else "r11w",
                    comment=path + " :="
                )

            elif range_info.size == 4:
                self.emit_mov_dword_ptr_store(
                    address_reg,
                    field.offset,
                    "ebx" if is_nt32 else "r11d",
                    comment=path + " :="
                )

            else:
                raise CompileError(
                    ctx,
                    "E0013",
                    var_type=field_type
                )

            return True

        if field_type in (
            "integer",
            "boolean"
        ):
            self.emit_mov_dword_ptr_store(
                address_reg,
                field.offset,
                "ebx" if is_nt32 else "r11d",
                comment=path + " :="
            )
            return True

        if field_type == "char":
            self.emit_mov_byte_ptr_store(
                address_reg,
                field.offset,
                "bl" if is_nt32 else "r11b",
                comment=path + " :="
            )
            return True

        if (
            field_type == "string"
            or field_type in self.classes
            or self.is_pointer_type(
                field_type,
                include_nil=False
            )
        ):
            if is_nt32:
                self.emit_mov_dword_ptr_store(
                    "eax",
                    field.offset,
                    "ebx",
                    comment=path + " :="
                )
            else:
                self.emit_mov_qword_ptr_store(
                    "rax",
                    field.offset,
                    "r11",
                    comment=path + " :="
                )

            return True

        raise CompileError(
            ctx,
            "E0013",
            var_type=field_type
        )


    def emit_store_self_field(self, ctx, name, expr_type):
        field = self.find_current_class_field(name)

        if field is None:
            return False
        
        field_type = self.resolve_type ( field.type )
        value_type = self.resolve_type ( expr_type  )
        range_info = self.subrange_info( field_type )

        # --------------------------------------------------------------
        # Byte, Word, SmallInt, Cardinal, DWord und andere Subranges
        # --------------------------------------------------------------
        if (range_info is not None
            and self.scalar_base_type(field_type) == "integer"):
            if self.scalar_base_type(value_type) != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected=field_type
                )

            # EAX enthält den zu speichernden Wert.
            self.emit_subrange_check(
                ctx,
                field_type,
                value_reg="eax"
            )

            # Wert sichern, weil EAX gleich mit Self überschrieben wird.
            self.emit_mov(
                "ebx",
                "eax",
                comment=f"save Self.{name} value"
            )

            if CDATA.args_target in ("nt35", "winnt", "win32"):
                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    -4,
                    comment="Self"
                )

                if range_info.size == 1:
                    self.emit_mov_byte_ptr_store(
                        "eax",
                        field.offset,
                        "bl",
                        comment=f"Self.{name} :="
                    )

                elif range_info.size == 2:
                    self.emit_mov_word_ptr_store(
                        "eax",
                        field.offset,
                        "bx",
                        comment=f"Self.{name} :="
                    )

                elif range_info.size == 4:
                    self.emit_mov_dword_ptr_store(
                        "eax",
                        field.offset,
                        "ebx",
                        comment=f"Self.{name} :="
                    )

                else:
                    raise CompileError(
                        ctx,
                        "E0013",
                        var_type=field_type
                    )

                return True

            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "class subrange field assignment "
                    f"is not implemented for target "
                    f"{CDATA.args_target}"
                )
            )

        if field_type == "double" and value_type == "integer":
            self.emit_cvtsi2sd(
                "xmm0",
                "eax"
            )
            value_type = "double"
            expr_type = "double"

        if field_type == "boolean":
            if value_type not in ("boolean", "integer"):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected="boolean"
                )

            self.emit_and(
                "eax",
                1,
                comment=f"normalize Self.{name}"
            )
            value_type = "boolean"
            expr_type = "boolean"
        
        # --------------------------------------------------------------
        # Klassenfelder sind Objektzeiger
        # --------------------------------------------------------------
        if field_type in self.classes:
            if not self.class_assignment_compatible(
                value_type,
                field_type
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected=field_type
                )

            if CDATA.args_target in ("nt35", "winnt", "win32"):
                # EAX = zu speichernder Objektzeiger
                self.emit_mov(
                    "ebx",
                    "eax",
                    comment=f"save Self.{name} object"
                )

                # EAX = aktuelles Self
                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    -4,
                    comment="Self"
                )

                # [Self + Feldoffset] = Objektzeiger
                self.emit_mov_dword_ptr_store(
                    "eax",
                    field.offset,
                    "ebx",
                    comment=f"Self.{name} :="
                )

            else:
                self.emit_mov(
                    "r11",
                    "rax",
                    comment=f"save Self.{name} object"
                )

                self.emit_mov_qword_ptr(
                    "rax",
                    "rbp",
                    -8,
                    comment="Self"
                )

                self.emit_mov_qword_ptr_store(
                    "rax",
                    field.offset,
                    "r11",
                    comment=f"Self.{name} :="
                )

            return True

        # Pointer- und Handle-Felder enthalten wie Klassenfelder eine
        # zeigergroße Referenz.
        if self.is_pointer_type(
            field_type,
            include_nil=False
        ):
            if not self.pointer_assignment_compatible(
                value_type,
                field_type
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected=field_type
                )

            if CDATA.args_target in ("nt35", "winnt", "win32"):
                self.emit_mov(
                    "ebx",
                    "eax",
                    comment=f"save Self.{name} pointer"
                )
                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    -4,
                    comment="Self"
                )
                self.emit_mov_dword_ptr_store(
                    "eax",
                    field.offset,
                    "ebx",
                    comment=f"Self.{name} :="
                )
            else:
                self.emit_mov(
                    "r11",
                    "rax",
                    comment=f"save Self.{name} pointer"
                )
                self.emit_mov_qword_ptr(
                    "rax",
                    "rbp",
                    -8,
                    comment="Self"
                )
                self.emit_mov_qword_ptr_store(
                    "rax",
                    field.offset,
                    "r11",
                    comment=f"Self.{name} :="
                )

            return True

        if field_type != value_type:
            raise CompileError(
                ctx,
                "E0005",
                got      = value_type,
                expected = field_type
            )

        if field_type in ("integer", "boolean"):
            self.emit_mov("ebx", "eax")
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_mov_dword_ptr("eax", "ebp", -4, comment="Self")
                self.emit_mov_dword_ptr_store(
                    "eax",
                    field.offset,
                    "ebx",
                    comment=f"Self.{name} :="
                )
            else:
                self.emit_mov_qword_ptr("rax", "rbp", -8, comment="Self")
                self.emit_mov_dword_ptr_store(
                    "rax",
                    field.offset,
                    "ebx",
                    comment=f"Self.{name} :="
                )

            return True

        if field_type == "char":
            self.emit_mov(
                "ebx",
                "eax",
                comment=f"save Self.{name} char"
            )

            if CDATA.args_target in ("nt35", "winnt", "win32"):
                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    -4,
                    comment="Self"
                )
                self.emit_mov_byte_ptr_store(
                    "eax",
                    field.offset,
                    "bl",
                    comment=f"Self.{name} :="
                )
            else:
                self.emit_mov_qword_ptr(
                    "rax",
                    "rbp",
                    -8,
                    comment="Self"
                )
                self.emit_mov_byte_ptr_store(
                    "rax",
                    field.offset,
                    "bl",
                    comment=f"Self.{name} :="
                )

            return True

        if field_type == "double":
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_sub(
                    "esp",
                    8,
                    comment=f"save Self.{name} double"
                )

                self.emit_movsd_store(
                    "esp",
                    0,
                    "xmm0"
                )

                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    -4,
                    comment="Self"
                )

                self.emit_movsd_load(
                    "xmm0",
                    "esp",
                    0
                )

                self.emit_add(
                    "esp",
                    8,
                    comment=f"restore Self.{name} double"
                )

                self.emit_movsd_store(
                    "eax",
                    field.offset,
                    "xmm0",
                    comment=f"Self.{name} :="
                )
            else:
                self.emit_sub(
                    "rsp",
                    8,
                    comment=f"save Self.{name} double"
                )

                self.emit_movsd_store(
                    "rsp",
                    0,
                    "xmm0"
                )

                self.emit_mov_qword_ptr(
                    "rax",
                    "rbp",
                    -8,
                    comment="Self"
                )

                self.emit_movsd_load(
                    "xmm0",
                    "rsp",
                    0
                )

                self.emit_add(
                    "rsp",
                    8,
                    comment=f"restore Self.{name} double"
                )

                self.emit_movsd_store(
                    "rax",
                    field.offset,
                    "xmm0",
                    comment=f"Self.{name} :="
                )

            return True

        if field_type == "string":
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                # EAX enthält den dynamischen String-Datenpointer.
                self.emit_push(
                    "eax",
                    comment=f"save Self.{name} string"
                )

                # In NT32-Klassenmethoden liegt Self bei [ebp-4].
                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    -4,
                    comment="Self"
                )

                self.emit_pop(
                    "ebx",
                    comment=f"restore Self.{name} string"
                )

                self.emit_mov_dword_ptr_store(
                    "eax",
                    field.offset,
                    "ebx",
                    comment=f"Self.{name} :="
                )
            else:
                self.emit_push(
                    "rax",
                    comment=f"save Self.{name} string"
                )

                self.emit_mov_qword_ptr(
                    "rax",
                    "rbp",
                    -8,
                    comment="Self"
                )

                self.emit_pop(
                    "r11",
                    comment=f"restore Self.{name} string"
                )

                self.emit_mov_qword_ptr_store(
                    "rax",
                    field.offset,
                    "r11",
                    comment=f"Self.{name} :="
                )

            return True

        raise CompileError(ctx, "E0013", var_type=field.type)
    
    def emit_store_object_var(self, ctx, name, info):
        var_info = info
        
        if CDATA.args_target in ["dos", "dos16"]:
            symbol = var_info.get("symbol")

            if not symbol:
                symbol = f"_var_{var_info['name']}"
                var_info["symbol"] = symbol

            # Constructor liefert:
            # AX = Offset
            # DX = Segment
            self.backend.emit_store_far_pointer_var(symbol)
            return
            
        slot   = info["slot"]
        target = CDATA.args_target.lower()

        if target in ["winnt", "nt35", "win32"]:
            symbol = info.get("symbol")

            if not symbol:
                symbol = f"_var_{name}"
                info["symbol"] = symbol

                if self.coff.find_symbol_index(symbol) is None:
                    self.coff.add_data_i32(symbol, 0)

            self.coff.emit_mov_data_label_r32(symbol, "eax")
            return

        if hasattr(self, "coff") and "symbol" in info:
            self.coff.emit_mov_data_label_r64(
                info["symbol"],
                "rax"
            )
            return

        self.emit_mov_qword("r11", "r12", "pointr_vars")
        self.emit_mov_qword_ptr_store("r11", slot * self.pointer_slot_size(), "rax", comment=f"object {name}")
        return
    
    def emit_store_class_property(self, ctx, parts, expr_type):
        obj_name  = parts[0]
        prop_name = parts[1]

        (
            source_kind,
            var_info,
            class_type
        ) = self.resolve_named_storage(
            ctx,
            obj_name
        )

        if class_type not in self.classes:
            return False

        cls = self.classes[class_type]
        prop = self.resolve_class_property(class_type, prop_name)

        if prop is None:
            return False

        if prop.write_name is None:
            raise CompileError(ctx, "E0006")

        value_type = self.resolve_type(
            expr_type
        )
        property_type = self.resolve_type(
            prop.ptype
        )

        if property_type == "double" and value_type == "integer":
            self.emit_cvtsi2sd(
                "xmm0",
                "eax"
            )
            value_type = "double"
            compatible = True
        elif property_type == "boolean" and value_type == "integer":
            self.emit_and(
                "eax",
                1,
                comment=f"normalize property {prop_name}"
            )
            value_type = "boolean"
            compatible = True
        elif property_type in self.classes:
            compatible = self.class_assignment_compatible(
                value_type,
                property_type
            )
        elif self.is_pointer_type(
            property_type,
            include_nil=False
        ):
            compatible = self.pointer_assignment_compatible(
                value_type,
                property_type
            )
        else:
            compatible = value_type == property_type

        if not compatible:
            raise CompileError(
                ctx,
                "E0005",
                got=value_type,
                expected=property_type
            )

        write_name = prop.write_name
        write_key  = write_name.lower()

        # Variante A:
        # property Value: Integer read FValue write FValue;
        if write_key in cls.fields:
            self.emit_store_class_field(
                ctx,
                [obj_name, write_name],
                expr_type
            )
            return True

        # Variante B:
        # property Value: Integer read GetValue write SetValue;
        is_nt32 = CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        )

        if property_type == "double":
            self.emit_sub(
                "esp" if is_nt32 else "rsp",
                8,
                comment="save property double value"
            )
            self.emit_movsd_store(
                "esp" if is_nt32 else "rsp",
                0,
                "xmm0"
            )
        else:
            self.emit_push(
                "eax" if is_nt32 else "rax",
                comment="property value"
            )

        method, owner_cls = self.find_class_method_recursive(
            ctx,
            class_type,
            write_name,
            [value_type]
        )

        self.emit_load_object_var(ctx, obj_name, var_info)
        self.emit_nil_pointer_check(obj_name)

        if is_nt32:
            if property_type == "double":
                # The saved 8-byte value is already in the correct cdecl
                # stack position. Self is pushed last and therefore becomes
                # the first hidden method parameter.
                cleanup_size = 12
            else:
                self.emit_pop("ebx")
                self.emit_push("ebx", comment="property setter value")
                cleanup_size = 8

            self.emit_push("eax", comment="Self")
            self.emit_class_method_call(
                method,
                comment=f"{owner_cls.name}.{method.name}"
            )
            self.backend.emit_cleanup_stack(cleanup_size)
            self.writer.emit_lea_reg_data_label("esi", "ctx")
            return True

        if property_type == "double":
            self.emit_movsd_load(
                "xmm1",
                "rsp",
                0
            )
            self.emit_add(
                "rsp",
                8,
                comment="restore property double value"
            )
        else:
            self.emit_pop("rdx")

        self.emit_mov("rcx", "rax", comment="Self")
        self.emit_sub("rsp", 32)
        self.emit_call_lbl(method.label)
        self.emit_add("rsp", 32)

        return True
    
    def emit_store_class_field(self, ctx, parts, expr_type):
        (
            var_info,
            resolved
        ) = self.resolve_class_field_path(
            ctx,
            parts
        )
        field, field_type = resolved[-1]
        value_type = self.resolve_type(
            expr_type
        )
        range_info = self.subrange_info(
            field_type
        )
        is_nt32 = CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        )
        address_reg = "eax" if is_nt32 else "rax"
        stack_reg = "esp" if is_nt32 else "rsp"
        path = ".".join(parts)

        if (
            range_info is not None
            and self.scalar_base_type(field_type) == "integer"
        ):
            if self.scalar_base_type(value_type) != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected=field_type
                )

            self.emit_subrange_check(
                ctx,
                field_type,
                value_reg="eax"
            )

        elif field_type == "double" and value_type == "integer":
            self.emit_cvtsi2sd(
                "xmm0",
                "eax"
            )
            value_type = "double"

        elif field_type == "integer":
            if self.scalar_base_type(value_type) != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected="integer"
                )

        elif field_type == "boolean":
            if value_type not in ("boolean", "integer"):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected="boolean"
                )

            self.emit_and(
                "eax",
                1,
                comment=f"normalize {path}"
            )
            value_type = "boolean"

        elif field_type == "char":
            if value_type != "char":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected="char"
                )

        elif self.is_class_type(field_type):
            if not self.class_assignment_compatible(
                value_type,
                field_type
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected=field_type
                )

        elif self.is_pointer_type(
            field_type,
            include_nil=False
        ):
            if not self.pointer_assignment_compatible(
                value_type,
                field_type
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected=field_type
                )

        elif field_type != value_type:
            raise CompileError(
                ctx,
                "E0005",
                got=value_type,
                expected=field_type
            )

        # Preserve the right-hand value before EAX/RAX is reused for
        # loading the object reference.
        if field_type == "double":
            self.emit_sub(
                stack_reg,
                8,
                comment="save class field double"
            )
            self.emit_movsd_store(
                stack_reg,
                0,
                "xmm0"
            )
        else:
            self.emit_push(
                "eax" if is_nt32 else "rax",
                comment="save class field value"
            )

        loaded_field, loaded_field_type = self.emit_class_member_address(
            ctx,
            parts
        )

        # Resolve and address generation must agree on the final member.
        field = loaded_field
        field_type = loaded_field_type

        if field_type == "double":
            self.emit_movsd_load(
                "xmm0",
                stack_reg,
                0
            )
            self.emit_add(
                stack_reg,
                8,
                comment="restore class field double"
            )
            self.emit_movsd_store(
                address_reg,
                field.offset,
                "xmm0",
                comment=path + " :="
            )
            return

        value_reg = "ebx" if is_nt32 else "r11"
        self.emit_pop(
            value_reg,
            comment="restore class field value"
        )

        if (
            range_info is not None
            and self.scalar_base_type(field_type) == "integer"
        ):
            if range_info.size == 1:
                self.emit_mov_byte_ptr_store(
                    address_reg,
                    field.offset,
                    "bl" if is_nt32 else "r11b",
                    comment=path + " :="
                )
            elif range_info.size == 2:
                self.emit_mov_word_ptr_store(
                    address_reg,
                    field.offset,
                    "bx" if is_nt32 else "r11w",
                    comment=path + " :="
                )
            elif range_info.size == 4:
                self.emit_mov_dword_ptr_store(
                    address_reg,
                    field.offset,
                    "ebx" if is_nt32 else "r11d",
                    comment=path + " :="
                )
            else:
                raise CompileError(
                    ctx,
                    "E0013",
                    var_type=field_type
                )

            return

        if field_type in ("integer", "boolean"):
            self.emit_mov_dword_ptr_store(
                address_reg,
                field.offset,
                "ebx" if is_nt32 else "r11d",
                comment=path + " :="
            )
            return

        if field_type == "char":
            self.emit_mov_byte_ptr_store(
                address_reg,
                field.offset,
                "bl" if is_nt32 else "r11b",
                comment=path + " :="
            )
            return

        if (
            field_type == "string"
            or self.is_class_type(field_type)
            or self.is_pointer_type(
                field_type,
                include_nil=False
            )
        ):
            if is_nt32:
                self.emit_mov_dword_ptr_store(
                    "eax",
                    field.offset,
                    "ebx",
                    comment=path + " :="
                )
            else:
                self.emit_mov_qword_ptr_store(
                    "rax",
                    field.offset,
                    "r11",
                    comment=path + " :="
                )

            return

        raise CompileError(
            ctx,
            "E0013",
            var_type=field_type
        )
    
    def emit_store_string_var_from_rax(self, ctx, name):
        var_info = self.var_info(ctx, name)
        slot = var_info["slot"]

        self.emit_mov_qword("rdx", "r12", "string_vars")
        self.emit_mov_qword_ptr_store("rdx", slot * self.pointer_slot_size(), "rax")
    
    def emit_store_string_char(self, ctx, name, index_exprs, expr_type):
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]

        if len(index_exprs) != 1:
            raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

        if expr_type != "char":
            raise CompileError(ctx, "E0005", got=expr_type, expected="char")

        is_nt32 = CDATA.args_target in ["nt35", "winnt", "win32"]

        if is_nt32:
            # Char-Wert aus EAX sichern.
            self.emit_mov(
                "ebx",
                "eax",
                comment="save string char value"
            )

            # Index berechnen -> eax
            index_type = self.visit(index_exprs[0])
            if index_type != "integer":
                raise CompileError(ctx, "E0005", got=index_type, expected="integer")

            self.emit_mov("ecx", "eax", comment="pascal string index")

            # String laden:
            # Bei Inline-Data-Modell zeigt S auf data, nicht auf Header.
            var_info = self.var_info(ctx, name)
            self.emit_load_var(name, var_info)

            # edx = data pointer
            self.emit_mov("edx", "eax", comment="string data")

            ok_not_nil = self.new_named_label("string_not_nil")
            self.emit_test("edx", "edx")
            self.emit_jnz(ok_not_nil)
            self.emit_call("_jit_error_string_range")
            self.emit_bind_label(ok_not_nil)

            # header = data - sizeof(DynStringHeader)
            # Layout:
            # +0 magic
            # +4 reserved
            # +8 length
            self.emit_mov("edi", "edx", comment="string data")
            self.emit_sub("edi", 12, comment="string header")

            # length = [header + 8]
            self.emit_mov_dword_ptr("eax", "edi", 8, comment="string length")

            ok_label   = self.new_named_label("string_index_ok")
            fail_label = self.new_named_label("string_index_fail")

            self.emit_cmp("ecx", 1)
            self.emit_jl(fail_label)

            self.emit_cmp("ecx", "eax")
            self.emit_jg(fail_label)

            self.emit_jmp(ok_label)

            self.emit_bind_label(fail_label)
            self.emit_call("_jit_error_string_range")

            self.emit_bind_label(ok_label)

            # data[index - 1] = bl
            self.emit_sub("ecx", 1)
            self.emit_add("edx", "ecx", comment="string char address")

            self.backend.writer.emit_mov_byte_ptr_reg8("edx", 0, "bl")
            return None

        # Win64-Pfad, ebenfalls Inline-Data-Modell.
        # Der Char-Wert liegt direkt in EAX.
        self.emit_mov(
            "ebx",
            "eax",
            comment="save string char value"
        )

        index_type = self.visit(index_exprs[0])
        if index_type != "integer":
            raise CompileError(ctx, "E0005", got=index_type, expected="integer")

        self.emit_mov("ecx", "eax", comment="pascal string index")

        var_info = self.var_info(ctx, name)
        self.emit_load_var(name, var_info)

        # rdx = data pointer
        self.emit_mov("rdx", "rax", comment="string data")

        ok_not_nil = self.new_named_label("string_not_nil")
        self.emit_test("rdx", "rdx")
        self.emit_jnz(ok_not_nil)

        self.emit_mov_imm("rax", "&_jit_error_string_range")
        self.emit_call("rax")

        self.emit_bind_label(ok_not_nil)

        # r11 = header = data - 12
        self.emit_mov("r11", "rdx", comment="string data")
        self.emit_sub("r11", 12, comment="string header")

        # length = [header + 8]
        self.emit_mov_reg_dword("eax", "r11", 8, comment="string length")

        ok_label   = self.new_named_label("string_index_ok")
        fail_label = self.new_named_label("string_index_fail")

        self.emit_cmp("ecx", 1)
        self.emit_jl(fail_label)

        self.emit_cmp("ecx", "eax")
        self.emit_jg(fail_label)

        self.emit_jmp(ok_label)

        self.emit_bind_label(fail_label)
        self.emit_mov_imm("rax", "&_jit_error_string_range")
        self.emit_call("rax")

        self.emit_bind_label(ok_label)

        self.emit_sub("ecx", 1)
        self.emit_movsxd("rcx", "ecx")
        self.emit_add("rdx", "rcx", comment="string char address")

        self.emit_mov_byte_ptr_store("rdx", 0, "bl", comment="s[index] :=")
        return None
    
    def pointer_slot_size(self):
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            return 4
        return 8
    
    def emit_store_pointer_var_from_rax(self, ctx, name):
        var_info = self.var_info(ctx, name)
        slot = var_info["slot"]

        self.emit_mov_qword("rdx", "r12", "pointr_vars")
        self.emit_mov_qword_ptr_store("rdx", slot * self.pointer_slot_size(), "rax")
    
    def resolve_named_storage(
        self,
        ctx,
        name
    ):
        """
        Ermittelt eine benannte Variable unabhängig von ihrem Speicherort.

        Rückgabe:
            (source_kind, info, resolved_type)

        source_kind:
            local
            param
            global
        """
        info = self.find_local_var(
            name
        )

        if info is not None:
            return (
                "local",
                info,
                self.resolve_type(
                    info["type"]
                )
            )

        info = self.find_param(
            name
        )

        if info is not None:
            return (
                "param",
                info,
                self.resolve_type(
                    info["type"]
                )
            )

        info = self.vars.get(
            name.lower()
        )

        if info is not None:
            return (
                "global",
                info,
                self.resolve_type(
                    info["type"]
                )
            )

        raise CompileError(
            ctx,
            "E0001",
            name=name
        )

    def lookup_var(
        self,
        name,
        ctx=None
    ):
        (
            source_kind,
            info,
            resolved_type
        ) = self.resolve_named_storage(
            ctx,
            name
        )

        return info


    def emit_load_named_value(
        self,
        ctx,
        name,
        source_kind,
        info
    ):
        if source_kind == "local":
            return self.emit_load_local_var(
                ctx,
                name,
                info
            )

        if source_kind == "param":
            return self.emit_load_param(
                ctx,
                name
            )

        if source_kind == "global":
            return self.emit_load_var(
                name,
                info
            )

        raise CompileError(
            ctx,
            "E0019",
            text=(
                f"unknown storage kind for "
                f"{name}: {source_kind}"
            )
        )

    def emit_load_var_value(
        self,
        name,
        ctx=None
    ):
        (
            source_kind,
            info,
            resolved_type
        ) = self.resolve_named_storage(
            ctx,
            name
        )

        return self.emit_load_named_value(
            ctx,
            name,
            source_kind,
            info
        )

    def emit_store_named_value(
        self,
        ctx,
        name,
        source_kind,
        info,
        value_type
    ):
        resolved_type = self.resolve_type(
            info["type"]
        )

        if source_kind == "local":
            self.emit_store_local_var(
                ctx,
                name,
                value_type
            )
            return

        if source_kind == "param":
            self.emit_store_param(
                ctx,
                name,
                value_type
            )
            return

        if source_kind == "global":
            if resolved_type in self.classes:
                self.emit_store_object_var(
                    ctx,
                    name,
                    info
                )
            else:
                self.emit_store_var(
                    ctx,
                    name,
                    info
                )

            return

        raise CompileError(
            ctx,
            "E0019",
            text=(
                f"unknown storage kind for "
                f"{name}: {source_kind}"
            )
        )


    def pointed_element_type(
        self,
        ctx,
        pointer_type
    ):
        resolved_pointer_type = self.resolve_type(
            pointer_type
        )

        if resolved_pointer_type in (
            "pchar",
            "pansichar"
        ):
            return "char"

        if resolved_pointer_type == "pointer":
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "untyped Pointer cannot be indexed; "
                    "cast it to a typed pointer first"
                )
            )

        if (
            not isinstance(
                resolved_pointer_type,
                str
            )
            or not resolved_pointer_type.startswith("^")
        ):
            raise CompileError(
                ctx,
                "E0005",
                got=resolved_pointer_type,
                expected="typed pointer"
            )

        return self.resolve_type(
            resolved_pointer_type[1:]
        )


    def emit_load_pointer_element(
        self,
        ctx,
        name,
        index_exprs
    ):
        """
        Lädt P[Index] für einen typisierten Pointer.

        PAnsiChar verwendet bewusst nullbasierte Indizes:
            P[0] = erstes Byte
        """
        if not isinstance(
            index_exprs,
            list
        ):
            index_exprs = [
                index_exprs
            ]

        if len(index_exprs) != 1:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(index_exprs)),
                expected="1"
            )

        (
            source_kind,
            info,
            pointer_type
        ) = self.resolve_named_storage(
            ctx,
            name
        )

        if not self.is_pointer_type(
            pointer_type,
            include_nil=False
        ):
            raise CompileError(
                ctx,
                "E0005",
                got=pointer_type,
                expected="typed pointer"
            )

        element_type = self.pointed_element_type(
            ctx,
            pointer_type
        )

        index_type = self.visit(
            index_exprs[0]
        )

        if self.scalar_base_type(
            index_type
        ) != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=index_type,
                expected="integer"
            )

        is_nt32 = CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        )

        if is_nt32:
            self.emit_mov(
                "ecx",
                "eax",
                comment=f"{name} pointer index"
            )
        else:
            self.emit_mov(
                "ecx",
                "eax",
                comment=f"{name} pointer index"
            )

        self.emit_load_named_value(
            ctx,
            name,
            source_kind,
            info
        )

        self.emit_nil_pointer_check(
            name
        )

        element_size = self.type_size(
            ctx,
            element_type
        )

        if element_size != 1:
            self.emit_imul(
                "ecx",
                "ecx",
                element_size,
                comment=f"{name} pointer byte offset"
            )

        address_reg = (
            "eax"
            if is_nt32
            else "rax"
        )

        if is_nt32:
            self.emit_add(
                "eax",
                "ecx",
                comment=f"{name}[index] address"
            )
        else:
            self.emit_movsxd(
                "rcx",
                "ecx"
            )

            self.emit_add(
                "rax",
                "rcx",
                comment=f"{name}[index] address"
            )

        range_info = self.subrange_info(
            element_type
        )

        if element_type == "char":
            self.backend.writer.emit_movzx_r32_byte_ptr(
                "eax",
                address_reg,
                0
            )

            return "char"

        if element_type == "boolean":
            self.backend.writer.emit_movzx_r32_byte_ptr(
                "eax",
                address_reg,
                0
            )

            self.emit_and(
                "eax",
                1
            )

            return "boolean"

        if (
            element_type == "integer"
            or (
                range_info is not None
                and range_info.base_type == "integer"
            )
        ):
            size = (
                int(range_info.size)
                if range_info is not None
                else 4
            )

            if size == 1:
                self.backend.writer.emit_movzx_r32_byte_ptr(
                    "eax",
                    address_reg,
                    0
                )

            elif size == 4:
                self.emit_mov_dword_ptr(
                    "eax",
                    address_reg,
                    0,
                    comment=f"load {name}[index]"
                )

            else:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "indexed pointer load currently "
                        f"does not support {size}-byte integers"
                    )
                )

            return (
                element_type
                if range_info is not None
                else "integer"
            )

        raise CompileError(
            ctx,
            "E0019",
            text=(
                "indexed pointer load is not implemented "
                f"for element type {element_type}"
            )
        )


    def emit_store_pointer_element(
        self,
        ctx,
        name,
        index_exprs,
        expr_type
    ):
        """
        Speichert P[Index] := Value für einen typisierten Pointer.

        Der aktuelle CRC-Anwendungsfall ist:
            Result: PAnsiChar
            Result[0] := HexDigits[...]
            Result[4] := #0
        """
        if not isinstance(
            index_exprs,
            list
        ):
            index_exprs = [
                index_exprs
            ]

        if len(index_exprs) != 1:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(index_exprs)),
                expected="1"
            )

        (
            source_kind,
            info,
            pointer_type
        ) = self.resolve_named_storage(
            ctx,
            name
        )

        if not self.is_pointer_type(
            pointer_type,
            include_nil=False
        ):
            raise CompileError(
                ctx,
                "E0005",
                got=pointer_type,
                expected="typed pointer"
            )

        element_type = self.pointed_element_type(
            ctx,
            pointer_type
        )

        resolved_expr_type = self.resolve_type(
            expr_type
        )

        element_base_type = self.scalar_base_type(
            element_type
        )

        expression_base_type = self.scalar_base_type(
            resolved_expr_type
        )

        if element_base_type != expression_base_type:
            raise CompileError(
                ctx,
                "E0005",
                got=resolved_expr_type,
                expected=element_type
            )

        is_nt32 = CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        )

        # Rechten Wert sichern, weil die Indexauswertung EAX verändert.
        self.emit_push(
            "eax" if is_nt32 else "rax",
            comment=f"save {name}[index] value"
        )

        index_type = self.visit(
            index_exprs[0]
        )

        if self.scalar_base_type(
            index_type
        ) != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=index_type,
                expected="integer"
            )

        self.emit_mov(
            "ecx",
            "eax",
            comment=f"{name} pointer index"
        )

        self.emit_load_named_value(
            ctx,
            name,
            source_kind,
            info
        )

        self.emit_nil_pointer_check(
            name
        )

        element_size = self.type_size(
            ctx,
            element_type
        )

        if element_size != 1:
            self.emit_imul(
                "ecx",
                "ecx",
                element_size,
                comment=f"{name} pointer byte offset"
            )

        if is_nt32:
            self.emit_add(
                "eax",
                "ecx",
                comment=f"{name}[index] address"
            )

            self.emit_pop(
                "ebx",
                comment=f"restore {name}[index] value"
            )

            if element_type in (
                "char",
                "boolean"
            ) or (
                self.subrange_info(
                    element_type
                ) is not None
                and self.subrange_info(
                    element_type
                ).size == 1
            ):
                self.backend.writer.emit_mov_byte_ptr_reg8(
                    "eax",
                    0,
                    "bl"
                )

                return None

            if element_type == "integer":
                self.emit_mov_dword_ptr_store(
                    "eax",
                    0,
                    "ebx",
                    comment=f"{name}[index] :="
                )

                return None

        else:
            self.emit_movsxd(
                "rcx",
                "ecx"
            )

            self.emit_add(
                "rax",
                "rcx",
                comment=f"{name}[index] address"
            )

            self.emit_pop(
                "rbx",
                comment=f"restore {name}[index] value"
            )

            if element_type in (
                "char",
                "boolean"
            ) or (
                self.subrange_info(
                    element_type
                ) is not None
                and self.subrange_info(
                    element_type
                ).size == 1
            ):
                self.emit_mov_byte_ptr_store(
                    "rax",
                    0,
                    "bl",
                    comment=f"{name}[index] :="
                )

                return None

            if element_type == "integer":
                self.emit_mov_dword_ptr_store(
                    "rax",
                    0,
                    "ebx",
                    comment=f"{name}[index] :="
                )

                return None

        raise CompileError(
            ctx,
            "E0019",
            text=(
                "indexed pointer store is not implemented "
                f"for element type {element_type}"
            )
        )


    def emit_store_pointer_deref(self, ctx, name, expr_type):
        key = name.lower()

        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=name)

        info = self.vars[key]
        typ = info["type"]

        if not isinstance(typ, str) or not typ.startswith("^"):
            raise CompileError(ctx, "E0005", got=typ, expected="pointer")

        base_type = typ[1:]

        if base_type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=base_type)

        if expr_type == "integer":
            self.emit_mov("ebx", "eax")

        elif expr_type == "double":
            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")

        elif expr_type == "string":
            self.emit_push("rax")

        self.emit_load_var(name, info)

        if expr_type == "integer":
            self.emit_mov_dword_ptr_store("rax", 0, "ebx", comment="p^ :=")
            return

        if expr_type == "double":
            self.emit_movsd_load("xmm0", "rsp")
            self.emit_add("rsp", 8)
            self.emit_movsd_store("rax", 0, "xmm0", comment="p^ :=")
            return

        if expr_type == "string":
            self.emit_pop("r11")
            self.emit_mov_qword_ptr_store("rax", 0, "r11", comment="p^ :=")
            return
        
    def emit_store_record_field(self, ctx, parts, expr_type):
        (
            source_kind,
            info,
            field_offset,
            field
        ) = self.resolve_record_path(
            ctx,
            parts
        )

        path = ".".join(parts)
        is_nt32 = CDATA.args_target in ["nt35", "winnt", "win32"]
        field_type = self.resolve_type(
            field.type
        )
        value_type = self.resolve_type(
            expr_type
        )

        if field_type == "double" and value_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")
            value_type = "double"

        if field_type == "boolean":
            if value_type not in ("boolean", "integer"):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected="boolean"
                )

            self.emit_and("eax", 1)

            value_type = "boolean"

        elif field_type in self.classes:
            if not self.class_assignment_compatible(
                value_type,
                field_type
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected=field_type
                )

        elif self.is_pointer_type(
            field_type,
            include_nil=False
        ):
            if not self.pointer_assignment_compatible(
                value_type,
                field_type
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected=field_type
                )

        elif field_type != value_type:
            raise CompileError(
                ctx,
                "E0005",
                got=value_type,
                expected=field_type
            )

        address_reg = (
            "edx"
            if is_nt32
            else "r11"
        )

        self.emit_record_base_address(
            ctx,
            parts[0],
            source_kind,
            info,
            address_reg
        )

        if field_type in ("integer", "boolean"):
            self.emit_mov_dword_ptr_store(
                address_reg,
                field_offset,
                "eax",
                comment=path
            )
            return

        if field_type == "char":
            self.emit_mov_byte_ptr_store(
                address_reg,
                field_offset,
                "al",
                comment=path
            )
            return

        if field_type == "double":
            self.emit_movsd_store(
                address_reg,
                field_offset,
                "xmm0",
                comment=path
            )
            return

        if (
            field_type == "string"
            or field_type in self.classes
            or self.is_pointer_type(
                field_type,
                include_nil=False
            )
        ):
            if is_nt32:
                self.emit_mov_dword_ptr_store(
                    address_reg,
                    field_offset,
                    "eax",
                    comment=path
                )
            else:
                self.emit_mov_qword_ptr_store(
                    address_reg,
                    field_offset,
                    "rax",
                    comment=path
                )

            return

        raise CompileError(
            ctx,
            "E0013",
            var_type=field_type
        )
    
    def emit_store_param(self, ctx, name, expr_type):
        param = self.find_param(name)

        if not param:
            raise CompileError(ctx, "E0001", name=name)

        typ = self.resolve_type(param["type"])
        value_type = self.resolve_type(expr_type)
        offset = param["stack_offset"]

        if typ in self.classes:
            compatible = self.class_assignment_compatible(
                value_type,
                typ
            )
        elif self.is_pointer_type(
            typ,
            include_nil=False
        ):
            compatible = self.pointer_assignment_compatible(
                value_type,
                typ
            )
        elif typ == "boolean":
            compatible = value_type in (
                "boolean",
                "integer"
            )
        else:
            compatible = typ == value_type

        if not compatible:
            raise CompileError(
                ctx,
                "E0005",
                got=value_type,
                expected=typ
            )

        if typ == "boolean":
            self.emit_and(
                "eax",
                1,
                comment=f"normalize var parameter {name}"
            )

        # -------------------------------------------------------
        # NT32
        # -------------------------------------------------------
        if CDATA.args_target in ["nt35", "winnt", "win32"]:

            if param.get("is_var", False):
                #
                # Stack:
                #
                # [ebp+8]  -> Adresse der eigentlichen Variable
                #
                self.emit_mov_dword_ptr("ebx", "ebp", offset)

                if typ in ("integer", "boolean"):
                    self.emit_mov_dword_ptr_store("ebx", 0, "eax")
                    return

                if typ == "char":
                    self.emit_mov_byte_ptr_store("ebx", 0, "al")
                    return

                if typ == "double":
                    self.emit_movsd_store("ebx", 0, "xmm0")
                    return

                if typ == "string":
                    self.emit_mov_dword_ptr_store("ebx", 0, "eax")
                    return

                if (
                    typ in self.classes
                    or self.is_pointer_type(
                        typ,
                        include_nil=False
                    )
                ):
                    self.emit_mov_dword_ptr_store("ebx", 0, "eax")
                    return

                raise CompileError(ctx, "E0013", var_type=typ)

            #
            # normale Parameter dürfen nicht beschrieben werden
            #
            raise CompileError(ctx, "E0006", name=name)

        # -------------------------------------------------------
        # Win64
        # -------------------------------------------------------
        if not param.get("is_var", False):
            raise CompileError(ctx, "E0006", name=name)

        #
        # var-Parameter:
        # [rbp+offset] enthält die Adresse der Variablen
        #
        self.emit_mov_qword_ptr("r11", "rbp", offset)

        if typ in ("integer", "boolean"):
            self.emit_mov_reg_dword_store("r11", "eax")
            return

        if typ == "char":
            self.emit_mov_byte_ptr_store("r11", 0, "al")
            return

        if typ == "double":
            self.emit_movsd_store("r11", 0, "xmm0")
            return

        if typ == "string":
            self.emit_mov_reg_qword_store("r11", "rax")
            return

        if (
            typ in self.classes
            or self.is_pointer_type(
                typ,
                include_nil=False
            )
        ):
            self.emit_mov_reg_qword_store("r11", "rax")
            return

        raise CompileError(ctx, "E0013", var_type=typ)

    def emit_mov_byte_ptr_store(
        self,
        base,
        offset,
        src,
        comment=""
    ):
        self.backend.emit_mov_byte_ptr_store(
            base,
            offset,
            src,
            comment
        )
        
    def emit_mov_word_ptr_store(
        self,
        base,
        offset,
        src,
        comment=""
    ):
        self.backend.emit_mov_word_ptr_store(
            base,
            offset,
            src,
            comment
        )
    
    def emit_store_pointer_record_field(
        self,
        ctx,
        parts,
        expr_type
    ):
        if not parts or len(parts) < 2:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "pointer record field assignment "
                    "requires a pointer and a field"
                )
            )

        (
            ptr_info,
            field_offset,
            field
        ) = self.resolve_pointer_record_path(
            ctx,
            parts
        )

        if field is None:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "pointer record field assignment "
                    "could not resolve the target field"
                )
            )

        ptr_name = parts[0]

        path = (
            ptr_name
            + "^."
            + ".".join(parts[1:])
        )

        is_nt32 = (
            CDATA.args_target
            in (
                "nt35",
                "winnt",
                "win32"
            )
        )

        address_reg = (
            "eax"
            if is_nt32
            else "rax"
        )

        stack_reg = (
            "esp"
            if is_nt32
            else "rsp"
        )

        # ----------------------------------------------------------
        # Deklarierten und tatsächlichen Typ normalisieren
        # ----------------------------------------------------------
        declared_field_type = str(
            field.type
        ).lower()

        resolved_field_type = self.resolve_type(
            declared_field_type
        )

        resolved_expr_type = self.resolve_type(
            expr_type
        )

        field_base_type = self.scalar_base_type(
            declared_field_type
        )

        expr_base_type = self.scalar_base_type(
            resolved_expr_type
        )

        field_range = self.subrange_info(
            declared_field_type
        )

        field_size = getattr(
            field,
            "size",
            None
        )

        if field_size is None:
            field_size = self.type_size(
                ctx,
                declared_field_type
            )

        field_size = int(
            field_size
        )

        # ----------------------------------------------------------
        # Hilfsfunktion: Zieladresse laden
        # ----------------------------------------------------------
        def load_target_address():
            self.emit_load_pointer_reference(
                ctx,
                ptr_name,
                ptr_info
            )

            self.emit_nil_pointer_check(
                ptr_name
            )

            if field_offset != 0:
                self.emit_add(
                    address_reg,
                    field_offset,
                    comment="record field offset"
                )

        # ----------------------------------------------------------
        # Hilfsfunktion: Integerwert passend zur Feldgröße speichern
        #
        # Der Wert befindet sich in EBX.
        # ----------------------------------------------------------
        def store_scalar_from_ebx():
            if field_size == 1:
                self.emit_mov_byte_ptr_store(
                    address_reg,
                    0,
                    "bl",
                    comment=f"{path} :="
                )

                return

            if field_size == 2:
                self.emit_mov_word_ptr_store(
                    address_reg,
                    0,
                    "bx",
                    comment=f"{path} low byte"
                )

                return

            if field_size == 4:
                self.emit_mov_dword_ptr_store(
                    address_reg,
                    0,
                    "ebx",
                    comment=f"{path} :="
                )

                return

            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"unsupported scalar field size "
                    f"{field_size} for {path}"
                )
            )

        # ==========================================================
        # Pointerfeld
        # ==========================================================
        field_is_pointer = self.is_pointer_type(
            resolved_field_type,
            include_nil=False
        )

        expr_ctx = (
            ctx.expr()
            if hasattr(ctx, "expr")
            else None
        )

        expr_text = (
            expr_ctx.getText().strip()
            if expr_ctx is not None
            else ""
        )

        expression_is_zero_literal = (
            resolved_expr_type == "integer"
            and expr_text in (
                "0",
                "+0",
                "-0",
                "$0",
                "#0"
            )
        )

        expression_is_nil = (
            resolved_expr_type
            in (
                "nil",
                "^nil"
            )
            or expression_is_zero_literal
        )

        if field_is_pointer:
            if expression_is_nil:
                # XOR EAX,EAX löscht unter x64 zugleich ganz RAX.
                self.emit_xor(
                    "eax",
                    "eax",
                    comment="nil pointer value"
                )

            else:
                expression_is_pointer = self.is_pointer_type(
                    resolved_expr_type,
                    include_nil=False
                )

                if not expression_is_pointer:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=expr_type,
                        expected=declared_field_type
                    )

                if (
                    resolved_field_type
                    != resolved_expr_type
                ):
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=expr_type,
                        expected=declared_field_type
                    )

            if is_nt32:
                self.emit_push(
                    "eax",
                    comment="save right pointer value"
                )

                load_target_address()

                self.emit_pop(
                    "ebx",
                    comment="restore right pointer value"
                )

                self.emit_mov_dword_ptr_store(
                    "eax",
                    0,
                    "ebx",
                    comment=f"{path} :="
                )

                return

            self.emit_push(
                "rax",
                comment="save right pointer value"
            )

            load_target_address()

            self.emit_pop(
                "r11",
                comment="restore right pointer value"
            )

            self.emit_mov_qword_ptr_store(
                "rax",
                0,
                "r11",
                comment=f"{path} :="
            )

            return

        # ==========================================================
        # Klassenfeld
        #
        # Klassenvariablen enthalten ebenfalls einen Objektpointer.
        # ==========================================================
        field_is_class = (
            isinstance(resolved_field_type, str)
            and resolved_field_type in self.classes
        )

        if field_is_class:
            if expression_is_nil:
                self.emit_xor(
                    "eax",
                    "eax",
                    comment="nil object value"
                )

            else:
                expression_is_class = (
                    isinstance(resolved_expr_type, str)
                    and resolved_expr_type in self.classes
                )

                if (
                    not expression_is_class
                    or not self.class_is_descendant(
                        resolved_expr_type,
                        resolved_field_type
                    )
                ):
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=expr_type,
                        expected=declared_field_type
                    )

            if is_nt32:
                self.emit_push(
                    "eax",
                    comment="save right object value"
                )

                load_target_address()

                self.emit_pop(
                    "ebx",
                    comment="restore right object value"
                )

                self.emit_mov_dword_ptr_store(
                    "eax",
                    0,
                    "ebx",
                    comment=f"{path} :="
                )

                return

            self.emit_push(
                "rax",
                comment="save right object value"
            )

            load_target_address()

            self.emit_pop(
                "r11",
                comment="restore right object value"
            )

            self.emit_mov_qword_ptr_store(
                "rax",
                0,
                "r11",
                comment=f"{path} :="
            )

            return

        # ==========================================================
        # Stringfeld
        # ==========================================================
        if resolved_field_type == "string":
            if resolved_expr_type != "string":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=expr_type,
                    expected=declared_field_type
                )

            if is_nt32:
                self.emit_push(
                    "eax",
                    comment="save right string value"
                )

                load_target_address()

                self.emit_pop(
                    "ebx",
                    comment="restore right string value"
                )

                self.emit_mov_dword_ptr_store(
                    "eax",
                    0,
                    "ebx",
                    comment=f"{path} :="
                )

                return

            self.emit_push(
                "rax",
                comment="save right string value"
            )

            load_target_address()

            self.emit_pop(
                "r11",
                comment="restore right string value"
            )

            self.emit_mov_qword_ptr_store(
                "rax",
                0,
                "r11",
                comment=f"{path} :="
            )

            return

        # ==========================================================
        # Doublefeld
        # ==========================================================
        if resolved_field_type == "double":
            if expr_base_type == "integer":
                self.emit_cvtsi2sd(
                    "xmm0",
                    "eax",
                    comment="integer to double"
                )

            elif resolved_expr_type != "double":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=expr_type,
                    expected=declared_field_type
                )

            # XMM0 sichern, weil das Laden der Zieladresse weitere
            # Generatoroperationen ausführt.
            self.emit_sub(
                stack_reg,
                8,
                comment="save right double value"
            )

            self.emit_movsd_store(
                stack_reg,
                0,
                "xmm0"
            )

            load_target_address()

            self.emit_movsd_load(
                "xmm0",
                stack_reg,
                0
            )

            self.emit_add(
                stack_reg,
                8,
                comment="restore stack after double value"
            )

            self.emit_movsd_store(
                address_reg,
                0,
                "xmm0",
                comment=f"{path} :="
            )

            return

        # ==========================================================
        # Booleanfeld
        # ==========================================================
        if resolved_field_type == "boolean":
            if resolved_expr_type != "boolean":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=expr_type,
                    expected=declared_field_type
                )

            self.emit_and(
                "eax",
                1,
                comment="normalize boolean value"
            )

            self.emit_push(
                address_reg,
                comment="save right boolean value"
            )

            load_target_address()

            if is_nt32:
                self.emit_pop(
                    "ebx",
                    comment="restore right boolean value"
                )
            else:
                self.emit_pop(
                    "rbx",
                    comment="restore right boolean value"
                )

            store_scalar_from_ebx()
            return

        # ==========================================================
        # Integer, Enum und Subrange
        #
        # Beispiele:
        #
        #     Integer
        #     Byte
        #     Word
        #     DWord
        #     ShortInt
        #     SmallInt
        # ==========================================================
        if field_base_type == "integer":
            if expr_base_type != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=expr_type,
                    expected=declared_field_type
                )

            if field_range is not None:
                self.emit_subrange_check(
                    ctx,
                    declared_field_type,
                    "eax"
                )

            self.emit_push(
                address_reg,
                comment="save right integer value"
            )

            load_target_address()

            if is_nt32:
                self.emit_pop(
                    "ebx",
                    comment="restore right integer value"
                )
            else:
                self.emit_pop(
                    "rbx",
                    comment="restore right integer value"
                )

            store_scalar_from_ebx()
            return

        # ==========================================================
        # Char / AnsiChar
        # ==========================================================
        if field_base_type == "char":
            if expr_base_type != "char":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=expr_type,
                    expected=declared_field_type
                )

            self.emit_push(
                address_reg,
                comment="save right char value"
            )

            load_target_address()

            if is_nt32:
                self.emit_pop(
                    "ebx",
                    comment="restore right char value"
                )
            else:
                self.emit_pop(
                    "rbx",
                    comment="restore right char value"
                )

            self.emit_mov_byte_ptr_store(
                address_reg,
                0,
                "bl",
                comment=f"{path} :="
            )

            return

        # Eingebettete Record-Gesamtzuweisungen sind hier noch
        # nicht implementiert.
        raise CompileError(
            ctx,
            "E0013",
            var_type=declared_field_type
        )    

    def emit_store_array_element(self, ctx, var_name, index_expr_ctx, expr_type):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]

        var_info, array_info = self.get_array_info(ctx, var_name)
        elem_type = self.normalize_array_element_type(array_info.element_type)

        is_nt32 = CDATA.args_target in ["nt35", "winnt", "win32"]

        # ------------------------------------------------------------
        # Boolean wird wie 32-bit Integer gespeichert,
        # bleibt aber vom Sprachtyp her boolean.
        # ------------------------------------------------------------
        if elem_type == "boolean":
            if expr_type != "boolean":
                raise CompileError(ctx, "E0005", got=expr_type, expected="boolean")

            self.emit_and("eax", 1, comment="normalize boolean")

        elif elem_type == "double" and expr_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")
            expr_type = "double"

        elif elem_type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=elem_type)

        # ------------------------------------------------------------
        # Dynamic array
        # ------------------------------------------------------------
        if getattr(array_info, "is_dynamic", False):
            if len(index_exprs) != 1:
                raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

            # Wert sichern
            if elem_type in ("integer", "boolean"):
                if is_nt32:
                    self.emit_push("eax", comment="save array value")
                else:
                    self.emit_mov_dword_ptr_store(
                        "r12",
                        "offsetof(JitContext, print_int_tmp)",
                        "eax"
                    )

            elif elem_type == "double":
                if is_nt32:
                    self.emit_sub("esp", 8)
                    self.emit_movsd_store("esp", 0, "xmm0")
                else:
                    self.emit_movsd_store(
                        "r12",
                        "offsetof(JitContext, print_double_tmp)",
                        "xmm0"
                    )

            elif elem_type == "string":
                self.emit_push("eax" if is_nt32 else "rax")

            else:
                raise CompileError(ctx, "E0013", var_type=elem_type)

            # Index berechnen
            index_type = self.visit(index_exprs[0])
            if index_type != "integer":
                raise CompileError(ctx, "E0005", got=index_type, expected="integer")

            if is_nt32:
                self.emit_imul("eax", "eax", array_info.element_size)
                self.emit_mov("edx", "eax", comment="dynamic array byte offset")

                self.emit_load_var(var_name, var_info)   # eax = data pointer
                self.emit_add("eax", "edx", comment="dynamic array element address")

                if elem_type in ("integer", "boolean"):
                    self.emit_pop("ebx", comment="restore array value")
                    self.emit_mov_dword_ptr_store("eax", 0, "ebx")
                    return None

                if elem_type == "double":
                    self.emit_movsd_load("xmm0", "esp")
                    self.emit_add("esp", 8)
                    self.emit_movsd_store("eax", 0, "xmm0")
                    return None

                if elem_type == "string":
                    self.emit_pop("ebx")
                    self.emit_mov_dword_ptr_store("eax", 0, "ebx")
                    return None

            # Win64 dynamic
            self.emit_imul("eax", "eax", array_info.element_size)
            self.emit_mov("r10d", "eax", comment="save dynamic array byte offset")

            self.emit_load_var(var_name, var_info)   # rax = data pointer
            self.emit_movsxd("r11", "r10d")
            self.emit_add("r11", "rax", comment="dynamic array element address")

            if elem_type in ("integer", "boolean"):
                self.emit_mov_dword("eax", "r12", "print_int_tmp")
                self.emit_mov_dword_ptr_store("r11", 0, "eax")
                return None

            if elem_type == "double":
                self.emit_movsd_load_field("xmm0", "r12", "print_double_tmp")
                self.emit_movsd_store("r11", 0, "xmm0")
                return None

            if elem_type == "string":
                self.emit_pop("rax")
                self.emit_mov_qword_ptr_store("r11", 0, "rax")
                return None

            raise CompileError(ctx, "E0013", var_type=elem_type)

        # ------------------------------------------------------------
        # Static array
        # ------------------------------------------------------------

        # Wert sichern
        if elem_type in ("integer", "boolean"):
            if is_nt32:
                self.emit_push("eax", comment="save array value")
            else:
                self.emit_mov_dword_ptr_store(
                    "r12",
                    "offsetof(JitContext, print_int_tmp)",
                    "eax"
                )

        elif elem_type == "double":
            if is_nt32:
                self.emit_sub("esp", 8)
                self.emit_movsd_store("esp", 0, "xmm0")
            else:
                self.emit_sub("rsp", 8)
                self.emit_movsd_store("rsp", 0, "xmm0")

        elif elem_type == "string":
            self.emit_push("eax" if is_nt32 else "rax")

        else:
            raise CompileError(ctx, "E0013", var_type=elem_type)

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        if is_nt32:
            self.emit_imul("eax", "eax", array_info.element_size)
            self.emit_add("eax", var_info["slot"])

            self.emit_mov("edx", "eax", comment="array byte offset")

            symbol = var_info.get("symbol")
            if not symbol:
                symbol = f"_var_{var_info['name']}"
                var_info["symbol"] = symbol

            self.writer.emit_lea_reg_data_label("eax", symbol)
            self.emit_add("eax", "edx", comment="array element address")

            if elem_type in ("integer", "boolean"):
                self.emit_pop("ebx", comment="restore array value")
                self.emit_mov_dword_ptr_store("eax", 0, "ebx")
                return None

            if elem_type == "double":
                self.emit_movsd_load("xmm0", "esp")
                self.emit_add("esp", 8)
                self.emit_movsd_store("eax", 0, "xmm0")
                return None

            if elem_type == "string":
                self.emit_pop("ebx")
                self.emit_mov_dword_ptr_store("eax", 0, "ebx")
                return None

            raise CompileError(ctx, "E0013", var_type=elem_type)

        # Win64 static
        self.emit_imul("eax", "eax", array_info.element_size)
        self.emit_add("eax", var_info["slot"])

        self.emit_mov_qword("r11", "r12", "arrays_vars")
        self.emit_movsxd("rax", "eax")
        self.emit_add("r11", "rax")

        if elem_type in ("integer", "boolean"):
            self.emit_mov_dword("eax", "r12", "print_int_tmp")
            self.emit_mov_dword_ptr_store("r11", 0, "eax")
            return None

        if elem_type == "double":
            self.emit_movsd_load("xmm0", "rsp")
            self.emit_add("rsp", 8)
            self.emit_movsd_store("r11", 0, "xmm0")
            return None

        if elem_type == "string":
            self.emit_pop("rax")
            self.emit_mov_qword_ptr_store("r11", 0, "rax")
            return None

        raise CompileError(ctx, "E0013", var_type=elem_type)

    def normalize_array_element_type(self, t):
        raw = str(t).lower()

        if raw == "boolean":
            return "boolean"

        resolved = self.resolve_type(t)

        if str(resolved).lower() == "boolean":
            return "boolean"

        return resolved
    
    def emit_load_array_element(self, ctx, var_name, index_expr_ctx):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]

        var_info, array_info = self.get_array_info(ctx, var_name)
        elem_type = self.normalize_array_element_type(array_info.element_type)

        is_nt32 = CDATA.args_target in ["nt35", "winnt", "win32"]

        # ------------------------------------------------------------
        # Dynamic array
        # ------------------------------------------------------------
        if getattr(array_info, "is_dynamic", False):
            if len(index_exprs) != 1:
                raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

            index_type = self.visit(index_exprs[0])
            if index_type != "integer":
                raise CompileError(ctx, "E0005", got=index_type, expected="integer")

            if is_nt32:
                self.emit_imul("eax", "eax", array_info.element_size)
                self.emit_mov("edx", "eax", comment="dynamic array byte offset")

                self.emit_load_var(var_name, var_info)   # eax = data pointer
                self.emit_add("eax", "edx", comment="dynamic array element address")

                if elem_type in ("integer", "boolean"):
                    self.emit_mov_dword_ptr("eax", "eax", 0, comment="load array element")

                    if elem_type == "boolean":
                        self.emit_and("eax", 1)
                        return "boolean"

                    return "integer"

                if elem_type == "double":
                    self.emit_movsd_load("xmm0", "eax")
                    return "double"

                if elem_type == "string":
                    self.emit_mov_dword_ptr("eax", "eax", 0, comment="load string pointer")
                    return "string"

                raise CompileError(ctx, "E0014", var_type=elem_type)

            # Win64 dynamic array
            self.emit_imul("eax", "eax", array_info.element_size)
            self.emit_mov("r10d", "eax", comment="save dynamic array byte offset")

            self.emit_load_var(var_name, var_info)   # rax = data pointer
            self.emit_movsxd("r11", "r10d")
            self.emit_add("r11", "rax", comment="dynamic array element address")

            if elem_type in ("integer", "boolean"):
                self.emit_mov_reg_dword("eax", "r11")

                if elem_type == "boolean":
                    self.emit_and("eax", 1)
                    return "boolean"

                return "integer"

            if elem_type == "double":
                self.emit_movsd_load("xmm0", "r11")
                return "double"

            if elem_type == "string":
                self.emit_mov_reg_qword("rax", "r11")
                return "string"

            raise CompileError(ctx, "E0014", var_type=elem_type)

        # ------------------------------------------------------------
        # Static array
        # ------------------------------------------------------------
        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        if is_nt32:
            # eax = linear index
            self.emit_imul("eax", "eax", array_info.element_size)
            self.emit_mov("edx", "eax", comment="array byte offset")

            symbol = var_info.get("symbol")
            if not symbol:
                symbol = f"_var_{var_info['name']}"
                var_info["symbol"] = symbol

            # eax = &_var_flags
            self.writer.emit_lea_reg_data_label("eax", symbol)

            # eax = &_var_flags + byte_offset
            self.emit_add("eax", "edx", comment="array element address")

            if elem_type in ("integer", "boolean"):
                self.emit_mov_dword_ptr("eax", "eax", 0, comment="load array element")

                if elem_type == "boolean":
                    self.emit_and("eax", 1)
                    return "boolean"

                return "integer"

            if elem_type == "double":
                self.emit_movsd_load("xmm0", "eax")
                return "double"

            if elem_type == "string":
                self.emit_mov_dword_ptr("eax", "eax", 0, comment="load string pointer")
                return "string"

            raise CompileError(ctx, "E0014", var_type=elem_type)

        # Win64 static array
        self.emit_imul("eax", "eax", array_info.element_size)
        self.emit_add("eax", var_info["slot"])

        self.emit_mov_qword("r11", "r12", "arrays_vars")
        self.emit_movsxd("rax", "eax")
        self.emit_add("r11", "rax")

        if elem_type in ("integer", "boolean"):
            self.emit_mov_reg_dword("eax", "r11")

            if elem_type == "boolean":
                self.emit_and("eax", 1)
                return "boolean"

            return "integer"

        if elem_type == "double":
            self.emit_movsd_load("xmm0", "r11")
            return "double"

        if elem_type == "string":
            self.emit_mov_reg_qword("rax", "r11")
            return "string"

        raise CompileError(ctx, "E0014", var_type=elem_type)
        
    def emit_store_result(self, ctx, expr_type):
        if self.current_function is None:
            raise CompileError(ctx, "E0006")

        declared_return_type = self.resolve_type(
            self.current_function["return_type"]
        )

        return_type = self.current_function.get(
            "abi_return_type"
        )

        if return_type is None:
            return_type = self.function_abi_return_type(
                declared_return_type
            )

        resolved_expr_type = self.resolve_type(
            expr_type
        )

        expr_abi_type = self.function_abi_return_type(
            resolved_expr_type
        )

        # ----------------------------------------------------------
        # Subrange-Ergebnis
        #
        # Beispiel:
        #
        #     function F: Word;
        #
        # Der Ausdruck wird intern als Integer berechnet, muss aber
        # vor dem Speichern gegen 0..65535 geprüft werden.
        # ----------------------------------------------------------
        return_range = self.subrange_info(
            declared_return_type
        )

        if return_range is not None:
            if self.scalar_base_type(
                resolved_expr_type
            ) != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=resolved_expr_type,
                    expected=declared_return_type
                )

            self.emit_subrange_check(
                ctx,
                declared_return_type,
                "eax"
            )

            expr_abi_type = "integer"

        # ----------------------------------------------------------
        # Pointer- oder Klassenresultat
        # ----------------------------------------------------------
        if return_type == "pointer":
            declared_is_class = (
                isinstance(declared_return_type, str)
                and declared_return_type in self.classes
            )

            expression_is_nil = (
                resolved_expr_type in (
                    "nil",
                    "^nil"
                )
            )

            if declared_is_class:
                expression_is_class = (
                    isinstance(resolved_expr_type, str)
                    and resolved_expr_type in self.classes
                )

                if not expression_is_nil:
                    if (
                        not expression_is_class
                        or not self.class_is_descendant(
                            resolved_expr_type,
                            declared_return_type
                        )
                    ):
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=resolved_expr_type,
                            expected=declared_return_type
                        )
            else:
                if not self.is_pointer_type(
                    resolved_expr_type,
                    include_nil=True
                ):
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=resolved_expr_type,
                        expected=declared_return_type
                    )

            expr_abi_type = "pointer"

        # Char kann ohne Konvertierung als Integer zurückgegeben werden.
        if (
            return_type == "integer"
            and expr_abi_type == "char"
        ):
            expr_abi_type = "integer"

        if return_type != expr_abi_type:
            raise CompileError(
                ctx,
                "E0005",
                got=resolved_expr_type,
                expected=declared_return_type
            )

        result_var = self.find_local_var(
            "Result"
        )

        if result_var is None:
            raise CompileError(
                ctx,
                "E0012",
                name="Result"
            )

        offset = result_var["offset"]

        if CDATA.args_target in (
            "dos",
            "dos16"
        ):
            if return_type in (
                "integer",
                "boolean",
                "char"
            ):
                self.backend.writer.emit_mov_mem16_base_disp_reg16(
                    "bp",
                    offset,
                    "ax"
                )
                return None

            if return_type == "string":
                # Bestehendes DOS-String-ABI beibehalten.
                self.backend.writer.emit_mov_mem16_base_disp_reg16(
                    "bp",
                    offset,
                    "dx"
                )

                self.backend.writer.emit_mov_reg16_imm16(
                    "ax",
                    0
                )

                self.backend.writer.emit_mov_mem16_base_disp_reg16(
                    "bp",
                    offset + 2,
                    "ax"
                )
                return None

            if return_type == "pointer":
                # DOS-Far-Pointer: AX = Offset, DX = Segment.
                self.backend.writer.emit_mov_mem16_base_disp_reg16(
                    "bp",
                    offset,
                    "ax"
                )

                self.backend.writer.emit_mov_mem16_base_disp_reg16(
                    "bp",
                    offset + 2,
                    "dx"
                )
                return None

            raise CompileError(
                ctx,
                "E0005",
                got=declared_return_type,
                expected="integer/string/pointer"
            )

        if CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        ):
            if return_type in (
                "integer",
                "boolean",
                "char",
                "string",
                "pointer"
            ):
                self.emit_mov_dword_ptr_store(
                    "ebp",
                    offset,
                    "eax"
                )
                return None

            if return_type == "double":
                self.emit_movsd_store(
                    "ebp",
                    offset,
                    "xmm0"
                )
                return None

            raise CompileError(
                ctx,
                "E0005",
                got=declared_return_type,
                expected=(
                    "integer/boolean/char/string/"
                    "double/pointer/subrange"
                )
            )

        # Win64
        if return_type in (
            "integer",
            "boolean",
            "char"
        ):
            self.emit_mov_dword_ptr_store(
                "rbp",
                offset,
                "eax"
            )
            return None

        if return_type in (
            "string",
            "pointer"
        ):
            self.emit_mov_qword_ptr_store(
                "rbp",
                offset,
                "rax"
            )
            return None

        if return_type == "double":
            self.emit_movsd_store(
                "rbp",
                offset,
                "xmm0"
            )
            return None

        raise CompileError(
            ctx,
            "E0005",
            got=declared_return_type,
            expected=(
                "integer/boolean/char/string/"
                "double/pointer/subrange"
            )
        )
        
    def emit_load_array_record_field(self, ctx, var_name, index_expr_ctx, field_parts):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
            
        field = self.resolve_array_record_field(
            ctx,
            var_name,
            index_expr_ctx,
            field_parts
        )

        path = var_name + "[...]." + ".".join(field_parts)

        if field.type == "integer":
            self.emit_mov_dword_ptr("eax", "r11", 0, comment=path)
            return "integer"

        if field.type == "double":
            self.emit_movsd_load("xmm0", "r11", 0, comment=path)
            return "double"

        if field.type == "string":
            self.emit_mov_qword_ptr("rax", "r11", 0, comment=path)
            return "string"

        return field.type

    def emit_store_array_record_field(self, ctx, var_name, index_expr_ctx, field_parts, expr_type):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
            
        # Wert sichern, bevor Index/Adresse berechnet wird
        if expr_type == "integer":
            self.emit_mov_dword_ptr_store("r12", "offsetof(JitContext, print_int_tmp)", "eax")

        elif expr_type == "double":
            self.emit_movsd_store("r12", "offsetof(JitContext, print_double_tmp)", "xmm0")

        else:
            raise CompileError(ctx, "E0005", got=expr_type, expected="integer/double")

        field = self.resolve_array_record_field(
            ctx,
            var_name,
            index_expr_ctx,
            field_parts
        )

        if field.type == "double" and expr_type == "integer":
            self.emit_mov_dword("eax", "r12", "print_int_tmp")
            self.emit_cvtsi2sd("xmm0", "eax")
            self.emit_movsd_store("r11", 0, "xmm0", comment=f"{var_name}[...].{'.'.join(field_parts)} :=")
            return

        if field.type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)

        if field.type == "integer":
            self.emit_mov_dword("eax", "r12", "print_int_tmp")
            self.emit_mov_dword_ptr_store("r11", 0, "eax", comment=f"{var_name}[...].{'.'.join(field_parts)} :=")
            return

        if field.type == "double":
            self.emit_movsd_load_field("xmm0", "r12", "print_double_tmp")
            self.emit_movsd_store("r11", 0, "xmm0", comment=f"{var_name}[...].{'.'.join(field_parts)} :=")
            return

        raise CompileError(ctx, "E0013", var_type=field.type)

    def emit_store_dynamic_array_element(self, ctx, name, index_ctx, value_ctx):
        arr = self.lookup_var(name)

        self.visit(index_ctx)                  # eax = index
        self.emit_mov("r10d", "eax")

        self.emit_load_var_value(name)         # rax = data pointer
        self.emit_test("rax", "rax")
        self.emit_jz("label_array_nil_error")

        # Bounds Check
        self.emit_mov("r11", "rax")
        self.emit_sub("r11", 16)      # Header
        self.emit_mov_reg_qword("r11", "r11")  # length
        self.emit_cmp("r10", "r11")
        self.emit_jae("label_error_array_bounds")

        self.visit(value_ctx)                  # eax = value

        self.emit_load_var_value(name)         # rax = data pointer
        self.emit_movsxd("r11", "r10d")
        self.emit_imul("r11", "r11", 4)
        self.emit_add("r11", "rax")
        self.emit_mov_dword_ptr_store("r11", 0, "eax")
    
    def emit_store_dynamic_array_record_field(self,
        ctx,
        var_name,
        index_exprs,
        field_parts,
        expr_type):
        
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]

        if len(index_exprs) != 1:
            raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

        var_info, array_info = self.get_array_info(ctx, var_name)

        record_type = array_info.element_type

        if record_type not in self.records:
            raise CompileError(ctx, "E0005", got=record_type, expected="record")

        # Wert sichern
        if expr_type == "integer":
            self.emit_mov_dword_ptr_store("r12", "offsetof(JitContext, print_int_tmp)", "eax")
        elif expr_type == "double":
            self.emit_movsd_store("r12", "offsetof(JitContext, print_double_tmp)", "xmm0")
        elif expr_type == "string":
            self.emit_push("rax")
        else:
            raise CompileError(ctx, "E0005", got=expr_type, expected="integer/double/string")

        # Index berechnen
        index_type = self.visit(index_exprs[0])

        if index_type != "integer":
            raise CompileError(ctx, "E0005", got=index_type, expected="integer")

        self.emit_mov("r10d", "eax", comment='dynamic record array index')

        # Datenpointer laden
        self.emit_load_var(var_name, var_info)  # RAX = data pointer

        # Elementadresse: data + index * record_size
        self.emit_movsxd("r11", "r10d")
        self.emit_imul("r11", "r11", array_info.element_size)
        self.emit_add("r11", "rax", comment="record element address")

        # Feldoffset berechnen
        current_type = record_type
        field = None
        field_offset = 0

        for field_name in field_parts:
            record = self.records[current_type]
            key = field_name.lower()

            if key not in record.fields:
                raise CompileError(ctx, "E0001", name=field_name)

            field = record.fields[key]
            field_offset += field.offset
            current_type = field.type

        if field is None:
            raise CompileError(ctx, "E0005", got="field", expected="record field")

        if field.type == "double" and expr_type == "integer":
            self.emit_mov_dword("eax", "r12", "print_int_tmp")
            self.emit_cvtsi2sd("xmm0", "eax")
            self.emit_movsd_store("r11", field_offset, "xmm0")
            return

        if field.type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)

        if field.type == "integer":
            self.emit_mov_dword("eax", "r12", "print_int_tmp")
            self.emit_mov_dword_ptr_store("r11", field_offset, "eax")
            return

        if field.type == "double":
            self.emit_movsd_load_field("xmm0", "r12", "print_double_tmp")
            self.emit_movsd_store("r11", field_offset, "xmm0")
            return

        if field.type == "string":
            self.emit_pop("rax")
            self.emit_mov_qword_ptr_store("r11", field_offset, "rax")
            return

        raise CompileError(ctx, "E0013", var_type=field.type)
    
    def emit_store_local_var(self, ctx, name, expr_type):
        var = self.find_local_var(name)

        if not var:
            raise CompileError(ctx, "E0012", name=name)

        typ    = self.resolve_type(var["type"])
        value_type = self.resolve_type(expr_type)
        offset = var["offset"]

        if typ == "integer":
            if self.scalar_base_type(value_type) != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected=typ
                )

            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_mov_dword_ptr_store(
                    "ebp",
                    offset,
                    "eax",
                    comment = f"local {name} :="
                )
            else:
                self.emit_mov_dword_ptr_store(
                    "rbp",
                    offset,
                    "eax",
                    comment = f"local {name} :="
                )

            return

        if typ == "boolean":
            if value_type not in ("boolean", "integer"):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected="boolean"
                )

            self.emit_and(
                "eax",
                1,
                comment=f"normalize local boolean {name}"
            )

            self.emit_mov_dword_ptr_store(
                "ebp" if CDATA.args_target in ("nt35", "winnt", "win32") else "rbp",
                offset,
                "eax",
                comment=f"local {name} :="
            )
            return

        if typ == "char":
            if value_type != "char":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected="char"
                )

            self.emit_mov_byte_ptr_store(
                "ebp" if CDATA.args_target in ("nt35", "winnt", "win32") else "rbp",
                offset,
                "al",
                comment=f"local {name} :="
            )
            return

        if typ == "string":
            if value_type not in ("string", "char"):
                raise CompileError(ctx, "E0005", got=value_type, expected=typ)

            if CDATA.args_target in ["dos", "dos16"]:
                # DOS-String-Literal liegt in DX.
                # Lokaler String als Far Pointer: offset + segment.
                self.backend.writer.emit_mov_mem16_base_disp_reg16("bp", offset, "dx")
                
                # Segment nicht verwenden, immer 0 setzen
                self.backend.writer.emit_mov_reg16_imm16("ax", 0)
                self.backend.writer.emit_mov_mem16_base_disp_reg16("bp", offset + 2, "ax")
                return

            if CDATA.args_target in ("nt35", "winnt", "win32"):
                self.emit_mov_dword_ptr_store(
                    "ebp",
                    offset,
                    "eax",
                    comment=f"local string {name} :="
                )
            else:
                self.emit_mov_qword_ptr_store(
                    "rbp",
                    offset,
                    "rax",
                    comment=f"local string {name} :="
                )

            return

        if self.is_pointer_type(typ, include_nil=False):
            if not self.pointer_assignment_compatible(
                value_type,
                typ
            ):
                raise CompileError(ctx, "E0005", got=value_type, expected=typ)

            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_mov_dword_ptr_store("ebp", offset, "eax", comment=f"local pointer {name} :=")
                return
            else:
                self.emit_mov_qword_ptr_store("rbp", offset, "rax", comment=f"local pointer {name} :=")
                return

        # Lokale Klassenvariable enthält einen Objektzeiger.
        if self.is_class_type(typ):
            if not self.class_assignment_compatible(
                value_type,
                typ
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected=typ
                )

            if CDATA.args_target in ("nt35", "winnt", "win32"):
                self.emit_mov_dword_ptr_store(
                    "ebp",
                    offset,
                    "eax",
                    comment=f"local object {name} :="
                )
            else:
                self.emit_mov_qword_ptr_store(
                    "rbp",
                    offset,
                    "rax",
                    comment=f"local object {name} :="
                )

            return

        raise CompileError(ctx, "E0011", typ=typ)
        
    def emit_call_rax(self):
        self.backend.emit_call("rax")
    
    def emit_load_var(self, name, info):
        typ  = self.resolve_type(info["type"])
        slot = info["slot"]
        
        if CDATA.args_target in ["dos", "dos16"]:
            var_type = self.resolve_type(info["type"])

            if var_type == "integer":
                symbol = info.get("symbol")

                if not symbol:
                    symbol = f"_var_{info['name']}"
                    info["symbol"] = symbol

                self.backend.emit_load_word_var("ax", symbol)
                return "integer"
            
            if isinstance(var_type, str) and var_type.startswith("^"):
                symbol = info.get("symbol")

                if not symbol:
                    symbol = f"_var_{info['name']}"
                    info["symbol"] = symbol

                self.backend.emit_load_far_pointer_var(symbol)
                return var_type
                
        elif CDATA.args_target in ["nt35", "winnt", "win32"]:
            if self.is_pointer_type(
                typ,
                include_nil=False
            ):
                symbol = info.get("symbol")

                if not symbol:
                    symbol = f"_var_{info['name']}"
                    info["symbol"] = symbol
                    if self.coff.find_symbol_index(symbol) is None:
                        self.coff.add_data_i32(
                            symbol,
                            0
                        )
                self.coff.emit_mov_reg_from_data_label32(
                    "eax",
                    symbol
                )
                return typ
                
            var_type = self.resolve_type(
                info["type"]
            )
            if var_type == "string":
                symbol = info.get("symbol")
                if not symbol:
                    symbol = f"_var_{info['name']}"
                    info["symbol"] = symbol
                    if self.coff.find_symbol_index(symbol) is None:
                        self.coff.add_data_i32(
                            symbol,
                            0
                        )
                self.backend.writer.emit_mov_reg_from_data_label32(
                    "eax",
                    symbol
                )
                return "string"

            if var_type == "integer":
                symbol = info.get("symbol")
                if not symbol:
                    symbol = f"_var_{info['name']}"
                    info["symbol"] = symbol
                    if self.coff.find_symbol_index(symbol) is None:
                        self.coff.add_data_i32(
                            symbol,
                            0
                        )
                self.backend.writer.emit_mov_reg_from_data_label32(
                    "eax",
                    symbol
                )
                return "integer"

            if var_type == "double":
                symbol = info.get("symbol")

                if not symbol:
                    symbol = f"_var_{info['name']}"
                    info["symbol"] = symbol

                    if self.coff.find_symbol_index(symbol) is None:
                        self.coff.add_data_double(
                            symbol,
                            0.0
                        )

                self.backend.writer.emit_movsd_xmm0_data_label32(
                    symbol
                )

                return "double"
                
        # -------------------------------------------------
        # Neues COFF-Backend:
        # direkte globale Variable per Symbol laden
        # -------------------------------------------------
        if hasattr(self, "coff") and "symbol" in info:
            symbol = info["symbol"]

            if typ == "integer":
                self.coff.emit_mov_r32_data_label("eax", symbol)
                return

            if typ == "double":
                self.coff.emit_movsd_data_label("xmm0", symbol)
                return

            if typ == "string":
                self.coff.emit_mov_r64_data_label("rax", symbol)
                return

            if self.is_pointer_type(
                typ,
                include_nil=False
            ):
                self.coff.emit_mov_r64_data_label("rax", symbol)
                return
        
        # -------------------------------------------------
        # Altes System über JitContext / r12
        # -------------------------------------------------
        if self.is_pointer_type(
            typ,
            include_nil=False
        ):
            self.emit_mov_qword("rax", "r12", "pointr_vars")
            self.emit_mov_qword_ptr("rax", "rax", slot * self.pointer_slot_size(), comment=f"{name}")
            return
        
        if isinstance(typ, str) and typ in self.classes:
            return self.emit_load_object_var(None, name, info)
        
        if isinstance(typ, str) and typ in self.arrays:
            array_info = self.arrays[typ]
            
            if getattr(array_info, "is_dynamic", False):
                self.emit_mov_qword("rax", "r12", "pointr_vars")
                self.emit_mov_qword_ptr("rax", "rax", slot * self.pointer_slot_size(), comment=f"dynamic array {name}")
                return
        
        if typ == "integer":
            self.emit_mov_qword("rax", "r12", "int_vars")
            self.emit_mov_dword_ptr("eax", "rax", slot * self.pointer_slot_size(), comment=f"{name}")
            return
        
        if typ == "double":
            self.emit_mov_qword("rax", "r12", "double_vars")
            self.emit_movsd_load("xmm0", "rax", slot * self.pointer_slot_size(), comment=f"{name}")
            return
        
        if typ == "string":
            self.emit_mov_qword("rax", "r12", "string_vars")
            self.emit_mov_qword_ptr("rax", "rax", slot * self.pointer_slot_size(), comment=f"{name}")
            return
        
        raise CompileError(None, "E0014", var_type=typ)
    
    def emit_load_dynamic_array_element(self, ctx, name, index_ctx):
        arr = self.lookup_var(name)

        self.visit(index_ctx)
        self.emit_mov("r10d", "eax")

        self.emit_load_var_value(name)         # rax = data pointer

        self.emit_movsxd("r11", "r10d")
        self.emit_imul("r11", "r11", 4)
        self.emit_add("r11", "rax")
        self.emit_mov_reg_dword("eax", "r11")

        return "integer"
    
    def emit_load_dynamic_array_record_field(self,
        ctx,
        var_name,
        index_exprs,
        field_parts):
        
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]

        if len(index_exprs) != 1:
            raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

        var_info, array_info = self.get_array_info(ctx, var_name)

        record_type = array_info.element_type

        if record_type not in self.records:
            raise CompileError(ctx, "E0005", got=record_type, expected="record")

        index_type = self.visit(index_exprs[0])

        if index_type != "integer":
            raise CompileError(ctx, "E0005", got=index_type, expected="integer")

        self.emit_mov("r10d", "eax", comment='dynamic record array index')

        self.emit_load_var(var_name, var_info)  # RAX = data pointer

        self.emit_movsxd("r11", "r10d")
        self.emit_imul("r11", "r11", array_info.element_size)
        self.emit_add("r11", "rax", comment="record element address")

        current_type = record_type
        field = None
        field_offset = 0

        for field_name in field_parts:
            record = self.records[current_type]
            key = field_name.lower()

            if key not in record.fields:
                raise CompileError(ctx, "E0001", name=field_name)

            field = record.fields[key]
            field_offset += field.offset
            current_type = field.type

        if field.type == "integer":
            self.emit_mov_dword_ptr("eax", "r11", field_offset)
            return "integer"

        if field.type == "double":
            self.emit_movsd_load("xmm0", "r11", field_offset)
            return "double"

        if field.type == "string":
            self.emit_mov_qword_ptr("rax", "r11", field_offset)
            return "string"

        raise CompileError(ctx, "E0014", var_type=field.type)
    
    def emit_store_var(self, ctx, name, info):
        typ  = self.resolve_type(info["type"])
        slot = info["slot"]

        # Deklarierter Typ muss erhalten bleiben, z. B. "byte".
        # info["type"] kann für Rechenoperationen bereits "integer" sein.
        declared_type = info.get(
            "declared_type",
            info["type"]
        )

        range_info = self.subrange_info(
            declared_type
        )

        if range_info is not None:
            if typ != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=typ,
                    expected="integer subrange"
                )

            # EAX enthält zu diesem Zeitpunkt den zu speichernden Integerwert.
            # Bei normalen Typen macht emit_subrange_check() nichts.
            self.emit_subrange_check(
                ctx,
                declared_type,
                "eax"
            )

        if CDATA.args_target in ["nt35", "winnt", "win32"] and typ == "string":
            symbol = info.get("symbol")
            if not symbol:
                symbol = f"_var_{info['name']}"
                info["symbol"] = symbol

                if self.coff.find_symbol_index(symbol) is None:
                    self.coff.add_data_i32(symbol, 0)

            self.coff.emit_mov_data_label_r32(
                symbol,
                "eax"
            )
            return
    
        if hasattr(self, "coff") and "symbol" in info:
            symbol = info["symbol"]

            if typ == "integer":
                self.coff.emit_mov_data_label_r32(symbol, "eax")
                return

            if typ == "double":
                self.coff.emit_movsd_data_label_xmm0_store(symbol)
                return

            if typ == "string":
                self.coff.emit_mov_data_label_r64(symbol, "rax")
                return

            if self.is_pointer_type(
                typ,
                include_nil=False
            ):
                if CDATA.args_target in ["winnt", "nt35", "win32"]:
                    self.coff.emit_mov_data_label_r32(symbol, "eax")
                else:
                    self.coff.emit_mov_data_label_r64(symbol, "rax")
                return

        if self.is_pointer_type(
            typ,
            include_nil=False
        ):
            if hasattr(self, "coff") and CDATA.args_target in ["winnt", "nt35", "win32"]:
                symbol = info.get("symbol")
                if not symbol:
                    symbol = f"_var_{info['name']}"
                    info["symbol"] = symbol
                    if self.coff.find_symbol_index(symbol) is None:
                        self.coff.add_data_i32(symbol, 0)

                self.coff.emit_mov_data_label_r32(symbol, "eax")
                return

            self.emit_mov_qword("r11", "r12", "pointr_vars")
            self.emit_mov_qword_ptr_store("r11", slot * self.pointer_slot_size(), "rax", comment=f"{name}")
            return

        if isinstance(typ, str) and typ in self.arrays:
            array_info = self.arrays[typ]
            
            if getattr(array_info, "is_dynamic", False):
                self.emit_mov_qword("r11", "r12", "pointr_vars")
                self.emit_mov_qword_ptr_store("r11", slot * self.pointer_slot_size(), "rax", comment=f"dynamic array {name}")
                return
                
        if typ == "integer":
            if CDATA.args_backend in ["exefile"]:
                if CDATA.args_target in ["dos", "dos16"]:
                    var_type = self.resolve_type(info["type"])

                    if var_type == "integer":
                        symbol = info.get("symbol")

                        if not symbol:
                            symbol = f"_var_{info['name']}"
                            info["symbol"] = symbol

                        self.backend.emit_store_word_var(symbol, "ax")
                        return
                        
                    if isinstance(var_type, str) and var_type.startswith("^"):
                        symbol = info.get("symbol")
                        
                        if not symbol:
                            symbol = f"_var_{info['name']}"
                            info["symbol"] = symbol
                        
                        self.backend.emit_store_word_var(symbol, "ax")
                        return
            
            self.emit_mov("ebx", "eax")
            self.emit_mov_qword("rax", "r12", "int_vars")
            self.emit_mov_dword_ptr_store("rax", slot * self.pointer_slot_size(), "ebx", comment=f"{name}")
            return

        if typ == "double":
            self.emit_mov_qword("r11", "r12", "double_vars")
            self.emit_movsd_store("r11", slot * self.pointer_slot_size(), "xmm0", comment=f"{name}")
            return

        if typ == "string":
            self.emit_mov_qword("r11", "r12", "string_vars")
            self.emit_mov_qword_ptr_store("r11", slot * self.pointer_slot_size(), "rax", comment=f"{name}")
            return

        raise CompileError(ctx, "E0013", var_type=typ)
    
    def emit_procedure_declaration(self, ctx):
        proc_name = ctx.IDENT().getText()

        end_label = self.new_named_label(
            f"endproc_{proc_name}"
        )

        self.emit_jmp(end_label)
        self.emit_bind_label(proc_name)

        self.emit_push("rbp")
        self.emit_mov("rbp", "rsp")
        self.emit_sub("rsp", 256, comment="local variables")

        self.push_local_scope()

        # lokale var-Deklarationen einsammeln
        for child in ctx.children:
            cname = type(child).__name__

            if "VarSectionContext" in cname:
                self.visit(child)

        # eigentlichen Procedure-Block erzeugen
        block = ctx.block()
        if block:
            self.visit(block)

        self.pop_local_scope()

        self.emit_mov("rsp", "rbp")
        self.emit_pop("rbp")
        self.emit_ret()

        self.emit_bind_label(end_label)
    
    def emit_function_declaration(self, ctx, name, return_type):
        key    = name.lower()
        scoped = self.scoped_name(name)

        if scoped.lower() in self.functions:
            fkey = scoped.lower()
        elif key in self.functions:
            fkey = key
        else:
            raise CompileError(ctx, "E0001", name=name)

        label      = self.functions[key]["label"]
        exit_label = self.new_named_label("exitfunc_" + name)
        skip_label = self.new_named_label("skipfunc_" + name)

        self.functions[fkey]["label"] = label

        params = self.collect_formal_params(ctx)
        self.functions[scoped.lower()]["params"] = params

        param_regs = ["rcx", "rdx", "r8", "r9"]

        if len(params) > len(param_regs):
            raise CompileError(
                ctx,
                "E0005",
                got="too many params",
                expected="max 4 params"
            )

        declared_rt = self.resolve_type(
            return_type
        )

        rt = self.function_abi_return_type(
            declared_rt
        )

        if rt not in (
            "integer",
            "boolean",
            "char",
            "string",
            "double",
            "pointer"
        ):
            raise CompileError(
                ctx,
                "E0005",
                got=declared_rt,
                expected=(
                    "integer/boolean/char/string/"
                    "double/pointer/subrange"
                )
            )

        # Die Funktionsdefinition im normalen Programmfluss überspringen.
        # Dieses Ziel darf nicht zugleich das Ziel von Pascal Exit sein:
        # Exit muss zuerst Rückgabewert und Stack-Epilog durchlaufen.
        self.emit_jmp(skip_label)
        self.emit_bind_label(label)

        # -------------------------------------------------
        # Prolog
        # -------------------------------------------------
        if CDATA.args_target in ["dos", "dos16"]:
            self.backend.writer.emit_push_reg16("bp")
            self.backend.writer.emit_mov_reg16_reg16("bp", "sp")
        elif CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_push("ebp", comment="function prolog")
            self.emit_mov("ebp", "esp", comment="stack frame")
            self.emit_push("ebx", comment="preserve EBX")
        else:
            self.emit_push("rbp", comment="function prolog")
            self.emit_mov("rbp", "rsp", comment="stack frame")
            self.emit_push("rbx", comment="preserve RBX")

        old_params   = self.current_proc_params
        old_function = self.current_function

        self.current_proc_params = {}
        self.current_function = {
            "name": name,

            # Pascal-Typ, zum Beispiel Word oder PAnsiChar.
            "return_type": declared_rt,

            # Physischer ABI-Typ, zum Beispiel integer oder pointer.
            "abi_return_type": rt,

            "scoped_name": scoped
        }

        # -------------------------------------------------
        # Lokalen Scope zuerst anlegen
        # -------------------------------------------------
        self.scope_stack.append(name)
        self.push_local_scope()
        self.push_const_scope()

        # Result als echte lokale Variable. Subranges und Char verwenden
        # einen 32-Bit-Slot, damit NT32-Store und EAX-Rückgabe sicher sind.
        result_storage_type = self.function_result_storage_type(
            declared_rt
        )

        self.declare_local_var(
            ctx,
            "Result",
            result_storage_type
        )

        result_var = self.find_local_var("Result")
        result_off = result_var["offset"]

        # -------------------------------------------------
        # Lokale Deklarationen der Funktion einsammeln.
        # -------------------------------------------------
        nested_declarations = []

        for declaration in ctx.declarationPart():
            if declaration is None:
                continue

            var_section = declaration.varSection()

            if var_section is not None:
                self.visitVarSection(
                    var_section
                )
                continue

            const_section = declaration.constSection()

            if const_section is not None:
                self.visitConstSection(
                    const_section
                )
                continue

            type_section = declaration.typeSection()

            if type_section is not None:
                self.visitTypeSection(
                    type_section
                )
                continue

            procedure_declaration = (
                declaration.procedureDeclaration()
                if hasattr(
                    declaration,
                    "procedureDeclaration"
                )
                else None
            )

            if procedure_declaration is not None:
                nested_declarations.append(
                    procedure_declaration
                )
                continue

            function_declaration = (
                declaration.functionDeclaration()
                if hasattr(
                    declaration,
                    "functionDeclaration"
                )
                else None
            )

            if function_declaration is not None:
                nested_declarations.append(
                    function_declaration
                )
                continue

        scope = self.current_local_scope()

        local_size = scope["next_offset"]
        local_size = (local_size + 15) & ~15

        if local_size:
            if CDATA.args_target in ["dos", "dos16"]:
                self.emit_sub(
                    "sp",
                    local_size,
                    comment=f"{local_size} bytes locals"
                )
            elif CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_sub(
                    "esp",
                    local_size,
                    comment=f"{local_size} bytes locals"
                )
            else:
                self.emit_sub(
                    "rsp",
                    local_size,
                    comment=f"{local_size} bytes locals"
                )

        # -------------------------------------------------
        # Parameter sichern / Offsets eintragen
        # -------------------------------------------------
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            stack_offset = 8

            for p in params:
                pname = p["name"]

                param_info = {
                    "type": p["type"],
                    "reg": None,
                    "stack_offset": stack_offset,
                    "is_var": p.get("is_var", False),
                    "is_const": p.get("is_const", False),
                    "is_open_array": p.get("is_open_array", False),
                    "element_type": p.get("element_type")
                }

                if param_info["is_open_array"]:
                    param_info["high_offset"] = stack_offset + 4
                    stack_offset += 8
                else:
                    stack_offset += 4

                self.current_proc_params[
                    pname.lower()
                ] = param_info

        elif CDATA.args_target in ["dos", "dos16"]:
            for index, p in enumerate(params):
                pname = p["name"]

                self.current_proc_params[pname.lower()] = {
                    "type": p["type"],
                    "reg": None,
                    "stack_offset": 4 + index * 2,
                    "is_var": p.get("is_var", False),
                    "is_const": p.get("is_const", False),
                    "is_open_array": p.get("is_open_array", False),
                    "element_type": p.get("element_type")
                }
        else:
            for index, p in enumerate(params):
                reg   = param_regs[index]
                pname = p["name"]

                self.emit_push(
                    reg,
                    comment=f"save function param {pname}"
                )

                self.current_proc_params[pname.lower()] = {
                    "type": p["type"],
                    "reg": reg,
                    "stack_offset": -8 * (index + 2),
                    "is_var": p.get("is_var", False),
                    "is_const": p.get("is_const", False),
                    "is_open_array": p.get("is_open_array", False),
                    "element_type": p.get("element_type")
                }

            if len(params) % 2 == 0:
                self.emit_sub(
                    "rsp",
                    8,
                    comment="align stack in function"
                )

        # Verschachtelte Funktionen und Prozeduren erzeugen.
        for declaration in nested_declarations:
            self.visit(
                declaration
            )
        # -------------------------------------------------
        # Nur den ausführbaren Funktionskörper besuchen.
        # -------------------------------------------------
        self.exit_label_stack.append(exit_label)

        try:
            block_ctx = ctx.block()

            if block_ctx is not None:
                statement_list = block_ctx.statementList()

                if statement_list is not None:
                    self.visit(statement_list)

        finally:
            self.exit_label_stack.pop()

        self.pop_const_scope()
        self.pop_local_scope()
        self.scope_stack.pop()

        self.current_function = old_function
        self.current_proc_params = old_params

        # Gemeinsames Ziel für das normale Funktionsende und Pascal Exit.
        # Ab hier wird Result geladen und anschließend der korrekte
        # zielabhängige Stack-Epilog ausgeführt.
        self.emit_bind_label(exit_label)

        # -------------------------------------------------
        # Return-Wert laden
        # -------------------------------------------------
        if CDATA.args_target in ["dos", "dos16"]:
            if rt == "string":
                self.backend.writer.emit_mov_reg16_mem16_base_disp(
                    "dx",
                    "bp",
                    result_off
                )
                self.backend.writer.emit_mov_reg16_mem16_base_disp(
                    "ax",
                    "bp",
                    result_off + 2
                )
            elif rt in (
                "integer",
                "boolean",
                "char"
            ):
                self.backend.writer.emit_mov_reg16_mem16_base_disp(
                    "ax",
                    "bp",
                    result_off
                )
            elif rt == "pointer":
                self.backend.writer.emit_mov_reg16_mem16_base_disp(
                    "ax",
                    "bp",
                    result_off
                )
                self.backend.writer.emit_mov_reg16_mem16_base_disp(
                    "dx",
                    "bp",
                    result_off + 2
                )
            else:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=declared_rt,
                    expected="integer/string/pointer"
                )

            self.backend.writer.emit_mov_reg16_reg16("sp", "bp")
            self.backend.writer.emit_pop_reg16("bp")
            self.backend.writer.emit_ret()

            self.emit_bind_label(skip_label)
            return

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            if rt in (
                "integer",
                "boolean",
                "char",
                "string",
                "pointer"
            ):
                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    result_off,
                    comment=f"{name} result"
                )
            elif rt == "double":
                self.emit_movsd_load(
                    "xmm0",
                    "ebp",
                    result_off,
                    comment=f"{name} result"
                )
            else:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=declared_rt,
                    expected=(
                        "integer/boolean/char/string/"
                        "double/pointer/subrange"
                    )
                )

            self.emit_mov("esp", "ebp")
            self.emit_pop("ebp")
            #self.emit_ret() ### hier
            
            convention = self.routine_calling_convention(
                self.functions[fkey]
            )

            stack_bytes = self.nt32_parameter_stack_bytes(
                params
            )

            if convention in ("stdcall", "pascal") and stack_bytes:
                self.writer.emit_ret_imm16(stack_bytes)
            else:
                self.emit_ret()

            self.emit_bind_label(skip_label)
            return

        if rt in (
            "string",
            "pointer"
        ):
            self.emit_mov_qword_ptr(
                "rax",
                "rbp",
                result_off
            )
        elif rt in (
            "integer",
            "boolean",
            "char"
        ):
            self.emit_mov_dword_ptr(
                "eax",
                "rbp",
                result_off
            )
        elif rt == "double":
            self.emit_movsd_load(
                "xmm0",
                "rbp",
                result_off
            )
        else:
            raise CompileError(
                ctx,
                "E0005",
                got=declared_rt,
                expected=(
                    "integer/boolean/char/string/"
                    "double/pointer/subrange"
                )
            )

        self.emit_mov("rsp", "rbp")
        self.emit_pop("rbp")
        self.emit_ret()

        self.emit_bind_label(skip_label)
    
    def emit_try_except_statement(self, ctx):
        except_label = self.new_named_label("except")
        end_label    = self.new_named_label("endtry")

        frame_size = 512

        # ExceptionFrame auf Stack reservieren
        self.emit_sub("esp", frame_size, comment="exception frame")
        self.emit_mov("ebx", "esp", comment="frame ptr")

        # _jit_push_exception(frame)
        self.emit_push("ebx")
        self.emit_call("_jit_exception_push")
        self.backend.emit_cleanup_stack(4)

        # setjmp(frame->env)
        # frame beginnt direkt mit jmp_buf/env
        self.emit_push("ebx")
        self.emit_call("_jit_setjmp")
        self.backend.emit_cleanup_stack(4)

        # setjmp == 0 -> try block
        # setjmp != 0 -> except block
        self.emit_cmp("eax", 0)
        self.emit_jne(except_label)

        # TRY-Block
        self.visit(ctx.statementList(0))

        # Kein Fehler: ExceptionFrame entfernen
        self.emit_push("ebx")
        self.emit_call("_jit_exception_pop")
        self.backend.emit_cleanup_stack(4)

        self.emit_add("esp", frame_size, comment="free exception frame")
        self.emit_jmp(end_label)

        # EXCEPT-Block
        self.emit_bind_label(except_label)

        # Nach longjmp ist esp wieder korrekt im setjmp-Kontext,
        # EBX aber nicht garantiert. Frame liegt wieder bei ESP.
        self.emit_mov("ebx", "esp", comment="restore frame ptr")

        self.emit_push("ebx")
        self.emit_call("_jit_exception_pop")
        self.backend.emit_cleanup_stack(4)

        self.visit(ctx.statementList(1))

        self.emit_add("esp", frame_size, comment="free exception frame")
        self.emit_bind_label(end_label)
        
        if (self.coff.find_symbol_index("ctx") is not None):
            self.writer.emit_lea_reg_data_label(
                "esi",
                "ctx"
            )
        
        return None
    
    def emit_self_method_call(
        self,
        ctx,
        method_name,
        actual_types=None
    ):
        if actual_types is None:
            actual_types = []

        if self.current_class is None:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"{method_name} cannot be called through "
                    "Self outside a class method"
                )
            )

        method, owner_cls = self.find_class_method_recursive(
            ctx,
            self.current_class,
            method_name,
            actual_types
        )

        if method.kind not in ("function", "constructor"):
            raise CompileError(
                ctx,
                "E0019",
                text=f"{method_name} is not a function"
            )

        # ----------------------------------------------------------
        # NT32
        #
        # Im Klassenmethoden-Prolog wird Self unter [ebp-4]
        # gespeichert.
        # ----------------------------------------------------------
        if CDATA.args_target in ("nt35", "winnt", "win32"):
            self.emit_mov_dword_ptr("eax", "ebp", -4, comment="load Self")

            # cdecl-Klassenmethoden erwarten Self als ersten
            # Stackparameter.
            self.emit_push("eax", comment=f"Self for {method.name}")

            # Unterstützt:
            # - lokale Labels,
            # - PUI-Symbole/Methoden
            # - virtuelle Methoden über VMT
            self.emit_class_method_call(
                method,
                comment=(
                    f"{owner_cls.name}."
                    f"{method.name}"
                )
            )

            self.backend.emit_cleanup_stack(4)

            # Laufzeitaufrufe oder fremde Units können ESI verändern.
            if self.coff.find_symbol_index("ctx") is not None:
                self.writer.emit_lea_reg_data_label(
                    "esi",
                    "ctx"
                )

            return self.resolve_type(
                method.return_type
            )

        # ----------------------------------------------------------
        # Win64
        # ----------------------------------------------------------
        else:
            self.emit_mov_qword_ptr(
                "rcx",
                "rbp",
                -8,
                comment="load Self"
            )

            self.emit_sub(
                "rsp",
                32,
                comment="method shadow space"
            )

            self.emit_class_method_direct_call(
                method,
                comment=(
                    f"{owner_cls.name}."
                    f"{method.name}"
                )
            )

            self.emit_add(
                "rsp",
                32,
                comment="remove method shadow space"
            )

            return self.resolve_type(
                method.return_type
            )
    
    def emit_init_array_var(self, ctx, name, info):
        array_type = info["type"]

        if array_type not in self.arrays:
            return

        array_info = self.arrays[array_type]

        if not array_info.init_values:
            return

        base_offset = info["slot"]

        self.emit_mov_qword("r11", "r12", "arrays_vars")

        for index, value in enumerate(array_info.init_values):
            offset = base_offset + index * array_info.element_size

            if array_info.element_type == "integer":
                if CDATA.args_target in ["nt35", "winnt", "win32"]:
                    self.emit_mov("eax", value)
                    self.emit_mov_dword_ptr_store(
                        "r11",
                        offset,
                        "eax",
                        comment=f"init {name}[{index + array_info.index_min}]"
                    )
                    
                else:
                    self.emit_mov_dword_ptr_store("r11", offset, value, comment=f"init {name}[{index + array_info.index_min}]")

            elif array_info.element_type == "double":
                self.emit_mov_imm("rax", double_to_bits(float(value)))
                self.emit_movq("xmm0", "rax")
                self.emit_movsd_store("r11", offset, "xmm0", comment=f"init {name}[{index + array_info.index_min}]")

            elif array_info.element_type == "string":
                label = self.add_string_literal(value)
                self.emit_mov_imm("rax", label)
                self.emit_mov_qword_ptr_store("r11", offset, "rax", comment=f"init {name}[{index + array_info.index_min}]")
                
    def emit_if_statement(self, ctx):
        else_name = self.new_named_label("else")
        end_name  = self.new_named_label("endif")

        self.emit_condition_jump_false(ctx.condition(), else_name)

        self.visit(ctx.statement(0))

        if ctx.ELSE():
            self.emit_jmp(end_name)
            self.emit_bind_label(else_name)
            self.visit(ctx.statement(1))
            self.emit_bind_label(end_name)
        else:
            self.emit_bind_label(else_name)
        
    def emit_int_to_double(self):
        self.emit_cvtsi2sd("xmm0", "eax")
    
    def emit_condition_jump_false(self, ctx, false_label):
        # Boolean-Ausdruck ohne Vergleich:
        # if a and not b then
        if ctx.compareOp() is None:
            expr_type = self.visit(ctx.expr(0))

            if expr_type not in ("integer", "boolean"):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=expr_type,
                    expected="boolean/integer 6"
                )

            self.normalize_bool_eax()
            self.emit_cmp("eax", 0)
            self.emit_je(false_label)
            return

        left_ctx  = ctx.expr(0)
        right_ctx = ctx.expr(1)
        op        = ctx.compareOp().getText()

        left_type = self.visit(left_ctx)
        
        if isinstance(left_type, str) and left_type.startswith("^"):
            is_nt32 = CDATA.args_target in ["nt35", "winnt", "win32"]

            REG_A = "eax" if is_nt32 else "rax"
            REG_B = "ebx" if is_nt32 else "rbx"

            self.emit_push(REG_A, comment="save left pointer")

            right_type = self.visit(right_ctx)

            if right_type != left_type and right_type != "^nil":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=right_type,
                    expected=left_type + "/nil"
                )

            self.emit_mov(REG_B, REG_A, comment="right pointer")
            self.emit_pop(REG_A, comment="left pointer")
            self.emit_cmp(REG_A, REG_B)

            if op == "=":
                self.emit_jne(false_label)
                return

            if op == "<>":
                self.emit_je(false_label)
                return

            raise CompileError(ctx, "E0005", got=op, expected="= or <>")

        if left_type == "boolean":
            self.normalize_bool_eax()
            self.emit_push("eax")

            right_type = self.visit(right_ctx)

            if right_type not in ("boolean", "integer"):
                raise CompileError(ctx, "E0005", got=right_type, expected="boolean")

            self.normalize_bool_eax()

            self.emit_mov("ebx", "eax")
            self.emit_pop("eax")
            self.emit_cmp("eax", "ebx")

            if op == "=":
                self.emit_jne(false_label)
                return

            if op == "<>":
                self.emit_je(false_label)
                return

            raise CompileError(ctx, "E0005", got=op, expected="= or <>")
            
        elif left_type == "integer":
            self.emit_push("rax")
            
        elif left_type == "double":
            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")
            
        else:
            raise CompileError(ctx, "E0005", got=left_type, expected="integer/double")

        right_type = self.visit(right_ctx)

        if left_type == "double" or right_type == "double":
            if right_type == "integer":
                self.emit_cvtsi2sd("xmm0", "eax")
            elif right_type != "double":
                raise CompileError(ctx, "E0005", got=right_type, expected="integer/double")

            self.emit_movapd("xmm1", "xmm0")

            if left_type == "integer":
                self.emit_pop("rax")
                self.emit_cvtsi2sd("xmm0", "eax")
            else:
                self.emit_movsd_load("xmm0", "rsp")
                self.emit_add("rsp", 8)

            self.emit_ucomisd("xmm0", "xmm1")

            jump_map = {
                "=":  self.emit_jne,
                "<>": self.emit_je,
                "<":  self.emit_jae,
                "<=": self.emit_ja,
                ">":  self.emit_jbe,
                ">=": self.emit_jb,
            }

            jump_map[op](false_label)
            return

        self.emit_mov("ebx", "eax")
        self.emit_pop("rax")
        self.emit_cmp("eax", "ebx")

        jump_map = {
            "=":  self.emit_jne,
            "<>": self.emit_je,
            "<":  self.emit_jge,
            "<=": self.emit_jg,
            ">":  self.emit_jle,
            ">=": self.emit_jl,
        }

        jump_map[op](false_label)
    
    def emit_expr_as_double(self, ctx):
        expr_type = self.visit(ctx)

        if expr_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")

        elif expr_type != "double":
            raise CompileError(ctx, "E0005", got=expr_type, expected="double")

        return "double"

    def emit_while_statement(self, ctx):
        start_name = self.new_named_label("while")
        end_name   = self.new_named_label("endwhile")

        self.emit_bind_label(start_name)
        self.emit_condition_jump_false(ctx.condition(), end_name)

        self.visit(ctx.statement())

        self.emit_jmp(start_name)
        self.emit_bind_label(end_name)
    
    def require_var(self, ctx, name):
        key = name.lower()
        
        if key not in self.vars:
            raise CompileError(ctx, "E0003", name=key)  # Variable not declared
        
        return self.vars[key]
    
    def emit_repeat_statement(self, ctx):
        start_name = self.new_named_label("repeat")
        end_name   = self.new_named_label("endrepeat")

        self.emit_bind_label(start_name)

        for stmt in ctx.statementList().statement():
            self.visit(stmt)

        self.emit_condition_jump_false(ctx.condition(), start_name)

        self.emit_bind_label(end_name)
    
    def emit_for_statement(self, ctx):
        var_name = ctx.IDENT().getText()

        # ------------------------------------------------------------
        # Schleifenvariable suchen:
        # zuerst lokal, danach global
        # ------------------------------------------------------------
        info = self.find_local_var(var_name)
        is_local = info is not None

        if info is None:
            key = var_name.lower()

            if key not in self.vars:
                raise CompileError(
                    ctx,
                    "E0001",
                    name=var_name
                )

            info = self.vars[key]

        var_type = self.resolve_type(
            info["type"]
        )

        if var_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=var_type,
                expected="integer"
            )

        target = CDATA.args_target.lower()

        start_name = self.new_named_label(
            "for"
        )

        continue_name = self.new_named_label(
            "for_continue"
        )

        end_name = self.new_named_label(
            "endfor"
        )

        # ------------------------------------------------------------
        # Hilfsfunktionen für lokale/globale Schleifenvariable
        # ------------------------------------------------------------
        def load_for_variable():
            if is_local:
                return self.emit_load_local_var(
                    ctx,
                    var_name,
                    info
                )

            return self.emit_load_var(
                var_name,
                info
            )

        def store_for_variable():
            if is_local:
                return self.emit_store_local_var(
                    ctx,
                    var_name,
                    "integer"
                )

            return self.emit_store_var(
                ctx,
                var_name,
                info
            )

        # ------------------------------------------------------------
        # Startwert:
        #
        # for I := start ...
        # ------------------------------------------------------------
        start_type = self.visit(
            ctx.expr(0)
        )

        if start_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=start_type,
                expected="integer"
            )

        store_for_variable()

        # ------------------------------------------------------------
        # Endwert nur einmal auswerten
        # ------------------------------------------------------------
        end_type = self.visit(
            ctx.expr(1)
        )

        if end_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=end_type,
                expected="integer"
            )

        # ------------------------------------------------------------
        # Endwert sichern
        # ------------------------------------------------------------
        if target in ["dos", "dos16"]:
            # Erwartet, dass das Backend den aktuellen AX-Wert
            # als FOR-Endwert sichert.
            self.backend.emit_store_for_end_ax()

        elif target in ["winnt", "nt35", "win32"]:
            if self.coff.find_symbol_index(
                "__for_end_tmp"
            ) is None:
                self.coff.add_data_i32(
                    "__for_end_tmp",
                    0
                )

            self.coff.emit_mov_data_label_r32(
                "__for_end_tmp",
                "eax"
            )

        else:
            self.emit_mov_dword_ptr_store(
                "r12",
                JIT_CONTEXT_OFFSETS["print_int_tmp"],
                "eax",
                comment="for end value"
            )

        # ------------------------------------------------------------
        # Schleifenanfang
        # ------------------------------------------------------------
        self.emit_bind_label(
            start_name
        )

        load_for_variable()

        # Grammar:
        #
        # FOR IDENT ASSIGN expr (TO | DOWNTO) expr DO statement
        #
        # Der Richtungsoperator liegt bei dir aktuell an Child 4.
        # ------------------------------------------------------------
        direction = (
            ctx.getChild(4)
            .getText()
            .lower()
        )

        if direction not in ("to", "downto"):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "invalid for-loop direction: "
                    + direction
                )
            )

        # ------------------------------------------------------------
        # Schleifenbedingung prüfen
        # ------------------------------------------------------------
        if target in ["dos", "dos16"]:
            self.backend.emit_load_for_end_bx()
            self.emit_cmp(
                "eax",
                "ebx"
            )

            if direction == "to":
                self.emit_jg(end_name)
            else:
                self.emit_jl(end_name)

        elif target in ["winnt", "nt35", "win32"]:
            self.coff.emit_mov_reg_from_data_label32(
                "ebx",
                "__for_end_tmp"
            )

            self.emit_cmp(
                "eax",
                "ebx"
            )

            if direction == "to":
                self.emit_jg(end_name)
            else:
                self.emit_jl(end_name)

        else:
            self.emit_cmp_dword(
                "eax",
                "r12",
                "_print_int_tmp"
            )

            if direction == "to":
                self.emit_jg(end_name)
            else:
                self.emit_jl(end_name)

        # ------------------------------------------------------------
        # BREAK und CONTINUE für den Schleifenrumpf
        # ------------------------------------------------------------
        self.break_label_stack.append(end_name)
        self.continue_label_stack.append(continue_name)

        try:
            self.visit(ctx.statement())
        finally:
            self.continue_label_stack.pop()
            self.break_label_stack.pop()

        # ------------------------------------------------------------
        # CONTINUE springt hierher, damit die Schleifenvariable
        # trotzdem erhöht beziehungsweise verringert wird.
        # ------------------------------------------------------------
        self.emit_bind_label(
            continue_name
        )

        load_for_variable()

        if direction == "to":
            self.emit_add(
                "eax",
                1,
                comment="increment for variable"
            )
        else:
            self.emit_sub(
                "eax",
                1,
                comment="decrement for variable"
            )

        store_for_variable()

        self.emit_jmp(start_name)
        self.emit_bind_label(end_name)
    
    # typen überprüfung ...
    def var_info(self, ctx, name):
        key = name.lower()
        
        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=name)
        
        return self.vars[key]
        
    def var_type_of(self, ctx, name):
        return self.var_info(ctx, name)["type"]
    
    def variable_ref_has_dot(self, ref):
        return any(
            self.suffix_is_dot(s)
            for s in ref.variableSuffix()
        )
    
    def variable_ref_has_index(self, ref):
        return any(
            self.suffix_is_index(s)
            for s in ref.variableSuffix()
        )
    
    def slot_for(self, ctx, name):
        return self.var_info(ctx, name)["slot"]
    
    def emit(self, line):
        self.backend.emit(line)
    
    def emit_add(self, reg, value, comment=""):
        self.backend.emit_add(reg, value, comment)

    def emit_imul(self, dst, src, value=None, comment=""):
        self.backend.emit_imul(dst, src, value, comment)
    
    def emit_bind_label(self, label, comment=""):
        self.backend.emit_bind_label(label, comment)

    def emit_new_label_decl(self, name, comment=""):
        self.backend.emit_new_label_decl(name, comment)
    
    def emit_call(self, dst, comment=""):
        self.backend.emit_call(dst, comment)

    def emit_cmp(self, reg, value, comment=""):
        self.backend.emit_cmp(reg, value, comment)

    def emit_cmp_dword(self, reg, base, field, comment=""):
        self.backend.emit_cmp_dword(reg, base, field, comment)

    def emit_dec(self, reg, comment=""): self.backend.emit_dec(reg, comment)

    def emit_jg(self, label, comment=""): self.backend.emit_jg(label, comment)
    def emit_jl(self, label, comment=""): self.backend.emit_jl(label, comment)
    def emit_jz(self, label, comment=""): self.backend.emit_jz(label, comment)
    def emit_jb(self, label, comment=""): self.backend.emit_jb(label, comment)
    def emit_ja(self, label, comment=""): self.backend.emit_ja(label, comment)
    def emit_jae(self, label, comment=""): self.backend.emit_jae(label, comment)
    def emit_jbe(self, label, comment=""): self.backend.emit_jbe(label, comment)
    def emit_je(self, label, comment=""): self.backend.emit_je(label, comment)
    def emit_jle(self, label, comment=""): self.backend.emit_jle(label, comment)
    def emit_jge(self, label, comment=""): self.backend.emit_jge(label, comment)
    def emit_jne(self, label, comment=""): self.backend.emit_jne(label, comment)
    def emit_jnz(self, label, comment=""): self.backend.emit_jnz(label, comment)

    def emit_jmp(self, target, comment=""):
        self.backend.emit_jmp(target, comment)
    
    def emit_lea_byte (self, reg1, reg2, offset, comment=""):
        self.backend.emit_lea_byte(reg1, reg2, offset, comment)
        
    def emit_lea_dword(self, reg1, reg2, offset, comment=""):
        self.backend.emit_lea_dword(reg1, reg2, offset, comment)
        
    def emit_lea_qword(self, reg1, reg2, offset, comment=""):
        self.backend.emit_lea_qword(reg1, reg2, offset, comment)
    
    def emit_mov_byte (self, reg1, reg2, vars, comment=""):
        self.backend.emit_mov_byte(reg1, reg2, vars, comment)
    
    def emit_mov_dword(self, reg1, reg2, vars, comment=""):
        self.backend.emit_mov_dword(reg1, reg2, vars, comment)
        
    def emit_mov_qword(self, reg1, reg2, vars, comment=""):
        self.backend.emit_mov_qword(reg1, reg2, vars, comment)
    
    def emit_mov    (self, dst, src, comment=""): self.backend.emit_mov    (dst, src, comment)
    def emit_mov_imm(self, dst, src, comment=""): self.backend.emit_mov_imm(dst, src, comment)
    def emit_movzx  (self, dst, src, comment=""): self.backend.emit_movzx  (dst, src, comment)
    def emit_movsxd (self, dst, src, comment=""): self.backend.emit_movsxd (dst, src, comment)
    def emit_movq(self, dst, src, comment=""): self.backend.emit_movq(dst, src, comment)
    def emit_movsd_load(self, dst, base, offset=0, comment=""): self.backend.emit_movsd_load(dst, base, offset, comment)
    def emit_movsd_load_field(self, dst, base, field, comment=""): self.backend.emit_movsd_load_field(dst, base, field, comment)
    def emit_movsd_store(self, base, offset, src, comment=""): self.backend.emit_movsd_store(base, offset, src, comment)
    def emit_ucomisd(self, dst, src, comment=""): self.backend.emit_ucomisd(dst, src, comment)
    def emit_cvtsi2sd(self, dst, src, comment=""): self.backend.emit_cvtsi2sd(dst, src, comment)
    def emit_movapd(self, dst, src, comment=""): self.backend.emit_movapd(dst, src, comment)
    def emit_addsd(self, dst, src, comment=""): self.backend.emit_addsd(dst, src, comment)
    def emit_subsd(self, dst, src, comment=""): self.backend.emit_subsd(dst, src, comment)
    def emit_mulsd(self, dst, src, comment=""): self.backend.emit_mulsd(dst, src, comment)
    def emit_divsd(self, dst, src, comment=""): self.backend.emit_divsd(dst, src, comment)
    def emit_cdq(self, comment=""): self.backend.emit_cdq(comment)
    def emit_idiv(self, reg, comment=""): self.backend.emit_idiv(reg, comment)
    def emit_mov_byte_ptr (self, dst, base, offset=0, comment=""): self.backend.emit_mov_byte_ptr (dst, base, offset, comment)
    def emit_mov_dword_ptr(self, dst, base, offset=0, comment=""): self.backend.emit_mov_dword_ptr(dst, base, offset, comment)
    def emit_mov_qword_ptr(self, dst, base, offset=0, comment=""): self.backend.emit_mov_qword_ptr(dst, base, offset, comment)
    def emit_mov_qword_ptr_store(self, base, offset, src, comment=""): self.backend.emit_mov_qword_ptr_store(base, offset, src, comment)
    def emit_mov_dword_ptr_store(self, base, offset, src, comment=""): self.backend.emit_mov_dword_ptr_store(base, offset, src, comment)
    def emit_mov_reg_dword_store(self, base, src, comment=""): self.backend.emit_mov_reg_dword_store(base, src, comment)
    def emit_mov_reg_qword_store(self, base, src, comment=""): self.backend.emit_mov_reg_qword_store(base, src, comment)
    def emit_mov_reg_byte (self, dst, base, comment=""): self.backend.emit_mov_reg_byte (dst, base, comment)
    def emit_mov_reg_dword(self, dst, base, comment=""): self.backend.emit_mov_reg_dword(dst, base, comment)
    def emit_mov_reg_qword(self, dst, base, comment=""): self.backend.emit_mov_reg_qword(dst, base, comment)
    def emit_test(self, reg1, reg2, comment=""): self.backend.emit_test(reg1, reg2, comment)
    def emit_call_reg(self, target, comment=""): self.backend.emit_call_reg(target, comment)
    def emit_call_lbl(self, target, comment=""): self.backend.emit_call_lbl(target, comment)
    
    def emit_and(self, dst, src, comment=""):
        self.backend.emit_and(dst, src, comment)

    def emit_or(self, dst, src, comment=""):
        self.backend.emit_or(dst, src, comment)

    def emit_xor(self, dst, src, comment=""):
        self.backend.emit_xor(dst, src, comment)
    
    def emit_push(self, reg, comment=""): self.backend.emit_push(reg, comment)
    def emit_pop (self, reg, comment=""): self.backend.emit_pop (reg, comment)
    
    def emit_sub (self, reg, value, comment=""):
        self.backend.emit_sub(reg, value, comment)
    
    def emit_shift_left (self, dst, count, comment=""): self.backend.emit_shift_left (dst, count, comment)
    def emit_shift_right(self, dst, count, comment=""): self.backend.emit_shift_right(dst, count, comment)
    
    def emit_ret(self, comment=""):
        self.backend.emit_ret(comment)
    
    def emit_backend_jmp(self, label):
        self.backend.emit_jmp(label)
    
    def emit_backend_label(self, label):
        self.backend.emit_bind_label(label)
    
    def emit_load_integer_const(self, value):
        self.backend.emit_mov_imm("eax", value)
        return "integer"
    
    def new_label_name(self, prefix):
        self.label_id += 1
        return f"{prefix}_{self.label_id}"
    
    # ------------------------------------------------------------
    # Bereits vorhandenes identisches Literal wiederverwenden
    # ------------------------------------------------------------
    def add_string_literal(self, text):
        for label, old_text in self.string_literals:
            if old_text == text:
                return label

        label = f"str_{len(self.string_literals)}"
        self.string_literals.append((label, text))

        target = CDATA.args_target.lower()

        # ------------------------------------------------------------
        # DOS
        # ------------------------------------------------------------
        if target in ["dos", "dos16"]:
            if self.writer is None:
                raise RuntimeError(
                    "DOS writer not installed"
                )

            self.writer.add_dos_string(
                label,
                text
            )

            return label

        # ------------------------------------------------------------
        # Windows COFF32 / COFF64
        #
        # Gilt sowohl für:
        #   - reine .o/.obj-Dateien
        #   - spätere EXE-/DLL-Erzeugung
        # ------------------------------------------------------------
        if target in ["nt35", "winnt", "win32", "win64"]:
            coff = getattr(self, "coff", None)

            if coff is None:
                raise RuntimeError(
                    "COFF writer not installed"
                )

            if coff.find_symbol_index(label) is None:
                coff.add_data_string(
                    label,
                    text
                )

            return label

        raise RuntimeError(
            f"string literal target not supported: {target}"
        )
        
    def visit(self, tree):
        if tree is None:
            return None

        return super().visit(tree)
    
    def visitCompilerDirective(self, ctx):
        cmd, arg = self.compiler_directive_parts(ctx)

        if not cmd:
            return None

        if cmd == "embed":
            if self.root_module_kind == "unit":
                if arg not in self.root_embedded_objects:
                    self.root_embedded_objects.append(arg)
            else:
                # Bei Programmen/Libraries genügt die normale
                # Verarbeitung beim finalen Link.
                if arg not in CDATA.link_object_files:
                    CDATA.link_object_files.append(arg)

        elif cmd == "link":
            # Explizit auf den späteren Link verschieben.
            if arg not in CDATA.link_object_files:
                CDATA.link_object_files.append(arg)

        elif cmd == "linklib":
            if arg not in CDATA.link_archive_files:
                CDATA.link_archive_files.append(arg)

        elif cmd == "resource":
            target = str(
                getattr(
                    CDATA,
                    "args_target",
                    ""
                )
            ).lower()

            if target not in (
                "nt35",
                "winnt",
                "win32"
            ):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "{$R} resources require a COFF32 "
                        "Windows target"
                    )
                )

            resource_files = getattr(
                CDATA,
                "link_resource_files",
                None
            )

            if resource_files is None:
                resource_files = []
                CDATA.link_resource_files = resource_files

            if arg not in resource_files:
                resource_files.append(arg)

        return None
    
    def visitLocalDeclaration(self, ctx):
        if ctx is None:
            return None

        if hasattr(ctx, "constSection") and ctx.constSection():
            return self.visit(ctx.constSection())

        if hasattr(ctx, "typeSection") and ctx.typeSection():
            return self.visit(ctx.typeSection())

        if hasattr(ctx, "varSection") and ctx.varSection():
            return self.visit(ctx.varSection())

        if (hasattr(ctx, "procedureDeclaration") and ctx.procedureDeclaration()):
            return self.visit(
                ctx.procedureDeclaration()
            )

        if (hasattr(ctx, "functionDeclaration") and ctx.functionDeclaration()):
            return self.visit(
                ctx.functionDeclaration()
            )

        return self.visitChildren(ctx)
    
    def visitIncStatement(self, ctx):
        ref = ctx.variableRef()

        if ref is None:
            raise CompileError(ctx, "E0001", name="Inc")

        name = ref.IDENT().getText()

        (
            source_kind,
            info,
            typ
        ) = self.resolve_named_storage(
            ctx,
            name
        )

        #
        # Schrittweite
        #
        step = 1

        if len(ctx.expr()) == 2:
            step_type = self.visit(ctx.expr(1))

            if step_type != "integer":
                raise CompileError(ctx, "E0005",
                    got=step_type,
                    expected="integer")

            self.emit_mov("ebx", "eax")
        else:
            self.emit_mov_imm("ebx", 1)

        #
        # Variable laden
        #
        self.emit_load_named_value(
            ctx,
            name,
            source_kind,
            info
        )

        if typ == "integer":
            self.emit_add("eax", "ebx")
            self.emit_store_named_value(
                ctx,
                name,
                source_kind,
                info,
                "integer"
            )
            return None

        #
        # Pointer
        #
        if typ.startswith("^"):

            base = self.resolve_type(typ[1:])

            if base == "integer":
                size = 4

            elif base == "double":
                size = 8

            elif base == "string":
                size = self.pointer_slot_size()

            elif base in self.records:
                size = self.records[base].size

            else:
                raise CompileError(
                    ctx,
                    "E0004",
                    name=base
                )

            if size != 1:
                self.emit_imul("ebx", "ebx", size)

            self.emit_add("eax", "ebx")
            self.emit_store_named_value(
                ctx,
                name,
                source_kind,
                info,
                typ
            )

            return None

        raise CompileError(
            ctx,
            "E0005",
            got=typ,
            expected="integer or pointer"
        )

    def visitDecStatement(self, ctx):
        ref = ctx.variableRef()

        if ref is None:
            raise CompileError(ctx, "E0001", name="Dec")

        name = ref.IDENT().getText()

        (
            source_kind,
            info,
            typ
        ) = self.resolve_named_storage(
            ctx,
            name
        )

        step = 1

        if len(ctx.expr()) == 2:
            step_type = self.visit(ctx.expr(1))

            if step_type != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=step_type,
                    expected="integer"
                )

            self.emit_mov("ebx", "eax")
        else:
            self.emit_mov_imm("ebx", 1)

        self.emit_load_named_value(
            ctx,
            name,
            source_kind,
            info
        )

        if typ == "integer":
            self.emit_sub("eax", "ebx")
            self.emit_store_named_value(
                ctx,
                name,
                source_kind,
                info,
                "integer"
            )
            return None

        if typ.startswith("^"):

            base = self.resolve_type(typ[1:])

            if base == "integer":
                size = 4

            elif base == "double":
                size = 8

            elif base == "string":
                size = self.pointer_slot_size()

            elif base in self.records:
                size = self.records[base].size

            else:
                raise CompileError(
                    ctx,
                    "E0004",
                    name=base
                )

            if size != 1:
                self.emit_imul("ebx", "ebx", size)

            self.emit_sub("eax", "ebx")
            self.emit_store_named_value(
                ctx,
                name,
                source_kind,
                info,
                typ
            )

            return None

        raise CompileError(
            ctx,
            "E0005",
            got=typ,
            expected="integer or pointer"
        )
    
    def visit_actual_param_expr(self, arg):
        if arg is None:
            return None

        # argumentList().expr() liefert bereits ExprContext-Objekte.
        if isinstance(
            arg,
            PascalParser.ExprContext
        ):
            return self.visit(arg)

        if hasattr(arg, "expr") and arg.expr():
            return self.visit(
                arg.expr()
            )

        if hasattr(arg, "STRING") and arg.STRING():
            value = arg.STRING().getText()[1:-1]
            label = self.add_string_literal(value)

            self.emit_mov("rax", label)

            if len(value) == 1:
                return "char"

            if CDATA.args_target in (
                "nt35",
                "winnt",
                "win32"
            ):
                self.emit_push("rax")
                self.emit_mov_imm(
                    "rax",
                    "&_jit_dynstring_from_cstr"
                )
                self.emit_call_rax()
                self.backend.emit_cleanup_stack(4)

                if self.coff.find_symbol_index("ctx") is not None:
                    self.coff.emit_lea_reg_data_label(
                        "esi",
                        "ctx"
                    )
            else:
                self.emit_mov("rcx", "rax")
                self.emit_mov_imm(
                    "rax",
                    "&_jit_dynstring_from_cstr"
                )
                self.emit_call_rax()

            return "string"

        raise CompileError(
            arg,
            "E0015",
            text=arg.getText()
        )
    
    def visitSourceFile(self, ctx):
        self.source_file_depth += 1
        is_root_source = self.source_file_depth == 1

        try:
            # ----------------------------------------------------------
            # Typ des äußersten Moduls merken
            # ----------------------------------------------------------
            if is_root_source:
                if ctx.programFile():
                    self.root_module_kind = "program"
                    self.root_unit_name   = None

                elif ctx.unitFile():
                    self.root_module_kind = "unit"
                    self.root_unit_name = (
                        ctx.unitFile()
                        .qualifiedIdent()
                        .getText()
                    )

                elif ctx.libraryFile():
                    self.root_module_kind = "library"
                    self.root_unit_name   = None

            # ----------------------------------------------------------
            # Compiler-Direktiven dieser Quelldatei verarbeiten
            # ----------------------------------------------------------
            for directive in ctx.compilerDirective():
                cmd, arg = self.compiler_directive_parts(directive)

                if is_root_source and self.root_module_kind == "unit":
                    if cmd == "embed":
                        if arg not in self.root_embedded_objects:
                            self.root_embedded_objects.append(arg)
                    
                    if cmd == "link":
                        if arg not in self.root_link_objects:
                            self.root_link_objects.append(arg)

                    elif cmd == "linklib":
                        if arg not in self.root_link_archives:
                            self.root_link_archives.append(arg)

                    elif cmd == "resource":
                        if arg not in self.root_resource_files:
                            self.root_resource_files.append(arg)

                self.visit(directive)

            # ----------------------------------------------------------
            # Modul besuchen
            # ----------------------------------------------------------
            if ctx.programFile():
                return self.visit(ctx.programFile())

            if ctx.unitFile():
                return self.visit(ctx.unitFile())

            if ctx.libraryFile():
                return self.visit(ctx.libraryFile())

            return None

        finally:
            self.source_file_depth -= 1
    
    def visitUsesClause(self, ctx):
        for ident in ctx.qualifiedIdentList().qualifiedIdent():
            self.load_unit(ctx, ident.getText())
        
        return None
    
    def visitProgramFile(self, ctx):
        self.program_name       = ctx.IDENT().getText()
        self.module_kind        = "program"
        self.module_kind_value  = 1
        
        if ctx.usesClause():
            self.visit(ctx.usesClause())
        
        for decl in ctx.declarationPart():
            if decl is not None:
                self.visit(decl)

        self.validate_class_methods(ctx)
        
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.writer.emit_lea_reg_data_label("esi", "ctx")
            self.emit_push("ebx")
        else:
            self.emit_push("r12")
            self.emit_push("rbx")
            self.emit_sub("rsp", 8, comment="align stack")
            self.emit_mov("r12", "rcx", comment="ctx")
        
        self.emit_unit_initializers()
        
        for name, info in self.vars.items():
            if info["type"] in self.arrays:
                self.emit_init_array_var(ctx, name, info)
        
        self.visit(ctx.block())
        return self.render_cpp()
    
    def visitLibraryFile(self, ctx):
        self.program_name       = ctx.IDENT().getText()
        self.module_kind        = "library"
        self.module_kind_value  = 3

        target = CDATA.args_target.lower()
        is_nt32 = target in ["nt35", "winnt", "win32"]

        if is_nt32:
            dll_filename = (
                getattr(CDATA, "exe_file", None)
                or getattr(CDATA, "dll_file", None)
                or (self.program_name.lower() + ".dll")
            )

            self.writer.configure_dll(
                dll_filename,
                entry_label=None
            )

        if ctx.usesClause():
            self.visit(ctx.usesClause())

        for decl in ctx.declarationPart():
            if decl is not None:
                self.visit(decl)

        if ctx.exportsClause():
            self.visit(ctx.exportsClause())

        self.validate_class_methods(ctx)

        if is_nt32:
            # Export targets are real COFF symbols.  The export name can be
            # different from the internal code label; aliases created by the
            # declaration visitors point both names to the same RVA.
            for item in self.exports:
                export_name = item.get("mangled")

                if not export_name:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "DLL export has no mangled symbol: "
                            + str(item.get("name"))
                        )
                    )

                if self.writer.find_symbol_index(export_name) is None:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "DLL export target symbol not found: "
                            + export_name
                        )
                    )

                self.writer.add_export(
                    name=export_name,
                    target_label=export_name,
                    ordinal=item.get("ordinal")
                )

            # The library owns a static JIT context.  Exported routines that
            # use global data can therefore reference the same context as an
            # executable generated by this compiler.
            self.finalize_coff_context()

            entry_label = self.new_named_label(
                "dll_entry_" + self.program_name
            )
            done_label = self.new_named_label(
                "dll_entry_done_" + self.program_name
            )

            self.writer.dll_entry_label = entry_label
            self.writer.bind_label(entry_label)

            # BOOL WINAPI DllMain(HINSTANCE, DWORD reason, LPVOID)
            # stdcall: callee removes 12 argument bytes.
            self.writer.emit_push_reg32("ebp")
            self.writer.emit_mov_reg_reg32("ebp", "esp")
            self.writer.emit_push_reg32("ebx")
            self.writer.emit_push_reg32("esi")

            self.writer.emit_lea_reg_data_label("esi", "ctx")

            # reason is the second argument: [ebp + 12].
            self.writer.emit_mov_reg_mem32("eax", "ebp", 12)
            self.writer.emit_cmp_reg_imm32("eax", 1)  # DLL_PROCESS_ATTACH
            self.writer.emit_jne(done_label)

            self.emit_unit_initializers()

            for name, info in self.vars.items():
                if info["type"] in self.arrays:
                    self.emit_init_array_var(ctx, name, info)

            # Pascal's library begin/end block is executed once when the DLL
            # is attached to a process.
            if ctx.block() is not None:
                self.visit(ctx.block())

            self.writer.bind_label(done_label)
            self.writer.emit_mov_reg_imm32("eax", 1)  # TRUE

            self.writer.emit_pop_reg32("esi")
            self.writer.emit_pop_reg32("ebx")
            self.writer.emit_mov_reg_reg32("esp", "ebp")
            self.writer.emit_pop_reg32("ebp")
            self.writer.emit_ret_imm16(12)

            self.write_fpc_import_unit()
            return None

        # Existing non-NT32 path.
        self.emit_push("r12")
        self.emit_push("rbx")
        self.emit_sub("rsp", 8, comment="align stack")
        self.emit_mov("r12", "rcx", comment="ctx")

        self.emit_unit_initializers()

        for name, info in self.vars.items():
            if info["type"] in self.arrays:
                self.emit_init_array_var(ctx, name, info)

        self.visit(ctx.block())
        return self.render_cpp()

    def visitUnitFile(self, ctx):
        unit_name = ctx.qualifiedIdent().getText()
        unit_key  = self.normalize_unit_name(unit_name)

        old_unit       = self.current_unit
        old_kind       = self.module_kind
        old_kind_value = self.module_kind_value
        old_collect    = self.collect_pui_interface

        is_root_unit = (
            self.source_file_depth == 1
            and self.root_module_kind == "unit"
        )

        self.module_kind       = "unit"
        self.module_kind_value = 2
        self.current_unit      = unit_key

        try:
            # ------------------------------------------------------
            # PUI nur für die äußerste, tatsächlich kompilierte Unit
            # ------------------------------------------------------
            if is_root_unit:
                self.begin_unit_pui(unit_name)

                interface_uses = ctx.interfaceSection().usesClause()

                if interface_uses:
                    self.pending_pui["uses"]["interface"] = [
                        item.getText()
                        for item in (
                            interface_uses
                            .qualifiedIdentList()
                            .qualifiedIdent()
                        )
                    ]

                implementation_uses = (
                    ctx.implementationSection().usesClause()
                )

                if implementation_uses:
                    self.pending_pui["uses"]["implementation"] = [
                        item.getText()
                        for item in (
                            implementation_uses
                            .qualifiedIdentList()
                            .qualifiedIdent()
                        )
                    ]

            # ------------------------------------------------------
            # Interface: öffentliche Deklarationen sammeln
            # ------------------------------------------------------
            self.collect_pui_interface = is_root_unit
            self.visit(ctx.interfaceSection())

            # ------------------------------------------------------
            # Implementation nicht als Interface exportieren
            # ------------------------------------------------------
            self.collect_pui_interface = False
            self.visit(ctx.implementationSection())

            self.validate_class_methods(ctx)

            # ------------------------------------------------------
            # Stabiles Unit-Initialisierungssymbol
            #
            # Dieses Symbol wird auch erzeugt, wenn kein expliziter
            # initialization/begin-Block vorhanden ist.
            # ------------------------------------------------------
            init_symbol = (
                f"_{self.fpc_mangle_unit(unit_name)}$$_INIT"
            )

            init_label = self.new_named_label(
                "unit_init_" + unit_key
            )

            skip_label = self.new_named_label(
                "skip_unit_init_" + unit_key
            )

            self.emit_jmp(skip_label)
            self.emit_bind_label(init_label)

            if ctx.unitInitBlock():
                self.visit(ctx.unitInitBlock())

            self.emit_ret()
            self.emit_bind_label(skip_label)

            if hasattr(self.backend.writer, "add_symbol_alias"):
                self.backend.writer.add_symbol_alias(
                    init_symbol,
                    init_label
                )

            # Eigenes Initialisierungslabel ist innerhalb dieser COFF-Datei.
            self.add_unit_initializer(
                init_label,
                external=False
            )

            if is_root_unit:
                self.pending_pui["initialization"]["symbol"] = (
                    init_symbol
                )

        finally:
            self.collect_pui_interface = old_collect

            self.module_kind       = old_kind
            self.module_kind_value = old_kind_value
            self.current_unit      = old_unit

        return None
    
    def visitInterfaceDeclarationPart(self, ctx):
        if ctx.constSection():
            return self.visit(ctx.constSection())
        
        if ctx.typeSection():
            return self.visit(ctx.typeSection())
        
        if ctx.varSection():
            return self.visit(ctx.varSection())
        
        if ctx.procedureHeader():
            return self.visit(ctx.procedureHeader())
        
        if ctx.functionHeader():
            return self.visit(ctx.functionHeader())
        
        return None
    
    def visitImplementationDeclarationPart(self, ctx):
        if ctx.constSection():
            return self.visit(ctx.constSection())
        
        if ctx.typeSection():
            return self.visit(ctx.typeSection())
        
        if ctx.varSection():
            return self.visit(ctx.varSection())
        
        if ctx.procedureDeclaration():
            return self.visit(ctx.procedureDeclaration())
        
        if ctx.functionDeclaration():
            return self.visit(ctx.functionDeclaration())
        
        if ctx.classMethodImplementation():
            return self.visit(ctx.classMethodImplementation())
        
        return None
    
    def visitInterfaceSection(self, ctx):
        if ctx.usesClause():
            self.visit(ctx.usesClause())

        for decl in ctx.interfaceDeclarationPart():
            self.visit(decl)

        return None
    
    def visitImplementationSection(self, ctx):
        if ctx.usesClause():
            self.visit(ctx.usesClause())

        for decl in ctx.implementationDeclarationPart():
            self.visit(decl)

        return None
    
    def load_pui_macros(
        pui_filename
    ):
        with open(
            pui_filename,
            "r",
            encoding="utf-8"
        ) as stream:
            data = json.load(stream)

        macros = data.get(
            "macros",
            {}
        )

        if not isinstance(macros, dict):
            raise RuntimeError(
                f"invalid macros section in PUI: "
                f"{pui_filename}"
            )

        return {
            str(name).upper(): value
            for name, value in macros.items()
        }

    # ------------------------------------------------------------
    # Schreibt die PUI-Metadaten einer Pascal-Unit.
    #
    # Neben Typen, Routinen und Linkinformationen werden auch die
    # innerhalb der Unit definierten Preprocessor-Makros gespeichert.
    #
    # Beispiel:
    #
    #    {$define VERSION 1}
    #    {$define VERSION_TEXT '1.0.0'}
    #
    # ergibt in der PUI:
    #
    #    "macros": {
    #        "VERSION": 1,
    #        "VERSION_TEXT": "1.0.0"
    #    }
    # ------------------------------------------------------------
    def write_unit_pui(
        self,
        object_file,
        pui_file=None
    ):
        # ------------------------------------------------------------
        # Nur Units erzeugen eine PUI-Datei
        # ------------------------------------------------------------
        if self.root_module_kind != "unit":
            return None

        if self.pending_pui is None:
            raise RuntimeError(
                "No PUI metadata was generated for the unit"
            )

        # ------------------------------------------------------------
        # Objektdatei bestimmen
        # ------------------------------------------------------------
        object_path = Path(
            object_file
        ).resolve()

        # ------------------------------------------------------------
        # Zielpfad der PUI-Datei bestimmen
        # ------------------------------------------------------------
        if pui_file is None:
            pui_path = object_path.with_suffix(
                ".pui"
            )
        else:
            pui_path = Path(
                pui_file
            ).resolve()

        pui_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # ------------------------------------------------------------
        # PUI-Bereiche sicherstellen
        # ------------------------------------------------------------
        object_info = self.pending_pui.setdefault(
            "object",
            {}
        )

        link_info = self.pending_pui.setdefault(
            "link",
            {}
        )

        # ------------------------------------------------------------
        # Name der zugehörigen Objektdatei
        # ------------------------------------------------------------
        object_info["file"] = object_path.name

        # Pfade aus {$link} und {$linklib} werden später relativ zum
        # Verzeichnis der PUI-Datei ausgewertet.
        link_info["base_directory"] = "pui"

        # ------------------------------------------------------------
        # Unit-Makros übernehmen
        # ------------------------------------------------------------
        source_macros = getattr(
            self,
            "unit_source_macros",
            {}
        )

        if not source_macros:
            source_macros = getattr(
                CDATA,
                "unit_source_macros",
                {}
            )
    
        if source_macros is None:
            source_macros = {}

        if not isinstance(source_macros, dict):
            raise RuntimeError(
                "Unit macro metadata must be a dictionary"
            )

        pui_macros = {}

        for macro_name, macro_value in source_macros.items():
            name = str(
                macro_name
            ).strip().upper()

            if not name:
                raise RuntimeError(
                    "PUI macro name must not be empty"
                )

            if not re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_]*",
                name
            ):
                raise RuntimeError(
                    f"Invalid PUI macro name: {name}"
                )

            # JSON-kompatible und vom Preprocessor unterstützte Werte.
            if isinstance(
                macro_value,
                (
                    bool,
                    int,
                    float,
                    str
                )
            ):
                value = macro_value

            elif macro_value is None:
                value = None

            else:
                raise RuntimeError(
                    f"Unsupported value type for PUI macro "
                    f"{name}: "
                    f"{type(macro_value).__name__}"
                )

            pui_macros[name] = value

        # Sortierte Ausgabe macht die PUI-Dateien reproduzierbarer.
        self.pending_pui["macros"] = dict(
            sorted(
                pui_macros.items()
            )
        )

        # ------------------------------------------------------------
        # Temporäre Datei für atomisches Schreiben
        # ------------------------------------------------------------
        temporary_path = Path(
            str(pui_path) + ".tmp"
        )
        
        if CDATA.debug_mode:
            print("PUI MACROS:", pui_macros)
        try:
            with open(
                temporary_path,
                "w",
                encoding="utf-8",
                newline="\n"
            ) as stream:
                json.dump(
                    self.pending_pui,
                    stream,
                    ensure_ascii=False,
                    indent=4
                )

                stream.write("\n")

            # Die vorhandene PUI wird erst ersetzt, wenn die temporäre
            # Datei vollständig geschrieben wurde.
            os.replace(
                temporary_path,
                pui_path
            )

        except Exception:
            # Eine möglicherweise unvollständige temporäre Datei entfernen.
            try:
                if temporary_path.exists():
                    temporary_path.unlink()

            except OSError:
                pass

            raise

        return str(
            pui_path
        )
    
    def visitExitStatement(self, ctx):
        if not self.exit_label_stack:
            raise CompileError(ctx, "E0006")

        self.emit_jmp(self.exit_label_stack[-1], comment="Exit")
        return None
    
    def visitConstSection(self, ctx):
        for decl in ctx.constDeclaration():
            self.visit(decl)
        return None

    def emit_class_method_direct_call(
        self,
        method,
        comment=""
    ):
        local_label = getattr(
            method,
            "label",
            None
        )

        mangled = getattr(
            method,
            "mangled",
            None
        )

        target = (
            local_label
            if local_label is not None
            else mangled
        )

        if not isinstance(target, str) or not target:
            raise RuntimeError(
                "class method has no direct call target: "
                + str(method.name)
            )

        if CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        ):
            self.writer.emit_call_external(
                target
            )
            return

        if local_label is None:
            raise RuntimeError(
                "PUI class imports currently require COFF32"
            )

        self.emit_call_lbl(
            local_label,
            comment=comment
        )

    def visitInheritedStatement(self, ctx):
        if self.current_class is None or self.current_method is None:
            raise CompileError(
                ctx,
                "E0019",
                text="inherited used outside class method"
            )

        cls = self.classes[self.current_class]

        if not cls.parent:
            raise CompileError(
                ctx,
                "E0019",
                text=f"class {cls.name} has no parent class"
            )

        # inherited;
        # inherited Create;
        if ctx.IDENT():
            method_name = ctx.IDENT().getText()
        else:
            method_name = self.current_method.name

        args = self.function_call_args(ctx)
        argument_bytes = 0
        actual_types   = []

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            for arg in reversed(args):
                arg_type = self.resolve_type(self.visit_actual_param_expr(arg))
                actual_types.insert(0, arg_type)
                
                if arg_type in ["integer", "boolean", "char", "string"]:
                    self.emit_push("eax", comment="inherited argument")
                    argument_bytes += 4
                    continue
            
                if self.is_pointer_type(arg_type):
                    self.emit_push("eax", comment="inherted pointer argument")
                    argument_bytes += 4
                    continue
                    
                if arg_type == "double":
                    self.emit_sub("esp", 8)
                    self.emit_movsd_store("esp", 0, "xmm0")
                    argument_bytes += 8
                    continue
            
                raise CompileError(ctx, "E0019",
                    text=(f"unsupported inherited argument type {arg_type}")
                )
        
            method, owner_cls = self.find_class_method_recursive(
                ctx,
                cls.parent,
                method_name,
                actual_types
            )

            # Self wurde im Prolog nach [ebp-4] gesichert.
            self.emit_mov_dword_ptr("eax", "ebp", -4, comment="inherited Self")
            
            # Self muss unmittelbar vor dem Call oben auf
            # dem Stack liegen:
            #
            #   [esp+0] = Self
            #   [esp+4] = Parameter 1
            #
            self.emit_push("eax", comment="inherited Self")
            self.emit_class_method_direct_call(
                method,
                comment=(
                    f"inherited "
                    f"{owner_cls.name}."
                    f"{method.name}"
                )
            )
            
            self.backend.emit_cleanup_stack(argument_bytes + 4)
            
            if (self.coff.find_symbol_index("ctx") is not None):
                self.writer.emit_lea_reg_data_label("esi", "ctx")
                
            if method.kind == "function":
                return self.resolve_type(
                    method.return_type
                )

            return None
            
        # Windows 64-bit
        else:
            # Der derzeitige Aufbau unterstützt nur die drei Registerparameter
            # nach Self:
            #
            #   RCX = Self
            #   RDX = Parameter 1
            #   R8  = Parameter 2
            #   R9  = Parameter 3
            #
            if len(args) > 3:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "Win64 inherited calls currently "
                        "support at most three parameters"
                    )
                )

            for arg in reversed(args):
                arg_type = self.resolve_type(
                    self.visit_actual_param_expr(
                        arg
                    )
                )

                actual_types.insert(
                    0,
                    arg_type
                )

                if arg_type == "integer":
                    self.emit_movsxd(
                        "rax",
                        "eax"
                    )

                    self.emit_push(
                        "rax",
                        comment="inherited integer argument"
                    )

                    continue

                if arg_type in (
                    "boolean",
                    "char"
                ):
                    # Ein Schreiben nach EAX löscht unter x64 die
                    # oberen 32 Bits von RAX.
                    self.emit_and(
                        "eax",
                        0xFFFFFFFF
                    )

                    self.emit_push(
                        "rax",
                        comment="inherited scalar argument"
                    )

                    continue

                if (
                    arg_type == "string"
                    or self.is_pointer_type(
                        arg_type
                    )
                ):
                    self.emit_push(
                        "rax",
                        comment="inherited pointer argument"
                    )

                    continue

                if arg_type == "double":
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "Win64 Double arguments in inherited "
                            "calls are not implemented yet"
                        )
                    )

                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "unsupported inherited "
                        f"argument type {arg_type}"
                    )
                )

            method, owner_cls = (
                self.find_class_method_recursive(
                    ctx,
                    cls.parent,
                    method_name,
                    actual_types
                )
            )

            # Self wurde im Prolog nach [rbp-8] gesichert.
            self.emit_mov_qword_ptr(
                "rcx",
                "rbp",
                -8,
                comment="inherited Self"
            )

            param_regs = [
                "rdx",
                "r8",
                "r9"
            ]

            # Durch das Pushen in umgekehrter Reihenfolge liegt
            # Parameter 1 jetzt oben auf dem Stack.
            for index in range(
                len(args)
            ):
                self.emit_pop(
                    param_regs[index],
                    comment=(
                        f"inherited argument "
                        f"{index + 1}"
                    )
                )

            # Windows-x64 Shadow Space.
            #
            # Falls dein Methoden-Prolog RSP vor diesem Punkt nur auf
            # 8 modulo 16 ausrichtet, müssen hier 40 statt 32 Bytes
            # reserviert werden.
            self.emit_sub(
                "rsp",
                32,
                comment="inherited shadow space"
            )

            self.emit_class_method_direct_call(
                method,
                comment=(
                    f"inherited "
                    f"{owner_cls.name}."
                    f"{method.name}"
                )
            )

            self.emit_add(
                "rsp",
                32,
                comment="remove inherited shadow space"
            )
            
            if method.kind == "function":
                return self.resolve_type(
                    method.return_type
                )

            return None
    
    def visitClassMethodImplementation(self, ctx):
        class_name  = ctx.IDENT(0).getText()
        method_name = ctx.IDENT(1).getText()
        
        class_key   = class_name.lower()
        method_key  = method_name.lower()
        
        if class_key not in self.classes:
            raise CompileError(ctx, "E0004", name=class_name)
        
        cls = self.classes[class_key]
        
        if method_key not in cls.methods:
            raise CompileError(
                ctx,
                "E0019",
                text=f"class {class_name} has no declared method {method_name}"
            )
        
        params = self.collect_formal_params(ctx)
        method = self.find_class_method_overload(
            ctx,
            cls,
            method_name,
            [p["type"] for p in params]
        )

        if method.owner != class_key:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"cannot implement inherited method "
                    f"{class_name}.{method_name}; "
                    f"declare it in {class_name} first"
                )
            )

        method.implemented = True
        
        skip_label = self.new_named_label(
            "skip_class_" + class_name + "_" + method_name
        )

        exit_label = self.new_named_label(
            "exit_class_" + class_name + "_" + method_name
        )
        
        self.emit_jmp(skip_label)
        self.emit_bind_label(method.label)
        
        if (method.mangled
            and hasattr(self.backend.writer, "add_symbol_alias")
        ):
            self.backend.writer.add_symbol_alias(
                method.mangled,
                method.label
            )
        
        old_params = self.current_proc_params
        
        # ------------------------------------------------------------
        # NT32 / Windows NT 3.5
        # ------------------------------------------------------------
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            # Stack beim Eintritt:
            #
            # [esp+0]  = Return-Adresse
            # [esp+4]  = Self
            # [esp+8]  = Parameter 1
            # [esp+12] = Parameter 2
            #
            self.emit_push("ebp", comment="class method prolog")
            self.emit_mov("ebp", "esp", comment="class method frame")

            # Nach dem Prolog:
            #
            # [ebp+4]  = Return-Adresse
            # [ebp+8]  = Self
            # [ebp+12] = Parameter 1
            # [ebp+16] = Parameter 2
            #
            self.emit_mov_dword_ptr(
                "eax",
                "ebp",
                8,
                comment="Self"
            )

            # Self als lokalen 32-Bit-Wert sichern:
            # [ebp-4] = Self
            self.emit_push("eax", comment="save Self")

            self.current_proc_params = {
                "self": {
                    "type": "^" + class_key,
                    "reg": None,
                    "stack_offset": -4,
                    "is_var": False
                }
            }

            for index, p in enumerate(params):
                pname = p["name"]
                ptype = self.resolve_type(p["type"])

                self.current_proc_params[pname.lower()] = {
                    "type": ptype,
                    "reg": None,
                    "stack_offset": 12 + index * 4,
                    "is_var": p.get("is_var", False)
                }

            self.emit_sub(
                "esp",
                256,
                comment="class method locals"
            )
        
        # ------------------------------------------------------------
        # Win64
        # ------------------------------------------------------------
        else:
            # Windows-x64:
            # RCX = Self
            # RDX = Parameter 1
            # R8  = Parameter 2
            # R9  = Parameter 3
            self.emit_push("rbp", comment="class method prolog")
            self.emit_mov("rbp", "rsp", comment="class method frame")

            # [rbp-8] = Self
            self.emit_push("rcx", comment="save Self")

            self.current_proc_params = {
                "self": {
                    "type": "^" + class_key,
                    "reg": "rcx",
                    "stack_offset": -8,
                    "is_var": False
                }
            }

            param_regs = ["rdx", "r8", "r9"]

            for index, p in enumerate(params):
                pname = p["name"]
                ptype = self.resolve_type(p["type"])

                if index < len(param_regs):
                    reg = param_regs[index]

                    self.emit_push(
                        reg,
                        comment=f"save class method param {pname}"
                    )

                    stack_offset = -8 * (index + 2)

                else:
                    reg = None

                    # Return-Adresse + gespeichertes RBP + Shadow Space
                    stack_offset = 48 + (
                        (index - len(param_regs)) * 8
                    )

                self.current_proc_params[pname.lower()] = {
                    "type": ptype,
                    "reg": reg,
                    "stack_offset": stack_offset,
                    "is_var": p.get("is_var", False)
                }

            self.emit_sub(
                "rsp",
                256,
                comment="class method locals"
            )
        
        self.push_local_scope()
        self.push_const_scope()
        
        # Self liegt bereits unterhalb von BP/RBP auf dem Stack.
        # Lokale Variablen dürfen diesen Bereich nicht überschreiben.
        scope = self.current_local_scope()

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            scope["next_offset"] = 4      # [ebp-4] = Self
        else:
            scope["next_offset"] = 8      # [rbp-8] = Self
        
        old_class    = self.current_class
        old_method   = self.current_method
        old_function = self.current_function

        self.current_class  = class_key
        self.current_method = method

        result_off = None

        if method.kind == "function":
            rt = self.resolve_type(method.return_type)

            self.current_function = {
                "name": method.name,
                "return_type": rt,
                "scoped_name": class_name + "_" + method.name
            }

            self.declare_local_var(ctx, "Result", rt)
            result_var = self.find_local_var("Result")
            result_off = result_var["offset"]
        
        # Exit in Methoden, Konstruktoren und Destruktoren verlässt immer
        # die komplette aktuelle Routine. Schleifen legen deshalb kein
        # eigenes Exit-Ziel ab; auch aus FOR/WHILE/REPEAT wird dieses
        # Methoden-Epilogziel verwendet.
        self.exit_label_stack.append(exit_label)

        try:
            self.visit(ctx.block())

        finally:
            self.exit_label_stack.pop()

        self.current_class    = old_class
        self.current_method   = old_method
        self.current_function = old_function
        
        self.pop_const_scope()
        self.pop_local_scope()
        
        self.current_proc_params = old_params

        # Normales Ende und Pascal Exit laufen über denselben Epilog.
        self.emit_bind_label(exit_label)

        if method.kind == "function":
            declared_rt = self.resolve_type(
                method.return_type
            )

            # Pascal-Klassen, Pointer-Aliase und Subranges auf ihren
            # tatsächlichen ABI-Rückgabetyp abbilden.
            abi_rt = self.function_abi_return_type(
                declared_rt
            )

            # --------------------------------------------------------------
            # NT32
            # --------------------------------------------------------------
            if CDATA.args_target in (
                "nt35",
                "winnt",
                "win32"
            ):
                if abi_rt in (
                    "integer",
                    "boolean",
                    "char",
                    "string",
                    "pointer"
                ):
                    self.emit_mov_dword_ptr(
                        "eax",
                        "ebp",
                        result_off,
                        comment=(
                            f"{class_name}.{method.name} result "
                            f"({declared_rt})"
                        )
                    )

                    if abi_rt == "boolean":
                        self.emit_and(
                            "eax",
                            1
                        )

                elif abi_rt == "double":
                    self.emit_movsd_load(
                        "xmm0",
                        "ebp",
                        result_off,
                        comment=(
                            f"{class_name}.{method.name} result"
                        )
                    )

                else:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=declared_rt,
                        expected=(
                            "integer/boolean/char/string/"
                            "double/pointer/class/subrange"
                        )
                    )

            # --------------------------------------------------------------
            # Win64
            # --------------------------------------------------------------
            else:
                if abi_rt in (
                    "string",
                    "pointer"
                ):
                    self.emit_mov_qword_ptr(
                        "rax",
                        "rbp",
                        result_off,
                        comment=(
                            f"{class_name}.{method.name} result "
                            f"({declared_rt})"
                        )
                    )

                elif abi_rt in (
                    "integer",
                    "boolean",
                    "char"
                ):
                    self.emit_mov_dword_ptr(
                        "eax",
                        "rbp",
                        result_off,
                        comment=(
                            f"{class_name}.{method.name} result"
                        )
                    )

                    if abi_rt == "boolean":
                        self.emit_and(
                            "eax",
                            1
                        )

                elif abi_rt == "double":
                    self.emit_movsd_load(
                        "xmm0",
                        "rbp",
                        result_off,
                        comment=(
                            f"{class_name}.{method.name} result"
                        )
                    )

                else:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=declared_rt,
                        expected=(
                            "integer/boolean/char/string/"
                            "double/pointer/class/subrange"
                        )
                    )
            
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_mov("esp", "ebp")
            self.emit_pop("ebp")
            self.emit_ret()
        else:
            self.emit_mov("rsp", "rbp")
            self.emit_pop("rbp")
            self.emit_ret()
        
        self.emit_bind_label(skip_label)
        
        return None
    
    def visitDeclarationPart(self, ctx):
        if ctx is None:
            return None
        
        if hasattr(ctx, "classMethodImplementation") and ctx.classMethodImplementation():
            return self.visit(ctx.classMethodImplementation())
        
        if hasattr(ctx, "typeSection") and ctx.typeSection():
            return self.visit(ctx.typeSection())
        
        if hasattr(ctx, "constDeclaration") and ctx.constDeclaration():
            return self.visit(ctx.constDeclaration())
        
        if hasattr(ctx, "constSection") and ctx.constSection():
            return self.visit(ctx.constSection())
        
        if hasattr(ctx, "varSection") and ctx.varSection():
            return self.visit(ctx.varSection())
        
        if hasattr(ctx, "procedureDeclaration") and ctx.procedureDeclaration():
            return self.visit(ctx.procedureDeclaration())
        
        if hasattr(ctx, "functionDeclaration") and ctx.functionDeclaration():
            return self.visit(ctx.functionDeclaration())
        
        return None
    
    def visitExportsClause(self, ctx):
        for item in ctx.exportItem():
            name  = item.qualifiedIdent().getText()
            parts = name.split(".")
            
            wanted_types = []
            
            if item.exportSignature():
                lst = item.exportSignature().exportTypeList()
                
                if lst:
                    for t in lst.typeName():
                        wanted_types.append(
                            self.resolve_type(t.getText())
                        )
            
            # Klassenmethode: TFoo.Create / TFoo.Create(String) / TFoo.Add(Integer,Integer)
            if len(parts) == 2:
                class_name  = parts[0]
                method_name = parts[1]
                
                cls = self.classes.get(class_name.lower())
                
                if not cls:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=f"export class not found: {class_name}"
                    )
                
                overloads = cls.methods.get(method_name.lower(), [])
                
                if not overloads:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=f"export method not found: {name}"
                    )
                
                if item.exportSignature():
                    methods_to_export = [
                        self.find_export_method_overload(
                            ctx,
                            overloads,
                            wanted_types
                        )
                    ]
                else:
                    methods_to_export = overloads
                
                for method in methods_to_export:
                    export_name = (
                        class_name
                        + "_"
                        + method.name
                        + self.export_wrapper_suffix(method.params)
                    )
                    
                    self.exports.append({
                        "kind"          : "class_method",
                        "name"          : name,
                        "class_name"    : class_name,
                        "method_name"   : method.name,
                        "method_kind"   : method.kind,
                        "mangled"       : method.mangled,
                        "export_name"   : export_name,
                        "return_type"   : method.return_type,
                        "params"        : method.params
                    })
                
                continue
            
            # Normale Funktion: Add / Add(Integer,Integer)
            if wanted_types:
                func = self.find_export_function_overload(name, wanted_types)
            else:
                func = self.find_function(name)
            
            if func:
                self.exports.append({
                    "kind"          : "function",
                    "name"          : name,
                    "mangled"       : func["mangled"],
                    "export_name"   : name,
                    "return_type"   : func["return_type"],
                    "params"        : func.get("params", [])
                })
                continue
            
            key = name.lower()
            
            if key in self.procedures:
                proc = self.procedures[key]
                
                self.exports.append({
                    "kind"          : "procedure",
                    "name"          : name,
                    "mangled"       : proc["mangled"],
                    "export_name"   : name,
                    "return_type"   : None,
                    "params"        : proc.get("params", [])
                })
                continue
            
            raise CompileError(
                ctx,
                "E0019",
                text=f"export symbol not found: {name}"
            )
        
        return None
    
    def visitBlock(self, ctx):
        if ctx is None:
            return None

        local_decls = ctx.localDeclaration()

        if local_decls:
            for decl in local_decls:
                if decl is not None:
                    self.visit(decl)

        stmt_list = ctx.statementList()

        if stmt_list is not None:
            return self.visit(stmt_list)

        return None
    
    def visitBoolXorExpr(self, ctx):
        result_type = self.visit(ctx.boolAndExpr(0))

        # Kein XOR vorhanden: normalen Ausdruck durchreichen
        if len(ctx.boolAndExpr()) == 1:
            return result_type

        if result_type not in ("boolean", "integer"):
            raise CompileError(ctx, "E0005", got=result_type, expected="boolean/integer xor left")

        self.normalize_bool_eax()

        for i in range(1, len(ctx.boolAndExpr())):
            self.emit_push("eax", comment="lhs xor boolean")

            right_type = self.visit(ctx.boolAndExpr(i))

            if right_type not in ("boolean", "integer"):
                raise CompileError(ctx, "E0005", got=right_type, expected="boolean/integer xor right")

            self.normalize_bool_eax()

            self.emit_pop("ebx", comment="lhs xor boolean")
            self.emit_xor("eax", "ebx")
            self.emit_and("eax", 1)

            result_type = "boolean"

        return result_type
    
    def visitBoolOrExpr(self, ctx):
        operands = ctx.boolXorExpr()
        result_type = self.visit(operands[0])

        # Kein OR vorhanden: Typ unverändert weiterreichen.
        if len(operands) == 1:
            return result_type

        # Boolean-Subranges werden intern als Integer gespeichert.
        if result_type not in ("boolean", "integer"):
            raise CompileError(
                ctx,
                "E0005",
                got=result_type,
                expected="boolean/integer or left"
            )

        self.normalize_bool_eax()

        for operand in operands[1:]:
            self.emit_push(
                "eax",
                comment="lhs boolean or"
            )

            right_type = self.visit(operand)

            if right_type not in ("boolean", "integer"):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=right_type,
                    expected="boolean/integer or right"
                )

            self.normalize_bool_eax()

            self.emit_pop(
                "ebx",
                comment="lhs boolean or"
            )

            self.emit_or("eax", "ebx")
            self.emit_and("eax", 1)

            result_type = "boolean"

        return result_type
    
    def visitBoolAndExpr(self, ctx):
        result_type = self.visit(ctx.compareExpr(0))
        
        # Kein AND vorhanden: Typ einfach durchreichen,
        # z.B. integer, boolean, string, ^nil, ^tnode ...
        if len(ctx.compareExpr()) == 1:
            return result_type

        if result_type not in ("boolean", "integer"):
            raise CompileError(ctx, "E0005", got=result_type, expected="boolean/integer 2")

        self.normalize_bool_eax()

        for i in range(1, len(ctx.compareExpr())):
            self.emit_push("eax", comment="lhs boolean")

            right_type = self.visit(ctx.compareExpr(i))

            if right_type not in ("boolean", "integer"):
                raise CompileError(ctx, "E0005", got=right_type, expected="boolean/integer 3")

            self.normalize_bool_eax()

            self.emit_pop("ebx", comment="lhs boolean")
            self.emit_and("eax", "ebx")
            self.emit_and("eax", 1)

        return "boolean"
    
    def visitUnaryNotExpr(self, ctx):
        expr_type = self.visit(ctx.unaryExpr())

        if expr_type not in ("boolean", "integer"):
            raise CompileError(ctx, "E0005", got=expr_type, expected="boolean/integer 4")

        self.emit_cmp("eax", 0)
        self.emit_sete("al")
        self.emit_movzx("eax", "al")

        return "boolean"
    

    def visitBreakStatement(self, ctx):
        if not self.break_label_stack:
            raise CompileError(ctx, "E0006")
        
        self.emit_jmp(self.break_label_stack[-1], comment="break")
        return None

    def visitContinueStatement(self, ctx):
        if not self.continue_label_stack:
            raise CompileError(ctx, "E0006")
        
        self.emit_jmp(self.continue_label_stack[-1], comment="continue")
        return None

    def visitCompareExpr(self, ctx):
        left_type = self.visit(
            ctx.addExpr(0)
        )

        if len(ctx.addExpr()) == 1:
            return left_type

        operator = (
            ctx.compareOp()
            .getText()
            .lower()
        )

        integer_types = (
            "integer",
            "byte",
            "word",
            "cardinal",
            "dword",
            "longint",
            "smallint",
            "shortint",
            "char",
            "boolean"
        )

        def is_integer_like(type_name):
            return (
                type_name in integer_types
                or self.scalar_base_type(type_name)
                in (
                    "integer",
                    "boolean",
                    "char"
                )
            )

        # ----------------------------------------------------------
        # Linken Operanden sichern.
        #
        # Integer/Pointer: EAX
        # Double:          XMM0
        # ----------------------------------------------------------
        if left_type == "double":
            self.emit_sub(
                "rsp",
                8,
                comment="save left double comparison operand"
            )

            self.emit_movsd_store(
                "rsp",
                0,
                "xmm0"
            )
        else:
            self.emit_push(
                "eax",
                comment="save left comparison operand"
            )

        right_type = self.visit(
            ctx.addExpr(1)
        )

        # ----------------------------------------------------------
        # Double-Vergleich, einschließlich gemischter Vergleiche:
        #
        #     Double  < Double
        #     Integer < Double
        #     Double  < Integer
        # ----------------------------------------------------------
        if (
            left_type == "double"
            or right_type == "double"
        ):
            # Rechten Operanden nach XMM1 übernehmen.
            if right_type == "double":
                self.emit_movapd(
                    "xmm1",
                    "xmm0"
                )

            elif is_integer_like(
                right_type
            ):
                self.emit_cvtsi2sd(
                    "xmm1",
                    "eax"
                )

            else:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=right_type,
                    expected="integer/double"
                )

            # Linken Operanden nach XMM0 zurückholen.
            if left_type == "double":
                self.emit_movsd_load(
                    "xmm0",
                    "rsp",
                    0
                )

                self.emit_add(
                    "rsp",
                    8,
                    comment="restore left double comparison operand"
                )

            elif is_integer_like(
                left_type
            ):
                self.emit_pop(
                    "eax",
                    comment="restore left integer comparison operand"
                )

                self.emit_cvtsi2sd(
                    "xmm0",
                    "eax"
                )

            else:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=left_type,
                    expected="integer/double"
                )

            # Flags für XMM0 (links) gegen XMM1 (rechts).
            self.emit_ucomisd(
                "xmm0",
                "xmm1"
            )

            true_label = self.new_named_label(
                "double_compare_true"
            )

            done_label = self.new_named_label(
                "double_compare_done"
            )

            jump_map = {
                "=":  self.emit_je,
                "<>": self.emit_jne,
                "<":  self.emit_jb,
                "<=": self.emit_jbe,
                ">":  self.emit_ja,
                ">=": self.emit_jae,
            }

            jump = jump_map.get(
                operator
            )

            if jump is None:
                raise CompileError(
                    ctx,
                    "E0015",
                    text=(
                        "unsupported comparison operator: "
                        + operator
                    )
                )

            # Standardresultat FALSE.
            self.emit_xor(
                "eax",
                "eax",
                comment="double comparison false"
            )

            jump(
                true_label
            )

            self.emit_jmp(
                done_label
            )

            self.emit_bind_label(
                true_label
            )

            self.emit_mov_imm(
                "eax",
                "1",
                comment="double comparison true"
            )

            self.emit_bind_label(
                done_label
            )

            return "boolean"

        # ----------------------------------------------------------
        # Integer- und Pointerwerte zurückholen.
        # ----------------------------------------------------------
        self.emit_mov(
            "ebx",
            "eax",
            comment="right comparison operand"
        )

        self.emit_pop(
            "eax",
            comment="restore left comparison operand"
        )

        left_resolved_type = self.resolve_type(
            left_type
        )

        right_resolved_type = self.resolve_type(
            right_type
        )

        left_is_class = (
            left_resolved_type in self.classes
        )

        right_is_class = (
            right_resolved_type in self.classes
        )

        left_is_pointer = self.is_pointer_type(
            left_resolved_type,
            include_nil=False
        )

        right_is_pointer = self.is_pointer_type(
            right_resolved_type,
            include_nil=False
        )

        left_is_reference = (
            left_is_pointer
            or left_is_class
        )

        right_is_reference = (
            right_is_pointer
            or right_is_class
        )

        left_is_nil = (
            left_type in (
                "nil",
                "^nil"
            )
        )

        right_is_nil = (
            right_type in (
                "nil",
                "^nil"
            )
        )

        # ----------------------------------------------------------
        # Pointer = nil / Pointer <> nil
        # ----------------------------------------------------------
        reference_comparison = (
            (
                left_is_reference
                and right_is_nil
            )
            or
            (
                left_is_nil
                and right_is_reference
            )
            or
            (
                left_is_reference
                and right_is_reference
            )
        )

        if reference_comparison:
            if operator not in (
                "=",
                "<>"
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=operator,
                    expected="= or <> for pointer comparison"
                )

            self.emit_cmp(
                "eax",
                "ebx"
            )

            if operator == "=":
                self.emit_sete(
                    "al"
                )
            else:
                self.emit_setne(
                    "al"
                )

            self.emit_movzx(
                "eax",
                "al"
            )

            return "boolean"

        # ----------------------------------------------------------
        # Normale Integervergleiche.
        # ----------------------------------------------------------
        if not is_integer_like(
            left_type
        ):
            raise CompileError(
                ctx,
                "E0005",
                got=left_type,
                expected="integer/double"
            )

        if not is_integer_like(
            right_type
        ):
            raise CompileError(
                ctx,
                "E0005",
                got=right_type,
                expected="integer/double"
            )

        self.emit_cmp(
            "eax",
            "ebx"
        )

        if operator == "=":
            self.emit_sete("al")

        elif operator == "<>":
            self.emit_setne("al")

        elif operator == "<":
            self.emit_setl("al")

        elif operator == "<=":
            self.emit_setle("al")

        elif operator == ">":
            self.emit_setg("al")

        elif operator == ">=":
            self.emit_setge("al")

        else:
            raise CompileError(
                ctx,
                "E0015",
                text=(
                    "unsupported comparison operator: "
                    + operator
                )
            )

        self.emit_movzx(
            "eax",
            "al"
        )

        return "boolean"

    def visitRecordDeclaration(self, ctx):
        record_name = ctx.IDENT().getText()
        is_packed = ctx.PACKED() is not None

        fields = []

        for field_ctx in ctx.recordFieldDeclaration():
            field_type = (
                field_ctx
                .typeName()
                .getText()
            )

            for ident in (
                field_ctx
                .identList()
                .IDENT()
            ):
                fields.append((
                    ident.getText(),
                    field_type
                ))

        self.declare_record(
            ctx,
            record_name,
            fields,
            packed=is_packed
        )

        if self.collect_pui_interface:
            self.pui_add_record(
                record_name
            )

        return None
    
    def visitArrayType(self, ctx):
        dimensions = []

        if ctx.arrayRange():
            for r in ctx.arrayRange():
                min_value = int(r.expr(0).getText())
                max_value = int(r.expr(1).getText())

                dimensions.append({
                    "min": min_value,
                    "max": max_value
                })

            is_dynamic = False
        else:
            is_dynamic = True

        element_type = ctx.typeName().getText()

        return {
            "kind": "array",
            "dimensions": dimensions,
            "element_type": element_type,
            "is_dynamic": is_dynamic
        }
        
    def array_total_count(self, array_info):
        total = 1
        for dim in array_info["dimensions"]:
            total *= (dim["max"] - dim["min"] + 1)
        return total
    
    def visitArrayDeclaration(self, ctx):
        array_name = ctx.IDENT().getText()

        array_type = self.visit(ctx.arrayType())

        dimensions   = array_type["dimensions"]
        element_type = array_type["element_type"]
        
        if not dimensions:
            resolved_type = self.resolve_type(element_type)
            element_size  = self.type_size(ctx, resolved_type)

            self.arrays[array_name.lower()] = ArrayInfo(
                name         = array_name,
                index_min    = 0,
                index_max    = -1,
                element_type = resolved_type,
                element_size = element_size,
                size         = 0,
                init_values  = [],
                dimensions   = [],
                is_dynamic   = True
            )

            return None
            
        # vorerst Kompatibilität für alte eindimensionale Funktionen
        index_min = dimensions[0]["min"]
        index_max = dimensions[0]["max"]

        resolved_type = self.resolve_type(element_type)

        init_values = []

        if ctx.arrayInitializer():
            value_list = ctx.arrayInitializer().arrayValueList()

            if value_list:
                for value_ctx in value_list.constValue():
                    text = value_ctx.getText()

                    if resolved_type == "integer":
                        init_values.append(int(text, 0))
                    elif resolved_type == "double":
                        init_values.append(float(text))
                    elif resolved_type == "string":
                        init_values.append(text[1:-1])
                    else:
                        raise CompileError(ctx, "E0014", var_type=resolved_type)

        self.declare_array(
            ctx,
            array_name,
            index_min,
            index_max,
            element_type,
            init_values,
            dimensions
        )

        return None
    
    def visitConstDeclaration(self, ctx):
        for item in ctx.constItem():
            self.visit(item)

        return None

    @staticmethod
    def parse_pascal_integer_literal(value_text):
        """
        Wandelt eine ganzzahlige Pascal-Konstante in einen Python-Integer um.

        Unterstützt werden neben Dezimalzahlen auch die Pascal-Präfixe:

            $FF     hexadezimal
            %1010   binär
            &377    oktal

        Ein vorangestelltes Plus- oder Minuszeichen ist ebenfalls erlaubt.
        """
        text = str(
            value_text
        ).strip().replace(
            "_",
            ""
        )

        if not text:
            raise ValueError(
                "empty Pascal integer literal"
            )

        sign = 1

        if text[0] in (
            "+",
            "-"
        ):
            if text[0] == "-":
                sign = -1

            text = text[1:]

        if not text:
            raise ValueError(
                "invalid Pascal integer literal"
            )

        if text.startswith("$"):
            base = 16
            text = text[1:]

        elif text.startswith("%"):
            base = 2
            text = text[1:]

        elif text.startswith("&"):
            base = 8
            text = text[1:]

        elif text.lower().startswith("0x"):
            base = 16
            text = text[2:]

        else:
            base = 10

        if not text:
            raise ValueError(
                "invalid Pascal integer literal"
            )

        return sign * int(
            text,
            base
        )

    def parse_char_code(
        self,
        ctx,
        text
    ):
        if not text.startswith("#"):
            raise CompileError(
                ctx,
                "E0005",
                got=text,
                expected="character code"
            )

        value_text = text[1:]

        if value_text.startswith("$"):
            value = int(
                value_text[1:],
                16
            )
        else:
            value = int(
                value_text,
                10
            )

        if value < 0 or value > 255:
            raise CompileError(
                ctx,
                "E0005",
                got=str(value),
                expected="character code 0..255"
            )

        return value
    
    def visitConstItem(self, ctx):
        name = ctx.IDENT().getText()

        # ============================================================
        # Typisierte konstante Arrays
        # ============================================================
        if ctx.arrayType() is not None:
            array_type = self.visit(
                ctx.arrayType()
            )

            dimensions = array_type[
                "dimensions"
            ]

            element_type = self.resolve_type(
                array_type["element_type"]
            )

            if not dimensions:
                raise CompileError(
                    ctx,
                    "E0014",
                    var_type=(
                        "dynamic constant array"
                    )
                )

            value_list = ctx.arrayValueList()

            init_values = []

            if value_list is not None:
                for value_ctx in value_list.constValue():
                    text = value_ctx.getText()

                    # --------------------------------------------
                    # Integer/Subrange
                    # --------------------------------------------
                    if element_type in (
                        "integer",
                        "byte",
                        "word",
                        "dword",
                        "cardinal",
                        "longint",
                        "smallint",
                        "shortint"
                    ):
                        if text.startswith("$"):
                            value = int(
                                text[1:],
                                16
                            )
                        elif text.startswith("#"):
                            value = self.parse_char_code(
                                value_ctx,
                                text
                            )
                        else:
                            value = int(
                                text,
                                10
                            )

                        init_values.append(value)

                    # --------------------------------------------
                    # Char/AnsiChar
                    # --------------------------------------------
                    elif element_type in (
                        "char",
                        "ansichar"
                    ):
                        if text.startswith("#"):
                            value = self.parse_char_code(
                                value_ctx,
                                text
                            )

                        elif (
                            len(text) >= 2
                            and text[0] == "'"
                            and text[-1] == "'"
                        ):
                            literal = text[1:-1]

                            # Pascal-Escaping: '' ergibt '
                            literal = literal.replace(
                                "''",
                                "'"
                            )

                            if len(literal) != 1:
                                raise CompileError(
                                    value_ctx,
                                    "E0005",
                                    got=literal,
                                    expected="single character"
                                )

                            value = ord(literal)

                        else:
                            raise CompileError(
                                value_ctx,
                                "E0005",
                                got=text,
                                expected="character"
                            )

                        init_values.append(value)

                    # --------------------------------------------
                    # Double
                    # --------------------------------------------
                    elif element_type == "double":
                        init_values.append(
                            float(text)
                        )

                    # --------------------------------------------
                    # String
                    # --------------------------------------------
                    elif element_type == "string":
                        if not (
                            len(text) >= 2
                            and text[0] == "'"
                            and text[-1] == "'"
                        ):
                            raise CompileError(
                                value_ctx,
                                "E0005",
                                got=text,
                                expected="string"
                            )

                        init_values.append(
                            text[1:-1].replace(
                                "''",
                                "'"
                            )
                        )

                    else:
                        raise CompileError(
                            ctx,
                            "E0014",
                            var_type=element_type
                        )

            expected_count = 1

            for dimension in dimensions:
                expected_count *= (
                    dimension["max"]
                    - dimension["min"]
                    + 1
                )

            if len(init_values) != expected_count:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=str(len(init_values)),
                    expected=str(expected_count)
                )

            self.declare_const_array(
                ctx=ctx,
                name=name,
                dimensions=dimensions,
                element_type=element_type,
                init_values=init_values
            )

            return None

        # ============================================================
        # Normale skalare Konstante
        # ============================================================
        value_ctx = ctx.constValue()

        if value_ctx is None:
            raise CompileError(
                ctx,
                "E0015",
                text="missing constant value"
            )

        value_text = value_ctx.getText()

        if value_text.startswith("#"):
            value = self.parse_char_code(
                value_ctx,
                value_text
            )
            typ = "char"

        elif (
            value_text.startswith("'")
            and value_text.endswith("'")
        ):
            value = (
                value_text[1:-1]
                .replace("''", "'")
            )

            typ = (
                "char"
                if len(value) == 1
                else "string"
            )

        elif "." in value_text:
            value = float(value_text)
            typ = "double"

        else:
            value = self.parse_pascal_integer_literal(
                value_text
            )
            typ = "integer"

        self.declare_const(
            ctx,
            name,
            value,
            typ
        )

        # Nur Konstanten aus dem Interface einer Root-Unit sind öffentlich.
        # Konstanten aus dem Implementation-Teil bleiben unit-lokal.
        if self.collect_pui_interface:
            self.pui_add_constant(
                name
            )

        return None
    
    def visitEnumDeclaration(self, ctx):
        enum_name = ctx.IDENT().getText()

        values = []
        current_value = 0

        for enum_ctx in ctx.enumValueList().enumValue():
            name        = enum_ctx.IDENT().getText()
            number_node = enum_ctx.NUMBER()

            if number_node is not None:
                current_value = int(number_node.getText(), 0)

            values.append((name, current_value))
            current_value += 1

        self.declare_enum(ctx, enum_name, values)
        return None
    
    def visitTryStatement(self, ctx):
        if ctx.EXCEPT():
            return self.emit_try_except_statement(ctx)

        if ctx.FINALLY():
            self.visit(ctx.statementList(0))
            self.visit(ctx.statementList(1))
            return None

        return None
        
        
        if ctx.FINALLY():
            self.visit(ctx.statementList(0))
            self.visit(ctx.statementList(1))
            return None

        if ctx.EXCEPT():
            except_label = self.new_named_label("except")
            end_label    = self.new_named_label("endtry")

            try_esp_symbol = None

            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                try_esp_symbol = self.new_named_label("__try_esp")
                self.writer.add_data_i32(try_esp_symbol, 0)
                self.writer.emit_mov_data_label_r32(try_esp_symbol, "esp")

            frame = {
                "except_label": except_label,
                "end_label": end_label,
                "esp_symbol": try_esp_symbol,
            }

            self.try_except_stack.append(frame)

            # try-block
            self.visit(ctx.statementList(0))

            self.try_except_stack.pop()

            # kein Fehler -> except überspringen
            self.emit_jmp(end_label)

            # except-block
            self.emit_bind_label(except_label)

            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                if try_esp_symbol:
                    self.writer.emit_mov_reg_from_data_label32("esp", try_esp_symbol)

                self.writer.emit_lea_reg_data_label("esi", "ctx")

            self.visit(ctx.statementList(1))

            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.writer.emit_lea_reg_data_label("esi", "ctx")

            self.emit_bind_label(end_label)

            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.writer.emit_lea_reg_data_label("esi", "ctx")

            return None

        return None
    
    def case_label_value(self, ctx, label_ctx):
        if label_ctx.NUMBER():
            return int(label_ctx.NUMBER().getText(), 0)

        if label_ctx.IDENT():
            name = label_ctx.IDENT().getText()
            const_info = self.find_const(name)

            if const_info is None:
                raise CompileError(label_ctx, "E0001", name=name)

            if const_info["type"] != "integer":
                raise CompileError(label_ctx, "E0005", got=const_info["type"], expected="integer")

            return int(const_info["value"])

        raise CompileError(label_ctx, "E0015", text=label_ctx.getText())
    
    def visitCaseStatement(self, ctx):
        end_label  = self.new_named_label("case_end")
        else_label = self.new_named_label("case_else")

        item_labels = []

        expr_type = self.visit(ctx.expr())

        if expr_type != "integer":
            raise CompileError(ctx, "E0005", got=expr_type, expected="integer")

        self.emit_mov("ebx", "eax", comment='case selector')

        items = list(ctx.caseItem())

        for index, item in enumerate(items):
            item_label = self.new_named_label(f"case_item_{index}")
            item_labels.append((item, item_label))

            for label_ctx in item.caseLabelList().caseLabel():
                value = self.case_label_value(ctx, label_ctx)

                self.emit_cmp("ebx", value)
                self.emit_je(item_label)

        if ctx.caseElse():
            self.emit_jmp(else_label)
        else:
            self.emit_jmp(end_label)

        for item, item_label in item_labels:
            self.emit_bind_label(item_label)
            self.visit(item.statement())
            self.emit_jmp(end_label)

        if ctx.caseElse():
            self.emit_bind_label(else_label)
            self.visit(ctx.caseElse().statementList())

        self.emit_bind_label(end_label)
        return None
    
    def visitStatementList(self, ctx):
        if ctx is None:
            return None
        
        for st in ctx.statement():
            if st is not None:
                self.visit(st)
        
        return None
    
    def visitStatement(self, ctx):
        if ctx.procedureCallStatement():
            return self.visit(ctx.procedureCallStatement())
        
        if ctx.inheritedStatement():
            return self.visit(ctx.inheritedStatement())
        
        if ctx.tryStatement():
            return self.visit(ctx.tryStatement())
        
        if ctx.assignment():
            return self.visit(ctx.assignment())
        
        if ctx.writeLnStatement():
            return self.visit(ctx.writeLnStatement())
        
        if ctx.ifStatement():
            return self.visit(ctx.ifStatement())
        
        if ctx.whileStatement():
            return self.visit(ctx.whileStatement())
        
        if ctx.repeatStatement():
            return self.visit(ctx.repeatStatement())
        
        if ctx.forStatement():
            return self.visit(ctx.forStatement())
        
        if ctx.exitStatement():
            return self.visit(ctx.exitStatement())
        
        if ctx.caseStatement():
            return self.visit(ctx.caseStatement())
        
        if ctx.breakStatement():
            return self.visit(ctx.breakStatement())
        
        if ctx.continueStatement():
            return self.visit(ctx.continueStatement())
        
        if ctx.compoundStatement():
            return self.visit(ctx.compoundStatement())
        
        return None

    def compiler_directive_parts(self, ctx):
        text = ctx.getText()

        # {$link foo.o}
        # {$linklib libfoo.a}
        # {$R foo.res}
        text = text[2:-1].strip()

        parts = text.split(None, 1)

        if len(parts) != 2:
            return None, None

        cmd = parts[0].strip().lower()
        arg = parts[1].strip()

        # Standard-Pascal-Syntax:
        #
        #   {$L crc16.o}
        #
        # Im Gegensatz zu {$link ...} soll das Objekt physisch in die
        # erzeugte Unit-Objektdatei eingebettet werden.
        if cmd == "l":
            cmd = "embed"

        # Win32-Ressourcenobjekt im COFF32-Format:
        #
        #   {$R application.res}
        #
        # Die Kurzform wird intern von {$L ...} getrennt behandelt,
        # weil die .rsrc-Sektion erst beim finalen EXE-/DLL-Link in
        # das PE-Image aufgenommen werden darf.
        elif cmd == "r":
            cmd = "resource"

        # Optional gesetzte Anführungszeichen entfernen
        if (
            len(arg) >= 2
            and arg[0] == arg[-1]
            and arg[0] in ("'", '"')
        ):
            arg = arg[1:-1]

        return cmd, arg

    def pui_target_info(self):
        target = CDATA.args_target.lower()

        if target in ("nt35", "winnt", "win32"):
            return {
                "target": target,
                "object_format": "coff32",
                "machine": "i386",
                "pointer_size": 4,
                "calling_convention": "cdecl"
            }

        if target == "win64":
            return {
                "target": target,
                "object_format": "coff64",
                "machine": "amd64",
                "pointer_size": 8,
                "calling_convention": "win64"
            }

        raise RuntimeError(
            f"PUI target currently unsupported: {target}"
        )

    def pui_param_data(self, params):
        result = []

        for param in params:
            result.append({
                "name": param["name"],
                "type": self.resolve_type(param["type"]),
                "is_var": bool(param.get("is_var", False))
            })

        return result

    def begin_unit_pui(self, unit_name):
        target_info = self.pui_target_info()

        self.pending_pui = {
            "format": "dBase2Many Pascal Unit Interface",
            "version": 1,

            "unit": {
                "name": unit_name,
                "normalized_name": self.normalize_unit_name(
                    unit_name
                )
            },

            "target": target_info,

            "object": {
                "file": None,
                "format": target_info["object_format"],
                "machine": target_info["machine"]
            },

            "uses": {
                "interface": [],
                "implementation": []
            },

            # DLL-Imports, die von der erzeugten Unit-Objektdatei
            # referenziert werden. Das Hauptprogramm muss für diese
            # internen COFF-Symbole Import-Thunks erzeugen.
            "imports": {},

            "initialization": {
                "symbol": None
            },

            "finalization": {
                "symbol": None
            },

            # Öffentliche Compile-Time-Konstanten aus dem Interface.
            # Sie besitzen kein eigenes COFF-Symbol.
            "constants": [],

            # Compile-Time-Typinformationen
            "types": {
                "aliases": [],
                "subranges": [],
                "records": []
            },

            # Linkbare Routinen und Klassen
            "symbols": {
                "functions": [],
                "procedures": [],
                "classes": []
            },
            "link": {
                # Nur verzögert zu linkende Dateien.
                "objects": list(
                    self.root_link_objects
                ),

                "archives": list(
                    self.root_link_archives
                ),

                "resources": list(
                    self.root_resource_files
                ),

                # Nur Information; diese Dateien sind bereits physisch in
                # der Unit-Objektdatei enthalten.
                "embedded_objects": list(
                    self.root_embedded_objects
                )
            },
        }

    def pui_add_constant(
        self,
        name
    ):
        if self.pending_pui is None:
            return

        key = str(
            name
        ).lower()

        info = self.constants.get(
            key
        )

        if info is None:
            raise RuntimeError(
                f"constant not registered: {name}"
            )

        if info.get("kind") == "array":
            raise RuntimeError(
                f"PUI constant arrays are not supported: {name}"
            )

        typ = str(
            info.get(
                "type",
                ""
            )
        ).lower()

        value = info.get(
            "value"
        )

        if typ == "integer":
            value = int(
                value
            )

        elif typ == "boolean":
            value = (
                1
                if bool(value)
                else 0
            )

        elif typ == "double":
            # Text vermeidet unnötige zusätzliche Rundung beim JSON-
            # Export und passt zu emit_load_double_literal().
            value = str(
                value
            )

        elif typ == "string":
            value = str(
                value
            )

        elif typ == "char":
            value = str(
                value
            )

            if len(value) != 1:
                raise RuntimeError(
                    f"invalid character constant: {name}"
                )

        else:
            raise RuntimeError(
                f"unsupported PUI constant type "
                f"for {name}: {typ}"
            )

        entries = self.pending_pui.setdefault(
            "constants",
            []
        )

        for old_item in entries:
            if (
                str(
                    old_item.get(
                        "name",
                        ""
                    )
                ).lower()
                == key
            ):
                return

        entries.append({
            "name": info["name"],
            "scoped_name": self.unit_scoped_name(
                info["name"]
            ),
            "type": typ,
            "value": value
        })

    def pui_add_record(
        self,
        record_name
    ):
        if self.pending_pui is None:
            return

        key = str(record_name).lower()
        info = self.records.get(key)

        if info is None:
            raise RuntimeError(
                f"record type not registered: {record_name}"
            )

        entries = (
            self.pending_pui
            .setdefault("types", {})
            .setdefault("records", [])
        )

        if any(
            str(item.get("name", "")).lower() == key
            for item in entries
        ):
            return

        fields = []

        for field_info in info.fields.values():
            fields.append({
                "name": field_info.name,
                "type": field_info.type,
                "offset": int(field_info.offset),
                "size": int(field_info.size)
            })

        entries.append({
            "kind": "record",
            "name": info.name,
            "packed": bool(
                getattr(info, "packed", False)
            ),
            "alignment": int(
                getattr(info, "alignment", 1)
            ),
            "size": int(info.size),
            "fields": fields
        })

    def pui_add_type_alias(
        self,
        name,
        target_type
    ):
        if self.pending_pui is None:
            return

        type_section = self.pending_pui.setdefault(
            "types",
            {}
        )

        entries = type_section.setdefault(
            "aliases",
            []
        )

        key = str(name).lower()

        for old_item in entries:
            if (
                str(old_item.get("name", "")).lower()
                == key
            ):
                return

        entries.append({
            "kind": "alias",
            "name": name,
            "target_type": str(target_type).lower()
        })

    def pui_add_subrange_type(self, name):
        if self.pending_pui is None:
            return

        key = str(name).lower()

        info = self.subrange_types.get(key)

        if info is None:
            raise RuntimeError(
                f"subrange type not registered: {name}"
            )

        type_section = self.pending_pui.setdefault(
            "types",
            {}
        )

        entries = type_section.setdefault(
            "subranges",
            []
        )

        for old_item in entries:
            if (
                str(old_item.get("name", "")).lower()
                == key
            ):
                return

        entries.append({
            "kind": "subrange",
            "name": info.name,
            "base_type": info.base_type,
            "min_value": int(info.min_value),
            "max_value": int(info.max_value),
            "size": int(info.size),
            "signed": bool(info.signed)
        })

    def pui_add_symbol(self, section, item):
        if self.pending_pui is None:
            return

        entries = self.pending_pui["symbols"][section]

        if section == "classes":
            key = str(item.get("name", "")).lower()

            for old_item in entries:
                if str(old_item.get("name", "")).lower() == key:
                    return
        else:
            symbol = item.get("symbol")

            for old_item in entries:
                if old_item.get("symbol") == symbol:
                    return

        entries.append(item)

    def visitShiftExpr(self, ctx):
        operands = ctx.term()

        if not operands:
            raise CompileError(
                ctx,
                "E0019",
                text="shift expression has no operand"
            )

        result_type = self.visit(
            ctx.term(0)
        )

        # Kein SHL/SHR vorhanden:
        # Typ unverändert weiterreichen.
        #
        # Das ist wichtig für:
        #   Ctx = nil
        #   S = ''
        #   Flag = True
        #   Obj <> nil
        if len(operands) == 1:
            return result_type

        integer_types = (
            "integer",
            "byte",
            "word",
            "cardinal",
            "dword",
            "longint",
            "smallint",
            "shortint",
            "char"
        )

        left_scalar_type = self.scalar_base_type(
            result_type
        )

        if (
            result_type not in integer_types
            and left_scalar_type != "integer"
        ):
            raise CompileError(
                ctx,
                "E0005",
                got=result_type,
                expected="integer"
            )

        for index in range(
            1,
            len(operands)
        ):
            operator = (
                ctx.getChild(
                    2 * index - 1
                )
                .getText()
                .lower()
            )

            # Linken Wert sichern.
            if CDATA.args_target in (
                "nt35",
                "winnt",
                "win32"
            ):
                self.emit_push(
                    "eax",
                    comment="save shift value"
                )
            else:
                self.emit_push(
                    "rax",
                    comment="save shift value"
                )

            shift_type = self.visit(
                ctx.term(index)
            )

            shift_scalar_type = self.scalar_base_type(
                shift_type
            )

            if (
                shift_type not in integer_types
                and shift_scalar_type != "integer"
            ):
                if CDATA.args_target in (
                    "nt35",
                    "winnt",
                    "win32"
                ):
                    self.emit_pop("eax")
                else:
                    self.emit_pop("rax")

                raise CompileError(
                    ctx,
                    "E0005",
                    got=shift_type,
                    expected="integer"
                )

            if CDATA.args_target in (
                "nt35",
                "winnt",
                "win32"
            ):
                # ECX = Shiftanzahl
                self.emit_mov(
                    "ecx",
                    "eax",
                    comment="shift count"
                )

                # EAX = linker Operand
                self.emit_pop(
                    "eax",
                    comment="restore shift value"
                )

                if operator == "shl":
                    self.backend.emit_shl_reg_cl(
                        "eax"
                    )

                elif operator == "shr":
                    self.backend.emit_shr_reg_cl(
                        "eax"
                    )

                else:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "unsupported shift operator: "
                            + operator
                        )
                    )

            else:
                self.emit_mov(
                    "rcx",
                    "rax",
                    comment="shift count"
                )

                self.emit_pop(
                    "rax",
                    comment="restore shift value"
                )

                if operator == "shl":
                    self.backend.emit_shl_reg_cl(
                        "rax"
                    )

                elif operator == "shr":
                    self.backend.emit_shr_reg_cl(
                        "rax"
                    )

                else:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "unsupported shift operator: "
                            + operator
                        )
                    )

            result_type = "integer"

        return result_type
    
    def pui_add_dll_import(
        self,
        dll_name,
        import_item
    ):
        if self.pending_pui is None:
            return

        dll_name = os.path.basename(
            str(dll_name).strip()
        )

        if not dll_name:
            raise RuntimeError(
                "PUI DLL import has no library name"
            )

        if not isinstance(import_item, dict):
            raise RuntimeError(
                "PUI DLL import item must be a dictionary"
            )

        symbol = import_item.get(
            "symbol"
        )

        import_name = import_item.get(
            "name"
        )

        ordinal = import_item.get(
            "ordinal"
        )

        if not isinstance(symbol, str) or not symbol:
            raise RuntimeError(
                "PUI DLL import has no internal symbol"
            )

        if (
            not isinstance(import_name, str)
            or not import_name
        ):
            import_name = None

        if import_name is None and ordinal is None:
            raise RuntimeError(
                "PUI DLL import requires a name or ordinal: "
                + symbol
            )

        imports = self.pending_pui.setdefault(
            "imports",
            {}
        )

        entries = imports.setdefault(
            dll_name,
            []
        )

        item = {
            "symbol": symbol
        }

        if import_name is not None:
            item["name"] = import_name

        if ordinal is not None:
            item["ordinal"] = int(
                ordinal
            )

        for old_item in entries:
            if (
                isinstance(old_item, dict)
                and old_item.get("symbol") == symbol
            ):
                if old_item != item:
                    raise RuntimeError(
                        "conflicting PUI DLL import symbol "
                        + symbol
                    )

                return

        entries.append(
            item
        )

    def visitFunctionHeader(self, ctx):
        name   = ctx.IDENT().getText()
        scoped = self.unit_scoped_name(name)
        key    = name.lower()

        params = self.collect_formal_params(ctx)

        return_type = self.resolve_type(
            ctx.typeName().getText()
        )

        convention = (
            self.local_routine_calling_convention(
                ctx
            )
        )

        if self.routine_is_external(ctx):
            dll_name = self.routine_external_library(
                ctx
            )

            if dll_name is None:
                return self.register_local_external_routine(
                    ctx=ctx,
                    kind="function",
                    name=name,
                    params=params,
                    return_type=return_type,
                    convention=convention
                )

            return self.register_external_routine(
                ctx=ctx,
                kind="function",
                name=name,
                params=params,
                return_type=return_type,
                spec_ctx=ctx.externalRoutineDirective(),
                convention=convention
            )
        
        mangled = self.fpc_mangle_routine(
            name,
            params,
            self.current_unit if self.current_unit else None
        )

        if key not in self.functions:
            self.functions[key] = {
                "name": name,
                "scoped_name": scoped,
                "return_type": return_type,
                "label": None,
                "mangled": mangled,
                "params": params
            }

        self.functions[name.lower()] = self.functions[key]

        if self.collect_pui_interface:
            self.pui_add_symbol(
                "functions",
                {
                    "name": name,
                    "scoped_name": scoped,
                    "symbol": mangled,
                    "params": self.pui_param_data(params),
                    "return_type": return_type,
                    "calling_convention": convention
                }
            )

        return None
    
    def visitProcedureHeader(self, ctx):
        name   = ctx.IDENT().getText()
        scoped = self.unit_scoped_name(name)
        key    = name.lower()

        params = self.collect_formal_params(ctx)

        convention = (
            self.local_routine_calling_convention(
                ctx
            )
        )

        if self.routine_is_external(ctx):
            dll_name = self.routine_external_library(
                ctx
            )

            if dll_name is None:
                return self.register_local_external_routine(
                    ctx=ctx,
                    kind="procedure",
                    name=name,
                    params=params,
                    return_type=None,
                    convention=convention
                )

            return self.register_external_routine(
                ctx=ctx,
                kind="procedure",
                name=name,
                params=params,
                return_type=None,
                spec_ctx=ctx.externalRoutineDirective(),
                convention=convention
            )

        mangled = self.fpc_mangle_routine(
            name,
            params,
            self.current_unit if self.current_unit else None
        )

        if key not in self.procedures:
            self.procedures[key] = {
                "name"       : name,
                "scoped_name": scoped,
                "label"      : None,
                "mangled"    : mangled,
                "params"     : params
            }

        self.procedures[name.lower()] = self.procedures[key]
        
        if self.collect_pui_interface:
            self.pui_add_symbol(
                "procedures",
                {
                    "name"       : name,
                    "scoped_name": scoped,
                    "symbol"     : mangled,
                    "params"     : self.pui_param_data(params),
                    "calling_convention": convention
                }
            )

        return None
    
    def visitTypeSection(self, ctx):
        for decl in ctx.typeDeclaration():
            self.visit(decl)

        return None
        
    def visitVarSection(self, ctx):
        for decl in ctx.varDeclaration():
            self.visit(decl)
        return None
    
    def visitVarDeclaration(self, ctx):
        vtype_ctx = ctx.varType()

        if vtype_ctx.arrayType():
            array_type = self.visit(vtype_ctx.arrayType())

            dimensions   = array_type["dimensions"]
            element_type = array_type["element_type"]
            is_dynamic   = array_type.get("is_dynamic", False)

            for ident in ctx.identList().IDENT():
                name = ident.getText()

                if is_dynamic:
                    # anonymen dynamischen Array-Typ anlegen
                    array_type_name = "$dynarray_" + name.lower()
                    resolved_element_type = self.resolve_type(element_type)
                    
                    self.arrays[array_type_name] = ArrayInfo(
                        name         = array_type_name,
                        index_min    = 0,
                        index_max    = -1,
                        element_type = resolved_element_type,
                        element_size = self.type_size(ctx, resolved_element_type),
                        size         = 8,
                        init_values  = [],
                        dimensions   = [],
                        is_dynamic   = True
                    )

                    if self.local_var_stack:
                        self.declare_local_var(ctx, name, array_type_name)
                    else:
                        self.declare_var(ctx, name, array_type_name)
                else:
                    raise CompileError(ctx, "E0005", got="static inline array", expected="named array type")
            
            return None

        vtype = vtype_ctx.typeName().getText()

        for ident in ctx.identList().IDENT():
            name = ident.getText()

            if self.local_var_stack:
                self.declare_local_var(ctx, name, vtype)
            else:
                self.declare_var(ctx, name, vtype)

        return None
    

    def pui_add_class(
        self,
        class_name
    ):
        if self.pending_pui is None:
            return

        class_key = class_name.lower()
        cls = self.classes[
            class_key
        ]

        fields = []

        for field in cls.fields.values():
            # Geerbte Felder werden für ein vollständiges Layout
            # weiterhin gespeichert.
            fields.append({
                "name": field.name,
                "type": self.resolve_type(
                    field.type
                ),
                "offset": field.offset,
                "size": field.size,
                "visibility": getattr(
                    field,
                    "visibility",
                    "public"
                )
            })

        methods = []

        for overloads in cls.methods.values():
            for method in overloads:
                if method.owner != class_key:
                    continue

                methods.append({
                    "name": method.name,
                    "kind": method.kind,
                    "symbol": method.mangled,
                    "params": self.pui_param_data(
                        method.params
                    ),
                    "return_type": (
                        self.resolve_type(
                            method.return_type
                        )
                        if method.return_type
                        else None
                    ),
                    "visibility": method.visibility,
                    "calling_convention": "cdecl",
                    "is_virtual": bool(
                        getattr(
                            method,
                            "is_virtual",
                            False
                        )
                    ),
                    "is_override": bool(
                        getattr(
                            method,
                            "is_override",
                            False
                        )
                    ),
                    "vmt_offset": getattr(
                        method,
                        "vmt_offset",
                        None
                    )
                })

        properties = []

        for prop in getattr(
            cls,
            "properties",
            {}
        ).values():
            properties.append({
                "name": prop.name,
                "type": self.resolve_type(
                    prop.ptype
                ),
                "visibility": prop.visibility,
                "read": prop.read_name,
                "write": prop.write_name
            })

        self.pui_add_symbol(
            "classes",
            {
                "name": cls.name,
                "parent": cls.parent,
                "size": cls.size,
                "vmt_symbol": cls.vmt_symbol,
                "class_name_symbol": (
                    cls.class_name_symbol
                ),
                "fields": fields,
                "methods": methods,
                "properties": properties
            }
        )


    def visitClassDeclaration(
        self,
        ctx
    ):
        class_name = (
            ctx.IDENT().getText()
        )

        fields = []
        methods = []
        properties = {}

        parent_name = None
        current_visibility = "public"

        if ctx.classParent():
            parent_name = (
                ctx.classParent()
                .IDENT()
                .getText()
            )

        for member in (
            ctx.classBody()
            .classMember()
        ):
            if member.visibilitySection():
                current_visibility = (
                    member
                    .visibilitySection()
                    .getText()
                    .lower()
                )

                continue

            if member.classFieldDeclaration():
                field_ctx = (
                    member
                    .classFieldDeclaration()
                )

                field_type = (
                    field_ctx
                    .typeName()
                    .getText()
                )

                for ident in (
                    field_ctx
                    .identList()
                    .IDENT()
                ):
                    fields.append((
                        ident.getText(),
                        field_type,
                        current_visibility
                    ))

                continue

            declaration = None
            method_kind = None
            return_type = None

            if member.constructorDeclaration():
                declaration = (
                    member
                    .constructorDeclaration()
                )

                method_kind = "constructor"

            elif member.destructorDeclaration():
                declaration = (
                    member
                    .destructorDeclaration()
                )

                method_kind = "destructor"

            elif member.classFunctionDeclaration():
                declaration = (
                    member
                    .classFunctionDeclaration()
                )

                method_kind = "function"

                return_type = self.resolve_type(
                    declaration
                    .typeName()
                    .getText()
                )

            elif member.classProcedureDeclaration():
                declaration = (
                    member
                    .classProcedureDeclaration()
                )

                method_kind = "procedure"

            if declaration is not None:
                method_name = (
                    declaration
                    .IDENT()
                    .getText()
                )

                params = self.collect_formal_params(
                    declaration
                )

                flags = self.method_directive_flags(
                    declaration
                )

                mangled = self.fpc_mangle_class_method(
                    class_name,
                    method_name,
                    params,
                    (
                        self.current_unit
                        if self.current_unit
                        else self.program_name
                    )
                )

                methods.append({
                    "name": method_name,
                    "kind": method_kind,
                    "label": self.new_named_label(
                        "class_"
                        + class_name
                        + "_"
                        + method_name
                    ),
                    "mangled": mangled,
                    "params": params,
                    "return_type": return_type,
                    "visibility": current_visibility,
                    "virtual": flags["virtual"],
                    "override": flags["override"]
                })

                continue

            if member.propertyDeclaration():
                prop = (
                    member
                    .propertyDeclaration()
                )

                prop_name = (
                    prop.IDENT().getText()
                )

                prop_type = self.resolve_type(
                    prop.typeName().getText()
                )

                read_name = None
                write_name = None

                for accessor in (
                    prop.propertyAccessor()
                ):
                    accessor_text = (
                        accessor
                        .getText()
                        .lower()
                    )

                    accessor_name = (
                        accessor
                        .IDENT()
                        .getText()
                    )

                    if accessor_text.startswith(
                        "read"
                    ):
                        read_name = accessor_name

                    elif accessor_text.startswith(
                        "write"
                    ):
                        write_name = accessor_name

                properties[
                    prop_name.lower()
                ] = PropertyInfo(
                    name=prop_name,
                    ptype=prop_type,
                    visibility=current_visibility,
                    read_name=read_name,
                    write_name=write_name
                )

        self.declare_class(
            ctx,
            class_name,
            fields,
            methods,
            properties,
            parent_name=parent_name
        )

        if self.collect_pui_interface:
            self.pui_add_class(
                class_name
            )

        # Das Datensymbol muss vor Konstruktor-Code existieren.
        self.emit_class_vmt_data(
            class_name
        )

        return None

    def register_pui_constants(
        self,
        ctx,
        unit_name,
        data
    ):
        items = data.get(
            "constants",
            []
        )

        # PUI-v1-Dateien ohne Konstantenbereich bleiben gültig.
        if items is None:
            items = []

        if not isinstance(
            items,
            list
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"invalid constant section in "
                    f"PUI for unit {unit_name}"
                )
            )

        unit_prefix = self.normalize_unit_name(
            unit_name
        )

        for item in items:
            if not isinstance(
                item,
                dict
            ):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"invalid constant entry in "
                        f"PUI for unit {unit_name}"
                    )
                )

            name = str(
                item.get(
                    "name",
                    ""
                )
            ).strip()

            typ = str(
                item.get(
                    "type",
                    ""
                )
            ).strip().lower()

            if (
                not name
                or "value" not in item
                or typ not in (
                    "integer",
                    "boolean",
                    "double",
                    "string",
                    "char"
                )
            ):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"invalid constant metadata in "
                        f"PUI for unit {unit_name}"
                    )
                )

            stored_value = item[
                "value"
            ]

            try:
                if typ == "integer":
                    value = self.parse_pascal_integer_literal(
                        stored_value
                    )

                elif typ == "boolean":
                    value = int(
                        stored_value
                    )

                    if value not in (
                        0,
                        1
                    ):
                        raise ValueError(
                            "boolean constant must be 0 or 1"
                        )

                elif typ == "double":
                    # Prüfen, aber in derselben Form wie lokale Double-
                    # Konstanten an emit_load_double_literal() geben.
                    float(
                        stored_value
                    )

                    value = str(
                        stored_value
                    )

                elif typ == "char":
                    if (
                        not isinstance(
                            stored_value,
                            str
                        )
                        or len(stored_value) != 1
                    ):
                        raise ValueError(
                            "character constant must contain one character"
                        )

                    value = stored_value

                else:
                    if not isinstance(
                        stored_value,
                        str
                    ):
                        raise ValueError(
                            "string constant must contain text"
                        )

                    value = stored_value

            except (
                TypeError,
                ValueError
            ) as error:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"invalid value for PUI constant "
                        f"{unit_name}.{name}: {error}"
                    )
                )

            scoped_name = str(
                item.get(
                    "scoped_name",
                    unit_prefix + "_" + name
                )
            )

            info = {
                "name": name,
                "scoped_name": scoped_name,
                "type": typ,
                "value": value,
                "unit": unit_name,
                "pui": True
            }

            # Wie bei PUI-Routinen bleibt der erste unqualifizierte
            # Import sichtbar. Zusätzlich existiert der Unit-Schlüssel.
            self.constants[
                scoped_name.lower()
            ] = info

            self.constants.setdefault(
                name.lower(),
                info
            )

    def register_pui_types(
        self,
        ctx,
        unit_name,
        data
    ):
        types = data.get("types", {})

        if not isinstance(types, dict):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"invalid type section in "
                    f"PUI for unit {unit_name}"
                )
            )

        # ------------------------------------------------------------
        # Subranges zuerst registrieren.
        #
        # Aliases können anschließend auf diese Typen zeigen.
        # ------------------------------------------------------------
        for item in types.get(
            "subranges",
            []
        ):
            if not isinstance(item, dict):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"invalid subrange entry "
                        f"in PUI for {unit_name}"
                    )
                )

            name = str(
                item.get("name", "")
            ).strip()

            if not name:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"unnamed subrange type "
                        f"in PUI for {unit_name}"
                    )
                )

            try:
                min_value = int(
                    item["min_value"]
                )

                max_value = int(
                    item["max_value"]
                )

            except (
                KeyError,
                TypeError,
                ValueError
            ):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"invalid bounds for "
                        f"subrange type {name}"
                    )
                )

            self.declare_subrange_type(
                ctx,
                name,
                min_value,
                max_value
            )

            # Gespeicherte Größe gegen die für das aktuelle
            # Target berechnete Typbeschreibung prüfen.
            loaded_info = self.subrange_info(
                name
            )

            stored_size = item.get("size")

            if (
                stored_size is not None
                and int(stored_size)
                != int(loaded_info.size)
            ):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"PUI size mismatch for "
                        f"{unit_name}.{name}: "
                        f"stored {stored_size}, "
                        f"calculated "
                        f"{loaded_info.size}"
                    )
                )

            stored_signed = item.get("signed")

            if (
                stored_signed is not None
                and bool(stored_signed)
                != bool(loaded_info.signed)
            ):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"PUI signedness mismatch "
                        f"for {unit_name}.{name}"
                    )
                )

        # ------------------------------------------------------------
        # Typaliases danach registrieren.
        # ------------------------------------------------------------
        for item in types.get(
            "aliases",
            []
        ):
            if not isinstance(item, dict):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"invalid type alias entry "
                        f"in PUI for {unit_name}"
                    )
                )

            name = str(
                item.get("name", "")
            ).strip()

            target_type = str(
                item.get("target_type", "")
            ).strip()

            if not name or not target_type:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"invalid type alias "
                        f"in PUI for {unit_name}"
                    )
                )

            self.declare_type_alias(
                ctx,
                name,
                target_type
            )
    
        self.register_pui_record_types(
            ctx,
            unit_name,
            types
        )

    def register_pui_record_types(
        self,
        ctx,
        unit_name,
        types
    ):
        for item in types.get(
            "records",
            []
        ):
            if not isinstance(item, dict):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"invalid record entry "
                        f"in PUI for {unit_name}"
                    )
                )

            name = str(
                item.get("name", "")
            ).strip()

            if not name:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"unnamed record type "
                        f"in PUI for {unit_name}"
                    )
                )

            key = name.lower()

            if (
                key in self.records
                or key in self.arrays
                or key in self.classes
                or key in self.enums
                or key in self.subrange_types
            ):
                raise CompileError(
                    ctx,
                    "E0002",
                    name=name
                )

            record_fields = {}

            for field_item in item.get(
                "fields",
                []
            ):
                if not isinstance(field_item, dict):
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            f"invalid field in "
                            f"PUI record {unit_name}.{name}"
                        )
                    )

                field_name = str(
                    field_item.get("name", "")
                ).strip()

                field_type = str(
                    field_item.get("type", "")
                ).strip()

                if not field_name or not field_type:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            f"invalid field in "
                            f"PUI record {unit_name}.{name}"
                        )
                    )

                try:
                    field_offset = int(
                        field_item["offset"]
                    )
                    field_size = int(
                        field_item["size"]
                    )
                except (
                    KeyError,
                    TypeError,
                    ValueError
                ):
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            f"invalid field layout in "
                            f"PUI record {unit_name}.{name}"
                        )
                    )

                if field_offset < 0 or field_size <= 0:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            f"invalid field layout in "
                            f"PUI record {unit_name}.{name}"
                        )
                    )

                field_key = field_name.lower()

                if field_key in record_fields:
                    raise CompileError(
                        ctx,
                        "E0002",
                        name=field_name
                    )

                record_fields[field_key] = RecordFieldInfo(
                    name=field_name,
                    type=self.resolve_type(field_type),
                    offset=field_offset,
                    size=field_size
                )

            try:
                record_size = int(item["size"])
                alignment = int(
                    item.get("alignment", 1)
                )
            except (
                KeyError,
                TypeError,
                ValueError
            ):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"invalid layout for "
                        f"PUI record {unit_name}.{name}"
                    )
                )

            if record_size < 0 or alignment <= 0:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"invalid layout for "
                        f"PUI record {unit_name}.{name}"
                    )
                )

            for field_info in record_fields.values():
                if (
                    field_info.offset
                    + field_info.size
                    > record_size
                ):
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            f"field {field_info.name} exceeds "
                            f"PUI record {unit_name}.{name}"
                        )
                    )

            self.records[key] = RecordInfo(
                name=name,
                fields=record_fields,
                size=record_size,
                packed=bool(
                    item.get("packed", False)
                ),
                alignment=alignment
            )

    def visitTypeDeclaration(self, ctx):
        # ------------------------------------------------------------
        # Deklarationen mit eigener Unterregel
        # ------------------------------------------------------------
        if ctx.enumDeclaration():
            return self.visit(
                ctx.enumDeclaration()
            )

        if ctx.recordDeclaration():
            return self.visit(
                ctx.recordDeclaration()
            )

        if ctx.arrayDeclaration():
            return self.visit(
                ctx.arrayDeclaration()
            )

        if ctx.classDeclaration():
            return self.visit(
                ctx.classDeclaration()
            )

        # ------------------------------------------------------------
        # Ab hier:
        #
        #     Byte = 0..255;
        #     Boolean = 0..1;
        #     MyInteger = Integer;
        # ------------------------------------------------------------
        type_identifier = ctx.typeIdentifier()

        if type_identifier is None:
            raise CompileError(
                ctx,
                "E0019",
                text="type declaration has no type identifier"
            )

        name = type_identifier.getText()

        # ------------------------------------------------------------
        # Subrange-Typ
        # ------------------------------------------------------------
        if ctx.subrangeType():
            range_ctx = ctx.subrangeType()

            bounds = list(
                range_ctx.signedInteger()
            )

            if len(bounds) != 2:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "subrange type requires "
                        "two bounds"
                    )
                )

            min_value = self.parse_signed_integer(
                bounds[0]
            )

            max_value = self.parse_signed_integer(
                bounds[1]
            )

            self.declare_subrange_type(
                ctx,
                name,
                min_value,
                max_value
            )

            # Nur öffentliche Typen aus dem Interface
            # werden in die PUI übernommen.
            if self.collect_pui_interface:
                self.pui_add_subrange_type(
                    name
                )

            return None

        # ------------------------------------------------------------
        # Normaler Typalias
        #
        # Beispiel:
        #
        #     MyInteger = Integer;
        # ------------------------------------------------------------
        if ctx.typeName():
            target_type = ctx.typeName().getText()

            self.declare_type_alias(
                ctx,
                name,
                target_type
            )

            if self.collect_pui_interface:
                self.pui_add_type_alias(
                    name,
                    target_type
                )

            return None

        raise CompileError(
            ctx,
            "E0019",
            text=f"unsupported type declaration: {ctx.getText()}"
        )
    
    def visitFunctionDeclaration(self, ctx):
        name = ctx.IDENT().getText()

        convention = (
            self.local_routine_calling_convention(
                ctx
            )
        )
        
        if self.routine_is_external(ctx):
            params = self.collect_formal_params(
                ctx
            )

            return_type = self.resolve_type(
                ctx.typeName().getText()
            )

            directive = (
                ctx.externalRoutineDirective()
            )

            dll_name = (
                self.routine_external_library(
                    ctx
                )
            )

            if dll_name is None:
                return self.register_local_external_routine(
                    ctx=ctx,
                    kind="function",
                    name=name,
                    params=params,
                    return_type=return_type,
                    convention=convention
                )

            return self.register_external_routine(
                ctx=ctx,
                kind="function",
                name=name,
                params=params,
                return_type=return_type,
                spec_ctx=directive,
                convention=convention
            )

        return_type = self.resolve_type(
            ctx.typeName().getText()
        )

        params  = self.collect_formal_params(ctx)
        
        scoped  = self.unit_scoped_name(self.scoped_name(name))
        key     = scoped.lower()

        asmjit_label = self.new_named_label("func_" + scoped)
        fpc_name     = self.fpc_mangle_routine(
            name,
            params,
            self.current_unit if self.current_unit else None)

        self.add_asm_label_mapping(
            asmjit_label,
            fpc_name
        )
        
        self.functions[key] = {
            "name": name,
            "scoped_name": scoped,
            "return_type": return_type,
            "label": asmjit_label,      # für a.bind(...)
            "mangled": fpc_name,        # für NASM / Export / Mapping
            "params": params,
            "calling_convention": convention
        }

        # globaler Alias, damit "Add" gefunden wird
        self.functions[name.lower()] = self.functions[key]

        old_function = self.current_function
        self.emit_function_declaration(ctx, name, return_type)
        self.current_function = old_function
        
        if (CDATA.args_target in ["nt35", "winnt", "win32"]
            and hasattr(self.backend.writer, "add_symbol_alias")):
            
            target_index = self.backend.writer.find_symbol_index(
                asmjit_label
            )

            if target_index is None:
                raise RuntimeError(
                    "internal function symbol was not generated: "
                    f"{asmjit_label}"
                )

            if self.backend.writer.find_symbol_index(fpc_name) is None:
                self.backend.writer.add_symbol_alias(
                    fpc_name,
                    asmjit_label
                )
        return None
    
    def routine_is_external(
        self,
        ctx
    ):
        if not hasattr(
            ctx,
            "externalRoutineDirective"
        ):
            return False

        return (
            ctx.externalRoutineDirective()
            is not None
        )

    def routine_external_library(
        self,
        ctx
    ):
        """
        Liefert die externe Bibliothek einer Routine.

        Unterstützt beide Grammar-Varianten:

            externalRoutineDirective
                -> externalLibrary

        sowie die ältere Zwischenstruktur:

            externalRoutineDirective
                -> externalRoutineSpec
                    -> externalLibrary
        """
        if not hasattr(
            ctx,
            "externalRoutineDirective"
        ):
            return None

        directive = ctx.externalRoutineDirective()

        if directive is None:
            return None

        # Aktuelle Grammar:
        #
        #   externalRoutineDirective
        #       : EXTERNAL externalLibrary ... SEMI
        #
        spec_ctx = directive

        # Kompatibilität mit einer älteren Grammar, die noch einen
        # externalRoutineSpec-Unterknoten verwendete.
        spec_accessor = getattr(
            directive,
            "externalRoutineSpec",
            None
        )

        if spec_accessor is not None:
            old_spec_ctx = spec_accessor()

            if old_spec_ctx is not None:
                spec_ctx = old_spec_ctx

        library_accessor = getattr(
            spec_ctx,
            "externalLibrary",
            None
        )

        library_ctx = (
            library_accessor()
            if library_accessor is not None
            else None
        )

        if library_ctx is None:
            # Nur:
            #
            #   external;
            #
            # also ein externes COFF-Symbol ohne DLL-Angabe.
            return None

        # STRING oder Konstantenname wie DLL_FILE auflösen.
        return self.resolve_external_library(
            ctx,
            library_ctx
        )
    
    def routine_calling_convention(self, routine):
        convention = routine.get(
            "calling_convention",
            "cdecl"
        ).lower()

        if convention not in (
            "cdecl",
            "stdcall",
            "pascal"
        ):
            raise RuntimeError(
                f"unsupported calling convention: {convention}"
            )

        return convention

    def nt32_argument_order(self, routine, count):
        convention = self.routine_calling_convention(
            routine
        )

        if convention == "pascal":
            return range(0, count)

        # cdecl und stdcall
        return range(count - 1, -1, -1)

    def nt32_caller_cleans_stack(self, routine):
        return (
            self.routine_calling_convention(routine)
            == "cdecl"
        )
    
    def nt32_parameter_stack_bytes(self, params):
        result = 0

        for param in params:
            if param.get("is_var", False):
                result += 4
                continue

            if param.get("is_open_array", False):
                result += 8
                continue

            param_type = self.resolve_type(
                param["type"]
            )

            if param_type == "double":
                result += 8
            else:
                result += 4

        return result
    
    def emit_nt32_routine_arguments(
        self,
        ctx,
        routine,
        actuals,
        params,
        actuals_are_wrapped=False
    ):
        if len(actuals) != len(params):
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(actuals)),
                expected=str(len(params))
            )

        arg_bytes = 0

        for index in self.nt32_argument_order(
            routine,
            len(actuals)
        ):
            actual = actuals[index]
            formal = params[index]

            formal_type = self.resolve_type(
                formal["type"]
            )

            # ------------------------------------------------------
            # VAR-Parameter
            # ------------------------------------------------------
            if formal.get("is_var", False):
                if not actuals_are_wrapped:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "var parameters in function expressions "
                            "are not implemented yet"
                        )
                    )

                ref = self.actual_param_variable_ref(
                    ctx,
                    actual
                )

                var_name = ref.IDENT().getText()

                actual_type = self.addressable_name_type(
                    ctx,
                    var_name
                )

                if actual_type != formal_type:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=actual_type,
                        expected=formal_type
                    )

                self.emit_address_of_var(
                    ctx,
                    var_name
                )

                self.emit_push(
                    "eax",
                    comment=f"var parameter {index + 1}"
                )

                arg_bytes += 4
                continue

            # ------------------------------------------------------
            # Wert auswerten
            # ------------------------------------------------------
            if actuals_are_wrapped:
                actual_type = self.visit_actual_param_expr(
                    actual
                )
            else:
                actual_type = self.visit(actual)

            actual_type = self.resolve_type(
                actual_type
            )

            # ------------------------------------------------------
            # 32-Bit-Werte und Pointer
            # ------------------------------------------------------
            if formal_type in (
                "integer",
                "boolean",
                "char",
                "string"
            ):
                valid = actual_type == formal_type

                if (
                    formal_type == "boolean"
                    and actual_type == "integer"
                ):
                    valid = True

                if not valid:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=actual_type,
                        expected=formal_type
                    )

                self.emit_push(
                    "eax",
                    comment=f"parameter {index + 1}"
                )

                arg_bytes += 4
                continue

            # ------------------------------------------------------
            # Pointer
            # ------------------------------------------------------
            if self.is_pointer_type(
                formal_type,
                include_nil=False
            ):
                if not self.pointer_assignment_compatible(
                    actual_type,
                    formal_type
                ):
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=actual_type,
                        expected=formal_type
                    )

                self.emit_push(
                    "eax",
                    comment=f"pointer parameter {index + 1}"
                )

                arg_bytes += 4
                continue

            # ------------------------------------------------------
            # Klassen sind in NT32 Objektpointer
            # ------------------------------------------------------
            if formal_type in self.classes:
                if not self.class_assignment_compatible(
                    actual_type,
                    formal_type
                ):
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=actual_type,
                        expected=formal_type
                    )

                self.emit_push(
                    "eax",
                    comment=f"object parameter {index + 1}"
                )

                arg_bytes += 4
                continue

            # ------------------------------------------------------
            # Double: 8 Byte auf den Stack
            # ------------------------------------------------------
            if formal_type == "double":
                if actual_type != "double":
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=actual_type,
                        expected="double"
                    )

                self.emit_sub(
                    "esp",
                    8,
                    comment=f"double parameter {index + 1}"
                )

                self.backend.emit_movsd_store(
                    "esp",
                    0,
                    "xmm0"
                )

                arg_bytes += 8
                continue

            raise CompileError(
                ctx,
                "E0005",
                got=formal_type,
                expected=(
                    "integer/boolean/char/string/"
                    "double/pointer/class"
                )
            )

        return arg_bytes
    
    def finish_nt32_routine_call(
        self,
        routine,
        arg_bytes
    ):
        if (arg_bytes
            and self.nt32_caller_cleans_stack(routine)
        ):
            self.emit_add(
                "esp",
                arg_bytes,
                comment="cdecl caller cleanup"
            )
    
    def suffix_text(
        self,
        suffix
    ):
        if suffix is None:
            return ""

        return suffix.getText()

    def suffix_is_caret(
        self,
        suffix
    ):
        return (
            self.suffix_text(suffix)
            == "^"
        )

    def suffix_is_dot(
        self,
        suffix
    ):
        return (
            self.suffix_text(suffix)
            .startswith(".")
        )

    def suffix_index_exprs(
        self,
        suffix
    ):
        """
        Liefert die äußeren Indexausdrücke eines VariableSuffixContext.

        Abhängig von der ANTLR-Grammatik liegen die ExprContext-Knoten
        entweder direkt im Suffix oder unter einem Zwischenkontext wie
        indexList/indexExpressionList. Deshalb darf hier nicht nur
        suffix.expr() abgefragt werden.
        """
        if suffix is None:
            return []

        # Schneller Pfad für Grammatiken, in denen expr direkt Teil
        # von variableSuffix ist.
        expr_method = getattr(
            suffix,
            "expr",
            None
        )

        if callable(expr_method):
            exprs = expr_method()

            if exprs is not None:
                if isinstance(exprs, list):
                    result = list(exprs)
                else:
                    result = [exprs]

                if result:
                    return result

        # Robuster Fallback:
        #
        #   variableSuffix
        #       '['
        #       indexList
        #           expr
        #           ','
        #           expr
        #       ']'
        #
        # Sobald ein ExprContext gefunden wurde, wird nicht weiter in
        # diesen Ausdruck hinabgestiegen. Sonst würden Teilausdrücke
        # eines Indexes wie A[I + 1] mehrfach gesammelt.
        result = []

        def collect_outer_exprs(node):
            if node is None:
                return

            if isinstance(
                node,
                PascalParser.ExprContext
            ):
                result.append(
                    node
                )
                return

            for child in (
                getattr(
                    node,
                    "children",
                    None
                )
                or []
            ):
                collect_outer_exprs(
                    child
                )

        for child in (
            getattr(
                suffix,
                "children",
                None
            )
            or []
        ):
            collect_outer_exprs(
                child
            )

        return result

    def suffix_is_index(
        self,
        suffix
    ):
        text = self.suffix_text(
            suffix
        )

        return (
            text.startswith("[")
            or bool(
                self.suffix_index_exprs(
                    suffix
                )
            )
        )

    def suffix_field_name(
        self,
        suffix
    ):
        text = self.suffix_text(
            suffix
        )

        if not text.startswith("."):
            return None

        field_name = text[1:]

        if not field_name:
            return None

        return field_name
        
    def suffix_identifier_name(
        self,
        ctx,
        suffix
    ):
        """
        Ermittelt den Feldbezeichner eines VariableSuffixContext.

        Unterstützt alte und neu erzeugte ANTLR-Parser:

            .Field
            DOT IDENT
            DOT identifier

        Ein direkter IDENT()-Accessor ist nicht zwingend vorhanden.
        """
        if suffix is None:
            raise CompileError(
                ctx,
                "E0019",
                text="missing variable suffix"
            )

        # Grammar-unabhängig: der komplette Suffixtext lautet
        # normalerweise ".Field".
        field_name = self.suffix_field_name(
            suffix
        )

        if field_name:
            return field_name

        # Ältere Grammar:
        #
        #     variableSuffix : DOT IDENT;
        ident_accessor = getattr(
            suffix,
            "IDENT",
            None
        )

        if callable(
            ident_accessor
        ):
            ident = ident_accessor()

            if isinstance(
                ident,
                list
            ):
                for item in ident:
                    if item is None:
                        continue

                    value = item.getText()

                    if value:
                        return value

            elif ident is not None:
                value = ident.getText()

                if value:
                    return value

        # Neuere Grammar:
        #
        #     variableSuffix : DOT identifier;
        identifier_accessor = getattr(
            suffix,
            "identifier",
            None
        )

        if callable(
            identifier_accessor
        ):
            identifier_ctx = identifier_accessor()

            if isinstance(
                identifier_ctx,
                list
            ):
                for item in identifier_ctx:
                    if item is None:
                        continue

                    value = item.getText()

                    if value:
                        return value

            elif identifier_ctx is not None:
                value = identifier_ctx.getText()

                if value:
                    return value

        # Letzter Parse-Tree-Fallback.
        ignored_tokens = {
            ".",
            "^",
            "[",
            "]",
            ",",
            "(",
            ")"
        }

        for index in range(
            suffix.getChildCount() - 1,
            -1,
            -1
        ):
            child = suffix.getChild(
                index
            )

            if child is None:
                continue

            value = child.getText()

            if (
                value
                and value not in ignored_tokens
            ):
                return value.lstrip(".")

        suffix_text = self.suffix_text(
            suffix
        )

        if (
            suffix_text.startswith(".")
            and len(suffix_text) > 1
        ):
            return suffix_text[1:]

        raise CompileError(
            ctx,
            "E0019",
            text=(
                "could not determine field name from suffix "
                + repr(suffix_text)
            )
        )


    def suffix_is_field(
        self,
        suffix
    ):
        return (
            self.suffix_text(suffix)
            .startswith(".")
        )
    
    def visitAssignment(self, ctx):
        target_ctx = ctx.variableRef()

        if target_ctx is None:
            raise CompileError(
                ctx,
                "E0019",
                text="assignment has no target"
            )

        target = target_ctx.getText()

        # IDENT() kann bei reservierten beziehungsweise speziell
        # tokenisierten Namen wie Result None liefern. Der vorhandene
        # Helfer verwendet zusätzlich identifier(), Starttoken und
        # den ersten Kindknoten.
        base_target_name = self.variable_ref_name(
            ctx,
            target_ctx
        )

        expr_type = self.visit(
            ctx.expr()
        )

        # --------------------------------------------------------------
        # Ausdruckstyp für Subrange-Zieltypen normalisieren.
        #
        # Beispiel:
        #     Boolean = 0..1;
        #     b := False;
        #
        # False liefert "boolean", die Subrange-Variable wird intern
        # derzeit jedoch über den Basistyp "integer" gespeichert.
        # --------------------------------------------------------------
        def normalize_subrange_assignment(
            info,
            current_expr_type
        ):
            declared_type = self.resolve_type(
                info.get(
                    "declared_type",
                    info["type"]
                )
            )

            resolved_expr_type = self.resolve_type(
                current_expr_type
            )

            range_info = self.subrange_info(
                declared_type
            )

            # Das Ziel ist kein Subrange-Typ.
            if range_info is None:
                return resolved_expr_type

            target_base_type = self.scalar_base_type(
                declared_type
            )

            expr_base_type = self.scalar_base_type(
                resolved_expr_type
            )

            # Boolean-Subrange 0..1.
            if (
                resolved_expr_type == "boolean"
                and range_info.min_value == 0
                and range_info.max_value == 1
            ):
                self.emit_and(
                    "eax",
                    1,
                    comment="normalize boolean subrange"
                )

                return "integer"

            # Byte, Word, DWord, Cardinal und Integer besitzen für
            # Zuweisungen denselben skalaren ABI-Basistyp.
            #
            # Beispiel:
            #
            #     CRC: Word;
            #     CRC := crc16_calc(...);   // Word := Word
            #
            # Der Ausdruck kann weiterhin den deklarierten Typ "word"
            # tragen. Für den Speicherpfad wird er auf "integer"
            # normalisiert.
            if (
                target_base_type == "integer"
                and expr_base_type == "integer"
            ):
                return "integer"

            # Ein einzelnes Zeichen darf in einen Byte-kompatiblen
            # Integer-Subrange übernommen werden.
            if (
                target_base_type == "integer"
                and resolved_expr_type == "char"
                and range_info.min_value <= 0
                and range_info.max_value >= 255
            ):
                self.emit_and(
                    "eax",
                    0xFF,
                    comment=(
                        f"normalize char for "
                        f"{declared_type}"
                    )
                )

                return "integer"

            raise CompileError(
                ctx,
                "E0005",
                got=resolved_expr_type,
                expected=declared_type
            )

        # --------------------------------------------------------------
        # Funktionsrückgabewert
        # --------------------------------------------------------------
        if target.lower() == "result":
            self.emit_store_result(ctx, expr_type)
            return None

        # --------------------------------------------------------------
        # Implizites Self-Feld innerhalb einer Methode
        # --------------------------------------------------------------
        if (
            "." not in target
            and "[" not in target
            and "^" not in target
        ):
            if self.emit_store_self_field(ctx, target, expr_type):
                return None

        # --------------------------------------------------------------
        # VAR-Parameter
        # --------------------------------------------------------------
        param = self.find_param(target)

        if param and param.get("is_var", False):
            self.emit_store_param(ctx, target, expr_type)
            return None

        # --------------------------------------------------------------
        # Variable mit Suffix: P^, P^.X, A[0], A[0].X, S[1], Obj.X
        # --------------------------------------------------------------
        suffixes = list(target_ctx.variableSuffix())

        if suffixes:
            first = suffixes[0]
            
            suffixes = list(
                target_ctx.variableSuffix()
            )

            has_caret = any(
                self.suffix_is_caret(suffix)
                for suffix in suffixes
            )

            has_dot = any(
                self.suffix_is_dot(suffix)
                for suffix in suffixes
            )

            # Pointer auf Recordfeld:
            #
            #     Ctx^.crc := $FFFF;
            #
            if has_caret and has_dot:
                parts = [
                    base_target_name
                ]

                after_caret = False

                for suffix in suffixes:
                    if self.suffix_is_caret(
                        suffix
                    ):
                        after_caret = True
                        continue

                    if (
                        after_caret
                        and self.suffix_is_dot(
                            suffix
                        )
                    ):
                        field_name = (
                            self.suffix_field_name(
                                suffix
                            )
                        )

                        if field_name:
                            parts.append(
                                field_name
                            )

                if len(parts) < 2:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "pointer record assignment "
                            "has no field name"
                        )
                    )

                self.emit_store_pointer_record_field(
                    ctx,
                    parts,
                    expr_type
                )

                return None

            # Einfacher Pointer-Dereferenzzugriff: P^ := ...
            if self.suffix_is_caret(first):
                var_name = base_target_name

                self.emit_store_pointer_deref(
                    ctx,
                    var_name,
                    expr_type
                )
                return None

            # Array- oder Stringindex
            if self.suffix_is_index(first):
                var_name = base_target_name

                index_exprs, rest_suffixes = self.collect_array_suffix_exprs(
                    suffixes
                )

                # Typisierter Pointer:
                #
                #   Result[0] := 'a';
                #   PAnsiCharVar[I] := #0;
                #
                # Result ist eine lokale Variable und darf deshalb nicht
                # über var_info() gesucht werden.
                pointer_info = self.find_local_var(
                    var_name
                )

                if pointer_info is None:
                    pointer_info = self.find_param(
                        var_name
                    )

                if pointer_info is None:
                    pointer_info = self.vars.get(
                        var_name.lower()
                    )

                if pointer_info is not None:
                    pointer_type = self.resolve_type(
                        pointer_info["type"]
                    )

                    if self.is_pointer_type(
                        pointer_type,
                        include_nil=False
                    ):
                        if rest_suffixes:
                            raise CompileError(
                                ctx,
                                "E0019",
                                text=(
                                    "field access after an indexed "
                                    "pointer is not implemented yet"
                                )
                            )

                        self.emit_store_pointer_element(
                            ctx,
                            var_name,
                            index_exprs,
                            expr_type
                        )

                        return None

                var_info = self.var_info(
                    ctx,
                    var_name
                )

                var_type = self.resolve_type(
                    var_info["type"]
                )

                # Stringzeichen: S[1] := 'A'
                if var_type == "string":
                    self.emit_store_string_char(
                        ctx,
                        var_name,
                        index_exprs,
                        expr_type
                    )
                    return None

                if (
                    not isinstance(var_type, str)
                    or var_type not in self.arrays
                ):
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=var_type,
                        expected="array/string"
                    )

                var_info, array_info = self.get_array_info(ctx, var_name)

                # Array von Records: Points[0].X := ...
                if rest_suffixes and self.suffix_is_dot(rest_suffixes[0]):
                    field_parts = []

                    for suffix in rest_suffixes:
                        if not self.suffix_is_dot(suffix):
                            continue

                        field_name = self.suffix_identifier_name(
                            ctx,
                            suffix
                        )

                        if field_name:
                            field_parts.append(
                                field_name
                            )

                    if not field_parts:
                        raise CompileError(
                            ctx,
                            "E0019",
                            text="record field missing after array index"
                        )

                    if getattr(array_info, "is_dynamic", False):
                        self.emit_store_dynamic_array_record_field(
                            ctx,
                            var_name,
                            index_exprs,
                            field_parts,
                            expr_type
                        )
                        return None

                    self.emit_store_array_record_field(
                        ctx,
                        var_name,
                        index_exprs,
                        field_parts,
                        expr_type
                    )
                    return None

                # emit_store_array_element unterscheidet intern bereits
                # zwischen statischen und dynamischen Arrays.
                self.emit_store_array_element(
                    ctx,
                    var_name,
                    index_exprs,
                    expr_type
                )
                return None

            # Klassen- oder Recordfeld
            if self.suffix_is_dot(first):
                parts = [base_target_name]

                for suffix in suffixes:
                    if not self.suffix_is_dot(suffix):
                        continue

                    field_name = self.suffix_identifier_name(
                        ctx,
                        suffix
                    )

                    if field_name:
                        parts.append(
                            field_name
                        )

                if len(parts) < 2:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text="field name missing after '.'"
                    )

                var_name = parts[0]

                # Impliziter beziehungsweise expliziter Self-Pfad:
                #
                #   FAppForm.WndClass.style := CS_REDRAW;
                #   Self.FAppForm.WndClass.style := CS_REDRAW;
                #
                # FAppForm ist keine lokale/globale Variable. Der Pfad muss
                # deshalb vor var_info() über die aktuelle Klasse aufgelöst
                # werden.
                if var_name.lower() == "self":
                    if self.emit_store_self_member_path(
                        ctx,
                        parts[1:],
                        expr_type
                    ):
                        return None

                elif self.find_current_class_field(
                    var_name
                ) is not None:
                    self.emit_store_self_member_path(
                        ctx,
                        parts,
                        expr_type
                    )
                    return None

                (
                    source_kind,
                    var_info,
                    var_type
                ) = self.resolve_named_storage(
                    ctx,
                    var_name
                )

                if (
                    isinstance(var_type, str)
                    and var_type in self.records
                ):
                    self.emit_store_record_field(
                        ctx,
                        parts,
                        expr_type
                    )
                    return None

                if (isinstance(var_type, str) and var_type in self.classes ):
                    if self.emit_store_class_property(ctx, parts, expr_type):
                        return None

                    self.emit_store_class_field(ctx, parts, expr_type)
                    return None

                raise CompileError(
                    ctx,
                    "E0005",
                    got=var_type,
                    expected="class/record"
                )

        # --------------------------------------------------------------
        # Konstanten dürfen nicht beschrieben werden
        # --------------------------------------------------------------
        if self.find_const(target):
            raise CompileError(ctx, "E0010", name=target)

        # --------------------------------------------------------------
        # Lokale Variable
        # --------------------------------------------------------------
        local_var = self.find_local_var(target)

        if local_var:
            expr_type = normalize_subrange_assignment(
                local_var,
                expr_type
            )

            declared_type = local_var.get(
                "declared_type",
                local_var["type"]
            )

            if self.subrange_info(declared_type) is not None:
                self.emit_subrange_check(
                    ctx,
                    declared_type,
                    "eax"
                )

            self.emit_store_local_var(
                ctx,
                target,
                expr_type
            )
            return None

        # --------------------------------------------------------------
        # Globale Variable
        # --------------------------------------------------------------
        var_info = self.var_info(ctx, target)
        var_type = self.resolve_type(var_info["type"])

        expr_type = normalize_subrange_assignment(
            var_info,
            expr_type
        )

        # Pointer, including Pointer/PChar/PAnsiChar aliases.
        if self.is_pointer_type(
            var_type,
            include_nil=False
        ):
            if not self.pointer_assignment_compatible(
                expr_type,
                var_type
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=expr_type,
                    expected=var_type
                )

            self.emit_store_var(ctx, target, var_info)
            return None

        # Klassenvariable
        if (
            isinstance(var_type, str)
            and var_type in self.classes
        ):
            if not self.class_assignment_compatible(
                expr_type,
                var_type
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=expr_type,
                    expected=var_type
                )

            self.emit_store_object_var(ctx, target, var_info)
            return None

        # Implizite Integer-nach-Double-Konvertierung
        if var_type == "double" and expr_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")
            expr_type = "double"

        if var_type != expr_type:
            raise CompileError(
                ctx,
                "E0005",
                got=expr_type,
                expected=var_type
            )

        # emit_store_var führt bei globalen Subrange-Variablen bereits
        # emit_subrange_check aus.
        self.emit_store_var(ctx, target, var_info)
        return None
    def visitExpr(self, ctx):
        return self.visit(ctx.boolOrExpr())
    
    def visitAddExpr(self, ctx):
        result_type = self.visit(ctx.shiftExpr(0))
        
        for i in range(1, len(ctx.shiftExpr())):
            op = ctx.getChild(2 * i - 1).getText()

            # string + string
            if result_type == "string":
                if op != "+":
                    raise CompileError(ctx, "E0005", got="string -", expected="string + string")

                if CDATA.args_target in ["nt35", "winnt", "win32"]:
                    self.emit_push("eax", comment="save left DynString")

                    right_type = self.visit(ctx.shiftExpr(i))
                    if right_type != "string":
                        raise CompileError(ctx, "E0005", got=right_type, expected="string")

                    # eax = right DynString
                    self.emit_pop("ebx", comment="left DynString")

                    # cdecl: push right, dann left
                    self.emit_push("eax", comment="right DynString")
                    self.emit_push("ebx", comment="left DynString")

                    self.emit_call("_jit_dynstring_concat")
                    self.backend.emit_cleanup_stack(8)

                    # eax = neuer DynStringHeader*
                    self.writer.emit_lea_reg_data_label("esi", "ctx")

                else:
                    self.emit_push("rax", comment="save left DynString")

                    right_type = self.visit(ctx.shiftExpr(i))
                    if right_type != "string":
                        raise CompileError(ctx, "E0005", got=right_type, expected="string")

                    # Win64: rcx = left, rdx = right
                    self.emit_mov("rdx", "rax", comment="right DynString")
                    self.emit_pop("rcx", comment="left DynString")

                    self.emit_mov_imm("rax", "&_jit_dynstring_concat")
                    self.emit_call_rax()

                    # rax = neuer DynStringHeader*

                result_type = "string"
                continue

            # integer links
            if result_type == "integer":
                self.emit_push("rax", comment="save left integer")

                right_type = self.visit(ctx.shiftExpr(i))

                if right_type == "integer":
                    self.emit_mov("ebx", "eax")
                    self.emit_pop("rax")

                    if op == "+":
                        self.emit_add("eax", "ebx")
                    elif op == "-":
                        self.emit_sub("eax", "ebx")

                    result_type = "integer"
                    continue

                if right_type == "double":
                    self.emit_pop("eax")
                    self.emit_cvtsi2sd("xmm1", "eax")

                    if op == "+":
                        self.emit_addsd("xmm1", "xmm0")
                    elif op == "-":
                        self.emit_subsd("xmm1", "xmm0")

                    self.emit_movapd("xmm0", "xmm1")
                    result_type = "double"
                    continue

                raise CompileError(ctx, "E0005", got=right_type, expected="integer/double")

            # double links
            if result_type == "double":
                self.emit_sub("rsp", 8)
                self.emit_movsd_store("rsp", 0, "xmm0")

                right_type = self.visit(ctx.shiftExpr(i))

                if right_type == "integer":
                    self.emit_cvtsi2sd("xmm0", "eax")
                elif right_type != "double":
                    raise CompileError(ctx, "E0005", got=right_type, expected="integer/double")

                self.emit_movsd_load("xmm1", "rsp", 0)
                self.emit_add("rsp", 8)

                if op == "+":
                    self.emit_addsd("xmm1", "xmm0")
                elif op == "-":
                    self.emit_subsd("xmm1", "xmm0")

                self.emit_movapd("xmm0", "xmm1")
                result_type = "double"
                continue

            raise CompileError(ctx, "E0005", got=result_type, expected="integer/double/string")

        return result_type
    
    def visitTerm(self, ctx):
        result_type = self.visit(ctx.factor(0))

        for i in range(1, len(ctx.factor())):
            op = ctx.getChild(2 * i - 1).getText()

            if result_type == "integer":
                self.emit_push("rax")

                right_type = self.visit(ctx.factor(i))

                if right_type == "integer":
                    self.emit_mov("ebx", "eax")
                    self.emit_pop("rax")

                    if op == "*":
                        self.emit_imul("eax", "ebx")
                        result_type = "integer"

                    elif op == "/":
                        self.emit_cdq()
                        self.emit_idiv("ebx")
                        result_type = "integer"

                    continue

                self.emit_pop("rax")
                self.emit_cvtsi2sd("xmm1", "eax")
                result_type = "double"

            else:
                self.emit_sub("rsp", 8)
                self.emit_movsd_store("rsp", 0, "xmm0")

                right_type = self.visit(ctx.factor(i))

                self.emit_movsd_load("xmm1", "rsp", 0)
                self.emit_add("rsp", 8)

            if result_type == "double":
                if right_type == "integer":
                    self.emit_cvtsi2sd("xmm0", "eax")

                if op == "*":
                    self.emit_mulsd("xmm0", "xmm1")

                elif op == "/":
                    self.emit_movapd("xmm2", "xmm0")
                    self.emit_movapd("xmm0", "xmm1")
                    self.emit_divsd("xmm0", "xmm2")

                result_type = "double"

        return result_type
    def emit_address_of_array_element(self, ctx, var_name, index_expr_ctx):
        index_exprs = index_expr_ctx

        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]

        var_info, array_info = self.get_array_info(ctx, var_name)

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)
        self.emit_imul("eax", "eax", array_info.element_size)

        is_nt32 = CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        )

        if getattr(array_info, "is_dynamic", False):
            if is_nt32:
                self.emit_mov(
                    "edx",
                    "eax",
                    comment="dynamic array byte offset"
                )
                self.emit_load_var(
                    var_name,
                    var_info
                )
                self.emit_add(
                    "eax",
                    "edx",
                    comment=f"@{var_name}[...]"
                )
            else:
                self.emit_mov(
                    "r10d",
                    "eax",
                    comment="dynamic array byte offset"
                )
                self.emit_load_var(
                    var_name,
                    var_info
                )
                self.emit_movsxd(
                    "r11",
                    "r10d"
                )
                self.emit_add(
                    "rax",
                    "r11",
                    comment=f"@{var_name}[...]"
                )

            return "^" + array_info.element_type

        if is_nt32:
            self.emit_mov(
                "edx",
                "eax",
                comment="static array byte offset"
            )

            symbol = var_info.get("symbol")

            if not symbol:
                symbol = f"_var_{var_info['name']}"
                var_info["symbol"] = symbol

            self.writer.emit_lea_reg_data_label(
                "eax",
                symbol
            )
            self.emit_add(
                "eax",
                "edx",
                comment=f"@{var_name}[...]"
            )
        else:
            self.emit_add(
                "eax",
                var_info["slot"]
            )
            self.emit_mov_qword(
                "r11",
                "r12",
                "arrays_vars"
            )
            self.emit_movsxd(
                "rax",
                "eax"
            )
            self.emit_add(
                "rax",
                "r11",
                comment=f"@{var_name}[...]"
            )

        return "^" + array_info.element_type
    
    def variable_ref_name(self, ctx, ref):
        if ref is None:
            raise CompileError(
                ctx,
                "E0019",
                text="missing variable reference"
            )

        # Normaler IDENT-Token. Nach einer Grammar-Änderung besitzt
        # VariableRefContext nicht zwingend einen IDENT()-Accessor.
        ident_accessor = getattr(
            ref,
            "IDENT",
            None
        )

        if callable(
            ident_accessor
        ):
            ident = ident_accessor()

            if ident is not None:
                if isinstance(
                    ident,
                    list
                ):
                    for item in ident:
                        if item is None:
                            continue

                        value = item.getText()

                        if value:
                            return value
                else:
                    value = ident.getText()

                    if value:
                        return value

        # Falls die Grammar eine allgemeine identifier-Regel besitzt
        if hasattr(ref, "identifier"):
            identifier_ctx = ref.identifier()

            if identifier_ctx is not None:
                return identifier_ctx.getText()

        # Sicherer Fallback: erster Token der variableRef
        start_token = getattr(
            ref,
            "start",
            None
        )

        if (
            start_token is not None
            and start_token.text
        ):
            return start_token.text

        # Letzter Fallback
        if ref.getChildCount() > 0:
            return ref.getChild(0).getText()

        raise CompileError(
            ctx,
            "E0019",
            text=(
                "could not determine variable name from "
                + ref.getText()
            )
        )
    
    def emit_load_open_array_element(
        self,
        ctx,
        name,
        param,
        index_exprs
    ):
        if not isinstance(
            index_exprs,
            list
        ):
            index_exprs = [
                index_exprs
            ]

        if len(index_exprs) != 1:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(index_exprs)),
                expected="1"
            )

        element_type = self.resolve_type(
            param.get(
                "element_type"
            )
        )

        data_offset = param.get(
            "stack_offset"
        )

        high_offset = param.get(
            "high_offset"
        )

        if data_offset is None:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"open array parameter {name} "
                    f"has no data offset"
                )
            )

        if high_offset is None:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"open array parameter {name} "
                    f"has no High offset"
                )
            )

        index_type = self.visit(
            index_exprs[0]
        )

        if index_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=index_type,
                expected="integer"
            )

        # --------------------------------------------------------
        # NT32
        #
        # [ebp + data_offset] = Datenpointer
        # [ebp + high_offset] = High-Wert
        # --------------------------------------------------------
        if CDATA.args_target in [
            "nt35",
            "winnt",
            "win32"
        ]:
            fail_label = self.new_named_label(
                "open_array_bounds_fail"
            )

            ok_label = self.new_named_label(
                "open_array_bounds_ok"
            )

            # ECX = Index
            self.emit_mov(
                "ecx",
                "eax",
                comment=f"{name} index"
            )

            # Index >= 0
            self.emit_cmp(
                "ecx",
                0
            )

            self.emit_jl(
                fail_label
            )

            # EDX = High(Values)
            self.emit_mov_dword_ptr(
                "edx",
                "ebp",
                high_offset,
                comment=f"High({name})"
            )

            # Index <= High
            self.emit_cmp(
                "ecx",
                "edx"
            )

            self.emit_jg(
                fail_label
            )

            self.emit_jmp(
                ok_label
            )

            self.emit_bind_label(
                fail_label
            )

            self.emit_soft_runtime_error(
                f"Array bounds error: {name}"
            )

            self.emit_bind_label(
                ok_label
            )

            # EDX = Datenpointer
            self.emit_mov_dword_ptr(
                "edx",
                "ebp",
                data_offset,
                comment=f"{name} data"
            )

            # ----------------------------------------------------
            # Variant open array (``array of const``).
            #
            # Each element is a JitVariantArg descriptor.  Return
            # its address in EAX; consumers such as WriteLn inspect
            # the runtime kind stored at offset zero.
            # ----------------------------------------------------
            if (
                param.get(
                    "is_variant_open_array",
                    False
                )
                or element_type == "const"
            ):
                self.emit_imul(
                    "ecx",
                    "ecx",
                    JIT_VARIANT_ARG_SIZE
                )

                self.emit_add(
                    "edx",
                    "ecx",
                    comment=f"{name}[index] variant address"
                )

                self.emit_mov(
                    "eax",
                    "edx",
                    comment=f"{name}[index] variant"
                )

                return "variant"

            if element_type in (
                "integer",
                "boolean"
            ):
                element_size = 4

            elif element_type == "double":
                element_size = 8

            elif element_type == "string":
                element_size = 4

            elif (
                isinstance(element_type, str)
                and element_type.startswith("^")
            ):
                element_size = 4

            else:
                raise CompileError(
                    ctx,
                    "E0014",
                    var_type=element_type
                )

            if element_size != 1:
                self.emit_imul(
                    "ecx",
                    "ecx",
                    element_size
                )

            self.emit_add(
                "edx",
                "ecx",
                comment=f"{name}[index] address"
            )

            if element_type == "integer":
                self.emit_mov_dword_ptr(
                    "eax",
                    "edx",
                    0,
                    comment=f"{name}[index]"
                )

                return "integer"

            if element_type == "boolean":
                self.emit_mov_dword_ptr(
                    "eax",
                    "edx",
                    0,
                    comment=f"{name}[index]"
                )

                self.emit_and(
                    "eax",
                    1
                )

                return "boolean"

            if element_type == "double":
                self.emit_movsd_load(
                    "xmm0",
                    "edx",
                    0,
                    comment=f"{name}[index]"
                )

                return "double"

            if element_type == "string":
                self.emit_mov_dword_ptr(
                    "eax",
                    "edx",
                    0,
                    comment=f"{name}[index]"
                )

                return "string"

            if (
                isinstance(element_type, str)
                and element_type.startswith("^")
            ):
                self.emit_mov_dword_ptr(
                    "eax",
                    "edx",
                    0,
                    comment=f"{name}[index]"
                )

                return element_type

        raise CompileError(
            ctx,
            "E0019",
            text=(
                "open array element access is currently "
                "implemented only for NT32"
            )
        )

    def find_array_constructor_context(self, ctx):
        """Return the first nested ArrayConstructorContext, if present."""
        if ctx is None:
            return None

        if isinstance(
            ctx,
            PascalParser.ArrayConstructorContext
        ):
            return ctx

        for child in (
            getattr(ctx, "children", None)
            or []
        ):
            result = self.find_array_constructor_context(
                child
            )

            if result is not None:
                return result

        return None

    def variant_kind_for_type(self, ctx, value_type):
        value_type = self.resolve_type(
            value_type
        )

        if value_type == "integer":
            return JIT_VARIANT_INTEGER

        if value_type == "boolean":
            return JIT_VARIANT_BOOLEAN

        if value_type == "char":
            return JIT_VARIANT_CHAR

        if value_type == "string":
            return JIT_VARIANT_STRING

        if value_type == "double":
            return JIT_VARIANT_DOUBLE

        if value_type == "^nil":
            return JIT_VARIANT_POINTER

        if (
            isinstance(value_type, str)
            and value_type.startswith("^")
        ):
            return JIT_VARIANT_POINTER

        if (
            isinstance(value_type, str)
            and value_type in self.classes
        ):
            return JIT_VARIANT_POINTER

        raise CompileError(
            ctx,
            "E0005",
            got=value_type,
            expected=(
                "integer/boolean/char/string/"
                "double/pointer"
            )
        )

    def emit_store_variant_descriptor_nt32(
        self,
        ctx,
        data_label,
        index,
        value_type
    ):
        """Store the value currently in EAX/XMM0 as JitVariantArg."""
        value_type = self.resolve_type(
            value_type
        )

        kind = self.variant_kind_for_type(
            ctx,
            value_type
        )

        descriptor_offset = (
            index * JIT_VARIANT_ARG_SIZE
        )

        # Loading EDX does not destroy the expression result in EAX/XMM0.
        self.writer.emit_lea_reg_data_label(
            "edx",
            data_label
        )

        self.emit_mov(
            "ecx",
            kind,
            comment=f"variant element {index} kind"
        )

        self.emit_mov_dword_ptr_store(
            "edx",
            descriptor_offset + JIT_VARIANT_KIND_OFFSET,
            "ecx"
        )

        if value_type == "double":
            self.emit_movsd_store(
                "edx",
                descriptor_offset + JIT_VARIANT_LOW_OFFSET,
                "xmm0",
                comment=f"variant double element {index}"
            )
            return

        self.emit_mov_dword_ptr_store(
            "edx",
            descriptor_offset + JIT_VARIANT_LOW_OFFSET,
            "eax",
            comment=f"variant element {index} value"
        )

        self.emit_xor(
            "ecx",
            "ecx"
        )

        self.emit_mov_dword_ptr_store(
            "edx",
            descriptor_offset + JIT_VARIANT_HIGH_OFFSET,
            "ecx"
        )

    def emit_variant_open_array_actual_nt32(
        self,
        ctx,
        argument_ctx
    ):
        """Build an NT32 ``array of const`` actual parameter."""
        if CDATA.args_target not in (
            "nt35",
            "winnt",
            "win32"
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "array of const is currently "
                    "implemented only for NT32"
                )
            )

        constructor_ctx = (
            self.find_array_constructor_context(
                argument_ctx
            )
        )

        if constructor_ctx is not None:
            elements = (
                self.collect_array_constructor_elements(
                    constructor_ctx
                )
            )
        else:
            # Project extension: a scalar actual can be wrapped as a
            # one-element variant open array.
            elements = [argument_ctx]

        count = len(elements)
        literal_id = self.next_variant_array_id
        self.next_variant_array_id += 1

        data_label = (
            f"__variant_open_array_{literal_id}"
        )

        allocation_size = max(
            1,
            count
        ) * JIT_VARIANT_ARG_SIZE

        if self.coff.find_symbol_index(
            data_label
        ) is None:
            self.coff.add_data_zeros(
                data_label,
                allocation_size,
                alignment=4
            )

        for index, element_ctx in enumerate(elements):
            value_type = self.visit(
                element_ctx
            )

            if value_type is None:
                raise CompileError(
                    element_ctx,
                    "E0019",
                    text=(
                        "array-of-const element "
                        "produced no type"
                    )
                )

            value_type = self.resolve_type(
                value_type
            )

            self.emit_store_variant_descriptor_nt32(
                element_ctx,
                data_label,
                index,
                value_type
            )

        self.writer.emit_lea_reg_data_label(
            "eax",
            data_label
        )

        result = {
            "element_type": "const",
            "high": count - 1,
            "count": count,
            "element_size": JIT_VARIANT_ARG_SIZE,
            "data_label": data_label,
            "stack_bytes": 0
        }

        self.pending_open_array_actual = result
        return result

    def visitArrayConstructor(self, ctx):
        elements = self.collect_array_constructor_elements(
            ctx
        )

        if CDATA.debug_mode:
            print(
                "ARRAY CONSTRUCTOR:",
                ctx.getText()
            )

            print(
                "ARRAY ELEMENTS:",
                [
                    element.getText()
                    for element in elements
                ]
            )

        if not elements:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "array constructor contains no "
                    "recognizable expression elements: "
                    + ctx.getText()
                )
            )

        if CDATA.args_target not in [
            "nt35",
            "winnt",
            "win32"
        ]:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "array constructors are currently "
                    "implemented only for NT32"
                )
            )

        literal_id = self.next_open_array_literal_id
        self.next_open_array_literal_id += 1

        data_label = (
            f"__open_array_literal_{literal_id}"
        )

        # ------------------------------------------------------------
        # Erstes Element auswerten und Elementtyp bestimmen
        # ------------------------------------------------------------
        element_type = self.visit(
            elements[0]
        )

        element_type = self.resolve_type(
            element_type
        )

        if element_type in (
            "integer",
            "boolean"
        ):
            element_size = 4

        elif element_type == "double":
            element_size = 8

        elif element_type == "string":
            element_size = 4

        elif (
            isinstance(element_type, str)
            and element_type.startswith("^")
        ):
            element_size = 4

        else:
            raise CompileError(
                elements[0],
                "E0005",
                got=element_type,
                expected=(
                    "integer/boolean/double/string/pointer"
                )
            )

        total_size = (
            len(elements)
            * element_size
        )

        # ------------------------------------------------------------
        # Speicherplatz für das Arrayliteral im COFF-Datenbereich
        # ------------------------------------------------------------
        if self.coff.find_symbol_index(
            data_label
        ) is None:
            self.coff.add_data_zeros(
                data_label,
                total_size,
                alignment=(
                    8
                    if element_size == 8
                    else 4
                )
            )

        # ------------------------------------------------------------
        # Aktuell ausgewertetes Element speichern
        # ------------------------------------------------------------
        def store_element(index):
            byte_offset = (
                index
                * element_size
            )

            # EDX = Basisadresse des Arrayliterals
            self.writer.emit_lea_reg_data_label(
                "edx",
                data_label
            )

            if element_type in (
                "integer",
                "boolean"
            ):
                if element_type == "boolean":
                    self.emit_and(
                        "eax",
                        1,
                        comment="normalize boolean array element"
                    )

                self.emit_mov_dword_ptr_store(
                    "edx",
                    byte_offset,
                    "eax",
                    comment=(
                        f"array literal element {index}"
                    )
                )

                return

            if element_type == "double":
                self.emit_movsd_store(
                    "edx",
                    byte_offset,
                    "xmm0",
                    comment=(
                        f"array literal element {index}"
                    )
                )

                return

            if element_type == "string":
                self.emit_mov_dword_ptr_store(
                    "edx",
                    byte_offset,
                    "eax",
                    comment=(
                        f"array literal element {index}"
                    )
                )

                return

            if (
                isinstance(element_type, str)
                and element_type.startswith("^")
            ):
                self.emit_mov_dword_ptr_store(
                    "edx",
                    byte_offset,
                    "eax",
                    comment=(
                        f"array literal element {index}"
                    )
                )

                return

            raise CompileError(
                ctx,
                "E0014",
                var_type=element_type
            )

        # Erstes Element wurde bereits ausgewertet.
        store_element(
            0
        )

        # ------------------------------------------------------------
        # Restliche Elemente auswerten
        # ------------------------------------------------------------
        for index in range(
            1,
            len(elements)
        ):
            current_type = self.visit(
                elements[index]
            )

            current_type = self.resolve_type(
                current_type
            )

            # Integer und Boolean nicht stillschweigend mischen.
            if current_type != element_type:
                raise CompileError(
                    elements[index],
                    "E0005",
                    got=current_type,
                    expected=element_type
                )

            store_element(
                index
            )

        # ------------------------------------------------------------
        # Ergebnisadresse laden
        # ------------------------------------------------------------
        self.writer.emit_lea_reg_data_label(
            "eax",
            data_label
        )

        # Metadaten müssen erst nach der Auswertung aller Elemente
        # gesetzt werden, damit verschachtelte Visitor-Aufrufe sie
        # nicht überschreiben.
        self.pending_open_array_actual = {
            "element_type": element_type,
            "high": len(elements) - 1,
            "count": len(elements),
            "element_size": element_size,
            "data_label": data_label,
            "stack_bytes": 0
        }

        return (
            f"open_array:{element_type}"
        )
    
    def visitInheritedExpression(self, ctx):
        result_type = self.visitInheritedStatement(
            ctx
        )

        if result_type is None:
            raise CompileError(
                ctx,
                "E0019",
                text=(tr("inherited expression requires "
                    "a parent function")
                )
            )

        return result_type
    
    def visitFactor(self, ctx):
        text = ctx.getText()

        # ------------------------------------------------------------
        # Identifier einer variableRef sicher ermitteln.
        #
        # Bei reservierten Wörtern wie VALUES kann ref.IDENT() None
        # liefern, obwohl der Name als erster Token vorhanden ist.
        # ------------------------------------------------------------
        def variable_ref_name(ref):
            if ref is None:
                raise CompileError(
                    ctx,
                    "E0019",
                    text="missing variable reference"
                )

            if hasattr(ref, "IDENT"):
                ident = ref.IDENT()

                if isinstance(ident, list):
                    if ident:
                        return ident[0].getText()

                elif ident is not None:
                    return ident.getText()

            if hasattr(ref, "identifier"):
                ident_ctx = ref.identifier()

                if ident_ctx is not None:
                    return ident_ctx.getText()

            start_token = getattr(
                ref,
                "start",
                None
            )

            if (
                start_token is not None
                and getattr(start_token, "text", None)
            ):
                return start_token.text

            if ref.getChildCount() > 0:
                return ref.getChild(0).getText()

            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "could not determine variable name from "
                    + ref.getText()
                )
            )

        # ------------------------------------------------------------
        # Identifier hinter einem Punkt ermitteln:
        #
        #   Object.Field
        #   Pointer^.Field
        #
        # Auch hier kann IDENT() bei reservierten Tokens None liefern.
        # ------------------------------------------------------------
        def suffix_identifier(suffix):
            if suffix is None:
                raise CompileError(
                    ctx,
                    "E0019",
                    text="missing variable suffix"
                )

            # VariableSuffixContext kann den kompletten Text ".crc"
            # als einen einzigen Parse-Tree-Knoten liefern. In diesem
            # Fall darf der fuehrende Punkt nicht Teil des Feldnamens
            # werden, sonst entsteht der Pfad "Ctx..crc".
            field_name = self.suffix_field_name(suffix)

            if field_name:
                return field_name

            return self.suffix_identifier_name(
                ctx,
                suffix
            )

        # ------------------------------------------------------------
        # Einfachen Identifier laden.
        #
        # Diese zentrale Funktion ersetzt die bisher mehrfach
        # vorhandene Identifier-Auflösung.
        # ------------------------------------------------------------
        def load_plain_identifier(name):
            # Lokale Variable hat höchste Priorität.
            local_var = self.find_local_var(
                name
            )

            if local_var is not None:
                return self.emit_load_local_var(
                    ctx,
                    name,
                    local_var
                )

            # Danach formaler Parameter.
            param = self.find_param(
                name
            )

            if param is not None:
                # Ein offenes Array ohne Index wird als Datenpointer
                # geladen. Das ist unter anderem für eine spätere
                # Weitergabe an andere Routinen nützlich.
                if param.get(
                    "is_open_array",
                    False
                ):
                    offset = param.get(
                        "stack_offset"
                    )

                    if offset is None:
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                f"open array parameter {name} "
                                f"has no stack offset"
                            )
                        )

                    if CDATA.args_target in [
                        "nt35",
                        "winnt",
                        "win32"
                    ]:
                        self.emit_mov_dword_ptr(
                            "eax",
                            "ebp",
                            offset,
                            comment=f"{name} data"
                        )

                        return param["type"]

                    if CDATA.args_target in [
                        "dos",
                        "dos16"
                    ]:
                        self.backend.writer.emit_mov_reg16_mem16_base_disp(
                            "ax",
                            "bp",
                            offset
                        )

                        return param["type"]

                    self.emit_mov_qword_ptr(
                        "rax",
                        "rbp",
                        offset,
                        comment=f"{name} data"
                    )

                    return param["type"]

                return self.emit_load_param(
                    ctx,
                    name
                )

            # Klassenfeld von Self.
            self_field_type = self.emit_load_self_field(
                ctx,
                name
            )

            if self_field_type is not None:
                return self_field_type

            # Lokale oder globale Konstante.
            const_info = self.find_const(
                name
            )

            if const_info is not None:
                if const_info.get("kind") == "array":
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            f"constant array {name} "
                            "requires an index"
                        )
                    )

                return self.emit_load_const(
                    ctx,
                    name
                )

            # Globale Variable.
            key = name.lower()

            if key in self.vars:
                info = self.var_info(
                    ctx,
                    name
                )

                self.emit_load_var(
                    name,
                    info
                )

                return self.resolve_type(
                    info["type"]
                )

            # Parameterlose Methode der aktuellen Klasse.
            if self.current_class is not None:
                try:
                    return self.emit_self_method_call(
                        ctx,
                        name,
                        []
                    )

                except CompileError:
                    pass

            # Eingebaute parameterlose Funktionen ohne Klammern.
            builtin_key = name.lower()

            if builtin_key == "paramcount":
                return self.emit_builtin_paramcount(
                    ctx
                )

            if builtin_key == "commandline":
                return self.emit_builtin_commandline(
                    ctx
                )
            
            if builtin_key == "ownerclassname":
                return self.emit_builtin_owner_class_name(
                    ctx
                )

            # Parameterlose benutzerdefinierte Funktion ohne Klammern.
            func = self.find_function(
                name
            )

            if func is not None:
                params = func.get(
                    "params",
                    []
                )

                if len(params) == 0:
                    if CDATA.args_target in [
                        "nt35",
                        "winnt",
                        "win32"
                    ]:
                        self.emit_registered_routine_call(
                            func
                        )

                    else:
                        self.emit_sub(
                            "rsp",
                            32,
                            comment=(
                                "shadow space for "
                                "parameterless function call"
                            )
                        )

                        self.emit_registered_routine_call(
                            func
                        )

                        self.emit_add(
                            "rsp",
                            32
                        )

                    return self.resolve_type(
                        func["return_type"]
                    )

            raise CompileError(
                ctx,
                "E0001",
                name=name
            )

        # ============================================================
        # Vorzeichen
        # ============================================================
        if ctx.MINUS():
            expr_type = self.visit(
                ctx.factor()
            )

            if expr_type == "integer":
                self.emit_mov(
                    "ebx",
                    "eax"
                )

                self.emit_xor(
                    "eax",
                    "eax"
                )

                self.emit_sub(
                    "eax",
                    "ebx"
                )

                return "integer"

            if expr_type == "double":
                if CDATA.args_target in [
                    "nt35",
                    "winnt",
                    "win32"
                ]:
                    self.emit_sub(
                        "esp",
                        8
                    )

                    self.emit_movsd_store(
                        "esp",
                        0,
                        "xmm0"
                    )

                    self.emit_xor(
                        "eax",
                        "eax"
                    )

                    self.emit_cvtsi2sd(
                        "xmm0",
                        "eax"
                    )

                    self.emit_movsd_load(
                        "xmm1",
                        "esp",
                        0
                    )

                    self.emit_add(
                        "esp",
                        8
                    )

                else:
                    self.emit_sub(
                        "rsp",
                        8
                    )

                    self.emit_movsd_store(
                        "rsp",
                        0,
                        "xmm0"
                    )

                    self.emit_xor(
                        "eax",
                        "eax"
                    )

                    self.emit_cvtsi2sd(
                        "xmm0",
                        "eax"
                    )

                    self.emit_movsd_load(
                        "xmm1",
                        "rsp",
                        0
                    )

                    self.emit_add(
                        "rsp",
                        8
                    )

                self.emit_subsd(
                    "xmm0",
                    "xmm1"
                )

                return "double"

            raise CompileError(
                ctx,
                "E0005",
                got=expr_type,
                expected="integer/double"
            )

        if ctx.PLUS():
            return self.visit(
                ctx.factor()
            )

        # ============================================================
        # Boolean-Literale und NOT
        # ============================================================
        if ctx.TRUE():
            self.emit_mov_imm(
                "eax",
                1
            )

            return "boolean"

        if ctx.FALSE():
            self.emit_mov_imm(
                "eax",
                0
            )

            return "boolean"

        if ctx.NOT():
            expr_type = self.visit(
                ctx.factor()
            )

            if expr_type not in ("boolean", "integer"):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=expr_type,
                    expected="boolean/integer")
            
            #if expr_type != "boolean":
            #    raise CompileError(
            #        ctx,
            #        "E0005",
            #        got=expr_type,
            #        expected="boolean"
            #    )

            true_label = self.new_named_label(
                "not_true"
            )

            end_label = self.new_named_label(
                "not_end"
            )

            self.emit_cmp(
                "eax",
                0
            )

            self.emit_je(
                true_label
            )

            self.emit_mov(
                "eax",
                0
            )

            self.emit_jmp(
                end_label
            )

            self.emit_bind_label(
                true_label
            )

            self.emit_mov(
                "eax",
                1
            )

            self.emit_bind_label(
                end_label
            )

            return "boolean"

        # ============================================================
        # Adressoperator @
        # ============================================================
        if ctx.AT():
            ref = ctx.variableRef()

            if ref is None:
                raise CompileError(
                    ctx,
                    "E0019",
                    text="address operator requires a variable"
                )

            name = variable_ref_name(
                ref
            )

            suffixes = list(
                ref.variableSuffix()
            )

            if (name.lower() == "self"
                and any(
                    self.suffix_is_dot(suffix)
                    for suffix in suffixes
                )
            ):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "an instance method cannot be used as a raw "
                        "callback; declare a global stdcall callback"
                    )
                )

            if suffixes:
                first = suffixes[0]

                if self.suffix_is_index(first):
                    index_exprs, rest_suffixes = (
                        self.collect_array_suffix_exprs(
                            suffixes
                        )
                    )

                    if rest_suffixes:
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                "address of array record field "
                                "is not implemented yet"
                            )
                        )

                    param = self.find_param(
                        name
                    )

                    if (
                        param is not None
                        and param.get(
                            "is_open_array",
                            False
                        )
                    ):
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                "address of an open-array element "
                                "is not implemented yet"
                            )
                        )

                    return self.emit_address_of_array_element(
                        ctx,
                        name,
                        index_exprs
                    )

            # Variables keep precedence over routines when both namespaces
            # contain the same spelling.
            if (self.find_local_var(name) is None
                and name.lower() not in self.vars
            ):
                routine_type = self.emit_address_of_routine(
                    ctx,
                    name
                )

                if routine_type is not None:
                    return routine_type

            return self.emit_address_of_var(
                ctx,
                name
            )

        # ============================================================
        # Geerbter Funktionsaufruf:
        #
        #   Result := inherited GetWindowStyle;
        # ============================================================
        if (hasattr(ctx, "inheritedExpression") and ctx.inheritedExpression() is not None):
            return self.visit(
                ctx.inheritedExpression()
            )

        # ============================================================
        # Expliziter Funktionsaufruf
        # ============================================================
        if ctx.functionCallExpr():
            return self.visit(
                ctx.functionCallExpr()
            )

        # ============================================================
        # Arraykonstruktor
        #
        # Beispiel:
        #
        #   [1, 2, 3]
        #
        # Die eigentliche Implementierung gehört in
        # visitArrayConstructor().
        # ============================================================
        if (hasattr(ctx, "arrayConstructor")
            and ctx.arrayConstructor() is not None
        ):
            return self.visit(
                ctx.arrayConstructor()
            )

        # ============================================================
        # VariableRef:
        #
        #   Value
        #   Values[I]
        #   P^
        #   P^.Field
        #   Object.Field
        #   TFoo.Create
        # ============================================================
        if ctx.variableRef():
            ref = ctx.variableRef()

            name = variable_ref_name(
                ref
            )

            suffixes = list(
                ref.variableSuffix()
            )

            # --------------------------------------------------------
            # Einfacher Name ohne Suffix
            # --------------------------------------------------------
            if not suffixes:
                return load_plain_identifier(
                    name
                )

            first = suffixes[0]

            has_caret = any(
                self.context_contains_caret(suffix)
                for suffix in suffixes
            )

            has_dot = any(
                self.context_contains_dot(suffix)
                for suffix in suffixes
            )
            
            # --------------------------------------------------------
            # Pointer auf Record:
            #
            #   P^.Field
            # --------------------------------------------------------
            if has_caret and has_dot:
                parts = [
                    name
                ]

                after_caret = False

                for suffix in suffixes:
                    if self.context_contains_caret(suffix):
                        after_caret = True
                        continue

                    if (
                        after_caret
                        and self.context_contains_dot(suffix)
                    ):
                        parts.append(
                            suffix_identifier(
                                suffix
                            )
                        )

                return self.emit_load_pointer_record_field(
                    ctx,
                    parts
                )

            # --------------------------------------------------------
            # Einfaches Dereferenzieren:
            #
            #   P^
            # --------------------------------------------------------
            if self.suffix_is_caret(first):
                return self.emit_load_pointer_deref(
                    ctx,
                    name
                )

            # --------------------------------------------------------
            # Array- oder Stringzugriff:
            #
            #   Values[I]
            #   A[I]
            #   S[I]
            #   Points[I].X
            # --------------------------------------------------------
            if self.suffix_is_index(first):
                index_exprs, rest_suffixes = (
                    self.collect_array_suffix_exprs(
                        suffixes
                    )
                )

                if not index_exprs:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            f"array index missing for {name}"
                        )
                    )

                # ----------------------------------------------------
                # Offenes Array als Parameter:
                #
                #   Values[I]
                # ----------------------------------------------------
                param = self.find_param(
                    name
                )

                if (
                    param is not None
                    and param.get(
                        "is_open_array",
                        False
                    )
                ):
                    if rest_suffixes:
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                "record fields on open-array "
                                "elements are not implemented yet"
                            )
                        )

                    return self.emit_load_open_array_element(
                        ctx,
                        name,
                        param,
                        index_exprs
                    )

                # Typisiertes konstantes Array:
                #
                #   const
                #       HexDigits: array[0..15] of AnsiChar = (...);
                #
                # Solche Arrays liegen nicht in self.vars, sondern im
                # lokalen beziehungsweise globalen Konstanten-Scope.
                const_info = self.find_const(
                    name
                )

                if (
                    const_info is not None
                    and const_info.get("kind") == "array"
                ):
                    if rest_suffixes:
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                "record fields on constant-array "
                                "elements are not implemented yet"
                            )
                        )

                    return self.emit_load_const_array_element(
                        ctx,
                        name,
                        const_info,
                        index_exprs
                    )

                # Typisierter Pointer:
                #
                #   PAnsiCharVar[I]
                #   Result[I]
                #
                # Lokale Pointer und Parameter liegen nicht in self.vars.
                pointer_info = self.find_local_var(
                    name
                )

                if pointer_info is None:
                    pointer_info = self.find_param(
                        name
                    )

                if pointer_info is None:
                    pointer_info = self.vars.get(
                        name.lower()
                    )

                if pointer_info is not None:
                    pointer_type = self.resolve_type(
                        pointer_info["type"]
                    )

                    if self.is_pointer_type(
                        pointer_type,
                        include_nil=False
                    ):
                        if rest_suffixes:
                            raise CompileError(
                                ctx,
                                "E0019",
                                text=(
                                    "field access after an indexed "
                                    "pointer is not implemented yet"
                                )
                            )

                        return self.emit_load_pointer_element(
                            ctx,
                            name,
                            index_exprs
                        )

                # Veränderliche Arrays und Strings.
                var_info = self.var_info(
                    ctx,
                    name
                )

                var_type = self.resolve_type(
                    var_info["type"]
                )

                # ----------------------------------------------------
                # Stringzugriff:
                #
                #   S[0] = kompletter String
                #   S[I] = einzelnes Zeichen
                # ----------------------------------------------------
                if var_type == "string":
                    if (
                        len(index_exprs) == 1
                        and index_exprs[0].getText() == "0"
                    ):
                        self.emit_load_var(
                            name,
                            var_info
                        )

                        return "string"

                    return self.emit_load_string_char(
                        ctx,
                        name,
                        index_exprs
                    )

                # ----------------------------------------------------
                # Array aus Records:
                #
                #   Points[I].X
                # ----------------------------------------------------
                if (
                    rest_suffixes
                    and self.suffix_is_dot(rest_suffixes[0])
                ):
                    field_parts = []

                    for suffix in rest_suffixes:
                        if self.suffix_is_dot(suffix):
                            field_parts.append(
                                suffix_identifier(
                                    suffix
                                )
                            )

                    var_info, array_info = self.get_array_info(
                        ctx,
                        name
                    )

                    if getattr(
                        array_info,
                        "is_dynamic",
                        False
                    ):
                        return self.emit_load_dynamic_array_record_field(
                            ctx,
                            name,
                            index_exprs,
                            field_parts
                        )

                    return self.emit_load_array_record_field(
                        ctx,
                        name,
                        index_exprs,
                        field_parts
                    )

                # ----------------------------------------------------
                # Normaler Arrayzugriff
                # ----------------------------------------------------
                return self.emit_load_array_element(
                    ctx,
                    name,
                    index_exprs
                )

            # --------------------------------------------------------
            # Punktzugriff:
            #
            #   TFoo.Create
            #   Object.Field
            #   Object.Property
            #   Record.Field
            # --------------------------------------------------------
            if self.suffix_is_dot(first):
                parts = [
                    name
                ]

                for suffix in suffixes:
                    if self.suffix_is_dot(suffix):
                        parts.append(
                            suffix_identifier(
                                suffix
                            )
                        )

                # TFoo.Create
                if len(parts) == 2:
                    class_name = parts[0]
                    method_name = parts[1]

                    if (
                        class_name.lower() in self.classes
                        and method_name.lower() == "create"
                    ):
                        return self.emit_class_constructor_call(
                            ctx,
                            class_name,
                            method_name
                        )

                var_name = parts[0]

                # ------------------------------------------------------------
                # Expliziter Self-Zugriff:
                #
                #   Self.InstanceSize
                #   Self.ClassName
                #   Self.FValue
                #
                # Self ist keine lokale oder globale Variable. Der Objektzeiger
                # wurde im Methodenprolog unter [ebp-4] gespeichert.
                # ------------------------------------------------------------
                if var_name.lower() == "self":
                    if (
                        self.current_class is None
                        or self.current_method is None
                    ):
                        raise CompileError(
                            ctx,
                            "E0019",
                            text="Self may only be used inside a class method"
                        )

                    # Zuerst einen einfachen oder verschachtelten
                    # Klassen-/Recordfeldpfad prüfen:
                    #
                    #   Self.FValue
                    #   Self.FAppForm.WndClass.style
                    field_type = self.emit_load_self_member_path(
                        ctx,
                        parts[1:]
                    )

                    if field_type is not None:
                        return field_type

                    if len(parts) != 2:
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                "unsupported nested Self member access: "
                                + ".".join(parts)
                            )
                        )

                    # Danach parameterlose Funktionsmethode:
                    #
                    #   Self.InstanceSize
                    #   Self.ClassName
                    member_name = parts[1]

                    return self.emit_self_method_call(
                        ctx,
                        member_name,
                        []
                    )

                # Impliziter Self-Pfad:
                #
                #   FAppForm.WndClass.style
                #
                # Dieser Test muss vor var_info() erfolgen, weil FAppForm
                # ein Feld der aktuellen Klasse und keine Variable ist.
                if self.find_current_class_field(
                    var_name
                ) is not None:
                    return self.emit_load_self_member_path(
                        ctx,
                        parts
                    )

                (
                    source_kind,
                    var_info,
                    var_type
                ) = self.resolve_named_storage(
                    ctx,
                    var_name
                )

                if (
                    isinstance(var_type, str)
                    and var_type in self.records
                ):
                    return self.emit_load_record_field(
                        ctx,
                        parts
                    )

                if (
                    isinstance(var_type, str)
                    and var_type in self.classes
                ):
                    if source_kind != "global":
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                "class field loading is not yet "
                                f"implemented for {source_kind} variables"
                            )
                        )

                    property_type = self.emit_load_class_property(
                        ctx,
                        parts
                    )

                    if property_type is not None:
                        return property_type

                    # Parameterlose Funktionsmethode ohne Klammern:
                    #
                    #     Foo.InstanceSize
                    #
                    if len(parts) == 2:
                        cls = self.classes[
                            var_type
                        ]

                        method_key = (
                            parts[1].lower()
                        )

                        if method_key in cls.methods:
                            return self.emit_object_method_call(
                                ctx,
                                var_name,
                                parts[1],
                                actuals=[],
                                require_function=True
                            )

                    return self.emit_load_class_field(
                        ctx,
                        parts
                    )

                raise CompileError(
                    ctx,
                    "E0005",
                    got=var_type,
                    expected="class/record"
                )

            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "unsupported variable suffix: "
                    + ref.getText()
                )
            )

        # ============================================================
        # Geklammerter Ausdruck
        # ============================================================

        expr_list = ctx.expr()

        if expr_list:
            if isinstance(
                expr_list,
                list
            ):
                if expr_list:
                    return self.visit(
                        expr_list[0]
                    )

            else:
                return self.visit(
                    expr_list
                )

        # ============================================================
        # NIL
        # ============================================================
        if ctx.NIL():
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_xor(
                    "eax",
                    "eax",
                    comment="nil"
                )

            elif CDATA.args_target in [
                "dos",
                "dos16"
            ]:
                self.emit_xor(
                    "eax",
                    "eax",
                    comment="nil offset"
                )

                self.emit_xor(
                    "edx",
                    "edx",
                    comment="nil segment"
                )

            else:
                self.emit_xor(
                    "rax",
                    "rax",
                    comment="nil"
                )

            return "^nil"

        # ============================================================
        # Pascal-Zeichencode: #0, #13, #$0A
        # ============================================================
        if ctx.CHARCODE():
            token_text = (
                ctx.CHARCODE().getText()
            )

            value_text = token_text[1:]

            if value_text.startswith("$"):
                value = int(
                    value_text[1:],
                    16
                )
            else:
                value = int(
                    value_text,
                    10
                )

            if value < 0 or value > 255:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=str(value),
                    expected="character code 0..255"
                )

            self.emit_mov_imm(
                "eax",
                str(value)
            )

            return "char"

        # ============================================================
        # Pascal-Hexliteral
        # ============================================================
        if ctx.HEXNUMBER():
            token_text = (
                ctx.HEXNUMBER().getText()
            )

            value = int(
                token_text[1:],
                16
            )

            self.emit_mov_imm(
                "eax",
                str(value)
            )

            return "integer"
            
        # ============================================================
        # Integerliteral
        # ============================================================
        if ctx.NUMBER():
            value = ctx.NUMBER().getText()

            self.emit_mov_imm(
                "eax",
                value
            )

            return "integer"

        # ============================================================
        # Doubleliteral
        # ============================================================

        if ctx.FLOATNUMBER():
            value = ctx.FLOATNUMBER().getText()

            return self.emit_load_double_literal(
                value
            )

        # ============================================================
        # String- oder Zeichenliteral
        # ============================================================

        if ctx.STRING():
            try:
                value = self.pascal_token_string(
                    ctx.STRING()
                )
            except ValueError:
                value = ctx.STRING().getText()[1:-1]

            # Ein Pascal-Char ist ein skalarer 8-Bit-Wert.
            #
            # Vorher wurde bei 'A' die Adresse eines String-Literals
            # zurückgegeben, während #65 bereits den Wert 65 lieferte.
            # Diese zwei Darstellungen führten bei Pointer- und
            # Array-Zuweisungen zu falschen Bytes.
            if len(value) == 1:
                char_value = ord(
                    value
                )

                if char_value < 0 or char_value > 0xFF:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=str(char_value),
                        expected="AnsiChar 0..255"
                    )

                if CDATA.args_target in (
                    "dos",
                    "dos16"
                ):
                    self.backend.writer.emit_mov_reg16_imm16(
                        "ax",
                        char_value
                    )
                else:
                    self.emit_mov_imm(
                        "eax",
                        str(char_value)
                    )

                return "char"

            label = self.add_string_literal(
                value
            )

            # Mehrere Zeichen werden in einen dynamischen String
            # umgewandelt.
            if CDATA.args_target in [
                "nt35",
                "winnt",
                "win32"
            ]:
                self.backend.writer.emit_push_data_label32(
                    label
                )

                self.emit_call(
                    "_jit_dynstring_from_cstr"
                )

                self.backend.emit_cleanup_stack(
                    4
                )

                if self.coff.find_symbol_index(
                    "ctx"
                ) is not None:
                    self.writer.emit_lea_reg_data_label(
                        "esi",
                        "ctx"
                    )

            elif CDATA.args_target in [
                "dos",
                "dos16"
            ]:
                self.backend.writer.emit_mov_dx_label(
                    label
                )

            else:
                self.emit_mov_imm(
                    "rcx",
                    label
                )

                self.emit_mov_imm(
                    "rax",
                    "&_jit_dynstring_from_cstr"
                )

                self.emit_call_rax()

            return "string"

        # ============================================================
        # Direkter IDENT-Faktor
        #
        # Einige Grammar-Alternativen erzeugen keinen variableRef-
        # Kontext, sondern liefern den Identifier direkt.
        # ============================================================

        if ctx.IDENT():
            ident = ctx.IDENT()

            if isinstance(ident, list):
                if not ident:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text="empty identifier"
                    )

                name = ident[0].getText()

            else:
                name = ident.getText()

            return load_plain_identifier(
                name
            )

        raise CompileError(
            ctx,
            "E0015",
            text=text
        )
    
    def HEXNUMBER(self):
        return self.getToken(
            PascalParser.HEXNUMBER,
            0
        )
    
    def get_single_builtin_arg(self, ctx):
        actuals = []

        if ctx.argumentList():
            actuals = list(ctx.argumentList().expr())

        #if ctx.actualParamList():
        #    actuals = [p.expr() for p in ctx.actualParamList().actualParam()]

        if len(actuals) != 1:
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected="1")

        return actuals[0]
        
    def emit_builtin_low(self, ctx):
        arg_ctx = self.get_single_builtin_arg(ctx)

        name = arg_ctx.getText()

        # --------------------------------------------------------
        # Offenes Array als Funktionsparameter
        #
        # function Sum(
        #     const Values: array of Integer
        # ): Integer;
        #
        # Offene Arrays beginnen immer bei Index 0.
        # --------------------------------------------------------
        param = self.find_param(
            name
        )

        if (
            param is not None
            and param.get(
                "is_open_array",
                False
            )
        ):
            self.emit_mov(
                "eax",
                0,
                comment=f"Low({name})"
            )

            return "integer"

        # --------------------------------------------------------
        # Lokale Arrayvariable
        # --------------------------------------------------------
        local_var = self.find_local_var(
            name
        )

        if local_var is not None:
            var_type = self.resolve_type(
                local_var["type"]
            )

            if (
                isinstance(var_type, str)
                and var_type in self.arrays
            ):
                array_info = self.arrays[
                    var_type
                ]

                if getattr(
                    array_info,
                    "is_dynamic",
                    False
                ):
                    self.emit_mov(
                        "eax",
                        0,
                        comment=f"Low({name})"
                    )

                    return "integer"

                self.emit_mov(
                    "eax",
                    array_info.index_min,
                    comment=f"Low({name})"
                )

                return "integer"

        # --------------------------------------------------------
        # Globale Arrayvariable
        # --------------------------------------------------------
        key = name.lower()

        if key in self.vars:
            var_info = self.vars[key]

            var_type = self.resolve_type(
                var_info["type"]
            )

            if (
                isinstance(var_type, str)
                and var_type in self.arrays
            ):
                array_info = self.arrays[
                    var_type
                ]

                if getattr(
                    array_info,
                    "is_dynamic",
                    False
                ):
                    self.emit_mov(
                        "eax",
                        0,
                        comment=f"Low({name})"
                    )

                    return "integer"

                self.emit_mov(
                    "eax",
                    array_info.index_min,
                    comment=f"Low({name})"
                )

                return "integer"

        raise CompileError(
            ctx,
            "E0005",
            got=name,
            expected="array"
        )

    def emit_builtin_high(self, ctx):
        arg_ctx = self.get_single_builtin_arg(
            ctx
        )

        name = arg_ctx.getText()

        # --------------------------------------------------------
        # Offenes Array als Funktionsparameter
        # --------------------------------------------------------
        param = self.find_param(
            name
        )

        if (
            param is not None
            and param.get(
                "is_open_array",
                False
            )
        ):
            high_offset = param.get(
                "high_offset"
            )

            if high_offset is None:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        f"open array parameter {name} "
                        f"has no High offset"
                    )
                )

            if CDATA.args_target in [
                "nt35",
                "winnt",
                "win32"
            ]:
                self.emit_mov_dword_ptr(
                    "eax",
                    "ebp",
                    high_offset,
                    comment=f"High({name})"
                )

                return "integer"

            if CDATA.args_target in [
                "dos",
                "dos16"
            ]:
                self.backend.writer.emit_mov_reg16_mem16_base_disp(
                    "ax",
                    "bp",
                    high_offset
                )

                return "integer"

            self.emit_mov_dword_ptr(
                "eax",
                "rbp",
                high_offset,
                comment=f"High({name})"
            )

            return "integer"

        # --------------------------------------------------------
        # Lokale Arrayvariable
        # --------------------------------------------------------
        local_var = self.find_local_var(
            name
        )

        if local_var is not None:
            var_type = self.resolve_type(
                local_var["type"]
            )

            if (
                isinstance(var_type, str)
                and var_type in self.arrays
            ):
                array_info = self.arrays[
                    var_type
                ]

                if getattr(
                    array_info,
                    "is_dynamic",
                    False
                ):
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "High() for local dynamic arrays "
                            "is not implemented yet"
                        )
                    )

                self.emit_mov(
                    "eax",
                    array_info.index_max,
                    comment=f"High({name})"
                )

                return "integer"

        # --------------------------------------------------------
        # Globale Arrayvariable
        # --------------------------------------------------------
        key = name.lower()

        if key in self.vars:
            var_info = self.vars[key]

            var_type = self.resolve_type(
                var_info["type"]
            )

            if (
                isinstance(var_type, str)
                and var_type in self.arrays
            ):
                array_info = self.arrays[
                    var_type
                ]

                if getattr(
                    array_info,
                    "is_dynamic",
                    False
                ):
                    self.emit_builtin_length(
                        ctx
                    )

                    self.emit_sub(
                        "eax",
                        1,
                        comment=f"High({name})"
                    )

                    return "integer"

                self.emit_mov(
                    "eax",
                    array_info.index_max,
                    comment=f"High({name})"
                )

                return "integer"

        raise CompileError(
            ctx,
            "E0005",
            got=name,
            expected="array"
        )

    def collect_array_constructor_elements(self, ctx):
        result = []

        def walk(node):
            if node is None:
                return

            children = getattr(
                node,
                "children",
                None
            )

            if not children:
                return

            for child in children:
                # Sobald ein ExprContext gefunden wurde, ist dies ein
                # vollständiges Element des Arraykonstruktors.
                #
                # Nicht weiter in diesen Ausdruck hinabsteigen, sonst
                # würden bei "1 + 2" zusätzlich die Unterausdrücke
                # eingesammelt.
                if isinstance(
                    child,
                    PascalParser.ExprContext
                ):
                    result.append(
                        child
                    )

                    continue

                walk(
                    child
                )

        walk(
            ctx
        )

        return result
    
    def is_known_type_name(
        self,
        name
    ):
        if not isinstance(name, str):
            return False

        key = name.strip().lower()

        if not key:
            return False

        if key in (
            "integer",
            "boolean",
            "char",
            "double",
            "string",
            "pointer",
            "pchar",
            "pansichar"
        ):
            return True

        if key in self.type_aliases:    return True
        if key in self.subrange_types:  return True
        if key in self.enums:           return True
        if key in self.records:         return True
        if key in self.arrays:          return True
        if key in self.classes:         return True

        return False
    
    def emit_explicit_type_cast(self, ctx, target_name):
        actuals = self.function_call_args(ctx)

        if len(actuals) != 1:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(actuals)),
                expected="1"
            )

        argument = actuals[0]

        if hasattr(argument, "expr"):
            nested_expr = argument.expr()
            if nested_expr is not None:
                argument = nested_expr

        target_type = self.resolve_type(target_name)
        source_type = self.resolve_type(self.visit(argument))

        target_is_pointer = self.is_pointer_type(
            target_type,
            include_nil=False
        )
        source_is_pointer = self.is_pointer_type(
            source_type,
            include_nil=True
        )
        source_is_class = (
            isinstance(source_type, str)
            and source_type in self.classes
        )
        target_is_class = (
            isinstance(target_type, str)
            and target_type in self.classes
        )
        source_is_nil = source_type in ("nil", "^nil")

        source_is_integer = (
            self.scalar_base_type(source_type) == "integer"
        )

        integer_address_cast_allowed = (
            source_is_integer
            and CDATA.args_target in (
                "nt35",
                "winnt",
                "win32"
            )
        )

        if target_is_pointer:
            # PAnsiChar(StringValue) beziehungsweise PChar(StringValue):
            #
            # Das dBase2Many-String-ABI liefert bereits den Zeiger auf die
            # nullterminierten Inline-Daten. Der 12-Byte-Header liegt direkt
            # davor. Deshalb darf hier insbesondere nicht [eax+12] geladen
            # werden: Das würde vier Zeichen des Strings als Adresse
            # interpretieren.
            if (
                source_type == "string"
                and self.is_char_pointer_type(
                    target_type
                )
            ):
                if CDATA.args_target in (
                    "nt35",
                    "winnt",
                    "win32",
                    "win64"
                ):
                    return target_type

                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "String to PChar/PAnsiChar cast is not "
                        f"implemented for target {CDATA.args_target}"
                    )
                )

            if not (
                source_is_pointer
                or source_is_class
                or source_is_nil
                or integer_address_cast_allowed
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=source_type,
                    expected="pointer/class/nil/integer address"
                )
            return target_type

        if target_is_class:
            if not (
                source_is_pointer
                or source_is_class
                or source_is_nil
                or integer_address_cast_allowed
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=source_type,
                    expected="pointer/class/nil/integer address"
                )
            return target_type

        if target_type == "integer":
            if self.scalar_base_type(source_type) in (
                "integer",
                "boolean",
                "char"
            ):
                return "integer"

            if source_is_pointer or source_is_class:
                if CDATA.args_target not in (
                    "nt35",
                    "winnt",
                    "win32"
                ):
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "pointer to Integer cast is only "
                            "supported for NT32"
                        )
                    )
                return "integer"

            raise CompileError(
                ctx,
                "E0005",
                got=source_type,
                expected="integer/boolean/char/pointer"
            )

        if target_type == "boolean":
            if self.scalar_base_type(source_type) not in (
                "integer",
                "boolean",
                "char"
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=source_type,
                    expected="integer/boolean/char"
                )

            self.emit_cmp("eax", 0)
            self.emit_setne("al")
            self.emit_movzx("eax", "al")
            return "boolean"

        if target_type == "char":
            if self.scalar_base_type(source_type) not in (
                "integer",
                "char"
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=source_type,
                    expected="integer/char"
                )

            self.emit_and("eax", 0xFF, comment="cast to char")
            return "char"

        if target_type == "double":
            if source_type == "double":
                return "double"

            if self.scalar_base_type(source_type) in (
                "integer",
                "boolean",
                "char"
            ):
                self.emit_cvtsi2sd("xmm0", "eax")
                return "double"

            raise CompileError(
                ctx,
                "E0005",
                got=source_type,
                expected="integer/boolean/char/double"
            )

        # target_name kann ein Alias sein:
        #
        #   Cardinal -> DWord
        #   UInt32   -> DWord
        #
        # Die Subrange-Information muss deshalb über den bereits
        # aufgelösten Zieltyp gesucht werden.
        range_info = self.subrange_info(
            target_type
        )

        if range_info is not None:
            source_is_address = (
                source_is_pointer
                or source_is_class
                or source_is_nil
            )

            if source_is_address:
                if CDATA.args_target not in (
                    "nt35",
                    "winnt",
                    "win32"
                ):
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            "address to integer-subrange cast "
                            "is only supported for NT32"
                        )
                    )

                is_full_int32 = (
                    (
                        range_info.min_value == -2147483648
                        and range_info.max_value == 2147483647
                    )
                    or (
                        range_info.min_value == 0
                        and range_info.max_value == 4294967295
                    )
                )

                if (
                    range_info.base_type != "integer"
                    or range_info.size != 4
                    or not is_full_int32
                ):
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=source_type,
                        expected="full-width 32-bit integer type"
                    )

                # EAX enthält bereits den unveränderten 32-Bit-Zeiger.
                return target_type

            source_scalar_type = self.scalar_base_type(
                source_type
            )

            if source_scalar_type not in (
                "integer",
                "boolean",
                "char"
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=source_type,
                    expected="integer/boolean/char"
                )

            if range_info.base_type != "integer":
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "unsupported subrange cast base type: "
                        + str(range_info.base_type)
                    )
                )

            # Explizite Integer-Casts verhalten sich wie eine
            # Größenkonvertierung. Für vorzeichenlose kleine Typen
            # wird der Wert auf die passende Bitbreite begrenzt.
            if not range_info.signed:
                if range_info.size == 1:
                    self.emit_and(
                        "eax",
                        0xFF,
                        comment=f"cast to {target_name}"
                    )

                elif range_info.size == 2:
                    self.emit_and(
                        "eax",
                        0xFFFF,
                        comment=f"cast to {target_name}"
                    )

                elif range_info.size == 4:
                    # Cardinal/DWord: Der Wert befindet sich bereits
                    # als vollständiges 32-Bit-Muster in EAX.
                    pass

                else:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=(
                            f"unsupported subrange cast size: "
                            f"{range_info.size}"
                        )
                    )

            else:
                # Für vorzeichenbehaftete Subranges zunächst die
                # bestehende Bereichsprüfung weiterverwenden.
                self.emit_subrange_check(
                    ctx,
                    target_type,
                    "eax"
                )

            # Wichtig: den aufgelösten Typ zurückgeben.
            #
            # Cardinal -> dword
            # Word     -> word
            # Byte     -> byte
            return target_type

        raise CompileError(
            ctx,
            "E0019",
            text=f"unsupported explicit type cast: {target_name}({source_type})"
        )

    def emit_compile_time_string(
        self,
        ctx,
        value
    ):
        label = self.add_string_literal(
            str(value)
        )

        if CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        ):
            self.backend.writer.emit_push_data_label32(
                label
            )

            self.emit_call(
                "_jit_dynstring_from_cstr"
            )

            self.backend.emit_cleanup_stack(
                4
            )

            self.restore_nt32_context_after_runtime_call()

            return "string"

        if CDATA.args_target in (
            "dos",
            "dos16"
        ):
            self.backend.writer.emit_mov_dx_label(
                label
            )

            return "string"

        # Win64
        self.emit_mov_imm(
            "rcx",
            label
        )

        self.emit_mov_imm(
            "rax",
            "&_jit_dynstring_from_cstr"
        )

        self.emit_call(
            "rax"
        )

        return "string"

    def emit_builtin_owner_class_name(
        self,
        ctx
    ):
        args = self.function_call_args(
            ctx
        )

        if args:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="0"
            )

        if (
            self.current_class is None
            or self.current_method is None
        ):
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "OwnerClassName may only be used "
                    "inside a class method"
                )
            )

        owner_key = getattr(
            self.current_method,
            "owner",
            None
        )

        if not owner_key:
            owner_key = self.current_class

        owner_key = str(
            owner_key
        ).lower()

        owner_class = self.classes.get(
            owner_key
        )

        if owner_class is None:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    "class method owner not found: "
                    + str(owner_key)
                )
            )

        return self.emit_compile_time_string(
            ctx,
            owner_class.name
        )

    def visitFunctionCallExpr(self, ctx):
        names = list(ctx.functionName())

        if not names:
            raise CompileError(
                ctx,
                "E0015",
                text=ctx.getText()
            )
        
        name = names[0].getText()
        
        if len(names) >= 2:
            left_name   = names[0].getText()
            method_name = names[1].getText()

            # Klassenkonstruktor:
            #   TForm.Create(...)
            if (
                method_name.lower() == "create"
                and left_name.lower() in self.classes
            ):
                return self.emit_class_constructor_call(
                    ctx,
                    left_name,
                    method_name
                )

            # Prüfen, ob die linke Seite eine Klassenreferenz ist.
            object_info = self.find_local_var(
                left_name
            )

            if object_info is None:
                object_info = self.find_param(
                    left_name
                )

            object_type = None

            if object_info is not None:
                object_type = self.resolve_type(
                    object_info["type"]
                )
            else:
                self_field = self.find_current_class_field(
                    left_name
                )

                if self_field is not None:
                    object_type = self.resolve_type(
                        self_field.type
                    )
                else:
                    object_info = self.vars.get(
                        left_name.lower()
                    )

                    if object_info is not None:
                        object_type = self.resolve_type(
                            object_info["type"]
                        )

            # Objektmethode beziehungsweise Objektfunktion:
            #   AppForm.DispatchMessage(...)
            if object_type in self.classes:
                actuals = self.function_call_args(
                    ctx
                )

                return self.emit_object_method_call(
                    ctx,
                    left_name,
                    method_name,
                    actuals=actuals,
                    require_function=True
                )

            # Möglicherweise qualifizierte normale Funktion.
            name = method_name

        key  = name.lower()
        
        # ------------------------------------------------------------
        # Explizite Pascal-Typumwandlung
        #
        #     Pointer(P)
        #     PByte(Data)
        #     Word(Value)
        #
        # Nur unqualifizierte Aufrufe können Typcasts sein.
        # ------------------------------------------------------------
        if (
            len(names) == 1
            and self.is_known_type_name(name)
        ):
            return self.emit_explicit_type_cast(
                ctx,
                name
            )
        
        self.builtin_functions = {
            "ownerclassname": self.emit_builtin_owner_class_name,
            "assigned"      : self.emit_builtin_assigned,
            "length"        : self.emit_builtin_length,
            "low"           : self.emit_builtin_low,
            "high"          : self.emit_builtin_high,
            "paramcount"    : self.emit_builtin_paramcount,
            "paramstr"      : self.emit_builtin_paramstr,
            "commandline"   : self.emit_builtin_commandline,
            "copy"          : self.emit_builtin_copy,
            "pos"           : self.emit_builtin_pos,
        
            "blake2"        : self.emit_builtin_blake2,
            "blake3"        : self.emit_builtin_blake3,
            "crc16"         : self.emit_builtin_crc16,
            "crc32"         : self.emit_builtin_crc32,
            "crc32c"        : self.emit_builtin_crc32c,
            "crc64"         : self.emit_builtin_crc64,
            "md5"           : self.emit_builtin_md5,
            "sha1"          : self.emit_builtin_sha1,
            "sha3"          : self.emit_builtin_sha3,
            "sha224"        : self.emit_builtin_sha224,
            "sha256"        : self.emit_builtin_sha256,
            "sha384"        : self.emit_builtin_sha384,
            "sha512"        : self.emit_builtin_sha512,
            
            "diskfree"      : self.emit_builtin_diskfree,
            "disktotal"     : self.emit_builtin_disktotal,
            "disklabel"     : self.emit_builtin_disklabel,
            "diskserial"    : self.emit_builtin_diskserial,
            "diskfilesystem": self.emit_builtin_diskfilesystem,
            "disktype"      : self.emit_builtin_disktype,
            "diskshare"     : self.emit_builtin_diskshare,
        }
        handler = self.builtin_functions.get(key)
        if handler:
            return handler(ctx)
        
        func = self.find_function(name)

        if func is None:
            raise CompileError(ctx, "E0001", name=name)
        
        params = func.get("params", [])

        actuals = []
        if ctx.argumentList():
            actuals = list(ctx.argumentList().expr())

        if len(actuals) != len(params):
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected=str(len(params)))

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            arg_bytes = 0

            # --------------------------------------------------------
            # cdecl: Parameter rechts nach links auswerten und pushen
            # cdecl/stdcall: rechts nach links; pascal: links nach rechts.
            # --------------------------------------------------------
            for index in self.nt32_argument_order(
                func,
                len(actuals)
             ):
                arg_expr = actuals[index]
                formal   = params[index]

                raw_formal_type = formal.get(
                    "type"
                )

                formal_type = self.resolve_type(
                    raw_formal_type
                )

                # ====================================================
                # VAR-Parameter in Funktionsausdrücken
                #
                # GetMessageA(var Msg: TMsg; ...) erwartet die Adresse
                # des lokalen Records. Der Ausdruck darf deshalb nicht
                # über emit_load_local_var() als Record-Wert geladen
                # werden.
                # ====================================================
                if formal.get("is_var", False):
                    ref = self.expression_variable_ref(
                        ctx,
                        arg_expr
                    )

                    var_name = ref.IDENT().getText()
                    info = self.find_local_var(
                        var_name
                    )

                    if info is None:
                        info = self.var_info(
                            ctx,
                            var_name
                        )

                    actual_type = self.resolve_type(
                        info["type"]
                    )

                    if actual_type != formal_type:
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=actual_type,
                            expected=formal_type
                        )

                    self.emit_address_of_var(
                        ctx,
                        var_name
                    )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"function var parameter "
                            f"{index + 1}"
                        )
                    )

                    arg_bytes += 4
                    continue

                # Pascal-Deklaration und Maschinen-ABI getrennt behandeln.
                # Beispiele:
                #
                #   Byte/Cardinal/DWord/Word -> integer
                #   PAnsiChar                -> pointer
                #
                # Der deklarierte Typ bleibt für Diagnosen und strenge
                # Pointerprüfungen erhalten.
                declared_formal_type = formal_type
                formal_abi_type = self.scalar_base_type(
                    formal_type
                )

                is_open_array = (
                    formal.get(
                        "is_open_array",
                        False
                    )
                    or (
                        isinstance(formal_type, str)
                        and formal_type.startswith(
                            "open_array:"
                        )
                    )
                )

                is_variant_open_array = (
                    formal.get(
                        "is_variant_open_array",
                        False
                    )
                    or formal_type == "open_array:const"
                )

                # Alten Zustand löschen, damit keine Metadaten eines
                # vorherigen Arguments verwendet werden.
                self.pending_open_array_actual = None

                if is_variant_open_array:
                    self.emit_variant_open_array_actual_nt32(
                        ctx,
                        arg_expr
                    )
                    expr_type = "open_array:const"
                else:
                    expr_type = self.visit(
                        arg_expr
                    )

                    expr_type = self.resolve_type(
                        expr_type
                    )

                declared_expr_type = expr_type
                expr_abi_type = self.scalar_base_type(
                    expr_type
                )

                # ====================================================
                # Offenes Array
                #
                # function Sum(
                #     const Values: array of Integer
                # ): Integer;
                #
                # Interne NT32-ABI:
                #
                #     [ebp+8]  = data pointer
                #     [ebp+12] = High-Wert
                #
                # cdecl Push-Reihenfolge:
                #
                #     push High
                #     push data
                # ====================================================
                if is_open_array:
                    element_type = formal.get(
                        "element_type"
                    )

                    if not element_type:
                        element_type = formal_type.split(
                            ":",
                            1
                        )[1]

                    element_type = self.resolve_type(
                        element_type
                    )

                    expected_type = (
                        f"open_array:{element_type}"
                    )

                    if expr_type != expected_type:
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=expr_type,
                            expected=expected_type
                        )

                    actual_info = (
                        self.pending_open_array_actual
                    )

                    if actual_info is None:
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                "open-array expression returned a type, "
                                "but no open-array metadata"
                            )
                        )

                    high_value = actual_info[
                        "high"
                    ]

                    # EAX enthält weiterhin den Datenpointer.
                    #
                    # cdecl rechts nach links:
                    #
                    #     push High
                    #     push data
                    self.backend.writer.emit_push_imm32(
                        high_value
                    )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"open-array data parameter "
                            f"{index + 1}"
                        )
                    )

                    arg_bytes += 8

                    self.pending_open_array_actual = None
                    continue

                # ====================================================
                # Integer und Integer-Subranges
                #
                # Word, Byte, DWord, Cardinal usw. werden unter NT32
                # als 32-Bit-Wert übergeben. Die Pascal-Typinformation
                # bleibt trotzdem in declared_* erhalten.
                # ====================================================
                if formal_abi_type == "integer":
                    if expr_abi_type != "integer":
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=declared_expr_type,
                            expected=declared_formal_type
                        )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"function integer/subrange parameter "
                            f"{index + 1}: "
                            f"{declared_formal_type}"
                        )
                    )

                    arg_bytes += 4
                    continue

                # ====================================================
                # Boolean
                # ====================================================
                if formal_abi_type == "boolean":
                    if expr_abi_type not in (
                        "boolean",
                        "integer"
                    ):
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=declared_expr_type,
                            expected=declared_formal_type
                        )

                    self.emit_and(
                        "eax",
                        1,
                        comment="normalize boolean"
                    )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"function boolean parameter "
                            f"{index + 1}"
                        )
                    )

                    arg_bytes += 4
                    continue

                # ====================================================
                # Char
                # ====================================================
                if formal_abi_type == "char":
                    if expr_abi_type != "char":
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=declared_expr_type,
                            expected=declared_formal_type
                        )

                    self.emit_and(
                        "eax",
                        0xFF,
                        comment="normalize char"
                    )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"function char parameter "
                            f"{index + 1}"
                        )
                    )

                    arg_bytes += 4
                    continue

                # ====================================================
                # String
                # ====================================================
                if formal_abi_type == "string":
                    if expr_abi_type != "string":
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=declared_expr_type,
                            expected=declared_formal_type
                        )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"function string parameter "
                            f"{index + 1}"
                        )
                    )

                    arg_bytes += 4
                    continue

                # ====================================================
                # Double
                # ====================================================
                if formal_abi_type == "double":
                    if expr_abi_type != "double":
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=declared_expr_type,
                            expected=declared_formal_type
                        )

                    self.emit_sub(
                        "esp",
                        8,
                        comment=(
                            f"function double parameter "
                            f"{index + 1}"
                        )
                    )

                    self.backend.emit_movsd_store(
                        "esp",
                        0,
                        "xmm0"
                    )

                    arg_bytes += 8
                    continue

                # ====================================================
                # Pointer
                # ====================================================
                if self.is_pointer_type(formal_type, include_nil=False):
                    if formal_type == "pointer":
                        # Generischer Pointer akzeptiert:
                        #   Pointer
                        #   ^T
                        #   Klasseninstanz
                        #   nil
                        if not self.is_pointer_type(expr_type):
                            raise CompileError(
                                ctx,
                                "E0005",
                                got=expr_type,
                                expected="pointer"
                            )

                    else:
                        # Typisierter Pointer bleibt grundsätzlich streng.
                        # Ein expliziter Pointer(...) Cast darf ihn jedoch
                        # ebenfalls passieren.
                        if expr_type not in (
                            formal_type,
                            "pointer",
                            "^nil"
                        ):
                            raise CompileError(
                                ctx,
                                "E0005",
                                got=expr_type,
                                expected=formal_type
                            )

                    self.emit_push("eax",
                        comment=(
                            f"function pointer parameter "
                            f"{index + 1}"
                        )
                    )

                    arg_bytes += 4
                    continue

                raise CompileError(
                    ctx,
                    "E0005",

                    # Nicht formal_type verwenden:
                    got=expr_type,

                    expected=(
                        "boolean/integer/subrange/char/string/"
                        "double/pointer/open-array"
                    )
                )

            self.emit_registered_routine_call(
                func
            )

            self.finish_nt32_routine_call(
                func,
                arg_bytes
            )

            return self.resolve_type(
                func["return_type"]
            )
            
        else:
            int_regs = ["ecx", "edx", "r8d", "r9d"]
            
            self.emit_sub("rsp", 32, comment = "shadow space for function call")
            self.emit_registered_routine_call(func)
            self.emit_add("rsp", 32)

            return func["return_type"].lower()
    
    def visitProcedureDeclaration(self, ctx):
        name = ctx.IDENT().getText()
        key  = name.lower()

        convention = (
            self.local_routine_calling_convention(
                ctx
            )
        )
        
        # --------------------------------------------------------------
        # Externe Prozedur
        # --------------------------------------------------------------
        if self.routine_is_external(ctx):
            params = self.collect_formal_params(
                ctx
            )

            directive = (
                ctx.externalRoutineDirective()
            )

            dll_name = (
                self.routine_external_library(
                    ctx
                )
            )

            if dll_name is None:
                return self.register_local_external_routine(
                    ctx=ctx,
                    kind="procedure",
                    name=name,
                    params=params,
                    return_type=None,
                    convention=convention
                )

            return self.register_external_routine(
                ctx=ctx,
                kind="procedure",
                name=name,
                params=params,
                return_type=None,
                spec_ctx=directive,
                convention=convention
            )

        label      = self.new_named_label("proc_"     + name)
        skip_label = self.new_named_label("skipproc_" + name)
        exit_label = self.new_named_label("exitproc_" + name)

        params = self.collect_formal_params(ctx)

        if len(params) > 64:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(params)),
                expected="max 64 params"
            )

        scoped = self.unit_scoped_name(name)

        mangled = self.fpc_mangle_routine(
            name,
            params,
            self.current_unit if self.current_unit else None
        )

        self.procedures[key] = {
            "name": name,
            "scoped_name": scoped,
            "label": label,
            "mangled": mangled,
            "params": params,
            "calling_convention": convention
        }

        # Die COFF-Aliase dürfen hier noch nicht angelegt werden.
        # Das interne Label wird vom Writer erst während der vollständigen
        # Prozedur-Codeerzeugung als Symbol registriert. Die Aliase werden
        # deshalb nach dem Prozedur-Epilog und dem Skip-Label erzeugt.

        # Prozedurcode im normalen Programmfluss überspringen.
        self.emit_jmp(skip_label)
        self.emit_bind_label(label)

        old_params = self.current_proc_params
        self.current_proc_params = {}

        target = CDATA.args_target.lower()

        # --------------------------------------------------------------
        # Prolog und Parameterabbildung
        # --------------------------------------------------------------
        if target in ("nt35", "winnt", "win32"):
            self.emit_push(
                "ebp",
                comment="procedure prolog"
            )

            self.emit_mov(
                "ebp",
                "esp",
                comment="stack frame"
            )

            # EBX wird von mehreren Emittern als Arbeitsregister benutzt.
            self.emit_push(
                "ebx",
                comment="preserve EBX"
            )

            stack_offset = 8

            for param in params:
                pname = param["name"]

                param_info = {
                    "type": param["type"],
                    "reg": None,
                    "stack_offset": stack_offset,
                    "is_var": param.get("is_var", False),
                    "is_const": param.get("is_const", False),
                    "is_open_array": param.get(
                        "is_open_array",
                        False
                    ),
                    "is_variant_open_array": param.get(
                        "is_variant_open_array",
                        False
                    ),
                    "element_type": param.get("element_type")
                }

                if param_info["is_open_array"]:
                    # Interne NT32-ABI:
                    #
                    # [ebp + stack_offset]     = Datenpointer
                    # [ebp + stack_offset + 4] = High-Wert
                    param_info["high_offset"] = stack_offset + 4
                    stack_offset += 8
                else:
                    stack_offset += 4

                self.current_proc_params[
                    pname.lower()
                ] = param_info

            # [ebp-4] enthält den gesicherten EBX-Wert.
            local_base_offset = 4

        elif target in ("dos", "dos16"):
            self.backend.writer.emit_push_reg16("bp")
            self.backend.writer.emit_mov_reg16_reg16(
                "bp",
                "sp"
            )

            stack_offset = 4

            for param in params:
                pname = param["name"]

                param_info = {
                    "type": param["type"],
                    "reg": None,
                    "stack_offset": stack_offset,
                    "is_var": param.get("is_var", False),
                    "is_const": param.get("is_const", False),
                    "is_open_array": param.get(
                        "is_open_array",
                        False
                    ),
                    "is_variant_open_array": param.get(
                        "is_variant_open_array",
                        False
                    ),
                    "element_type": param.get("element_type")
                }

                if param_info["is_open_array"]:
                    param_info["high_offset"] = stack_offset + 2
                    stack_offset += 4
                else:
                    stack_offset += 2

                self.current_proc_params[
                    pname.lower()
                ] = param_info

            local_base_offset = 0

        else:
            self.emit_push(
                "rbp",
                comment="procedure prolog"
            )

            self.emit_mov(
                "rbp",
                "rsp",
                comment="stack frame"
            )

            param_regs = [
                "rcx",
                "rdx",
                "r8",
                "r9"
            ]

            saved_param_count = min(
                len(params),
                len(param_regs)
            )

            for index, param in enumerate(params):
                pname = param["name"]

                if index < len(param_regs):
                    reg = param_regs[index]

                    self.emit_push(
                        reg,
                        comment=f"save param {pname}"
                    )

                    stack_offset = -8 * (index + 1)
                else:
                    reg = None
                    stack_offset = 48 + ((index - 4) * 8)

                self.current_proc_params[pname.lower()] = {
                    "type": param["type"],
                    "reg": reg,
                    "stack_offset": stack_offset,
                    "is_var": param.get("is_var", False),
                    "is_const": param.get("is_const", False),
                    "is_open_array": param.get(
                        "is_open_array",
                        False
                    ),
                    "is_variant_open_array": param.get(
                        "is_variant_open_array",
                        False
                    ),
                    "element_type": param.get("element_type")
                }

            local_base_offset = saved_param_count * 8

        # --------------------------------------------------------------
        # Lokale Scopes VOR den Deklarationen öffnen.
        # --------------------------------------------------------------
        self.exit_label_stack.append(exit_label)
        self.scope_stack.append(name)
        self.push_local_scope()
        self.push_const_scope()

        scope = self.current_local_scope()

        # Bereits belegte negative Stackplätze nicht überschreiben.
        scope["next_offset"] = local_base_offset

        nested_declarations = []

        def process_local_declaration(declaration):
            if declaration is None:
                return

            var_section = (
                declaration.varSection()
                if hasattr(declaration, "varSection")
                else None
            )

            const_section = (
                declaration.constSection()
                if hasattr(declaration, "constSection")
                else None
            )

            type_section = (
                declaration.typeSection()
                if hasattr(declaration, "typeSection")
                else None
            )

            procedure_declaration = (
                declaration.procedureDeclaration()
                if hasattr(declaration, "procedureDeclaration")
                else None
            )

            function_declaration = (
                declaration.functionDeclaration()
                if hasattr(declaration, "functionDeclaration")
                else None
            )

            if var_section is not None:
                self.visitVarSection(var_section)
                return

            if const_section is not None:
                self.visitConstSection(const_section)
                return

            if type_section is not None:
                self.visitTypeSection(type_section)
                return

            if procedure_declaration is not None:
                nested_declarations.append(
                    procedure_declaration
                )
                return

            if function_declaration is not None:
                nested_declarations.append(
                    function_declaration
                )

        # --------------------------------------------------------------
        # Laut Grammar stehen lokale Deklarationen direkt in
        # procedureDeclaration.declarationPart().
        # --------------------------------------------------------------
        if hasattr(ctx, "declarationPart"):
            for declaration in ctx.declarationPart():
                process_local_declaration(declaration)

        block_ctx = ctx.block()

        if block_ctx is None:
            raise CompileError(
                ctx,
                "E0015",
                text="procedure block missing"
            )

        # Zusätzlich block.localDeclaration() berücksichtigen.
        if hasattr(block_ctx, "localDeclaration"):
            for declaration in block_ctx.localDeclaration():
                process_local_declaration(declaration)

        local_bytes = scope["next_offset"] - local_base_offset

        if target in ("dos", "dos16"):
            aligned_local_bytes = (local_bytes + 1) & ~1

            if aligned_local_bytes:
                self.emit_sub(
                    "sp",
                    aligned_local_bytes,
                    comment=f"{aligned_local_bytes} bytes locals"
                )

        elif target in ("nt35", "winnt", "win32"):
            aligned_local_bytes = (local_bytes + 15) & ~15

            if aligned_local_bytes:
                self.emit_sub(
                    "esp",
                    aligned_local_bytes,
                    comment=f"{aligned_local_bytes} bytes locals"
                )

        else:
            aligned_local_bytes = (local_bytes + 15) & ~15

            if aligned_local_bytes:
                self.emit_sub(
                    "rsp",
                    aligned_local_bytes,
                    comment=f"{aligned_local_bytes} bytes locals"
                )

        # Verschachtelte Routinen erst nach lokalen Typen/Konstanten.
        for declaration in nested_declarations:
            self.visit(declaration)

        # Nur ausführbare Statements besuchen. Die Deklarationen wurden
        # bereits verarbeitet und dürfen nicht doppelt besucht werden.
        statement_list = block_ctx.statementList()

        if statement_list is not None:
            self.visit(statement_list)

        self.pop_const_scope()
        self.pop_local_scope()
        self.scope_stack.pop()
        self.exit_label_stack.pop()

        self.current_proc_params = old_params

        # --------------------------------------------------------------
        # Gemeinsamer EXIT-Punkt und Epilog
        # --------------------------------------------------------------
        self.emit_bind_label(exit_label)

        if target in ("nt35", "winnt", "win32"):
            self.emit_mov_dword_ptr(
                "ebx",
                "ebp",
                -4,
                comment="restore EBX"
            )

            self.emit_mov(
                "esp",
                "ebp"
            )

            self.emit_pop("ebp")
            #self.emit_ret() ### hier

            stack_bytes = self.nt32_parameter_stack_bytes(
                params
            )

            if convention in ("stdcall", "pascal") and stack_bytes:
                self.writer.emit_ret_imm16(stack_bytes)
            else:
                self.emit_ret()

        elif target in ("dos", "dos16"):
            self.backend.writer.emit_mov_reg16_reg16(
                "sp",
                "bp"
            )

            self.backend.writer.emit_pop_reg16("bp")
            self.backend.writer.emit_ret()

        else:
            self.emit_mov(
                "rsp",
                "rbp"
            )

            self.emit_pop("rbp")
            self.emit_ret()

        self.emit_bind_label(skip_label)

        # --------------------------------------------------------------
        # COFF-Symbole erst nach vollständiger Prozedur-Codeerzeugung
        # aliasieren. Zu diesem Zeitpunkt muss das interne Label bereits
        # als Writer-Symbol existieren. Das entspricht dem bereits
        # funktionierenden Ablauf bei visitFunctionDeclaration().
        # --------------------------------------------------------------
        if (
            CDATA.args_target in (
                "nt35",
                "winnt",
                "win32"
            )
            and hasattr(
                self.backend.writer,
                "add_symbol_alias"
            )
        ):
            target_index = (
                self.backend.writer.find_symbol_index(
                    label
                )
            )

            if target_index is None:
                raise RuntimeError(
                    "internal procedure symbol was not generated: "
                    f"{label}"
                )

            if (
                self.backend.writer.find_symbol_index(
                    mangled
                )
                is None
            ):
                self.backend.writer.add_symbol_alias(
                    mangled,
                    label
                )

            # Historischen Alias nur bei Programmen beibehalten.
            if not self.current_unit:
                legacy_symbol = "_" + name.lower()

                if (
                    self.backend.writer.find_symbol_index(
                        legacy_symbol
                    )
                    is None
                ):
                    self.backend.writer.add_symbol_alias(
                        legacy_symbol,
                        label
                    )

        return None

    def visitProcedureCallStatement(self, ctx):
        idents = list(ctx.IDENT())

        if not idents:
            raise CompileError(
                ctx,
                "E0019",
                text="procedure or function name missing"
            )

        name = idents[0].getText()
        key  = name.lower()

        param_regs = [
            "rcx",
            "rdx",
            "r8",
            "r9"
        ]

        # ------------------------------------------------------------------
        # Objektmethoden
        # ------------------------------------------------------------------
        if ctx.DOT():
            if len(idents) < 2:
                raise CompileError(
                    ctx,
                    "E0019",
                    text="method name missing after '.'"
                )

            obj_name    = idents[0].getText()
            method_name = idents[1].getText()

            if method_name.lower() == "free":
                return self.emit_class_free_call(
                    ctx,
                    obj_name
                )

            actuals = []

            if ctx.actualParamList():
                actuals = list(
                    ctx.actualParamList().actualParam()
                )

            return self.emit_object_method_call(
                ctx,
                obj_name,
                method_name,
                actuals=actuals,
                require_function=False
            )

        # ------------------------------------------------------------------
        # Eingebaute Prozeduren
        # ------------------------------------------------------------------
        if key == "new":
            return self.emit_builtin_new(ctx)

        if key == "dispose":
            return self.emit_builtin_dispose(ctx)

        if key == "setlength":
            return self.emit_builtin_setlength(ctx)

        if key == "readln":
            return self.emit_builtin_readln(ctx)

        if key == "__debug_break":
            return self.emit_builtin_debug_break()

        # ------------------------------------------------------------------
        # Funktion oder Prozedur suchen
        #
        # Funktionen dürfen auch als Statement aufgerufen werden.
        # Der Rückgabewert wird dann einfach verworfen.
        # ------------------------------------------------------------------
        routine = self.find_function(name)

        if routine is None:
            routine = self.procedures.get(key)

        if routine is None:
            raise CompileError(
                ctx,
                "E0001",
                name=name
            )

        params = routine.get("params", [])

        actuals = []

        if ctx.actualParamList():
            actuals = list(
                ctx.actualParamList().actualParam()
            )

        if len(actuals) != len(params):
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(actuals)),
                expected=str(len(params))
            )

        # ==================================================================
        # DOS16
        # ==================================================================
        if CDATA.args_target in ("dos", "dos16"):
            if actuals:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "procedure/function calls with parameters "
                        "are not implemented for DOS16 yet"
                    )
                )

            self.emit_registered_routine_call(routine)
            return None

        # ==================================================================
        # NT32 / Win32
        # ==================================================================
        if CDATA.args_target in (
            "nt35",
            "winnt",
            "win32"
        ):
            convention = str(
                routine.get(
                    "calling_convention",
                    "cdecl"
                )
            ).lower()

            # Optionaler interner Alias.
            if convention == "c":
                convention = "cdecl"

            if convention not in (
                "cdecl",
                "stdcall",
                "pascal"
            ):
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "unsupported NT32 calling convention: "
                        + convention
                    )
                )

            # --------------------------------------------------------------
            # Reihenfolge der Parameter
            #
            # cdecl   : rechts nach links
            # stdcall : rechts nach links
            # pascal  : links nach rechts
            # --------------------------------------------------------------
            if convention == "pascal":
                argument_indices = range(
                    0,
                    len(actuals)
                )
            else:
                argument_indices = range(
                    len(actuals) - 1,
                    -1,
                    -1
                )

            arg_bytes = 0

            for index in argument_indices:
                arg    = actuals[index]
                formal = params[index]

                formal_type = self.resolve_type(
                    formal["type"]
                )
                
                declared_formal_type = formal_type
                formal_abi_type = self.scalar_base_type(
                    formal_type
                )

                is_open_array = (
                    formal.get(
                        "is_open_array",
                        False
                    )
                    or (
                        isinstance(formal_type, str)
                        and formal_type.startswith("open_array:")
                    )
                )

                is_variant_open_array = (
                    formal.get(
                        "is_variant_open_array",
                        False
                    )
                    or formal_type == "open_array:const"
                )

                # ----------------------------------------------------------
                # Offenes Array / array of const
                # ----------------------------------------------------------
                if is_open_array:
                    if convention == "pascal":
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                "open-array parameters with Pascal "
                                "calling convention are not implemented"
                            )
                        )

                    argument_expr = (
                        arg.expr()
                        if arg.expr() is not None
                        else arg
                    )

                    self.pending_open_array_actual = None

                    if is_variant_open_array:
                        actual_info = (
                            self.emit_variant_open_array_actual_nt32(
                                ctx,
                                argument_expr
                            )
                        )
                        expr_type = "open_array:const"
                    else:
                        expr_type = self.visit_actual_param_expr(
                            arg
                        )
                        expr_type = self.resolve_type(
                            expr_type
                        )
                        actual_info = (
                            self.pending_open_array_actual
                        )

                    if expr_type != formal_type:
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=expr_type,
                            expected=formal_type
                        )

                    if actual_info is None:
                        raise CompileError(
                            ctx,
                            "E0019",
                            text=(
                                "open-array expression produced "
                                "no metadata"
                            )
                        )

                    # Interne NT32-cdecl-ABI:
                    #   push High
                    #   push data
                    self.backend.writer.emit_push_imm32(
                        int(actual_info["high"])
                    )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"open-array data parameter "
                            f"{index + 1}"
                        )
                    )

                    arg_bytes += 8
                    self.pending_open_array_actual = None
                    continue

                # ----------------------------------------------------------
                # VAR-Parameter
                # ----------------------------------------------------------
                if formal.get("is_var", False):
                    ref = self.actual_param_variable_ref(
                        ctx,
                        arg
                    )

                    if ref is None:
                        raise CompileError(
                            ctx,
                            "E0005",
                            got="expression",
                            expected="addressable variable"
                        )

                    var_name = ref.IDENT().getText()

                    actual_type = self.addressable_name_type(
                        ctx,
                        var_name
                    )

                    if actual_type != formal_type:
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=actual_type,
                            expected=formal_type
                        )

                    self.emit_address_of_var(
                        ctx,
                        var_name
                    )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"var parameter {index + 1}"
                        )
                    )

                    arg_bytes += 4
                    continue

                # ----------------------------------------------------------
                # Ausdruck auswerten
                # ----------------------------------------------------------
                expr_type = self.visit_actual_param_expr(
                    arg
                )

                expr_type = self.resolve_type(
                    expr_type
                )

                declared_expr_type = expr_type
                expr_abi_type = self.scalar_base_type(
                    expr_type
                )

                # ----------------------------------------------------------
                # Boolean
                # ----------------------------------------------------------
                if formal_abi_type == "boolean":
                    if expr_abi_type not in (
                        "boolean",
                        "integer"
                    ):
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=declared_expr_type,
                            expected=declared_formal_type
                        )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"boolean parameter {index + 1}"
                        )
                    )

                    arg_bytes += 4
                    continue

                # ----------------------------------------------------------
                # Integer
                # ----------------------------------------------------------
                if formal_abi_type == "integer":
                    if expr_abi_type != "integer":
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=declared_expr_type,
                            expected=declared_formal_type
                        )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"integer/subrange parameter "
                            f"{index + 1}: "
                            f"{declared_formal_type}"
                        )
                    )

                    arg_bytes += 4
                    continue

                # ----------------------------------------------------------
                # Char
                # ----------------------------------------------------------
                if formal_abi_type == "char":
                    if expr_abi_type != "char":
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=declared_expr_type,
                            expected=declared_formal_type
                        )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"char parameter {index + 1}"
                        )
                    )

                    arg_bytes += 4
                    continue

                # ----------------------------------------------------------
                # String
                # ----------------------------------------------------------
                if formal_abi_type == "string":
                    if expr_abi_type != "string":
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=declared_expr_type,
                            expected=declared_formal_type
                        )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"string parameter {index + 1}"
                        )
                    )

                    arg_bytes += 4
                    continue

                # ----------------------------------------------------------
                # Double
                #
                # Das Ergebnis liegt in XMM0. Auf NT32 werden acht Byte
                # direkt auf dem Stack reserviert und dort gespeichert.
                # ----------------------------------------------------------
                if formal_abi_type == "double":
                    if expr_abi_type != "double":
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=declared_expr_type,
                            expected=declared_formal_type
                        )

                    self.emit_sub(
                        "esp",
                        8,
                        comment=(
                            f"double parameter {index + 1}"
                        )
                    )

                    self.backend.emit_movsd_store(
                        "esp",
                        0,
                        "xmm0"
                    )

                    arg_bytes += 8
                    continue

                # ----------------------------------------------------------
                # Pointer
                #
                # Unterstützt:
                #   Pointer
                #   ^Integer
                #   ^Record
                #   Klasseninstanzen
                #   nil
                # ----------------------------------------------------------
                if self.is_pointer_type(formal_type, include_nil=False):
                    if formal_type == "pointer":
                        # Der generische Typ Pointer akzeptiert alle
                        # Pointer- und Klassenreferenzen sowie nil.
                        if not self.is_pointer_type(
                            expr_type
                        ):
                            raise CompileError(
                                ctx,
                                "E0005",
                                got=expr_type,
                                expected="pointer"
                            )

                    else:
                        # Typisierte Pointer bleiben streng.
                        # Ein expliziter Pointer(...) Cast darf ebenfalls
                        # übergeben werden.
                        if expr_type not in (
                            formal_type,
                            "pointer",
                            "^nil"
                        ):
                            raise CompileError(
                                ctx,
                                "E0005",
                                got=expr_type,
                                expected=formal_type
                            )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"pointer parameter {index + 1}"
                        )
                    )

                    arg_bytes += 4
                    continue

                # ----------------------------------------------------------
                # Klasseninstanz
                #
                # Eine Klassenvariable ist unter NT32 ein 32-Bit-
                # Objektpointer.
                # ----------------------------------------------------------
                if (
                    isinstance(formal_type, str)
                    and formal_type in self.classes
                ):
                    if expr_type != formal_type:
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=expr_type,
                            expected=formal_type
                        )

                    self.emit_push(
                        "eax",
                        comment=(
                            f"object parameter {index + 1}"
                        )
                    )

                    arg_bytes += 4
                    continue

                raise CompileError(
                    ctx,
                    "E0005",
                    got=formal_type,
                    expected=(
                        "integer/boolean/char/string/"
                        "double/pointer/class"
                    )
                )

            # --------------------------------------------------------------
            # Externe oder lokale Routine aufrufen
            # --------------------------------------------------------------
            self.emit_registered_routine_call(
                routine,
                comment=name
            )

            # --------------------------------------------------------------
            # Stackbereinigung
            #
            # cdecl:
            #     Aufrufer räumt den Stack auf.
            #
            # stdcall / pascal:
            #     Die aufgerufene Funktion verwendet RET n.
            # --------------------------------------------------------------
            if convention == "cdecl" and arg_bytes:
                self.emit_add(
                    "esp",
                    arg_bytes,
                    comment="cdecl caller cleanup"
                )

            return None

        # ==================================================================
        # Windows x64
        # ==================================================================
        def emit_push_argument(index):
            arg    = actuals[index]
            formal = params[index]

            formal_type = self.resolve_type(
                formal["type"]
            )

            # --------------------------------------------------------------
            # VAR-Parameter
            # --------------------------------------------------------------
            if formal.get("is_var", False):
                ref = self.actual_param_variable_ref(
                    ctx,
                    arg
                )

                if ref is None:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got="expression",
                        expected="addressable variable"
                    )

                var_name = ref.IDENT().getText()

                actual_type = self.addressable_name_type(
                    ctx,
                    var_name
                )

                if actual_type != formal_type:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=actual_type,
                        expected=formal_type
                    )

                self.emit_address_of_var(
                    ctx,
                    var_name
                )

                self.emit_push(
                    "rax",
                    comment=(
                        f"var parameter {index + 1}"
                    )
                )

                return

            # --------------------------------------------------------------
            # Ausdruck auswerten
            # --------------------------------------------------------------
            expr_type = self.visit_actual_param_expr(
                arg
            )

            expr_type = self.resolve_type(
                expr_type
            )

            # --------------------------------------------------------------
            # Integer
            # --------------------------------------------------------------
            if formal_type == "integer":
                if expr_type != "integer":
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=expr_type,
                        expected="integer"
                    )

                self.emit_movsxd(
                    "rax",
                    "eax"
                )

                self.emit_push(
                    "rax",
                    comment=(
                        f"integer parameter {index + 1}"
                    )
                )

                return

            # --------------------------------------------------------------
            # Boolean
            # --------------------------------------------------------------
            if formal_type == "boolean":
                if expr_type not in (
                    "boolean",
                    "integer"
                ):
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=expr_type,
                        expected="boolean/integer"
                    )

                self.emit_movsxd(
                    "rax",
                    "eax"
                )

                self.emit_push(
                    "rax",
                    comment=(
                        f"boolean parameter {index + 1}"
                    )
                )

                return

            # --------------------------------------------------------------
            # Char
            # --------------------------------------------------------------
            if formal_type == "char":
                if expr_type != "char":
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=expr_type,
                        expected="char"
                    )

                self.emit_movsxd(
                    "rax",
                    "eax"
                )

                self.emit_push(
                    "rax",
                    comment=(
                        f"char parameter {index + 1}"
                    )
                )

                return

            # --------------------------------------------------------------
            # String
            # --------------------------------------------------------------
            if formal_type == "string":
                if expr_type != "string":
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=expr_type,
                        expected="string"
                    )

                self.emit_push(
                    "rax",
                    comment=(
                        f"string parameter {index + 1}"
                    )
                )

                return

            # --------------------------------------------------------------
            # Pointer
            # --------------------------------------------------------------
            if self.is_pointer_type(
                formal_type,
                include_nil=False
            ):
                if formal_type == "pointer":
                    if not self.is_pointer_type(
                        expr_type
                    ):
                        raise CompileError(
                            ctx,
                            "E0005",
                            got=expr_type,
                            expected="pointer"
                        )

                elif expr_type not in (
                    formal_type,
                    "pointer",
                    "^nil"
                ):
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=expr_type,
                        expected=formal_type
                    )

                self.emit_push(
                    "rax",
                    comment=(
                        f"pointer parameter {index + 1}"
                    )
                )

                return
            # --------------------------------------------------------------
            # Klasseninstanz
            # --------------------------------------------------------------
            if (
                isinstance(formal_type, str)
                and formal_type in self.classes
            ):
                if expr_type != formal_type:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=expr_type,
                        expected=formal_type
                    )

                self.emit_push(
                    "rax",
                    comment=(
                        f"object parameter {index + 1}"
                    )
                )

                return

            # Double benötigt unter Win64 eine gesonderte Zuweisung
            # an XMM0..XMM3 beziehungsweise einen Stack-Slot.
            if formal_type == "double":
                raise CompileError(
                    ctx,
                    "E0019",
                    text=(
                        "double parameters in Win64 procedure "
                        "statements are not implemented yet"
                    )
                )

            raise CompileError(
                ctx,
                "E0005",
                got       = expr_type,
                expected  = (
                    "integer/boolean/char/string/"
                    "pointer/class"
                )
            )

        # ------------------------------------------------------------------
        # Parameter 5..N liegen auf dem Stack.
        #
        # Das Alignment-Padding muss VOR den Stackparametern angelegt
        # werden. Andernfalls würde Parameter 5 nicht mehr an seiner
        # vorgeschriebenen Position liegen.
        # ------------------------------------------------------------------
        stack_count = max(
            0,
            len(actuals) - 4
        )

        align_pad = 0

        if stack_count % 2 == 1:
            self.emit_sub(
                "rsp",
                8,
                comment="align stack before stack arguments"
            )

            align_pad = 8

        # Parameter N..5 rückwärts pushen.
        # Danach liegt Parameter 5 oben auf dem Stack.
        for index in range(
            len(actuals) - 1,
            3,
            -1
        ):
            emit_push_argument(index)

        # ------------------------------------------------------------------
        # Parameter 1..4 temporär auf den Stack legen und danach in
        # RCX, RDX, R8 und R9 laden.
        # ------------------------------------------------------------------
        reg_count = min(
            4,
            len(actuals)
        )

        for index in range(
            reg_count - 1,
            -1,
            -1
        ):
            emit_push_argument(index)

        for index in range(reg_count):
            self.emit_pop(
                param_regs[index],
                comment=(
                    f"load parameter {index + 1}"
                )
            )

        # ------------------------------------------------------------------
        # Windows-x64 Shadow Space
        # ------------------------------------------------------------------
        self.emit_sub(
            "rsp",
            32,
            comment="Windows x64 shadow space"
        )

        self.emit_registered_routine_call(
            routine,
            comment=name
        )

        self.emit_add(
            "rsp",
            32,
            comment="remove Windows x64 shadow space"
        )

        # ------------------------------------------------------------------
        # Stackparameter entfernen
        # ------------------------------------------------------------------
        if stack_count:
            self.emit_add(
                "rsp",
                stack_count * 8,
                comment="remove stack parameters"
            )

        if align_pad:
            self.emit_add(
                "rsp",
                align_pad,
                comment="remove stack alignment padding"
            )

        return None
    
    def visitIfStatement(self, ctx):
        self.emit_if_statement(ctx)
        return None
    
    def visitCompoundStatement(self, ctx):
        return self.visit(ctx.statementList())
    
    def visitWhileStatement(self, ctx):
        self.emit_while_statement(ctx)
        return None
    
    def visitRepeatStatement(self, ctx):
        return self.emit_repeat_statement(ctx)
    
    def visitForStatement(self, ctx):
        return self.emit_for_statement(ctx)
    
    def emit_nt32_call_cdecl(self, name, arg_bytes):
        self.backend.emit_call(name)
        if arg_bytes:
            self.emit_add("esp", arg_bytes)
    
    def visitWriteLnStatement(self, ctx):
        args = ctx.writeArgList()
        
        if args:
            for arg in args.writeArg():
                if arg.STRING():
                    value = arg.STRING().getText()[1:-1]
                    label = self.add_string_literal(value)
                    
                    if CDATA.args_target in ["nt35", "winnt", "win32"]:
                        self.backend.writer.emit_push_data_label32(label)
                        self.emit_nt32_call_cdecl("_jit_print_text", 4)
                    else:
                        self.emit_mov_imm("rcx", f"{label}")
                        self.emit_mov_imm("rax", "&_jit_print_text")
                        self.emit_call_rax()
                else:
                    if arg.expr() and arg.expr().getText().lower() in self.current_proc_params:
                        pname  = arg.expr().getText().lower()
                        pinfo  = self.current_proc_params[pname]
                        offset = pinfo["stack_offset"]
                        
                        if pinfo["type"] == "integer":
                            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                                self.emit_mov_dword_ptr("eax", "ebp", offset)
                                self.emit_push("eax")
                                self.emit_nt32_call_cdecl("_jit_print_int", 4)
                                continue
                            else:
                                offset = pinfo["stack_offset"]
                                self.emit_mov_dword_ptr("eax", "rbp", offset, comment=f"load integer parameter")
                                self.emit_mov("ecx", "eax")
                                self.emit_mov_imm("rax", "&_jit_print_int")
                                self.emit_call_rax()
                                continue
                            
                        if pinfo["type"] == "string":
                            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                                self.emit_mov_dword_ptr("eax", "ebp", offset, comment="load string parameter")
                                self.emit_push("eax")
                                self.emit_nt32_call_cdecl("_jit_print_text", 4)
                            else:
                                self.emit_mov_qword_ptr("rax", "rbp", offset, comment="load string parameter")
                                self.emit_mov("rcx", "rax")
                                self.emit_mov_imm("rax", "&_jit_print_text")
                                self.emit_call_rax()

                            continue
                    
                    expr_type = self.visit(arg.expr())
                    
                    if expr_type == "char":
                        if CDATA.args_target in ["nt35", "winnt", "win32"]:
                            self.emit_push("eax")
                            self.emit_nt32_call_cdecl("_jit_print_char", 4)
                        else:
                            self.emit_mov("ecx", "eax")
                            self.emit_mov_imm("rax", "&_jit_print_char")
                            self.emit_call_rax()
                    
                    elif expr_type == "string":
                        if CDATA.args_target in ["dos", "dos16"]:
                            # DX enthält bereits Offset auf $-String
                            self.backend.writer.emit_print_string_current_dx()
                        elif CDATA.args_target in ["nt35", "winnt", "win32"]:
                            self.emit_push("rax")
                            self.emit_nt32_call_cdecl("_jit_print_text", 4)
                        else:
                            self.emit_mov("rcx", "rax")
                            self.emit_mov_imm("rax", "&_jit_print_text")
                            self.emit_call_rax()
                    
                    elif expr_type in ("integer", "boolean"):
                        if CDATA.args_target in ["nt35", "winnt", "win32"]:
                            self.emit_push("eax")
                            self.emit_nt32_call_cdecl("_jit_print_int", 4)
                        else:
                            self.emit_mov("ecx", "eax")
                            self.emit_mov_imm("rax", "&_jit_print_int")
                            self.emit_call_rax()
                    
                    elif expr_type == "double":
                        if CDATA.args_target in ["nt35", "winnt", "win32"]:
                            self.backend.writer.emit_sub_reg_imm32("esp", 8)
                            self.backend.writer.emit_movsd_qword_ptr_esp_xmm0()
                            self.emit_nt32_call_cdecl("_jit_print_double", 8)
                        else:
                            # Windows x64: double-Argument liegt in xmm0
                            self.emit_mov_imm("rax", "&_jit_print_double")
                            self.emit_call_rax()

                    elif expr_type == "variant":
                        if CDATA.args_target in ["nt35", "winnt", "win32"]:
                            # EAX zeigt auf einen JitVariantArg-Deskriptor.
                            self.emit_push(
                                "eax",
                                comment="variant descriptor"
                            )
                            self.emit_nt32_call_cdecl(
                                "_jit_print_variant",
                                4
                            )
                        else:
                            raise CompileError(
                                arg,
                                "E0019",
                                text=(
                                    "variant output is currently "
                                    "implemented only for NT32"
                                )
                            )
        
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_nt32_call_cdecl("_jit_print_newline", 0)
        else:
            self.emit_mov_imm("rax", "&_jit_print_newline")
            self.emit_call_rax()
        
        return None
    
    def cpp_escape(self, text):
        return (
            text
            .replace("\\", "\\\\")
            .replace("\"", "\\\"")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
        )
    
    def new_named_label(self, prefix):
        name = self.new_label_name(prefix)
        asmjit_label = f"L{len(self.asm_label_mappings)}"

        self.emit_new_label_decl(name)

        self.add_asm_label_mapping(
            asmjit_label,
            name
        )

        return name
    
    def render_asm_exports(self):
        out = []

        for item in self.exports:
            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append(f'{ASM_OUT_PH}"global {item["mangled"]}" << std::endl;')
            elif CDATA.BackEnd.current == BACKEND_NASM:
                out.append(f'global {item["mangled"]}')

        if out:
            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append('{ASM_OUT_PH}std::endl;')
            elif CDATA.BackEnd.current == BACKEND_NASM:
                out.append(NL)

        return "\n".join(out)
    
    def render_asm_double_replacements(self):
        out = []
        for name, value in self.double_literals:
            out.append(
                f'replace_all(asm_text, std::to_string(_double_to_bits({value})), "{name}");'
            )
        return "\n    ".join(out)
        
    def render_asm_string_replacements(self):
        out = []
        for name, text in self.string_literals:
            out.append(
                f'replace_all(asm_text, std::to_string((uint64_t)&{name}), "_{name}");'
            )
        return "\n    ".join(out)
    
    def render_string_literals(self):
        out = []

        for name, text in self.string_literals:
            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append(f'static const char {name}[] = "{self.cpp_escape(text)}";')
            elif CDATA.BackEnd.current == BACKEND_NASM:
                out.append(f'{name}: db "{self.cpp_escape(text)}", 0')

        return "\n".join(out)
    
    def render_asm_double_symbols(self):
        out = []
        for name, value in self.double_literals:
            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append(f'{ASM_OUT_PH}"{name} equ " << std::to_string(_double_to_bits({value})) << " ; {value}" << std::endl;')
            elif CDATA.BackEnd.current == BACKEND_NASM:
                out.append(f'{name} equ {value}' + NL)
        return "\n    ".join(out)
    
    def render_asm_nasm_header(self):
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            return (
                f'{ASM_OUT_PH}std::endl << "; {COMMENT_REPL}"' + NL +
                f'{ASM_OUT_PH}std::endl << "; GENERATED WITH PYTHON 3.14 ON: {dt.now().strftime("%Y-%m-%d")}"' + NL +
                f'{ASM_OUT_PH}std::endl << "; Copyright (c) 2026 by Jens Kallup - paule32"' + NL +
                f'{ASM_OUT_PH}std::endl << "; all rights reserved."' + NL +
                f'{ASM_OUT_PH}std::endl << "; {COMMENT_REPL}"'  + NL + NL +
                f'')
        elif CDATA.BackEnd.current == BACKEND_NASM:
            return ""
    
    def render_asm_nasm_structs(self):
        result = ""
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            result = (
                f'{ASM_OUT_PH}"struc JitContext\n";'                         + NL +
                f'{ASM_OUT_PH}"    .int_vars:         resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .double_vars:      resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .string_vars:      resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .record_vars:      resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .arrays_vars:      resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .pointr_vars:      resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .print_int_tmp:    resd 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .print_double_tmp: resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"endstruc" << std::endl << std::endl;'         + NL +
                f'')
        elif CDATA.BackEnd.current == BACKEND_NASM:
            result = (
                f'struc JitContext'            + NL +
                f'  .int_vars:         resq 1' + NL +
                f'  .double_vars:      resq 1' + NL +
                f'  .string_vars:      resq 1' + NL +
                f'  .record_vars:      resq 1' + NL +
                f'  .arrays_vars:      resq 1' + NL +
                f'  .pointr_vars:      resq 1' + NL +
                f'  .print_int_tmp:    resd 1' + NL +
                f'  .print_double_tmp: resq 1' + NL +
                f'endstruc'                    + NL +
                f''
            )
        return result

    def render_asm_context_data(self,
        int_count,
        double_count,
        string_count,
        record_count,
        arrays_count,
        pointr_count):
        
        std_end = " << std::endl"
        result  = ""
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            result = [
                f'{ASM_OUT_PH}std::endl << "section .data"{std_end};',
                f'{ASM_OUT_PH}"ctx:"{std_end};',
                f'{ASM_OUT_PH}"    istruc JitContext"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.int_vars,         dq int_vars"   {std_end};',
                f'{ASM_OUT_PH}"        at JitContext.double_vars,      dq double_vars"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.string_vars,      dq string_vars"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.record_vars,      dq record_vars"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.arrays_vars,      dq arrays_vars"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.pointr_vars,      dq pointr_vars"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.print_int_tmp,    dd 0"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.print_double_tmp, dq 0"{std_end};',
                f'{ASM_OUT_PH}"    iend"{std_end};',
                f'{ASM_OUT_PH}std::endl;',
                f'{ASM_OUT_PH}"int_vars:    times {int_count} dd 0" {std_end};',
                f'{ASM_OUT_PH}"double_vars: times {double_count} dq 0"{std_end};',
                f'{ASM_OUT_PH}"string_vars: times {string_count} dq 0"{std_end};',
                f'{ASM_OUT_PH}"record_vars: times {record_count} db 0"{std_end};',
                f'{ASM_OUT_PH}"arrays_vars: times {arrays_count} db 0"{std_end};',
                f'{ASM_OUT_PH}"pointr_vars: times {pointr_count} dq 0"{std_end};',
                f'{ASM_OUT_PH}std::endl;',
                f'']
            result = NL.join(result) + NL
            return result
        elif CDATA.BackEnd.current == BACKEND_NASM:
            result = [
                f"section .data",
                f"ctx:",
                f"istruc JitContext",
                f"  at JitContext.int_vars,         dq int_vars",
                f"  at JitContext.double_vars,      dq double_vars",
                f"  at JitContext.string_vars,      dq string_vars",
                f"  at JitContext.record_vars,      dq record_vars",
                f"  at JitContext.arrays_vars,      dq arrays_vars",
                f"  at JitContext.pointr_vars,      dq pointr_vars",
                f"  at JitContext.print_int_tmp,    dd 0",
                f"  at JitContext.print_double_tmp, dq 0",
                f"iend",
                f"",
                f"",
                f"int_vars:    times {int_count} dd 0",
                f"double_vars: times {double_count} dq 0",
                f"string_vars: times {string_count} dq 0",
                f"record_vars: times {record_count} db 0",
                f"arrays_vars: times {arrays_count} db 0",
                f"pointr_vars: times {pointr_count} dq 0",
                f""]
            result = NL.join(result) + NL
            return result
        else:
            return "<unknown backend>"

    def render_asm_context_replacements(self):
        result = ""
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            result = (
                r'replace_all(asm_text, "[r12]",     "[r12 + JitContext.int_vars]"        );' + NL +
                r'replace_all(asm_text, "[r12+8]",   "[r12 + JitContext.double_vars]"     );' + NL +
                r'replace_all(asm_text, "[r12+16]",  "[r12 + JitContext.string_vars]"     );' + NL +
                r'replace_all(asm_text, "[r12+24]",  "[r12 + JitContext.record_vars]"     );' + NL +
                r'replace_all(asm_text, "[r12+32]",  "[r12 + JitContext.arrays_vars]"     );' + NL +
                r'replace_all(asm_text, "[r12+40]",  "[r12 + JitContext.pointr_vars]"     );' + NL +
                r'replace_all(asm_text, "[r12+48]",  "[r12 + JitContext.print_int_tmp]"   );' + NL +
                r'replace_all(asm_text, "[r12+56]",  "[r12 + JitContext.print_double_tmp]");' + NL +
                r""
            )
        elif CDATA.BackEnd.current == BACKEND_NASM:
            result = ""
        return result
    
    def render_asm_extern_symbols(self):
        out = []

        if not self.emit_local_string_data:
            for name, text in self.string_literals:
                if CDATA.BackEnd.current == BACKEND_ASMJIT:
                    out.append(f'{ASM_OUT_PH}"extern _{name}"; << std::endl')
                elif CDATA.BackEnd.current == BACKEND_NASM:
                    out.append(f'extern _{name}')

            if self.string_literals:
                if CDATA.BackEnd.current == BACKEND_ASMJIT:
                    out.append(f'{ASM_OUT_PH}std::endl;')
                elif CDATA.BackEnd.current == BACKEND_NASM:
                    out.append(NL)

        func_list = [
            "print_text",
            "print_int",
            "print_double",
            "print_newline",
            "",
            "new_memory",
            "dispose_memory",
            "",
            "dynarray_setlength",
            "",
            "dynstring_from_cstr",
            "dynstring_setlength",
            "dynstring_length",
            "dynstring_concat",
            "dynstring_copy",
            "dynstring_pos",
            "",
            "set_exception",
            "runtime_error",
            "",
            "error_nil_pointer",
            "error_out_of_memory",
            "error_array_bounds",
            "error_string_range",
            "",
            "debug_break",
            "",
            "ExitProcess"
        ]
        for fun in func_list:
            if len(fun) > 1:
                if CDATA.BackEnd.current == BACKEND_ASMJIT:
                    out.append(f'{ASM_OUT_PH}"extern _jit_{fun}" << std::endl;')
                    continue
                elif CDATA.BackEnd.current == BACKEND_NASM:
                    out.append(f'extern _jit_{fun}')
                    continue
            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append('{ASM_OUT_PH}std::endl;')

        return NL.join(out) + NL
    
    def render_asm_symbol_mappings(self):
        out = []

        for name, text in self.string_literals:
            out.append(
                f'symbols.add(std::to_string((uint64_t)&{name}), "_{name}");'
            )
        out.append("")
        out.append(f'_jit_symbols_add(symbols);')

        return "\n    ".join(out)
        
    def render_asm_string_data(self):
        if not self.emit_local_string_data:
            return ""

        out = []
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            out.append('{ASM_OUT_PH}std::endl << "section .data" << std::endl;')
        elif CDATA.BackEnd.current == BACKEND_NASM:
            out.append('section .data' + NL)

        for name, text in self.string_literals:
            escaped = self.cpp_escape(text)
            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append(f'{ASM_OUT_PH}"_{name} db \\"{escaped}\\", 0" << std::endl;')
            elif CDATA.BackEnd.current == BACKEND_NASM:
                out.append(f'_{name} db \"{escaped}\", 0' + NL)
        
        return "\n    ".join(out)
    
    def render_asm_label_mappings(self):
        out = []
        for item in self.asm_label_mappings:
            out.append(f'labels.add("{item["asmjit"]}", "{item["target"]}");')
        return "\n    ".join(out)
        
    def render_cpp(self):
        body            = "\n".join(self.lines)
        
        var_count       = max(257, self.next_slot)
        int_count       = max(  1, self.next_int_slot)
        
        double_count    = max(  1, self.next_double_slot)
        string_count    = max(  1, self.next_string_slot)
        record_count    = max(  1, self.next_record_slot)
        arrays_count    = max(  1, self.next_arrays_slot)
        pointr_count    = max(  1, self.next_pointr_slot)
        
        # todo !!!
        self.func_name  = "main"
        self.date_str   = dt.now().strftime("%Y-%m-%d")
        
        module_kind     = self.module_kind_value
        
        src_comment     = ('-' * 77)
        src_linecom     = ""
        
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            src_linecom = "//"
        else:
            src_linecom = ";"
        
        output_header   = (
            f"{src_linecom} {src_comment}"                                                    + NL +
            f"{src_linecom} AUTOMATIC GENERATED WITH Python 3.14 SCRIPT ON: {self.date_str}"  + NL +
            f"{src_linecom}"                                                                  + NL +
            f"{src_linecom} DON'T MODIFIED THIS CODE. ALL CHANGES WILL BE LOST BY NEXT RUN !" + NL +
            f"{src_linecom} Copyright (c) 2026 by Jens Kallup - paule32"                      + NL +
            f"{src_linecom} all rights reserved."                                             + NL +
            f"{src_linecom} {src_comment}"                                                    + NL +
            f""
        )
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            result = [
                output_header,
                '# include "runtime/dbase2many.hpp"',
                '',
                'using namespace std;' ,
                'using namespace asmjit;' ,
                '' ,
                f'static constexpr int DBASE2MANY_MODULE_KIND = {self.module_kind_value};',
                '' ,
                f'{self.render_string_literals()}' ,
                '' ,
                'int main() {{' ,
                '  JitRuntime rt;',
                '',
                '   CodeHolder code;',
                '  code.init(rt.environment());',
                '',
                '  StringLogger logger;',
                '',
                '  logger.options().set_indentation(FormatIndentationGroup::kCode, 1);',
                '  logger.options().set_padding(FormatPaddingGroup::kMachineCode, 0);',
                '',
                '  code.set_logger(&logger);',
                '  x86::Assembler a(&code);',
                '',
                f'{body}',
                '  a.add(x86::rsp, 8); // undo alignment',
                '  a.pop(x86::rbx);',
                '  a.pop(x86::r12);',
                '',
                '  a.xor_(x86::ecx, x86::ecx);',
                '  a.sub(x86::rsp, 32);',
                '  a.mov(x86::rax, imm((uint64_t)&_jit_ExitProcess));',
                '  a.call(x86::rax);',
                '  a.ret();        // never reach',
                '',
                '  JitFunc fn = nullptr;',
                '  Error err = rt.add(&fn, &code);',
                '  if (err != Error::kOk) {{',
                '      std::cerr << \"AsmJit error: \" << DebugUtils::error_as_string(err) << std::endl;',
                '      return 1;',
                '  }}',
                '',
                '  std::ostringstream asm_out;',
                '  std::string asm_text = logger.data();',
                '',
                '  replace_all_fun(asm_text);',
                '',
                '  SymbolMappings symbols;',
                f'  {self.render_asm_symbol_mappings()}',
                '  symbols.apply(asm_text);',
                '',
                '  LabelMappings labels;',
                f'  {self.render_asm_label_mappings()}',
                '  labels.apply(asm_text);',
                '',
                '  replace_all_ptr(asm_text);',
                '  replace_all(asm_text, "mov r12, rcx", "lea r12, [rel ctx]");',
                '',
                f'  {self.render_asm_context_replacements()}',
                '',
                f'  {self.render_asm_nasm_header()}',
                f'  {self.render_asm_nasm_structs()}',
                '',
                f'  {self.render_asm_double_replacements()}',
                f'  {ASM_OUT_PH}std::endl;',
                f'  {ASM_OUT_PH}std::endl;',
                '',
                f'  {self.render_asm_double_symbols()}',
                f'  {self.render_asm_extern_symbols()}',
                '',
                f'  {self.render_asm_context_data(
                        int_count,
                        double_count,
                        string_count,
                        record_count,
                        arrays_count,
                        pointr_count)}',
                f'',
                f'    {ASM_OUT_PH}std::endl;',
                f'    {ASM_OUT_PH}"dbase2many_module_kind dq {self.module_kind_value}" << std::endl;',
                f'    {ASM_OUT_PH}"dbase2many_module_kind_program  equ 1" << std::endl;',
                f'    {ASM_OUT_PH}"dbase2many_module_kind_unit     equ 2" << std::endl;',
                f'    {ASM_OUT_PH}"dbase2many_module_kind_library  equ 3" << std::endl << std::endl;',
                f'',
                f'    {ASM_OUT_PH}std::endl;',
                f'    {ASM_OUT_PH}"section .text" << std::endl;',
                f'    {ASM_OUT_PH}"global " << "_{self.func_name}" << std::endl;',
                f'    {self.render_asm_exports()}',
                f'    {ASM_OUT_PH}"_{self.func_name}" << ":" << std::endl;',
                f'',
                f'    asm_out << asm_text;',
                f'',
                f'    {self.render_asm_export_thunks()}',
                f'    {self.render_asm_string_data()}',
                f'',
                f'    std::string final_asm_text = asm_out.str();',
                f'',
                f'    if (!write_formatted_asm_file(',
                f'        final_asm_text.c_str(),',
                f'        \"{self.asm_file}\")) {{',
                f'        std::cerr << "Could not write ASM file: {self.asm_file}" << std::endl;',
                f'    }}',
                f'',
                f'    std::array<int,      {int_count}> int_vars{{}};',
                f'    std::array<double,   {double_count}> double_vars{{}};',
                f'    std::array<char*,    {string_count}> string_vars{{}};',
                f'    std::array<uint8_t,  {record_count}> record_vars{{}};',
                f'    std::array<uint8_t,  {arrays_count}> arrays_vars{{}};',
                f'    std::array<uint64_t, {pointr_count}> pointr_vars{{}};',
                '',
                '    JitContext ctx{};',
                '    ctx.int_vars    = int_vars.data();',
                '',
                '    ctx.double_vars = double_vars.data();',
                '    ctx.string_vars = string_vars.data();',
                '    ctx.record_vars = record_vars.data();',
                '    ctx.arrays_vars = arrays_vars.data();',
                '    ctx.pointr_vars = pointr_vars.data();',
                '',
                '    try {',
                '        fn(&ctx);',
                '    }',
                '    catch (const JitRuntimeError& e) {',
                '        std::cerr << "JIT runtime error: " << e.what() << std::endl;',
                '        rt.release(fn);',
                '        return 2;',
                '    }',
                '    catch (const std::exception& e) {',
                '        std::cerr << "C++ exception: " << e.what() << std::endl;',
                '        rt.release(fn);',
                '        return 3;',
                '    }',
                '    catch (...) {',
                '        std::cerr << "Unknown JIT exception" << std::endl;',
                '        rt.release(fn);',
                '        return 4;',
                '   }',
                '',
                '    rt.release(fn);',
                '    return 0;',
                '}',
                '']
            result = NL.join(result) + NL
            return result
        elif CDATA.BackEnd.current == BACKEND_NASM:
            result = [
                output_header,
                f'section .text',
                f'{self.render_asm_exports()}',
                f'{self.render_asm_export_thunks()}',
                #f'{self.render_asm_string_data()}',
                f'',
                f'section .text',
                f'global _{self.func_name}',
                f'_{self.func_name}:',
                f'{body}',
                '  add rsp, 8  ; undo alignment',
                '  pop rbx',
                '  pop r12',
                '',
                '  xor ecx, ecx',
                '  sub rsp, 32',
                '  lea rax, [rel _jit_ExitProcess]',
                '  call rax',
                '  ret      ; never reach',
                '',
                f'{self.render_asm_nasm_structs()}',
                f'{self.render_asm_context_data(
                    int_count,
                    double_count,
                    string_count,
                    record_count,
                    arrays_count,
                    pointr_count)}',
                f'',
                f'{self.render_string_literals()}' ,
                f'',
                f'{self.render_asm_double_symbols()}',
                f'{self.render_asm_extern_symbols()}',
                f''
                f'DBASE2MANY_MODULE_KIND: db {self.module_kind_value}'
            ]            
            result = NL.join(result) + NL
            return result
        else:
            return "<unknown backend>"
        
    def render_variable_output(self):
        out = []
        
        for key, info in sorted(self.vars.items(), key=lambda x: x[1]["slot"]):
            name = info["name"]
            typ  = info["type"]
            slot = info["slot"]
            
            if typ == "integer":
                out.append(
                    f'    std::cout << "{name} = " << int_vars[{slot}] << std::endl;'
                )
            elif typ == "double":
                out.append(
                    f'    std::cout << "{name} = " << double_vars[{slot}] << std::endl;'
                )
        
        return "\\n".join(out)
        
    def render_print_output(self):
        return "\n".join(self.cpp_print_lines)

# ---------------------------------------------------------------------------
# generator class
# ---------------------------------------------------------------------------
class PascalGenerator(AsmJitGenerator):
    def __init__(self, backend, writer=None):
        super().__init__(backend)
        self.writer = writer
        self.coff   = None

        self.pending_open_array_actual = None
        self.next_open_array_literal_id = 0

        if writer is None:
            raise RuntimeError("generator writer invalid")

        # EXE-Writer bekommen: echten COFF-Writer herausziehen
        if isinstance(writer, NT32Writer):
            self.coff = writer.coff
            self.writer = writer.coff

        elif isinstance(writer, PE64Writer):
            self.coff = writer.coff
            self.writer = writer.coff

        elif isinstance(writer, (PE32Writer, PE64CoffWriter)):
            self.coff = writer

        else:
            raise RuntimeError(f"unsupported generator writer: {type(writer)}")

    def emit_mov_eax_ebx(self):
        """
        Kopiert den berechneten linearen Array-Index aus EBX nach EAX.

        Im COFF32-/PE32-Modus besitzt der Generator keine NASM-Textliste
        namens self.asm. Die Instruktion wird ausschließlich über den
        aktiven Backend-Emitter ausgegeben.
        """
        self.emit_mov(
            "eax",
            "ebx",
            comment="copy linear array index to eax"
        )

    def emit_mov_ebx_eax(self):
        self.emit_mov("ebx", "eax")

    def collect_array_suffix_exprs(self, suffixes):
        index_exprs = []
        rest_suffixes = []

        in_array_part = True

        for s in suffixes:
            if in_array_part and self.suffix_is_index(s):
                index_exprs.extend(
                    self.suffix_index_exprs(s)
                )
                continue

            in_array_part = False
            rest_suffixes.append(s)

        return index_exprs, rest_suffixes

    def write_string_literals_to_coff(self):
        for label, text in self.string_literals:
            if self.writer.find_symbol_index(label) is None:
                self.writer.add_data_string(label, text)

    def write_double_literals_to_coff(self):
        for name, value in self.double_literals:
            self.writer.add_data_double(name, float(value))

    def visitProgramFile(self, ctx):
        self.program_name = ctx.IDENT().getText()
        self.module_kind = "program"
        self.module_kind_value = 1

        target = CDATA.args_target.lower()

        # GeneratorClass arbeitet bei Windows-Zielen bereits direkt mit dem
        # COFF-Writer. Die Erzeugung von _main darf deshalb nicht von
        # CDATA.args_backend == BACKEND_EXEFILE/BACKEND_OBJFILE abhängen.
        is_windows_coff = target in [
            "nt35",
            "winnt",
            "win32",
            "win64"
        ]

        is_dos_file = (
            target in ["dos", "dos16"]
            and CDATA.args_backend in [
                BACKEND_OBJFILE,
                BACKEND_EXEFILE
            ]
        )

        dos_main_label = None

        if is_dos_file:
            dos_main_label = "__dos_main_start"
            self.writer.emit_jmp(dos_main_label)

        if ctx.usesClause():
            self.visit(ctx.usesClause())

        for decl in ctx.declarationPart():
            if decl is not None:
                self.visit(decl)

        self.validate_class_methods(ctx)

        # ------------------------------------------------------------
        # Windows COFF program entry: _main
        # ------------------------------------------------------------
        if is_windows_coff:
            self.finalize_coff_context()
            self.writer.begin_function(
                "_main",
                local_size=0
            )

            if target in ["nt35", "winnt", "win32"]:
                # NT32: ESI hält den JIT-Kontext.
                self.writer.emit_lea_reg_data_label(
                    "esi",
                    "ctx"
                )

                # Programmargumente werden absichtlich NICHT hier
                # initialisiert. ParamCount und ParamStr initialisieren
                # die Runtime bei Bedarf selbst. Dadurch können Programme,
                # die keine Kommandozeilenparameter verwenden, bereits vor
                # der ersten Ausgabe nicht an der Argument-Runtime scheitern.
            else:
                # Win64
                self.emit_push("r12")
                self.emit_push("rbx")
                self.emit_sub("rsp", 8)

                self.writer.emit_lea_reg_data_label(
                    "r12",
                    "ctx"
                )

        # ------------------------------------------------------------
        # DOS program entry
        # ------------------------------------------------------------
        elif is_dos_file:
            self.writer.bind_label(dos_main_label)
            self.writer.emit_startup()
            self.backend.emit_heap_init(0x40)

        # Unit-Initialisierungen müssen innerhalb von _main liegen.
        self.emit_unit_initializers()

        for name, info in self.vars.items():
            if info["type"] in self.arrays:
                self.emit_init_array_var(
                    ctx,
                    name,
                    info
                )

        self.visit(ctx.block())

        # ------------------------------------------------------------
        # Windows program exit
        # ------------------------------------------------------------
        if is_windows_coff:
            if target in ["nt35", "winnt", "win32"]:
                self.writer.emit_push_imm32(0)
                self.writer.emit_call_external(
                    "ExitProcess"
                )
                self.writer.end_function()

            elif target == "win64":
                self.emit_mov("ecx", 0)
                self.writer.emit_runtime_call(
                    "ExitProcess"
                )
                self.writer.end_function()

        # ------------------------------------------------------------
        # DOS program exit
        # ------------------------------------------------------------
        elif is_dos_file:
            self.writer.emit_exit(0)

        return None

    def finalize_coff_context(self):
        if getattr(self, "coff_context_done", False):
            return
        
        target = CDATA.args_target.lower()
        
        if target in ["winnt", "nt35", "win32"]:
            self.writer.add_jit_context32("ctx")
            self.coff_context_done = True
            return
        
        self.writer.add_jit_context(
            int_count     = max(1, self.next_int_slot),
            double_count  = max(1, self.next_double_slot),
            string_count  = max(1, self.next_string_slot),
            record_bytes  = max(8, self.next_record_slot),
            arrays_bytes  = max(8, self.next_arrays_slot),
            pointer_count = max(1, self.next_pointr_slot)
        )
        self.coff_context_done = True
        
    def coff_main(self):
        if getattr(self, "coff_main_done", False):
            return
        
        self.finalize_coff_context()
        
        self.coff.begin_function("_main", local_size = 0)
        self.coff.emit_lea_reg_data_label("r12", "ctx")
        self.coff.emit_lea_rcx_data_label("str_0")
        self.coff.emit_runtime_call("_jit_print_text")
        self.coff.emit_mov_reg_imm32("ecx", 123)
        self.coff.emit_runtime_call("_jit_print_int")
        self.coff.end_function()
        
        self.coff_main_done = True
        
    def write_main(self, obj_file, exe_file):
        if self.coff.find_symbol_index("str_0") is None:
            self.coff.add_data_string("str_0", "Hallo aus COFF")
            
        self.coff_main()
        self.coff.write(obj_file)
        
        pe = PE64Writer(self.coff)
        pe.emit_ret()
        pe.write(exe_file)
