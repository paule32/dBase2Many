# ---------------------------------------------------------------------------
# File:   pascal2asmjit.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
import sys
import os

from datetime    import datetime
from dataclasses import dataclass
from antlr4      import *

from parsers.pascal.MiniPascalLexer          import MiniPascalLexer
from parsers.pascal.MiniPascalParser         import MiniPascalParser
from parsers.pascal.MiniPascalParserVisitor  import MiniPascalParserVisitor

# ---------------------------------------------------------------------------
# used error code to information text map ...
# ---------------------------------------------------------------------------
ERROR_MAP = {
    "E0001": "Identifier not found: {name}",
    "E0002": "Duplicate identifier: {name}",
    "E0003": "Variable not declared: {name}",
    "E0004": "Unknown type: {name}",
    "E0005": "Incompatible types: got {got}, expected {expected}",
    "E0006": "Illegal assignment",
    "E0007": "Variable identifier expected",
    "E0008": "Unknown type",
    "E0009": "Duplicate variable declaration",
    "E0010": "Constant cannot be assigned",
    "E0011": "Unsupported local variable type: {typ}",
    "E0012": "Local variable not found: {name}",
    "E0013": "Unsupported assignment type: {var_type}",
    "E0014": "Unsupported variable type: {var_type}",
    "E0015": "Unsupported factor: {text}",
    "E0016": "Duplicate enum type: {name}",
    "E0017": "Duplicate enum value: {value_name}",
    "E0018": "Enum value name expected"
}

COMMENT_REPL = ('-' * 77)

# ---------------------------------------------------------------------------
# data classes as record workaround ...
# ---------------------------------------------------------------------------
@dataclass
class EnumInfo:
    name: str
    values: dict[str, int]

@dataclass
class RecordFieldInfo:
    name: str
    type: str
    offset: int
    size: int

@dataclass
class RecordInfo:
    name: str
    fields: dict[str, RecordFieldInfo]
    size: int

@dataclass
class ArrayInfo:
    name        : str
    index_min   : int
    index_max   : int
    element_type: str
    element_size: int
    size        : int
    init_values : list
    dimensions  : list

# ---------------------------------------------------------------------------
# Compiler Exception to mark errors in compilation unit ...
# ---------------------------------------------------------------------------
class CompileError(Exception):
    def __init__(self, ctx, code, **params):
        token       = ctx.start if hasattr(ctx, "start") else ctx
        
        self.line   = token.line
        self.column = token.column
        self.code   = code
        self.params = params
        
        super().__init__(code)

# ---------------------------------------------------------------------------
# the transpiler generator for Pascal->Assembly
# ---------------------------------------------------------------------------
class AsmJitGenerator(MiniPascalParserVisitor):
    def __init__(self, asm_file = None):
        self.vars               = {}
        self.next_slot          = 0
        self.lines              = []
        self.program_name       = "Program"
        self.var_types          = {}
        self.cpp_print_lines    = []
        
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
        
        
        self.type_aliases       = {}
        self.pointer_types      = {}
        
        self.scope_stack        = []
        
        self.local_var_stack    = []
        self.local_const_stack  = []

        self.asm_label_mappings = []
        
        self.current_function   = None
        self.current_proc_params= {}

        self.asm_file               = asm_file
        self.emit_local_string_data = True
    
    def format_error(self, filename, err):
        template = ERROR_MAP.get(err.code, err.code)
        message  = template.format(**err.params)
        
        return f"{err.code}: {os.path.basename(filename)} {err.line}:{err.column} {message}"
    
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

    def type_size(self, ctx, typ):
        typ = self.resolve_type(typ)

        if typ.startswith("^"):
            return 8
            
        if typ == "integer":
            return 4
            
        if typ == "double":
            return 8
            
        if typ == "string":
            return 8

        if typ in self.records:
            return self.records[typ].size
        
        if typ in self.arrays:
            return self.arrays[typ].size

        raise CompileError(ctx, "E0004", name=typ)

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
    
    def declare_array(self, ctx, name, index_min, index_max, element_type, init_values=None, dimensions=None):
        key = name.lower()

        if key in self.arrays:
            raise CompileError(ctx, "E0002", name=name)

        resolved_type = self.resolve_type(element_type)
        element_size = self.type_size(ctx, resolved_type)

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
        
        if typ != "integer":
            raise CompileError(ctx, "E0005", got=typ, expected="integer")
        
        scope["next_offset"] += 8
        offset = -scope["next_offset"]
        
        scope["vars"][key] = {
            "name": name,
            "type": typ,
            "offset": offset
        }
    
    def declare_var(self, ctx, name, vtype):
        key = name.lower()
        typ = self.resolve_type(vtype)
        
        if key in self.vars:
            raise CompileError(ctx, "E0002", name=name)
        
        if typ == "integer":
            slot = self.next_int_slot
            self.next_int_slot += 1
        
        elif typ == "double":
            slot = self.next_double_slot
            self.next_double_slot += 1
        
        elif typ == "string":
            slot = self.next_string_slot
            self.next_string_slot += 1
        
        elif typ in self.records:
            slot = self.next_record_slot
            self.next_record_slot += self.records[typ].size
        
        elif typ in self.arrays:
            slot = self.next_arrays_slot
            self.next_arrays_slot += self.arrays[typ].size
        
        elif typ.startswith("^"):
            slot = self.next_pointr_slot
            self.next_pointr_slot += 1
            
        else:
            raise CompileError(ctx, "E0004", name=vtype)
        
        self.vars[key] = {
            "name": name,
            "type": typ,
            "slot": slot,
        }
        
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
    
    def resolve_pointer_record_path(self, ctx, parts):
        ptr_name = parts[0]
        ptr_key  = ptr_name.lower()

        if ptr_key not in self.vars:
            raise CompileError(ctx, "E0001", name=ptr_name)

        ptr_info = self.vars[ptr_key]
        ptr_type = ptr_info["type"]

        if not ptr_type.startswith("^"):
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
            current_type = field.type

            if field_name != parts[-1]:
                if current_type not in self.records:
                    raise CompileError(ctx, "E0005", got=current_type, expected="record")

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

        self.emit_array_bounds_check(ctx, var_name, array_info)

        if array_info.index_min != 0:
            self.emit(f"a.sub(x86::eax, {array_info.index_min});")

        self.emit(f"a.imul(x86::eax, x86::eax, {array_info.element_size});")
        self.emit(f"a.add(x86::eax, {var_info['slot']});")

        # Array-Basis holen
        self.emit("a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));")
        self.emit("a.movsxd(x86::rax, x86::eax);")
        self.emit("a.add(x86::r11, x86::rax);")

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
            self.emit(f"a.add(x86::r11, {field_offset});")

        return field
    
    def resolve_type(self, type_name):
        typ = type_name.lower()

        if typ.startswith("^"):
            return typ

        while typ in self.type_aliases:
            typ = self.type_aliases[typ].lower()

        if typ in self.enums:
            return "integer"

        if typ in self.records:
            return typ

        if typ in self.arrays:
            return typ

        return typ
    
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
            typ = p.typeName().getText().lower()
            for ident in p.identList().IDENT():
                params.append({
                    "name": ident.getText(),
                    "type": typ
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
    
    def emit_multi_array_index_offset(self, ctx, var_name, array_info, index_exprs):
        dims = array_info.dimensions

        if len(index_exprs) != len(dims):
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(index_exprs)),
                expected=str(len(dims))
            )

        self.emit("a.xor_(x86::ebx, x86::ebx); // linear array index")

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
                self.emit(f"a.sub(x86::eax, {dim['min']});")

            factor = 1
            for next_dim in dims[i + 1:]:
                factor *= next_dim["max"] - next_dim["min"] + 1

            if factor != 1:
                self.emit(f"a.imul(x86::eax, x86::eax, {factor});")

            self.emit("a.add(x86::ebx, x86::eax);")

        self.emit("a.mov(x86::eax, x86::ebx); // final linear index")

    def emit_array_bounds_check_dimension(self, ctx, var_name, min_value, max_value):
        ok_label    = self.new_named_label("array_bounds_ok")
        fail_label  = self.new_named_label("array_bounds_fail")
        array_label = self.add_string_literal(var_name)

        self.emit("a.mov(x86::r10d, x86::eax); // save dimension index")

        self.emit(f"a.cmp(x86::eax, {min_value});")
        self.emit(f"a.jl({fail_label});")

        self.emit(f"a.cmp(x86::eax, {max_value});")
        self.emit(f"a.jg({fail_label});")

        self.emit(f"a.jmp({ok_label});")

        self.emit(f"a.bind({fail_label});")
        self.emit(f"a.mov(x86::rcx, imm((uint64_t){array_label}));")
        self.emit("a.mov(x86::edx, x86::r10d);")
        self.emit(f"a.mov(x86::r8d, {min_value});")
        self.emit(f"a.mov(x86::r9d, {max_value});")
        self.emit("a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));")
        self.emit_call_rax()

        self.emit(f"a.bind({ok_label});")
        self.emit("a.mov(x86::eax, x86::r10d); // restore dimension index")
    
    def emit_array_bounds_check_for_dimension(self, dim):
        min_value = dim["min"]
        max_value = dim["max"]

        self.asm.emit("push rax")

        self.asm.emit(f"cmp eax, {min_value}")
        self.asm.emit("jl array_bounds_error")

        self.asm.emit(f"cmp eax, {max_value}")
        self.asm.emit("jg array_bounds_error")

        self.asm.emit("pop rax")
    
    def emit_address_of_array_element(self, ctx, var_name, index_exprs):
        var_info, array_info = self.get_array_info(ctx, var_name)

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        self.emit(f"a.imul(x86::eax, x86::eax, {array_info.element_size});")
        self.emit(f"a.add(x86::eax, {var_info['slot']});")

        self.emit("a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));")
        self.emit("a.movsxd(x86::rax, x86::eax);")
        self.emit("a.add(x86::rax, x86::r11); // @array[index]")

        return "^" + array_info.element_type
        
        """def emit_array_bounds_check(self, ctx, var_name, array_info):
        ok_label    = self.new_named_label("array_bounds_ok")
        fail_label  = self.new_named_label("array_bounds_fail")
        array_label = self.add_string_literal(var_name)

        self.emit("a.mov(x86::r10d, x86::eax); // save array index")

        self.emit(f"a.cmp(x86::eax, {array_info.index_min});")
        self.emit(f"a.jl({fail_label});")

        self.emit(f"a.cmp(x86::eax, {array_info.index_max});")
        self.emit(f"a.jg({fail_label});")

        self.emit(f"a.jmp({ok_label});")

        self.emit(f"a.bind({fail_label});")
        self.emit(f"a.mov(x86::rcx, imm((uint64_t){array_label}));")
        self.emit("a.mov(x86::edx, x86::r10d);")
        self.emit(f"a.mov(x86::r8d, {array_info.index_min});")
        self.emit(f"a.mov(x86::r9d, {array_info.index_max});")
        self.emit("a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));")
        self.emit_call_rax()

        self.emit(f"a.bind({ok_label});")
        self.emit("a.mov(x86::eax, x86::r10d); // restore array index")"""
        
    def emit_array_bounds_check(self, ctx, var_name, array_info):
        ok_label    = self.new_named_label("array_bounds_ok")
        fail_label  = self.new_named_label("array_bounds_fail")
        array_label = self.add_string_literal(var_name)

        # Originalindex in EBX sichern
        self.emit("a.mov(x86::ebx, x86::eax); // save array index")

        self.emit(f"a.cmp(x86::eax, {array_info.index_min});")
        self.emit(f"a.jl({fail_label});")

        self.emit(f"a.cmp(x86::eax, {array_info.index_max});")
        self.emit(f"a.jg({fail_label});")

        self.emit(f"a.jmp({ok_label});")

        self.emit(f"a.bind({fail_label});")
        self.emit(f"a.mov(x86::rcx, imm((uint64_t){array_label}));")
        self.emit("a.mov(x86::edx, x86::ebx);")
        self.emit(f"a.mov(x86::r8d, {array_info.index_min});")
        self.emit(f"a.mov(x86::r9d, {array_info.index_max});")
        self.emit("a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));")
        self.emit_call_rax()

        self.emit(f"a.bind({ok_label});")

        # Index wiederherstellen
        self.emit("a.mov(x86::eax, x86::ebx); // restore array index")
    
    def emit_load_const(self, ctx, name):
        c = self.find_const(name)

        if not c:
            raise CompileError(ctx, "E0001", name=name)

        typ = c["type"]
        val = c["value"]

        if typ == "integer":
            self.emit(f"a.mov(x86::eax, {val});")
            return "integer"

        if typ == "double":
            return self.emit_load_double_literal(val)

        if typ == "string":
            label = self.add_string_literal(val)
            self.emit(f"a.mov(x86::rax, imm((uint64_t){label}));")
            return "string"

        raise CompileError(ctx, "E0014", var_type=typ)
    
    def emit_load_double_literal(self, value):
        value_text = str(value)

        self.add_double_literal(value_text)

        self.emit(f"a.mov(x86::rax, imm(double_to_bits({value_text})));")
        self.emit("a.movq(x86::xmm0, x86::rax);")

        return "double"
    
    def emit_load_pointer_deref(self, ctx, name):
        key = name.lower()

        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=name)

        info = self.vars[key]
        typ = info["type"]

        if not typ.startswith("^"):
            raise CompileError(ctx, "E0005", got=typ, expected="pointer")

        base_type = typ[1:]

        self.emit_load_var(name, info)

        if base_type == "integer":
            self.emit("a.mov(x86::eax, x86::dword_ptr(x86::rax)); // p^")
            return "integer"

        if base_type == "double":
            self.emit("a.movsd(x86::xmm0, x86::qword_ptr(x86::rax)); // p^")
            return "double"

        if base_type == "string":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::rax)); // p^")
            return "string"

        raise CompileError(ctx, "E0014", var_type=base_type)
    
    def emit_load_param(self, ctx, name):
        param = self.find_param(name)

        if not param:
            raise CompileError(ctx, "E0001", name=name)

        typ = param["type"]
        offset = param["stack_offset"]

        if typ == "integer":
            self.emit(f"a.mov(x86::eax, x86::dword_ptr(x86::rbp, {offset}));")
            return "integer"

        if typ == "string":
            self.emit(f"a.mov(x86::rax, x86::qword_ptr(x86::rbp, {offset}));")
            return "string"

        raise CompileError(ctx, "E0014", var_type=typ)
    
    def emit_load_record_field(self, ctx, parts):
        field_offset, field = self.resolve_record_path(ctx, parts)
        path = ".".join(parts)

        self.emit("a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, record_vars)));")

        if field.type == "integer":
            self.emit(f"a.mov(x86::eax, x86::dword_ptr(x86::r11, {field_offset})); // {path}")
            return "integer"

        if field.type == "double":
            self.emit(f"a.movsd(x86::xmm0, x86::qword_ptr(x86::r11, {field_offset})); // {path}")
            return "double"

        if field.type == "string":
            self.emit(f"a.mov(x86::rax, x86::qword_ptr(x86::r11, {field_offset})); // {path}")
            return "string"

        return field.type
    
    def emit_load_pointer_record_field(self, ctx, parts):
        ptr_info, field_offset, field = self.resolve_pointer_record_path(ctx, parts)
        ptr_name = parts[0]
        path = "^.".join([ptr_name, ".".join(parts[1:])])

        # Pointer-Wert nach RAX laden
        self.emit_load_var(ptr_name, ptr_info)

        if field_offset != 0:
            self.emit(f"a.add(x86::rax, {field_offset}); // field offset")

        if field.type == "integer":
            self.emit(f"a.mov(x86::eax, x86::dword_ptr(x86::rax)); // {path}")
            return "integer"

        if field.type == "double":
            self.emit(f"a.movsd(x86::xmm0, x86::qword_ptr(x86::rax)); // {path}")
            return "double"

        if field.type == "string":
            self.emit(f"a.mov(x86::rax, x86::qword_ptr(x86::rax)); // {path}")
            return "string"

        return field.type
    
    def emit_load_local_var(self, ctx, name, info):
        var = self.find_local_var(name)

        if not var:
            raise CompileError(ctx, "E0012", name=name)

        typ    = var["type"]
        offset = var["offset"]

        if typ == "integer":
            self.emit(f"mov eax, [rbp-{offset}]")
            return "integer"

        raise CompileError(ctx, "E0011", name=typ)

    def emit_store_pointer_deref(self, ctx, name, expr_type):
        key = name.lower()

        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=name)

        info = self.vars[key]
        typ = info["type"]

        if not typ.startswith("^"):
            raise CompileError(ctx, "E0005", got=typ, expected="pointer")

        base_type = typ[1:]

        if base_type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=base_type)

        if expr_type == "integer":
            self.emit("a.mov(x86::ebx, x86::eax);")

        elif expr_type == "double":
            self.emit("a.sub(x86::rsp, 8);")
            self.emit("a.movsd(x86::qword_ptr(x86::rsp), x86::xmm0);")

        elif expr_type == "string":
            self.emit("a.push(x86::rax);")

        self.emit_load_var(name, info)

        if expr_type == "integer":
            self.emit("a.mov(x86::dword_ptr(x86::rax), x86::ebx); // p^ :=")
            return

        if expr_type == "double":
            self.emit("a.movsd(x86::xmm0, x86::qword_ptr(x86::rsp));")
            self.emit("a.add(x86::rsp, 8);")
            self.emit("a.movsd(x86::qword_ptr(x86::rax), x86::xmm0); // p^ :=")
            return

        if expr_type == "string":
            self.emit("a.pop(x86::r11);")
            self.emit("a.mov(x86::qword_ptr(x86::rax), x86::r11); // p^ :=")
            return
        
    def emit_store_record_field(self, ctx, parts, expr_type):
        field_offset, field = self.resolve_record_path(ctx, parts)

        if field.type == "double" and expr_type == "integer":
            self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")
            expr_type = "double"

        if field.type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)

        path = ".".join(parts)

        self.emit("a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, record_vars)));")

        if field.type == "integer":
            self.emit(f"a.mov(x86::dword_ptr(x86::r11, {field_offset}), x86::eax); // {path}")
            return

        if field.type == "double":
            self.emit(f"a.movsd(x86::qword_ptr(x86::r11, {field_offset}), x86::xmm0); // {path}")
            return

        if field.type == "string":
            self.emit(f"a.mov(x86::qword_ptr(x86::r11, {field_offset}), x86::rax); // {path}")
            return

        raise CompileError(ctx, "E0013", var_type=field.type)
    
    def emit_store_pointer_record_field(self, ctx, parts, expr_type):
        ptr_info, field_offset, field = self.resolve_pointer_record_path(ctx, parts)
        ptr_name = parts[0]
        path = "^.".join([ptr_name, ".".join(parts[1:])])

        if field.type == "double" and expr_type == "integer":
            self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")
            expr_type = "double"

        if field.type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)

        if expr_type == "integer":
            self.emit("a.mov(x86::ebx, x86::eax);")
        elif expr_type == "double":
            self.emit("a.sub(x86::rsp, 8);")
            self.emit("a.movsd(x86::qword_ptr(x86::rsp), x86::xmm0);")
        elif expr_type == "string":
            self.emit("a.push(x86::rax);")

        # Pointer-Wert nach RAX laden
        self.emit_load_var(ptr_name, ptr_info)

        if field_offset != 0:
            self.emit(f"a.add(x86::rax, {field_offset}); // field offset")

        if field.type == "integer":
            self.emit(f"a.mov(x86::dword_ptr(x86::rax), x86::ebx); // {path} :=")
            return

        if field.type == "double":
            self.emit("a.movsd(x86::xmm0, x86::qword_ptr(x86::rsp));")
            self.emit("a.add(x86::rsp, 8);")
            self.emit(f"a.movsd(x86::qword_ptr(x86::rax), x86::xmm0); // {path} :=")
            return

        if field.type == "string":
            self.emit("a.pop(x86::r11);")
            self.emit(f"a.mov(x86::qword_ptr(x86::rax), x86::r11); // {path} :=")
            return

        raise CompileError(ctx, "E0013", var_type=field.type)
    
    def emit_store_array_element(self, ctx, var_name, index_expr_ctx, expr_type):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
            
        var_info, array_info = self.get_array_info(ctx, var_name)

        if array_info.element_type == "double" and expr_type == "integer":
            self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")
            expr_type = "double"

        if array_info.element_type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=array_info.element_type)

        if expr_type == "integer":
            self.emit("a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax);")

        elif expr_type == "double":
            self.emit("a.sub(x86::rsp, 8);")
            self.emit("a.movsd(x86::qword_ptr(x86::rsp), x86::xmm0);")

        elif expr_type == "string":
            self.emit("a.push(x86::rax);")

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        self.emit(f"a.imul(x86::eax, x86::eax, {array_info.element_size});")
        self.emit(f"a.add(x86::eax, {var_info['slot']});")

        self.emit("a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));")
        self.emit("a.movsxd(x86::rax, x86::eax);")
        self.emit("a.add(x86::r11, x86::rax);")

        if array_info.element_type == "integer":
            self.emit("a.mov(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));")
            self.emit("a.mov(x86::dword_ptr(x86::r11), x86::eax);")
            return

        if array_info.element_type == "double":
            self.emit("a.movsd(x86::xmm0, x86::qword_ptr(x86::rsp));")
            self.emit("a.add(x86::rsp, 8);")
            self.emit("a.movsd(x86::qword_ptr(x86::r11), x86::xmm0);")
            return

        if array_info.element_type == "string":
            self.emit("a.pop(x86::rax);")
            self.emit("a.mov(x86::qword_ptr(x86::r11), x86::rax);")
            return

        raise CompileError(ctx, "E0013", var_type=array_info.element_type)

    def emit_load_array_element(self, ctx, var_name, index_expr_ctx):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
            
        var_info, array_info = self.get_array_info(ctx, var_name)

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        self.emit(f"a.imul(x86::eax, x86::eax, {array_info.element_size});")
        self.emit(f"a.add(x86::eax, {var_info['slot']});")

        self.emit("a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));")
        self.emit("a.movsxd(x86::rax, x86::eax);")
        self.emit("a.add(x86::r11, x86::rax);")

        if array_info.element_type == "integer":
            self.emit("a.mov(x86::eax, x86::dword_ptr(x86::r11));")
            return "integer"

        if array_info.element_type == "double":
            self.emit("a.movsd(x86::xmm0, x86::qword_ptr(x86::r11));")
            return "double"

        if array_info.element_type == "string":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r11));")
            return "string"

        raise CompileError(ctx, "E0014", var_type=array_info.element_type)
        
    def emit_store_result(self, ctx, expr_type):
        if self.current_function is None:
            raise CompileError(ctx, "E0006")

        return_type = self.current_function["return_type"]

        if return_type == "double" and expr_type == "integer":
            self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")
            expr_type = "double"

        if return_type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=return_type)

        # Integer: Ergebnis liegt bereits in EAX
        if return_type == "integer":
            return None

        # Double: Ergebnis liegt bereits in XMM0
        if return_type == "double":
            return None

        # String: Ergebnis liegt bereits in RAX
        if return_type == "string":
            return None

        raise CompileError(ctx, "E0005", got=return_type, expected="integer/string/double")

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
            self.emit(f"a.mov(x86::eax, x86::dword_ptr(x86::r11)); // {path}")
            return "integer"

        if field.type == "double":
            self.emit(f"a.movsd(x86::xmm0, x86::qword_ptr(x86::r11)); // {path}")
            return "double"

        if field.type == "string":
            self.emit(f"a.mov(x86::rax, x86::qword_ptr(x86::r11)); // {path}")
            return "string"

        return field.type

    def emit_store_array_record_field(self, ctx, var_name, index_expr_ctx, field_parts, expr_type):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
            
        # Wert sichern, bevor Index/Adresse berechnet wird
        if expr_type == "integer":
            self.emit("a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax);")

        elif expr_type == "double":
            self.emit("a.movsd(x86::qword_ptr(x86::r12, offsetof(JitContext, print_double_tmp)), x86::xmm0);")

        else:
            raise CompileError(ctx, "E0005", got=expr_type, expected="integer/double")

        field = self.resolve_array_record_field(
            ctx,
            var_name,
            index_expr_ctx,
            field_parts
        )

        if field.type == "double" and expr_type == "integer":
            self.emit("a.mov(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));")
            self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")
            self.emit(f"a.movsd(x86::qword_ptr(x86::r11), x86::xmm0); // {var_name}[...].{'.'.join(field_parts)} :=")
            return

        if field.type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)

        if field.type == "integer":
            self.emit("a.mov(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));")
            self.emit(f"a.mov(x86::dword_ptr(x86::r11), x86::eax); // {var_name}[...].{'.'.join(field_parts)} :=")
            return

        if field.type == "double":
            self.emit("a.movsd(x86::xmm0, x86::qword_ptr(x86::r12, offsetof(JitContext, print_double_tmp)));")
            self.emit(f"a.movsd(x86::qword_ptr(x86::r11), x86::xmm0); // {var_name}[...].{'.'.join(field_parts)} :=")
            return

        raise CompileError(ctx, "E0013", var_type=field.type)

    def emit_store_local_var(self, ctx, name, info):
        var = self.find_local_var(name)

        if not var:
            raise CompileError(ctx, "E0012", name)

        typ = var["type"]
        offset = var["offset"]

        if typ != expr_type:
            raise CompileError(ctx, "E0005", name=typ, name2=expr_type)

        if typ == "integer":
            self.emit(f"mov [rbp-{offset}], eax")
            return
        
        raise CompileError(ctx, "E0011", name=typ)
        
    def emit_call_rax(self):
        self.emit("a.sub(x86::rsp, 32); // Windows x64 shadow space")
        self.emit("a.call(x86::rax);")
        self.emit("a.add(x86::rsp, 32);")
    
    def emit_load_var(self, name, info):
        typ  = info["type"]
        slot = info["slot"]

        if typ.startswith("^"):
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));")
            self.emit(f"a.mov(x86::rax, x86::qword_ptr(x86::rax, {slot * 8})); // {name}")
            return
        
        if typ == "integer":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, int_vars)));")
            self.emit(f"a.mov(x86::eax, x86::dword_ptr(x86::rax, {slot * 4})); // {name}")
            return

        if typ == "double":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, double_vars)));")
            self.emit(f"a.movsd(x86::xmm0, x86::qword_ptr(x86::rax, {slot * 8})); // {name}")
            return

        if typ == "string":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, string_vars)));")
            self.emit(f"a.mov(x86::rax, x86::qword_ptr(x86::rax, {slot * 8})); // {name}")
            return

        raise CompileError(None, "E0014", var_type=typ)
    
    def emit_store_var(self, ctx, name, info):
        typ  = info["type"]
        slot = info["slot"]

        if typ.startswith("^"):
            self.emit("a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));")
            self.emit(f"a.mov(x86::qword_ptr(x86::r11, {slot * 8}), x86::rax); // {name}")
            return
    
        if typ == "integer":
            self.emit("a.mov(x86::ebx, x86::eax);")
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, int_vars)));")
            self.emit(f"a.mov(x86::dword_ptr(x86::rax, {slot * 4}), x86::ebx); // {name}")
            return

        if typ == "double":
            self.emit("a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, double_vars)));")
            self.emit(f"a.movsd(x86::qword_ptr(x86::r11, {slot * 8}), x86::xmm0); // {name}")
            return

        if typ == "string":
            self.emit("a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, string_vars)));")
            self.emit(f"a.mov(x86::qword_ptr(x86::r11, {slot * 8}), x86::rax); // {name}")
            return

        raise CompileError(ctx, "E0013", var_type=typ)
    
    def emit_procedure_declaration(self, ctx):
        proc_name = ctx.IDENT().getText()

        end_label = self.new_label(f"endproc_{proc_name}")

        self.emit(f"jmp {end_label}")
        self.emit(f"{proc_name}:")

        self.emit("push rbp")
        self.emit("mov rbp, rsp")
        self.emit("sub rsp, 256")

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

        self.emit("mov rsp, rbp")
        self.emit("pop rbp")
        self.emit("ret")

        self.emit(f"{end_label}:")
    
    def emit_address_of_var(self, ctx, name):
        key = name.lower()

        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=name)

        info = self.vars[key]
        typ  = info["type"]
        slot = info["slot"]

        if typ == "integer":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, int_vars)));")
            self.emit(f"a.add(x86::rax, {slot * 4}); // @{name}")
            return "^integer"

        if typ == "double":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, double_vars)));")
            self.emit(f"a.add(x86::rax, {slot * 8}); // @{name}")
            return "^double"

        if typ == "string":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, string_vars)));")
            self.emit(f"a.add(x86::rax, {slot * 8}); // @{name}")
            return "^string"

        if typ in self.records:
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, record_vars)));")
            self.emit(f"a.add(x86::rax, {slot}); // @{name}")
            return "^" + typ

        raise CompileError(ctx, "E0005", got=typ, expected="addressable variable")
    
    def emit_function_declaration(self, ctx, name, return_type):
        key = name.lower()

        scoped = self.scoped_name(name)

        label     = self.new_named_label("func_" + scoped)
        end_label = self.new_named_label("endfunc_" + scoped)

        self.functions[scoped.lower()]["label"] = label

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

        self.emit(f"a.jmp({end_label});")
        self.emit(f"a.bind({label});")

        self.emit("a.push(x86::rbp);")
        self.emit("a.mov(x86::rbp, x86::rsp);")
        self.emit("a.push(x86::rbx); // preserve non-volatile RBX")

        old_params   = self.current_proc_params
        old_function = self.current_function

        self.current_proc_params = {}
        self.current_function = {
            "name": name,
            "return_type": return_type.lower(),
            "scoped_name": scoped
        }

        for index, p in enumerate(params):
            reg = param_regs[index]
            pname = p["name"]

            self.emit(f"a.push(x86::{reg}); // save function param {pname}")

            self.current_proc_params[pname.lower()] = {
                "type": p["type"],
                "reg": reg,
                "stack_offset": -8 * (index + 2)
            }
            
        if len(params) % 2 == 0:
            self.emit("a.sub(x86::rsp, 8); // align stack in function")

        self.scope_stack.append(name)
        self.emit("a.sub(x86::rsp, 256); // local variables")
        
        self.push_local_scope()
        self.push_const_scope()

        self.visit(ctx.block())

        self.pop_const_scope()
        self.pop_local_scope()
        
        self.scope_stack.pop()

        self.current_function = old_function
        self.current_proc_params = old_params

        if return_type.lower() not in ["integer", "string", "double"]:
            raise CompileError(ctx, "E0005", got=return_type, expected="integer/string/double")

        self.emit("a.mov(x86::rbx, x86::qword_ptr(x86::rbp, -8));")
        self.emit("a.mov(x86::rsp, x86::rbp);")
        self.emit("a.pop(x86::rbp);")
        self.emit("a.ret();")

        self.emit(f"a.bind({end_label});")
    
    def emit_init_array_var(self, ctx, name, info):
        array_type = info["type"]

        if array_type not in self.arrays:
            return

        array_info = self.arrays[array_type]

        if not array_info.init_values:
            return

        base_offset = info["slot"]

        self.emit("a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));")

        for index, value in enumerate(array_info.init_values):
            offset = base_offset + index * array_info.element_size

            if array_info.element_type == "integer":
                self.emit(f"a.mov(x86::dword_ptr(x86::r11, {offset}), {value}); // init {name}[{index + array_info.index_min}]")

            elif array_info.element_type == "double":
                self.emit(f"a.mov(x86::rax, imm(double_to_bits({value})));")
                self.emit("a.movq(x86::xmm0, x86::rax);")
                self.emit(f"a.movsd(x86::qword_ptr(x86::r11, {offset}), x86::xmm0); // init {name}[{index + array_info.index_min}]")

            elif array_info.element_type == "string":
                label = self.add_string_literal(value)
                self.emit(f"a.mov(x86::rax, imm((uint64_t){label}));")
                self.emit(f"a.mov(x86::qword_ptr(x86::r11, {offset}), x86::rax); // init {name}[{index + array_info.index_min}]")
                
    def emit_if_statement(self, ctx):
        else_name = self.new_named_label("else")
        end_name  = self.new_named_label("endif")

        self.emit_condition_jump_false(ctx.condition(), else_name)

        self.visit(ctx.statement(0))

        if ctx.ELSE():
            self.emit(f"a.jmp({end_name});")
            self.emit(f"a.bind({else_name});")
            self.visit(ctx.statement(1))
            self.emit(f"a.bind({end_name});")
        else:
            self.emit(f"a.bind({else_name});")
        
    def emit_int_to_double(self):
        self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")
    
    def emit_condition_jump_false(self, ctx, false_label):
        left_ctx  = ctx.expr(0)
        right_ctx = ctx.expr(1)
        op        = ctx.compareOp().getText()

        left_type  = self.visit(left_ctx)

        # Linken Wert sichern
        if left_type == "double":
            self.emit("a.sub(x86::rsp, 8);")
            self.emit("a.movsd(x86::qword_ptr(x86::rsp), x86::xmm0);")
        elif left_type == "integer":
            self.emit("a.push(x86::rax);")
        else:
            raise CompileError(ctx, "E0005", got=left_type, expected="integer/double")

        right_type = self.visit(right_ctx)

        # Double-Vergleich, sobald eine Seite Double ist
        if left_type == "double" or right_type == "double":
            if right_type == "integer":
                self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")
            elif right_type != "double":
                raise CompileError(ctx, "E0005", got=right_type, expected="integer/double")

            self.emit("a.movapd(x86::xmm1, x86::xmm0);")

            if left_type == "integer":
                self.emit("a.pop(x86::rax);")
                self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")
            else:
                self.emit("a.movsd(x86::xmm0, x86::qword_ptr(x86::rsp));")
                self.emit("a.add(x86::rsp, 8);")

            # Vergleich: left xmm0 gegen right xmm1
            self.emit("a.ucomisd(x86::xmm0, x86::xmm1);")

            jump_map = {
                "=":  "jne",
                "<>": "je",
                "<":  "jae",
                "<=": "ja",
                ">":  "jbe",
                ">=": "jb",
            }

            self.emit(f"a.{jump_map[op]}({false_label});")
            return

        # Integer-Vergleich
        self.emit("a.mov(x86::ebx, x86::eax);")
        self.emit("a.pop(x86::rax);")
        self.emit("a.cmp(x86::eax, x86::ebx);")

        jump_map = {
            "=":  "jne",
            "<>": "je",
            "<":  "jge",
            "<=": "jg",
            ">":  "jle",
            ">=": "jl",
        }

        self.emit(f"a.{jump_map[op]}({false_label});")
    
    def emit_expr_as_double(self, ctx):
        expr_type = self.visit(ctx)

        if expr_type == "integer":
            self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")

        elif expr_type != "double":
            raise CompileError(ctx, "E0005", got=expr_type, expected="double")

        return "double"

    def emit_while_statement(self, ctx):
        start_name = self.new_named_label("while")
        end_name   = self.new_named_label("endwhile")

        self.emit(f"a.bind({start_name});")
        self.emit_condition_jump_false(ctx.condition(), end_name)

        self.visit(ctx.statement())

        self.emit(f"a.jmp({start_name});")
        self.emit(f"a.bind({end_name});")
    
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

        self.emit(f"a.bind({start_name});")

        for stmt in ctx.statementList().statement():
            self.visit(stmt)

        self.emit_condition_jump_false(ctx.condition(), start_name)

        self.emit(f"a.bind({end_name});")
    
    def emit_for_statement(self, ctx):
        var_name = ctx.IDENT().getText()
        info = self.var_info(ctx, var_name)

        if info["type"] != "integer":
            raise CompileError(ctx, "E0005", got=info["type"], expected="integer")

        start_name = self.new_named_label("for")
        end_name   = self.new_named_label("endfor")

        # Startwert auswerten
        start_type = self.visit(ctx.expr(0))

        if start_type != "integer":
            raise CompileError(ctx, "E0005", got=start_type, expected="integer")

        self.emit_store_var(ctx, var_name, info)

        # Endwert auswerten und in r10d sichern
        end_type = self.visit(ctx.expr(1))

        if end_type != "integer":
            raise CompileError(ctx, "E0005", got=end_type, expected="integer")

        self.emit("a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax); // for end value")

        self.emit(f"a.bind({start_name});")

        # Laufvariable laden
        self.emit_load_var(var_name, info)

        direction = ctx.getChild(4).getText().lower()

        if direction == "to":
            self.emit("a.cmp(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));")
            self.emit(f"a.jg({end_name});")
        else:
            self.emit("a.cmp(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_double_tmp)));")
            self.emit(f"a.jl({end_name});")

        self.visit(ctx.statement())

        # Laufvariable erneut laden, ändern, speichern
        self.emit_load_var(var_name, info)

        if direction == "to":
            self.emit("a.add(x86::eax, 1);")
        else:
            self.emit("a.sub(x86::eax, 1);")

        self.emit_store_var(ctx, var_name, info)

        self.emit(f"a.jmp({start_name});")
        self.emit(f"a.bind({end_name});")
    
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
        self.lines.append("    " + line)
    
    def new_label_name(self, prefix):
        self.label_id += 1
        return f"{prefix}_{self.label_id}"
    
    def add_string_literal(self, text):
        name = f"str_{len(self.string_literals)}"
        self.string_literals.append((name, text))
        return name
    
    def visitProgramFile(self, ctx):
        self.program_name = ctx.IDENT().getText()

        for decl in ctx.declarationPart():
            self.visit(decl)

        self.emit("a.push(x86::r12);")
        self.emit("a.push(x86::rbx);")
        self.emit("a.sub(x86::rsp, 8); // align stack")
        self.emit("a.mov (x86::r12, x86::rcx); // ctx")
        
        for name, info in self.vars.items():
            if info["type"] in self.arrays:
                self.emit_init_array_var(ctx, name, info)
        
        self.visit(ctx.block())
        return self.render_cpp()
    
    def visitDeclarationPart(self, ctx):
        return self.visit(ctx.getChild(0))
    
    def visitBlock(self, ctx):
        if ctx.localDeclaration():
            for decl in ctx.localDeclaration():
                self.visit(decl)

        return self.visit(ctx.statementList())
    
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

        for r in ctx.arrayRange():
            min_value = int(r.expr(0).getText())
            max_value = int(r.expr(1).getText())

            dimensions.append({
                "min": min_value,
                "max": max_value
            })

        element_type = ctx.typeName().getText()

        return {
            "kind": "array",
            "dimensions": dimensions,
            "element_type": element_type
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
    
    def visitStatementList(self, ctx):
        for st in ctx.statement():
            self.visit(st)
    
    def visitStatement(self, ctx):
        if ctx.procedureCallStatement():
            return self.visit(ctx.procedureCallStatement())
    
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
        
        if ctx.compoundStatement():
            return self.visit(ctx.compoundStatement())
        
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
        vtype = ctx.typeName().getText()

        for ident in ctx.identList().IDENT():
            name = ident.getText()

            if self.local_var_stack:
                self.declare_local_var(ctx, name, vtype)
            else:
                self.declare_var(ctx, name, vtype)

        return None
    
    def visitTypeDeclaration(self, ctx):
        if ctx.enumDeclaration():
            return self.visit(ctx.enumDeclaration())
        
        if ctx.recordDeclaration():
            return self.visit(ctx.recordDeclaration())
        
        if ctx.arrayDeclaration():
            return self.visit(ctx.arrayDeclaration())
        
        type_name  = ctx.IDENT().getText()
        alias_name = ctx.typeName().getText()
        
        self.declare_type_alias(ctx, type_name, alias_name)
        return None
    
    def visitFunctionDeclaration(self, ctx):
        name = ctx.IDENT().getText()
        return_type = ctx.typeName().getText()

        scoped = self.scoped_name(name)
        key = scoped.lower()

        self.functions[key] = {
            "name": name,
            "scoped_name": scoped,
            "return_type": return_type,
            "label": f"func_{scoped}",
            "params": self.collect_formal_params(ctx)
        }

        old_function = self.current_function
        #self.current_function = name

        self.emit_function_declaration(ctx, name, return_type)
        self.current_function = old_function
    
    def visitAssignment(self, ctx):
        target_ctx = ctx.variableRef()
        target     = target_ctx.getText()
        expr_type  = self.visit(ctx.expr())

        if target.lower() == "result":
            self.emit_store_result(ctx, expr_type)
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
                
                # points[0].X
                if len(suffixes) > 1 and suffixes[1].DOT():
                    field_parts = []
                    
                    for s in suffixes[1:]:
                        if s.DOT():
                            field_parts.append(s.IDENT().getText())
                    
                    self.emit_store_array_record_field(
                        ctx,
                        var_name,
                        list(first.expr()),
                        field_parts,
                        expr_type
                    )
                    return None
                
                # normales a[0]
                self.emit_store_array_element(
                    ctx,
                    var_name,
                    list(first.expr()),
                    expr_type
                )
                return None
            
            if first.DOT():
                parts = [target_ctx.IDENT().getText()]
                
                for s in suffixes:
                    if s.DOT():
                        parts.append(s.IDENT().getText())
                
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

        if var_type.startswith("^") and expr_type == var_type:
            self.emit_store_var(ctx, target, var_info)
            return None
            
        if var_type == "double" and expr_type == "integer":
            self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")
            expr_type = "double"
            
        if var_type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=var_type)

        self.emit_store_var(ctx, target, var_info)
        return None
    
    def visitExpr(self, ctx):
        result_type = self.visit(ctx.term(0))

        for i in range(1, len(ctx.term())):
            op = ctx.getChild(2 * i - 1).getText()

            if result_type == "integer":
                self.emit("a.push(x86::rax);")

                right_type = self.visit(ctx.term(i))

                if right_type == "integer":
                    self.emit("a.mov(x86::ebx, x86::eax);")
                    self.emit("a.pop(x86::rax);")

                    if op == "+":
                        self.emit("a.add(x86::eax, x86::ebx);")
                    elif op == "-":
                        self.emit("a.sub(x86::eax, x86::ebx);")

                    result_type = "integer"
                    continue

                self.emit("a.pop(x86::rax);")
                self.emit("a.cvtsi2sd(x86::xmm1, x86::eax);")
                result_type = "double"

            # Double-Fallback
            self.emit("a.sub(x86::rsp, 8);")
            self.emit("a.movsd(x86::qword_ptr(x86::rsp), x86::xmm0);")

            right_type = self.visit(ctx.term(i))

            if right_type == "integer":
                self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")

            self.emit("a.movsd(x86::xmm1, x86::qword_ptr(x86::rsp));")
            self.emit("a.add(x86::rsp, 8);")

            if op == "+":
                self.emit("a.addsd(x86::xmm0, x86::xmm1);")
            elif op == "-":
                self.emit("a.movapd(x86::xmm2, x86::xmm0);")
                self.emit("a.movapd(x86::xmm0, x86::xmm1);")
                self.emit("a.subsd(x86::xmm0, x86::xmm2);")

            result_type = "double"

        return result_type
    
    def visitTerm(self, ctx):
        result_type = self.visit(ctx.factor(0))

        for i in range(1, len(ctx.factor())):
            op = ctx.getChild(2 * i - 1).getText()

            if result_type == "integer":
                self.emit("a.push(x86::rax);")

                right_type = self.visit(ctx.factor(i))

                if right_type == "integer":
                    self.emit("a.mov(x86::ebx, x86::eax);")
                    self.emit("a.pop(x86::rax);")

                    if op == "*":
                        self.emit("a.imul(x86::eax, x86::ebx);")
                        result_type = "integer"

                    elif op == "/":
                        self.emit("a.cdq();")
                        self.emit("a.idiv(x86::ebx);")
                        result_type = "integer"

                    continue

                self.emit("a.pop(x86::rax);")
                self.emit("a.cvtsi2sd(x86::xmm1, x86::eax);")
                result_type = "double"

            else:
                self.emit("a.sub(x86::rsp, 8);")
                self.emit("a.movsd(x86::qword_ptr(x86::rsp), x86::xmm0);")

                right_type = self.visit(ctx.factor(i))

                self.emit("a.movsd(x86::xmm1, x86::qword_ptr(x86::rsp));")
                self.emit("a.add(x86::rsp, 8);")

            if result_type == "double":
                if right_type == "integer":
                    self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")

                if op == "*":
                    self.emit("a.mulsd(x86::xmm0, x86::xmm1);")

                elif op == "/":
                    self.emit("a.movapd(x86::xmm2, x86::xmm0);")
                    self.emit("a.movapd(x86::xmm0, x86::xmm1);")
                    self.emit("a.divsd(x86::xmm0, x86::xmm2);")

                result_type = "double"

        return result_type
    
    def visitFactor(self, ctx):
        text = ctx.getText()
        key  = text.lower()

        if key in self.constants:
            c = self.constants[key]

            if c["type"] == "integer":
                self.emit(f"a.mov(x86::eax, {c['value']});")
                return "integer"

            if c["type"] == "double":
                return self.emit_load_double_literal(c["value"])

            if c["type"] == "string":
                label = self.add_string_literal(c["value"])
                self.emit(f"a.mov(x86::rax, imm((uint64_t){label}));")
                return "string"
        
        if ctx.AT():
            ref = ctx.variableRef()
            name = ref.IDENT().getText()
            return self.emit_address_of_var(ctx, name)
    
        if ctx.variableRef():
            ref = ctx.variableRef()
            suffixes = ref.variableSuffix()

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
                    
                    # points[0].X
                    if len(suffixes) > 1 and suffixes[1].DOT():
                        field_parts = []

                        for s in suffixes[1:]:
                            if s.DOT():
                                field_parts.append(s.IDENT().getText())

                        return self.emit_load_array_record_field(
                            ctx,
                            var_name,
                            list(first.expr()),
                            field_parts
                        )
                    
                    # normales a[0]
                    return self.emit_load_array_element(
                        ctx,
                        var_name,
                        list(first.expr())
                    )
                
                if first.DOT():
                    parts = [ref.IDENT().getText()]
                    
                    for s in suffixes:
                        if s.DOT():
                            parts.append(s.IDENT().getText())
                    
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

            func = self.find_function(name)
            if func:
                params = func.get("params", [])

                if len(params) == 0:
                    self.emit("a.sub(x86::rsp, 32); // shadow space for parameterless function call")
                    self.emit(f"a.call({func['label']});")
                    self.emit("a.add(x86::rsp, 32);")
                    return func["return_type"].lower()

                raise CompileError(ctx, "E0005", got="0", expected=str(len(params)))

            raise CompileError(ctx, "E0001", name=name)
    
        # Function call zuerst
        if ctx.functionCallExpr():
            return self.visit(ctx.functionCallExpr())

        # Klammerausdruck nur wenn wirklich vorhanden
        expr_list = ctx.expr()
        if expr_list:
            if isinstance(expr_list, list):
                if len(expr_list) > 0:
                    return self.visit(expr_list[0])
            else:
                return self.visit(expr_list)

        # Integer
        if ctx.NUMBER():
            value = ctx.NUMBER().getText()
            self.emit(f"a.mov(x86::eax, {value});")
            return "integer"

        # Double
        if ctx.FLOATNUMBER():
            value = ctx.FLOATNUMBER().getText()
            return self.emit_load_double_literal(value)

        # String
        if ctx.STRING():
            value = ctx.STRING().getText()[1:-1]
            label = self.add_string_literal(value)
            self.emit(f"a.mov(x86::rax, imm((uint64_t){label}));")
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

            # parameterlose Funktion ohne Klammern:
            func = self.find_function(name)
            if func:
                params = func.get("params", [])

                if len(params) == 0:
                    self.emit("a.sub(x86::rsp, 32); // shadow space for parameterless function call")
                    self.emit(f"a.call({func['label']});")
                    self.emit("a.add(x86::rsp, 32);")
                    return func["return_type"].lower()

                raise CompileError(ctx, "E0005", got="0", expected=str(len(params)))

            raise CompileError(ctx, "E0001", name=name)

        raise CompileError(ctx, "E0015", text=text)
    
    def visitFunctionCallExpr(self, ctx):
        name = ctx.IDENT().getText()
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

                self.emit(f"a.mov(x86::{int_regs[index]}, x86::eax);")
            else:
                raise CompileError(ctx, "E0005", got=formal["type"], expected="integer")

        self.emit("a.sub(x86::rsp, 32); // shadow space for function call")
        self.emit(f"a.call({func['label']});")
        self.emit("a.add(x86::rsp, 32);")

        return func["return_type"].lower()
    
    def visitProcedureDeclaration(self, ctx):
        name = ctx.IDENT().getText()
        key  = name.lower()

        label     = self.new_named_label("proc_" + name)
        end_label = self.new_named_label("endproc_" + name)

        params = self.collect_formal_params(ctx)

        self.procedures[key] = {
            "name": name,
            "label": label,
            "params": params
        }

        param_regs = ["rcx", "rdx", "r8", "r9"]

        if len(params) > len(param_regs):
            raise CompileError(ctx,
                "E0005",
                got="too many params",
                expected="max 4 params")

        self.emit(f"a.jmp({end_label});")
        self.emit(f"a.bind({label});")
        
        self.emit("a.push(x86::rbp);")
        self.emit("a.mov(x86::rbp, x86::rsp);")

        old_params = self.current_proc_params
        self.current_proc_params = {}

        for index, p in enumerate(params):
            reg = param_regs[index]
            pname = p["name"]
            self.emit(f"a.push(x86::{reg}); // save param {pname}")
            
            self.current_proc_params[p["name"].lower()] = {
                "type": p["type"],
                "reg": param_regs[index],
                "stack_offset": -8 * (index + 1)
            }
            
        self.visit(ctx.block())
        
        self.current_proc_params = old_params
        
        self.emit("a.mov(x86::rsp, x86::rbp);")
        self.emit("a.pop(x86::rbp);")
        self.emit("a.ret();")
        
        self.emit(f"a.bind({end_label});")
        return None
    
    def visitProcedureCallStatement(self, ctx):
        name = ctx.IDENT().getText()
        key  = name.lower()
        param_regs = ["rcx", "rdx", "r8", "r9"]
        
        if key not in self.procedures:
            raise CompileError(ctx, "E0001", name=name)

        proc = self.procedures[key]
        params = proc["params"]

        actuals = []
        if ctx.actualParamList():
            actuals = list(ctx.actualParamList().actualParam())

        if len(actuals) != len(params):
            raise CompileError(ctx,
                "E0005",
                got=str(len(actuals)),
                expected=str(len(params)))

        for index, arg in enumerate(actuals):
            formal = params[index]

            if formal["type"] == "integer":
                expr_type = self.visit(arg.expr())

                if expr_type != "integer":
                    raise CompileError(ctx, "E0005", got=expr_type, expected="integer")

                int_regs = ["ecx", "edx", "r8d", "r9d"]
                reg = int_regs[index]
                self.emit(f"a.mov(x86::{reg}, x86::eax);")

            elif formal["type"] == "string":
                if not arg.STRING():
                    raise CompileError(ctx, "E0005", got="expr", expected="string")

                value = arg.STRING().getText()[1:-1]
                label = self.add_string_literal(value)

                reg = param_regs[index]
                self.emit(f"a.mov(x86::{reg}, imm((uint64_t){label}));")

            else:
                raise CompileError(ctx, "E0005", got=formal["type"], expected="string/integer")

        self.emit("a.sub(x86::rsp, 32); // shadow space for procedure call")
        self.emit(f"a.call({proc['label']});")
        self.emit("a.add(x86::rsp, 32);")
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
    
    def visitWriteLnStatement(self, ctx):
        args = ctx.writeArgList()
        
        if args:
            for arg in args.writeArg():
                if arg.STRING():
                    value = arg.STRING().getText()[1:-1]
                    label = self.add_string_literal(value)

                    self.emit(f"a.mov(x86::rcx, imm((uint64_t){label}));")
                    self.emit("a.mov(x86::rax, imm((uint64_t)&jit_print_text));")
                    self.emit_call_rax()
                    
                else:
                    if arg.expr() and arg.expr().getText().lower() in self.current_proc_params:
                        pname = arg.expr().getText().lower()
                        pinfo = self.current_proc_params[pname]
                        
                        if pinfo["type"] == "integer":
                            offset = pinfo["stack_offset"]
                            offset = pinfo["stack_offset"]
                            self.emit(f"a.mov(x86::eax, x86::dword_ptr(x86::rbp, {offset})); // load integer parameter")
                            self.emit("a.mov(x86::ecx, x86::eax);")
                            self.emit("a.mov(x86::rax, imm((uint64_t)&jit_print_int));")
                            self.emit_call_rax()
                            continue
                            
                        if pinfo["type"] == "string":
                            offset = pinfo["stack_offset"]
                            self.emit(f"a.mov(x86::rcx, x86::qword_ptr(x86::rbp, {offset})); // load string parameter")
                            self.emit("a.mov(x86::rax, imm((uint64_t)&jit_print_text));")
                            self.emit_call_rax()
                            continue
                    
                    expr_type = self.visit(arg.expr())
                    
                    if expr_type == "string":
                        self.emit("a.mov(x86::rcx, x86::rax);")
                        self.emit("a.mov(x86::rax, imm((uint64_t)&jit_print_text));")
                        self.emit_call_rax()
                    
                    if expr_type == "integer":
                        self.emit("a.mov(x86::ecx, x86::eax);")
                        self.emit("a.mov(x86::rax, imm((uint64_t)&jit_print_int));")
                        self.emit_call_rax()
                    
                    elif expr_type == "double":
                        # Windows x64: double-Argument liegt in xmm0
                        self.emit("a.mov(x86::rax, imm((uint64_t)&jit_print_double));")
                        self.emit_call_rax()
        
        self.emit("a.mov(x86::rax, imm((uint64_t)&jit_print_newline));")
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

        self.emit(f"Label {name} = a.new_label();")

        self.add_asm_label_mapping(
            asmjit_label,
            name
        )

        return name
    
    def render_asm_double_replacements(self):
        out = []
        for name, value in self.double_literals:
            out.append(
                f'replace_all(asm_text, std::to_string(double_to_bits({value})), "{name}");'
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
            out.append(
                f'static const char {name}[] = "{self.cpp_escape(text)}";'
            )

        return "\n".join(out)
    
    def render_asm_double_symbols(self):
        out = []
        for name, value in self.double_literals:
            out.append(f'asm_out << "{name} equ " << std::to_string(double_to_bits({value})) << " ; {value}\\n";')
        return "\n    ".join(out)
    
    def render_asm_nasm_header(self):
        return f"""
    asm_out << "; {COMMENT_REPL}\\n";
    asm_out << "; GENERATED WITH PYTHON 3.14 ON: {datetime.now().strftime("%Y-%m-%d")}\\n";
    asm_out << "; Copyright (c) 2026 by Jens Kallup - paule32\\n";
    asm_out << "; all rights reserved.\\n";
    asm_out << "; {COMMENT_REPL}\\n\\n";
    """
    
    def render_asm_nasm_structs(self):
        return r"""
    asm_out << "struc JitContext\n";
    asm_out << "    .int_vars:         resq 1\n";
    asm_out << "    .double_vars:      resq 1\n";
    asm_out << "    .print_int_tmp:    resd 1\n";
    asm_out << "    .print_double_tmp: resq 1\n";
    asm_out << "endstruc\n\n";
    """

    def render_asm_context_replacements(self):
        return r"""
    replace_all(asm_text, "[r12]",     "[r12 + JitContext.int_vars]");
    replace_all(asm_text, "[r12+8]",   "[r12 + JitContext.double_vars]");
    replace_all(asm_text, "[r12+16]",  "[r12 + JitContext.print_int_tmp]");
    replace_all(asm_text, "[r12+24]",  "[r12 + JitContext.print_double_tmp]");
    """
    
    def render_asm_extern_symbols(self):
        out = []

        if not self.emit_local_string_data:
            for name, text in self.string_literals:
                out.append(f'asm_out << "extern _{name}\\n";')

            if self.string_literals:
                out.append('asm_out << "\\n";')

        out.append('asm_out << "extern _jit_print_text\\n";')
        out.append('asm_out << "extern _jit_print_int\\n";')
        out.append('asm_out << "extern _jit_print_double\\n";')
        out.append('asm_out << "extern _jit_print_newline\\n";')

        return "\n    ".join(out)
    
    def render_asm_string_mappings(self):
        out = []
        for name, text in self.string_literals:
            out.append(
                f'symbols.add(std::to_string((uint64_t)&{name}), "_{name}");'
            )
        return "\n    ".join(out)
        
    def render_asm_string_data(self):
        if not self.emit_local_string_data:
            return ""

        out = []
        out.append('asm_out << "\\nsection .data\\n";')

        for name, text in self.string_literals:
            escaped = self.cpp_escape(text)
            out.append(f'asm_out << "_{name} db \\"{escaped}\\", 0\\n";')

        return "\n    ".join(out)
    
    def render_asm_label_mappings(self):
        out = []
        for item in self.asm_label_mappings:
            out.append(f'labels.add("{item["asmjit"]}", "{item["target"]}");')
        return "\n    ".join(out)
        
    def render_cpp(self):
        body         = "\n".join(self.lines)
        
        var_count    = max(257, self.next_slot)
        int_count    = max(  1, self.next_int_slot)
        
        double_count = max(  1, self.next_double_slot)
        string_count = max(  1, self.next_string_slot)
        record_count = max(  1, self.next_record_slot)
        arrays_count = max(  1, self.next_arrays_slot)
        pointr_count = max(  1, self.next_pointr_slot)
        
        # todo !!!
        self.func_name = "main"
        self.date_str  = datetime.now().strftime("%Y-%m-%d")
        
        return f'''// automaically created per Python 3.14 script on: {self.date_str}
//
// DON'T MODIFIED THIS CODE. ALL CHANGES WILL BE LOST BY NEXT RUN !
// Copyright (c) 2026 by Jens Kallup - paule32
// all rights reserved.
//
# include "runtime/dbase2many.hpp"

using namespace std;
using namespace asmjit;

{self.render_string_literals()}

int main() {{
    JitRuntime rt;

    CodeHolder code;
    code.init(rt.environment());
    
    StringLogger logger;
    
    logger.options().set_indentation(FormatIndentationGroup::kCode, 1);
    logger.options().set_padding(FormatPaddingGroup::kMachineCode, 0);
    
    code.set_logger(&logger);
    x86::Assembler a(&code);

{body}
    a.add(x86::rsp, 8); // undo alignment
    a.pop(x86::rbx);
    a.pop(x86::r12);
    a.ret();

    JitFunc fn = nullptr;
    Error err = rt.add(&fn, &code);
    if (err != Error::kOk) {{
        std::cerr << \"AsmJit error: \" << DebugUtils::error_as_string(err) << std::endl;
        return 1;
    }}
    
    std::ofstream asm_out(\"{self.asm_file}\");
    std::string asm_text = logger.data();

    replace_all_fun(asm_text);
    
    SymbolMappings symbols;
    {self.render_asm_string_mappings()}
    symbols.apply(asm_text);
    
    LabelMappings labels;
    {self.render_asm_label_mappings()}
    labels.apply(asm_text);

    replace_all_ptr(asm_text);
    
    
    {self.render_asm_context_replacements()}
    
    {self.render_asm_nasm_header()}
    {self.render_asm_nasm_structs()}
    
    {self.render_asm_double_replacements()}
    asm_out << "\\n";

    std::istringstream iss(asm_text);
    std::string line;

    {self.render_asm_double_symbols()}
    {self.render_asm_extern_symbols()}
    
    asm_out << "\\n";
    asm_out << "section .text\\n";
    asm_out << \"global \" << \"_{self.func_name}\" << \"\\n\";
    asm_out << \"_{self.func_name}\" << \":\\n\";
    
    replace_all_str(asm_text, asm_out);
    
    {self.render_asm_string_data()}
    
    asm_out.close();
   
    std::array<int,         {int_count}> int_vars{{}};
    std::array<double,      {double_count}> double_vars{{}};
    std::array<const char*, {string_count}> string_vars{{}};
    std::array<uint8_t,     {record_count}> record_vars{{}};
    std::array<uint8_t,     {arrays_count}> arrays_vars{{}};
    std::array<uint64_t,    {pointr_count}> pointr_vars{{}};
    
    JitContext ctx{{}};
    ctx.int_vars    = int_vars.data();
    
    ctx.double_vars = double_vars.data();
    ctx.string_vars = string_vars.data();
    ctx.record_vars = record_vars.data();
    ctx.arrays_vars = arrays_vars.data();
    ctx.pointr_vars = pointr_vars.data();
    
    fn(&ctx);

    rt.release(fn);
    return 0;
}}
'''

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

def main():
    if len(sys.argv) != 2:
        print("Usage: python pascal_to_asmjit.py file.pas", file=sys.stderr)
        return 1
    
    generator   = None
    source_file = ""
    
    try:
        source_file = sys.argv[1]
        base_name   = os.path.basename(source_file)
        asm_file    = os.path.splitext(base_name)[0] + ".asm"
        
        stream = FileStream(sys.argv[1], encoding="utf-8")
        lexer  = MiniPascalLexer(stream)
        tokens = CommonTokenStream(lexer)
        parser = MiniPascalParser(tokens)
        
        tree = parser.programFile()
        
        if parser.getNumberOfSyntaxErrors() > 0:
            return 1
        
        generator = AsmJitGenerator(asm_file)
        cpp = generator.visit(tree)
        print(cpp)
        return 0
        
    except CompileError as e:
        if generator is not None:
            print(generator.format_error(source_file, e), file = sys.stderr)
            return 2
        else:
            print(e, file = sys.stderr)
            return 2
            
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
