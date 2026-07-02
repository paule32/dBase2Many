# ---------------------------------------------------------------------------
# File: generator.py - Pascal Transpiler
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

import os
import sys

from dataclasses import dataclass, field
from antlr4      import *

from compiler.frontend.pascal.preprocessor   import PascalPreprocessor

from parsers.pascal.MiniPascalLexer          import MiniPascalLexer
from parsers.pascal.MiniPascalParser         import MiniPascalParser
from parsers.pascal.MiniPascalParserVisitor  import MiniPascalParserVisitor

from compiler.common.error     import *
from compiler.common.types     import *
from compiler.common.constants import *

from compiler.writer.nt32 import *
from compiler.writer.pe32 import *
from compiler.writer.pe64 import *

from compiler.writer.pe64coff  import *

class PropertyInfo:
    def __init__(self, name, ptype, visibility, read_name=None, write_name=None):
        self.name       = name
        self.ptype      = ptype
        self.visibility = visibility
        self.read_name  = read_name
        self.write_name = write_name

# ---------------------------------------------------------------------------
# the transpiler generator for Pascal->Assembly
# ---------------------------------------------------------------------------
class AsmJitGenerator(MiniPascalParserVisitor):
    def __init__(self, backend=None):
        self.backend = backend or AsmJitBackend()   # default backend
        self.lines   = self.backend.lines
        
        self.vars               = {}
        self.next_slot          = 0
        self.program_name       = "Program"
        self.var_types          = {}
        self.cpp_print_lines    = []
        
        self.source_file       = None
        self.source_dir        = None
        
        self.loaded_units      = {}
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
        
        self.section_text = []
        self.section_data = []
        
        self.constants["true"] = {
            "name": "True",
            "type": "integer",
            "value": 1
        }

        self.constants["false"] = {
            "name": "False",
            "type": "integer",
            "value": 0
        }

        self.asm_file               = CDATA.asm_file
        self.emit_local_string_data = True
        
        self.module_kind        = "program"
        self.module_kind_value  = 1
        
        self.exports = []
    
    def format_error(self, filename, err):
        template = ERROR_MAP.get(err.code, err.code)
        message  = template.format(**err.params)
        
        return f"{err.code}: {os.path.basename(filename)} {err.line}:{err.column} {message}"

    def find_unit_file(self, ctx, unit_name):
        print("----> ", unit_name)
        candidates = [
            unit_name + ".pas",
            unit_name + ".pp",
            unit_name.lower() + ".pas",
            unit_name.lower() + ".pp"
        ]

        search_dirs = []

        if self.source_dir:
            search_dirs.append(self.source_dir)

        search_dirs.append(os.getcwd())

        for p in getattr(CDATA, "IncludePaths", []):
            search_dirs.append(os.path.abspath(p))

        for item in getattr(CDATA, "UnitFiles", []):
            item_path = os.path.abspath(item)

            if os.path.isfile(item_path):
                base = os.path.splitext(os.path.basename(item_path))[0].lower()

                if base == unit_name.lower():
                    return item_path

            elif os.path.isdir(item_path):
                search_dirs.append(item_path)

        seen = set()
        for directory in search_dirs:
            directory = os.path.abspath(directory)

            if directory in seen:
                continue
            seen.add(directory)

            for filename in candidates:
                path = os.path.abspath(os.path.join(directory, filename))

                if os.path.exists(path):
                    return path

        raise CompileError(
            ctx,
            "E0019",
            text=f"unit {unit_name} not found"
        )
    
    def format_method_signature(self, params):
        if not params:
            return "()"
            
        types = []
        
        for p in params:
            types.append(self.resolve_type(p["type"]))
            
        return "(" + ", ".join(types) + ")"
    
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
    
    def method_signature(self, params):
        return tuple(self.resolve_type(p["type"]) for p in params)
    
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
        typ = self.resolve_type(typ)
        
        if isinstance(typ, dict):
            if typ.get("kind") == "array":
                return typ["size"]
        
        if isinstance(typ, str) and typ in self.classes:
            return typ
        
        if isinstance(typ, str) and typ.startswith("^"):
            return 8
        
        if typ == "integer":
            return 4
            
        if typ == "double":
            return 8
            
        if typ == "string":
            return 8

        if isinstance(typ, str) and typ in self.records:
            return self.records[typ].size
        
        if isinstance(typ, str) and typ in self.arrays:
            return self.arrays[typ].size

        raise CompileError(ctx, "E0004", name=typ)

    def actual_param_variable_ref(self, ctx, arg):
        expr = arg.expr()

        if expr is None:
            raise CompileError(ctx, "E0005", got="empty", expected="pointer variable")

        refs = []

        def walk(node):
            if node is None:
                return

            if isinstance(node, MiniPascalParser.VariableRefContext):
                refs.append(node)
                return

            if hasattr(node, "children") and node.children:
                for child in node.children:
                    walk(child)

        walk(expr)

        if len(refs) != 1:
            raise CompileError(ctx, "E0005", got=expr.getText(), expected="single variable")

        if refs[0].getText() != expr.getText():
            raise CompileError(ctx, "E0005", got=expr.getText(), expected="single variable")

        return refs[0]
    
    def declare_record(self, ctx, name, fields):
        key = name.lower()

        if key in self.records:
            raise CompileError(ctx, "E0002", name=name)

        offset = 0
        record_fields = {}

        for field_name, field_type in fields:
            field_key = field_name.lower()
            resolved_type = self.resolve_type(field_type)
            size = self.type_size(ctx, resolved_type)

            record_fields[field_key] = RecordFieldInfo(
                name    = field_name,
                type    = resolved_type,
                offset  = offset,
                size    = size
            )

            offset += size

        self.records[key] = RecordInfo(
            name    = name,
            fields  = record_fields,
            size    = offset
        )
    
    def declare_class(self, ctx, name, fields, methods, properties=None, parent_name=None):
        key = name.lower()
        
        if properties is None:
            properties  = {}
            
        parent_key      = None
        parent_size     = 0
        parent_fields   = {}
        parent_methods  = {}
        
        if parent_name:
            parent_key = parent_name.lower()

            if parent_key not in self.classes:
                raise CompileError(ctx, "E0004", name=parent_name)

            parent_cls    = self.classes[parent_key]
            parent_size   = parent_cls.size

            parent_fields = dict(parent_cls.fields)

            for mname, overloads in parent_cls.methods.items():
                parent_methods[mname] = list(overloads)
        
        if key in self.classes:
            raise CompileError(ctx, "E0002", name=name)
        
        offset = parent_size
        class_fields = dict(parent_fields)
        
        for field_name, field_type, visibility in fields:
            field_key = field_name.lower()
            resolved_type = self.resolve_type(field_type)
            size = self.type_size(ctx, resolved_type)
            
            class_fields[field_key] = RecordFieldInfo(
                name        = field_name,
                type        = resolved_type,
                offset      = offset,
                size        = size,
                visibility  = visibility
            )
            
            offset += size
        
        class_methods = dict(parent_methods)
        
        for method in methods:
            method_key = method["name"].lower()
            
            info = ClassMethodInfo(
                name        = method["name"],
                kind        = method["kind"],
                label       = method["label"],
                params      = method.get("params", []),
                owner       = key,
                return_type = method.get("return_type", None),
                implemented = False,
                mangled     = method.get("mangled", None),
                visibility  = method.get("visibility", "public")
            )
            
            class_methods.setdefault(method_key, [])
            sig = self.method_signature(info.params)
            
            # gleiche Signatur aus Parent-Klasse entfernen:
            # Kindklasse überschreibt diese Methode
            class_methods[method_key] = [
                old for old in class_methods[method_key]
                if self.method_signature(old.params) != sig
            ]
            
            class_methods[method_key].append(info)
        
        has_create  = "create"  in class_methods
        has_destroy = "destroy" in class_methods
        
        if not has_create:
            raise CompileError(
                ctx,
                "E0019",
                text = f"class {name} requires constructor Create"
            )
        
        if not has_destroy:
            raise CompileError(
                ctx,
                "E0019",
                text = f"class {name} requires destructor Destroy"
            )
        
        if "create" not in class_methods:
            raise CompileError(ctx, "E0019", text = f"class {name} requires constructor Create")
        
        if "destroy" not in class_methods:
            raise CompileError(ctx, "E0019", text = f"class {name} requires destructor Destroy")
        
        class_properties = dict(properties)

        if parent_name:
            parent_properties = getattr(parent_cls, "properties", {})
            class_properties = dict(parent_properties)
            class_properties.update(properties)
        
        print("DECLARE CLASS:", name, "size=", offset)
        print("FIELDS:", list(class_fields.keys()))

        self.classes[key] = ClassInfo(
            name       = name,
            fields     = class_fields,
            methods    = class_methods,
            properties = class_properties,
            size       = offset,
            parent     = parent_key
        )
    
    def validate_class_methods(self, ctx):
        for class_key, cls in self.classes.items():
            for method_name, overloads in cls.methods.items():
                for method in overloads:
                    
                    # geerbte Methode gehört nicht zu dieser Klasse
                    if method.owner != class_key:
                        continue
                    
                    if not method.implemented:
                        raise CompileError(
                            ctx,
                            "E0019",
                            text = (
                                f"{tr('class')} {cls.name} {tr('method')} "
                                f"{method.name}{self.format_method_signature(method.params)} "
                                f"{tr('is declared but not implemented')}"
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

        resolved_type = self.resolve_type(element_type)

        if resolved_type == "integer":
            element_size = 4

        elif resolved_type == "double":
            element_size = 8

        elif resolved_type == "string":
            element_size = self.pointer_slot_size()

        elif isinstance(resolved_type, str) and resolved_type.startswith("^"):
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
        typ = self.resolve_type(vtype)
        
        if key in scope["vars"]:
            raise CompileError(ctx, "E0002", name=name)
        
        if typ == "integer":
            size = 8
        
        elif typ == "double":
            size = 8
        
        elif typ == "string":
            if CDATA.args_target in ["dos", "dos16"]:
                size = 4      # DOS Far Pointer: offset + segment
            else:
                size = 8
        
        elif isinstance(typ, str) and typ.startswith("^"):
            size = 8
        
        elif isinstance(typ, str) and typ in self.records:
            size = self.records[typ].size
        
        elif isinstance(typ, str) and typ in self.arrays:
            array_info = self.arrays[typ]

            if getattr(array_info, "is_dynamic", False):
                slot = self.next_pointr_slot
                self.next_pointr_slot += 1
            else:
                slot = self.next_arrays_slot
                self.next_arrays_slot += array_info.size
        
        elif isinstance(typ, str) and typ in self.enums:
            typ = "integer"
            size = 8
        
        else:
            raise CompileError(
                ctx,
                "E0005",
                got=typ,
                expected="integer/double/string/pointer/record/array/enum"
            )
        
        scope["next_offset"] += size
        offset = -scope["next_offset"]
        
        scope["vars"][key] = {
            "name": name,
            "type": typ,
            "offset": offset,
            "size": size
        }
    
    def declare_var(self, ctx, name, vtype):
        key = name.lower()
        typ = self.resolve_type(vtype)
        
        if key in self.vars:
            raise CompileError(ctx, "E0002", name=name)
        
        symbol = None
        
        use_direct_coff_globals = (
            hasattr(self, "coff")
            and self.backend.name == CDATA.args_backend
        )
        
        if typ == "integer":
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
            
            if use_direct_coff_globals:
                symbol = f"_var_{name}"
                self.coff.add_data_double(symbol)
        
        elif typ == "string":
            slot = self.next_string_slot
            self.next_string_slot += 1
            
            if use_direct_coff_globals:
                symbol = f"_var_{name}"
                self.coff.add_data_qword(symbol)
        
        elif isinstance(typ, str) and typ in self.records:
            slot = self.next_record_slot
            self.next_record_slot += self.records[typ].size
        
        elif isinstance(typ, str) and typ in self.arrays:
            array_info = self.arrays[typ]
            
            if getattr(array_info, "is_dynamic", False):
                slot = self.next_pointr_slot
                self.next_pointr_slot += 1
            else:
                slot = self.next_arrays_slot
                self.next_arrays_slot += array_info.size
        
        elif isinstance(typ, str) and typ in self.classes:
            slot = self.next_pointr_slot
            self.next_pointr_slot += 1
            
            if CDATA.args_target in ["dos", "dos16"]:
                symbol = f"_var_{name}"
                self.backend.writer.add_dword_var(symbol)
            
            if use_direct_coff_globals:
                symbol = f"_var_{name}"
                self.coff.add_data_qword(symbol)
            
        elif isinstance(typ, str) and typ.startswith("^"):
            slot = self.next_pointr_slot
            self.next_pointr_slot += 1
            
            if CDATA.args_target in ["dos", "dos16"]:
                symbol = f"_var_{name}"
                self.backend.writer.add_dword_var(symbol)
                
            elif use_direct_coff_globals:
                symbol = f"_var_{name}"
                self.coff.add_data_qword(symbol)
            
        else:
            raise CompileError(ctx, "E0004", name=vtype)
        
        self.vars[key] = {
            "name": name,
            "type": typ,
            "slot": slot,
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
        var_name = parts[0]
        var_info = self.var_info(ctx, var_name)

        class_type = var_info["type"]

        if class_type not in self.classes:
            raise CompileError(ctx, "E0005", got=class_type, expected="class")

        cls = self.classes[class_type]

        field_name = parts[1].lower()

        if field_name not in cls.fields:
            raise CompileError(ctx, "E0001", name=parts[1])

        return var_info, cls.fields[field_name]
    
    def resolve_record_path(self, ctx, parts):
        var_name = parts[0]
        var_key  = var_name.lower()

        if var_key not in self.vars:
            raise CompileError(ctx, "E0001", name=var_name)

        var_info = self.vars[var_key]
        current_type = var_info["type"]

        if current_type not in self.records:
            raise CompileError(ctx, "E0005", got=current_type, expected="record")

        offset = var_info["slot"]
        field = None

        for field_name in parts[1:]:
            record = self.records[current_type]
            field_key = field_name.lower()

            if field_key not in record.fields:
                raise CompileError(ctx, "E0001", name=".".join(parts))

            field = record.fields[field_key]
            offset += field.offset
            current_type = field.type

            if field_name != parts[-1]:
                if current_type not in self.records:
                    raise CompileError(ctx, "E0005", got=current_type, expected="record")

        return offset, field

    def pascal_import_type(self, typ):
        typ = self.resolve_type(typ)

        if typ == "integer":
            return "Integer"

        if typ == "double":
            return "Double"

        if typ == "string":
            return "AnsiString"

        if isinstance(typ, str) and typ.startswith("^"):
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
    
    def resolve_pointer_record_path(self, ctx, parts):
        ptr_name = parts[0]
        ptr_key  = ptr_name.lower()

        ptr_info = self.find_local_var(ptr_name)
        is_local = ptr_info is not None

        if ptr_info is None:
            if ptr_key not in self.vars:
                raise CompileError(ctx, "E0001", name=ptr_name)

            ptr_info = self.vars[ptr_key]

        ptr_type = self.resolve_type(ptr_info["type"])

        if not isinstance(ptr_type, str) or not ptr_type.startswith("^"):
            raise CompileError(ctx, "E0005", got=ptr_type, expected="pointer")

        record_type = ptr_type[1:]

        if record_type not in self.records:
            raise CompileError(ctx, "E0005", got=record_type, expected="record")

        offset = 0
        field = None
        current_type = record_type

        for field_name in parts[1:]:
            record = self.records[current_type]
            field_key = field_name.lower()

            if field_key not in record.fields:
                raise CompileError(ctx, "E0001", name=".".join(parts))

            field = record.fields[field_key]
            offset += field.offset
            current_type = self.resolve_type(field.type)

            if field_name != parts[-1]:
                if isinstance(current_type, str) and current_type.startswith("^"):
                    current_type = current_type[1:]

                if current_type not in self.records:
                    raise CompileError(ctx, "E0005", got=current_type, expected="record")

        ptr_info = dict(ptr_info)
        ptr_info["is_local"] = is_local
        ptr_info["type"] = ptr_type

        return ptr_info, offset, field
    
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
    
    def resolve_type(self, type_name):
        if not isinstance(type_name, str):
            return type_name

        typ = type_name.lower()

        if typ.startswith("^"):
            base = typ[1:]
            
            while base in self.type_aliases:
                base = self.type_aliases[base].lower()
                
                if base.startswith("^"):
                    return base
                    
            return "^" + base

        while typ in self.type_aliases:
            typ = self.type_aliases[typ].lower()

        if typ == "boolean":
            return "integer"
        
        if typ in self.enums:
            return "integer"

        if isinstance(typ, str) and typ in self.records:
            return typ

        if isinstance(typ, str) and typ in self.arrays:
            return typ

        return typ
    
    def load_unit(self, ctx, unit_name):
        unit_key = unit_name.lower()

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

        with open(unit_file, "r", encoding="utf-8") as f:
            raw_text = f.read()

        pp = PascalPreprocessor(defines=getattr(CDATA, "Defines", []))
        text = pp.process(raw_text)

        self.source_file  = unit_file
        self.source_dir   = os.path.dirname(unit_file)
        self.current_unit = unit_key

        stream = InputStream(text)
        lexer  = MiniPascalLexer(stream)
        tokens = CommonTokenStream(lexer)
        parser = MiniPascalParser(tokens)

        tree = parser.sourceFile()

        if parser.getNumberOfSyntaxErrors() > 0:
            raise CompileError(
                ctx,
                "E0019",
                text=f"syntax error in unit {unit_name}"
            )

        self.visit(tree)

        self.current_unit = old_unit
        self.source_file  = old_source_file
        self.source_dir   = old_source_dir

        self.loading_units.remove(unit_key)
        self.loaded_units[unit_key] = unit_file

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

        if not ctx.formalParamList():
            return params

        for p in ctx.formalParamList().formalParam():
            typ = self.resolve_type(p.typeName().getText())
            is_var = p.VAR() is not None

            for ident in p.identList().IDENT():
                params.append({
                    "name": ident.getText(),
                    "type": typ,
                    "is_var": is_var
                })

        return params
    
    def scoped_name(self, name):
        if self.scope_stack:
            return "_".join(self.scope_stack + [name])
        return name

    def variable_ref_has_caret(self, ref):
        return any(s.CARET() for s in ref.variableSuffix())
    
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

        if isinstance(typ, str) and typ.startswith("^"):
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

                elif isinstance(arg_type, str) and arg_type.startswith("^"):
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
                if isinstance(typ, str) and typ.startswith("^"):
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

            # Constructor-Argumente rechts-nach-links auswerten
            for arg in reversed(args):
                arg_type = self.visit(arg)
                actual_types.insert(0, arg_type)

                if arg_type in ("integer", "char"):
                    self.emit_push("eax", comment="ctor int arg")

                elif arg_type == "string":
                    self.emit_push("eax", comment="ctor string arg")

                elif isinstance(arg_type, str) and arg_type.startswith("^"):
                    self.emit_push("eax", comment="ctor pointer arg")

                else:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=f"unsupported NT32 constructor argument type {arg_type}"
                    )

            method, owner_cls = self.find_class_method_recursive(
                ctx,
                cls,
                method_name,
                actual_types
            )

            size = cls.size
            #size = max(cls.size, self.pointer_slot_size())
            
            print("CTOR ALLOC:", class_name, "size=", size)

            # _jit_new_memory(size)
            self.backend.writer.emit_push_imm32(size)
            #self.emit(f"push {size}")
            
            self.emit_call("_jit_new_memory")
            self.backend.emit_cleanup_stack(4)
            #self.emit("add esp, 4")

            # Runtime-Call kann ESI zerstören
            self.writer.emit_lea_reg_data_label("esi", "ctx")

            # EAX = neues Objekt
            ok_label = self.new_named_label("class_alloc_ok")
            self.emit_test("eax", "eax")
            self.emit_jnz(ok_label)
            self.emit_call("_jit_out_of_memory_error")
            self.emit_bind_label(ok_label)

            # Objekt für Rückgabe sichern
            self.emit_push("eax", comment="save constructor result")

            # Self als erster Parameter
            self.emit_push("eax", comment="Self")

            # Konstruktor aufrufen
            self.emit_call(method.label)

            # Stack bereinigen: Self + Constructor-Argumente
            self.backend.emit_cleanup_stack((len(args) + 1) * 4)

            # Rückgabewert wiederherstellen
            self.emit_pop("eax", comment="constructor result")

            self.writer.emit_lea_reg_data_label("esi", "ctx")

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
                
                elif isinstance(arg_type, str) and arg_type.startswith("^"):
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
            self.emit_call_lbl(method.label)
            self.emit_add("rsp", 32)
            self.emit_pop("rax", comment = "constructor result")
            
            return class_key
    
    def emit_class_free_call(self, ctx, obj_name):
        info = self.var_info(ctx, obj_name)
        class_type = info["type"]

        if CDATA.args_target in ["dos", "dos16"]:
            if class_type not in self.classes:
                raise CompileError(ctx, "E0005", got=class_type, expected="class")

            cls = self.classes[class_type]
            symbol = info.get("symbol")

            if not symbol:
                symbol = f"_var_{info['name']}"
                info["symbol"] = symbol

            null_label = self.new_named_label("free_nil")
            end_label  = self.new_named_label("free_end")

            # AX = Offset, DX = Segment
            self.backend.emit_load_far_pointer_var(symbol)

            # nil?
            self.backend.writer.emit_cmp_reg16_imm16("dx", 0)
            self.backend.writer.emit_je(null_label)

            self.backend.writer.emit_cmp_reg16_imm16("ax", 0)
            self.backend.writer.emit_je(null_label)

            # Destructor mit Self in AX/DX aufrufen
            if "destroy" in cls.methods:
                method, owner_cls = self.find_class_method_recursive(
                    ctx,
                    cls,
                    "Destroy",
                    []
                )

                self.backend.writer.emit_push_reg16("dx")
                self.backend.writer.emit_push_reg16("ax")

                self.backend.writer.emit_call_label(method.label)

                self.backend.writer.emit_pop_reg16("ax")
                self.backend.writer.emit_pop_reg16("dx")

            # Speicher vorerst nicht wirklich freigeben, nur NIL setzen
            self.backend.emit_dispose_pointer_far(symbol)

            self.backend.writer.emit_jmp(end_label)

            self.emit_bind_label(null_label)
            self.emit_bind_label(end_label)

            return None

        if class_type not in self.classes:
            raise CompileError(ctx, "E0005", got=class_type, expected="class")

        cls = self.classes[class_type]

        self.emit_load_object_var(ctx, obj_name, info)

        null_label = self.new_named_label("free_nil")
        end_label  = self.new_named_label("free_end")

        self.emit_test("rax", "rax")
        self.emit_jz(null_label)

        self.emit_push("rax", comment='save object for dispose')

        if "destroy" in cls.methods:
            method, owner_cls = self.find_class_method_recursive(
                ctx,
                class_type,
                "Destroy",
                []
            )
            
            self.emit_mov("rcx", "rax", comment='Self')
            self.emit_sub("rsp", 32)
            self.emit_call_lbl(method.label)
            self.emit_add("rsp", 32)

        self.emit_pop("rcx")
        self.emit_mov_imm("rax", "&_jit_dispose_memory")
        self.emit_call("rax")

        # foo := nil
        self.emit_xor("rax", "rax")
        self.emit_store_object_var(ctx, obj_name, info)

        self.emit_jmp(end_label)
        self.emit_bind_label(null_label)
        self.emit_bind_label(end_label)

        return None
    
    def emit_setne(self, reg, comment=""):
        self.backend.emit_setne(reg, comment)
    
    def emit_soft_runtime_error(self, message):
        except_label = self.current_except_label()
        label = self.get_or_add_runtime_error_string(message)
        #label = self.add_string_literal(message)

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            if except_label is None:
                self.backend.emit_push_data_label32(label)
                self.emit_call("_jit_runtime_error")
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
            self.emit_mov_imm("rax", "&_jit_runtime_error")
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
            raise CompileError(ctx, "E0005", got=str(len(args)), expected="1")

        expr_type = self.visit(args[0])

        if not isinstance(expr_type, str) or not expr_type.startswith("^"):
            raise CompileError(ctx, "E0005", got=expr_type, expected="pointer")

        self.emit_test (REG_RAX, REG_RAX)
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
            self.writer.emit_lea_reg_data_label("esi", "ctx")
            
            if is_local:
                self.emit_store_local_var(ctx, name, ptr_type)
            else:
                slot = info["slot"]
                self.emit_mov_qword("rdx", "r12", "pointr_vars")
                self.emit_mov_qword_ptr_store("rdx", slot * 4, "rax")
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
            raise CompileError(ctx, "E0005", got=str(len(args)), expected="3")

        t1 = self.visit(args[0])
        if t1 != "string":
            raise CompileError(ctx, "E0005", got=t1, expected="string")

        self.emit_push("rax", comment='Copy source')

        t2 = self.visit(args[1])
        if t2 != "integer":
            raise CompileError(ctx, "E0005", got=t2, expected="integer")

        self.emit_movsxd(REG_RAX, REG_EAX)
        self.emit_push  (REG_RAX, comment='Copy start')

        t3 = self.visit(args[2])
        if t3 != "integer":
            raise CompileError(ctx, "E0005", got=t3, expected="integer")

        self.emit_movsxd(REG_RAX, REG_EAX)
        self.emit_push  (REG_RAX, comment='Copy count')

        self.emit_pop("r8")
        self.emit_pop(REG_RBX)
        self.emit_pop(REG_RCX)

        self.emit_sub     (REG_RSP, 32)
        self.emit_mov_imm (REG_RAX, "&_jit_dynstring_copy")
        self.emit_call    (REG_RAX)
        self.emit_add     (REG_RSP, 32)

        return "string"
    
    # ----------------------------------------
    # rcx = Suchstring
    # rdx = Quellstring
    # eax = Position oder 0
    # ----------------------------------------
    def emit_builtin_pos(self, ctx):
        args = self.function_call_args(ctx)

        if len(args) != 2:
            raise CompileError(ctx, "E0005", got=str(len(args)), expected="2")

        t1 = self.visit(args[0])
        if t1 != "string":
            raise CompileError(ctx, "E0005", got=t1, expected="string")

        self.emit_push(REG_RAX, comment='Pos needle')

        t2 = self.visit(args[1])
        if t2 != "string":
            raise CompileError(ctx, "E0005", got=t2, expected="string")

        self.emit_push("rax", comment='Pos haystack')

        self.emit_pop(REG_RDX)
        self.emit_pop(REG_RCX)

        self.emit_sub     (REG_RSP, 32)
        self.emit_mov_imm (REG_RAX, "&_jit_dynstring_pos")
        self.emit_call    (REG_RAX)
        self.emit_add     (REG_RSP, 32)

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
            # Länge sichern
            self.emit_push("eax")

            # old array pointer laden
            self.emit_load_var(name, var_info)

            # cdecl: Argumente rechts nach links pushen
            # _jit_dynarray_setlength(old_ptr, length, element_size)
            self.backend.writer.emit_push_imm32(array_info.element_size)

            self.emit_pop("ebx")      # ebx = length
            self.emit_push("ebx")

            self.emit_push("eax")     # old pointer

            self.emit_call("_jit_dynarray_setlength")
            self.backend.emit_cleanup_stack(12)

            # Runtime-Call kann ESI/ctx zerstören
            self.writer.emit_lea_reg_data_label("esi", "ctx")

            # Rückgabe eax = neuer array pointer
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
        array_label = self.add_string_literal(var_name)

        self.emit_mov("r10d", "eax", comment = "// save dimension index")

        self.emit_cmp("eax", min_value)
        self.emit_jl(fail_label)

        self.emit_cmp("eax", max_value)
        self.emit_jg(fail_label)

        self.emit_jmp(ok_label)

        self.emit_bind_label(fail_label)
        
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_bind_label(fail_label)
            msg = (
                f"Array bounds error: {var_name} index out of range "
                f"allowed range {min_value}..{max_value}"
            )

            self.emit_soft_runtime_error(msg)

            self.emit_bind_label(ok_label)
            self.emit_mov("eax", "r10d", comment="restore dimension index")
        else:
            self.emit_mov_imm("rcx", array_label)
            self.emit_mov("edx", "r10d")
            self.emit_mov("r8d", min_value)
            self.emit_mov("r9d", max_value)
            self.emit_mov_imm("rax", "&_jit_array_bounds_error")
            self.emit_call("rax")

            self.emit_bind_label(ok_label)
            self.emit_mov("eax", "r10d", comment = "restore dimension index")
    
    def emit_array_bounds_check_for_dimension(self, dim):
        min_value = dim["min"]
        max_value = dim["max"]

        self.emit_push("rax")

        self.emit_cmp("eax", min_value)
        self.emit_jl("array_bounds_error")

        self.emit_cmp("eax", max_value)
        self.emit_jg("array_bounds_error")

        self.emit_pop("rax")
    
    def emit_address_of_var(self, ctx, name):
        local_var = self.find_local_var(name)

        if local_var:
            typ    = local_var["type"]
            offset = local_var["offset"]

            if typ == "integer":
                self.emit_lea_dword("rax", "rbp", offset, comment = "@{name}")
                return "^integer"

            if typ == "double":
                self.emit_lea_qword("rax", "rbp", offset, comment = "@{name}")
                return "^double"

            if typ == "string":
                self.emit_lea_qword("rax", "rbp", offset, comment = "@{name}")
                return "^string"

            if isinstance(typ, str) and typ.startswith("^"):
                self.emit_lea_qword("rax", "rbp", offset, comment = "@{name}")
                return "^" + typ

            if isinstance(typ, str) and typ in self.records:
                self.emit_lea_byte("rax", "rbp", offset, comment = "@{name}")
                return "^" + typ

            if isinstance(typ, str) and typ in self.arrays:
                self.emit_lea_byte("rax", "rbp", offset, comment = "@{name}")
                return "^" + typ

            raise CompileError(ctx, "E0014", var_type=typ)

        key = name.lower()

        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=name)

        info = self.vars[key]
        typ  = info["type"]
        slot = info["slot"]

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

        if isinstance(typ, str) and typ.startswith("^"):
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
    
    def emit_address_of_array_element(self, ctx, var_name, index_exprs):
        var_info, array_info = self.get_array_info(ctx, var_name)

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        self.emit_imul("eax", "eax", array_info.element_size)
        self.emit_add("eax", var_info["slot"])

        self.emit_mov_qword("r11", "r12", "arrays_vars")
        self.emit_movsxd("rax", "eax")
        self.emit_add("rax", "r11", comment="@array[index]")

        return "^" + array_info.element_type
        
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
        self.emit_mov_imm("rax", "&_jit_array_bounds_error")
        self.emit_call("rax")

        self.emit_bind_label(ok_label)

        # Index wiederherstellen
        self.emit_mov("eax", "ebx", comment='restore array index')
    
    def emit_load_self_field(self, ctx, name):
        if self.current_class is None:
            return None

        cls = self.classes[self.current_class]
        key = name.lower()

        if key not in cls.fields:
            return None

        field = cls.fields[key]

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_mov_dword_ptr("eax", "ebp", -4, comment="Self")
        else:
            self.emit_mov_qword_ptr("rax", "rbp", -8, comment="Self")

        if field.type == "integer":
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_mov_dword_ptr("eax", "eax", field.offset, comment="Self")
            else:
                self.emit_mov_dword_ptr("eax", "rax", field.offset, comment=f"Self.{name}")
            return "integer"

        if field.type == "double":
            self.emit_movsd_load("xmm0", "rax", field.offset, comment=f"Self.{name}")
            return "double"

        if field.type == "string":
            self.emit_mov_qword_ptr("rax", "rax", field.offset, comment=f"Self.{name}")
            return "string"

        return field.type
    
    def emit_load_object_var(self, ctx, name, info):
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
        
        index_type = self.visit(index_exprs[0])
        
        if index_type != "integer":
            raise CompileError(ctx, "E0005", got=index_type, expected="integer")
        
        self.emit_sub("eax", 1)
        self.emit_mov("r10d", "eax")
        
        var_info = self.var_info(ctx, name)
        self.emit_load_var(name, var_info)
        
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

        var_info = self.var_info(ctx, obj_name)
        class_type = self.resolve_type(var_info["type"])

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
            self.emit_call(method.label)
            self.backend.emit_cleanup_stack(4)
            self.writer.emit_lea_reg_data_label("esi", "ctx")
            return self.resolve_type(method.return_type)

        self.emit_mov("rcx", "rax", comment="Self")
        self.emit_sub("rsp", 32)
        self.emit_call_lbl(method.label)
        self.emit_add("rsp", 32)

        return self.resolve_type(method.return_type)
    
    def emit_load_class_field(self, ctx, parts):
        var_info, field = self.resolve_class_field_path(ctx, parts)

        path = ".".join(parts)

        self.emit_load_object_var(ctx, parts[0], var_info)
        self.emit_nil_pointer_check(parts[0])

        if field.type == "integer":
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_mov_dword_ptr("eax", "eax", field.offset, comment=f"{path}")
            else:
                self.emit_mov_dword_ptr("eax", "rax", field.offset, comment=f"{path}")
            return "integer"

        if field.type == "double":
            self.emit_movsd_load("xmm0", "rax", field.offset, comment=path)
            return "double"

        if field.type == "string":
            self.emit_mov_qword_ptr("rax", "rax", field.offset, comment=f"{path}")
            return "string"

        return field.type
    
    def emit_load_const(self, ctx, name):
        c = self.find_const(name)

        if not c:
            raise CompileError(ctx, "E0001", name=name)

        typ = c["type"]
        val = c["value"]

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
    
    def emit_load_string_var_to_rax(self, ctx, name):
        var_info = self.var_info(ctx, name)
        slot = var_info["slot"]

        self.emit_mov_qword("rax", "r12", "string_vars")
        self.emit_mov_qword_ptr("rax", "rax", slot * self.pointer_slot_size())
    
    def emit_load_pointer_var_to_rax(self, ctx, name):
        var_info = self.var_info(ctx, name)
        slot = var_info["slot"]

        self.emit_mov_qword("rax", "r12", "pointr_vars")
        self.emit_mov_qword_ptr("rax", "rax", slot * self.pointer_slot_size())
    
    def emit_load_pointer_deref(self, ctx, name):
        key = name.lower()

        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=name)

        info = self.vars[key]
        typ = info["type"]

        if not isinstance(typ, str) or not typ.startswith("^"):
            raise CompileError(ctx, "E0005", got=typ, expected="pointer")

        base_type = typ[1:]

        self.emit_load_var(name, info)

        if base_type == "integer":
            self.emit_mov_reg_dword("eax", "rax", comment='p^')
            return "integer"

        if base_type == "double":
            self.emit_movsd_load("xmm0", "rax", 0, comment="p^")
            return "double"

        if base_type == "string":
            self.emit_mov_reg_qword("rax", "rax", comment='p^')
            return "string"

        raise CompileError(ctx, "E0014", var_type=base_type)
    
    def emit_load_param(self, ctx, name):
        param = self.find_param(name)

        if not param:
            raise CompileError(ctx, "E0001", name=name)
            
        typ    = self.resolve_type(param["type"])
        offset = param["stack_offset"]
        
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            if typ == "integer":
                self.emit_mov_dword_ptr("eax", "ebp", offset)
                return "integer"

            if typ == "string":
                self.emit_mov_dword_ptr("eax", "ebp", offset)
                return "string"

            if isinstance(typ, str) and typ.startswith("^"):
                self.emit_mov_dword_ptr("eax", "ebp", offset)
                return typ
        
        if param.get("is_var", False):
            self.emit_mov_qword_ptr("r11", "rbp", offset, comment=f"var param address {name}")
            
            if typ == "integer":
                self.emit_mov_reg_dword("eax", "r11")
                return "integer"
            
            if isinstance(typ, str) and typ.startswith("^"):
                self.emit_mov_reg_qword("rax", "r11")
                return typ
            
            raise CompileError(ctx, "E0014", var_type=typ)
        
        if typ == "integer":
            self.emit_mov_dword_ptr("eax", "rbp", offset)
            return "integer"
        
        if typ == "string":
            self.emit_mov_qword_ptr("rax", "rbp", offset)
            return "string"
        
        if isinstance(typ, str) and typ.startswith("^"):
            self.emit_mov_qword_ptr("rax", "rbp", offset)
            return typ
            
        raise CompileError(ctx, "E0014", var_type=typ)
    
    def emit_load_record_field(self, ctx, parts):
        field_offset, field = self.resolve_record_path(ctx, parts)
        path = ".".join(parts)

        self.emit_mov_qword("r11", "r12", "record_vars")

        if field.type == "integer":
            self.emit_mov_dword_ptr("eax", "r11", field_offset, comment=f"{path}")
            return "integer"

        if field.type == "double":
            self.emit_movsd_load("xmm0", "r11", field_offset, comment=path)
            return "double"

        if field.type == "string":
            self.emit_mov_qword_ptr("rax", "r11", field_offset, comment=f"{path}")
            return "string"

        return field.type
    
    def emit_load_pointer_record_field(self, ctx, parts):
        ptr_name = parts[0]
        ptr_key  = ptr_name.lower()

        ptr_info = self.find_local_var(ptr_name)
        is_local = ptr_info is not None

        if ptr_info is None:
            if ptr_key not in self.vars:
                raise CompileError(ctx, "E0001", name=ptr_name)

            ptr_info = self.vars[ptr_key]

        ptr_type = self.resolve_type(ptr_info["type"])

        if not isinstance(ptr_type, str) or not ptr_type.startswith("^"):
            raise CompileError(ctx, "E0005", got=ptr_type, expected="pointer")

        current_type = ptr_type[1:]

        # Startpointer laden: n1
        if is_local:
            self.emit_load_local_var(ctx, ptr_name, ptr_info)
        else:
            self.emit_load_var(ptr_name, ptr_info)
        
        #if CDATA.args_target not in ["nt35", "winnt", "win32"]:
        self.emit_nil_pointer_check(ptr_name)
        
        for index, field_name in enumerate(parts[1:]):
            if current_type not in self.records:
                raise CompileError(ctx, "E0005", got=current_type, expected="record")

            record = self.records[current_type]
            field_key = field_name.lower()

            if field_key not in record.fields:
                raise CompileError(ctx, "E0001", name=field_name)

            field = record.fields[field_key]
            is_last = index == len(parts[1:]) - 1

            if is_last:
                if field.type == "integer":
                    self.emit_mov_dword_ptr("eax", "rax", field.offset, comment=f"{'.'.join(parts)}")
                    return "integer"

                if field.type == "double":
                    self.emit_movsd_load("xmm0", "rax", field.offset, comment=f"{'.'.join(parts)}")
                    return "double"

                if field.type == "string":
                    self.emit_mov_qword_ptr("rax", "rax", field.offset, comment=f"{'.'.join(parts)}")
                    return "string"

                if field.type.startswith("^"):
                    self.emit_mov_qword_ptr("rax", "rax", field.offset, comment=f"{'.'.join(parts)}")
                    return field.type

                return field.type

            # Weiter in der Kette:
            # Next ist Pointer -> Pointerwert laden
            if field.type.startswith("^"):
                self.emit_mov_qword_ptr("rax", "rax", field.offset, comment=f"follow pointer {field_name}")
                current_type = field.type[1:]
                continue

            # eingebetteter Record
            if field.type in self.records:
                if field.offset != 0:
                    self.emit_add("rax", field.offset, comment=f"nested record {field_name}")
                current_type = field.type
                continue

            raise CompileError(ctx, "E0005", got=field.type, expected="record/pointer")
    
    def emit_load_local_var(self, ctx, name, info):
        var = self.find_local_var(name)

        if not var:
            raise CompileError(ctx, "E0012", name=name)

        typ    = var["type"]
        offset = var["offset"]

        if typ == "integer":
            self.emit_mov_dword_ptr("eax", "rbp", offset, comment=f"local {name}")
            return "integer"

        if typ == "string":
            if CDATA.args_target in ["dos", "dos16"]:
                # DX = Offset, DS bleibt unverändert
                self.backend.writer.emit_mov_reg16_mem16_base_disp("dx", "bp", offset)
                return "string"

            self.emit_mov_qword_ptr("rax", "rbp", offset, comment=f"local string {name}")
            return "string"

        if isinstance(typ, str) and typ.startswith("^"):
            self.emit_mov_qword_ptr("rax", "rbp", offset, comment=f"local pointer {name}")
            return typ

        raise CompileError(ctx, "E0011", typ=typ)

    def emit_builtin_string_setlength(self, ctx, name, length_ctx):
        self.visit(length_ctx)
        self.emit_movsxd("rdx", "eax")
        self.emit_load_string_var_to_rax(ctx, name)
        self.emit_mov("rcx", "rax")
        self.emit_mov_imm("rax", "&_jit_dynstring_setlength")
        self.emit_call("rax")
        self.emit_store_string_var_from_rax(ctx, name)
    
    def emit_store_self_field(self, ctx, name, expr_type):
        field = self.find_current_class_field(name)

        if field is None:
            return False

        if field.type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)

        if expr_type == "integer":
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

        if expr_type == "double":
            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")
            self.emit_mov_qword_ptr("rax", "rbp", -8, comment='Self')
            self.emit_movsd_load("xmm0", "rsp")
            self.emit_add("rsp", 8)
            self.emit_movsd_store("rax", field.offset, "xmm0", comment=f"Self.{name} :=")
            return True

        if expr_type == "string":
            self.emit_push("rax")
            self.emit_mov_qword_ptr("rax", "rbp", -8, comment='Self')
            self.emit_pop("r11")
            self.emit_mov_qword_ptr_store("rax", field.offset, "r11", comment=f"Self.{name} :=")
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
            
        if hasattr(self, "coff") and "symbol" in info:
            self.coff.emit_mov_data_label_r64(info["symbol"], "rax")
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

        self.emit_mov_qword("r11", "r12", "pointr_vars")
        self.emit_mov_qword_ptr_store("r11", slot * self.pointer_slot_size(), "rax", comment=f"object {name}")
        return
    
    def emit_store_class_property(self, ctx, parts, expr_type):
        obj_name  = parts[0]
        prop_name = parts[1]

        var_info = self.var_info(ctx, obj_name)
        class_type = self.resolve_type(var_info["type"])

        if class_type not in self.classes:
            return False

        cls = self.classes[class_type]
        prop = self.resolve_class_property(class_type, prop_name)

        if prop is None:
            return False

        if prop.write_name is None:
            raise CompileError(ctx, "E0006")

        if expr_type != prop.ptype:
            raise CompileError(ctx, "E0005", got=expr_type, expected=prop.ptype)

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
        self.emit_push("rax", comment="property value")

        method, owner_cls = self.find_class_method_recursive(
            ctx,
            class_type,
            write_name,
            [expr_type]
        )

        self.emit_load_object_var(ctx, obj_name, var_info)
        self.emit_nil_pointer_check(obj_name)

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_pop("ebx")
            self.emit_push("ebx", comment="property setter value")
            self.emit_push("eax", comment="Self")
            self.emit_call(method.label)
            self.backend.emit_cleanup_stack(8)
            self.writer.emit_lea_reg_data_label("esi", "ctx")
            return True

        self.emit_pop("rdx")
        self.emit_mov("rcx", "rax", comment="Self")
        self.emit_sub("rsp", 32)
        self.emit_call_lbl(method.label)
        self.emit_add("rsp", 32)

        return True
    
    def emit_store_class_field(self, ctx, parts, expr_type):
        var_info, field = self.resolve_class_field_path(ctx, parts)
        
        if field.type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)
        
        # rechten Wert sichern, bevor RAX für Objektpointer benutzt wird
        if expr_type == "integer":
            self.emit_mov("ebx", "eax", comment='save class field value')
        
        elif expr_type == "double":
            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")
        
        elif expr_type == "string":
            self.emit_push("rax", comment='save string field value')
        
        else:
            raise CompileError(ctx, "E0013", var_type=field.type)
        
        self.emit_load_object_var(ctx, parts[0], var_info)
        self.emit_nil_pointer_check(parts[0])
        
        if field.type == "integer":
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_mov_dword_ptr_store("eax", field.offset, "ebx", comment=f"{'.'.join(parts)} :=")
            else:
                self.emit_mov_dword_ptr_store("rax", field.offset, "ebx", comment=f"{'.'.join(parts)} :=")
            return
        
        if field.type == "double":
            self.emit_movsd_load("xmm0", "rsp")
            self.emit_add("rsp", 8)
            self.emit_movsd_store("rax", field.offset, "xmm0", comment=f"{'.'.join(parts)} :=")
            return
        
        if field.type == "string":
            self.emit_pop("r11")
            self.emit_mov_qword_ptr_store("rax", field.offset, "r11", comment=f"{'.'.join(parts)} :=")
            return
        
        raise CompileError(ctx, "E0013", var_type=field.type)
    
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

        # Zeichenwert sichern: RAX zeigt auf Stringliteral, erstes Zeichen laden
        self.emit_movzx("ebx", "byte_ptr(rax)", comment="char value")

        # Index berechnen
        index_type = self.visit(index_exprs[0])

        if index_type != "integer":
            raise CompileError(ctx, "E0005", got=index_type, expected="integer")

        # Pascal: s[1] -> data[0]
        self.emit_sub("eax", 1)
        self.emit_mov("r10d", "eax", comment='zero based string index')

        # String-Datenpointer laden
        var_info = self.var_info(ctx, name)
        self.emit_load_var(name, var_info)  # RAX = char*

        # nil check
        nil_ok = self.new_named_label("string_not_nil")
        self.emit_test("rax", "rax")
        self.emit_jnz(nil_ok)
        self.emit_mov_imm("rax", "&_jit_string_range_error")
        self.emit_call("rax")
        self.emit_bind_label(nil_ok)

        # length aus Header laden: header liegt 16 Bytes vor data
        self.emit_mov("r11", "rax")
        self.emit_sub("r11", 16)
        self.emit_mov_reg_qword("r11", "r11", comment='string length')

        # Range Check:
        # r10d darf nicht negativ sein und muss < length sein
        ok_label = self.new_named_label("string_index_ok")
        fail_label = self.new_named_label("string_index_fail")

        self.emit_cmp("r10d", 0)
        self.emit_jl(fail_label)

        self.emit_cmp("r10", "r11")
        self.emit_jb(ok_label)

        self.emit_bind_label(fail_label)
        self.emit_mov_imm("rax", "&_jit_string_range_error")
        self.emit_call("rax")

        self.emit_bind_label(ok_label)

        # Adresse berechnen und schreiben
        self.emit_movsxd("r11", "r10d")
        self.emit_add("r11", "rax")
        self.emit_mov_byte_ptr_store("r11", 0, "bl", comment="s[index] :=")
    
    def pointer_slot_size(self):
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            return 4
        return 8
    
    def emit_store_pointer_var_from_rax(self, ctx, name):
        var_info = self.var_info(ctx, name)
        slot = var_info["slot"]

        self.emit_mov_qword("rdx", "r12", "pointr_vars")
        self.emit_mov_qword_ptr_store("rdx", slot * self.pointer_slot_size(), "rax")
    
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
        field_offset, field = self.resolve_record_path(ctx, parts)

        if field.type == "double" and expr_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")
            expr_type = "double"

        if field.type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)

        path = ".".join(parts)

        self.emit_mov_qword("r11", "r12", "record_vars")

        if field.type == "integer":
            self.emit_mov_dword_ptr_store("r11", field_offset, "eax", comment=path)
            return

        if field.type == "double":
            self.emit_movsd_store("r11", field_offset, "xmm0", comment=path)
            return

        if field.type == "string":
            self.emit_mov_qword_ptr_store("r11", field_offset, "rax", comment=path)
            return

        raise CompileError(ctx, "E0013", var_type=field.type)
    
    def emit_store_param(self, ctx, name, expr_type):
        param = self.find_param(name)

        if not param:
            raise CompileError(ctx, "E0001", name=name)

        if not param.get("is_var", False):
            raise CompileError(ctx, "E0006")

        typ    = self.resolve_type(param["type"])
        offset = param["stack_offset"]

        if typ != expr_type and expr_type != "^nil":
            raise CompileError(ctx, "E0005", got=expr_type, expected=typ)

        self.emit_mov_qword_ptr("r11", "rbp", offset, comment=f"var param address {name}")

        if typ == "integer":
            self.emit_mov_dword_ptr_store("r11", 0, "eax")
            return

        if isinstance(typ, str) and typ.startswith("^"):
            self.emit_mov_qword_ptr_store("r11", 0, "rax")
            return

        raise CompileError(ctx, "E0013", var_type=typ)
    
    def emit_store_pointer_record_field(self, ctx, parts, expr_type):
        ptr_info, field_offset, field = self.resolve_pointer_record_path(ctx, parts)
        ptr_name = parts[0]
        path = "^.".join([ptr_name, ".".join(parts[1:])])

        is_nil_pointer = (
            isinstance(field.type, str)
            and field.type.startswith("^")
            and expr_type in ("integer", "^nil")
        )
        
        if isinstance(field.type, str) and field.type.startswith("^"):
            if is_nil_pointer:
                self.emit_xor("rax", "rax", comment="nil pointer")

        if field.type != expr_type and not is_nil_pointer:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)

        # Pointer-Feld zuerst behandeln!
        if isinstance(field.type, str) and field.type.startswith("^"):
            if is_nil_pointer:
                self.emit_xor("rax", "rax", comment="nil pointer")

            self.emit_push("rax", comment='save right pointer value')

            if ptr_info.get("is_local", False):
                self.emit_load_local_var(ctx, ptr_name, ptr_info)
            else:
                self.emit_load_var(ptr_name, ptr_info)

            if field_offset != 0:
                self.emit_add("rax", field_offset, comment="field offset")

            self.emit_pop("r11")
            self.emit_mov_qword_ptr_store("rax", 0, "r11", comment=f"{path} :=")
            return

        if field.type == "double" and expr_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")
            expr_type = "double"

        if expr_type == "integer":
            self.emit_mov("ebx", "eax")

        elif expr_type == "double":
            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")

        elif expr_type == "string":
            self.emit_push("rax")

        if ptr_info.get("is_local", False):
            self.emit_load_local_var(ctx, ptr_name, ptr_info)
        else:
            self.emit_load_var(ptr_name, ptr_info)
        
        if CDATA.args_target not in ["nt35", "winnt", "win32"]:
            self.emit_nil_pointer_check(ptr_name)

        if field_offset != 0:
            self.emit_add("rax", field_offset, comment="field offset")

        if field.type == "integer":
            self.emit_mov_dword_ptr_store("rax", 0, "ebx", comment=f"{path} :=")
            return

        if field.type == "double":
            self.emit_movsd_load("xmm0", "rsp")
            self.emit_add("rsp", 8)
            self.emit_movsd_store("rax", 0, "xmm0", comment=f"{path} :=")
            return

        if field.type == "string":
            self.emit_pop("r11")
            self.emit_mov_qword_ptr_store("rax", 0, "r11", comment=f"{path} :=")
            return

        raise CompileError(ctx, "E0013", var_type=field.type)
    
    def emit_store_array_element(self, ctx, var_name, index_expr_ctx, expr_type):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
            
        var_info, array_info = self.get_array_info(ctx, var_name)
        
        if getattr(array_info, "is_dynamic", False):
            if array_info.element_type == "double" and expr_type == "integer":
                self.emit_cvtsi2sd("xmm0", "eax")
                expr_type = "double"

            if array_info.element_type != expr_type:
                raise CompileError(ctx, "E0005", got=expr_type, expected=array_info.element_type)

            if expr_type == "integer":
                self.emit_mov_dword_ptr_store("r12", "offsetof(JitContext, print_int_tmp)", "eax")
            elif expr_type == "double":
                self.emit_movsd_store("r12", "offsetof(JitContext, print_double_tmp)", "xmm0")
            elif expr_type == "string":
                self.emit_push("rax")

            index_exprs = index_expr_ctx
            if not isinstance(index_exprs, list):
                index_exprs = [index_exprs]

            if len(index_exprs) != 1:
                raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

            index_type = self.visit(index_exprs[0])

            if index_type != "integer":
                raise CompileError(ctx, "E0005", got=index_type, expected="integer")

            self.emit_imul("eax", "eax", array_info.element_size)
            self.emit_mov("r10d", "eax", comment='save dynamic array byte offset')

            self.emit_load_var(var_name, var_info)   # RAX = data pointer
            self.emit_movsxd("r11", "r10d")
            self.emit_add("r11", "rax", comment="dynamic array element address")

            if array_info.element_type == "integer":
                self.emit_mov_dword("eax", "r12", "print_int_tmp")
                self.emit_mov_dword_ptr_store("r11", 0, "eax")
                return

            if array_info.element_type == "double":
                self.emit_movsd_load_field("xmm0", "r12", "print_double_tmp")
                self.emit_movsd_store("r11", 0, "xmm0")
                return
                
            # AsmJitGenerator
            if array_info.element_type == "string":
                self.emit_pop("rax")
                self.emit_mov_qword_ptr_store("r11", 0, "rax")
                return

            raise CompileError(ctx, "E0013", var_type=array_info.element_type)

        if array_info.element_type == "double" and expr_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")
            expr_type = "double"

        if array_info.element_type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=array_info.element_type)

        if expr_type == "integer":
            self.emit_mov_dword_ptr_store("r12", "offsetof(JitContext, print_int_tmp)", "eax")

        elif expr_type == "double":
            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")

        elif expr_type == "string":
            self.emit_push("rax")

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        self.emit_imul("eax", "eax", array_info.element_size)
        self.emit_add("eax", var_info["slot"])

        self.emit_mov_qword("r11", "r12", "arrays_vars")
        self.emit_movsxd("rax", "eax")
        self.emit_add("r11", "rax")

        if array_info.element_type == "integer":
            self.emit_mov_dword("eax", "r12", "print_int_tmp")
            self.emit_mov_dword_ptr_store("r11", 0, "eax")
            return

        if array_info.element_type == "double":
            self.emit_movsd_load("xmm0", "rsp")
            self.emit_add("rsp", 8)
            self.emit_movsd_store("r11", 0, "xmm0")
            return

        # AsmJitGenerator
        if array_info.element_type == "string":
            self.emit_pop("rax")
            self.emit_mov_qword_ptr_store("r11", 0, "rax")
            return

        raise CompileError(ctx, "E0013", var_type=array_info.element_type)

    def emit_load_array_element(self, ctx, var_name, index_expr_ctx):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
            
        var_info, array_info = self.get_array_info(ctx, var_name)
        
        if getattr(array_info, "is_dynamic", False):
            index_exprs = index_expr_ctx
            if not isinstance(index_exprs, list):
                index_exprs = [index_exprs]

            if len(index_exprs) != 1:
                raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

            index_type = self.visit(index_exprs[0])

            if index_type != "integer":
                raise CompileError(ctx, "E0005", got=index_type, expected="integer")

            self.emit_imul("eax", "eax", array_info.element_size)
            self.emit_mov("r10d", "eax", comment='save dynamic array byte offset')

            self.emit_load_var(var_name, var_info)   # RAX = data pointer
            self.emit_movsxd("r11", "r10d")
            self.emit_add("r11", "rax", comment="dynamic array element address")

            if array_info.element_type == "integer":
                self.emit_mov_reg_dword("eax", "r11")
                return "integer"

            if array_info.element_type == "double":
                self.emit_movsd_load("xmm0", "r11")
                return "double"

            # AsmJitGenerator
            if array_info.element_type == "string":
                self.emit_mov_reg_qword("rax", "r11")
                return "string"

            raise CompileError(ctx, "E0014", var_type=array_info.element_type)

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        self.emit_imul("eax", "eax", array_info.element_size)
        self.emit_add("eax", var_info["slot"])

        self.emit_mov_qword("r11", "r12", "arrays_vars")
        self.emit_movsxd("rax", "eax")
        self.emit_add("r11", "rax")

        if array_info.element_type == "integer":
            self.emit_mov_reg_dword("eax", "r11")
            return "integer"

        if array_info.element_type == "double":
            self.emit_movsd_load("xmm0", "r11")
            return "double"

        if array_info.element_type == "string":
            self.emit_mov_reg_qword("rax", "r11")
            return "string"

        raise CompileError(ctx, "E0014", var_type=array_info.element_type)
        
    def emit_store_result(self, ctx, expr_type):
        if self.current_function is None:
            raise CompileError(ctx, "E0006")

        return_type = self.resolve_type(self.current_function["return_type"])

        if return_type == "integer" and expr_type == "char":
            expr_type = "integer"

        if return_type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=return_type)

        result_var = self.find_local_var("Result")
        if result_var is None:
            raise CompileError(ctx, "E0012", name="Result")

        offset = result_var["offset"]

        if CDATA.args_target in ["dos", "dos16"]:
            if return_type == "integer":
                self.backend.writer.emit_mov_mem16_base_disp_reg16("bp", offset, "ax")
                return None

            if return_type == "string":
                # DX enthält Offset auf DOS-$-String
                self.backend.writer.emit_mov_mem16_base_disp_reg16("bp", offset, "dx")

                # Segment bleibt 0 / unbenutzt
                self.backend.writer.emit_mov_reg16_imm16("ax", 0)
                self.backend.writer.emit_mov_mem16_base_disp_reg16("bp", offset + 2, "ax")
                return None

            raise CompileError(ctx, "E0005", got=return_type, expected="integer/string")

        elif CDATA.args_target in ["nt35", "winnt", "win32"]:
            if return_type == "integer":
                self.emit_mov_dword_ptr_store("ebp", offset, "eax")
                return None
                
            elif return_type == "string":
                self.emit_mov_dword_ptr_store("ebp", offset, "eax")
                return None
            
            elif return_type == "double":
                raise Exception(tr("double not implemented, yet"))
        else:
            if return_type == "integer":
                self.emit_mov_dword_ptr_store("rbp", offset, "eax")
                return None
                
            elif return_type == "string":
                self.emit_mov_dword_ptr_store("rbp", offset, "rax")
                return None
                
            elif return_type == "double":
                self.emit_movsd_store("rbp", offset, "xmm0")
                return None
        
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
        self.emit_jae("label_array_bounds_error")

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

        typ    = var["type"]
        offset = var["offset"]

        if typ == "integer":
            if expr_type != "integer":
                raise CompileError(ctx, "E0005", got=expr_type, expected=typ)

            self.emit_mov_dword_ptr_store("rbp", offset, "eax", comment=f"local {name} :=")
            return

        if typ == "string":
            if expr_type not in ("string", "char"):
                raise CompileError(ctx, "E0005", got=expr_type, expected=typ)

            if CDATA.args_target in ["dos", "dos16"]:
                # DOS-String-Literal liegt in DX.
                # Lokaler String als Far Pointer: offset + segment.
                self.backend.writer.emit_mov_mem16_base_disp_reg16("bp", offset, "dx")
                
                # Segment nicht verwenden, immer 0 setzen
                self.backend.writer.emit_mov_reg16_imm16("ax", 0)
                self.backend.writer.emit_mov_mem16_base_disp_reg16("bp", offset + 2, "ax")
                return

            self.emit_mov_qword_ptr_store("rbp", offset, "rax", comment=f"local string {name} :=")
            return
    
        if isinstance(typ, str) and typ.startswith("^"):
            if expr_type != typ and expr_type != "^nil":
                raise CompileError(ctx, "E0005", got=expr_type, expected=typ)

            self.emit_mov_qword_ptr_store("rbp", offset, "rax", comment=f"local pointer {name} :=")
            return

        raise CompileError(ctx, "E0011", typ=typ)
        
    def emit_call_rax(self):
        self.backend.emit_call("rax")
    
    def emit_load_pointer_var_to_rax(self, name, info):
        slot = info["slot"]

        self.emit_mov_qword("rax", "r12", "pointr_vars")
        self.emit_mov_qword_ptr(
            "rax",
            "rax",
            slot * self.pointer_slot_size()
        )
    
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
            if isinstance(typ, str) and typ.startswith("^"):
                self.emit_mov_qword("rax", "r12", "pointr_vars")
                self.emit_mov_qword_ptr("rax", "rax", slot * self.pointer_slot_size())
                return typ
            
            var_type = self.resolve_type(info["type"])
            if var_type == "integer":
                symbol = info.get("symbol")
                if not symbol:
                    symbol = f"_var_{info['name']}"
                    info["symbol"] = symbol
                    
                self.backend.writer.emit_mov_reg_from_data_label32("eax", symbol)
                return "integer"
                
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

            if isinstance(typ, str) and typ.startswith("^"):
                self.coff.emit_mov_r64_data_label("rax", symbol)
                return
        
        # -------------------------------------------------
        # Altes System über JitContext / r12
        # -------------------------------------------------
        if isinstance(typ, str) and typ.startswith("^"):
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

        if hasattr(self, "coff") and "symbol" in info:
            symbol = info["symbol"]

            if typ == "integer":
                self.coff.emit_mov_data_label_r32(symbol, "eax")
                return

            if typ == "double":
                self.coff.emit_movsd_data_label_store(symbol, "xmm0")
                return

            if typ == "string":
                self.coff.emit_mov_data_label_r64(symbol, "rax")
                return

            if isinstance(typ, str) and typ.startswith("^"):
                if CDATA.args_target in ["winnt", "nt35", "win32"]:
                    self.coff.emit_mov_data_label_r32(symbol, "eax")
                else:
                    self.coff.emit_mov_data_label_r64(symbol, "rax")
                return

        if typ.startswith("^"):
            if hasattr(self, "coff") and CDATA.args_target in ["winnt", "nt35", "win32"]:
                #symbol = info.get("symbol")
                #
                #if not symbol:
                #    symbol = f"_var_{name}"
                #    info["symbol"] = symbol
                #
                #    if self.coff.find_symbol_index(symbol) is None:
                #        self.coff.add_data_i32(symbol, 0)
                #
                #self.coff.emit_mov_data_label_r32(symbol, "eax")
                self.emit_mov_qword("r11", "r12", "pointr_vars")
                self.emit_mov_qword_ptr_store(
                    "r11",
                    slot * self.pointer_slot_size(),
                    "rax",
                    comment=f"{name}"
                )
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

        end_label = self.new_label(f"endproc_{proc_name}")

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
    
    def emit_address_of_array_element(self, ctx, var_name, index_exprs):
        var_info, array_info = self.get_array_info(ctx, var_name)

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        self.emit_imul("eax", "eax", array_info.element_size)
        self.emit_add("eax", var_info["slot"])

        self.emit_mov_qword("r11", "r12", "arrays_vars")
        self.emit_movsxd("rax", "eax")
        self.emit_add("rax", "r11", comment="@array[index]")

        return "^" + array_info.element_type

    def emit_function_declaration(self, ctx, name, return_type):
        key    = name.lower()
        scoped = self.scoped_name(name)

        label     = self.functions[key]["label"]
        end_label = self.new_named_label("endfunc_" + name)

        self.functions[scoped.lower()]["label"] = label

        params = self.collect_formal_params(ctx)
        self.functions[scoped.lower()]["params"] = params

        param_regs = ["rcx", "rdx", "r8", "r9"]

        if len(params) > len(param_regs):
            raise CompileError(ctx, "E0005", got="too many params", expected="max 4 params")

        rt = return_type.lower()

        if rt not in ["integer", "string", "double"]:
            raise CompileError(ctx, "E0005", got=return_type, expected="integer/string/double")

        self.emit_jmp(end_label)
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
            "return_type": rt,
            "scoped_name": scoped
        }

        # -------------------------------------------------
        # Lokalen Scope zuerst anlegen
        # -------------------------------------------------
        self.scope_stack.append(name)
        self.push_local_scope()
        self.push_const_scope()

        # Result als echte lokale Variable
        self.declare_local_var(ctx, "Result", rt)
        result_var = self.find_local_var("Result")
        result_off = result_var["offset"]

        # lokale var-Deklarationen vorab einsammeln,
        # damit scope["next_offset"] die echte Stackgröße enthält
        for child in ctx.children:
            cname = type(child).__name__
            if "VarSectionContext" in cname:
                self.visit(child)

        scope = self.current_local_scope()
        local_size = scope["next_offset"]
        local_size = (local_size + 15) & ~15

        if local_size:
            if CDATA.args_target in ["dos", "dos16"]:
                self.emit_sub("sp", local_size, comment=f"{local_size} bytes locals")
            elif CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_sub("esp", local_size, comment=f"{local_size} bytes locals")
            else:
                self.emit_sub("rsp", local_size, comment=f"{local_size} bytes locals")

        # -------------------------------------------------
        # Parameter sichern / Offsets eintragen
        # -------------------------------------------------
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            for index, p in enumerate(params):
                pname = p["name"]

                self.current_proc_params[pname.lower()] = {
                    "type": p["type"],
                    "reg": None,
                    "stack_offset": 8 + index * 4
                }

        elif CDATA.args_target in ["dos", "dos16"]:
            for index, p in enumerate(params):
                pname = p["name"]

                self.current_proc_params[pname.lower()] = {
                    "type": p["type"],
                    "reg": None,
                    "stack_offset": 4 + index * 2
                }

        else:
            for index, p in enumerate(params):
                reg = param_regs[index]
                pname = p["name"]

                self.emit_push(reg, comment=f"save function param {pname}")

                self.current_proc_params[pname.lower()] = {
                    "type": p["type"],
                    "reg": reg,
                    "stack_offset": -8 * (index + 2)
                }

            if len(params) % 2 == 0:
                self.emit_sub("rsp", 8, comment="align stack in function")

        # -------------------------------------------------
        # Funktionskörper
        # -------------------------------------------------
        self.exit_label_stack.append(end_label)
        self.visit(ctx.block())
        self.exit_label_stack.pop()

        self.pop_const_scope()
        self.pop_local_scope()
        self.scope_stack.pop()

        self.current_function = old_function
        self.current_proc_params = old_params

        # -------------------------------------------------
        # Return-Wert laden
        # -------------------------------------------------
        if CDATA.args_target in ["dos", "dos16"]:
            if rt == "string":
                self.backend.writer.emit_mov_reg16_mem16_base_disp("dx", "bp", result_off)
                self.backend.writer.emit_mov_reg16_mem16_base_disp("ax", "bp", result_off + 2)
            elif rt == "integer":
                self.backend.writer.emit_mov_reg16_mem16_base_disp("ax", "bp", result_off)
            else:
                raise CompileError(ctx, "E0005", got=return_type, expected="integer/string")

            self.backend.writer.emit_mov_reg16_reg16("sp", "bp")
            self.backend.writer.emit_pop_reg16("bp")
            self.backend.writer.emit_ret()

            self.emit_bind_label(end_label)
            return

        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            if rt == "string":
                self.emit_mov_dword_ptr("eax", "ebp", result_off)
            elif rt == "integer":
                self.emit_mov_dword_ptr("eax", "ebp", result_off)
            else:
                raise CompileError(ctx, "E0005", got=return_type, expected="integer/string")

            self.emit_mov("esp", "ebp")
            self.emit_pop("ebp")
            self.emit_ret()

            self.emit_bind_label(end_label)
            return

        if rt == "string":
            self.emit_mov_qword_ptr("rax", "rbp", result_off)
        elif rt == "integer":
            self.emit_mov_dword_ptr("eax", "rbp", result_off)
        else:
            self.emit_movsd_load("xmm0", "rbp", result_off)

        self.emit_mov("rsp", "rbp")
        self.emit_pop("rbp")
        self.emit_ret()

        self.emit_bind_label(end_label)
    
    def emit_try_except_statement(self, ctx):
        except_label = self.new_named_label("except")
        end_label    = self.new_named_label("endtry")

        frame_size = 512

        # ExceptionFrame auf Stack reservieren
        self.emit_sub("esp", frame_size, comment="exception frame")
        self.emit_mov("ebx", "esp", comment="frame ptr")

        # _jit_push_exception(frame)
        self.emit_push("ebx")
        self.emit_call("_jit_push_exception")
        self.backend.emit_cleanup_stack(4)

        # setjmp(frame->env)
        # frame beginnt direkt mit jmp_buf/env
        self.emit_push("ebx")
        self.emit_call("_setjmp")
        self.backend.emit_cleanup_stack(4)

        # setjmp == 0 -> try block
        # setjmp != 0 -> except block
        self.emit_cmp("eax", 0)
        self.emit_jne(except_label)

        # TRY-Block
        self.visit(ctx.statementList(0))

        # Kein Fehler: ExceptionFrame entfernen
        self.emit_push("ebx")
        self.emit_call("_jit_pop_exception")
        self.backend.emit_cleanup_stack(4)

        self.emit_add("esp", frame_size, comment="free exception frame")
        self.emit_jmp(end_label)

        # EXCEPT-Block
        self.emit_bind_label(except_label)

        # Nach longjmp ist esp wieder korrekt im setjmp-Kontext,
        # EBX aber nicht garantiert. Frame liegt wieder bei ESP.
        self.emit_mov("ebx", "esp", comment="restore frame ptr")

        self.emit_push("ebx")
        self.emit_call("_jit_pop_exception")
        self.backend.emit_cleanup_stack(4)

        self.visit(ctx.statementList(1))

        self.emit_add("esp", frame_size, comment="free exception frame")

        self.emit_bind_label(end_label)
        self.writer.emit_lea_reg_data_label("esi", "ctx")

        return None
    
    def emit_self_method_call(self, ctx, method_name, actual_types=None):
        if actual_types is None:
            actual_types = []

        if self.current_class is None:
            return None

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

        self.emit_mov_qword_ptr("rcx", "rbp", -8, comment='Self')
        self.emit_sub("rsp", 32)
        self.emit_call_lbl(method.label, comment=f"Self.{method.name}")
        self.emit_add("rsp", 32)

        return self.resolve_type(method.return_type)
    
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

            if expr_type != "integer":
                raise CompileError(ctx, "E0005", got=expr_type, expected="boolean/integer")

            self.normalize_bool_eax()
            self.emit_cmp("eax", 0)
            self.emit_je(false_label)
            return

        left_ctx  = ctx.expr(0)
        right_ctx = ctx.expr(1)
        op        = ctx.compareOp().getText()

        left_type = self.visit(left_ctx)
        
        if isinstance(left_type, str) and left_type.startswith("^"):
            self.emit_push("rax", comment='save left pointer')

            right_type = self.visit(right_ctx)

            if right_type != left_type and right_type != "^nil":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=right_type,
                    expected=left_type + "/nil"
                )

            self.emit_mov("rbx", "rax", comment='right pointer')
            self.emit_pop("rax", comment="left pointer")
            self.emit_cmp("rax", "rbx")

            if op == "=":
                self.emit_jne(false_label)
                return

            if op == "<>":
                self.emit_je(false_label)
                return

            raise CompileError(
                ctx,
                "E0005",
                got=op,
                expected="= or <>"
            )

        if left_type == "integer":
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
    
    def emit_repeat_statement(self, ctx):
        start_label = self.new_label_name("repeat")
        end_label   = self.new_label_name("endrepeat")

        self.emit_label(start_label)

        # Body
        for stmt in ctx.statement():
            self.visit(stmt)

        # Bedingung am Ende auswerten
        # Wichtig: Springe zurück, wenn Bedingung FALSE ist
        self.emit_condition_jump_false(ctx.condition(), start_label)
        self.emit_label(end_label)
    
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
        info = self.var_info(ctx, var_name)

        if info["type"] != "integer":
            raise CompileError(ctx, "E0005", got=info["type"], expected="integer")

        start_name    = self.new_named_label("for")
        continue_name = self.new_named_label("for_continue")
        end_name      = self.new_named_label("endfor")

        # Startwert auswerten
        start_type = self.visit(ctx.expr(0))

        if start_type != "integer":
            raise CompileError(ctx, "E0005", got=start_type, expected="integer")

        self.emit_store_var(ctx, var_name, info)

        # Endwert auswerten
        end_type = self.visit(ctx.expr(1))

        if end_type != "integer":
            raise CompileError(ctx, "E0005", got=end_type, expected="integer")

        target = CDATA.args_target.lower()

        if target in ["winnt", "nt35", "win32"]:
            # NT32: for-end-Wert erstmal in globaler Datenvariable speichern
            if self.coff.find_symbol_index("__for_end_tmp") is None:
                self.coff.add_data_i32("__for_end_tmp", 0)

            self.coff.emit_mov_data_label_r32("__for_end_tmp", "eax")

        else:
            self.emit_mov_dword_ptr_store(
                "r12",
                JIT_CONTEXT_OFFSETS["print_int_tmp"],
                "eax",
                comment="for end value"
            )

        self.emit_bind_label(start_name)
        self.emit_load_var(var_name, info)

        direction = ctx.getChild(4).getText().lower()

        target = CDATA.args_target.lower()

        if target in ["dos", "dos16"]:
            self.backend.emit_load_for_end_bx()
            self.emit_cmp("eax", "ebx")

            if direction == "to":
                self.emit_jg(end_name)
            else:
                self.emit_jl(end_name)
                
        elif target in ["winnt", "nt35", "win32"]:
            self.coff.emit_mov_reg_from_data_label32("ebx", "__for_end_tmp")
            self.emit_cmp("eax", "ebx")

            if direction == "to":
                self.emit_jg(end_name)
            else:
                self.emit_jl(end_name)
        else:
            if direction == "to":
                self.emit_cmp_dword("eax", "r12", "_print_int_tmp")
                self.emit_jg(end_name)
            else:
                self.emit_cmp_dword("eax", "r12", "_print_int_tmp")
                self.emit_jl(end_name)

        self.break_label_stack.append(end_name)
        self.continue_label_stack.append(continue_name)

        self.visit(ctx.statement())

        self.continue_label_stack.pop()
        self.break_label_stack.pop()

        self.emit_bind_label(continue_name)

        self.emit_load_var(var_name, info)

        if direction == "to":
            self.emit_add("eax", 1)
        else:
            self.emit_sub("eax", 1)

        self.emit_store_var(ctx, var_name, info)

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
        return any(s.DOT() for s in ref.variableSuffix())
    
    def variable_ref_has_index(self, ref):
        return any(s.LBRACK() for s in ref.variableSuffix())
    
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
    
    def emit_new_label_decl(self, name, comment=""):
        self.backend.emit_new_label_decl(name, comment)
        
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
    def emit_mov_byte_ptr_store(self, base, offset, src, comment=""): self.backend.emit_mov_byte_ptr_store(base, offset, src, comment)
    def emit_mov_reg_byte (self, dst, base, comment=""): self.backend.emit_mov_reg_byte (dst, base, comment)
    def emit_mov_reg_dword(self, dst, base, comment=""): self.backend.emit_mov_reg_dword(dst, base, comment)
    def emit_mov_reg_qword(self, dst, base, comment=""): self.backend.emit_mov_reg_qword(dst, base, comment)
    def emit_test(self, reg1, reg2, comment=""): self.backend.emit_test(reg1, reg2, comment)
    def emit_call_reg(self, target, comment=""): self.backend.emit_call_reg(target, comment)
    def emit_call_lbl(self, target, comment=""): self.backend.emit_call_lbl(target, comment)
    
    def emit_xor(self, dst, src, comment=""):
        self.backend.emit_xor(dst, src, comment)
    
    def emit_push(self, reg, comment=""): self.backend.emit_push(reg, comment)
    def emit_pop (self, reg, comment=""): self.backend.emit_pop (reg, comment)
    
    def emit_sub (self, reg, value, comment=""):
        self.backend.emit_sub(reg, value, comment)
    
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
    
    # de-dupplizierer - doppelte Zeichen ignorieren
    def add_string_literal(self, text):
        label = f"str_{len(self.string_literals)}"
        self.string_literals.append((label, text))

        if CDATA.args_backend == BACKEND_EXEFILE\
        or CDATA.args_backend == BACKEND_OBJFILE:
            
            target = CDATA.args_target.lower()
            
            if CDATA.args_target.lower() in ["dos", "dos16"]:
                self.writer.add_dos_string(label, text)
                return label
                
            elif target in ["win32", "win64", "winnt", "nt35"]:
                if not hasattr(self, "coff") or self.coff is None:
                    raise Exception("coff writer not installed")
                    
                if self.coff.find_symbol_index(label) is None:
                    self.coff.add_data_string(label, text)
                return label
                
            raise Exception("target not supported.")
        raise Exception("backend not supported.")
        
    def visit(self, tree):
        if tree is None:
            return None

        return super().visit(tree)
    
    def visitIncStatement(self, ctx):
        ref = ctx.variableRef()

        if ref is None:
            raise CompileError(ctx, "E0001", name="Inc")

        name = ref.IDENT().getText()

        info = self.lookup_var(name)
        typ  = self.resolve_type(info["type"])

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
        self.emit_load_var(ctx, name)

        if typ == "integer":
            self.emit_add("eax", "ebx")
            self.emit_store_var(ctx, name, "integer")
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
            self.emit_store_var(ctx, name, typ)

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

        info = self.lookup_var(name)
        typ  = self.resolve_type(info["type"])

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

        self.emit_load_var(ctx, name)

        if typ == "integer":
            self.emit_sub("eax", "ebx")
            self.emit_store_var(ctx, name, "integer")
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
            self.emit_store_var(ctx, name, typ)

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

        if arg.expr():
            return self.visit(arg.expr())

        if arg.STRING():
            value = arg.STRING().getText()[1:-1]
            label = self.add_string_literal(value)

            self.emit_mov("rax", label)

            if len(value) == 1:
                return "char"

            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_push("rax")
                self.emit_mov_imm("rax", "&_jit_dynstring_from_cstr")
                self.emit_call_rax()
                self.backend.emit_cleanup_stack(4)

                # Runtime kann ESI zerstören
                self.coff.emit_lea_reg_data_label("esi", "ctx")
            else:
                self.emit_mov("rcx", "rax")
                self.emit_mov_imm("rax", "&_jit_dynstring_from_cstr")
                self.emit_call_rax()

            return "string"

        raise CompileError(arg, "E0015", text=arg.getText())
    
    def visitSourceFile(self, ctx):
        if ctx.programFile():
            return self.visit(ctx.programFile())

        if ctx.unitFile():
            return self.visit(ctx.unitFile())
        
        if ctx.libraryFile():
            return self.visit(ctx.libraryFile())

        return None
    
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
        
        self.emit_push("r12")
        self.emit_push("rbx")
        self.emit_sub("rsp", 8, comment="align stack")
        self.emit_mov("r12", "rcx", comment="ctx")
        
        for init_label in self.unit_init_labels:
            self.emit_call_lbl(init_label, comment="unit init")
        
        for name, info in self.vars.items():
            if info["type"] in self.arrays:
                self.emit_init_array_var(ctx, name, info)
        
        self.visit(ctx.block())
        return self.render_cpp()
    
    def visitLibraryFile(self, ctx):
        self.program_name       = ctx.IDENT().getText()
        self.module_kind        = "library"
        self.module_kind_value  = 3

        if ctx.usesClause():
            self.visit(ctx.usesClause())

        for decl in ctx.declarationPart():
            if decl is not None:
                self.visit(decl)
        
        if ctx.exportsClause():
            self.visit(ctx.exportsClause())
            
        self.validate_class_methods(ctx)

        self.emit_push("r12")
        self.emit_push("rbx")
        self.emit_sub("rsp", 8, comment="align stack")
        self.emit_mov("r12", "rcx", comment="ctx")

        for init_label in self.unit_init_labels:
            self.emit_call_lbl(init_label, comment="unit init")

        for name, info in self.vars.items():
            if info["type"] in self.arrays:
                self.emit_init_array_var(ctx, name, info)

        self.visit(ctx.block())

        return self.render_cpp()
    
    def visitUnitFile(self, ctx):
        unit_name = ctx.qualifiedIdent().getText()
        unit_key  = self.normalize_unit_name(unit_name)
        old_unit  = self.current_unit
        
        old_kind        = self.module_kind
        old_kind_value  = self.module_kind_value
        
        self.module_kind        = "unit"
        self.module_kind_value  = 2
        
        self.current_unit       = unit_key

        self.visit(ctx.interfaceSection())
        self.visit(ctx.implementationSection())

        if ctx.unitInitBlock():
            safe_unit_name = self.normalize_unit_name(unit_name)

            init_label = self.new_named_label("unit_init_" + safe_unit_name)
            skip_label = self.new_named_label("skip_unit_init_" + safe_unit_name)

            self.unit_init_labels.append(init_label)

            self.emit_jmp(skip_label)
            self.emit_bind_label(init_label)
            self.visit(ctx.unitInitBlock())
            self.emit_ret()
            self.emit_bind_label(skip_label)

        self.module_kind        = old_kind
        self.module_kind_value  = old_kind_value
        self.current_unit       = old_unit
        
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
    
    def visitExitStatement(self, ctx):
        if not self.exit_label_stack:
            raise CompileError(ctx, "E0006")

        self.emit_jmp(self.exit_label_stack[-1], comment="Exit")
        return None
    
    def visitConstSection(self, ctx):
        for decl in ctx.constDeclaration():
            self.visit(decl)
        return None

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
        actual_types = []

        for arg in reversed(args):
            arg_type = self.visit_actual_param_expr(arg)
            actual_types.insert(0, arg_type)
            
            if arg_type == "integer":
                self.emit_movsxd("rax", "eax")
                self.emit_push("rax", comment="inherited integer arg")
            
            elif arg_type == "string":
                self.emit_push("rax", comment="inherited string arg")
            
            elif isinstance(arg_type, str) and arg_type.startswith("^"):
                self.emit_push("rax", comment="inherited pointer arg")
            
            else:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=f"unsupported inherited argument type {arg_type}"
                )
        
        method, owner_cls = self.find_class_method_recursive(
            ctx,
            cls.parent,
            method_name,
            actual_types
        )

        param_regs = ["rdx", "r8", "r9"]

        # Parameter 4..N bleiben als Stack-Parameter liegen
        stack_count = 0

        for index in range(len(args) - 1, 2, -1):
            stack_count += 1

        # Self laden
        self.emit_mov_qword_ptr("rcx", "rbp", -8, comment='inherited Self')

        # Parameter 1..3 aus temporärem Stack holen
        reg_count = min(3, len(args))

        for index in range(reg_count):
            self.emit_pop(param_regs[index], comment=f"inherited arg {index + 1}")

        align_pad = 0

        if stack_count % 2 == 1:
            self.emit_sub("rsp", 8, comment = "align stack before inherited call")
            align_pad = 8

        self.emit_call(method.label, comment = f"inherited {owner_cls.name}.{method.name}")

        if align_pad:
            self.emit_add("rsp", 8, comment = "remove inherited alignment padding")

        if stack_count > 0:
            self.emit_add("rsp", stack_count * 8, comment = "remove inherited stack args")

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
        
        self.emit_jmp(skip_label)
        self.emit_bind_label(method.label)
        
        # rcx = Self
        self.emit_push("rbp")
        self.emit_mov("rbp", "rsp")
        
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            # cdecl:
            # [ebp+4] = return address
            # [ebp+8] = Self
            self.emit_mov_dword_ptr("eax", "ebp", 8, comment="Self")
            self.emit_push("eax", comment="Self")
        else:
            # Win64:
            # rcx = Self
            self.emit_push("rcx", comment="Self")
        
        old_params = self.current_proc_params
        self.current_proc_params = {
            "self": {
                "type"          : "^" + class_key,
                "reg"           : "rcx",
                "stack_offset"  : -8,
                "is_var"        : False
            }
        }
        
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            for index, p in enumerate(params):
                pname = p["name"]
                ptype = self.resolve_type(p["type"])

                # Nach push rbp / mov rbp,rsp gilt:
                # [ebp+8]  = Self
                # [ebp+12] = Param 1
                # [ebp+16] = Param 2
                self.current_proc_params[pname.lower()] = {
                    "type": ptype,
                    "reg": None,
                    "stack_offset": 12 + index * 4,
                    "is_var": p.get("is_var", False)
                }
                
            self.emit_sub("esp", 256, comment="class method locals")
        else:
            param_regs = ["rdx", "r8", "r9"]

            for index, p in enumerate(params):
                pname = p["name"]
                ptype = self.resolve_type(p["type"])

                if index < len(param_regs):
                    reg = param_regs[index]
                    self.emit_push(reg, comment=f"save class method param {pname}")
                    stack_offset = -8 * (index + 2)
                else:
                    reg = None
                    stack_offset = 48 + ((index - len(param_regs)) * 8)

                self.current_proc_params[pname.lower()] = {
                    "type": ptype,
                    "reg": reg,
                    "stack_offset": stack_offset,
                    "is_var": p.get("is_var", False)
                }
        
            self.emit_sub("rsp", 256, comment = "class method locals")
        
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
        
        self.visit(ctx.block())

        self.current_class    = old_class
        self.current_method   = old_method
        self.current_function = old_function
        
        self.pop_const_scope()
        self.pop_local_scope()
        
        self.current_proc_params = old_params
        
        if method.kind == "function":
            rt = self.resolve_type(method.return_type)

            if rt == "string":
                if CDATA.args_target in ["nt35", "winnt", "win32"]:
                    self.emit_mov_dword_ptr("eax", "ebp", result_off)
                else:
                    self.emit_mov_qword_ptr("rax", "rbp", result_off)
                    
            elif rt == "integer":
                if CDATA.args_target in ["nt35", "winnt", "win32"]:
                    self.emit_mov_dword_ptr("eax", "ebp", result_off)
                else:
                    self.emit_mov_dword_ptr("eax", "rbp", result_off)
                    
            elif rt == "double":
                self.emit_movsd_load("xmm0", "rbp", result_off)
            else:
                raise CompileError(ctx, "E0005", got=rt, expected="integer/string/double")
        
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
    
    def visitBoolOrExpr(self, ctx):
        parts = list(ctx.boolXorExpr())

        if len(parts) == 1:
            return self.visit(parts[0])

        true_label = self.new_named_label("or_true")
        end_label  = self.new_named_label("or_end")

        for part in parts:
            expr_type = self.visit(part)

            if expr_type != "integer":
                raise CompileError(ctx, "E0005", got=expr_type, expected="boolean/integer")

            self.normalize_bool_eax()
            self.emit_cmp("eax", 0)
            self.emit_jne(true_label)

        self.emit_xor("eax", "eax")
        self.emit_jmp(end_label)

        self.emit_bind_label(true_label)
        self.emit_mov("eax", 1)

        self.emit_bind_label(end_label)

        return "integer"
    
    def visitBoolXorExpr(self, ctx):
        result_type = self.visit(ctx.boolAndExpr(0))

        for i in range(1, len(ctx.boolAndExpr())):
            if result_type != "integer":
                raise CompileError(ctx, "E0005", got=result_type, expected="boolean/integer")

            self.normalize_bool_eax()
            self.emit_push("rax")

            right_type = self.visit(ctx.boolAndExpr(i))

            if right_type != "integer":
                raise CompileError(ctx, "E0005", got=right_type, expected="boolean/integer")

            self.normalize_bool_eax()

            self.emit_pop("rbx")
            self.emit_mov("eax", "ebx")
            self.normalize_bool_eax()

            result_type = "integer"

        return result_type
    
    def visitBoolAndExpr(self, ctx):
        parts = list(ctx.compareExpr())

        if len(parts) == 1:
            return self.visit(parts[0])

        false_label = self.new_named_label("and_false")
        end_label   = self.new_named_label("and_end")

        for part in parts:
            expr_type = self.visit(part)

            if expr_type != "integer":
                raise CompileError(ctx, "E0005", got=expr_type, expected="boolean/integer")

            self.normalize_bool_eax()
            self.emit_cmp("eax", 0)
            self.emit_je(false_label)

        self.emit_mov("eax", 1)
        self.emit_jmp(end_label)

        self.emit_bind_label(false_label)
        self.emit_xor("eax", "eax")

        self.emit_bind_label(end_label)

        return "integer"

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
        left_type = self.visit(ctx.addExpr(0))

        if len(ctx.addExpr()) == 1:
            return left_type

        op = ctx.compareOp().getText()

        if left_type == "integer":
            self.emit_push("rax")
        elif isinstance(left_type, str) and left_type.startswith("^"):
            self.emit_push("rax")
        else:
            raise CompileError(ctx, "E0005", got=left_type, expected="integer/pointer")

        right_type = self.visit(ctx.addExpr(1))

        if isinstance(left_type, str) and left_type.startswith("^"):
            if right_type != left_type and right_type != "^nil":
                raise CompileError(ctx, "E0005", got=right_type, expected=left_type + "/nil")

            self.emit_mov("rbx", "rax")
            self.emit_pop("rax")
            self.emit_cmp("rax", "rbx")
        else:
            if right_type != "integer":
                raise CompileError(ctx, "E0005", got=right_type, expected="integer")

            self.emit_mov("ebx", "eax")
            self.emit_pop("rax")
            self.emit_cmp("eax", "ebx")

        true_label = self.new_named_label("cmp_true")
        end_label  = self.new_named_label("cmp_end")

        jump_map = {
            "=":  self.emit_je,
            "<>": self.emit_jne,
            "<":  self.emit_jl,
            "<=": self.emit_jle,
            ">":  self.emit_jg,
            ">=": self.emit_jge,
        }

        jump_map[op](true_label)
        self.emit_xor("eax", "eax")
        self.emit_jmp(end_label)
        self.emit_bind_label(true_label)
        self.emit_mov("eax", 1)
        self.emit_bind_label(end_label)

        return "integer"
    
    def visitRecordDeclaration(self, ctx):
        record_name = ctx.IDENT().getText()

        fields = []

        for field_ctx in ctx.recordFieldDeclaration():
            field_type = field_ctx.typeName().getText()

            for ident in field_ctx.identList().IDENT():
                fields.append((ident.getText(), field_type))

        self.declare_record(ctx, record_name, fields)
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
    
    def visitConstItem(self, ctx):
        name = ctx.IDENT().getText()
        value_text = ctx.constValue().getText()

        if value_text.startswith("'") and value_text.endswith("'"):
            value = value_text[1:-1]
            typ = "string"

        elif "." in value_text:
            value = value_text
            typ = "double"

        else:
            value = int(value_text)
            typ = "integer"

        self.declare_const(ctx, name, value, typ)
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
    
    def visitFunctionHeader(self, ctx):
        name    = ctx.IDENT().getText()
        scoped  = self.unit_scoped_name(name)
        key     = name.lower()

        if key not in self.functions:
            self.functions[key] = {
                "name"       : name,
                "scoped_name": scoped,
                "return_type": self.resolve_type(ctx.typeName().getText()),
                "label"      : None,
                "params"     : self.collect_formal_params(ctx)
            }
        
        # zusätzlich unqualifizierter Alias für uses
        self.functions[name.lower()] = self.functions[key]
        return None
    
    def visitProcedureHeader(self, ctx):
        name    = ctx.IDENT().getText()
        scoped  = self.unit_scoped_name(name)
        key     = name.lower()

        if key not in self.procedures:
            self.procedures[key] = {
                "name"       : name,
                "scoped_name": scoped,
                "label"      : None,
                "params"     : self.collect_formal_params(ctx)
            }
            
        self.procedures[name.lower()] = self.procedures[key]
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
    
    def visitClassDeclaration(self, ctx):
        class_name = ctx.IDENT().getText()
        
        fields     = []
        methods    = []
        properties = {}
        
        parent_name         = None
        current_visibility  = "public"
        
        if ctx.classParent():
            parent_name = ctx.classParent().IDENT().getText()
        
        for member in ctx.classBody().classMember():
            
            if member.visibilitySection():
                current_visibility = member.visibilitySection().getText().lower()
                continue
                
            if member.classFieldDeclaration():
                field_ctx = member.classFieldDeclaration()
                field_type = field_ctx.typeName().getText()
                
                for ident in field_ctx.identList().IDENT():
                    fields.append((ident.getText(), field_type, current_visibility))
            
            elif member.constructorDeclaration():
                ctor = member.constructorDeclaration()
                method_name = ctor.IDENT().getText()
                
                params  = self.collect_formal_params(ctor)
                mangled = self.fpc_mangle_class_method(
                    class_name,
                    method_name,
                    params,
                    self.current_unit if self.current_unit else self.program_name
                )
                
                methods.append({
                    "name"      : method_name,
                    "kind"      : "constructor",
                    "label"     : self.new_named_label("class_" + class_name + "_" + method_name),
                    "mangled"   : mangled,
                    "params"    : params,
                    "visibility": current_visibility
                })
            
            elif member.destructorDeclaration():
                dtor = member.destructorDeclaration()
                method_name = dtor.IDENT().getText()

                params  = self.collect_formal_params(dtor)
                mangled = self.fpc_mangle_class_method(
                    class_name,
                    method_name,
                    params,
                    self.current_unit if self.current_unit else self.program_name
                )

                methods.append({
                    "name"      : method_name,
                    "kind"      : "destructor",
                    "label"     : self.new_named_label("class_" + class_name + "_" + method_name),
                    "mangled"   : mangled,
                    "params"    : params,
                    "visibility": current_visibility
                })
            
            elif member.classFunctionDeclaration():
                fn = member.classFunctionDeclaration()
                method_name = fn.IDENT().getText()
                
                params  = self.collect_formal_params(fn)
                mangled = self.fpc_mangle_class_method(
                    class_name,
                    method_name,
                    params,
                    self.current_unit if self.current_unit else self.program_name
                )

                methods.append({
                    "name"       : method_name,
                    "kind"       : "function",
                    "label"      : self.new_named_label("class_" + class_name + "_" + method_name),
                    "mangled"    : mangled,
                    "params"     : params,
                    "return_type": self.resolve_type(fn.typeName().getText()),
                    "visibility" : current_visibility
                })
            
            elif member.classProcedureDeclaration():
                proc = member.classProcedureDeclaration()
                method_name = proc.IDENT().getText()
                
                params  = self.collect_formal_params(proc)
                mangled = self.fpc_mangle_class_method(
                    class_name,
                    method_name,
                    params,
                    self.current_unit if self.current_unit else self.program_name
                )

                methods.append({
                    "name"       : method_name,
                    "kind"       : "procedure",
                    "label"      : self.new_named_label("class_" + class_name + "_" + method_name),
                    "mangled"    : mangled,
                    "params"     : params,
                    "return_type": None,
                    "visibility" : current_visibility
                })
            
            elif member.propertyDeclaration():
                prop = member.propertyDeclaration()

                prop_name = prop.IDENT().getText()
                prop_type = self.resolve_type(prop.typeName().getText())

                read_name = None
                write_name = None

                for acc in prop.propertyAccessor():
                    acc_text = acc.getText().lower()
                    acc_name = acc.IDENT().getText()

                    if acc_text.startswith("read"):
                        read_name = acc_name
                    elif acc_text.startswith("write"):
                        write_name = acc_name

                properties[prop_name.lower()] = PropertyInfo(
                    name       = prop_name,
                    ptype      = prop_type,
                    visibility = current_visibility,
                    read_name  = read_name,
                    write_name = write_name
                )
        
        self.declare_class(
            ctx,
            class_name,
            fields,
            methods,
            properties,
            parent_name=parent_name
        )
        return None
    
    def visitTypeDeclaration(self, ctx):
        if ctx.enumDeclaration():
            return self.visit(ctx.enumDeclaration())
        
        if ctx.recordDeclaration():
            return self.visit(ctx.recordDeclaration())
        
        if ctx.arrayDeclaration():
            return self.visit(ctx.arrayDeclaration())
        
        if ctx.classDeclaration():
            return self.visit(ctx.classDeclaration())
        
        type_name  = ctx.IDENT().getText()
        alias_name = ctx.typeName().getText()
        
        self.declare_type_alias(ctx, type_name, alias_name)
        return None
    
    def visitFunctionDeclaration(self, ctx):
        name = ctx.IDENT().getText()

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
            "params": params
        }

        # globaler Alias, damit "Add" gefunden wird
        self.functions[name.lower()] = self.functions[key]

        old_function = self.current_function
        self.emit_function_declaration(ctx, scoped, return_type)
        self.current_function = old_function
        
        return None
    
    def visitAssignment(self, ctx):
        target_ctx = ctx.variableRef()
        target     = target_ctx.getText()
        expr_type  = self.visit(ctx.expr())

        if target.lower() == "result":
            self.emit_store_result(ctx, expr_type)
            return None
        
        if "." not in target and "[" not in target and "^" not in target:
            if self.emit_store_self_field(ctx, target, expr_type):
                return None
        
        param = self.find_param(target)
        if param and param.get("is_var", False):
            self.emit_store_param(ctx, target, expr_type)
            return None
        
        suffixes = target_ctx.variableSuffix()
        if suffixes:
            first     = suffixes[0]
            has_caret = any(s.CARET() for s in suffixes)
            has_dot   = any(s.DOT()   for s in suffixes)
            
            if has_caret and has_dot:
                parts = [target_ctx.IDENT().getText()]
                
                after_caret = False
                for s in suffixes:
                    if s.CARET():
                        after_caret = True
                        continue
                    
                    if after_caret and s.DOT():
                        parts.append(s.IDENT().getText())
                
                self.emit_store_pointer_record_field(ctx, parts, expr_type)
                return None
                
            if first.CARET():
                var_name = target_ctx.IDENT().getText()
                self.emit_store_pointer_deref(ctx, var_name, expr_type)
                return None
            
            if first.LBRACK():
                var_name = target_ctx.IDENT().getText()
                
                index_exprs, rest_suffixes = self.collect_array_suffix_exprs(suffixes)
                
                # dynamisches Array: a[0] := ...
                arr_info = self.var_info(ctx, var_name)
                arr_type = arr_info["type"]
                
                # String-Index
                if arr_type == "string":
                    self.emit_store_string_char(
                        ctx,
                        var_name,
                        index_exprs,
                        expr_type
                    )
                    return None
                
                # points[0].X
                if rest_suffixes and rest_suffixes[0].DOT():
                    field_parts = []

                    for s in rest_suffixes:
                        if s.DOT():
                            field_parts.append(s.IDENT().getText())

                    var_info, array_info = self.get_array_info(ctx, var_name)

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
                
                # dynamisches Array: a[0] := ...
                if getattr(arr_type, "is_dynamic", False):
                    self.emit_store_dynamic_array_element(
                        ctx,
                        var_name,
                        index_exprs,
                        expr_type
                    )
                    return None
                
                # statisches Array: a[0] := ...
                self.emit_store_array_element(
                    ctx,
                    var_name,
                    index_exprs,
                    expr_type
                )
                return None
            
            if first.DOT():
                parts = [target_ctx.IDENT().getText()]

                for s in suffixes:
                    if s.DOT():
                        parts.append(s.IDENT().getText())

                var_name = parts[0]
                var_info = self.var_info(ctx, var_name)
                var_type = self.resolve_type(var_info["type"])

                # Klasse: foo.field := ...
                if isinstance(var_type, str) and var_type in self.classes:
                    if self.emit_store_class_property(ctx, parts, expr_type):
                        return None
                    
                    self.emit_store_class_field(ctx, parts, expr_type)
                    return None
                
                # Record: rec.field := ...
                self.emit_store_record_field(ctx, parts, expr_type)
                return None
        
        if self.find_const(target):
            raise CompileError(ctx, "E0010", name=target)
        
        local_var = self.find_local_var(target)
        if local_var:
            self.emit_store_local_var(ctx, target, expr_type)
            return None
        
        var_info = self.var_info(ctx, target)
        var_type = var_info["type"]
        
        if isinstance(var_type, str) and var_type.startswith("^"):
            if expr_type == var_type or expr_type == "^nil":
                self.emit_store_var(ctx, target, var_info)
                return None
        
        if var_type in self.classes:
            if expr_type != var_type:
                raise CompileError(ctx, "E0005", got=expr_type, expected=var_type)
            
            self.emit_store_object_var(ctx, target, var_info)
            return None
        
        if var_type == "double" and expr_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")
            expr_type = "double"
            
        if var_type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=var_type)

        self.emit_store_var(ctx, target, var_info)
        return None
    
    def visitExpr(self, ctx):
        return self.visit(ctx.boolOrExpr())
    
    def visitAddExpr(self, ctx):
        result_type = self.visit(ctx.term(0))

        for i in range(1, len(ctx.term())):
            op = ctx.getChild(2 * i - 1).getText()

            # String-Verkettung nur mit +
            if result_type == "string":
                if op != "+":
                    raise CompileError(ctx, "E0005", got="string -", expected="string + string")

                self.emit_push("rax", comment='save left string')

                right_type = self.visit(ctx.term(i))

                if right_type != "string":
                    raise CompileError(ctx, "E0005", got=right_type, expected="string")

                self.emit_mov("rdx", "rax", comment="right string")
                self.emit_pop(rcx         , comment="left string")
                self.emit_mov_imm("rax", "&_jit_dynstring_concat")
                self.emit_call_rax()

                result_type = "string"
                continue

            if result_type == "integer":
                self.emit_push("rax")

                right_type = self.visit(ctx.term(i))

                # 'test' + S
                if right_type == "string":
                    if op != "+":
                        raise CompileError(ctx, "E0005", got="integer/string", expected="string + string")

                    self.emit_mov("rdx", "rax", comment = "right string")
                    self.emit_pop("rcx"       , comment = "left string/char literal")

                    self.emit_mov_imm("rax", "&_jit_dynstring_concat")
                    self.emit_call_rax()

                    result_type = "string"
                    continue

                if right_type == "integer":
                    self.emit_mov("ebx", "eax")
                    self.emit_pop("rax")

                    if op == "+":
                        self.emit_add("eax", "ebx")
                    elif op == "-":
                        self.emit_sub("eax", "ebx")

                    result_type = "integer"
                    continue

                self.emit_pop("rax")
                self.emit_cvtsi2sd("xmm1", "eax")
                result_type = "double"

            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")

            right_type = self.visit(ctx.term(i))

            if right_type == "integer":
                self.emit_cvtsi2sd("xmm0", "eax")

            self.emit_movsd_load("xmm1", "rsp", 0)
            self.emit_add("rsp", 8)

            if op == "+":
                self.emit_addsd("xmm0", "xmm1")
            elif op == "-":
                self.emit_movapd("xmm2", "xmm0")
                self.emit_movapd("xmm0", "xmm1")
                self.emit_subsd("xmm0", "xmm2")

            result_type = "double"

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
    ## ääää
    def emit_address_of_array_element(self, ctx, var_name, index_expr_ctx):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]

        var_info, array_info = self.get_array_info(ctx, var_name)

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        self.emit_imul("eax", "eax", array_info.element_size)
        self.emit_add("eax", var_info["slot"])

        self.emit_mov_qword("r11", "r12", "arrays_vars")
        self.emit_movsxd("rax", "eax")
        self.emit_add("r11", "rax")

        # Ergebnis von @A[i]
        self.emit_mov("rax", "r11")

        return "^" + array_info.element_type
    
    def visitFactor(self, ctx):
        text = ctx.getText()
        key  = text.lower()
        
        if ctx.MINUS():
            expr_type = self.visit(ctx.factor())

            if expr_type == "integer":
                self.emit_mov("ebx", "eax")
                self.emit_xor("eax", "eax")
                self.emit_sub("eax", "ebx")
                return "integer"

            if expr_type == "double":
                # 0.0 - xmm0
                self.emit_sub("rsp", 8)
                self.emit_movsd_store("rsp", 0, "xmm0")

                self.emit_mov("eax", 0)
                self.emit_cvtsi2sd("xmm0", "eax")

                self.emit_movsd_load("xmm1", "rsp", 0)
                self.emit_add("rsp", 8)

                self.emit_subsd("xmm0", "xmm1")
                return "double"

            raise CompileError(ctx, "E0005", got=expr_type, expected="integer/double")

        if ctx.PLUS():
            return self.visit(ctx.factor())
        
        if ctx.NOT():
            expr_type = self.visit(ctx.factor())
            
            if expr_type != "integer":
                raise CompileError(ctx, "E0005", got=expr_type, expected="boolean/integer")
                
            self.normalize_bool_eax()
            self.emit_xor("eax", 1, comment = "not")
            return "integer"
        
        if key in self.constants:
            c = self.constants[key]
            
            if c["type"] == "integer":
                self.emit_mov("eax", f"{c['value']}")
                return "integer"
                
            if c["type"] == "double":
                return self.emit_load_double_literal(c["value"])
                
            if c["type"] == "string":
                label = self.add_string_literal(c["value"])
                if CDATA.args_target in ["dos", "dos16"]:
                    self.backend.writer.emit_mov_dx_label(label)
                    return "string"
                else:
                    self.emit_mov_imm("rax", label)
                    return "string"
        
        if ctx.AT():
            ref = ctx.variableRef()
            name = ref.IDENT().getText()
            suffixes = ref.variableSuffix()
            
            if suffixes:
                first = suffixes[0]
                
                if first.LBRACK():
                    index_exprs, rest_suffixes = self.collect_array_suffix_exprs(suffixes)
                    return self.emit_address_of_array_element(
                        ctx,
                        name,
                        index_exprs
                    )
            
            return self.emit_address_of_var(ctx, name)
        
        # Function call zuerst
        if ctx.functionCallExpr():
            return self.visit(ctx.functionCallExpr())
        
        if ctx.variableRef():
            ref      = ctx.variableRef()
            suffixes = ref.variableSuffix()
            name     = ref.IDENT().getText()

            if not suffixes:
                self_field_type = self.emit_load_self_field(ctx, name)
                if self_field_type is not None:
                    return self_field_type
            
            if suffixes:
                first     = suffixes[0]
                has_caret = any(s.CARET() for s in suffixes)
                has_dot   = any(s.DOT()   for s in suffixes)
                
                if has_caret and has_dot:
                    parts = [ref.IDENT().getText()]
                    
                    after_caret = False
                    for s in suffixes:
                        if s.CARET():
                            after_caret = True
                            continue
                        
                        if after_caret and s.DOT():
                            parts.append(s.IDENT().getText())
                    
                    return self.emit_load_pointer_record_field(ctx, parts)
                
                if first.CARET():
                    var_name = ref.IDENT().getText()
                    return self.emit_load_pointer_deref(ctx, var_name)
                
                if first.LBRACK():
                    var_name = ref.IDENT().getText()
                    var_info = self.var_info(ctx, var_name)
                    var_type = var_info["type"]
                    
                    index_exprs, rest_suffixes = self.collect_array_suffix_exprs(suffixes)
                    
                    # Spezialfall: s[0] = ganzer String
                    if var_type == "string":
                        index_exprs = list(first.expr())
                        
                        if len(index_exprs) == 1 and index_exprs[0].getText() == "0":
                            self.emit_load_var(var_name, var_info)   # RAX = char*
                            return "string"
                        
                        return self.emit_load_string_char(
                            ctx,
                            var_name,
                            index_exprs
                        )
                    
                    # points[0].X
                    if rest_suffixes and rest_suffixes[0].DOT():
                        field_parts = []
                        
                        for s in rest_suffixes:
                            if s.DOT():
                                field_parts.append(s.IDENT().getText())
                        
                        var_info, array_info = self.get_array_info(ctx, var_name)
                        
                        if getattr(array_info, "is_dynamic", False):
                            return self.emit_load_dynamic_array_record_field(
                                ctx,
                                var_name,
                                index_exprs,
                                field_parts
                            )
                        
                        return self.emit_load_array_record_field(
                            ctx,
                            var_name,
                            index_exprs,
                            field_parts
                        )
                    
                    # normales a[0]
                    return self.emit_load_array_element(
                        ctx,
                        var_name,
                        index_exprs
                    )
                
                if first.DOT():
                    parts = [ref.IDENT().getText()]
                    
                    for s in suffixes:
                        if s.DOT():
                            parts.append(s.IDENT().getText())
                    
                    # TFoo.Create
                    if len(parts) == 2:
                        class_name  = parts[0]
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
                    var_info = self.var_info(ctx, var_name)
                    var_type = self.resolve_type(var_info["type"])
                    
                    if isinstance(var_type, str) and var_type in self.classes:
                        prop_type = self.emit_load_class_property(ctx, parts)
                        if prop_type:
                            return prop_type
                        return self.emit_load_class_field(ctx, parts)
                    return self.emit_load_record_field(ctx, parts)
            
            name = ref.IDENT().getText()
            
            local_var = self.find_local_var(name)
            if local_var:
                return self.emit_load_local_var(ctx, name, local_var)
            
            param = self.find_param(name)
            if param:
                return self.emit_load_param(ctx, name)
            
            const_info = self.find_const(name)
            if const_info:
                return self.emit_load_const(ctx, name)
            
            key = name.lower()
            if key in self.vars:
                info = self.var_info(ctx, name)
                self.emit_load_var(name, info)
                return info["type"]
            
            if self.current_class is not None:
                try:
                    return self.emit_self_method_call(ctx, name, [])
                except CompileError:
                    pass
            
            func = self.find_function(name)
            if func:
                params = func.get("params", [])
                
                if len(params) == 0:
                    self.emit_sub("rsp", 32, comment = "shadow space for parameterless function call")
                    self.emit_call(f"{func['label']}")
                    self.emit_add("rsp", 32)
                    return func["return_type"].lower()
                
                raise CompileError(ctx, "E0005", got="0", expected=str(len(params)))
            
            raise CompileError(ctx, "E0001", name=name)
        
        # Klammerausdruck nur wenn wirklich vorhanden
        expr_list = ctx.expr()
        if expr_list:
            if isinstance(expr_list, list):
                if len(expr_list) > 0:
                    return self.visit(expr_list[0])
            else:
                return self.visit(expr_list)
        
        if ctx.NIL():
            self.emit_xor("rax", "rax", comment = "nil")
            return "^nil"
        
        # Integer
        if ctx.NUMBER():
            value = ctx.NUMBER().getText()
            self.emit_mov_imm("eax", value)
            #self.emit(f"a.mov(x86::eax, {value});")
            return "integer"
        
        # Double
        if ctx.FLOATNUMBER():
            value = ctx.FLOATNUMBER().getText()
            return self.emit_load_double_literal(value)
        
        # String
        if ctx.STRING():
            value = ctx.STRING().getText()[1:-1]
            label = self.add_string_literal(value)

            if CDATA.args_target in ["dos", "dos16"]:
                self.backend.writer.emit_mov_dx_label(label)
                if len(value) == 1:
                    return "char"
                return "string"

            elif CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_mov_imm("rax", label)
                if len(value) == 1:
                    return "char"
                return "string"
            
            self.emit_mov_imm("rax", label)
            
            if len(value) == 1:
                return "char"
                
            self.emit_mov("rcx", "rax")
            self.emit_mov_imm("rax", "&_jit_dynstring_from_cstr")
            self.emit_call_rax()

            return "string"
        
        # Identifier
        if ctx.IDENT():
            name = ctx.IDENT().getText()
            
            local_var = self.find_local_var(name)
            if local_var:
                return self.emit_load_local_var(ctx, name, local_var)
            
            param = self.find_param(name)
            if param:
                return self.emit_load_param(ctx, name)
            
            self_field_type = self.emit_load_self_field(ctx, name)
            if self_field_type is not None:
                return self_field_type
            
            const_info = self.find_const(name)
            if const_info:
                return self.emit_load_const(ctx, name)
            
            key = name.lower()
            if key in self.vars:
                info = self.var_info(ctx, name)
                self.emit_load_var(name, info)
                return info["type"]
            
            func      = self.find_function(name)
            local_var = self.find_local_var(name)
            
            if local_var:
                return self.emit_load_local_var(ctx, name, local_var)
            
            param = self.find_param(name)
            if param:
                return self.emit_load_param(name)
            
            # globale Variable
            key = name.lower()
            if key in self.vars:
                info = self.var_info(ctx, name)
                self.emit_load_var(name, info)
                return info["type"]
            
            if self.current_class is not None:
                try:
                    return self.emit_self_method_call(ctx, name, [])
                except CompileError:
                    pass
            
            # parameterlose Funktion ohne Klammern:
            func = self.find_function(name)
            if func:
                params = func.get("params", [])
                
                if len(params) == 0:
                    self.emit_sub("rsp", 32, comment = "shadow space for parameterless function call")
                    self.emit_call(f"{func['label']}")
                    self.emit_add("rsp", 32)
                    return func["return_type"].lower()
                
                raise CompileError(ctx, "E0005", got="0", expected=str(len(params)))
            
            raise CompileError(ctx, "E0001", name=name)
        
        raise CompileError(ctx, "E0015", text=text)
    
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

        var_info = self.var_info(ctx, name)
        var_type = self.resolve_type(var_info["type"])

        if isinstance(var_type, str) and var_type in self.arrays:
            array_info = self.arrays[var_type]

            # Dynamische Arrays: immer 0
            if getattr(array_info, "is_dynamic", False):
                self.emit_mov("eax", 0)
                return "integer"

            # Statische Arrays: index_min
            self.emit_mov("eax", array_info.index_min)
            return "integer"

        raise CompileError(ctx, "E0005", got=var_type, expected="array")

    def emit_builtin_high(self, ctx):
        arg_ctx = self.get_single_builtin_arg(ctx)
        name = arg_ctx.getText()

        var_info = self.var_info(ctx, name)
        var_type = self.resolve_type(var_info["type"])

        if isinstance(var_type, str) and var_type in self.arrays:
            array_info = self.arrays[var_type]

            # Dynamische Arrays:
            # High(A) = Length(A) - 1
            if getattr(array_info, "is_dynamic", False):
                self.emit_builtin_length(ctx)
                self.emit_sub("eax", 1)
                return "integer"

            # Statische Arrays
            self.emit_mov("eax", array_info.index_max)
            return "integer"

        raise CompileError(ctx, "E0005", got=var_type, expected="array")
    
    def visitFunctionCallExpr(self, ctx):
        names  = list(ctx.functionName())

        if not names:
            raise CompileError(ctx, "E0015", text=ctx.getText())
        
        name = names[0].getText()
        
        if len(names) >= 2:
            left_name   = names[0].getText()
            method_name = names[1].getText()

            if method_name.lower() == "create":
                return self.emit_class_constructor_call(
                    ctx,
                    left_name,
                    method_name
                )
            name = method_name
        
        key  = name.lower()
        
        self.builtin_functions = {
            "assigned": self.emit_builtin_assigned,
            "length": self.emit_builtin_length,
            "low": self.emit_builtin_low,
            "high": self.emit_builtin_high,
            "copy": self.emit_builtin_copy,
            "pos": self.emit_builtin_pos,
        
            "blake2": self.emit_builtin_blake2,
            "blake3": self.emit_builtin_blake3,
            "crc16": self.emit_builtin_crc16,
            "crc32": self.emit_builtin_crc32,
            "crc32c": self.emit_builtin_crc32c,
            "crc64": self.emit_builtin_crc64,
            "md5": self.emit_builtin_md5,
            "sha1": self.emit_builtin_sha1,
            "sha3": self.emit_builtin_sha3,
            "sha224": self.emit_builtin_sha224,
            "sha256": self.emit_builtin_sha256,
            "sha384": self.emit_builtin_sha384,
            "sha512": self.emit_builtin_sha512,
            
            "diskfree": self.emit_builtin_diskfree,
            "disktotal": self.emit_builtin_disktotal,
            "disklabel": self.emit_builtin_disklabel,
            "diskserial": self.emit_builtin_diskserial,
            "diskfilesystem": self.emit_builtin_diskfilesystem,
            "disktype": self.emit_builtin_disktype,
            "diskshare": self.emit_builtin_diskshare,
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

        int_regs = ["ecx", "edx", "r8d", "r9d"]

        for index, arg_expr in enumerate(actuals):
            formal = params[index]

            if formal["type"] == "integer":
                expr_type = self.visit(arg_expr)

                if expr_type != "integer":
                    raise CompileError(ctx, "E0005", got=expr_type, expected="integer")

                self.emit_mov(int_regs[index], "eax")
            else:
                raise CompileError(ctx, "E0005", got=formal["type"], expected="integer")

        self.emit_sub("rsp", 32, comment = "shadow space for function call")
        self.emit_call_lbl(func["label"])
        self.emit_add("rsp", 32)

        return func["return_type"].lower()
    
    def visitProcedureDeclaration(self, ctx):
        name = ctx.IDENT().getText()
        key  = name.lower()

        label      = self.new_named_label("proc_"     + name)
        skip_label = self.new_named_label("skipproc_" + name)
        exit_label = self.new_named_label("exitproc_" + name)

        params = self.collect_formal_params(ctx)

        self.procedures[key] = {
            "name"  : name,
            "label" : label,
            "params": params
        }

        param_regs = ["rcx", "rdx", "r8", "r9"]
        
        if len(params) > 64:
            raise CompileError(ctx, "E0005", got=str(len(params)), expected="max 64 params")
            
        #if len(params) > len(param_regs):
        #    raise CompileError(ctx,
        #        "E0005",
        #        got="too many params",
        #        expected="max 4 params")
        
        self.emit_jmp(skip_label)
        self.emit_bind_label(label)
        
        # external coff .o file label
        self.backend.writer.add_symbol_alias(
            "_" + name.lower(),
            label
        )
        
        self.emit_push("rbp")
        self.emit_mov("rbp", "rsp")
        
        old_params = self.current_proc_params
        self.current_proc_params = {}
        
        #for index, p in enumerate(params):
        #    reg = param_regs[index]
        #    pname = p["name"]
        #    self.emit_push(reg, comment=f"save param {pname}")
        #    
        #    self.current_proc_params[p["name"].lower()] = {
        #        "type": p["type"],
        #        "reg": param_regs[index],
        #        "stack_offset": -8 * (index + 1),
        #        "is_var": p.get("is_var", False)
        #    }
        
        for index, p in enumerate(params):
            pname = p["name"]
            ptype = self.resolve_type(p["type"])
            
            
            if index < 4:
                reg = param_regs[index]
                self.emit_push(reg, comment=f"save param {pname}")
                stack_offset = -8 * (index + 1)
            else:
                reg = None
                stack_offset = 48 + ((index - 4) * 8)

            self.current_proc_params[pname.lower()] = {
                "type": ptype,
                "reg": reg,
                "stack_offset": stack_offset,
                "is_var": p.get("is_var", False)
            }
        
        saved_param_count = min(len(params), 4)
        
        if saved_param_count % 2 == 1:
            self.emit_sub("rsp", 8, comment = "align stack after odd param saves")
    
        self.emit_sub("rsp", 512, comment = "local variables")
        
        self.exit_label_stack.append(exit_label)
        self.push_local_scope()
        
        saved_param_count = min(len(params), 4)
        self.current_local_scope()["next_offset"] = saved_param_count * 8
        
        block_ctx = ctx.block()
        if block_ctx is None:
            raise CompileError(ctx, "E0015", text="procedure block missing")

        self.visit(block_ctx)
        
        self.pop_local_scope()
        self.exit_label_stack.pop()
        
        self.emit_bind_label(exit_label)
        self.current_proc_params = old_params
        
        self.emit_mov("rsp", "rbp")
        self.emit_pop("rbp")
        self.emit_ret()
        
        self.emit_bind_label(skip_label)
        return None
    
    def visitProcedureCallStatement(self, ctx):
        idents     = list(ctx.IDENT())
        name       = idents[0].getText()
        key        = name.lower()
        param_regs = ["rcx", "rdx", "r8", "r9"]

        if ctx.DOT():
            obj_name    = idents[0].getText()
            method_name = idents[1].getText()

            if method_name.lower() == "free":
                return self.emit_class_free_call(ctx, obj_name)
                
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
        
        func = self.find_function(name)
        if func:
            params = func.get("params", [])

            actuals = []
            if ctx.actualParamList():
                actuals = list(ctx.actualParamList().actualParam())

            if len(actuals) != len(params):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=str(len(actuals)),
                    expected=str(len(params))
                )

            # Für jetzt: parameterlose Funktion als Statement erlauben.
            if len(params) == 0:
                if CDATA.args_target in ["dos", "dos16"]:
                    self.emit_call_lbl(func["label"])
                else:
                    self.emit_sub("rsp", 32)
                    self.emit_call_lbl(func["label"])
                    self.emit_add("rsp", 32)

                return None

            raise CompileError(
                ctx,
                "E0019",
                text="function calls with parameters as statement not supported yet"
            )
        
        if key not in self.procedures:
            raise CompileError(ctx, "E0001", name=name)
        
        proc    = self.procedures[key]
        params  = proc["params"]
        actuals = []
        
        if ctx.actualParamList():
            actuals = list(ctx.actualParamList().actualParam())
        
        if len(actuals) != len(params):
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected=str(len(params)))
        
        def emit_push_argument(index):
            arg         = actuals[index]
            formal      = params[index]
            formal_type = self.resolve_type(formal["type"])

            if formal.get("is_var", False):
                ref = self.actual_param_variable_ref(ctx, arg)

                if ref is None:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got="expression",
                        expected="addressable variable"
                    )

                # einfache Variable: Head
                var_name = ref.IDENT(0).getText()

                info = self.find_local_var(var_name)
                if info is None:
                    info = self.var_info(ctx, var_name)

                actual_type = self.resolve_type(info["type"])

                if actual_type != formal_type:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got      = actual_type,
                        expected = formal_type
                    )

                self.emit_address_of_var(ctx, var_name)
                self.emit_push("rax", comment='var parameter')
                return

            expr_type = self.visit_actual_param_expr(arg)

            if formal_type == "integer":
                if expr_type != "integer":
                    raise CompileError(ctx, "E0005", got=expr_type, expected="integer")

                self.emit_movsxd("rax", "eax")
                self.emit_push("rax", comment = "integer parameter")
                return

            if formal_type == "string":
                if expr_type != "string":
                    raise CompileError(ctx, "E0005", got=expr_type, expected="string")

                self.emit_push("rax", comment='string parameter')
                return

            if isinstance(formal_type, str) and formal_type.startswith("^"):
                if expr_type != formal_type and expr_type != "^nil":
                    raise CompileError(ctx, "E0005", got=expr_type, expected=formal_type)

                self.emit_push("rax", comment='pointer parameter')
                return

            raise CompileError(ctx, "E0005", got=formal_type, expected="integer/string/pointer")

        # Parameter 5..N rückwärts auf Stack legen
        stack_count = 0
        for index in range(len(actuals) - 1, 3, -1):
            emit_push_argument(index)
            stack_count += 1

        # Parameter 1..4 rückwärts auswerten und temporär sichern
        reg_count = min(4, len(actuals))
        for index in range(reg_count - 1, -1, -1):
            emit_push_argument(index)

        for index in range(reg_count):
            self.emit_pop(param_regs[index], comment=f"load parameter {index + 1}")

        align_pad = 0

        if stack_count % 2 == 1:
            self.emit_sub("rsp", 8, comment="align stack before procedure call")
            align_pad = 8

        self.emit_sub("rsp", 32, comment = "Windows x64 shadow space")
        self.emit_call(f"{proc['label']}")
        self.emit_add("rsp", 32)

        if align_pad:
            self.emit_add("rsp", 8, comment = "remove stack alignment padding")

        if stack_count > 0:
            self.emit_add(f"rsp", {stack_count * 8}, comment = "remove stack parameters")

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
                        pname = arg.expr().getText().lower()
                        pinfo = self.current_proc_params[pname]
                        
                        if pinfo["type"] == "integer":
                            offset = pinfo["stack_offset"]
                            self.emit_mov_dword_ptr("eax", "rbp", offset, comment=f"load integer parameter")
                            self.emit_mov("ecx", "eax")
                            self.emit_mov_imm("rax", "&_jit_print_int")
                            self.emit_call_rax()
                            continue
                            
                        if pinfo["type"] == "string":
                            offset = pinfo["stack_offset"]
                            self.emit_mov_qword_ptr("rax", "rbp", offset, comment="load string parameter")

                            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                                self.emit_push("rax")
                                self.emit_nt32_call_cdecl("_jit_print_text", 4)
                            else:
                                self.emit_mov("rcx", "rax")
                                self.emit_mov_imm("rax", "&_jit_print_text")
                                self.emit_call_rax()

                            continue
                    
                    expr_type = self.visit(arg.expr())
                    
                    if expr_type == "char":
                        self.emit_mov("ecx", "eax")
                        self.emit_mov_imm("rax", "&_jit_print_char")
                        self.emit_call_rax()
                    
                    if expr_type == "string":
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
                    
                    if expr_type == "integer":
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
            "nil_pointer_error",
            "out_of_memory_error",
            "array_bounds_error",
            "string_range_error",
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
class GeneratorClass(AsmJitGenerator):
    def __init__(self, backend, writer=None):
        super().__init__(backend)
        self.writer = None
        self.coff   = None

        if writer is None:
            raise RuntimeError("generator writer invalid")

        self.writer = writer

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
        self.emit_mov("eax", "ebx")

    def emit_mov_ebx_eax(self):
        self.emit_mov("ebx", "eax")

    def collect_array_suffix_exprs(self, suffixes):
        index_exprs = []
        rest_suffixes = []

        in_array_part = True

        for s in suffixes:
            if in_array_part and s.LBRACK():
                index_exprs.extend(list(s.expr()))
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
        self.module_kind  = "program"
        self.module_kind_value = 1

        dos_main_label = None
        if ((CDATA.args_backend == BACKEND_OBJFILE or CDATA.args_backend == BACKEND_EXEFILE)
            and CDATA.args_target.lower() in ["dos", "dos16"]):
            dos_main_label = "__dos_main_start"
            self.writer.emit_jmp(dos_main_label)

        if ctx.usesClause():
            self.visit(ctx.usesClause())

        for decl in ctx.declarationPart():
            if decl is not None:
                self.visit(decl)

        self.validate_class_methods(ctx)

        if  CDATA.args_backend == BACKEND_OBJFILE\
        or  CDATA.args_backend == BACKEND_EXEFILE:
            if CDATA.args_target.lower() in ["win32", "win64", "nt35", "winnt"]:
                self.finalize_coff_context()
                self.writer.begin_function("_main", local_size=0)
                
                target = CDATA.args_target.lower()
                
                if target in ["winnt", "nt35", "win32"]:
                    # NT32: kein r12, kein Win64-Context, kein Shadow-Space
                    self.writer.emit_lea_reg_data_label("esi", "ctx")
                else:
                    self.emit_push("r12")
                    self.emit_push("rbx")
                    self.emit_sub("rsp", 8)

                    # PE-EXE hat keinen JIT-Aufrufer, also ctx direkt laden:
                    self.writer.emit_lea_reg_data_label("r12", "ctx")
        
            elif CDATA.args_target.lower() in ["dos", "dos16"]:
                self.writer.bind_label(dos_main_label)
                self.writer.emit_startup()
                self.backend.emit_heap_init(0x40)

        for init_label in self.unit_init_labels:
            self.emit_call_lbl(init_label)

        for name, info in self.vars.items():
            if info["type"] in self.arrays:
                self.emit_init_array_var(ctx, name, info)

        self.visit(ctx.block())

        if  CDATA.args_backend == BACKEND_OBJFILE\
        or  CDATA.args_backend == BACKEND_EXEFILE:
            target = CDATA.args_target.lower()

            if target in ["winnt", "nt35", "win32"]:
                # NT32 / PE32: stdcall, Parameter per Stack
                self.writer.emit_push_imm32(0)
                self.writer.emit_call_external("ExitProcess")
                self.writer.end_function()

            elif target == "win64":
                self.emit_mov("ecx", 0)
                self.writer.emit_runtime_call("ExitProcess")
                self.writer.end_function()
    
            elif target in ["dos", "dos16"]:
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
