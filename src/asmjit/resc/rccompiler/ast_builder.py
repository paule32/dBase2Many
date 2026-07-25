from __future__ import annotations

from pathlib import Path
from typing import Any

from antlr4 import TerminalNode

from .constants import (
    CONSTANTS,
    CONTROL_DEFAULTS,
    DIALOG_CLASS_ORDINALS,
    RESOURCE_TYPE_NAMES,
)
from .model import (
    AcceleratorEntry,
    AcceleratorResource,
    DialogControl,
    DialogFont,
    DialogResource,
    FileResource,
    MenuItem,
    MenuResource,
    RawItem,
    RawResource,
    ResourceId,
    ResourceOptions,
    ResourceUnit,
    SourceLocation,
    StringTable,
    VersionBlock,
    VersionInfo,
    VersionValue,
)
from .util import decode_rc_string, parse_integer_literal
from .generated.ResourceParserVisitor import ResourceParserVisitor


class SemanticError(RuntimeError):
    pass


class ResourceAstBuilder(ResourceParserVisitor):
    def __init__(
        self,
        *,
        filename: Path,
        symbols: dict[str, int] | None = None,
    ) -> None:
        super().__init__()
        self.filename = Path(filename).resolve()
        self.source_directory = self.filename.parent
        self.symbols = dict(CONSTANTS)
        if symbols:
            self.symbols.update({str(k): int(v) for k, v in symbols.items()})
        self.unit = ResourceUnit()
        self.current_language = 0
        self.current_characteristics = 0
        self.current_version = 0

    def location(self, ctx) -> SourceLocation:
        return SourceLocation(
            filename=str(self.filename),
            line=int(ctx.start.line),
            column=int(ctx.start.column),
        )

    def error(self, ctx, message: str) -> SemanticError:
        loc = self.location(ctx)
        return SemanticError(
            f"{loc.filename}:{loc.line}:{loc.column + 1}: {message}"
        )

    def visitResourceScript(self, ctx):
        for statement in ctx.resourceStatement():
            self.visit(statement)
        self.unit.default_language = self.current_language
        return self.unit

    def visitResourceStatement(self, ctx):
        for child in ctx.getChildren():
            if not isinstance(child, TerminalNode):
                result = self.visit(child)
                if result is not None:
                    return result
        return None

    def visitLanguageStatement(self, ctx):
        expressions = ctx.expression()
        primary = self.eval_expr(expressions[0]) & 0x3FF
        sublanguage = self.eval_expr(expressions[1]) & 0x3F
        self.current_language = primary | (sublanguage << 10)
        return self.current_language

    def visitCharacteristicsStatement(self, ctx):
        self.current_characteristics = self.eval_expr(ctx.expression()) & 0xFFFFFFFF

    def visitVersionStatement(self, ctx):
        self.current_version = self.eval_expr(ctx.expression()) & 0xFFFFFFFF

    def make_options(self, ctx) -> ResourceOptions:
        result = ResourceOptions(
            language=self.current_language,
            characteristics=self.current_characteristics,
            version=self.current_version,
        )
        if ctx is None:
            return result

        expressions = list(ctx.expression())
        expression_index = 0
        children = list(ctx.getChildren())
        i = 0

        while i < len(children):
            child = children[i]
            text = child.getText().upper()
            if text in {
                "MOVEABLE", "FIXED", "PURE", "IMPURE",
                "PRELOAD", "LOADONCALL", "DISCARDABLE",
            }:
                result.memory_flags.add(text)
            elif text == "LANGUAGE":
                if expression_index + 1 >= len(expressions):
                    raise self.error(ctx, "LANGUAGE option requires two expressions")
                primary = self.eval_expr(expressions[expression_index]) & 0x3FF
                sublanguage = self.eval_expr(expressions[expression_index + 1]) & 0x3F
                result.language = primary | (sublanguage << 10)
                expression_index += 2
            elif text == "CHARACTERISTICS":
                result.characteristics = self.eval_expr(expressions[expression_index]) & 0xFFFFFFFF
                expression_index += 1
            elif text == "VERSION":
                result.version = self.eval_expr(expressions[expression_index]) & 0xFFFFFFFF
                expression_index += 1
            i += 1
        return result

    def parse_resource_id(self, ctx) -> ResourceId:
        if ctx.INTEGER():
            return parse_integer_literal(ctx.INTEGER().getText())[0]
        if ctx.STRING():
            return decode_rc_string(ctx.STRING().getText())[0]
        name = ctx.IDENTIFIER().getText()
        if name in self.symbols:
            return self.symbols[name]
        return name

    def parse_resource_type(self, ctx) -> ResourceId:
        if ctx.INTEGER():
            return parse_integer_literal(ctx.INTEGER().getText())[0]
        if ctx.STRING():
            return decode_rc_string(ctx.STRING().getText())[0]
        name = ctx.IDENTIFIER().getText()
        return RESOURCE_TYPE_NAMES.get(name.upper(), self.symbols.get(name, name))

    def parse_string(self, ctx) -> tuple[str, bool]:
        return decode_rc_string(ctx.getText())

    def visitFileResource(self, ctx):
        name_id = self.parse_resource_id(ctx.resourceId())
        kind_ctx = ctx.fileResourceKind()
        if kind_ctx.fileResourceType():
            type_name: ResourceId = kind_ctx.fileResourceType().getText().upper()
        else:
            type_name = self.parse_resource_type(kind_ctx.resourceType())
        filename = self.parse_string(ctx.stringLiteral())[0]
        path = Path(filename)
        if not path.is_absolute():
            path = self.source_directory / path
        resource = FileResource(
            name_id=name_id,
            type_name=type_name,
            filename=path.resolve(),
            options=self.make_options(ctx.resourceOptions()),
            location=self.location(ctx),
        )
        self.unit.resources.append(resource)
        return resource

    def visitRawResource(self, ctx):
        resource = RawResource(
            name_id=self.parse_resource_id(ctx.resourceId()),
            type_id=(
                RESOURCE_TYPE_NAMES.get(
                    ctx.rawResourceType().getText().upper(),
                    self.parse_resource_type(ctx.rawResourceType().resourceType())
                    if ctx.rawResourceType().resourceType()
                    else ctx.rawResourceType().getText()
                )
            ),
            items=self.parse_raw_data(ctx.rawDataBlock()),
            options=self.make_options(ctx.resourceOptions()),
            location=self.location(ctx),
        )
        self.unit.resources.append(resource)
        return resource

    def parse_raw_data(self, ctx) -> list[RawItem]:
        item_list = ctx.rawDataItemList()
        if item_list is None:
            return []
        result: list[RawItem] = []
        for item in item_list.rawDataItem():
            if item.stringLiteral():
                value, wide = self.parse_string(item.stringLiteral())
                result.append(RawItem(value=value, wide=wide))
            else:
                expression = item.expression()
                value = self.eval_expr(expression)
                # The L suffix only matters for a single integer literal.
                text = expression.getText()
                dword = False
                try:
                    _, dword = parse_integer_literal(text)
                except Exception:
                    pass
                result.append(RawItem(value=value, dword=dword))
        return result

    def visitStringTableResource(self, ctx):
        entries: dict[int, str] = {}
        for entry in ctx.stringEntry():
            string_id = self.eval_expr(entry.expression())
            if not 0 <= string_id <= 0xFFFF:
                raise self.error(entry, f"STRINGTABLE id out of range: {string_id}")
            if string_id in entries:
                raise self.error(entry, f"duplicate STRINGTABLE id: {string_id}")
            entries[string_id] = self.parse_string(entry.stringLiteral())[0]
        resource = StringTable(
            entries=entries,
            options=self.make_options(ctx.resourceOptions()),
            location=self.location(ctx),
        )
        self.unit.resources.append(resource)
        return resource

    def visitVersionInfoResource(self, ctx):
        resource = VersionInfo(
            name_id=self.parse_resource_id(ctx.resourceId()),
            options=self.make_options(ctx.resourceOptions()),
            location=self.location(ctx),
        )
        for line in ctx.fixedVersionLine():
            if line.FILEVERSION():
                resource.file_version = self.quad(line.quadExpression())
            elif line.PRODUCTVERSION():
                resource.product_version = self.quad(line.quadExpression())
            elif line.FILEFLAGSMASK():
                resource.file_flags_mask = self.eval_expr(line.expression())
            elif line.FILEFLAGS():
                resource.file_flags = self.eval_expr(line.expression())
            elif line.FILEOS():
                resource.file_os = self.eval_expr(line.expression())
            elif line.FILETYPE():
                resource.file_type = self.eval_expr(line.expression())
            elif line.FILESUBTYPE():
                resource.file_subtype = self.eval_expr(line.expression())
        for element in ctx.versionElement():
            parsed = self.parse_version_element(element)
            if parsed is not None:
                resource.children.append(parsed)
        self.unit.resources.append(resource)
        return resource

    def quad(self, ctx) -> tuple[int, int, int, int]:
        values = tuple(self.eval_expr(item) & 0xFFFF for item in ctx.expression())
        if len(values) != 4:
            raise self.error(ctx, "version tuple requires four values")
        return values  # type: ignore[return-value]

    def parse_version_element(self, ctx):
        if ctx.versionBlock():
            block_ctx = ctx.versionBlock()
            block = VersionBlock(key=self.parse_string(block_ctx.stringLiteral())[0])
            for element in block_ctx.versionElement():
                child = self.parse_version_element(element)
                if child is not None:
                    block.children.append(child)
            return block
        if ctx.versionValue():
            value_ctx = ctx.versionValue()
            values: list[int | str] = []
            for item in value_ctx.versionValueItem():
                if item.stringLiteral():
                    values.append(self.parse_string(item.stringLiteral())[0])
                else:
                    values.append(self.eval_expr(item.expression()))
            return VersionValue(
                key=self.parse_string(value_ctx.stringLiteral())[0],
                values=values,
            )
        return None

    def visitMenuResource(self, ctx):
        extended = ctx.MENUEX() is not None
        items = [self.parse_menu_item(item, extended) for item in ctx.menuItem()]
        resource = MenuResource(
            name_id=self.parse_resource_id(ctx.resourceId()),
            extended=extended,
            items=items,
            options=self.make_options(ctx.resourceOptions()),
            location=self.location(ctx),
        )
        self.unit.resources.append(resource)
        return resource

    def parse_menu_item(self, ctx, extended: bool) -> MenuItem:
        if ctx.POPUP():
            item = MenuItem(
                text=self.parse_string(ctx.stringLiteral())[0],
                popup=True,
                children=[self.parse_menu_item(child, extended) for child in ctx.menuItem()],
            )
        elif ctx.SEPARATOR():
            item = MenuItem(separator=True, flags=0x0800, type_flags=0x0800)
        else:
            item = MenuItem(
                text=self.parse_string(ctx.stringLiteral())[0],
                item_id=self.eval_expr(ctx.expression()),
            )
        flags_ctx = ctx.menuFlags()
        if flags_ctx:
            for child in flags_ctx.getChildren():
                text = child.getText().upper()
                mapping = {
                    "CHECKED": 0x0008,
                    "GRAYED": 0x0001,
                    "HELP": 0x4000,
                    "INACTIVE": 0x0002,
                    "MENUBARBREAK": 0x0020,
                    "MENUBREAK": 0x0040,
                }
                if text in mapping:
                    item.flags |= mapping[text]
                    item.state_flags |= mapping[text]
            for expression in flags_ctx.expression():
                value = self.eval_expr(expression)
                item.flags |= value
                item.type_flags |= value
        return item

    def visitAcceleratorsResource(self, ctx):
        entries: list[AcceleratorEntry] = []
        for entry_ctx in ctx.acceleratorEntry():
            key_ctx = entry_ctx.acceleratorKey()
            if key_ctx.stringLiteral():
                text = self.parse_string(key_ctx.stringLiteral())[0]
                if not text:
                    raise self.error(key_ctx, "empty accelerator key")
                if len(text) == 2 and text[0] == "^":
                    key = ord(text[1].upper()) - ord("A") + 1
                else:
                    key = ord(text[0])
            else:
                key = self.eval_expr(key_ctx.expression())
            flags = 0
            flags_ctx = entry_ctx.acceleratorFlags()
            if flags_ctx:
                mapping = {
                    "VIRTKEY": 0x01,
                    "ASCII": 0x00,
                    "NOINVERT": 0x02,
                    "SHIFT": 0x04,
                    "CONTROL": 0x08,
                    "ALT": 0x10,
                }
                for child in flags_ctx.getChildren():
                    flags |= mapping.get(child.getText().upper(), 0)
            entries.append(AcceleratorEntry(
                key=key,
                command_id=self.eval_expr(entry_ctx.expression()),
                flags=flags,
            ))
        resource = AcceleratorResource(
            name_id=self.parse_resource_id(ctx.resourceId()),
            entries=entries,
            options=self.make_options(ctx.resourceOptions()),
            location=self.location(ctx),
        )
        self.unit.resources.append(resource)
        return resource

    def visitDialogResource(self, ctx):
        coords = [self.eval_expr(item) for item in ctx.expression()]
        if len(coords) < 4:
            raise self.error(ctx, "dialog needs x, y, width and height")
        dialog = DialogResource(
            name_id=self.parse_resource_id(ctx.resourceId()),
            extended=ctx.dialogKind().DIALOGEX() is not None,
            x=coords[0], y=coords[1], width=coords[2], height=coords[3],
            options=self.make_options(ctx.resourceOptions()),
            location=self.location(ctx),
        )
        for line in ctx.dialogHeaderLine():
            if line.STYLE():
                dialog.style = self.eval_expr(line.expression()[0])
            elif line.EXSTYLE():
                dialog.exstyle = self.eval_expr(line.expression()[0])
            elif line.CAPTION():
                dialog.caption = self.parse_string(line.stringLiteral())[0]
            elif line.CLASS():
                dialog.window_class = self.parse_resource_id(line.resourceId())
            elif line.MENU():
                dialog.menu = self.parse_resource_id(line.resourceId())
            elif line.FONT():
                expressions = line.expression()
                dialog.font = DialogFont(
                    point_size=self.eval_expr(expressions[0]),
                    face=self.parse_string(line.stringLiteral())[0],
                    weight=self.eval_expr(expressions[1]) if len(expressions) > 1 else 0,
                    italic=self.eval_expr(expressions[2]) if len(expressions) > 2 else 0,
                    charset=self.eval_expr(expressions[3]) if len(expressions) > 3 else 1,
                )
                dialog.style |= 0x0040
            elif line.LANGUAGE():
                expressions = line.expression()
                primary = self.eval_expr(expressions[0]) & 0x3FF
                sub = self.eval_expr(expressions[1]) & 0x3F
                dialog.options.language = primary | (sub << 10)
            elif line.CHARACTERISTICS():
                dialog.options.characteristics = self.eval_expr(line.expression()[0])
            elif line.VERSION():
                dialog.options.version = self.eval_expr(line.expression()[0])
        dialog.controls = [self.parse_dialog_control(item) for item in ctx.dialogControl()]
        self.unit.resources.append(dialog)
        return dialog

    def parse_dialog_control(self, ctx) -> DialogControl:
        expressions = [self.eval_expr(item) for item in ctx.expression()]
        if ctx.CONTROL():
            text: ResourceId | str = self.parse_string(ctx.stringLiteral())[0]
            if len(expressions) < 7:
                raise self.error(ctx, "CONTROL requires id, style and rectangle")
            control_id = expressions[0]
            class_id = self.parse_resource_id(ctx.resourceId())
            style = expressions[1]
            x, y, width, height = expressions[2:6]
            exstyle = expressions[6] if len(expressions) > 6 else 0
            kind = "CONTROL"
        elif ctx.controlWithText():
            kind = ctx.controlWithText().getText().upper()
            text = self.parse_string(ctx.stringLiteral())[0]
            if len(expressions) < 5:
                raise self.error(ctx, f"{kind} requires id and rectangle")
            control_id = expressions[0]
            x, y, width, height = expressions[1:5]
            extra_style = expressions[5] if len(expressions) > 5 else 0
            exstyle = expressions[6] if len(expressions) > 6 else 0
            class_name, default_style = CONTROL_DEFAULTS[kind]
            class_id = DIALOG_CLASS_ORDINALS[class_name]
            style = 0x50000000 | default_style | extra_style
        elif ctx.controlWithoutText():
            kind = ctx.controlWithoutText().getText().upper()
            text = ""
            if len(expressions) < 5:
                raise self.error(ctx, f"{kind} requires id and rectangle")
            control_id = expressions[0]
            x, y, width, height = expressions[1:5]
            extra_style = expressions[5] if len(expressions) > 5 else 0
            exstyle = expressions[6] if len(expressions) > 6 else 0
            class_name, default_style = CONTROL_DEFAULTS[kind]
            class_id = DIALOG_CLASS_ORDINALS[class_name]
            style = 0x50000000 | default_style | extra_style
        else:
            kind = "ICON"
            text = self.parse_resource_id(ctx.resourceId())
            if len(expressions) < 5:
                raise self.error(ctx, "ICON control requires id and rectangle")
            control_id = expressions[0]
            x, y, width, height = expressions[1:5]
            extra_style = expressions[5] if len(expressions) > 5 else 0
            exstyle = expressions[6] if len(expressions) > 6 else 0
            class_id = DIALOG_CLASS_ORDINALS["STATIC"]
            style = 0x50000003 | extra_style
        return DialogControl(
            kind=kind,
            text=text,
            control_id=control_id,
            class_id=class_id,
            style=style,
            exstyle=exstyle,
            x=x, y=y, width=width, height=height,
        )

    def eval_expr(self, ctx) -> int:
        if ctx is None:
            raise SemanticError("missing expression")
        count = ctx.getChildCount()
        if count == 1:
            child = ctx.getChild(0)
            if isinstance(child, TerminalNode):
                text = child.getText()
                token_type = child.symbol.type
                if hasattr(ctx, "INTEGER") and ctx.INTEGER():
                    return parse_integer_literal(text)[0]
                if hasattr(ctx, "IDENTIFIER") and ctx.IDENTIFIER():
                    if text not in self.symbols:
                        raise self.error(ctx, f"unknown constant in expression: {text}")
                    return int(self.symbols[text])
                # Wrapper contexts contain another parser context.
            return self.eval_expr(child)
        if count == 2:
            op = ctx.getChild(0).getText()
            value = self.eval_expr(ctx.getChild(1))
            return {"+": value, "-": -value, "~": ~value}[op]
        if count == 3 and ctx.getChild(0).getText() == "(":
            return self.eval_expr(ctx.getChild(1))

        value = self.eval_expr(ctx.getChild(0))
        index = 1
        while index < count:
            op = ctx.getChild(index).getText()
            right = self.eval_expr(ctx.getChild(index + 1))
            if op == "|": value |= right
            elif op == "^": value ^= right
            elif op == "&": value &= right
            elif op == "<<": value <<= right
            elif op == ">>": value >>= right
            elif op == "+": value += right
            elif op == "-": value -= right
            elif op == "*": value *= right
            elif op == "/":
                if right == 0: raise self.error(ctx, "division by zero")
                value = int(value / right)
            elif op == "%":
                if right == 0: raise self.error(ctx, "division by zero")
                value %= right
            else:
                raise self.error(ctx, f"unsupported expression operator: {op}")
            index += 2
        return value
