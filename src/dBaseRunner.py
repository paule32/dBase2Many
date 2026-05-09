# ---------------------------------------------------------------------------
# \file  : dbaseRunner.py
# \author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# \note  : All rights reserved
# ---------------------------------------------------------------------------
from __future__ import annotations

import sys

# -----------------------------------------------------------------------
from share                import run_language_app
from share.common         import *
# -----------------------------------------------------------------------
# graphical widgets for user interface ...
# -----------------------------------------------------------------------
from share.widgets.button import *

from share.editors.editor import FileEditorWindow
from share.editors.dbase  import *

# -----------------------------------------------------------------------
# dbase interpreter lexer + parser ...
# -----------------------------------------------------------------------
from parse.dbase.dBaseLexer          import dBaseLexer
from parse.dbase.dBaseParser         import dBaseParser
from parse.dbase.dBaseParserVisitor  import dBaseParserVisitor

# -----------------------------------------------------------------------
# parser logic ...
# -----------------------------------------------------------------------
from parse.dbase.parser              import *

class Symbols:
    def __init__(self) -> None:
        self.classes: Dict[str, object] = {}

    def has_class(self, name: str) -> bool:
        # dBase ist oft case-insensitive -> normalisieren:
        return name.upper() in self.classes

    def add_class(self, name: str, node: object) -> None:
        self.classes[name.upper()] = node
        
class SemanticVisitor(dBaseParserVisitor):
    def __init__(self):
        super().__init__()
        self.symbols = Symbols()
        self.classes = self.symbols.classes   # <- Alias
        self.errors: List[CompileError] = []
        self._current_class = None

    def error(self, ctx, msg: str):
        tok = ctx.start
        self.errors.append(CompileError(tok.line, tok.column, msg))
    
    def visitClassBody(self, ctx):
        # NUR member besuchen
        for m in ctx.classMember():
            self.visit(m)
        return None

def analyze(tree, parser):
    sema = SemanticVisitor()
    sema.visit(tree)

    if sema.errors:
        for e in sema.errors:
            _debug_print(f"{e.line}:{e.column}: error: {e.message}")
        raise SystemExit(1)

    return sema


class PasEmitter:
    def __init__(self):
        self.lines = []
        self.level = 0

    def emit(self, line=""):
        self.lines.append(("  " * self.level) + line)

    def indent(self): self.level += 1
    def dedent(self): self.level = max(0, self.level - 1)

    def text(self):
        return "\n".join(self.lines) + "\n"

class CppEmitter:
    def __init__(self):
        self.lines = []
        self.level = 0

    def emit(self, line=""):
        self.lines.append(("  " * self.level) + line)

    def indent(self): self.level += 1
    def dedent(self): self.level = max(0, self.level - 1)

    def text(self):
        return "\n".join(self.lines) + "\n"

class JavaEmitter:
    def __init__(self):
        self.lines = []
        self.level = 0

    def emit(self, line=""):
        self.lines.append(("  " * self.level) + line)

    def indent(self): self.level += 1
    def dedent(self): self.level = max(0, self.level - 1)

    def text(self):
        return "\n".join(self.lines) + "\n"

class DBaseToJava:
    def __init__(self, parser, classes=None, class_name="GenProg", package=None):
        self.p = parser
        self.out = JavaEmitter()
        self.classes = classes or {}
        self.class_name = class_name
        self.package = package
        self._tmp_i = 0

    def new_temp(self):
        self._tmp_i += 1
        return f"t{self._tmp_i}"

    def jstr(self, s: str) -> str:
        if os.name == "nt":
            s = s.replace("\\", "\\\\").replace('"', '\\"')
        else:
            s = s.replace("\\", "/")
        s = f'"{str}"'
        return s

    def jstr_list(self, items):
        # java.util.List.of("A","B")
        inner = ", ".join(self.jstr(x) for x in items)
        return f"java.util.List.of({inner})"

    def jval_list(self, exprs):
        # java.util.List.of(a, b, c)
        inner = ", ".join(exprs)
        return f"java.util.List.of({inner})"

    def generate(self, tree, out_path: str):
        o = self.out
        if self.package:
            o.emit(f"package {self.package};")
            o.emit("")
        o.emit("import java.util.*;")
        o.emit("")
        o.emit("public class " + self.class_name + " {")
        o.indent()
        o.emit("public static void main(String[] args) {")
        o.indent()
        o.emit("TRT rt = new TRT();")
        o.emit("try {")
        o.indent()

        self.gen_input(tree)

        o.dedent()
        o.emit("} catch (Exception e) {")
        o.indent()
        o.emit('System.err.println("ERROR: " + e.getMessage());')
        o.emit("e.printStackTrace();")
        o.dedent()
        o.emit("}")
        o.dedent()
        o.emit("}")
        o.dedent()
        o.emit("}")
        Path(out_path).write_text(o.text(), encoding="utf-8")

    # input : item* EOF
    def gen_input(self, ctx):
        for it in ctx.item():
            self.gen_item(it)

    # item : classDecl | methodDecl | statement
    def gen_item(self, it):
        if it.statement():
            return self.gen_stmt(it.statement())
        if it.classDecl():
            self.out.emit("// TODO classDecl not implemented in Java backend")
            return
        if it.methodDecl():
            self.out.emit("// TODO methodDecl not implemented in Java backend")
            return
        self.out.emit("// TODO unhandled item")

    # statement dispatcher (erweitern wie bei Python/Pascal)
    def gen_stmt(self, st):
        if st.writeStmt():         return self.gen_write(st.writeStmt())
        if st.assignStmt():        return self.gen_assign(st.assignStmt())
        if st.localDeclStmt():     return self.gen_local_decl(st.localDeclStmt())
        if st.localAssignStmt():   return self.gen_local_assign(st.localAssignStmt())
        if st.ifStmt():            return self.gen_if(st.ifStmt())
        if st.forStmt():           return self.gen_for(st.forStmt())
        if st.breakStmt():         return self.gen_break(st.breakStmt())
        if st.returnStmt():        return self.gen_return(st.returnStmt())
        if st.withStmt():          return self.gen_with(st.withStmt())
        if st.parameterStmt():     return self.gen_parameter(st.parameterStmt())
        if st.exprStmt():          return self.gen_expr_stmt(st.exprStmt())

        self.out.emit("// TODO unhandled statement: " + type(st.getChild(0)).__name__)

    # writeStmt : WRITE writeArg (PLUS writeArg)* ;
    def gen_write(self, ctx):
        parts = [self.gen_write_arg(a) for a in ctx.writeArg()]
        if not parts:
            self.out.emit("rt.WRITE(TRT.Null());")
            return

        expr = parts[0]
        for p in parts[1:]:
            expr = f"rt.BINOP({expr}, \"+\", {p})"
        self.out.emit(f"rt.WRITE({expr});")

    # writeArg : STRING | dottedRef | expr ;
    def gen_write_arg(self, actx):
        if actx.STRING():
            # actx.STRING().getText() liefert schon Anführungszeichen aus dem Lexer
            return f"TRT.V({actx.STRING().getText()})"
        if actx.dottedRef():
            base, path = self.gen_dotted_ref_parts(actx.dottedRef())
            return f"rt.GET('{base.upper()}', {path})"
        if actx.expr():
            return self.gen_expr(actx.expr())
        return "TRT.Null()"

    def gen_local_decl(self, ctx):
        name = ctx.name.text if hasattr(ctx, "name") else ctx.IDENT().getText()
        self.out.emit(f"rt.SET_NAME({self.jstr(name)}, TRT.Null());")

    def gen_local_assign(self, ctx):
        name = ctx.name.text if hasattr(ctx, "name") else ctx.IDENT().getText()
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.SET_NAME({self.jstr(name)}, {rhs});")

    # lvalue : postfixExpr | dottedRef ;
    def gen_assign(self, ctx):
        rhs = self.gen_expr(ctx.expr())
        lv = ctx.lvalue()

        if lv.dottedRef():
            base, path = self.gen_dotted_ref_parts(lv.dottedRef())
            self.out.emit(f"rt.SET({base}, {path}, {rhs});")
            return

        pe = lv.postfixExpr()
        if pe:
            chain = self.lvalue_chain_from_postfix(pe)

            if len(chain) == 1:
                self.out.emit(f"rt.SET_NAME({self.jstr(chain[0])}, {rhs});")
                return

            head = chain[0]
            if head.upper() == "THIS":
                base = "rt.GET_THIS()"
                path = self.jstr_list(chain[1:])
            else:
                base = f"rt.GET_NAME({self.jstr(head)})"
                path = self.jstr_list(chain[1:])

            self.out.emit(f"rt.SET({base}, {path}, {rhs});")
            return

        self.out.emit("// TODO unsupported lvalue: " + lv.getText())

    # ifStmt : IF expr block (ELSE block)? ENDIF ;
    def gen_if(self, ctx):
        cond = self.gen_expr(ctx.expr())
        self.out.emit(f"if (rt.TRUE({cond})) {{")
        self.out.indent()

        then_block = ctx.block(0)
        for st in then_block.statement():
            self.gen_stmt(st)

        self.out.dedent()
        self.out.emit("}")

        if ctx.ELSE():
            self.out.emit("else {")
            self.out.indent()
            else_block = ctx.block(1)
            for st in else_block.statement():
                self.gen_stmt(st)
            self.out.dedent()
            self.out.emit("}")

    # forStmt : FOR IDENT ASSIGN numberExpr TO numberExpr (STEP numberExpr)? block ENDFOR ;
    def gen_for(self, ctx):
        var = ctx.IDENT().getText()
        start = ctx.numberExpr(0).getText()
        end   = ctx.numberExpr(1).getText()
        step  = ctx.numberExpr(2).getText() if ctx.STEP() else "1"

        self.out.emit(f"rt.SET_NAME({self.jstr(var)}, TRT.V({start}));")
        self.out.emit(f"while (rt.TRUE(rt.FOR_COND(rt.GET_NAME({self.jstr(var)}), TRT.V({end}), TRT.V({step})))) {{")
        self.out.indent()

        for st in ctx.block().statement():
            self.gen_stmt(st)

        self.out.emit(f"rt.SET_NAME({self.jstr(var)}, rt.BINOP(rt.GET_NAME({self.jstr(var)}), \"+\", TRT.V({step})));")
        self.out.dedent()
        self.out.emit("}")

    def gen_break(self, ctx):
        self.out.emit("break;")

    def gen_return(self, ctx):
        # Top-level main: delegiere an Runtime (z.B. Exception oder Flag)
        if ctx.expr():
            self.out.emit(f"rt.RETURN({self.gen_expr(ctx.expr())});")
        else:
            self.out.emit("rt.RETURN(TRT.Null());")

    # parameterStmt : PARAMETER paramNames ;  paramNames : IDENT (',' IDENT)* ;
    def gen_parameter(self, ctx):
        p = ctx.paramNames()
        names = [t.getText() for t in p.IDENT()]
        self.out.emit(f"rt.PARAMETER({self.jstr_list(names)});")

    # exprStmt : postfixExpr ;
    def gen_expr_stmt(self, ctx):
        e = self.gen_postfix(ctx.postfixExpr())
        self.out.emit(e + ";")

    # WITH
    def gen_with(self, ctx):
        base = self.gen_with_target(ctx.withTarget())
        tmp = self.new_temp()
        self.out.emit(f"Object {tmp} = {base};")
        self.out.emit(f"rt.PUSH_WITH({tmp});")

        body = ctx.withBody()
        for ch in list(getattr(body, "children", []) or []):
            t = type(ch).__name__
            if t.endswith("WithAssignStmtContext"):
                self.gen_with_assign(ch)
            elif t.endswith("WithStmtContext"):
                self.gen_with(ch)
            elif t.endswith("StatementContext"):
                self.gen_stmt(ch)

        self.out.emit("rt.POP_WITH();")

    def gen_with_target(self, ctx):
        if ctx.THIS():
            return "rt.GET_THIS()"
        if ctx.dottedRef():
            base, path = self.gen_dotted_ref_parts(ctx.dottedRef())
            return f"rt.GET(\"{base.upper()}\", {path})"
        if ctx.IDENT():
            return f"rt.GET_NAME({self.jstr(ctx.IDENT().getText())})"
        if ctx.postfixExpr():
            return self.gen_postfix(ctx.postfixExpr())
        return "TRT.Null()"

    def gen_with_assign(self, ctx):
        path = [t.getText() for t in ctx.withLvalue().IDENT()]
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.WITH_SET({self.jstr_list(path)}, {rhs});")

    # ----- expr/postfix/primary (runtime-backed) -----
    def gen_expr(self, ctx):
        return self.gen_logical_or(ctx.logicalOr())

    def gen_logical_or(self, ctx):
        parts = [self.gen_logical_and(x) for x in ctx.logicalAnd()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, \"OR\", {rhs})"
        return out

    def gen_logical_and(self, ctx):
        parts = [self.gen_logical_not(x) for x in ctx.logicalNot()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, \"AND\", {rhs})"
        return out

    def gen_logical_not(self, ctx):
        if ctx.NOT():
            inner = self.gen_logical_not(ctx.logicalNot())
            return f"rt.UNOP(\"NOT\", {inner})"
        return self.gen_comparison(ctx.comparison())

    def gen_comparison(self, ctx):
        left = self.gen_additive(ctx.additiveExpr(0))
        if ctx.compareOp():
            op = ctx.compareOp().getText()
            right = self.gen_additive(ctx.additiveExpr(1))
            return f"rt.BINOP({left}, {self.jstr(op)}, {right})"
        return left

    def gen_additive(self, ctx):
        terms = [self.gen_multiplicative(x) for x in ctx.multiplicativeExpr()]
        out = terms[0]
        kids = list(ctx.getChildren())
        i = 1
        while i < len(kids):
            op = kids[i].getText()
            rhs = terms[(i + 1) // 2]
            out = f"rt.BINOP({out}, {self.jstr(op)}, {rhs})"
            i += 2
        return out

    def gen_multiplicative(self, ctx):
        factors = [self.gen_postfix(x) for x in ctx.postfixExpr()]
        out = factors[0]
        kids = list(ctx.getChildren())
        i = 1
        while i < len(kids):
            op = kids[i].getText()
            rhs = factors[(i + 1) // 2]
            out = f"rt.BINOP({out}, {self.jstr(op)}, {rhs})"
            i += 2
        return out

    def gen_postfix(self, ctx):
        cur = self.gen_primary(ctx.primary())
        kids = list(ctx.getChildren())
        k = 1
        while k < len(kids):
            t = kids[k].getText()
            if t == "(":
                args = []
                if kids[k+1].getText() != ")":
                    argctx = kids[k+1]
                    args = [self.gen_expr(e) for e in argctx.expr()]
                    k += 1
                cur = f"rt.CALL_ANY({cur}, {self.jval_list(args)})"
                k += 2
                continue
            if t in (".", "::"):
                name = kids[k+1].getText()
                cur = f"rt.GET_ATTR({cur}, {self.jstr(name)})"
                k += 2
                continue
            k += 1
        return cur

    def gen_primary(self, ctx):
        if ctx.THIS():
            return "rt.GET_THIS()"
        if ctx.STRING():
            return f"TRT.V({ctx.STRING().getText()})"
        if ctx.NUMBER():
            return f"TRT.V({ctx.NUMBER().getText()})"
        if ctx.FLOAT():
            return f"TRT.V({ctx.FLOAT().getText()})"
        if ctx.IDENT():
            return f"rt.GET_NAME({self.jstr(ctx.IDENT().getText())})"
        if ctx.newExpr():
            return self.gen_new(ctx.newExpr())
        if ctx.expr():
            return "(" + self.gen_expr(ctx.expr()) + ")"
        return "TRT.Null()"

    def gen_new(self, ctx):
        class_name = ctx.IDENT().getText()
        args = []
        if ctx.argList():
            args = [self.gen_expr(e) for e in ctx.argList().expr()]
        return f"rt.NEW({self.jstr(class_name)}, {self.jval_list(args)})"

    def gen_dotted_ref_parts(self, dctx):
        parts = [t.getText() for t in dctx.IDENT()]
        head = parts[0]
        if head.upper() == "THIS":
            base = "rt.GET_THIS()"
            path = self.jstr_list(parts[1:])
        else:
            base = f"rt.GET_NAME({self.jstr(head)})"
            path = self.jstr_list(parts[1:])
        return base, path

    def lvalue_chain_from_postfix(self, pe):
        chain = [pe.primary().getText()]
        i = 1
        while i < pe.getChildCount():
            ch = pe.getChild(i).getText()
            if ch == ".":
                chain.append(pe.getChild(i+1).getText())
                i += 2
                continue
            if ch == "(":
                raise RuntimeError(f"LVALUE darf keinen Call enthalten: {pe.getText()}")
            i += 1
        return chain

class DBaseToCSharp:
    def __init__(self, parser, class_name="GenProg", namespace=None, package=None):
        self.parser = parser
        self.class_name = class_name
        # Alias: falls du aus Gewohnheit package übergibst
        self.namespace = namespace if namespace is not None else package

        self.out = []
        self.indent = 0

    # ---------- public API ----------
    def generate(self, tree, outfile):
        self.out = []
        self.indent = 0

        # Header
        self.emit("using System;")
        self.emit()

        if self.namespace:
            self.emit(f"namespace {self.namespace} {{")
            self.indent += 1

        # Wenn tree eine Liste von items ist: iterieren, sonst direkt verarbeiten
        if hasattr(tree, "item"):
            # z.B. input: tree.item() -> liste
            for it in tree.item():
                self.gen_item(it)
        else:
            # fallback
            self.gen_any(tree)

        if self.namespace:
            self.indent -= 1
            self.emit("}")

        code = self.get_code()
        with open(outfile, "w", encoding="utf-8") as f:
            f.write(code)

    # ---------- basics ----------
    def emit(self, s=""):
        self.out.append("    " * self.indent + s)

    def get_code(self):
        return "\n".join(self.out)

    # ---------- generic fallback ----------
    def gen_any(self, node):
        # versuche typische top-level struktur
        if hasattr(node, "classDecl") and node.classDecl():
            return self.gen_class(node.classDecl())
        if hasattr(node, "children"):
            for ch in node.children or []:
                self.gen_any(ch)
        else:
            self.emit(f"// TODO top node: {type(node).__name__}")

    # ---------- dispatcher: item ----------
    def gen_item(self, it):
        if hasattr(it, "classDecl") and it.classDecl():
            return self.gen_class(it.classDecl())
        self.emit(f"// TODO item: {type(it).__name__}")

    # ---------- class ----------
    def gen_class(self, ctx):
        # Wenn du class_name erzwingen willst (z.B. immer "GenProg"), dann:
        # class_name = self.class_name
        class_name = ctx.name.text if hasattr(ctx, "name") else self.class_name
        parent = ctx.parent.text if getattr(ctx, "parent", None) else None

        self.emit(f"public class {class_name}" + (f" : {parent}" if parent else "") + " {")
        self.indent += 1

        body = ctx.classBody() if hasattr(ctx, "classBody") else None
        children = list(getattr(body, "children", []) or []) if body else []

        for ch in children:
            if hasattr(ch, "propertyDecl") and ch.propertyDecl():
                self.gen_property(ch.propertyDecl())
            elif hasattr(ch, "methodDecl") and ch.methodDecl():
                self.gen_method(ch.methodDecl())
            elif hasattr(ch, "initDecl") and ch.initDecl():
                self.gen_init(ch.initDecl(), class_name)
            else:
                self.emit(f"// TODO class body child: {type(ch).__name__}")

        self.indent -= 1
        self.emit("}")
        self.emit()

    # ---------- property ----------
    def gen_property(self, ctx):
        name = ctx.IDENT().getText()
        self.emit(f"public object {name};")

    # ---------- method ----------
    def gen_method(self, ctx):
        name = ctx.IDENT().getText()

        params = []
        if hasattr(ctx, "paramList") and ctx.paramList():
            for p in ctx.paramList().IDENT():
                params.append(f"object {p.getText()}")

        self.emit(f"public object {name}(" + ", ".join(params) + ") {{")
        self.indent += 1

        block = ctx.block()
        for st in self.iter_block_statements(block):
            self._emit_stmt_multiline(self.gen_stmt(st))

        self.emit("return null;")
        self.indent -= 1
        self.emit("}")
        self.emit()

    def get_write_exprs(self, wctx):
        """
        Gibt eine Liste von Expr-Contexts zurück, die WRITE ausgeben soll.
        Funktioniert auch, wenn es kein wctx.expr() gibt.
        """
        if wctx is None:
            return []

        # 1) expr(i) / expr() (ANTLR: expr() kann Liste zurückgeben ODER expr(i) existiert)
        if hasattr(wctx, "expr"):
            expr_attr = getattr(wctx, "expr")
            if callable(expr_attr):
                try:
                    res = expr_attr()  # manche Grammatiken liefern direkt Liste
                    if res is not None:
                        return res if isinstance(res, list) else [res]
                except TypeError:
                    # wahrscheinlich expr(i) Variante
                    pass

            # expr(i) Variante
            try:
                out = []
                i = 0
                while True:
                    out.append(expr_attr(i))
                    i += 1
            except Exception:
                if out:
                    return out

        # 2) exprList().expr()
        if hasattr(wctx, "exprList") and wctx.exprList():
            el = wctx.exprList()
            if hasattr(el, "expr") and callable(el.expr):
                res = el.expr()
                if res is not None:
                    return res if isinstance(res, list) else [res]

        # 3) primary() (WRITE primary)
        if hasattr(wctx, "primary") and wctx.primary():
            p = wctx.primary()
            return p if isinstance(p, list) else [p]

        # 4) Fallback: children nach “Expr/Primary”-ähnlichen Nodes filtern
        kids = list(getattr(wctx, "children", []) or [])
        out = []
        for ch in kids:
            t = type(ch).__name__.lower()
            if "expr" in t or "primary" in t:
                out.append(ch)
        return out
        
    def gen_init(self, ctx, class_name):
        self.emit(f"public {class_name}() {{")
        self.indent += 1
        for st in ctx.block().stmt():
            self._emit_stmt_multiline(self.gen_stmt(st))
        self.indent -= 1
        self.emit("}")
        self.emit()

    def _emit_stmt_multiline(self, s):
        for line in s.split("\n"):
            self.emit(line)

    def get_assign_lhs(self, actx):
        """
        Liefert den linken Teil einer Zuweisung als Context zurück.
        Unterstützt viele Grammatik-Varianten: lhs(), lvalue(), target(), ref(), dottedRef(), primary(), IDENT()
        """
        if actx is None:
            return None

        for name in ("lhs", "lvalue", "target", "left", "ref"):
            fn = getattr(actx, name, None)
            if callable(fn):
                try:
                    res = fn()
                    if res is not None:
                        return res
                except TypeError:
                    pass

        # oft ist LHS ein dottedRef
        if hasattr(actx, "dottedRef") and actx.dottedRef():
            return actx.dottedRef()

        # manchmal ist LHS einfach IDENT
        if hasattr(actx, "IDENT") and actx.IDENT():
            return actx.IDENT()

        # fallback: erstes child nehmen, das wie lvalue/ref aussieht
        kids = list(getattr(actx, "children", []) or [])
        for ch in kids:
            t = type(ch).__name__.lower()
            if "dottedref" in t or "lvalue" in t or "ref" in t or "primary" in t:
                return ch
        return None

    def get_assign_rhs(self, actx):
        """
        Liefert den rechten Teil einer Zuweisung als Expr-Context zurück.
        Häufig: expr() oder expr(i) (meist der letzte expr im AssignStmt)
        """
        if actx is None:
            return None

        if hasattr(actx, "expr") and callable(actx.expr):
            # Fall A: expr() gibt Liste oder einzelnes Element
            try:
                res = actx.expr()
                if isinstance(res, list):
                    return res[-1] if res else None
                if res is not None:
                    return res
            except TypeError:
                # Fall B: expr(i)
                i = 0
                last = None
                while True:
                    try:
                        last = actx.expr(i)
                        i += 1
                    except Exception:
                        break
                return last

        # fallback: letztes child, das wie expr aussieht
        kids = list(getattr(actx, "children", []) or [])
        for ch in reversed(kids):
            if "expr" in type(ch).__name__.lower() or hasattr(ch, "primary"):
                return ch
        return None
    
    def get_for_parts(self, fctx):
        """
        Liefert (var_name, start_expr_ctx, end_expr_ctx, step_expr_ctx, block_ctx)
        ohne vorauszusetzen, dass fctx.expr(i) existiert.
        """
        if fctx is None:
            return (None, None, None, None, None)

        # ---- var ----
        var = None
        if hasattr(fctx, "IDENT") and fctx.IDENT():
            var = fctx.IDENT().getText()

        # ---- block ----
        blk = None
        for bn in ("block", "stmtBlock", "forBlock"):
            fn = getattr(fctx, bn, None)
            if callable(fn):
                try:
                    blk = fn()
                    if blk is not None:
                        break
                except TypeError:
                    pass

        # ---- start/end/step: typische Namen ----
        start = end = step = None
        for sn in ("start", "startExpr", "fromExpr", "exprFrom"):
            fn = getattr(fctx, sn, None)
            if callable(fn):
                try:
                    start = fn()
                    if start is not None:
                        break
                except TypeError:
                    pass

        for en in ("end", "endExpr", "toExpr", "exprTo"):
            fn = getattr(fctx, en, None)
            if callable(fn):
                try:
                    end = fn()
                    if end is not None:
                        break
                except TypeError:
                    pass

        for pn in ("step", "stepExpr", "byExpr"):
            fn = getattr(fctx, pn, None)
            if callable(fn):
                try:
                    step = fn()
                    if step is not None:
                        break
                except TypeError:
                    pass

        # ---- falls FOR intern ein assignStmt hat: FOR i = <start> TO <end> ----
        if start is None:
            if hasattr(fctx, "assignStmt") and fctx.assignStmt():
                a = fctx.assignStmt()
                start = self.get_assign_rhs(a)  # aus deinem Assign-Helper von vorhin
                # var ggf. aus assign lhs
                if var is None:
                    lhs = get_assign_lhs(a)
                    # simplest: wenn lhs IDENT hat
                    if lhs is not None and hasattr(lhs, "IDENT") and lhs.IDENT():
                        var = lhs.IDENT().getText()

        # ---- letzter Fallback: children nach expr/primary durchsuchen ----
        if start is None or end is None:
            kids = list(getattr(fctx, "children", []) or [])
            expr_like = []
            for ch in kids:
                t = type(ch).__name__.lower()
                if "expr" in t or "primary" in t:
                    expr_like.append(ch)
            # Heuristik: erste = start, zweite = end, dritte = step
            if start is None and len(expr_like) >= 1:
                start = expr_like[0]
            if end is None and len(expr_like) >= 2:
                end = expr_like[1]
            if step is None and len(expr_like) >= 3:
                step = expr_like[2]

        return (var, start, end, step, blk)
        
    # ---------- statements ----------
    def gen_stmt(self, st):
        if hasattr(st, "writeStmt") and st.writeStmt():
            w = st.writeStmt()
            exprs = self.get_write_exprs(w)

            # wenn WRITE mehrere Werte erlaubt: jede Zeile einzeln ausgeben
            if not exprs:
                return "Console.WriteLine();"

            lines = []
            for ex in exprs:
                lines.append(f"Console.WriteLine({self.gen_expr(ex)});")
            return "\n".join(lines)

        if hasattr(st, "assignStmt") and st.assignStmt():
            a = st.assignStmt()
            
            lhs_ctx = self.get_assign_lhs(a)
            rhs_ctx = self.get_assign_rhs(a)

            lhs = self.gen_expr(lhs_ctx) if lhs_ctx is not None else "/* TODO lhs */"
            rhs = self.gen_expr(rhs_ctx) if rhs_ctx is not None else "/* TODO rhs */"
            
            return f"{lhs} = {rhs};"

        if hasattr(st, "returnStmt") and st.returnStmt():
            r = st.returnStmt()
            if hasattr(r, "expr") and r.expr():
                return f"return {self.gen_expr(r.expr())};"
            return "return null;"

        if hasattr(st, "breakStmt") and st.breakStmt():
            return "break;"

        if hasattr(st, "ifStmt") and st.ifStmt():
            return self.gen_if(st.ifStmt())

        if hasattr(st, "forStmt") and st.forStmt():
            return self.gen_for(st.forStmt())

        if hasattr(st, "expr") and st.expr():
            return self.gen_expr(st.expr()) + ";"

        return f"/* TODO stmt: {type(st).__name__} */;"

    def iter_block_statements(self, block):
        if block is None:
            return []

        for attr in ("stmt", "statement", "stat", "statementList", "stmtList", "stmts"):
            fn = getattr(block, attr, None)
            if callable(fn):
                try:
                    res = fn()
                    if res is None:
                        continue
                    return res if isinstance(res, list) else [res]
                except TypeError:
                    pass

        kids = list(getattr(block, "children", []) or [])
        out = []
        for ch in kids:
            t = type(ch).__name__.lower()
            if "stmt" in t or "statement" in t or "stat" in t:
                out.append(ch)
        return out
        
    def gen_if(self, ctx):
        cond = self.gen_expr(ctx.expr())

        lines = [f"if ({cond}) {{"]

        # then block
        then_blk = ctx.thenBlock() if hasattr(ctx, "thenBlock") else (ctx.block(0) if hasattr(ctx, "block") else None)
        self.indent += 1
        for st in self.iter_block_statements(then_blk):
            lines.append("    " * self.indent + self.gen_stmt(st))
        self.indent -= 1
        lines.append("    " * self.indent + "}")

        # else block (optional)
        else_blk = None
        if hasattr(ctx, "elseBlock") and ctx.elseBlock():
            else_blk = ctx.elseBlock()
        elif hasattr(ctx, "block") and len(ctx.block()) > 1:
            else_blk = ctx.block(1)

        if else_blk is not None:
            lines.append("    " * self.indent + "else {")
            self.indent += 1
            for st in self.iter_block_statements(else_blk):
                lines.append("    " * self.indent + self.gen_stmt(st))
            self.indent -= 1
            lines.append("    " * self.indent + "}")

        return "\n".join(lines)

    def gen_for(self, ctx):
        var, start_ctx, end_ctx, step_ctx, blk = self.get_for_parts(ctx)

        var = var or "i"
        start = self.gen_expr(start_ctx) if start_ctx is not None else "0"
        end   = self.gen_expr(end_ctx)   if end_ctx   is not None else "0"
        step  = self.gen_expr(step_ctx)  if step_ctx  is not None else "1"

        cmp_op = "<="
        inc = f"{var} += {step}"
        if isinstance(step, str) and step.strip().startswith("-"):
            cmp_op = ">="
            inc = f"{var} += {step}"

        lines = [f"for (int {var} = {start}; {var} {cmp_op} {end}; {inc}) {{"]

        if blk is not None:
            self.indent += 1
            for st in self.iter_block_statements(blk):  # aus deinem Block-Fix
                lines.append("    " * self.indent + self.gen_stmt(st))
            self.indent -= 1
        else:
            lines.append("    " * (self.indent + 1) + "/* TODO for-block */")

        lines.append("    " * self.indent + "}")
        return "\n".join(lines)

    # ---------- expressions ----------
    def gen_expr(self, e):
        if hasattr(e, "primary") and e.primary():
            return self.gen_primary(e.primary())

        # falls du binOps als left/right/op hast:
        if hasattr(e, "left") and hasattr(e, "right") and hasattr(e, "op"):
            a = self.gen_expr(e.left)
            b = self.gen_expr(e.right)
            op = e.op.text
            op_map = {"AND": "&&", "OR": "||", "=": "==", "<>": "!="}
            op2 = op_map.get(op.upper(), op)
            return f"({a} {op2} {b})"

        if hasattr(e, "getText"):
            return e.getText()

        return f"/* TODO expr: {type(e).__name__} */null"

    def gen_primary(self, ctx):
        if hasattr(ctx, "newExpr") and ctx.newExpr():
            return self.gen_new(ctx.newExpr())

        if hasattr(ctx, "NUMBER") and ctx.NUMBER():
            return ctx.NUMBER().getText()

        if hasattr(ctx, "STRING") and ctx.STRING():
            return ctx.STRING().getText()

        if hasattr(ctx, "IDENT") and ctx.IDENT():
            name = ctx.IDENT().getText()
            if name.upper() == "THIS":
                return "this"
            if name.upper() == "NIL":
                return "null"
            return name

        if hasattr(ctx, "dottedRef") and ctx.dottedRef():
            return self.gen_dotted_ref(ctx.dottedRef())

        if hasattr(ctx, "callExpr") and ctx.callExpr():
            return self.gen_call(ctx.callExpr())

        return f"/* TODO primary: {type(ctx).__name__} */null"

    def gen_dotted_ref(self, ctx):
        parts = [t.getText() for t in ctx.IDENT()]
        if parts and parts[0].upper() == "THIS":
            parts[0] = "this"
        return ".".join(parts)

    def gen_new(self, ctx):
        class_name = ctx.IDENT().getText()
        args = []
        if hasattr(ctx, "argList") and ctx.argList():
            for a in ctx.argList().expr():
                args.append(self.gen_expr(a))
        return f"new {class_name}(" + ", ".join(args) + ")"

    def gen_call(self, ctx):
        if hasattr(ctx, "dottedRef") and ctx.dottedRef():
            callee = self.gen_dotted_ref(ctx.dottedRef())
        elif hasattr(ctx, "IDENT") and ctx.IDENT():
            callee = ctx.IDENT().getText()
        else:
            callee = "/* TODO callee */"

        if callee.upper() == "WRITE":
            callee = "Console.WriteLine"

        args = []
        if hasattr(ctx, "argList") and ctx.argList():
            for a in ctx.argList().expr():
                args.append(self.gen_expr(a))

        return f"{callee}(" + ", ".join(args) + ")"
        
class DBaseToCpp:
    def __init__(self, parser, classes=None, prog_name="genprog"):
        self.p = parser
        self.out = CppEmitter()
        self.classes = classes or {}
        self.prog_name = prog_name
        self._tmp_i = 0

    def new_temp(self):
        self._tmp_i += 1
        return f"t{self._tmp_i}"

    # ---------- helpers ----------
    def cpp_str(self, s: str) -> str:
        return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

    def cpp_str_vec(self, items):
        # {"A","B"}
        inner = ", ".join(self.cpp_str(x) for x in items)
        return "{ " + inner + " }"

    def cpp_val_vec(self, exprs):
        # { a, b, c }
        inner = ", ".join(exprs)
        return "{ " + inner + " }"

    def norm_local(self, name: str) -> str:
        return "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in name).lower()

    # ---------- entry ----------
    def generate(self, tree, out_path: str):
        o = self.out
        o.emit("// generated dBase -> GNU C++ (runtime-backed)")
        o.emit("#include <iostream>")
        o.emit("#include <vector>")
        o.emit("#include <string>")
        o.emit("#include \"dBaseRT.hpp\"")
        o.emit("")
        o.emit("int main() {")
        o.indent()
        o.emit("TRT rt;")
        o.emit("try {")
        o.indent()

        self.gen_input(tree)

        o.dedent()
        o.emit("} catch (const std::exception& e) {")
        o.indent()
        o.emit('std::cerr << "ERROR: " << e.what() << std::endl;')
        o.emit("return 1;")
        o.dedent()
        o.emit("}")
        o.emit("return 0;")
        o.dedent()
        o.emit("}")
        Path(out_path).write_text(o.text(), encoding="utf-8")

    # ---------- root ----------
    def gen_input(self, ctx):
        for it in ctx.item():
            self.gen_item(it)

    def gen_item(self, it):
        if it.statement():
            return self.gen_stmt(it.statement())
        if it.classDecl():
            self.out.emit("// TODO classDecl not implemented in C++ backend")
            return
        if it.methodDecl():
            self.out.emit("// TODO methodDecl not implemented in C++ backend")
            return
        self.out.emit("// TODO unhandled item")

    # ---------- statements ----------
    def gen_stmt(self, st):
        if st.writeStmt():         return self.gen_write(st.writeStmt())
        if st.assignStmt():        return self.gen_assign(st.assignStmt())
        if st.localDeclStmt():     return self.gen_local_decl(st.localDeclStmt())
        if st.localAssignStmt():   return self.gen_local_assign(st.localAssignStmt())
        if st.ifStmt():            return self.gen_if(st.ifStmt())
        if st.forStmt():           return self.gen_for(st.forStmt())
        if st.breakStmt():         return self.gen_break(st.breakStmt())
        if st.returnStmt():        return self.gen_return(st.returnStmt())
        if st.withStmt():          return self.gen_with(st.withStmt())
        if st.parameterStmt():     return self.gen_parameter(st.parameterStmt())
        if st.exprStmt():          return self.gen_expr_stmt(st.exprStmt())

        self.out.emit("// TODO unhandled statement: " + type(st.getChild(0)).__name__)

    def gen_write(self, ctx):
        # writeStmt : WRITE writeArg (PLUS writeArg)* ;
        parts = [self.gen_write_arg(a) for a in ctx.writeArg()]
        if not parts:
            self.out.emit("rt.WRITE(TRT::Null());")
            return

        expr = parts[0]
        for p in parts[1:]:
            expr = f"rt.BINOP({expr}, \"+\", {p})"

        self.out.emit(f"rt.WRITE({expr});")

    def gen_write_arg(self, actx):
        if actx.STRING():
            return f"TRT::V({actx.STRING().getText()})"  # String-Literal inkl. Quotes kommt aus Lexer
        if actx.dottedRef():
            base, path = self.gen_dotted_ref_parts(actx.dottedRef())
            return f"rt.GET({base}, {path})"
        if actx.expr():
            return self.gen_expr(actx.expr())
        return "TRT::Null()"

    def gen_local_decl(self, ctx):
        name = ctx.name.text if hasattr(ctx, "name") else ctx.IDENT().getText()
        self.out.emit(f"rt.SET_NAME({self.cpp_str(name)}, TRT::Null());")

    def gen_local_assign(self, ctx):
        name = ctx.name.text if hasattr(ctx, "name") else ctx.IDENT().getText()
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.SET_NAME({self.cpp_str(name)}, {rhs});")

    def gen_assign(self, ctx):
        rhs = self.gen_expr(ctx.expr())
        lv = ctx.lvalue()

        if lv.dottedRef():
            base, path = self.gen_dotted_ref_parts(lv.dottedRef())
            self.out.emit(f"rt.SET({base}, {path}, {rhs});")
            return

        pe = lv.postfixExpr()
        if pe:
            chain = self.lvalue_chain_from_postfix(pe)

            if len(chain) == 1:
                self.out.emit(f"rt.SET_NAME({self.cpp_str(chain[0])}, {rhs});")
                return

            head = chain[0]
            if head.upper() == "THIS":
                base = "rt.GET_THIS()"
                path = self.cpp_str_vec(chain[1:])
            else:
                base = f"rt.GET_NAME({self.cpp_str(head)})"
                path = self.cpp_str_vec(chain[1:])

            self.out.emit(f"rt.SET({base}, {path}, {rhs});")
            return

        self.out.emit("// TODO unsupported lvalue: " + lv.getText())

    def gen_if(self, ctx):
        # ifStmt : IF expr block (ELSE block)? ENDIF ;
        cond = self.gen_expr(ctx.expr())
        self.out.emit(f"if (rt.TRUE({cond})) {{")
        self.out.indent()

        then_block = ctx.block(0)
        for st in then_block.statement():
            self.gen_stmt(st)

        self.out.dedent()
        self.out.emit("}")

        if ctx.ELSE():
            self.out.emit("else {")
            self.out.indent()
            else_block = ctx.block(1)
            for st in else_block.statement():
                self.gen_stmt(st)
            self.out.dedent()
            self.out.emit("}")

    def gen_for(self, ctx):
        # forStmt : FOR IDENT ASSIGN numberExpr TO numberExpr (STEP numberExpr)? block ENDFOR ;
        var = ctx.IDENT().getText()
        start = ctx.numberExpr(0).getText()
        end   = ctx.numberExpr(1).getText()
        step  = ctx.numberExpr(2).getText() if ctx.STEP() else "1"

        # Wir halten "i" als Runtime-Variable, damit Semantik identisch bleibt
        self.out.emit(f"rt.SET_NAME({self.cpp_str(var)}, TRT::V({start}));")
        self.out.emit(f"while (rt.TRUE(rt.FOR_COND(rt.GET_NAME({self.cpp_str(var)}), TRT::V({end}), TRT::V({step})))) {{")
        self.out.indent()

        for st in ctx.block().statement():
            self.gen_stmt(st)

        self.out.emit(f"rt.SET_NAME({self.cpp_str(var)}, rt.BINOP(rt.GET_NAME({self.cpp_str(var)}), \"+\", TRT::V({step})));")
        self.out.dedent()
        self.out.emit("}")

    def gen_break(self, ctx):
        self.out.emit("break;")

    def gen_return(self, ctx):
        # Top-level main(): wir delegieren an runtime (oder du kannst return 0/1 machen)
        if ctx.expr():
            self.out.emit(f"rt.RETURN({self.gen_expr(ctx.expr())});")
        else:
            self.out.emit("rt.RETURN(TRT::Null());")

    def gen_parameter(self, ctx):
        p = ctx.paramNames()
        names = [t.getText() for t in p.IDENT()]
        self.out.emit(f"rt.PARAMETER({self.cpp_str_vec(names)});")

    def gen_expr_stmt(self, ctx):
        # exprStmt : postfixExpr ;
        e = self.gen_postfix(ctx.postfixExpr())
        self.out.emit(f"(void){e};")

    # ---------- WITH ----------
    def gen_with(self, ctx):
        base = self.gen_with_target(ctx.withTarget())
        tmp = self.new_temp()
        self.out.emit(f"auto {tmp} = {base};")
        self.out.emit(f"rt.PUSH_WITH({tmp});")

        body = ctx.withBody()
        for ch in list(getattr(body, "children", []) or []):
            t = type(ch).__name__
            if t.endswith("WithAssignStmtContext"):
                self.gen_with_assign(ch)
            elif t.endswith("WithStmtContext"):
                self.gen_with(ch)
            elif t.endswith("StatementContext"):
                self.gen_stmt(ch)

        self.out.emit("rt.POP_WITH();")

    def gen_with_target(self, ctx):
        if ctx.THIS():
            return "rt.GET_THIS()"
        if ctx.dottedRef():
            base, path = self.gen_dotted_ref_parts(ctx.dottedRef())
            return f"rt.GET('{base.upper()}', {path})"
        if ctx.IDENT():
            return f"rt.GET_NAME({self.cpp_str(ctx.IDENT().getText())})"
        if ctx.postfixExpr():
            return self.gen_postfix(ctx.postfixExpr())
        return "TRT::Null()"

    def gen_with_assign(self, ctx):
        path = [t.getText() for t in ctx.withLvalue().IDENT()]
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.WITH_SET({self.cpp_str_vec(path)}, {rhs});")

    # ---------- expr / postfix / primary ----------
    # Hier kannst du (fast) genau deine Python-Version übernehmen, nur dass
    # du C++-Strings und TRT::V(...) nutzt. Ich mach’s minimal:

    def gen_expr(self, ctx):
        # expr : logicalOr ;
        return self.gen_logical_or(ctx.logicalOr())

    def gen_logical_or(self, ctx):
        parts = [self.gen_logical_and(x) for x in ctx.logicalAnd()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, \"OR\", {rhs})"
        return out

    def gen_logical_and(self, ctx):
        parts = [self.gen_logical_not(x) for x in ctx.logicalNot()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, \"AND\", {rhs})"
        return out

    def gen_logical_not(self, ctx):
        if ctx.NOT():
            inner = self.gen_logical_not(ctx.logicalNot())
            return f"rt.UNOP(\"NOT\", {inner})"
        return self.gen_comparison(ctx.comparison())

    def gen_comparison(self, ctx):
        left = self.gen_additive(ctx.additiveExpr(0))
        if ctx.compareOp():
            op = ctx.compareOp().getText()
            right = self.gen_additive(ctx.additiveExpr(1))
            return f"rt.BINOP({left}, {self.cpp_str(op)}, {right})"
        return left

    def gen_additive(self, ctx):
        terms = [self.gen_multiplicative(x) for x in ctx.multiplicativeExpr()]
        out = terms[0]
        kids = list(ctx.getChildren())
        i = 1
        while i < len(kids):
            op = kids[i].getText()
            rhs = terms[(i + 1) // 2]
            out = f"rt.BINOP({out}, {self.cpp_str(op)}, {rhs})"
            i += 2
        return out

    def gen_multiplicative(self, ctx):
        factors = [self.gen_postfix(x) for x in ctx.postfixExpr()]
        out = factors[0]
        kids = list(ctx.getChildren())
        i = 1
        while i < len(kids):
            op = kids[i].getText()
            rhs = factors[(i + 1) // 2]
            out = f"rt.BINOP({out}, {self.cpp_str(op)}, {rhs})"
            i += 2
        return out

    def gen_postfix(self, ctx):
        cur = self.gen_primary(ctx.primary())
        kids = list(ctx.getChildren())
        k = 1
        while k < len(kids):
            t = kids[k].getText()
            if t == "(":
                args = []
                if kids[k+1].getText() != ")":
                    argctx = kids[k+1]
                    args = [self.gen_expr(e) for e in argctx.expr()]
                    k += 1
                cur = f"rt.CALL_ANY({cur}, {self.cpp_val_vec(args)})"
                k += 2
                continue
            if t in (".", "::"):
                name = kids[k+1].getText()
                cur = f"rt.GET_ATTR({cur}, {self.cpp_str(name)})"
                k += 2
                continue
            k += 1
        return cur

    def gen_primary(self, ctx):
        if ctx.THIS():
            return "rt.GET_THIS()"
        if ctx.STRING():
            return f"TRT::V({ctx.STRING().getText()})"
        if ctx.NUMBER():
            return f"TRT::V({ctx.NUMBER().getText()})"
        if ctx.FLOAT():
            return f"TRT::V({ctx.FLOAT().getText()})"
        if ctx.IDENT():
            return f"rt.GET_NAME({self.cpp_str(ctx.IDENT().getText())})"
        if ctx.newExpr():
            return self.gen_new(ctx.newExpr())
        if ctx.expr():
            return "(" + self.gen_expr(ctx.expr()) + ")"
        return "TRT::Null()"

    def gen_new(self, ctx):
        class_name = ctx.IDENT().getText()
        args = []
        if ctx.argList():
            args = [self.gen_expr(e) for e in ctx.argList().expr()]
        return f"rt.NEW({self.cpp_str(class_name)}, {self.cpp_val_vec(args)})"

    def gen_dotted_ref_parts(self, dctx):
        parts = [t.getText() for t in dctx.IDENT()]
        head = parts[0]
        if head.upper() == "THIS":
            base = "rt.GET_THIS()"
            path = self.cpp_str_vec(parts[1:])
        else:
            base = f"rt.GET_NAME({self.cpp_str(head)})"
            path = self.cpp_str_vec(parts[1:])
        return base, path

    def lvalue_chain_from_postfix(self, pe):
        chain = [pe.primary().getText()]
        i = 1
        while i < pe.getChildCount():
            ch = pe.getChild(i).getText()
            if ch == ".":
                chain.append(pe.getChild(i+1).getText())
                i += 2
                continue
            if ch == "(":
                raise RuntimeError(f"LVALUE darf keinen Call enthalten: {pe.getText()}")
            i += 1
        return chain
        
class DBaseToPascal:
    def __init__(self, parser, classes=None, unit_name="GenProg"):
        self.p = parser
        self.out = PasEmitter()
        self.classes = classes or {}
        self.unit_name = unit_name
        self._tmp_i = 0

    def new_temp(self):
        self._tmp_i += 1
        return f"t{self._tmp_i}"

    # ----------------- ENTRY -----------------
    def generate(self, tree, out_path: str):
        o = self.out

        # Minimal-Programm. Du kannst auch "unit" generieren, wenn du willst.
        o.emit(f"program {self.unit_name};")
        o.emit("")
        o.emit("{$mode objfpc}{$H+}")
        o.emit("")
        o.emit("uses")
        o.indent()
        o.emit("SysUtils, Variants, dBaseRT;")
        o.dedent()
        o.emit(";")
        o.emit("")
        o.emit("var")
        o.indent()
        o.emit("rt: TRT;")
        o.dedent()
        o.emit("")
        o.emit("begin")
        o.indent()
        o.emit("rt := TRT.Create;")
        o.emit("try")
        o.indent()

        self.gen_input(tree)

        o.dedent()
        o.emit("finally")
        o.indent()
        o.emit("rt.Free;")
        o.dedent()
        o.emit("end;")
        o.dedent()
        o.emit("end.")
        Path(out_path).write_text(o.text(), encoding="utf-8")

    # ----------------- ROOT -----------------
    def gen_input(self, ctx):
        # input : item* EOF
        for it in ctx.item():
            self.gen_item(it)

    def gen_item(self, it):
        # item : classDecl | methodDecl | statement
        if it.statement():
            return self.gen_stmt(it.statement())
        if it.classDecl():
            return self.gen_class(it.classDecl())   # optional später
        if it.methodDecl():
            return self.gen_method(it.methodDecl()) # optional später
        self.out.emit("{ TODO unhandled item }")

    # ----------------- STATEMENTS -----------------
    def gen_stmt(self, st):
        # Passe das an die Stmt-Alternativen an, die du schon in Python eingebaut hast.
        if st.writeStmt():         return self.gen_write(st.writeStmt())
        if st.assignStmt():        return self.gen_assign(st.assignStmt())
        if st.localDeclStmt():     return self.gen_local_decl(st.localDeclStmt())
        if st.localAssignStmt():   return self.gen_local_assign(st.localAssignStmt())
        if st.ifStmt():            return self.gen_if(st.ifStmt())
        if st.forStmt():           return self.gen_for(st.forStmt())
        if st.returnStmt():        return self.gen_return(st.returnStmt())
        if st.breakStmt():         return self.gen_break(st.breakStmt())
        if st.withStmt():          return self.gen_with(st.withStmt())
        if st.parameterStmt():     return self.gen_parameter(st.parameterStmt())
        # … Schritt für Schritt erweitern …
        self.out.emit("{ TODO unhandled statement: " + type(st.getChild(0)).__name__ + " }")

    def gen_write(self, ctx):
        # writeStmt : WRITE writeArg (PLUS writeArg)* ;
        parts = [self.gen_write_arg(a) for a in ctx.writeArg()]
        if not parts:
            self.out.emit("rt.WRITE('');")
            return

        # dBase-Plus soll runtime-semantisch bleiben -> BINOP kaskadieren
        expr = parts[0]
        for p in parts[1:]:
            expr = f"rt.BINOP({expr}, '+', {p})"

        self.out.emit(f"rt.WRITE({expr});")

    def gen_write_arg(self, actx):
        # writeArg : STRING | dottedRef | expr ;
        if actx.STRING():
            return actx.STRING().getText()
        if actx.dottedRef():
            base_expr, path = self.gen_dotted_ref_parts(actx.dottedRef())
            return f"rt.GET('{base_expr.upper()}', {path})"
        if actx.expr():
            return self.gen_expr(actx.expr())
        return f"Null"

    def gen_local_decl(self, ctx):
        # LOCAL IDENT
        name = ctx.name.text if hasattr(ctx, "name") else ctx.IDENT().getText()
        self.out.emit(f"rt.SET_NAME('{name}', Null);")

    def gen_local_assign(self, ctx):
        name = ctx.name.text if hasattr(ctx, "name") else ctx.IDENT().getText()
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.SET_NAME('{name}', {rhs});")

    def gen_assign(self, ctx):
        rhs = self.gen_expr(ctx.expr())
        lv = ctx.lvalue()

        # lvalue : postfixExpr | dottedRef ;
        if lv.dottedRef():
            base_expr, path = self.gen_dotted_ref_parts(lv.dottedRef())
            self.out.emit(f"rt.SET_({base_expr}, {path}, {rhs});")
            return

        pe = lv.postfixExpr()
        if pe:
            chain = self.lvalue_chain_from_postfix(pe)  # ["Y"] oder ["THIS","X","Y"]

            if len(chain) == 1:
                self.out.emit(f"rt.SET_NAME('{chain[0]}', {rhs});")
                return

            head = chain[0]
            if head.upper() == "THIS":
                base_expr = "rt.GET_THIS()"
                path = chain[1:]
            else:
                base_expr = f"rt.GET_NAME('{head}')"
                path = chain[1:]

            self.out.emit(f"rt.SET_({base_expr}, {self.pas_str_array(path)}, {rhs});")
            return

        self.out.emit("{ TODO unsupported lvalue }")

    def gen_if(self, ctx):
        # ifStmt : IF expr block (ELSE block)? ENDIF ;
        cond = self.gen_expr(ctx.expr())
        self.out.emit(f"if rt.TRUE_({cond}) then")
        self.out.emit("begin")
        self.out.indent()

        then_block = ctx.block(0)
        for st in then_block.statement():
            self.gen_stmt(st)

        self.out.dedent()
        self.out.emit("end")

        if ctx.ELSE():
            self.out.emit("else")
            self.out.emit("begin")
            self.out.indent()

            else_block = ctx.block(1)
            for st in else_block.statement():
                self.gen_stmt(st)

            self.out.dedent()
            self.out.emit("end;")
        else:
            self.out.emit(";")

    def gen_for(self, ctx):
        # forStmt : FOR IDENT ASSIGN numberExpr TO numberExpr (STEP numberExpr)? block ENDFOR ;
        varname = self.norm_local(ctx.IDENT().getText())
        start = ctx.numberExpr(0).getText()
        end   = ctx.numberExpr(1).getText()
        step  = ctx.numberExpr(2).getText() if ctx.STEP() else "1"

        # STEP != 1 -> while-Schleife (FPC for kann keinen Step)
        if step == "1":
            self.out.emit(f"rt.SET_NAME('{varname}', {start});")
            self.out.emit(f"while rt.TRUE_(rt.BINOP(rt.GET_NAME('{varname}'), '<=', {end})) do")
            self.out.emit("begin")
            self.out.indent()
            # Body
            for st in ctx.block().statement():
                self.gen_stmt(st)
            # Increment
            self.out.emit(f"rt.SET_NAME('{varname}', rt.BINOP(rt.GET_NAME('{varname}'), '+', {step}));")
            self.out.dedent()
            self.out.emit("end;")
        else:
            # allgemein: i := start; while cond: body; i += step
            self.out.emit(f"rt.SET_NAME('{varname}', {start});")
            self.out.emit(f"while rt.TRUE_(rt.FOR_COND(rt.GET_NAME('{varname}'), {end}, {step})) do")
            self.out.emit("begin")
            self.out.indent()
            for st in ctx.block().statement():
                self.gen_stmt(st)
            self.out.emit(f"rt.SET_NAME('{varname}', rt.BINOP(rt.GET_NAME('{varname}'), '+', {step}));")
            self.out.dedent()
            self.out.emit("end;")

    def gen_break(self, ctx):
        # in Pascal: break;
        self.out.emit("break;")

    def gen_return(self, ctx):
        # Im Program-Level gibt es kein "return". In Methoden später: Exit(value).
        # Hier delegieren wir:
        if ctx.expr():
            self.out.emit(f"rt.RETURN_({self.gen_expr(ctx.expr())});")
        else:
            self.out.emit("rt.RETURN_(Null);")

    def gen_parameter(self, ctx):
        # parameterStmt : PARAMETER paramNames ;
        p = ctx.paramNames()
        names = [t.getText() for t in p.IDENT()]
        self.out.emit(f"rt.PARAMETER({self.pas_str_array(names)});")

    # ----------------- WITH -----------------
    def gen_with(self, ctx):
        # withStmt : WITH '(' withTarget ')' withBody ENDWITH ;
        base = self.gen_with_target(ctx.withTarget())
        tmp = self.new_temp()
        self.out.emit(f"var {tmp}: Variant; {tmp} := {base};")  # simpel, du kannst var-block auch global machen
        self.out.emit(f"rt.PUSH_WITH({tmp});")
        body = ctx.withBody()
        for ch in list(getattr(body, "children", []) or []):
            t = type(ch).__name__
            if t.endswith("WithAssignStmtContext"):
                self.gen_with_assign(ch)
            elif t.endswith("WithStmtContext"):
                self.gen_with(ch)
            elif t.endswith("StatementContext"):
                self.gen_stmt(ch)
        self.out.emit("rt.POP_WITH();")

    def gen_with_target(self, ctx):
        # withTarget : THIS | dottedRef | IDENT | postfixExpr ;
        if ctx.THIS():
            return "rt.GET_THIS()"
        if ctx.dottedRef():
            base_expr, path = self.gen_dotted_ref_parts(ctx.dottedRef())
            return f"rt.GET('{base_expr.upper()}', {path})"
        if ctx.IDENT():
            name = ctx.IDENT().getText()
            return f"rt.GET_NAME('{name}')"
        if ctx.postfixExpr():
            return self.gen_postfix(ctx.postfixExpr())
        return "Null"

    def gen_with_assign(self, ctx):
        # withAssignStmt : withLvalue ASSIGN expr ;
        path = [t.getText() for t in ctx.withLvalue().IDENT()]
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.WITH_SET({self.pas_str_array(path)}, {rhs});")

    # ----------------- EXPRESSIONS -----------------
    # Hier: nutze deine bereits angepassten gen_expr/gen_postfix/gen_primary-Methoden,
    # aber gib Pascal-Ausdrücke zurück, die auf rt.* basieren.

    def gen_expr(self, ctx):
        # expr : logicalOr ;
        return self.gen_logical_or(ctx.logicalOr())

    def gen_logical_or(self, ctx):
        parts = [self.gen_logical_and(x) for x in ctx.logicalAnd()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, 'OR', {rhs})"
        return out

    def gen_logical_and(self, ctx):
        parts = [self.gen_logical_not(x) for x in ctx.logicalNot()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, 'AND', {rhs})"
        return out

    def gen_logical_not(self, ctx):
        if ctx.NOT():
            inner = self.gen_logical_not(ctx.logicalNot())
            return f"rt.UNOP('NOT', {inner})"
        return self.gen_comparison(ctx.comparison())

    def gen_comparison(self, ctx):
        left = self.gen_additive(ctx.additiveExpr(0))
        if ctx.compareOp():
            op = ctx.compareOp().getText()
            right = self.gen_additive(ctx.additiveExpr(1))
            return f"rt.BINOP({left}, '{op}', {right})"
        return left

    def gen_additive(self, ctx):
        terms = [self.gen_multiplicative(x) for x in ctx.multiplicativeExpr()]
        out = terms[0]
        kids = list(ctx.getChildren())
        i = 1
        while i < len(kids):
            op = kids[i].getText()
            rhs = terms[(i + 1) // 2]
            out = f"rt.BINOP({out}, '{op}', {rhs})"
            i += 2
        return out

    def gen_multiplicative(self, ctx):
        factors = [self.gen_postfix(x) for x in ctx.postfixExpr()]
        out = factors[0]
        kids = list(ctx.getChildren())
        i = 1
        while i < len(kids):
            op = kids[i].getText()
            rhs = factors[(i + 1) // 2]
            out = f"rt.BINOP({out}, '{op}', {rhs})"
            i += 2
        return out

    def gen_postfix(self, ctx):
        # postfixExpr : primary ( '(' argList? ')' | ('.'|'::') IDENT )* ;
        cur = self.gen_primary(ctx.primary())
        kids = list(ctx.getChildren())
        k = 1
        while k < len(kids):
            t = kids[k].getText()
            if t == "(":
                args = []
                if kids[k+1].getText() != ")":
                    argctx = kids[k+1]
                    args = [self.gen_expr(e) for e in argctx.expr()]
                    k += 1
                cur = f"rt.CALL_ANY({cur}, {self.pas_expr_array(args)})"
                k += 2
                continue
            if t in (".", "::"):
                name = kids[k+1].getText()
                cur = f"rt.GET_ATTR({cur}, '{name}')"
                k += 2
                continue
            k += 1
        return cur
    
    def gen_new(self, ctx):
        # newExpr : NEW IDENT LPAREN argList? RPAREN ;
        class_name = ctx.IDENT().getText()
        args = []
        if ctx.argList():
            args = [self.gen_expr(e) for e in ctx.argList().expr()]
        
        # Pascal: array of Variant -> wir geben einen Pascal-Array-Ausdruck zurück
        return f"rt.NEW('{class_name}', {self.pas_expr_array(args)})"
    
    def gen_class(self, ctx):
        self.out.emit("{ TODO gen_class: " + ctx.name.text + " }")

    def gen_method(self, ctx):
        self.out.emit("{ TODO gen_method: " + ctx.IDENT().getText() + " }")
        
    def gen_primary(self, ctx):
        if ctx.THIS():    return "rt.GET_THIS()"
        if ctx.STRING():  return ctx.STRING().getText()
        if ctx.NUMBER():  return ctx.NUMBER().getText()
        if ctx.FLOAT():   return ctx.FLOAT().getText()
        if ctx.IDENT():
            name = ctx.IDENT().getText()
            return f"rt.GET_NAME('{name}')"
        if ctx.newExpr():
            return self.gen_new(ctx.newExpr())
        if ctx.expr():
            return f"({self.gen_expr(ctx.expr())})"
        return "Null"

    # ----------------- dottedRef / lvalue helpers -----------------
    def gen_dotted_ref_parts(self, dctx):
        parts = [t.getText() for t in dctx.IDENT()]
        head = parts[0]
        if head.upper() == "THIS":
            base = "rt.GET_THIS()"
            path = parts[1:]
        else:
            base = f"rt.GET_NAME('{head}')"
            path = parts[1:]
        return base, self.pas_str_array(path)

    def lvalue_chain_from_postfix(self, pe):
        chain = [pe.primary().getText()]
        i = 1
        while i < pe.getChildCount():
            ch = pe.getChild(i).getText()
            if ch == ".":
                chain.append(pe.getChild(i+1).getText())
                i += 2
                continue
            if ch == "(":
                raise RuntimeError(f"LVALUE darf keinen Call enthalten: {pe.getText()}")
            i += 1
        return chain

    # ----------------- small utils -----------------
    def pas_str_array(self, items):
        # ["A","B"] -> ['A','B']
        inner = ", ".join("'" + s.replace("'", "''") + "'" for s in items)
        return f"[{inner}]"

    def pas_expr_array(self, exprs):
        # ["rt.GET_NAME('X')", "5"] -> [rt.GET_NAME('X'), 5]
        inner = ", ".join(exprs)
        return f"[{inner}]"

    def norm_local(self, name: str) -> str:
        # optional (wenn du Namen in Pascal-Var-IDs brauchst)
        return "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in name).lower()

class DBaseToJavaScript:
    def __init__(self, parser, class_name="GenProg", module_name=None):
        self.parser = parser
        self.class_name = class_name
        self.module_name = module_name  # optional
        self.out = []
        self.indent = 0

    # ---------- robuste Helfer (wie zuvor) ----------
    def iter_block_statements(self, block):
        if block is None:
            return []
        for attr in ("stmt", "statement", "stat", "statementList", "stmtList", "stmts"):
            fn = getattr(block, attr, None)
            if callable(fn):
                try:
                    res = fn()
                    if res is None:
                        continue
                    return res if isinstance(res, list) else [res]
                except TypeError:
                    pass
        kids = list(getattr(block, "children", []) or [])
        out = []
        for ch in kids:
            t = type(ch).__name__.lower()
            if "stmt" in t or "statement" in t or "stat" in t:
                out.append(ch)
        return out

    def get_write_exprs(self, wctx):
        if wctx is None:
            return []
        if hasattr(wctx, "expr"):
            expr_attr = getattr(wctx, "expr")
            if callable(expr_attr):
                try:
                    res = expr_attr()
                    if res is not None:
                        return res if isinstance(res, list) else [res]
                except TypeError:
                    pass
            try:
                out = []
                i = 0
                while True:
                    out.append(expr_attr(i))
                    i += 1
            except Exception:
                if out:
                    return out
        if hasattr(wctx, "exprList") and wctx.exprList():
            el = wctx.exprList()
            if hasattr(el, "expr") and callable(el.expr):
                res = el.expr()
                if res is not None:
                    return res if isinstance(res, list) else [res]
        if hasattr(wctx, "primary") and wctx.primary():
            p = wctx.primary()
            return p if isinstance(p, list) else [p]
        kids = list(getattr(wctx, "children", []) or [])
        out = []
        for ch in kids:
            t = type(ch).__name__.lower()
            if "expr" in t or "primary" in t:
                out.append(ch)
        return out
        
    def get_assign_lhs(self, actx):
        if actx is None:
            return None
        for name in ("lhs", "lvalue", "target", "left", "ref"):
            fn = getattr(actx, name, None)
            if callable(fn):
                try:
                    res = fn()
                    if res is not None:
                        return res
                except TypeError:
                    pass
        if hasattr(actx, "dottedRef") and actx.dottedRef():
            return actx.dottedRef()
        if hasattr(actx, "IDENT") and actx.IDENT():
            return actx.IDENT()
        kids = list(getattr(actx, "children", []) or [])
        for ch in kids:
            t = type(ch).__name__.lower()
            if "dottedref" in t or "lvalue" in t or "ref" in t or "primary" in t:
                return ch
        return None

    def get_assign_rhs(self, actx):
        if actx is None:
            return None
        if hasattr(actx, "expr") and callable(actx.expr):
            try:
                res = actx.expr()
                if isinstance(res, list):
                    return res[-1] if res else None
                if res is not None:
                    return res
            except TypeError:
                i = 0
                last = None
                while True:
                    try:
                        last = actx.expr(i)
                        i += 1
                    except Exception:
                        break
                return last
        kids = list(getattr(actx, "children", []) or [])
        for ch in reversed(kids):
            if "expr" in type(ch).__name__.lower() or hasattr(ch, "primary"):
                return ch
        return None

    # --- API wie bei dir ---
    def generate(self, tree, outfile):
        self.out, self.indent = [], 0

        # Header: ES Modules, Runtime import
        self.emit('import { WRITE, NEWOBJ, ParentForm } from "./rt.js";')
        self.emit()

        # Tree abarbeiten
        if hasattr(tree, "item"):
            for it in tree.item():
                self.gen_item(it)
        else:
            self.gen_any(tree)

        # optional: Auto-Start / Main
        self.emit()
        self.emit(f"// --- optional quick test ---")
        self.emit(f"// const app = new {self.class_name}();")
        self.emit(f"// if (app.Init) app.Init();")

        with open(outfile, "w", encoding="utf-8") as f:
            f.write(self.get_code())

    # --- basics ---
    def emit(self, s=""):
        self.out.append("  " * self.indent + s)

    def get_code(self):
        return "\n".join(self.out)

    # --- tree fallback ---
    def gen_any(self, node):
        if hasattr(node, "classDecl") and node.classDecl():
            return self.gen_class(node.classDecl())
        if hasattr(node, "children"):
            for ch in (node.children or []):
                self.gen_any(ch)

    # --- old schema entrypoints ---
    def gen_item(self, it):
        if hasattr(it, "classDecl") and it.classDecl():
            return self.gen_class(it.classDecl())
        self.emit(f"// TODO item: {type(it).__name__}")

    def gen_class(self, ctx):
        # Du kannst wahlweise ctx.name.text nehmen, oder immer class_name erzwingen
        cls = self.class_name

        parent = "ParentForm"
        if getattr(ctx, "parent", None):
            parent = ctx.parent.text

        self.emit(f"export class {cls} extends {parent} " + "{")
        self.indent += 1

        body = ctx.classBody()
        children = list(getattr(body, "children", []) or [])

        # Properties -> in JS im ctor initialisieren
        props = []
        for ch in children:
            if hasattr(ch, "propertyDecl") and ch.propertyDecl():
                props.append(ch.propertyDecl().IDENT().getText())

        self.emit("constructor() {")
        self.indent += 1
        self.emit("super();")
        for p in props:
            self.emit(f"this.{p} = null;")
        self.indent -= 1
        self.emit("}")
        self.emit()

        # Methods
        for ch in children:
            if hasattr(ch, "methodDecl") and ch.methodDecl():
                self.gen_method(ch.methodDecl())

        self.indent -= 1
        self.emit("}")
        self.emit()

    def gen_method(self, ctx):
        name = ctx.IDENT().getText()

        params = []
        if hasattr(ctx, "paramList") and ctx.paramList():
            for p in ctx.paramList().IDENT():
                params.append(p.getText())

        self.emit(f"{name}(" + ", ".join(params) + ") {")
        self.indent += 1

        block = ctx.block()
        for st in self.iter_block_statements(block):
            self._emit_stmt_multiline(self.gen_stmt(st))

        self.indent -= 1
        self.emit("}")
        self.emit()

    def _emit_stmt_multiline(self, s):
        for line in s.split("\n"):
            self.emit(line)

    # --- statements ---
    def gen_stmt(self, st):
        # WRITE -> WRITE(...)
        if hasattr(st, "writeStmt") and st.writeStmt():
            w = st.writeStmt()
            exprs = self.get_write_exprs(w)
            args = ", ".join(self.gen_expr(ex) for ex in exprs)
            return f"WRITE({args});" if args else "WRITE();"

        # ASSIGN
        if hasattr(st, "assignStmt") and st.assignStmt():
            a = st.assignStmt()
            lhs_ctx = self.get_assign_lhs(a)
            rhs_ctx = self.get_assign_rhs(a)
            lhs = self.gen_expr(lhs_ctx) if lhs_ctx is not None else "/* TODO lhs */"
            rhs = self.gen_expr(rhs_ctx) if rhs_ctx is not None else "/* TODO rhs */"
            return f"{lhs} = {rhs};"

        # RETURN
        if hasattr(st, "returnStmt") and st.returnStmt():
            r = st.returnStmt()
            if hasattr(r, "expr") and r.expr():
                return f"return {self.gen_expr(r.expr())};"
            return "return;"

        # BREAK
        if hasattr(st, "breakStmt") and st.breakStmt():
            return "break;"

        # IF
        if hasattr(st, "ifStmt") and st.ifStmt():
            return self.gen_if(st.ifStmt())

        # FOR
        if hasattr(st, "forStmt") and st.forStmt():
            return self.gen_for(st.forStmt())

        # expr stmt
        if hasattr(st, "expr") and st.expr():
            return self.gen_expr(st.expr()) + ";"

        return f"// TODO stmt: {type(st).__name__}"

    def gen_if(self, ctx):
        cond = self.gen_expr(ctx.expr())
        lines = [f"if ({cond}) {{"]

        then_blk = ctx.thenBlock() if hasattr(ctx, "thenBlock") else (ctx.block(0) if hasattr(ctx, "block") else None)
        self.indent += 1
        for st in self.iter_block_statements(then_blk):
            lines.append("  " * self.indent + self.gen_stmt(st))
        self.indent -= 1
        lines.append("  " * self.indent + "}")

        # else optional
        else_blk = None
        if hasattr(ctx, "elseBlock") and ctx.elseBlock():
            else_blk = ctx.elseBlock()
        elif hasattr(ctx, "block") and len(ctx.block()) > 1:
            else_blk = ctx.block(1)

        if else_blk is not None:
            lines.append("  " * self.indent + "else {")
            self.indent += 1
            for st in self.iter_block_statements(else_blk):
                lines.append("  " * self.indent + self.gen_stmt(st))
            self.indent -= 1
            lines.append("  " * self.indent + "}")

        return "\n".join(lines)

    def gen_for(self, ctx):
        # Da dein ForStmtContext kein expr() hat, wieder heuristisch
        var = ctx.IDENT().getText() if hasattr(ctx, "IDENT") and ctx.IDENT() else "i"

        start_ctx = end_ctx = step_ctx = None
        for nm in ("startExpr", "fromExpr", "start"):
            fn = getattr(ctx, nm, None)
            if callable(fn):
                try:
                    start_ctx = fn()
                    if start_ctx is not None:
                        break
                except TypeError:
                    pass
        for nm in ("endExpr", "toExpr", "end"):
            fn = getattr(ctx, nm, None)
            if callable(fn):
                try:
                    end_ctx = fn()
                    if end_ctx is not None:
                        break
                except TypeError:
                    pass
        for nm in ("stepExpr", "byExpr", "step"):
            fn = getattr(ctx, nm, None)
            if callable(fn):
                try:
                    step_ctx = fn()
                    if step_ctx is not None:
                        break
                except TypeError:
                    pass

        start = self.gen_expr(start_ctx) if start_ctx is not None else "0"
        end   = self.gen_expr(end_ctx)   if end_ctx   is not None else "0"
        step  = self.gen_expr(step_ctx)  if step_ctx  is not None else "1"

        lines = [f"for (let {var} = {start}; {var} <= {end}; {var} += {step}) {{"]

        blk = ctx.block() if hasattr(ctx, "block") else None
        self.indent += 1
        for st in self.iter_block_statements(blk):
            lines.append("  " * self.indent + self.gen_stmt(st))
        self.indent -= 1

        lines.append("  " * self.indent + "}")
        return "\n".join(lines)

    # --- expressions ---
    def gen_expr(self, e):
        if e is None:
            return "null"

        if hasattr(e, "primary") and e.primary():
            return self.gen_primary(e.primary())

        if hasattr(e, "left") and hasattr(e, "right") and hasattr(e, "op"):
            a = self.gen_expr(e.left)
            b = self.gen_expr(e.right)
            op = e.op.text
            op_map = {"AND": "&&", "OR": "||", "=": "==", "<>": "!="}
            op2 = op_map.get(op.upper(), op)
            return f"({a} {op2} {b})"

        if hasattr(e, "getText"):
            return e.getText()

        return "null"

    def gen_primary(self, ctx):
        # NEW
        if hasattr(ctx, "newExpr") and ctx.newExpr():
            return self.gen_new(ctx.newExpr())

        if hasattr(ctx, "NUMBER") and ctx.NUMBER():
            return ctx.NUMBER().getText()

        if hasattr(ctx, "STRING") and ctx.STRING():
            return ctx.STRING().getText()

        if hasattr(ctx, "IDENT") and ctx.IDENT():
            name = ctx.IDENT().getText()
            if name.upper() == "THIS":
                return "this"
            if name.upper() == "NIL":
                return "null"
            return name

        if hasattr(ctx, "dottedRef") and ctx.dottedRef():
            return self.gen_dotted_ref(ctx.dottedRef())

        if hasattr(ctx, "callExpr") and ctx.callExpr():
            return self.gen_call(ctx.callExpr())

        return "null"

    def gen_dotted_ref(self, ctx):
        parts = [t.getText() for t in ctx.IDENT()]
        if parts and parts[0].upper() == "THIS":
            parts[0] = "this"
        return ".".join(parts)

    def gen_new(self, ctx):
        # JS: entweder direkt new ClassName(...) ODER Runtime NEWOBJ
        # Da du Klassen evtl. nicht immer als JS-Klasse hast: robust über NEWOBJ("Class", args)
        class_name = ctx.IDENT().getText()
        args = []
        if hasattr(ctx, "argList") and ctx.argList():
            for a in ctx.argList().expr():
                args.append(self.gen_expr(a))
        return f'NEWOBJ("{class_name}", ' + ", ".join(args) + ")" if args else f'NEWOBJ("{class_name}")'

    def gen_call(self, ctx):
        if hasattr(ctx, "dottedRef") and ctx.dottedRef():
            callee = self.gen_dotted_ref(ctx.dottedRef())
        elif hasattr(ctx, "IDENT") and ctx.IDENT():
            callee = ctx.IDENT().getText()
        else:
            callee = "/*callee*/"

        args = []
        if hasattr(ctx, "argList") and ctx.argList():
            for a in ctx.argList().expr():
                args.append(self.gen_expr(a))

        # WRITE als Funktion
        if callee.upper() == "WRITE":
            callee = "WRITE"

        return callee + "(" + ", ".join(args) + ")"
        
class DBaseToVBAAccess:
    """
    Generiert:
      - <module_name>.bas  (Standardmodul mit Public Sub Main oder Hilfsprocs)
      - <class_name>.cls   (Class Module)
      - RT.bas, PushButton.cls (Runtime)
    """
    def __init__(self, parser, class_name="GenProg", module_name="GenProg"):
        self.parser = parser
        self.class_name = class_name
        self.module_name = module_name

        self.out = []
        self.indent = 0
        self._cur_func = None  # für RETURN in VBA

    # --- Reuse von deinen robusten Helfern (Block/WRITE/ASSIGN/FOR) ---
    def iter_block_statements(self, block):
        if block is None:
            return []
        for attr in ("stmt", "statement", "stat", "statementList", "stmtList", "stmts"):
            fn = getattr(block, attr, None)
            if callable(fn):
                try:
                    res = fn()
                    if res is None:
                        continue
                    return res if isinstance(res, list) else [res]
                except TypeError:
                    pass
        kids = list(getattr(block, "children", []) or [])
        out = []
        for ch in kids:
            t = type(ch).__name__.lower()
            if "stmt" in t or "statement" in t or "stat" in t:
                out.append(ch)
        return out

    def get_write_exprs(self, wctx):
        if wctx is None:
            return []
        if hasattr(wctx, "expr"):
            expr_attr = getattr(wctx, "expr")
            if callable(expr_attr):
                try:
                    res = expr_attr()
                    if res is not None:
                        return res if isinstance(res, list) else [res]
                except TypeError:
                    pass
            try:
                out = []
                i = 0
                while True:
                    out.append(expr_attr(i))
                    i += 1
            except Exception:
                if out:
                    return out
        if hasattr(wctx, "exprList") and wctx.exprList():
            el = wctx.exprList()
            if hasattr(el, "expr") and callable(el.expr):
                res = el.expr()
                if res is not None:
                    return res if isinstance(res, list) else [res]
        if hasattr(wctx, "primary") and wctx.primary():
            p = wctx.primary()
            return p if isinstance(p, list) else [p]
        kids = list(getattr(wctx, "children", []) or [])
        out = []
        for ch in kids:
            t = type(ch).__name__.lower()
            if "expr" in t or "primary" in t:
                out.append(ch)
        return out

    def get_assign_lhs(self, actx):
        if actx is None:
            return None
        for name in ("lhs", "lvalue", "target", "left", "ref"):
            fn = getattr(actx, name, None)
            if callable(fn):
                try:
                    res = fn()
                    if res is not None:
                        return res
                except TypeError:
                    pass
        if hasattr(actx, "dottedRef") and actx.dottedRef():
            return actx.dottedRef()
        if hasattr(actx, "IDENT") and actx.IDENT():
            return actx.IDENT()
        kids = list(getattr(actx, "children", []) or [])
        for ch in kids:
            t = type(ch).__name__.lower()
            if "dottedref" in t or "lvalue" in t or "ref" in t or "primary" in t:
                return ch
        return None

    def get_assign_rhs(self, actx):
        if actx is None:
            return None
        if hasattr(actx, "expr") and callable(actx.expr):
            try:
                res = actx.expr()
                if isinstance(res, list):
                    return res[-1] if res else None
                if res is not None:
                    return res
            except TypeError:
                i = 0
                last = None
                while True:
                    try:
                        last = actx.expr(i)
                        i += 1
                    except Exception:
                        break
                return last
        kids = list(getattr(actx, "children", []) or [])
        for ch in reversed(kids):
            if "expr" in type(ch).__name__.lower() or hasattr(ch, "primary"):
                return ch
        return None

    # ---------- file writing ----------
    def generate(self, tree, filename):
        # 2) Klasse generieren
        self.out, self.indent = [], 0
        self._emit_class_header()
        self._gen_tree(tree)
        cls_code = self.get_code()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(cls_code)

    # ---------- emit helpers ----------
    def emit(self, s=""):
        self.out.append("    " * self.indent + s)

    def get_code(self):
        return "\n".join(self.out)

    def _emit_class_header(self):
        # Access .cls Textformat braucht keinen speziellen Header, nur Option/Explicit ist gut.
        self.emit("Option Compare Database")
        self.emit("Option Explicit")
        self.emit()

    # ---------- tree driving ----------
    def _gen_tree(self, tree):
        # je nach deinem parse-tree:
        if hasattr(tree, "item"):
            for it in tree.item():
                self.gen_item(it)
        else:
            self.gen_any(tree)

    def gen_any(self, node):
        if hasattr(node, "classDecl") and node.classDecl():
            return self.gen_class(node.classDecl())
        if hasattr(node, "children"):
            for ch in (node.children or []):
                self.gen_any(ch)

    # ---------- old schema entrypoints ----------
    def gen_item(self, it):
        if hasattr(it, "classDecl") and it.classDecl():
            return self.gen_class(it.classDecl())
        # sonst ignorieren
        return None

    def gen_class(self, ctx):
        # VBA: wir generieren i.d.R. genau eine Klasse als Ziel (class_name),
        # aber du kannst auch ctx.name.text nehmen – je nachdem was du willst.
        cls = self.class_name

        body = ctx.classBody()
        children = list(getattr(body, "children", []) or [])

        # Properties
        for ch in children:
            if hasattr(ch, "propertyDecl") and ch.propertyDecl():
                self.gen_property(ch.propertyDecl())

        # Methods
        for ch in children:
            if hasattr(ch, "methodDecl") and ch.methodDecl():
                self.gen_method(ch.methodDecl())

    def gen_property(self, ctx):
        name = ctx.IDENT().getText()
        # VBA: als Public Variant (dynamisch)
        self.emit(f"Public {name} As Variant")

    def gen_method(self, ctx):
        name = ctx.IDENT().getText()
        self._cur_func = name

        params = []
        if hasattr(ctx, "paramList") and ctx.paramList():
            for p in ctx.paramList().IDENT():
                params.append(f"ByVal {p.getText()} As Variant")

        self.emit()
        self.emit(f"Public Function {name}(" + ", ".join(params) + ") As Variant")
        self.indent += 1

        block = ctx.block()
        for st in self.iter_block_statements(block):
            self._emit_stmt_multiline(self.gen_stmt(st))

        # Default return
        self.emit(f"{name} = Null")
        self.indent -= 1
        self.emit("End Function")

        self._cur_func = None

    def _emit_stmt_multiline(self, s):
        for line in s.split("\n"):
            self.emit(line)

    # ---------- statements ----------
    def gen_stmt(self, st):
        # WRITE
        if hasattr(st, "writeStmt") and st.writeStmt():
            w = st.writeStmt()
            exprs = self.get_write_exprs(w)
            if not exprs:
                return "Debug.Print"
            args = ", ".join(self.gen_expr(ex) for ex in exprs)
            # wir nutzen RT.WRITE, damit multi-args sauber sind
            return f"WRITE {args}"

        # ASSIGN
        if hasattr(st, "assignStmt") and st.assignStmt():
            a = st.assignStmt()
            lhs_ctx = self.get_assign_lhs(a)
            rhs_ctx = self.get_assign_rhs(a)
            lhs = self.gen_expr(lhs_ctx) if lhs_ctx is not None else "/*lhs*/"
            rhs = self.gen_expr(rhs_ctx) if rhs_ctx is not None else "/*rhs*/"

            # VBA braucht Set bei Objektzuweisung. Heuristik: rhs beginnt mit NEWOBJ(...) oder New ...
            rhs_trim = rhs.lstrip()
            if rhs_trim.upper().startswith("NEWOBJ(") or rhs_trim.upper().startswith("NEW "):
                return f"Set {lhs} = {rhs}"
            return f"{lhs} = {rhs}"

        # RETURN
        if hasattr(st, "returnStmt") and st.returnStmt():
            r = st.returnStmt()
            if hasattr(r, "expr") and r.expr():
                val = self.gen_expr(r.expr())
                fn = self._cur_func or "/*func*/"
                return f"{fn} = {val}\nExit Function"
            return "Exit Function"

        # BREAK
        if hasattr(st, "breakStmt") and st.breakStmt():
            return "Exit For"

        # IF
        if hasattr(st, "ifStmt") and st.ifStmt():
            return self.gen_if(st.ifStmt())

        # FOR
        if hasattr(st, "forStmt") and st.forStmt():
            return self.gen_for(st.forStmt())

        # expr stmt
        if hasattr(st, "expr") and st.expr():
            return self.gen_expr(st.expr())

        return f"' TODO stmt: {type(st).__name__}"

    def gen_if(self, ctx):
        cond = self.gen_expr(ctx.expr())
        lines = [f"If {cond} Then"]

        then_blk = ctx.thenBlock() if hasattr(ctx, "thenBlock") else (ctx.block(0) if hasattr(ctx, "block") else None)
        self.indent += 1
        for st in self.iter_block_statements(then_blk):
            lines.append("    " * self.indent + self.gen_stmt(st))
        self.indent -= 1

        # else optional
        else_blk = None
        if hasattr(ctx, "elseBlock") and ctx.elseBlock():
            else_blk = ctx.elseBlock()
        elif hasattr(ctx, "block") and len(ctx.block()) > 1:
            else_blk = ctx.block(1)

        if else_blk is not None:
            lines.append("Else")
            self.indent += 1
            for st in self.iter_block_statements(else_blk):
                lines.append("    " * self.indent + self.gen_stmt(st))
            self.indent -= 1

        lines.append("End If")
        return "\n".join(lines)

    def gen_for(self, ctx):
        # Da deine ForStmtContext kein expr() hat, bleibt es heuristisch:
        var = ctx.IDENT().getText() if hasattr(ctx, "IDENT") and ctx.IDENT() else "i"

        start_ctx = None
        end_ctx = None
        step_ctx = None

        # häufig: startExpr/toExpr/stepExpr etc.
        for nm in ("startExpr", "fromExpr", "start"):
            fn = getattr(ctx, nm, None)
            if callable(fn):
                try:
                    start_ctx = fn()
                    if start_ctx is not None:
                        break
                except TypeError:
                    pass

        for nm in ("endExpr", "toExpr", "end"):
            fn = getattr(ctx, nm, None)
            if callable(fn):
                try:
                    end_ctx = fn()
                    if end_ctx is not None:
                        break
                except TypeError:
                    pass

        for nm in ("stepExpr", "byExpr", "step"):
            fn = getattr(ctx, nm, None)
            if callable(fn):
                try:
                    step_ctx = fn()
                    if step_ctx is not None:
                        break
                except TypeError:
                    pass

        start = self.gen_expr(start_ctx) if start_ctx is not None else "0"
        end = self.gen_expr(end_ctx) if end_ctx is not None else "0"
        step = self.gen_expr(step_ctx) if step_ctx is not None else "1"

        lines = [f"Dim {var} As Long", f"For {var} = {start} To {end} Step {step}"]

        blk = ctx.block() if hasattr(ctx, "block") else None
        self.indent += 1
        for st in self.iter_block_statements(blk):
            lines.append("    " * self.indent + self.gen_stmt(st))
        self.indent -= 1

        lines.append("Next")
        return "\n".join(lines)

    # ---------- expressions ----------
    def gen_expr(self, e):
        if e is None:
            return "Null"

        if hasattr(e, "primary") and e.primary():
            return self.gen_primary(e.primary())

        # binary op (wenn dein AST so liefert)
        if hasattr(e, "left") and hasattr(e, "right") and hasattr(e, "op"):
            a = self.gen_expr(e.left)
            b = self.gen_expr(e.right)
            op = e.op.text
            op_map = {"AND": "And", "OR": "Or", "=": "=", "<>": "<>"}
            op2 = op_map.get(op.upper(), op)
            return f"({a} {op2} {b})"

        if hasattr(e, "getText"):
            return e.getText()

        return "Null"

    def gen_primary(self, ctx):
        if hasattr(ctx, "newExpr") and ctx.newExpr():
            return self.gen_new(ctx.newExpr())

        if hasattr(ctx, "NUMBER") and ctx.NUMBER():
            return ctx.NUMBER().getText()

        if hasattr(ctx, "STRING") and ctx.STRING():
            return ctx.STRING().getText()

        if hasattr(ctx, "IDENT") and ctx.IDENT():
            name = ctx.IDENT().getText()
            if name.upper() == "THIS":
                return "Me"
            if name.upper() == "NIL":
                return "Nothing"
            return name

        if hasattr(ctx, "dottedRef") and ctx.dottedRef():
            return self.gen_dotted_ref(ctx.dottedRef())

        if hasattr(ctx, "callExpr") and ctx.callExpr():
            return self.gen_call(ctx.callExpr())

        return "Null"

    def gen_dotted_ref(self, ctx):
        parts = [t.getText() for t in ctx.IDENT()]
        if parts and parts[0].upper() == "THIS":
            parts[0] = "Me"
        return ".".join(parts)

    def gen_new(self, ctx):
        # VBA kann New <Class> nicht mit Args. Daher: RT.NEWOBJ("Class", args...)
        class_name = ctx.IDENT().getText()
        args = []
        if hasattr(ctx, "argList") and ctx.argList():
            for a in ctx.argList().expr():
                args.append(self.gen_expr(a))
        if args:
            return f'NEWOBJ("{class_name}", ' + ", ".join(args) + ")"
        return f'NEWOBJ("{class_name}")'

    def gen_call(self, ctx):
        # callee
        if hasattr(ctx, "dottedRef") and ctx.dottedRef():
            callee = self.gen_dotted_ref(ctx.dottedRef())
        elif hasattr(ctx, "IDENT") and ctx.IDENT():
            callee = ctx.IDENT().getText()
        else:
            callee = "/*callee*/"

        # args
        args = []
        if hasattr(ctx, "argList") and ctx.argList():
            for a in ctx.argList().expr():
                args.append(self.gen_expr(a))

        return callee + "(" + ", ".join(args) + ")"
        
class DBaseToPython:
    """
    ParseTree -> Python source (calls into your runtime 'rt').
    - No direct attribute access; all member ops go through rt.GET/rt.SET/rt.CALL
    - Keeps dBase semantics in runtime, not in generated python.
    """

    def __init__(self, parser, classes=None):
        self.p = parser
        self.out = PyEmitter()
        self.classes = classes or {}  # optional: your collected ClassDefs, if you want structure

    # ---------- public ----------
    def generate(self, tree, out_path: str):
        self.out.emit("# generated by dBaseToPython (runtime-backed)")
        self.out.emit("from dBaseRuntimeFacade import RT")
        self.out.emit("")
        self.out.emit("rt = RT()")
        self.out.emit("")
        self.out.emit("def main():")
        self.out.indent()

        self.gen_input(tree)  # adapt name to your root rule

        self.out.dedent()
        self.out.emit("")
        self.out.emit("if __name__ == '__main__':")
        self.out.indent()
        self.out.emit("main()")
        self.out.dedent()

        Path(out_path).write_text(self.out.text(), encoding="utf-8")

    # ---------- root / statements ----------
    def gen_input(self, ctx):
        # input : item* EOF
        for it in ctx.item():
            self.gen_item(it)

    def gen_item(self, it):
        # Dispatch by available child rule; adapt to your grammar structure
        # item : classDecl | methodDecl | statement
        if it.statement():
            return self.gen_stmt(it.statement())
        if it.classDecl():
            return self.gen_class(it.classDecl())
        if it.methodDecl():
            return self.gen_method(it.methodDecl())

        # fallback:
        self.out.emit(f"# TODO unhandled stmt: {type(it).__name__}")

    def gen_stmt(self, st):
        if st.ifStmt():            return self.gen_if(st.ifStmt())
        if st.forStmt():           return self.gen_for(st.forStmt())
        if st.doWhileStatement():  return self.gen_do_while(st.doWhileStatement())

        if st.writeStmt():         return self.gen_write(st.writeStmt())
        if st.assignStmt():        return self.gen_assign(st.assignStmt())
        if st.localDeclStmt():     return self.gen_local_decl(st.localDeclStmt())
        if st.localAssignStmt():   return self.gen_local_assign(st.localAssignStmt())

        if st.callStmt():          return self.gen_call_stmt(st.callStmt())
        if st.exprStmt():          return self.gen_expr_stmt(st.exprStmt())

        if st.parameterStmt():     return self.gen_parameter(st.parameterStmt())
        if st.createFileStmt():    return self.gen_create_file(st.createFileStmt())
        if st.deleteStmt():        return self.gen_delete(st.deleteStmt())

        if st.withStmt():          return self.gen_with(st.withStmt())
        if st.doStmt():            return self.gen_do(st.doStmt())

        if st.returnStmt():        return self.gen_return(st.returnStmt())
        if st.breakStmt():         return self.gen_break(st.breakStmt())

        if st.classDecl():         return self.gen_class(st.classDecl())

        # bessere Debug-Ausgabe: zeig, was wirklich drinsteckt
        child0 = st.getChild(0)
        self.out.emit(f"# TODO unhandled statement: {type(child0).__name__}  text={st.getText()!r}")
    
    def gen_local_decl(self, ctx):
        # localDeclStmt : LOCAL name=IDENT ;
        name = ctx.name.text
        self.out.emit(f"rt.SET_NAME({name!r}, None)")

    def gen_local_assign(self, ctx):
        # localAssignStmt : LOCAL name=IDENT ASSIGN expr ;
        name = ctx.name.text
        rhs  = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.SET_NAME({name!r}, {rhs})")

    def gen_expr_stmt(self, ctx):
        # exprStmt : postfixExpr ;
        e = self.gen_postfix(ctx.postfixExpr())
        self.out.emit(e)

    def gen_call_stmt(self, ctx):
        # callStmt : CALL callTarget ;
        # callTarget : (SUPER DCOLON)? IDENT LPAREN argList? RPAREN ;
        # simplest: delegiere als "exprStmt" (Call ist Effekt)
        txt = ctx.callTarget().getText()
        self.out.emit(f"rt.CALL_STMT({txt!r})  # TODO: map callTarget sauber")

    def gen_do_while(self, ctx):
        # doWhileStatement : DO WHILE condition block ENDDO ;
        cond = self.gen_logical_or(ctx.condition().logicalOr())
        self.out.emit(f"while rt.TRUE({cond}):")
        self.out.indent()
        for st in ctx.block().statement():
            self.gen_stmt(st)
        self.out.dedent()

    def gen_delete(self, ctx):
        # deleteStmt : DELETE IDENT ;
        self.out.emit(f"rt.DELETE_NAME({ctx.IDENT().getText()!r})")

    def gen_create_file(self, ctx):
        # createFileStmt : CREATE FILE (expr)? ;
        arg = self.gen_expr(ctx.expr()) if ctx.expr() else "None"
        self.out.emit(f"rt.CREATE_FILE({arg})")
        
    def gen_break(self, ctx):
        self.out.emit("break")
        
    def gen_parameter(self, ctx):
        p = ctx.paramNames()
        names = [t.getText() for t in p.IDENT()]
        self.out.emit(f"rt.PARAMETER({names!r})")
    
    def new_temp(self):
        n = getattr(self, "_tmp_i", 0) + 1
        self._tmp_i = n
        return f"_t{n}"

    def gen_with(self, ctx):
        # withStmt : WITH LPAREN withTarget RPAREN withBody ENDWITH ;

        base = self.gen_with_target(ctx.withTarget())
        tmp = self.new_temp()

        # base einmal auswerten (wichtig, falls es ein Call/Expr ist)
        self.out.emit(f"{tmp} = {base}")
        self.out.emit(f"rt.PUSH_WITH({tmp})")

        # body: (withAssignStmt | withStmt | statement)*
        body = ctx.withBody()
        for ch in list(getattr(body, "children", []) or []):
            # ANTLR liefert "TerminalNode" auch als children, die ignorieren wir
            if hasattr(ch, "withAssignStmt") and ch.withAssignStmt():
                self.gen_with_assign(ch.withAssignStmt())
            elif hasattr(ch, "withStmt") and ch.withStmt():
                self.gen_with(ch.withStmt())
            elif hasattr(ch, "statement") and ch.statement():
                self.gen_stmt(ch.statement())
            else:
                # manchmal ist ch direkt der Context-Typ
                t = type(ch).__name__
                if t.endswith("WithAssignStmtContext"):
                    self.gen_with_assign(ch)
                elif t.endswith("WithStmtContext"):
                    self.gen_with(ch)
                elif t.endswith("StatementContext"):
                    self.gen_stmt(ch)
                else:
                    pass

        self.out.emit("rt.POP_WITH()")


    def gen_with_target(self, ctx):
        # withTarget : THIS | dottedRef | IDENT | postfixExpr ;
        if ctx.THIS():
            return "this"

        if ctx.dottedRef():
            base_expr, path = self.gen_dotted_ref_parts(ctx.dottedRef())
            return f"rt.GET('{base_expr.upper()}', {path})"

        if ctx.IDENT():
            # Variablenzugriff: runtime-semantisch (Scoping/WITH)
            name = ctx.IDENT().getText()
            return f"rt.GET_NAME({name!r})"

        if ctx.postfixExpr():
            # postfix kann call/member enthalten -> dein gen_postfix liefert runtime-Ausdruck
            return self.gen_postfix(ctx.postfixExpr())

        return f"rt.PRIMARY({ctx.getText()!r})"


    def gen_with_assign(self, ctx):
        # withAssignStmt : withLvalue ASSIGN expr ;
        path = [t.getText() for t in ctx.withLvalue().IDENT()]  # z.B. ["top"] oder ["pushbutton1","width"]
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.WITH_SET({path!r}, {rhs})")
    # ---------- WRITE ----------
    def gen_write_arg(self, actx):
        # writeArg : STRING | dottedRef | expr ;
        if actx.STRING():
            return actx.STRING().getText()
        if actx.dottedRef():
            base_expr, path = self.gen_dotted_ref_parts(actx.dottedRef())
            return f"rt.GET('{base_expr.upper()}', {path})"
        if actx.expr():
            return self.gen_expr(actx.expr())
        return f"rt.PRIMARY({actx.getText()!r})"
        
    def gen_write(self, ctx):
        # writeStmt : WRITE writeArg (PLUS writeArg)* ;
        parts = [self.gen_write_arg(a) for a in ctx.writeArg()]

        if not parts:
            self.out.emit("rt.WRITE('')")   # sollte praktisch nie passieren
            return

        # WRITE a + b + c  -> runtime-konforme Verkettung
        expr = parts[0]
        for p in parts[1:]:
            expr = f"rt.BINOP({expr}, '+', {p})"

        self.out.emit(f"rt.WRITE({expr})")

    # ---------- assignment ----------
    def lvalue_chain_from_postfix(self, pe):
        # postfixExpr : primary ( '(' ... ')' | ('.'|'::') IDENT )*
        chain = [pe.primary().getText()]
        i = 1
        while i < pe.getChildCount():
            ch = pe.getChild(i).getText()

            if ch == '.':
                chain.append(pe.getChild(i + 1).getText())
                i += 2
                continue

            if ch == '(':
                raise Exception(f"LVALUE darf keinen Call enthalten: {pe.getText()}")

            i += 1
        return chain
        
    def gen_assign(self, ctx):
        rhs = self.gen_expr(ctx.expr())
        lv = ctx.lvalue()

        # 1) dottedRef direkt (THIS.X.Y ...)
        if lv.dottedRef():
            base_expr, path = self.gen_dotted_ref_parts(lv.dottedRef())
            self.out.emit(f"rt.SET({base_expr}, {path}, {rhs})")
            return

        # 2) postfixExpr als LHS: kann "Y" oder "THIS.X.Y" sein
        pe = lv.postfixExpr()
        if pe:
            chain = self.lvalue_chain_from_postfix(pe)   # z.B. ["Y"] oder ["THIS","PushButton1","Text"]

            if len(chain) == 1:
                # wichtig: über Runtime setzen, damit WITH/Scopes wie im Interpreter funktionieren
                self.out.emit(f"rt.SET_NAME({chain[0]!r}, {rhs})")
                return

            # Kette: base + path
            head = chain[0]
            if head.upper() == "THIS":
                base_expr = "this"
                path = chain[1:]
            else:
                base_expr = self.norm_local(head)
                path = chain[1:]

            self.out.emit(f"rt.SET({base_expr}, {path!r}, {rhs})")
            return

        self.out.emit(f"# TODO unsupported lvalue: {lv.getText()}")

    # ---------- IF ----------
    def gen_if(self, ctx):
        # ifStmt : IF expr block (ELSE block)? ENDIF ;
        cond = self.gen_expr(ctx.expr())
        self.out.emit(f"if rt.TRUE({cond}):")
        self.out.indent()

        # then-block
        then_block = ctx.block(0)
        for st in then_block.statement():
            self.gen_stmt(st)

        self.out.dedent()

        # else-block (optional)
        if ctx.ELSE():
            self.out.emit("else:")
            self.out.indent()

            else_block = ctx.block(1)
            for st in else_block.statement():
                self.gen_stmt(st)

            self.out.dedent()

    # ---------- FOR ----------
    def gen_for(self, ctx):
        # forStmt : FOR IDENT ASSIGN expr TO expr (STEP expr)? block ENDFOR ;
        
        var = self.norm_local(ctx.IDENT().getText())
        
        start = ctx.numberExpr(0).getText()
        end   = ctx.numberExpr(1).getText()
        step  = ctx.numberExpr(2).getText() if ctx.STEP() else "1"
        
        # dBase TO ist inklusiv -> Runtime-Helper
        self.out.emit(f"for {var} in rt.RANGE_INCL({start}, {end}, {step}):")
        self.out.indent()
        for st in ctx.block().statement():
            self.gen_stmt(st)
        self.out.dedent()

    # ---------- RETURN ----------
    def gen_return(self, ctx):
        if ctx.expr():
            self.out.emit(f"return {self.gen_expr(ctx.expr())}")
        else:
            self.out.emit("return")

    # ---------- CLASS / METHOD ----------
    def gen_class(self, ctx):
        cname = ctx.name.text  # adapt
        parent = ctx.parent.text if ctx.parent else "OBJECT"

        self.out.emit(f"class {self.norm_class(cname)}({self.norm_class(parent)}):")
        self.out.indent()
        self.out.emit("def __init__(self, *args):")
        self.out.indent()
        self.out.emit("super().__init__()")
        self.out.emit("self._instance = rt.MAKE_INSTANCE(self, args)")  # or however you represent instances
        self.out.dedent()
        self.out.emit("")

        # properties/methods in body: adapt to your classBody structure
        body = ctx.classBody()
        for ch in list(getattr(body, "children", []) or []):
            if hasattr(ch, "methodDecl") and ch.methodDecl():
                self.gen_method(ch.methodDecl())
            else:
                # propertyDecl / init statements -> put into __init__ or Init method
                pass

        self.out.dedent()
        self.out.emit("")

    def gen_method(self, mctx):
        mname = mctx.IDENT().getText()
        params = [p.getText() for p in mctx.paramList().IDENT()] if mctx.paramList() else []
        pyparams = ", ".join(["self"] + [self.norm_local(p) for p in params])

        self.out.emit(f"def {self.norm_method(mname)}({pyparams}):")
        self.out.indent()
        # inside methods, dBase THIS maps to `self` (or `this`)
        self.out.emit("this = self")
        # method statements:
        for st in mctx.block().statement():
            self.gen_stmt(st)
        self.out.dedent()
        self.out.emit("")


    def gen_new(self, ctx):
        class_name = ctx.IDENT().getText()
        args = [self.gen_expr(e) for e in ctx.argList().expr()] if ctx.argList() else []
        return f"rt.NEW({class_name!r}, {', '.join(args)})"

    def gen_call(self, ctx):
        # something like dottedRef '(' args ')'
        base_expr, path = self.gen_dotted_ref_parts(ctx.dottedRef())
        args = [self.gen_expr(e) for e in ctx.argList().expr()] if ctx.argList() else []
        return f"rt.CALL({base_expr}, {path}, [{', '.join(args)}])"

    def gen_dotted_ref_parts(self, dctx):
        # e.g. THIS.PushButton1.Text -> base=this, path=["PushButton1","Text"]
        parts = [t.getText() for t in dctx.IDENT()]

        head = parts[0]
        if head.upper() == "THIS":
            base = "this"
            path = parts[1:]
        else:
            base = self.norm_local(head)
            path = parts[1:]

        return base, repr(path)

    # ---------- naming ----------
    def norm_local(self, name: str) -> str:
        # conservative: keep letters/digits/_ and lower it
        return "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in name).lower()

    def norm_class(self, name: str) -> str:
        # keep it simple; you can make PascalCase if you like
        return "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in name)

    def norm_method(self, name: str) -> str:
        return self.norm_local(name)
        
        
    def gen_expr(self, ctx):
        # expr : logicalOr ;
        return self.gen_logical_or(ctx.logicalOr())

    def gen_logical_or(self, ctx):
        # logicalOr : logicalAnd (OR logicalAnd)* ;
        parts = [self.gen_logical_and(x) for x in ctx.logicalAnd()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, 'OR', {rhs})"
        return out

    def gen_logical_and(self, ctx):
        # logicalAnd : logicalNot (AND logicalNot)* ;
        parts = [self.gen_logical_not(x) for x in ctx.logicalNot()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, 'AND', {rhs})"
        return out

    def gen_logical_not(self, ctx):
        # logicalNot : NOT logicalNot | comparison ;
        if ctx.NOT():
            inner = self.gen_logical_not(ctx.logicalNot())
            return f"rt.UNOP('NOT', {inner})"
        return self.gen_comparison(ctx.comparison())

    def gen_comparison(self, ctx):
        # comparison : additiveExpr (compareOp additiveExpr)? ;
        left = self.gen_additive(ctx.additiveExpr(0))
        if ctx.compareOp():
            op = ctx.compareOp().getText()
            right = self.gen_additive(ctx.additiveExpr(1))
            return f"rt.BINOP({left}, {op!r}, {right})"
        return left

    def gen_additive(self, ctx):
        # additiveExpr : multiplicativeExpr ((PLUS|MINUS) multiplicativeExpr)* ;
        terms = [self.gen_multiplicative(x) for x in ctx.multiplicativeExpr()]
        out = terms[0]
        # Operatoren stehen als Token zwischen den Termen -> über getChildren laufen
        # Einfacher: Text-basiert paaren (robust genug für Start)
        # Wir bauen anhand der Kindersequenz: term (op term)*.
        children = list(ctx.getChildren())
        i = 1
        while i < len(children):
            op = children[i].getText()
            rhs = terms[(i + 1) // 2]
            out = f"rt.BINOP({out}, {op!r}, {rhs})"
            i += 2
        return out

    def gen_multiplicative(self, ctx):
        # multiplicativeExpr : postfixExpr ((STAR|SLASH) postfixExpr)* ;
        factors = [self.gen_postfix(x) for x in ctx.postfixExpr()]
        out = factors[0]
        children = list(ctx.getChildren())
        i = 1
        while i < len(children):
            op = children[i].getText()
            rhs = factors[(i + 1) // 2]
            out = f"rt.BINOP({out}, {op!r}, {rhs})"
            i += 2
        return out

    def gen_postfix(self, ctx):
        # postfixExpr : primary ( LPAREN argList? RPAREN | (DOT|DCOLON) IDENT )* ;
        cur = self.gen_primary(ctx.primary())

        # Wir laufen über die restlichen Kinder und erkennen Muster:
        # ( ... )  oder . IDENT / :: IDENT
        kids = list(ctx.getChildren())
        k = 1
        while k < len(kids):
            t = kids[k].getText()

            if t == "(":
                # call: ( argList? )
                # argList ist optional und sitzt zwischen '(' und ')'
                args = []
                # wenn nächstes Kind nicht ')', ist es argList
                if kids[k + 1].getText() != ")":
                    # kids[k+1] ist der argList-Context
                    argctx = kids[k + 1]
                    args = [self.gen_expr(e) for e in argctx.expr()]
                    k += 1  # argList "verbraucht"
                cur = f"rt.CALL_ANY({cur}, [{', '.join(args)}])"
                k += 2  # überspringe ')'
                continue

            if t in (".", "::"):
                name = kids[k + 1].getText()
                cur = f"rt.GET_ATTR({cur}, {name!r})"
                k += 2
                continue

            # fallback (sollte selten passieren)
            k += 1

        return cur

    def gen_primary(self, ctx):
        # primary:
        # handlerList | newExpr | memberExpr | literal | THIS | SUPER | FLOAT | NUMBER
        # | IDENT | STRING | BRACKET_STRING | '(' expr ')'
        if ctx.THIS():
            return "this"

        if ctx.SUPER():
            return "super_obj"  # falls du es nutzt; sonst an runtime delegieren

        if ctx.STRING():
            return ctx.STRING().getText()

        if ctx.BRACKET_STRING():
            return ctx.BRACKET_STRING().getText()

        if ctx.NUMBER():
            return ctx.NUMBER().getText()

        if ctx.FLOAT():
            return ctx.FLOAT().getText()

        if ctx.IDENT():
            return self.norm_local(ctx.IDENT().getText())

        if ctx.literal():
            return ctx.literal().getText()

        if ctx.newExpr():
            return self.gen_new(ctx.newExpr())

        # ( expr )
        if ctx.expr():
            return self.gen_expr(ctx.expr())

        # memberExpr/handlerList erstmal roh:
        return f"rt.PRIMARY({ctx.getText()!r})"


class ExceptionDialog(QDialog):
    def __init__(self, title, message, details, parent=None):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.resize(900, 520)

        layout = QVBoxLayout(self)

        label = QLabel(message, self)
        label.setWordWrap(True)
        layout.addWidget(label)

        self.details = QTextEdit(self)
        self.details.setReadOnly(True)
        self.details.setPlainText(details)
        layout.addWidget(self.details, 1)

        buttons = QHBoxLayout()
        buttons.addStretch(1)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.accept)

        buttons.addWidget(close_button)
        layout.addLayout(buttons)

# ---------------------------------------------------------------------------
# \brief setup exception handler output to gui application for python throw
# ---------------------------------------------------------------------------
def show_exception_dialog(exc_type, exc_value, exc_traceback):
    # KeyboardInterrupt normal durchlassen
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    details = "".join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)
    )

    with open("error.log", "a", encoding="utf-8") as f:
        f.write(details)
        f.write("\n" + "=" * 80 + "\n")

    print(details)

    app = QApplication.instance()
    if app is None:
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    dlg = ExceptionDialog(
        "Unhandled Exception",
        str(exc_value),
        details,
        None
    )
    dlg.exec_()
    sys.exit(1)


# ---------------------------------------------------------------------------
# \brief setup exception handler output to gui application for threaded throw
# ---------------------------------------------------------------------------
def show_thread_exception(args):
    show_exception_dialog(
        args.exc_type,
        args.exc_value,
        args.exc_traceback
    )


# ---------------------------------------------------------------------------
# \brief this is the main entry point definition to start the qt5 application
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sys      .excepthook = show_exception_dialog
    threading.excepthook = show_thread_exception

    sys.exit(run_language_app("dbase"))
