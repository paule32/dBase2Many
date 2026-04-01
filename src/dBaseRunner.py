from __future__ import annotations

import sys

from share import run_language_app

# -----------------------------------------------------------------------
# dbase interpreter lexer + parser ...
# -----------------------------------------------------------------------
from parse.dbase.dBaseLexer          import dBaseLexer
from parse.dbase.dBaseParser         import dBaseParser
from parse.dbase.dBaseParserVisitor  import dBaseParserVisitor

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

class ScopeStack:
    def __init__(self):
        self._scopes = [{}]  # global scope

    def push(self):
        self._scopes.append({})

    def pop(self):
        if len(self._scopes) == 1:
            raise RuntimeError("Cannot pop global scope")
        self._scopes.pop()

    def set(self, name: str, value):
        self._scopes[-1][name] = value

    def get(self, name: str):
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        raise KeyError(name)

    def has(self, name: str) -> bool:
        for scope in reversed(self._scopes):
            if name in scope:
                return True
        return False
        
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

# ---------------------------------------------------------------------------
# ExecVisitor - Interpreter for dBase DSL ...
# ---------------------------------------------------------------------------
class ExecVisitor(dBaseParserVisitor):
    def __init__(self):
        super().__init__()
        self.output  = []  # legacy buffer (WRITE wird direkt ins Debug-Fenster geroutet)
        self._mode = ""
        self._class_line_ranges = None
        
        self.vars: Dict[str, object] = {}   # normale Variablen
        self.this_obj: object | None = None # aktuelles "this"
        
        self.globals = {}
        self._scopes = [{}]        # stack of dicts
        
        self.env = ScopeStack()
        self.classes = {}          # className -> {"parent": str, "methods": {methodName: MethodDef}}
        
        self.classes["OBJECT"] = ClassDef(
            parent     = None,
            name       = "OBJECT",
            methods    = {"POPS": ""}
        )
        
        self.classes["PUSHBUTTON"] = ClassDef(
            parent     = "OBJECT",
            name       = "PUSHBUTTON",
            methods    = {"MOPS": ""},
            default_props = {       # <-- neu
                "path": "",
                "handle": None,
                "isopen": False,
                "mode": "",
                "eof": False,
                "pos": 0,
            }
        )
        
        self.methods = {}          # top-level METHOD name -> MethodDef / MethodDeclContext
        self._current_filename = ""

        self.frames: list[Frame] = [Frame(name="<global>")]  # globaler Frame
        self._current_class = None
        
        self.this_stack = []
        self.with_stack      : list[object] = []
        self.with_stack_owner: list[object] = []
        
        # --- DBF exclusive locks (USE ... EXCLUSIVE) ---
        # maps absolute dbf_path -> lockfile path
        self._dbf_exclusive_locks: dict[str, str] = {}
        
        # Builtins
        self.set_var("USE", self._builtin_USE)
        self.set_var("INPUT", self._builtin_INPUT)
        # interne Builtins aus der Vorverarbeitung
        self.set_var("__DBASE_USE__", self._builtin_USE)
        self.set_var("__DBASE_ERASE__", self._builtin_ERASE)
        self.set_var("__DBASE_SET_FORMAT__", self._builtin_SET_FORMAT)
        self.set_var("__DBASE_SET_PRINT__", self._builtin_SET_PRINT)
        self.set_var("__DBASE_SET_MARGIN__", self._builtin_SET_MARGIN)
        self.set_var("__DBASE_SET_COLOR__", self._builtin_SET_COLOR)
        self.set_var("__DBASE_SET_ESCAPE__", self._builtin_SET_ESCAPE)
        self.set_var("__DBASE_SET_CONFIRM__", self._builtin_SET_CONFIRM)
        self.set_var("__DBASE_SET_DELETE__", self._builtin_SET_DELETE)
        self.set_var("__DBASE_STORE__", self._builtin_STORE)
        self.set_var("__DBASE_SAVE__", self._builtin_SAVE)
        self.set_var("__DBASE_RESTORE__", self._builtin_RESTORE)
        self.set_var("__DBASE_RELEASE__", self._builtin_RELEASE)
        self.set_var("__DBASE_SELECT__", self._builtin_SELECT)
        self.set_var("__DBASE_RENAME__", self._builtin_RENAME)
        self.set_var("__DBASE_CLEAR_ALL__", self._builtin_CLEAR_ALL)
        self.set_var("__DBASE_SKIP__", self._builtin_SKIP)
        self.set_var("__DBASE_GOTO__", self._builtin_GOTO)
        self.set_var("__DBASE_DELETE_RECORD__", self._builtin_DELETE_RECORD)
        self.set_var("__DBASE_PACK__", self._builtin_PACK)
        self.set_var("__DBASE_ZAP__", self._builtin_ZAP)
        self.set_var("__DBASE_COUNT__", self._builtin_COUNT)

        # DBF-Arbeitsbereiche immer sofort initialisieren, damit SELECT/USE
        # bereits im ersten Script-Lauf sicher funktionieren.
        self._init_workareas()
    
    def _builtin_ERASE(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0
        _clear_runtime_output()
        return 0

    def _builtin_SET_FORMAT(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0
        mode = "SCREEN"
        if args:
            raw = args[0]
            mode = raw if isinstance(raw, str) else str(raw)
        return _set_runtime_output_format(mode)

    def _builtin_SET_PRINT(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0
        enabled = False
        if args:
            raw = args[0]
            if isinstance(raw, str):
                enabled = raw.strip().upper() in ("1", "ON", "TRUE", ".T.", "T", "Y", ".Y.")
            else:
                enabled = bool(raw)
        return _set_runtime_print_enabled(enabled)

    def _builtin_SET_MARGIN(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0
        return _set_runtime_print_margin(*args)

    def _builtin_SET_COLOR(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0
        return _set_runtime_color(*args)

    def _builtin_SET_ESCAPE(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0
        enabled = False
        if args:
            raw = args[0]
            if isinstance(raw, str):
                enabled = raw.strip().upper() in ("1", "ON", "TRUE", ".T.", "T", "Y", ".Y.")
            else:
                enabled = bool(raw)
        return _set_runtime_escape_enabled(enabled)

    def _builtin_SET_CONFIRM(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0
        enabled = False
        if args:
            raw = args[0]
            if isinstance(raw, str):
                enabled = raw.strip().upper() in ("1", "ON", "TRUE", ".T.", "T", "Y", ".Y.")
            else:
                enabled = bool(raw)
        return _set_runtime_confirm_enabled(enabled)

    def _decode_builtin_text_arg(self, value, default: str = "") -> str:
        if value is None:
            return default
        s = str(value).strip()
        if not s:
            return default
        if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
            return self._unescape_string(s)
        if len(s) >= 2 and s[0] == '[' and s[-1] == ']':
            return self._unescape_bracket_string(s)
        return s

    def _is_reserved_memvar(self, name: str, value=None) -> bool:
        key = (name or '').upper()
        if key in ('THIS', 'SELF'):
            return True
        if key.startswith('__DBASE_'):
            return True
        if callable(value):
            return True
        return False

    def _match_mem_mask(self, name: str, mask: str) -> bool:
        import fnmatch
        return fnmatch.fnmatchcase((name or '').upper(), (mask or '').upper())

    def _flatten_memory_vars(self) -> dict[str, object]:
        merged: dict[str, object] = {}
        for scope in self._scopes:
            for key, value in scope.items():
                merged[key.upper()] = value
        return {k: v for k, v in merged.items() if not self._is_reserved_memvar(k, v)}

    def _select_memory_vars(self, mode: str = 'ALL', mask: str = '') -> dict[str, object]:
        mode = (mode or 'ALL').upper()
        mask = (mask or '').strip()
        items = self._flatten_memory_vars()
        if mode == 'ALL' or not mask:
            return dict(items)
        if mode == 'LIKE':
            return {k: v for k, v in items.items() if self._match_mem_mask(k, mask)}
        if mode == 'EXCEPT':
            return {k: v for k, v in items.items() if not self._match_mem_mask(k, mask)}
        raise RuntimeError(f"SAVE/RELEASE: unbekannter Auswahlmodus '{mode}'")

    def _jsonify_mem_value(self, value, var_name: str = ''):
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, (list, tuple)):
            return [self._jsonify_mem_value(v, var_name) for v in value]
        if isinstance(value, dict):
            return {str(k): self._jsonify_mem_value(v, var_name) for k, v in value.items()}
        raise RuntimeError(f"SAVE: Variable '{var_name}' ist nicht JSON-serialisierbar ({type(value).__name__})")

    def _resolve_memfile_path(self, filename: str = '', drive: str = '') -> Path:
        name = self._decode_builtin_text_arg(filename, 'memory.mem').strip()
        if not name:
            name = 'memory.mem'
        if not Path(name).suffix:
            name += '.mem'

        drv = self._decode_builtin_text_arg(drive, '').strip().rstrip(':')
        if drv:
            base = Path(f"{drv.upper()}:\\")
            path = base / name
        else:
            path = Path(name)
            if not path.is_absolute():
                cur = getattr(self, '_current_filename', '') or ''
                base_dir = Path(cur).resolve().parent if cur else Path.cwd()
                path = base_dir / path
        return Path(os.path.abspath(str(path)))

    def _confirm_memfile_overwrite(self, path: Path) -> None:
        if not path.exists() or not _RUNTIME_CONFIRM_ENABLED:
            return

        parent = MAINAPP if 'MAINAPP' in globals() else None
        answer = QMessageBox.question(
            parent,
            'Datei überschreiben?',
            f'Die Datei existiert bereits und wird überschrieben:\n\n{path}\n\nSoll die Datei überschrieben werden?',
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
        if answer != QMessageBox.Ok:
            raise ProgramAbortSignal()

        backup_path = path.with_name(path.name + '.bak')
        shutil.copy2(str(path), str(backup_path))

    def _clear_memory_variables(self):
        for scope in self._scopes:
            for key in list(scope.keys()):
                value = scope.get(key)
                if self._is_reserved_memvar(key, value):
                    continue
                scope.pop(key, None)

    def _delete_memory_variable(self, name: str):
        key = (name or '').strip().upper()
        if not key:
            return
        for scope in self._scopes:
            scope.pop(key, None)


    def _workarea_empty(self) -> dict[str, object]:
        return {
            "dbf_path": "",
            "indexes": [],
            "fields": [],
            "records": [],
            "pointer": 1,
            "eof": True,
            "version": 0x03,
        }

    def _workarea_state_file_path(self) -> Path:
        return Path(tempfile.gettempdir()) / ".dbase_workareas.json"

    def _mark_hidden_path(self, path: Path) -> None:
        try:
            if SystemInfo.is_windows():
                ctypes.windll.kernel32.SetFileAttributesW(str(path), 0x02)
        except Exception:
            pass

    def _init_workareas(self):
        self._selected_workarea = 0
        self._workareas = {i: self._workarea_empty() for i in range(65)}
        self._workarea_state_path = self._workarea_state_file_path()
        self._sync_workareas_state()

    def _sync_workareas_state(self):
        try:
            payload = {
                "selected": int(getattr(self, "_selected_workarea", 0)),
                "workareas": {},
            }
            for idx, ws in getattr(self, "_workareas", {}).items():
                recs = ws.get("records", []) or []
                payload["workareas"][str(idx)] = {
                    "dbf_path": ws.get("dbf_path", ""),
                    "indexes": list(ws.get("indexes", []) or []),
                    "pointer": int(ws.get("pointer", 1) or 1),
                    "eof": bool(ws.get("eof", True)),
                    "record_count": len(recs),
                    "deleted_count": sum(1 for r in recs if r.get("__deleted__")),
                }
            self._workarea_state_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            self._mark_hidden_path(self._workarea_state_path)
        except Exception:
            pass

    def _current_workarea(self) -> dict[str, object]:
        if not hasattr(self, "_workareas") or not hasattr(self, "_selected_workarea"):
            self._init_workareas()
        idx = int(getattr(self, "_selected_workarea", 0) or 0)
        if idx < 0 or idx > 64:
            idx = 0
            self._selected_workarea = 0
        if idx not in self._workareas:
            self._workareas[idx] = self._workarea_empty()
        return self._workareas[idx]

    def _resolve_db_path(self, filename: str = "", default_ext: str = ".dbf") -> Path:
        name = self._decode_builtin_text_arg(filename, "").strip()
        if not name:
            return Path("")
        p = Path(name)
        if not p.suffix and default_ext:
            p = Path(str(p) + default_ext)
        if not p.is_absolute():
            cur = getattr(self, "_current_filename", "") or ""
            base_dir = Path(cur).resolve().parent if cur else Path.cwd()
            p = base_dir / p
        return Path(os.path.abspath(str(p)))

    def _resolve_index_paths(self, index_text: str = "", dbf_path: Path | None = None) -> list[str]:
        raw = self._decode_builtin_text_arg(index_text, "").strip()
        if not raw:
            return []
        base_dir = dbf_path.parent if isinstance(dbf_path, Path) and str(dbf_path) else (Path(getattr(self, "_current_filename", "")).resolve().parent if getattr(self, "_current_filename", "") else Path.cwd())
        parts = [p.strip() for p in self._split_args(raw) if p.strip()]
        resolved = []
        for part in parts:
            val = self._decode_builtin_text_arg(part, part).strip()
            if not val:
                continue
            p = Path(val)
            if not p.suffix:
                p = Path(str(p) + ".ndx")
            if not p.is_absolute():
                p = base_dir / p
            resolved.append(str(Path(os.path.abspath(str(p)))))
        return resolved

    def _dbf_read_header_runtime(self, path: str):
        with open(path, "rb") as f:
            hdr = f.read(32)
            if len(hdr) < 32:
                raise ValueError("DBF header too short")
            version = hdr[0]
            num_records = int.from_bytes(hdr[4:8], "little")
            header_len = int.from_bytes(hdr[8:10], "little")
            record_len = int.from_bytes(hdr[10:12], "little")

            f.seek(32)
            desc = f.read(max(0, header_len - 32))
            end = desc.find(b"\x0D")
            if end == -1:
                end = len(desc)
            desc = desc[:end]

            def _parse_standard_32(desc_bytes: bytes):
                parsed: list[DbfFieldSpec] = []
                offset = 1
                for i in range(0, len(desc_bytes), 32):
                    ch = desc_bytes[i:i+32]
                    if len(ch) < 32:
                        break
                    name_raw = ch[0:11].split(b"\x00", 1)[0]
                    name = name_raw.decode("ascii", errors="ignore").strip()
                    if not name:
                        continue
                    ftype = chr(ch[11]).upper()
                    flen = int(ch[16])
                    fdec = int(ch[17])
                    parsed.append(DbfFieldSpec(name=name, ftype=ftype, length=flen, decimals=fdec, offset=offset))
                    offset += flen
                return parsed

            def _parse_extended_48(desc_bytes: bytes):
                # Fallback für zuvor erzeugte DBF-Dateien mit 48-Byte-Deskriptoren
                # (32 Byte Feldname, Typ an Offset 32, Länge an 33, Dezimalen an 34).
                parsed: list[DbfFieldSpec] = []
                offset = 1
                for i in range(0, len(desc_bytes), 48):
                    ch = desc_bytes[i:i+48]
                    if len(ch) < 35:
                        break
                    name_raw = ch[0:32].split(b"\x00", 1)[0]
                    name = name_raw.decode("ascii", errors="ignore").strip()
                    if not name:
                        continue
                    try:
                        ftype = chr(ch[32]).upper()
                    except Exception:
                        continue
                    flen = int(ch[33]) if len(ch) > 33 else 0
                    fdec = int(ch[34]) if len(ch) > 34 else 0
                    if flen <= 0:
                        continue
                    parsed.append(DbfFieldSpec(name=name, ftype=ftype, length=flen, decimals=fdec, offset=offset))
                    offset += flen
                return parsed

            fields: list[DbfFieldSpec] = _parse_standard_32(desc)
            if not fields:
                fields = _parse_extended_48(desc)
            return version, header_len, record_len, num_records, fields

    def _dbf_decode_field_runtime(self, spec: DbfFieldSpec, raw: bytes):
        s = raw.decode("cp1252", errors="ignore")
        if spec.ftype in ("C", "M"):
            return s.rstrip()
        if spec.ftype in ("N", "F", "I"):
            txt = s.strip()
            if not txt:
                return 0
            try:
                if spec.decimals:
                    return float(txt.replace(",", "."))
                return int(float(txt.replace(",", ".")))
            except Exception:
                return txt
        if spec.ftype == "L":
            v = s.strip().upper()
            return True if v in ("T", "Y", "1") else False
        if spec.ftype == "D":
            return s.strip()
        return s.rstrip()

    def _dbf_encode_field_runtime(self, spec: DbfFieldSpec, value) -> bytes:
        if spec.ftype in ("C", "M"):
            txt = str(value or "")
            b = txt.encode("cp1252", errors="replace")[:spec.length]
            return b.ljust(spec.length, b" ")
        if spec.ftype in ("N", "F", "I"):
            if value is None or value == "":
                txt = ""
            elif isinstance(value, float) and spec.decimals:
                txt = f"{value:.{spec.decimals}f}"
            else:
                txt = str(value).strip().replace(",", ".")
            b = txt.encode("ascii", errors="ignore")[:spec.length]
            return b.rjust(spec.length, b" ")
        if spec.ftype == "L":
            ch = b"T" if bool(value) else b"F"
            return ch.ljust(spec.length, b" ")
        if spec.ftype == "D":
            txt = str(value or "").strip()
            b = txt.encode("ascii", errors="ignore")[:spec.length]
            return b.ljust(spec.length, b" ")
        txt = str(value or "")
        b = txt.encode("cp1252", errors="replace")[:spec.length]
        return b.ljust(spec.length, b" ")

    def _load_dbf_workarea(self, path: Path) -> dict[str, object]:
        version, header_len, record_len, num_records, fields = self._dbf_read_header_runtime(str(path))
        records = []
        with open(path, "rb") as f:
            f.seek(header_len)
            for recno in range(1, num_records + 1):
                rec = f.read(record_len)
                if len(rec) < record_len:
                    break
                deleted = rec[:1] == b"*"
                row = {"__deleted__": bool(deleted), "__recno__": recno}
                for spec in fields:
                    raw = rec[spec.offset:spec.offset + spec.length]
                    row[spec.name.upper()] = self._dbf_decode_field_runtime(spec, raw)
                records.append(row)
        ws = self._workarea_empty()
        ws.update({
            "dbf_path": str(path),
            "indexes": [],
            "fields": fields,
            "records": records,
            "pointer": 1,
            "eof": len(records) == 0,
            "version": version or 0x03,
        })
        return ws

    def _save_dbf_workarea(self, ws: dict[str, object]) -> None:
        path = Path(ws.get("dbf_path", ""))
        fields: list[DbfFieldSpec] = list(ws.get("fields", []) or [])
        records = list(ws.get("records", []) or [])
        if not path:
            return
        nfields = len(fields)
        header_len = 32 + 32 * nfields + 1
        record_len = 1 + sum(f.length for f in fields)
        today = datetime.date.today()

        hdr = bytearray(32)
        hdr[0] = int(ws.get("version", 0x03) or 0x03)
        hdr[1] = today.year - 1900
        hdr[2] = today.month
        hdr[3] = today.day
        hdr[4:8] = int(len(records)).to_bytes(4, "little", signed=False)
        hdr[8:10] = int(header_len).to_bytes(2, "little", signed=False)
        hdr[10:12] = int(record_len).to_bytes(2, "little", signed=False)

        out = bytearray()
        out += hdr
        for spec in fields:
            desc = bytearray(32)
            nb = spec.name.encode("ascii", errors="ignore")[:11]
            desc[0:len(nb)] = nb
            desc[11] = ord(spec.ftype[:1])
            desc[16] = int(spec.length) & 0xFF
            desc[17] = int(spec.decimals) & 0xFF
            out += desc
        out += b"\x0D"

        for row in records:
            rec = bytearray()
            rec += b"*" if row.get("__deleted__") else b" "
            for spec in fields:
                rec += self._dbf_encode_field_runtime(spec, row.get(spec.name.upper()))
            out += rec

        out += b"\x1A"
        path.write_bytes(bytes(out))

    def _set_workarea_pointer(self, ws: dict[str, object], pointer: int) -> int:
        records = list(ws.get("records", []) or [])
        count = len(records)
        if count <= 0:
            ws["pointer"] = 1
            ws["eof"] = True
            return 1
        pointer = int(pointer or 1)
        if pointer < 1:
            pointer = 1
        if pointer > count:
            ws["pointer"] = count + 1
            ws["eof"] = True
            return ws["pointer"]
        ws["pointer"] = pointer
        ws["eof"] = False
        return pointer

    def _current_record(self) -> dict[str, object] | None:
        ws = self._current_workarea()
        records = list(ws.get("records", []) or [])
        ptr = int(ws.get("pointer", 1) or 1)
        if ptr < 1 or ptr > len(records):
            return None
        return records[ptr - 1]

    def _confirm_runtime_action(self, title: str, text: str) -> None:
        if not _RUNTIME_CONFIRM_ENABLED:
            return
        parent = MAINAPP if 'MAINAPP' in globals() else None
        answer = QMessageBox.question(
            parent,
            title,
            text,
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
        if answer != QMessageBox.Ok:
            raise ProgramAbortSignal()

    def _record_visible_for_runtime(self, rec: dict[str, object] | None) -> bool:
        if rec is None:
            return False
        if _RUNTIME_DELETE_ENABLED and bool(rec.get('__deleted__')):
            return False
        return True

    def _count_records_runtime(self, range_part: str = '', mode: str = '', cond_expr: str = '') -> int:
        ws = self._current_workarea()
        records = list(ws.get('records', []) or [])
        old_ptr = int(ws.get('pointer', 1) or 1)
        old_eof = bool(ws.get('eof', True))
        total = 0

        # Bereich derzeit reserviert; standardmäßig werden alle Datensätze geprüft.
        start_idx = 1
        end_idx = len(records)

        mode_up = (mode or '').strip().upper()
        cond_expr = (cond_expr or '').strip()

        try:
            for recno in range(start_idx, end_idx + 1):
                self._set_workarea_pointer(ws, recno)
                rec = self._current_record()
                if rec is None:
                    break

                visible = self._record_visible_for_runtime(rec)
                cond_ok = True
                if cond_expr:
                    cond_ok = bool(self._eval_expr_text_from_source(cond_expr))

                if mode_up == 'WHILE':
                    if not cond_ok:
                        break
                    if visible:
                        total += 1
                elif mode_up == 'FOR':
                    if visible and cond_ok:
                        total += 1
                else:
                    if visible:
                        total += 1
        finally:
            ws['pointer'] = old_ptr
            ws['eof'] = old_eof

        return total

    def _builtin_SELECT(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        area = 0
        if args:
            try:
                area = int(float(args[0]))
            except Exception:
                area = 0
        if area < 0 or area > 64:
            parent = MAINAPP if 'MAINAPP' in globals() else None
            try:
                QMessageBox.warning(parent, 'Arbeitsbereich', 'Arbeitsbereich außerhalb des gültigen Bereichs 0..64. Es wird auf Arbeitsbereich 0 gewechselt.')
            except Exception:
                pass
            area = 0
        self._selected_workarea = area
        self._sync_workareas_state()
        return area

    def _builtin_RENAME(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        if len(args) < 2:
            raise RuntimeError('RENAME erwartet alten und neuen Dateinamen')
        old_path = self._resolve_db_path(args[0], '.dbf')
        new_name_raw = self._decode_builtin_text_arg(args[1], '').strip()
        if not old_path or not str(old_path):
            raise RuntimeError('RENAME: alter Dateiname fehlt')
        if not old_path.exists():
            raise RuntimeError(f'RENAME: Datei wurde nicht gefunden: {old_path}')
        if not new_name_raw:
            raise RuntimeError('RENAME: neuer Dateiname fehlt')
        new_path = Path(new_name_raw)
        if not new_path.suffix:
            new_path = Path(str(new_path) + (old_path.suffix or '.dbf'))
        if not new_path.is_absolute():
            new_path = old_path.parent / new_path

        self._confirm_runtime_action('Datei umbenennen?', f'Soll die Datei umbenannt werden?\n\n{old_path}\n→\n{new_path}')
        os.replace(str(old_path), str(new_path))

        old_abs = str(old_path.resolve())
        new_abs = str(new_path.resolve())
        for idx, ws in self._workareas.items():
            if ws.get('dbf_path', '') and str(Path(ws['dbf_path']).resolve()) == old_abs:
                reloaded = self._load_dbf_workarea(Path(new_abs))
                reloaded['indexes'] = list(ws.get('indexes', []) or [])
                self._set_workarea_pointer(reloaded, 1)
                self._workareas[idx] = reloaded

        self._sync_workareas_state()
        return 1

    def _builtin_CLEAR_ALL(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        self._clear_memory_variables()
        self._init_workareas()
        return 1

    def _builtin_SKIP(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        count = 1
        if args:
            try:
                count = int(float(args[0]))
            except Exception:
                count = 1
        ws = self._current_workarea()
        self._set_workarea_pointer(ws, int(ws.get('pointer', 1) or 1) + count)
        self._sync_workareas_state()
        return int(ws.get('pointer', 1) or 1)

    def _builtin_GOTO(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        ws = self._current_workarea()
        records = list(ws.get('records', []) or [])
        count = len(records)
        target = args[0] if args else 'TOP'
        if isinstance(target, str):
            up = target.strip().upper()
            if up == 'TOP':
                self._set_workarea_pointer(ws, 1)
                self._sync_workareas_state()
                return 1
            if up == 'BOTTOM':
                self._set_workarea_pointer(ws, count if count > 0 else 1)
                self._sync_workareas_state()
                return int(ws.get('pointer', 1) or 1)
        try:
            recno = int(float(target))
        except Exception:
            recno = 1

        if recno < 1 or recno > max(1, count):
            parent = MAINAPP if 'MAINAPP' in globals() else None
            try:
                QMessageBox.warning(parent, 'Datensatzzeiger', 'Ungültige Datensatznummer. Es wird auf Datensatz 1 gewechselt.')
            except Exception:
                pass
            recno = 1
        self._set_workarea_pointer(ws, recno)
        self._sync_workareas_state()
        return int(ws.get('pointer', 1) or 1)

    def _builtin_DELETE_RECORD(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        ws = self._current_workarea()
        rec = self._current_record()
        if rec is None:
            return 0
        rec['__deleted__'] = True
        self._save_dbf_workarea(ws)
        self._sync_workareas_state()
        return 1

    def _builtin_PACK(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        ws = self._current_workarea()
        if not ws.get('dbf_path'):
            return 0
        self._confirm_runtime_action('PACK', 'Sollen die löschmarkierten Datensätze endgültig entfernt werden?')
        records = [r for r in list(ws.get('records', []) or []) if not r.get('__deleted__')]
        ws['records'] = records
        self._save_dbf_workarea(ws)
        self._set_workarea_pointer(ws, 1)
        self._sync_workareas_state()
        return len(records)

    def _builtin_ZAP(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        ws = self._current_workarea()
        if not ws.get('dbf_path'):
            return 0
        self._confirm_runtime_action('ZAP', 'Sollen alle Datensätze endgültig gelöscht werden?')
        ws['records'] = []
        self._save_dbf_workarea(ws)
        self._set_workarea_pointer(ws, 1)
        self._sync_workareas_state()
        return 0

    def _builtin_STORE(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        if len(args) < 2:
            raise RuntimeError('STORE erwartet einen Ausdruck und eine Zielvariable')
        value = args[0]
        target_name = self._decode_builtin_text_arg(args[1], '').strip()
        if not target_name:
            raise RuntimeError('STORE: Zielvariable fehlt')
        self._assign_input_target(target_name, value)
        return value

    def _builtin_SAVE(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        filename = args[0] if len(args) > 0 else ''
        mode = self._decode_builtin_text_arg(args[1] if len(args) > 1 else 'ALL', 'ALL').upper()
        mask = self._decode_builtin_text_arg(args[2] if len(args) > 2 else '', '')
        drive = args[3] if len(args) > 3 else ''

        path = self._resolve_memfile_path(filename, drive)
        selected = self._select_memory_vars(mode, mask)
        payload_vars = {key: self._jsonify_mem_value(value, key) for key, value in selected.items()}

        path.parent.mkdir(parents=True, exist_ok=True)
        self._confirm_memfile_overwrite(path)
        payload = {
            'format': 'dbase.mem.json',
            'saved_at': datetime.datetime.now().isoformat(timespec='seconds'),
            'variables': payload_vars,
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
        return 1

    def _builtin_RESTORE(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        filename = args[0] if len(args) > 0 else ''
        additive = bool(args[1]) if len(args) > 1 else False
        drive = args[2] if len(args) > 2 else ''
        path = self._resolve_memfile_path(filename, drive)
        if not path.exists():
            raise RuntimeError(f'RESTORE: Datei wurde nicht gefunden: {path}')

        data = json.loads(path.read_text(encoding='utf-8'))
        if isinstance(data, dict) and isinstance(data.get('variables'), dict):
            variables = data['variables']
        elif isinstance(data, dict):
            variables = data
        else:
            raise RuntimeError('RESTORE: ungültiges Speicherformat')

        if not additive:
            self._clear_memory_variables()

        for key, value in variables.items():
            self._set_name(str(key), value, None)
        return len(variables)

    def _builtin_RELEASE(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        names_text = self._decode_builtin_text_arg(args[0] if len(args) > 0 else '', '')
        mode = self._decode_builtin_text_arg(args[1] if len(args) > 1 else 'LIST', 'LIST').upper()
        mask = self._decode_builtin_text_arg(args[2] if len(args) > 2 else '', '')

        if mode == 'ALL':
            self._clear_memory_variables()
            return 0
        if mode in ('LIKE', 'EXCEPT'):
            selected = self._select_memory_vars(mode, mask)
            for key in list(selected.keys()):
                self._delete_memory_variable(key)
            return len(selected)

        names = [part.strip() for part in names_text.split(',') if part.strip()]
        for name in names:
            self._delete_memory_variable(name)
        return len(names)

    def _builtin_USE(self, *args):
        """
        USE <table> [INDEX idx1, idx2, ...]
        Ohne Parameter wird der aktive Arbeitsbereich geschlossen.
        """
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0

        filename = args[0] if len(args) > 0 else ''
        index_text = args[1] if len(args) > 1 else ''
        _exclusive = bool(args[2]) if len(args) > 2 else False

        raw_name = self._decode_builtin_text_arg(filename, '').strip()
        ws = self._current_workarea()

        if not raw_name:
            self._workareas[self._selected_workarea] = self._workarea_empty()
            self._sync_workareas_state()
            return 0

        path = self._resolve_db_path(raw_name, '.dbf')
        if not path.exists():
            raise RuntimeError(f"USE: Datei wurde nicht gefunden: {path}")

        loaded = self._load_dbf_workarea(path)
        loaded['indexes'] = self._resolve_index_paths(index_text, path)
        self._set_workarea_pointer(loaded, 1)
        self._workareas[self._selected_workarea] = loaded
        self._sync_workareas_state()
        return 1
        
    @property
    def current_frame(self) -> Frame:
        return self.frames[-1]
    
    @property
    def current_with_base(self):
        return self.with_stack[-1] if self.with_stack else None

    def push_frame(self, name: str, args: list[Any] | None = None) -> None:
        self.frames.append(Frame(name=name, args=list(args or [])))

    def pop_frame(self) -> Frame:
        if len(self.frames) <= 1:
            raise RuntimeError("Cannot pop global frame")
        return self.frames.pop()
    
    def push_this(self, inst: Instance):
        self.this_stack.append(inst)

    def pop_this(self):
        self.this_stack.pop()

    def cur_this(self) -> Instance:
        if not self.this_stack:
            raise RuntimeError("THIS ist nicht gesetzt")
        return self.this_stack[-1]

    
    def _acquire_dbf_exclusive_lock(self, dbf_path: str) -> None:
        lock_path = dbf_path + ".lck"
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w", encoding="utf-8", errors="ignore") as f:
                f.write(str(os.getpid()))
        except FileExistsError:
            raise RuntimeError(f"DBF ist bereits exklusiv gesperrt: {dbf_path}")
        self._dbf_exclusive_locks[dbf_path] = lock_path
    
    # ----------------- MENU / POPUPMENU helpers -----------------
    def _detach_menu(self, inst: Instance) -> None:
        """Entfernt ein bereits angehängtes Menü aus MenuBar oder Parent-Menu (wenn möglich)."""
        try:
            container = inst.props.get("_QT_MENU_CONTAINER")  # QMenuBar oder QMenu
            action = inst.props.get("_QT_MENU_ACTION")        # QAction
            if container is not None and action is not None and hasattr(container, "removeAction"):
                container.removeAction(action)
        except Exception:
            pass
        inst.props["_QT_MENU_CONTAINER"] = None
        inst.props["_QT_MENU_ACTION"] = None

    def _attach_menu(self, inst: Instance, parent_inst: Any) -> None:
        """Hängt MENU/POPUPMENU an parent_inst (MENU => Submenu; MainWindow => Menübar)."""
        if inst is None or inst.backend is None:
            return
        if inst.class_name.upper() not in ("MENU", "POPUPMENU"):
            return

        self._detach_menu(inst)

        # Parent kann None sein (dann nur "lose" QMenu-Instanz)
        if not isinstance(parent_inst, Instance) or parent_inst.backend is None:
            return

        pb = parent_inst.backend

        # 1) Parent ist MENU/POPUPMENU => submenu
        if parent_inst.class_name.upper() in ("MENU", "POPUPMENU") and hasattr(pb, "addMenu"):
            act = pb.addMenu(inst.backend)  # returns QAction
            inst.props["_QT_MENU_CONTAINER"] = pb
            inst.props["_QT_MENU_ACTION"] = act
            inst.parent = parent_inst
            return

        # 2) Parent ist ein Qt-MainWindow (oder kompatibel) => MenuBar
        if hasattr(pb, "menuBar"):
            mb = pb.menuBar()
            if mb is not None and hasattr(mb, "addMenu"):
                act = mb.addMenu(inst.backend)  # returns QAction
                inst.props["_QT_MENU_CONTAINER"] = mb
                inst.props["_QT_MENU_ACTION"] = act
                inst.parent = parent_inst
                return

        # 3) Fallback: wenn Parent selbst eine MenuBar ist
        if hasattr(pb, "addMenu"):
            act = pb.addMenu(inst.backend)
            inst.props["_QT_MENU_CONTAINER"] = pb
            inst.props["_QT_MENU_ACTION"] = act
            inst.parent = parent_inst
            return

    def reparent_instance(self, child: Instance, new_parent: Optional[Instance]) -> None:
        """Re-parent a runtime instance (and its Qt backend) to a new parent instance.

        This makes `child.parent`, `child.parent.parent`, ... work and also updates Qt parenting,
        so property updates (like this.parent.text=...) hit the correct widget tree.
        """
        old_parent = child.parent
        if old_parent is new_parent:
            return

        # 1) detach from old parent's child map (best-effort)
        if old_parent is not None:
            try:
                # remove any aliases pointing to this child
                for k, v in list(old_parent.children.items()):
                    if v is child:
                        old_parent.children.pop(k, None)
                for k, v in list(old_parent.props.items()):
                    if v is child:
                        old_parent.props.pop(k, None)
            except Exception:
                pass

        # 2) update runtime parent
        child.parent = new_parent

        # 3) update Qt backend parent (best-effort; not every backend supports parenting)
        try:
            cb = getattr(child, "backend", None)
            pb = getattr(new_parent, "backend", None) if new_parent is not None else None
            if cb is not None and hasattr(cb, "setParent"):
                cb.setParent(pb)
        except Exception:
            # ignore backend parenting issues; runtime parenting still works
            pass

    def bind_child(self, owner: Instance, name: str, child: Instance):
        key = name.upper()
        
        # wenn Parent eine Font hat und Kind noch nicht: übernehmen
        if "FONT" in owner.props and "FONT" not in child.props:
            self.set_prop(child, "FONT", owner.props["FONT"], None)
            

        # runtime parenting + Qt parenting
        self.reparent_instance(child, owner)

        owner.children[key] = child
        owner.props[key] = child   # THIS.PushButton1 soll wie Property funktionieren

    def assign_name(self, name: str, value: Any):
        target = self.cur_with_target() or self.cur_this()
        set_prop_runtime(target, name, value)
    
    def cur_with_target(self) -> Optional[Instance]:
        return self.with_stack[-1] if self.with_stack else None
        
    def resolve_dotted(self, parts: list[str], ctx):
        if not parts:
            return None

        if parts[0].upper() == "THIS":
            obj = self.get_var("THIS", ctx)
        else:
            obj = self.get_var(parts[0], ctx)

        for member in parts[1:]:
            obj = self.get_member(obj, member, ctx)

        return obj
    
    def _need_value(self, v, ctx, what="Ausdruck"):
        if v is None:
            raise Exception(f"{ctx.start.line}:{ctx.start.column}: {what} ist None")
        return v

    def visitAdditiveExpr(self, ctx):
        # multiplicativeExpr ( (PLUS|MINUS) multiplicativeExpr )*
        res = self._need_value(self.visit(ctx.multiplicativeExpr(0)), ctx, "additiveExpr")
        n = len(ctx.multiplicativeExpr())
        for i in range(1, n):
            op = ctx.getChild(2*i - 1).getText()          # '+' oder '-'
            rhs = self._need_value(self.visit(ctx.multiplicativeExpr(i)), ctx, "additiveExpr rhs")
            if op == '+':
                res = res + rhs
            else:
                res = res - rhs
        return res

    def visitMultiplicativeExpr(self, ctx):
        # postfixExpr ( (STAR|SLASH) postfixExpr )*
        res = self._need_value(self.visit(ctx.postfixExpr(0)), ctx, "multiplicativeExpr")
        n = len(ctx.postfixExpr())
        for i in range(1, n):
            op = ctx.getChild(2*i - 1).getText()          # '*' oder '/'
            rhs = self._need_value(self.visit(ctx.postfixExpr(i)), ctx, "multiplicativeExpr rhs")
            if op == '*':
                res = res * rhs
            else:
                res = res / rhs
        return res

    def visitComparison(self, ctx):
        left = self._need_value(self.visit(ctx.additiveExpr(0)), ctx, "comparison left")
        if ctx.additiveExpr(1) is None:
            return left

        right = self._need_value(self.visit(ctx.additiveExpr(1)), ctx, "comparison right")
        op = ctx.compareOp().getText()

        if op == "<":  return left < right
        if op == "<=": return left <= right
        if op == ">":  return left > right
        if op == ">=": return left >= right
        if op == "==": return left == right
        if op == "!=": return left != right
        raise Exception(f"{ctx.start.line}:{ctx.start.column}: unbekannter Vergleichs-Operator {op}")

    def visitLogicalNot(self, ctx):
        # NOT logicalNot | comparison
        if ctx.NOT():
            return not bool(self._need_value(self.visit(ctx.logicalNot()), ctx, "logicalNot"))
        return self.visit(ctx.comparison())

    def visitLogicalAnd(self, ctx):
        result = self.visit(ctx.logicalNot(0))
        for i in range(1, len(ctx.logicalNot())):
            if not bool(result):      # short-circuit
                return result         # <-- NICHT False
            result = self.visit(ctx.logicalNot(i))
        return result

    def visitLogicalOr(self, ctx):
        result = self.visit(ctx.logicalAnd(0))
        for i in range(1, len(ctx.logicalAnd())):
            if bool(result):          # short-circuit
                return result         # <-- NICHT True
            result = self.visit(ctx.logicalAnd(i))
        return result

    def visitBreakStmt(self, ctx):
        raise BreakSignal()
    
    def visitExpr(self, ctx):
        # expr : logicalOr ;
        return self.visit(ctx.logicalOr())
    
    def visitWithBody(self, ctx):
        for ch in (ctx.children or []):
            if isinstance(ch, ParserRuleContext):
                self.visit(ch)
        return None
    
    def visitWithAssignStmt(self, ctx):
        value = self.visit(ctx.expr())
        parts = [t.getText() for t in ctx.withLvalue().IDENT()]

        target = self.with_stack[-1]
        owner  = self.with_stack_owner[-1]  # None oder Instance (z.B. Sender)

        # 1) Einfach: bold = .T.   oder   Text = "x"
        if len(parts) == 1:
            name = parts[0]

            if isinstance(target, Instance):
                self.set_prop(target, name.upper(), value, ctx)
                return None

            # z.B. WITH(Font) bold = .T.
            self.set_member(target, name, value, ctx)

            # wenn WITH(Font): neu anwenden
            if owner is not None and isinstance(target, FontValue):
                self.set_prop(owner, "FONT", target, ctx)

            return None

        # 2) Kette: Font.bold = .T.   innerhalb WITH(Sender)
        cur = target
        for seg in parts[:-1]:
            cur = self.get_member(cur, seg, ctx)

        self.set_member(cur, parts[-1], value, ctx)

        # wenn innerhalb WITH(Sender): Font.* geändert -> auf Sender neu setzen
        if isinstance(target, Instance) and parts and parts[0].upper() == "FONT":
            fv = target.props.get("FONT")
            if isinstance(fv, FontValue):
                self.set_prop(target, "FONT", fv, ctx)

        # wenn wir in WITH(Font) sind: owner neu setzen
        if owner is not None and isinstance(target, FontValue):
            self.set_prop(owner, "FONT", target, ctx)

        return None

    def set_property(self, obj, prop_name: str, value, ctx=None):
        key = prop_name.upper()

        # Wenn obj ein Qt-Widget ist:
        if hasattr(obj, "setFont") and key == "FONT":
            if isinstance(value, QFont):
                obj.setFont(value)
                return value
                
    def set_property_path(self, base_obj, path, value, ctx):
        obj = base
        for seg in path[:-1]:
            obj = self.get_member(obj, seg, ctx)

        last = path[-1]

        # Wir brauchen den "container" des letzten Members:
        container = base
        for seg in path[:-2]:
            container = self.get_member(container, seg, ctx)
            
        # obj ist jetzt das Zielobjekt (z.B. QFont), last ist "bold"
        self.set_member(obj, last, value, ctx)
        
        # -----------------------------------------
        # Wenn wir gerade Font.* geändert haben,
        # Font erneut ans Widget binden
        # -----------------------------------------
        if len(path) >= 2 and path[-2].upper() == "FONT":
            # -----------------------------------------------------
            # container ist dann das Objekt, das die Font-Property
            # besitzt falls das ein Qt-Widget ist:
            # -----------------------------------------------------
            qt_obj = getattr(container, "qt_obj", None)
            if qt_obj is not None and hasattr(qt_obj, "setFont"):
                qt_obj.setFont(obj)
            elif hasattr(container, "setFont"):
                container.setFont(obj)
                
        return value
        
    def push_scope(self):
        if not hasattr(self, "_scopes"):
            self._scopes = []
        self._scopes.append({})

    def pop_scope(self):
        self._scopes.pop()
    
    def visitStatement(self, ctx):
        if self._mode == "collect":
            # im Sammelpass Statements ignorieren
            return None

        # classDecl darf im Exec-Pass nie als normales Statement herunterlaufen.
        # In der Grammar ist classDecl sowohl als item als auch als statement erlaubt.
        # Falls der Parse-Tree hier dennoch eine Klassendeklaration liefert,
        # würden sonst Header-Tokens wie "ParentForm" als exprStmt/memberExpr
        # fehlinterpretiert werden.
        try:
            if hasattr(ctx, "classDecl") and ctx.classDecl() is not None:
                return None
        except Exception:
            pass

        return self.visitChildren(ctx)
    
    def ctx_text_token(ctx, token_name: str) -> str | None:
        fn = getattr(ctx, token_name, None)
        if callable(fn):
            t = fn()
            return t.getText() if t else None
        return None
        
    def eval_expr(self, ctx):
        text = ctx.getText()
        
        if getattr(ctx, "BRACKET_STRING", None) and ctx.BRACKET_STRING():
            tok = ctx.BRACKET_STRING().getSymbol()
            return self._unescape_bracket_string(tok.text)
            
        if self.is_simple_reference(text):
            return self.eval_reference_text(text)
        # Fallback: normale Expr-Auswertung über Visitor
        return self.visit(ctx)
    
    def is_simple_reference(self, s: str) -> bool:
        # erlaubt: X, this.width, a.b.c
        # (ohne Klammern/Operatoren)
        import re
        return re.fullmatch(r'(this|[A-Za-z_]\w*)(\.[A-Za-z_]\w*)*', s, re.IGNORECASE) is not None

    def eval_reference_text(self, s: str):
        parts = s.split('.')
        head = parts[0].upper()

        if head == "this":
            obj = self.this_object
            idx = 1
        else:
            obj = self._get_name(parts[0])
            idx = 1

        for name in parts[idx:]:
            obj = self.get_member(obj, name)
        return obj
        
    def visitBooleanLiteral(self, ctx):
        if ctx.TRUE():
            return True
        return False
        
    def eval_primary(self, ctx):
        if ctx.getText().upper() == "THIS":
            return self.this_object
        if ctx.NUMBER():
            return float(ctx.NUMBER().getText())
        if ctx.STRING():
            return self._unquote(ctx.STRING().getText())
        if ctx.identifier():
            name = ctx.identifier().getText()
            return self._get_name(name)   # <-- HIER
        if ctx.TRUE():
            return True
        if ctx.FALSE():
            return False
        if ctx.expr():
            return self.visit(ctx.expr())
            
        raise NotImplementedError(type(ctx).__name__)
    
    def has_method(self, obj, name: str) -> bool:
        # an dein Objektmodell anpassen:
        try:
            return name.upper() in obj.klass.methods
        except Exception:
            return False

    def resolve_method(self, start_class: str, method_name: str, ctx):
        c = start_class.upper()
        m = method_name.upper()

        while c is not None:
            self._ensure_class_methods_loaded(c)
            cdef = self.classes.get(c)
            if cdef is None:
                raise Exception(f"{ctx.start.line}:{ctx.start.column}: Klasse '{c}' ist nicht definiert")

            # ClassDef statt dict
            if m in cdef.methods:
                return c, cdef.methods[m]

            found = self._find_method_decl_in_tree(c, m)
            if found is None:
                found = self._find_method_decl_in_source(c, m)
            if found is not None:
                cdef.methods[m] = found
                self.classes[c] = cdef
                return c, found

            c = cdef.parent.upper() if cdef.parent else None

        raise Exception(f"{ctx.start.line}:{ctx.start.column}: Methode '{m}' nicht gefunden (ab '{start_class}')")


    def resolve_method_silent(self, class_name: str, method_name: str):
        c = class_name.upper() if class_name else None
        m = method_name.upper()

        while c:
            self._ensure_class_methods_loaded(c)
            cdef = self.classes.get(c)
            if cdef is None:
                return None

            methods = getattr(cdef, "methods", {}) or {}
            if m in methods:
                return methods[m]

            found = self._find_method_decl_in_tree(c, m)
            if found is None:
                found = self._find_method_decl_in_source(c, m)
            if found is not None:
                cdef.methods[m] = found
                self.classes[c] = cdef
                return found

            c = cdef.parent.upper() if cdef.parent else None

        return None

    def in_local_scope(self) -> bool:
        return bool(self._scopes)

    def visitLocalDeclStmt(self, ctx):
        var_name = ctx.name.text  # IDENT token text
        # Deklaration ohne Wert -> None
        self.set_var(var_name, None)
        return None
        
    def visitLocalAssignStmt(self, ctx):
        var_name = ctx.name.text
        value = self.visit(ctx.expr())
        self.set_var(var_name, value)
        return value
    
    def _resolve_root(self, name: str, ctx):
        n = name.upper()
        if n == "THIS":
            # ist THIS irgendwo gesetzt?
            try:
                return self.get_var("THIS", ctx)
            except Exception:
                raise Exception(f"{ctx.start.line}:{ctx.start.column}: 'this' ist nur innerhalb einer Instanzmethode gültig")
        return self.get_var(n, ctx)

    def loc(self, ctx):
        if ctx is not None and hasattr(ctx, "start") and ctx.start is not None:
            return f"{ctx.start.line}:{ctx.start.column}"
        return "<unknown>"

    def _normalize_handlers(self, value, ctx, event_name: str):
        # erlaubt: einzelner Delegate oder Liste/Tuple davon
        if value is None:
            return []
        if isinstance(value, (list, tuple)):
            handlers = list(value)
        else:
            handlers = [value]

        out = []
        for h in handlers:
            if not isinstance(h, Delegate):
                raise RuntimeError(
                    f"{self.loc(ctx)}: {event_name} erwartet Methode(n) (Delegate), bekam {type(h).__name__}"
                )
            out.append(h)
        return out

    def _bind_event(self, inst, prop_key: str, value, ctx=None):
        key = prop_key.upper()

        # welche Events gibt's?
        # (pass_event = ob Qt-event als 2s-Arg an Handler geht)
        EVENT_MAP = {
            "ONCLICK"       : ("_ONCLICK_WRAPPER",     "_ONCLICK_HANDLERS",     False),
            "ONDBLCLICK"    : ("_ONDBLCLICK_WRAPPER",  "_ONDBLCLICK_HANDLERS",  False),
            
            "ONMOUSEDOWN"   : ("_ONMOUSEDOWN_WRAPPER", "_ONMOUSEDOWN_HANDLERS", True),
            "ONMOUSEUP"     : ("_ONMOUSEUP_WRAPPER",   "_ONMOUSEUP_HANDLERS",   True),
            "ONMOUSEMOVE"   : ("_ONMOUSEMOVE_WRAPPER", "_ONMOUSEMOVE_HANDLERS", True),
            
            "ONMOUSELBUTTON": ("_ONMOUSELBUTTON_WRAPPER", "_ONMOUSELBUTTON_HANDLERS", True),
            "ONMOUSERBUTTON": ("_ONMOUSERBUTTON_WRAPPER", "_ONMOUSERBUTTON_HANDLERS", True),

            "ONKEYDOWN"     : ("_ONKEYDOWN_WRAPPER", "_ONKEYDOWN_HANDLERS", True),
            "ONKEYUP"       : ("_ONKEYUP_WRAPPER",   "_ONKEYUP_HANDLERS",   True),
        }

        if key not in EVENT_MAP:
            return False

        wrapper_prop, handlers_prop, pass_event = EVENT_MAP[key]
        handlers = self._normalize_handlers(value, ctx, key)

        # "löschen" erlauben: onX = NIL -> entfernt Handler
        if not handlers:
            inst.props.pop(wrapper_prop, None)
            inst.props.pop(handlers_prop, None)

            # bei Click auch Signal trennen
            if key == "ONCLICK" and hasattr(inst.backend, "clicked"):
                old = inst.props.get("_ONCLICK_WRAPPER")
                if old is not None:
                    try:
                        inst.backend.clicked.disconnect(old)
                    except Exception:
                        pass
            return True

        wrapper = self._make_multi_wrapper(inst, handlers, pass_event)
        inst.props[wrapper_prop] = wrapper
        inst.props[handlers_prop] = handlers

        # Click: lieber Qt-Signal (wie du’s schon hast)
        if key == "ONCLICK" and hasattr(inst.backend, "clicked"):
            old = inst.props.get("_ONCLICK_WRAPPER")
            if old is not None:
                try:
                    inst.backend.clicked.disconnect(old)
                except Exception:
                    pass

            inst.props["_ONCLICK_VIA_SIGNAL"] = True
            inst.backend.clicked.connect(wrapper)
            return True

        # Rest: EventFilter sicherstellen
        self._ensure_event_filter(inst, ctx)
        return True

    def _make_multi_wrapper(self, inst, handlers, pass_event: bool):
        def wrapper(ev=None):
            for h in handlers:
                try:
                    # dBase-Semantik: Sender ist inst
                    args = [inst]
                    if pass_event:
                        args.append(ev)
                    self.invoke_method(h.target, h.method_name, args, None)
                except (ReturnSignal, ProgramAbortSignal):
                    # RETURN in Handler -> nur diesen Handler beenden, nächste weiter
                    continue
            return None
        return wrapper
    
    def get_member(self, obj, prop: str, ctx=None):
        key = prop.upper()
        
        # --- QFont support ---
        if isinstance(obj, FontValue):
            if key == "BOLD":
                return bool(obj.bold)
            if key == "ITALIC":
                return bool(obj.italic)
            if key == "UNDERLINE":
                return bool(obj.underline)
            if key == "NAME":
                return str(obj.family)
            if key == "SIZE":
                return int(obj.size)
            
        if isinstance(obj, Instance):
            # 0) Parent chain
            if key == "PARENT":
                return obj.parent

            # 1) zuerst direkt in props, dann robust in children
            if key in obj.props:
                return obj.props[key]
            if key in obj.children:
                child = obj.children[key]
                # props/cache nachziehen, damit zukünftige Lookups konsistent sind
                obj.props[key] = child
                return child
            
            if key == "FONT" and getattr(obj, "backend", None) is not None and hasattr(obj.backend, "font"):
                qf = obj.backend.font()  # QFont vom Widget
                fv = FontValue(
                    family      = qf.family(),
                    size        = qf.pointSize(),
                    bold        = qf.bold(),
                    italic      = qf.italic(),
                    underline   = qf.underline(),
                    obj         = qf,     # wichtig: gleicher QFont
                )
                obj.props["FONT"] = fv
                return fv



            # 1b) Fallback: Geometry-Eigenschaften direkt vom Backend lesen,
            #     falls sie nicht im props-Dict liegen (damit Ausdrücke wie THIS.WIDTH = THIS.WIDTH + 10 gehen).
            if key in ("LEFT", "TOP", "WIDTH", "HEIGHT"):
                b = getattr(obj, "backend", None)
                if b is not None:
                    try:
                        # In MDI-Kontext beziehen wir uns auf das QMdiSubWindow (falls vorhanden),
                        # weil LEFT/TOP dort die Position im MDI-Bereich bedeutet.
                        mdi = _find_mdi_subwindow(b)
                        gb = mdi.geometry() if mdi is not None else b.geometry()
                        if key == "LEFT":
                            return int(gb.x())
                        if key == "TOP":
                            return int(gb.y())
                        if key == "WIDTH":
                            return int(gb.width())
                        if key == "HEIGHT":
                            return int(gb.height())
                    except Exception:
                        pass
                # Default, wenn kein Backend vorhanden
                return int(obj.props.get(key, 0) or 0)

            # 1b) Fallback: gängige Text-Eigenschaften direkt vom Backend lesen,
            #     falls sie nicht im props-Dict liegen (z.B. initialer Fenstertitel/Button-Text).
            if key in ("TEXT", "CAPTION", "TITLE"):
                b = getattr(obj, "backend", None)
                if b is not None:
                    # Form/Dialog
                    if hasattr(b, "windowTitle") and callable(getattr(b, "windowTitle")):
                        try:
                            return b.windowTitle()
                        except Exception:
                            pass
                    # Buttons/Labels etc.
                    if hasattr(b, "text") and callable(getattr(b, "text")):
                        try:
                            return b.text()
                        except Exception:
                            pass
                # Kein Backend oder nicht lesbar
                return ""

            cls_name = getattr(obj, "class_name", None)

            # 2) DSL-Methode? -> als Delegate zurückgeben
            if cls_name:
                if self.resolve_method_silent(cls_name.upper(), key) is not None:
                    return Delegate(target=obj, method_name=key, runner=self)

            # ✅ 3) Native Methode: OPEN (für FORM und alles was davon erbt)
            if key == "OPEN" and cls_name and self.is_descendant_of(cls_name.upper(), "FORM"):
                return Delegate(target=obj, method_name="OPEN", runner=self)

            raise RuntimeError(f"{self.loc(ctx)}: Member '{prop}' in {cls_name} nicht gefunden")

    def set_member(self, obj, prop: str, value, ctx):
        key = prop.upper()
        
        # --- QFont support ---
        if isinstance(obj, FontValue):
            if key == "BOLD":
                obj.bold = bool(value)
                obj.obj.setBold(obj.bold)
                return value
            if key == "ITALIC":
                obj.italic = bool(value)
                obj.obj.setItalic(obj.italic)
                return value
            if key == "UNDERLINE":
                obj.underline = bool(value)
                obj.obj.setUnderline(obj.underline)
                return value
            if key == "NAME":
                obj.family = str(value)
                obj.obj.setFamily(obj.family)
                return value
            if key == "SIZE":
                obj.size = int(value)
                obj.obj.setPointSize(obj.size)
                return value

        if not isinstance(obj, Instance):
            raise RuntimeError(f"{self.loc(ctx)}: '{prop}' setzen auf Nicht-Objekt")
        
        # Hauptspeicher: props
        self.set_prop(obj, key, value, ctx)
        return value

    def class_chain_base_to_derived(self, class_name: str) -> list[str]:
        chain = []
        c = class_name.upper()
        while c:
            if c not in self.classes:
                break
            chain.append(c)
            parent = self.classes[c].parent
            c = parent.upper() if parent else None
        return list(reversed(chain))  # base zuerst
        
    def eval_member(self, obj, name: str, ctx):
        key = name.upper()

        # Nur Beispiel: anpassen an deine Instance-Struktur!
        if isinstance(obj, Instance):
            # 1) Field/Property?
            # falls du z.B. obj.fields als dict hast:
            if hasattr(obj, "props") and key in obj.props:
                return obj.props[key]

            # 2) Methode?
            res = self.resolve_method_silent(obj.class_name.upper(), key)
            if res is not None:
                # Delegate ist bei dir offenbar genau das, was CallExpr ausführen kann
                return Delegate(target=obj, method_name=key, runner=self)

            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Member '{name}' nicht gefunden")

        raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Memberzugriff auf Nicht-Objekt: {type(obj).__name__}")
    
    def call_delegate(self, d: Delegate, args: list, ctx):
        # d.target ist deine Instance, d.method_name z.B. "INIT"
        return self.invoke_method(d.target, d.method_name, args, ctx)
        
    def visitCallExpr(self, ctx):
        callee = self.visit(ctx.expr())  # oder ctx.callee o.ä.
        args = []
        if ctx.argList() is not None:
            args = [self.visit(a) for a in ctx.argList().expr()]

        # ✅ Delegate direkt ausführen
        if isinstance(callee, Delegate):
            return self.call_delegate(callee, args, ctx)

        # normale Python-callables
        if not callable(callee):
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Ausdruck ist nicht aufrufbar: {ctx.getText()}")

        return callee(*args)
    
    def try_get_var(self, name, ctx):
        try:
            return self.get_var(name, ctx)
        except Exception:
            return None
        
    def get_chain(self, parts: list[str], ctx):
        parts = [p.upper() for p in parts]
        
        # --- SUPER::Method(...) ---
        if parts and parts[0] == "SUPER":
            if len(parts) < 2:
                raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: SUPER ohne Methodenname")
            
            this_obj = self.get_var("THIS", ctx)          # THIS muss gesetzt sein
            if not isinstance(this_obj, Instance):
                raise RuntimeError(f"{self.loc(ctx)}: SUPER nur innerhalb einer Instanzmethode gültig")
            
            cur_class = this_obj.class_name.upper()
            cdef = self.classes.get(cur_class)
            parent = cdef.parent.upper() if (cdef and cdef.parent) else None
            
            if not parent:
                raise RuntimeError(f"{self.loc(ctx)}: SUPER nicht möglich (keine Parent-Klasse)")
            
            mname = parts[1].upper()
            
            # Existiert die Methode irgendwo im Parent-Chain?
            if self.resolve_method_silent(parent, mname) is None:
                raise RuntimeError(f"{self.loc(ctx)}: SUPER-Methode '{mname}' nicht gefunden ab '{parent}'")
            
            # Delegate zurückgeben -> visitPostfixExpr ruft das dann auf
            return Delegate(target=this_obj, method_name=mname, runner=self)

        head = parts[0].upper()
        if head == "THIS":
            # bevorzugt this_obj (sicher in Methoden), fallback auf Variable THIS
            cur = self.this_obj
            if cur is None:
                cur = self.get_var("THIS", ctx)
        else:
            cur = self.get_var(parts[0], ctx)

        if cur is None:
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{parts[0]}' ist None")
        
        prev_path = parts[0].upper()

        for name in parts[1:]:
            # Wenn ein Zwischenergebnis None ist (z.B. Parent nicht gesetzt), sauber abbrechen
            if cur is None:
                raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{prev_path}' ist None (z.B. Parent nicht gesetzt)")
            key = name.upper()
            prev_path = prev_path + "." + key


            if isinstance(cur, Instance):
                if hasattr(cur, "props") and key in cur.props:
                    cur = cur.props[key]
                    if cur is None and name != parts[-1]:
                        raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{prev_path}' ist None (z.B. Parent nicht gesetzt)")
                    continue

                if self.resolve_method_silent(cur.class_name.upper(), key) is not None:
                    cur = Delegate(target=cur, method_name=key, runner=self)
                    continue
                    
                # 1) Property/Child?
                val = cur.props.get(name.upper())
                if val is not None:
                    cur = val
                    if cur is None and name != parts[-1]:
                        raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{prev_path}' ist None (z.B. Parent nicht gesetzt)")
                    continue

                # 2) Methode?
                mctx = self.resolve_method_silent(cur.class_name.upper(), name.upper())
                if mctx is not None:
                    return Delegate(target=cur, method_name=name.upper(), runner=self)

                # 3) Fallback: zentrale Member-Logik benutzen (inkl. native OPEN)
                try:
                    cur = self.get_member(cur, name, ctx)   # <-- name ist "Open" im Original
                    if cur is None and name != parts[-1]:
                        raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{prev_path}' ist None (z.B. Parent nicht gesetzt)")
                    continue
                except RuntimeError:
                    pass
                    
                # 4) sonst Fehler
                raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Member '{name}' nicht gefunden")

            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{parts[0]}' ist kein Objekt (ist {type(cur).__name__})")

        return cur

    def set_chain(self, dotted_ctx, value):
        parts = [t.getText() for t in dotted_ctx.IDENT()]  # z.B. ["THIS", "PushButton1"]
        if not parts:
            raise RuntimeError(f"{dotted_ctx.start.line}:{dotted_ctx.start.column}: leere dottedRef")

        # Startobjekt bestimmen
        head = parts[0].upper()
        if head == "THIS":
            cur = self.this_obj
            if cur is None:
                cur = self.get_var(parts[0], dotted_ctx)
                #raise RuntimeError(f"{dotted_ctx.start.line}:{dotted_ctx.start.column}: THIS ist nicht gesetzt")
        else:
            # z.B. A.B = ...
            cur = self.get_var(parts[0], dotted_ctx)

        # bis zum vorletzten Member entlanglaufen
        for name in parts[1:-1]:
            cur = self.get_member(cur, name, dotted_ctx)  # muss Instance zurückgeben, wenn weiter gekettet wird
        
        # letztes Member setzen
        last = parts[-1].upper()
        if isinstance(cur, Instance):
            self.set_prop(cur, last, value, dotted_ctx)
            #cur.props[last] = value
            #cur.fields[last] = value
            return

        raise RuntimeError(f"{dotted_ctx.start.line}:{dotted_ctx.start.column}: Ziel ist kein Objekt für Member-Set")
        
    def new_instance(self, class_name: str, args: list[Any]):
        cn = class_name.upper()
        
        # 1) FONT ist builtin -> zuerst abfangen
        if cn == "FONT":
            family    = str(args[0]) if len(args) > 0 else "Arial"
            size      = int(args[1]) if len(args) > 1 else 10
            
            bold      = bool(args[2]) if len(args) > 2 else False
            italic    = bool(args[3]) if len(args) > 3 else False
            underline = bool(args[4]) if len(args) > 4 else False
            
            font_obj = QFont(family, size)
            font_obj.setBold(bold)
            font_obj.setItalic(italic)
            font_obj.setUnderline(underline)
            
            return FontValue(
                obj         = font_obj,
                family      = family,
                size        = size,
                bold        = bold,
                italic      = italic,
                underline   = underline)


        # 1b) MENU / POPUPMENU (Qt: QMenu)
        # dBase-Semantik: NEW MENU(THIS) => Menu an Parent (MainWindow-Menubar oder Parent-Menu) anhängen.
        if cn in ("MENU", "POPUPMENU"):
            parent_inst = args[0] if args else None
            parent_backend = parent_inst.backend if isinstance(parent_inst, Instance) else None

            inst = Instance(class_name=cn)
            if isinstance(parent_inst, Instance):
                inst.parent = parent_inst

            # Backend ist immer ein QMenu
            inst.backend = QMenu(parent_backend) if parent_backend is not None else QMenu()

            # Anhängen (wenn Parent mitgegeben)
            try:
                self._attach_menu(inst, parent_inst)
            except Exception:
                # absichtlich leise: Parent kann später per Property gesetzt werden
                pass

            return inst

        # 2) native Qt-Klassen (FORM, PUSHBUTTON, ...)
        if cn in NATIVE_BASES:
            parent_inst = args[0] if args else None
            parent_backend = parent_inst.backend if isinstance(parent_inst, Instance) else None

            inst = Instance(class_name=cn)
            if isinstance(parent_inst, Instance):
                inst.parent = parent_inst
            inst.backend = create_backend_for_base(cn, parent_backend)
            return inst

        # 3) user-defined Klassen
        self._hydrate_class_from_source(cn)
        cdef = self.classes.get(cn)
        if cdef is None:
            known = ", ".join(sorted(self.classes.keys()))
            raise RuntimeError(
                f"{self.loc(None)}: Klasse '{cn}' ist nicht definiert. "
                f"Bekannte Klassen: {known}"
            )
        
        classdef = cdef
        inst = Instance(class_name=classdef.name)
        parent_inst = args[0] if args else None
        if isinstance(parent_inst, Instance):
            inst.parent = parent_inst
        parent_backend = parent_inst.backend if isinstance(parent_inst, Instance) else None
        
        # base backend (FORM etc.)
        if classdef.parent:
            inst.backend = create_backend_for_base(classdef.parent, parent_backend)
        
        # defaults apply
        #for k,v in getattr(classdef, "default_props", {}).items():
        #    set_prop_runtime(inst, k, v)
        for k, v in classdef.default_props.items():
            self.set_prop(inst, k, v)
        
        # execute class body with THIS = inst
        self.push_this(inst)
        self.push_scope()
        try:
            self._scopes[-1]["THIS"] = inst
            self._scopes[-1]["SELF"] = inst
            self.exec_class_body(classdef)
            self._ensure_declared_children_from_source(inst)
        finally:
            self.pop_scope()
            self.pop_this()
        
        if self.resolve_method_silent(classdef.name, "INIT") is not None:
            self.invoke_method(inst, "INIT", args, None)
        
        return inst

    def set_prop(self, inst: Instance, name: str, value: Any, ctx=None):
        key = name.upper()
        
        # 1) normal speichern
        inst.props[key] = value

        # 1a) Objekt-Kinder automatisch binden, damit THIS.PushButton1,
        #     THIS.Container1.PushButton1 usw. sowohl über props als auch
        #     über children zuverlässig auflösbar bleiben.
        if isinstance(value, Instance) and key != "PARENT":
            try:
                self.bind_child(inst, key, value)
            except Exception:
                # Fallback: wenigstens Runtime-Referenz sichern
                inst.children[key] = value

        # MENU/POPUPMENU: Text => Menü-Titel
        if inst.class_name.upper() in ("MENU", "POPUPMENU") and key in ("TEXT", "CAPTION", "TITLE"):
            try:
                if hasattr(inst.backend, "setTitle"):
                    inst.backend.setTitle(str(value))
                elif hasattr(inst.backend, "setWindowTitle"):
                    inst.backend.setWindowTitle(str(value))
            except Exception:
                pass
            return

        # MENU/POPUPMENU: SubMenu anhängen (THIS.MenuDatei.SubMenu = NEW MENU(...))
        if inst.class_name.upper() in ("MENU", "POPUPMENU") and key == "SUBMENU":
            if isinstance(value, Instance) and value.backend is not None:
                # Falls der SubMenu noch keinen Parent hat: automatisch hier einhängen
                try:
                    self._attach_menu(value, inst)
                except Exception:
                    try:
                        if hasattr(inst.backend, "addMenu"):
                            inst.backend.addMenu(value.backend)
                    except Exception:
                        pass
            return


        # 1b) Reparenting: `obj.parent = otherObj` (or `obj.parent = null`)

        if key == "PARENT":
            new_parent = value if isinstance(value, Instance) else None

            # MENU/POPUPMENU: nicht QWidget-reparenting, sondern im Menübaum umhängen
            if inst.class_name.upper() in ("MENU", "POPUPMENU"):
                inst.parent = new_parent
                inst.props[key] = new_parent
                try:
                    self._attach_menu(inst, new_parent)
                except Exception:
                    pass
                return

            # normale Widgets
            self.reparent_instance(inst, new_parent)
            # keep the property value as-is for scripts that inspect it
            inst.props[key] = new_parent
            return
        
        # 2) MouseMove/Focus (Events => EventFilter)
        # MouseMove nur zuverlässig mit MouseTracking
        if hasattr(inst.backend, "setMouseTracking"):
            inst.backend.setMouseTracking(True)
            
        # 2) Event hooks
        if key == "ONGOTFOCUS":
            self._bind_ongotfocus(inst, value, ctx)
            return
        if key == "ONLOSTFOCUS":
            self._bind_onlostfocus(inst, value, ctx)
            return
        
        # Event-Properties?
        if self._bind_event(inst, key, value, ctx):
            return
            
        # 3) normale Qt properties
        apply_property_to_qt(inst, key, value)
    
    def _ensure_event_filter(self, inst: Instance, ctx=None):
        if inst.backend is None:
            return

        # Focus möglich machen
        try:
            inst.backend.setFocusPolicy(Qt.StrongFocus)
        except Exception:
            pass

        # MouseMove auch ohne gedrückte Taste
        try:
            inst.backend.setMouseTracking(True)
        except Exception:
            pass

        if not inst.props.get("_QT_EVENT_FILTER"):
            f = _QtEventFilter(self, inst)
            inst.props["_QT_EVENT_FILTER"] = f
            inst.backend.installEventFilter(f)

    def _bind_onkeydown(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onKeyDown erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, ProgramAbortSignal):
                return None

        inst.props["_ONKEYDOWN_WRAPPER"] = wrapper

    def _bind_onkeyup(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onKeyUp erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, ProgramAbortSignal):
                return None

        inst.props["_ONKEYUP_WRAPPER"] = wrapper

    def _bind_ondblclick(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onDblClick erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, ProgramAbortSignal):
                return None

        inst.props["_ONDBLCLICK_WRAPPER"] = wrapper
        
    def _bind_onclick(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        
        # NEU: Liste/Tuple erlauben
        handlers = handler
        if isinstance(handler, (list, tuple)):
            handlers = list(handler)
        else:
            handlers = [handler]
        
        # Alle müssen Delegate sein
        for h in handlers:
            if not isinstance(h, Delegate):
                raise RuntimeError(
                    f"{self.loc(ctx)}: onClick erwartet Methode(n) (Delegate), bekam {type(h).__name__}"
                )
        
        def wrapper(*qt_args):
            try:
                # nacheinander ausführen
                for h in handlers:
                    try:
                        self.invoke_method(h.target, h.method_name, [inst], None)
                    except (ReturnSignal, ProgramAbortSignal):
                        # Return aus Handler ignorieren -> weiter zum nächsten
                        pass
            except (ReturnSignal, ProgramAbortSignal):
                return None
                
        # nur für Buttons (erstmal)
        if hasattr(inst.backend, "clicked"):
            old = inst.props.get("_ONCLICK_WRAPPER")
            try:
                if old is not None:
                    inst.backend.clicked.disconnect(old)
            except Exception:
                pass
            #raise RuntimeError(f"{self.loc(ctx)}: onClick nicht unterstützt für {inst.class_name}")
            #return
            
            inst.props["_ONCLICK_WRAPPER"   ] = wrapper
            inst.props["_ONCLICK_VIA_SIGNAL"] = True
            
            inst.backend.clicked.connect(wrapper)
            return
            
        inst.props["_ONCLICK_VIA_SIGNAL"] = False
        
        # Alles andere (z.B. FORM/QDialog): EventFilter via MouseRelease
        self._ensure_event_filter(inst, ctx)
        inst.props["_ONCLICK_WRAPPER"] = wrapper
        
    def _bind_onmousedown(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        
        # nur für Buttons (erstmal)
        if not hasattr(inst.backend, "pressed"):
            raise RuntimeError(f"{self.loc(ctx)}: onMouseDown nicht unterstützt für {inst.class_name}")
        
        # Handler muss Delegate sein (oder notfalls BoundMethod)
        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onMouseDown erwartet eine Methode (Delegate), bekam {type(handler).__name__}")
        
        # alten wrapper ggf. disconnecten
        old = inst.props.get("_ONMOUSEDOWN_WRAPPER")
        try:
            if old is not None:
                inst.backend.pressed.disconnect(old)
        except Exception:
            pass
        
        def wrapper(*qt_args):
            # Sender: inst (dBase-Instance)
            try:
                # Wenn dein Handler Sender erwartet:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, ProgramAbortSignal):
                # click-handler ignoriert return meistens
                return None
        
        inst.props["_ONMOUSEDOWN_WRAPPER"] = wrapper
        inst.backend.pressed.connect(wrapper)
    
    def _bind_onmouseup(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        
        # nur für Buttons (erstmal)
        if not hasattr(inst.backend, "released"):
            raise RuntimeError(f"{self.loc(ctx)}: onMouseUp nicht unterstützt für {inst.class_name}")
        
        # Handler muss Delegate sein (oder notfalls BoundMethod)
        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onMouseUp erwartet eine Methode (Delegate), bekam {type(handler).__name__}")
        
        # alten wrapper ggf. disconnecten
        old = inst.props.get("_ONMOUSEUP_WRAPPER")
        try:
            if old is not None:
                inst.backend.released.disconnect(old)
        except Exception:
            pass
        
        def wrapper(*qt_args):
            # Sender: inst (dBase-Instance)
            try:
                # Wenn dein Handler Sender erwartet:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, ProgramAbortSignal):
                # click-handler ignoriert return meistens
                return None
        
        inst.props["_ONMOUSEUP_WRAPPER"] = wrapper
        inst.backend.released.connect(wrapper)

    def _bind_onmousemove(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return

        if not isinstance(handler, Delegate):
            raise RuntimeError(
                f"{self.loc(ctx)}: onMouseMove erwartet eine Methode (Delegate), bekam {type(handler).__name__}"
            )

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                # Minimal: nur Sender
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, ProgramAbortSignal):
                return None

        inst.props["_ONMOUSEMOVE_WRAPPER"] = wrapper

    def _bind_ongotfocus(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return

        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onGotFocus erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, ProgramAbortSignal):
                return None

        inst.props["_ONFOCUSIN_WRAPPER"] = wrapper

    def _bind_onlostfocus(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return

        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onLostFocus erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, ProgramAbortSignal):
                return None

        inst.props["_ONFOCUSOUT_WRAPPER"] = wrapper
    
    def exec_class_body(self, cdef: ClassDef):
        """
        Führt die Init-Statements aus, die beim Collect-Pass gesammelt wurden.
        Das sind z.B. WITH(...), THIS.PushButton1 = NEW ..., WRITE ..., usw.
        """
        # Primär: gesammelt in cdef.inits
        if getattr(cdef, "inits", None):
            for st in cdef.inits:
                self.visit(st)
            return

        # Fallback: alter Weg über body_ctx (falls du den später setzt)
        body = getattr(cdef, "body_ctx", None)
        if body is None:
            return

        for item in body.classBodyItem():
            if item.propertyDecl() is not None:
                continue
            if item.methodDecl() is not None:
                continue
            st = item.statement()
            if st is not None:
                self.visit(st)
            
    def collect_default_props(self, class_name: str) -> dict:
        cname = class_name.upper()

        # Klassenkette sammeln: derived -> base
        chain = []
        c = cname
        while c:
            cdef = self.classes.get(c)
            if not cdef:
                break
            chain.append(cdef)
            c = cdef.parent.upper() if cdef.parent else None

        # base -> derived mergen (Kind überschreibt)
        out = {}
        for cdef in reversed(chain):
            for k, v in (cdef.default_props or {}).items():
                out[k.upper()] = deepcopy(v)
        return out
        
    # Wert für PROPERTY ... = <expr> auswerten.
    # Läuft in einem frischen Scope und setzt THIS/SELF auf die neue Instanz.
    def _eval_property_default(self, expr_ctx, this_obj: Instance):
        local = {"THIS": this_obj, "SELF": this_obj}
        self._scopes.append(local)
        try:
            return self.visit(expr_ctx)
        finally:
            self._scopes.pop()
    
    def _norm(self, name: str) -> str:
        return name.upper()

    def _ensure_classdef(self, class_name: str) -> dict:
        k = self._norm(class_name.upper())
        if k not in self.classes:
            self.classes[k] = {
                "props": set(),
                "methods": {},
                "inits": [],
                # optional: "base": None,
            }
        else:
            # falls Klasse schon existiert, aber alt aufgebaut ist:
            self.classes[k].setdefault("props", set())
            self.classes[k].setdefault("methods", {})
            self.classes[k].setdefault("inits", [])
        return self.classes[k]
        
    def _vkey(self, name: str) -> str:
        return name.upper()

    def has_var(self, name: str) -> bool:
        key = self._vkey(name)
        return any(key in s for s in reversed(self._scopes))

    def get_var(self, name: str, ctx=None):
        key = self._vkey(name)
        for s in reversed(self._scopes):
            if key in s:
                return s[key]
        if ctx:
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Variable '{key}' ist nicht definiert")
        raise RuntimeError(f"Variable '{key}' ist nicht definiert")

    def set_var(self, name: str, value):
        key = self._vkey(name)

        # wenn vorhanden: im nächstliegenden Scope updaten
        for s in reversed(self._scopes):
            if key in s:
                s[key] = value
                return

        # sonst: neu im aktuellen Scope anlegen
        self._scopes[-1][key] = value
    
    def _eval_input_text(self, raw_text: str):
        text = (raw_text or "").strip()
        if text == "":
            return ""

        upper = text.upper()
        if upper in ("T", ".T.", "Y", ".Y."):
            return True
        if upper in ("F", ".F.", "N", ".N."):
            return False

        source = InputStream(text)
        lexer = dBaseLexer(source)
        tokens = CommonTokenStream(lexer)
        tokens.fill()
        parser = dBaseParser(tokens)
        listener = _attach_silent_antlr_errors(lexer, parser)
        tree = parser.expr()

        if parser.getNumberOfSyntaxErrors() > 0:
            msg = listener.messages[0] if listener.messages else "Ungültiger Ausdruck"
            raise RuntimeError(msg)
        if tokens.LA(1) != Token.EOF:
            raise RuntimeError("Ungültiger Ausdruck")

        return self.visit(tree)

    def _assign_input_target(self, target_name: str, value):
        target_name = str(target_name or "").strip()
        if not target_name:
            raise RuntimeError("INPUT: Missing target variable name")

        parts = [p.strip() for p in target_name.split('.') if p.strip()]
        if not parts:
            raise RuntimeError("INPUT: Missing target variable name")

        if len(parts) == 1:
            self._set_name(parts[0], value, None)
            return

        self._set_chain_parts(parts, value, None)

    def _builtin_INPUT(self, prompt_expr="", target_name=""):
        prompt_text = "" if prompt_expr is None else str(prompt_expr)
        target_name = str(target_name or "").strip()
        if not target_name:
            raise RuntimeError("INPUT: Missing target variable name")

        parent = MAINAPP if "MAINAPP" in globals() else None

        while True:
            raw_text, rc = InputValueDialog.get_value(prompt=prompt_text, parent=parent)
            self.set_var("INPUT_RC", int(rc))
            self.set_var("_INPUT_RC", int(rc))

            if int(rc) == 0:
                self._assign_input_target(target_name, "")
                return 0

            try:
                value = self._eval_input_text(raw_text)
            except Exception as e:
                QMessageBox.warning(
                    parent,
                    "Ungültige Eingabe",
                    str(e)
                )
                continue

            self._assign_input_target(target_name, value)
            return 1

    # ---------- Statements ----------
    def _precollect_classes_from_source(self):
        text = getattr(self, "_pre_source", "") or ""
        if not text:
            return

        rx = re.compile(r'^\s*CLASS\s+(?P<name>[A-Za-z_]\w*)(?:\s+OF\s+(?P<parent>[A-Za-z_]\w*))?\b', re.IGNORECASE | re.MULTILINE)
        for m in rx.finditer(text):
            cname = m.group('name').upper()
            parent = m.group('parent').upper() if m.group('parent') else None
            cdef = self.classes.get(cname)
            if cdef is None or not isinstance(cdef, ClassDef):
                self.classes[cname] = ClassDef(name=cname, parent=parent)
            else:
                if parent and not cdef.parent:
                    cdef.parent = parent

    def _get_class_line_ranges(self):
        if self._class_line_ranges is not None:
            return self._class_line_ranges

        text = getattr(self, "_pre_source", "") or ""
        ranges = []
        stack = []

        for lineno, raw in enumerate(text.splitlines(), start=1):
            line = raw.strip()
            if re.match(r"^CLASS\b", line, re.IGNORECASE):
                stack.append(lineno)
                continue
            if re.match(r"^ENDCLASS\b", line, re.IGNORECASE):
                if stack:
                    start = stack.pop()
                    ranges.append((start, lineno))

        self._class_line_ranges = ranges
        return ranges


    def _eval_expr_text_from_source(self, expr_text: str):
        txt = (expr_text or "").strip()
        if not txt:
            return None
        try:
            sub_source = InputStream(txt)
            sub_lexer = dBaseLexer(sub_source)
            sub_tokens = CommonTokenStream(sub_lexer)
            sub_tokens.fill()
            sub_parser = dBaseParser(sub_tokens)
            _attach_silent_antlr_errors(sub_lexer, sub_parser)
            if hasattr(sub_parser, "expr"):
                ectx = sub_parser.expr()
                return self.visit(ectx)
        except Exception:
            pass

        u = txt.upper()
        if u in (".T.", "TRUE"):
            return True
        if u in (".F.", "FALSE"):
            return False
        if (txt.startswith('"') and txt.endswith('"')) or (txt.startswith("'") and txt.endswith("'")):
            try:
                return self._unescape_string(txt)
            except Exception:
                return txt[1:-1]
        try:
            if "." in txt:
                return float(txt)
            return int(txt)
        except Exception:
            return txt

    def _parse_statements_from_source(self, source_text: str):
        txt = source_text or ""
        if not txt.strip():
            return []
        try:
            if not txt.endswith("\n"):
                txt += "\n"
            sub_source = InputStream(txt)
            sub_lexer = dBaseLexer(sub_source)
            sub_tokens = CommonTokenStream(sub_lexer)
            sub_tokens.fill()
            sub_parser = dBaseParser(sub_tokens)
            _attach_silent_antlr_errors(sub_lexer, sub_parser)
            sub_tree = sub_parser.input_()
            out = []
            items = []
            try:
                items = sub_tree.item() or []
            except Exception:
                items = []
            if not isinstance(items, list):
                items = [items]
            for it in items:
                if it is None:
                    continue
                try:
                    st = it.statement()
                except Exception:
                    st = None
                if st is not None:
                    out.append(st)
            return out
        except Exception:
            return []

    def _hydrate_class_from_source(self, class_name: str):
        source = getattr(self, "_pre_source", "") or ""
        cname = (class_name or "").strip().upper()
        if not source or not cname:
            return

        class_pat = re.compile(
            rf'(?ims)^\s*CLASS\s+{re.escape(cname)}\b(?:\s+OF\s+(?P<parent>[A-Za-z_]\w*))?(?P<body>.*?)^\s*ENDCLASS\b'
        )
        m_class = class_pat.search(source)
        if not m_class:
            return

        parent_name = m_class.group('parent').upper() if m_class.group('parent') else None
        class_body = m_class.group('body') or ''

        cdef = self.classes.get(cname)
        if cdef is None or not isinstance(cdef, ClassDef):
            cdef = ClassDef(name=cname, parent=parent_name)
            self.classes[cname] = cdef
        else:
            cdef.name = cname
            cdef.parent = parent_name

        cdef.methods = {}
        cdef.default_props = {}
        cdef.inits = []

        pre_method = re.split(r'(?im)^\s*METHOD\b', class_body, maxsplit=1)[0]

        prop_rx = re.compile(r'(?im)^\s*PROPERTY\s+(?P<name>[A-Za-z_]\w*)\s*=\s*(?P<expr>.+?)\s*$')
        for pm in prop_rx.finditer(pre_method):
            pname = pm.group('name').upper()
            pexpr = pm.group('expr')
            cdef.default_props[pname] = self._eval_expr_text_from_source(pexpr)

        init_stmts = self._parse_statements_from_source(pre_method)
        if init_stmts:
            cdef.inits.extend(init_stmts)

        method_rx = re.compile(
            r'(?ims)^\s*METHOD\s+(?P<name>[A-Za-z_]\w*)\b\s*\((?P<params>.*?)\)\s*(?P<body>.*?)^\s*ENDMETHOD\b'
        )
        for mm in method_rx.finditer(class_body):
            mname = mm.group('name').upper()
            snippet = mm.group(0)
            try:
                if not snippet.endswith("\n"):
                    snippet += "\n"
                sub_source = InputStream(snippet)
                sub_lexer = dBaseLexer(sub_source)
                sub_tokens = CommonTokenStream(sub_lexer)
                sub_tokens.fill()
                sub_parser = dBaseParser(sub_tokens)
                _attach_silent_antlr_errors(sub_lexer, sub_parser)
                if hasattr(sub_parser, 'methodDecl'):
                    mctx = sub_parser.methodDecl()
                    if mctx is not None:
                        cdef.methods[mname] = mctx
                        continue
            except Exception:
                pass
            found = self._find_method_decl_in_source(cname, mname)
            if found is not None:
                cdef.methods[mname] = found

        self.classes[cname] = cdef

    def _hydrate_all_classes_from_source(self):
        text = getattr(self, "_pre_source", "") or ""
        if not text:
            return
        rx = re.compile(r'^\s*CLASS\s+(?P<name>[A-Za-z_]\w*)\b', re.IGNORECASE | re.MULTILINE)
        seen = set()
        for m in rx.finditer(text):
            cname = m.group('name').upper()
            if cname in seen:
                continue
            seen.add(cname)
            self._hydrate_class_from_source(cname)

    def _is_line_inside_class_block(self, lineno: int) -> bool:
        if not lineno:
            return False
        for start, stop in self._get_class_line_ranges():
            if start <= lineno <= stop:
                return True
        return False

    def _collect_all_classdecls(self, node, seen=None):
        if node is None:
            return
        if seen is None:
            seen = set()
        try:
            nid = id(node)
            if nid in seen:
                return
            seen.add(nid)
        except Exception:
            pass

        tname = type(node).__name__
        if tname.endswith("ClassDeclContext"):
            self.visitClassDecl(node)
            return

        if hasattr(node, "classDecl"):
            try:
                cd = node.classDecl()
            except TypeError:
                cd = None
            if cd is not None:
                if isinstance(cd, list):
                    for it in cd:
                        if it is not None:
                            self.visitClassDecl(it)
                else:
                    self.visitClassDecl(cd)

        children = getattr(node, "children", None)
        if children:
            for ch in children:
                self._collect_all_classdecls(ch, seen)

    def visitInput(self, ctx):
        # Pass 1: Klassen + top-level Methoden registrieren
        if self._mode == "collect":
            self._precollect_classes_from_source()
            self._collect_all_classdecls(ctx)
            self._hydrate_all_classes_from_source()
            for it in ctx.item():
                try:
                    mctx = it.methodDecl()
                except Exception:
                    mctx = None
                if mctx is not None:
                    self.visit(mctx)
            return None

        # Pass 2: nur echte Top-Level-Statements ausführen.
        # Parser-Recovery kann Anweisungen aus CLASS...ENDCLASS-Blöcken als
        # scheinbare Top-Level-Statements durchreichen; die dürfen hier nicht
        # laufen, weil z.B. WITH(THIS) nur beim Instanziieren gültig ist.
        for it in ctx.item():
            if it.statement():
                st = it.statement()
                if hasattr(st, "classDecl") and st.classDecl() is not None:
                    continue
                try:
                    st_line = getattr(getattr(st, "start", None), "line", 0) or 0
                except Exception:
                    st_line = 0
                if self._is_line_inside_class_block(st_line):
                    continue
                self.visit(st)

        return None

    def visitCallStmt(self, ctx):
        # callee irgendwie holen – z.B.:
        callee = self.visit(ctx.memberExpr())   # je nach Grammar: memberExpr/MemberExpr/etc.

        args = []
        if hasattr(ctx, "argList") and ctx.argList() is not None:
            args = [self.visit(e) for e in ctx.argList().expr()]

        # Delegate kann man "aufrufen", indem man die Methode im DSL ausführt
        if isinstance(callee, Delegate):
            return self.invoke_method(callee.target, callee.method_name, args, ctx)

        # normale Python-Funktionen
        if not callable(callee):
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Ausdruck ist nicht aufrufbar: {ctx.getText()}")

        return callee(*args)
            
    def visitDoWhileStatement(self, ctx):
        #_debug_print("DEBUG: enter DO WHILE")
        guard = 0
        while True:
            cond = self.visit(ctx.condition())
            #_debug_print("DEBUG: condition =", cond)
            
            if not cond:
                #_debug_print("DEBUG: leave DO WHILE (cond false)")
                break
            
            try:
                self.visit(ctx.block())
            except BreakSignal:
                break   # beendet Schleife
                
            guard += 1
            if guard > 1_000_000:
                raise RuntimeError("DO WHILE: Endlosschleife?")
            
    def visitNewExpr(self, ctx):
        class_name = ctx.IDENT().getText().upper()

        args = []
        if ctx.argList() is not None:
            args = [self.visit(e) for e in ctx.argList().expr()]

        # WICHTIG: benutze die robuste Instanz-Erzeugung
        return self.new_instance(class_name.upper(), args)
    
    def visitDeleteStmt(self, ctx):
        name = ctx.IDENT().getText().upper()

        # zuerst in lokalen Scopes suchen (innerstes zuerst)
        for scope in reversed(self._scopes):
            if name in scope:
                obj = scope[name]
                self._maybe_destroy(obj, ctx)
                del scope[name]
                return None

        # dann globals
        if name in self.globals:
            obj = self.globals[name]
            self._maybe_destroy(obj, ctx)
            del self.globals[name]
            return None

        raise Exception(f"{ctx.start.line}:{ctx.start.column}: DELETE: Variable '{name}' existiert nicht")


    def _maybe_destroy(self, obj, ctx):
        if not isinstance(obj, Instance):
            return
        # falls du sowas willst:
        try:
            owner_class, mctx = self.resolve_method(obj.class_name.upper(), "DESTROY", ctx)
        except Exception:
            return
        self.execute_method(owner_class, mctx, [], this_obj=obj)
    
    def execute_method(self, owner_class_name: str, method_ctx, arg_values, this_obj):
        prev_this = self.this_obj
        self.this_obj = this_obj
        self.push_scope()
        try:
            self.set_var("THIS", this_obj)
            params = self._get_method_params(method_ctx)
            for i, pname in enumerate(params):
                self.set_var(pname.upper(), arg_values[i] if i < len(arg_values) else None)
            return self.visit(method_ctx.block())
        finally:
            self.pop_scope()
            self.this_obj = prev_this
    
    def visitVarRef(self, ctx):
        name = ctx.IDENT().getSymbol().text
        return self._get_name(name)
    
    def _get_class_members(self, ctx):
        # probiere typische Namen in Reihenfolge
        for name in ("classBody", "classMembers", "classItems", "classItem", "classStmt", "classStatement", "member"):
            if hasattr(ctx, name):
                node = getattr(ctx, name)()
                if node is None:
                    continue
                # wenn node selbst die Liste hat:
                for list_name in ("classMember", "member", "classItem", "statement", "stmt"):
                    if hasattr(node, list_name):
                        return getattr(node, list_name)()
                # manchmal ist node schon eine Liste
                if isinstance(node, list):
                    return node
        return []
    
    def visitPropertyDecl(self, ctx):
        # PROPERTY <ident> = <expr>
        # zur Laufzeit: in THIS.props schreiben
        this_obj = self.get_var("THIS", ctx)

        if not isinstance(this_obj, Instance):
            raise RuntimeError(f"{self.loc(ctx)}: PROPERTY nur innerhalb einer Instanz gültig")

        pname = ctx.IDENT().getText().upper()
        pval  = self.visit(ctx.expr()) if ctx.expr() else None

        this_obj.props[pname] = pval
        return None
    
    def _handle_property_decl(self, pctx, cdef: ClassDef):
        # pctx ist propertyDeclContext
        pname = pctx.IDENT().getText().upper()
        pval  = self.visit(pctx.expr())   # Expression auswerten
        cdef.default_props[pname] = pval

    def _walk_tree_nodes(self, node, seen=None):
        if node is None:
            return
        if seen is None:
            seen = set()
        try:
            nid = id(node)
            if nid in seen:
                return
            seen.add(nid)
        except Exception:
            pass
        yield node
        children = getattr(node, 'children', None)
        if children:
            for ch in children:
                yield from self._walk_tree_nodes(ch, seen)

    def _collect_methods_from_node(self, node, cdef: ClassDef):
        changed = False
        for sub in self._walk_tree_nodes(node):
            tname = type(sub).__name__
            mctx = None
            if tname.endswith('MethodDeclContext'):
                mctx = sub
            elif hasattr(sub, 'methodDecl'):
                try:
                    tmp = sub.methodDecl()
                except TypeError:
                    tmp = None
                if isinstance(tmp, list):
                    for one in tmp:
                        if one is None:
                            continue
                        mname = self._method_name(one).upper()
                        cdef.methods[mname] = one
                        changed = True
                    continue
                mctx = tmp
            if mctx is not None:
                mname = self._method_name(mctx).upper()
                cdef.methods[mname] = mctx
                changed = True
        return changed

    def _find_method_decl_in_tree(self, class_name: str, method_name: str):
        tree = getattr(self, '_parse_tree', None)
        if tree is None:
            return None

        cname = (class_name or '').upper()
        mname = (method_name or '').upper()

        for node in self._walk_tree_nodes(tree):
            if not type(node).__name__.endswith('ClassDeclContext'):
                continue
            try:
                node_cname = node.name.text.upper()
            except Exception:
                continue
            if node_cname != cname:
                continue

            for sub in self._walk_tree_nodes(node):
                if not type(sub).__name__.endswith('MethodDeclContext'):
                    continue
                try:
                    if self._method_name(sub).upper() == mname:
                        return sub
                except Exception:
                    pass
        return None

    def _find_method_decl_in_source(self, class_name: str, method_name: str):
        source = getattr(self, '_pre_source', None)
        if not source:
            return None

        cname = (class_name or '').strip()
        mname = (method_name or '').strip()
        if not cname or not mname:
            return None

        try:
            class_pat = re.compile(
                rf'(?is)\bCLASS\s+{re.escape(cname)}\b(?:\s+OF\s+[A-Za-z_]\w*)?(?P<body>.*?)\bENDCLASS\b'
            )
            m_class = class_pat.search(source)
            if not m_class:
                return None

            class_body = m_class.group('body') or ''
            method_pat = re.compile(
                rf'(?is)\bMETHOD\s+{re.escape(mname)}\b\s*\((?P<params>.*?)\)\s*(?P<body>.*?)\bENDMETHOD\b'
            )
            m_method = method_pat.search(class_body)
            if not m_method:
                return None

            params = (m_method.group('params') or '').strip()
            body = (m_method.group('body') or '').strip()
            snippet = f"METHOD {mname}({params})\n{body}\nENDMETHOD\n"

            sub_source = InputStream(snippet)
            sub_lexer = dBaseLexer(sub_source)
            sub_tokens = CommonTokenStream(sub_lexer)
            sub_parser = dBaseParser(sub_tokens)

            if hasattr(sub_parser, 'methodDecl'):
                mctx = sub_parser.methodDecl()
                return mctx
        except Exception:
            return None

        return None

    def _ensure_declared_children_from_source(self, inst: Instance):
        source = getattr(self, "_pre_source", None)
        if not source or not isinstance(inst, Instance):
            return

        cname = (getattr(inst, "class_name", "") or "").strip()
        if not cname:
            return

        try:
            class_pat = re.compile(
                rf'(?is)\bCLASS\s+{re.escape(cname)}\b(?:\s+OF\s+[A-Za-z_]\w*)?(?P<body>.*?)\bENDCLASS\b'
            )
            m_class = class_pat.search(source)
            if not m_class:
                return

            class_body = m_class.group('body') or ''
            pre_method = re.split(r'(?im)^\s*METHOD\b', class_body, maxsplit=1)[0]

            # 1) direkte Kinder: THIS.PushButton1 = NEW PUSHBUTTON(THIS)
            rx_direct = re.compile(
                r'(?im)^\s*THIS\.(?P<name>[A-Za-z_]\w*)\s*=\s*NEW\s+(?P<klass>[A-Za-z_]\w*)\s*\(\s*THIS\s*\)\s*$'
            )
            for m in rx_direct.finditer(pre_method):
                key = m.group('name').upper()
                if key in inst.props or key in inst.children:
                    continue
                child_class = m.group('klass').upper()
                try:
                    child = self.new_instance(child_class, [inst])
                    self.bind_child(inst, key, child)
                except Exception:
                    pass

            # 2) ein Level verschachtelt: THIS.Container1.PushButton1 = NEW PUSHBUTTON(THIS.Container1)
            rx_nested = re.compile(
                r'(?im)^\s*THIS\.(?P<owner>[A-Za-z_]\w*)\.(?P<name>[A-Za-z_]\w*)\s*=\s*NEW\s+(?P<klass>[A-Za-z_]\w*)\s*\(\s*THIS\.(?P=owner)\s*\)\s*$'
            )
            for m in rx_nested.finditer(pre_method):
                owner_key = m.group('owner').upper()
                child_key = m.group('name').upper()
                owner_obj = inst.props.get(owner_key) or inst.children.get(owner_key)
                if not isinstance(owner_obj, Instance):
                    continue
                if child_key in owner_obj.props or child_key in owner_obj.children:
                    continue
                child_class = m.group('klass').upper()
                try:
                    child = self.new_instance(child_class, [owner_obj])
                    self.bind_child(owner_obj, child_key, child)
                except Exception:
                    pass
        except Exception:
            return

    def _ensure_class_methods_loaded(self, class_name: str):
        c = (class_name or '').upper()
        cdef = self.classes.get(c)
        if not isinstance(cdef, ClassDef):
            return

        # Nicht nur bei komplett leeren Methodenlisten laden.
        # In einigen Tree-Formen werden einzelne Methoden (z.B. INIT)
        # beim ersten Collect übersehen, obwohl andere Methoden schon
        # vorhanden sind. Deshalb immer noch einmal robust über body/decl
        # nachladen; das Dict verhindert Dubletten automatisch.
        body = getattr(cdef, 'body_ctx', None)
        decl = getattr(cdef, 'decl_ctx', None)
        if body is not None:
            self._collect_methods_from_node(body, cdef)
        if decl is not None:
            self._collect_methods_from_node(decl, cdef)
        self.classes[c] = cdef
        
    def visitClassDecl(self, ctx):
        if getattr(self, "_mode", "") != "collect":
            return None
        
        class_name  = ctx.name.text.upper()
        parent_name = ctx.parent.text.upper() if ctx.parent else None
        
        cdef = self.classes.get(class_name)
        if cdef is None or not isinstance(cdef, ClassDef):
            cdef = ClassDef(name=class_name.upper(), parent=parent_name)
            self.classes[class_name] = cdef
        else:
            cdef.name = class_name.upper()
            cdef.parent = parent_name
            # beim erneuten Collect nicht anhäufen
            cdef.methods = {}
            cdef.default_props = {}
            cdef.inits = []

        body = ctx.classBody()
        cdef.body_ctx = body
        cdef.decl_ctx = ctx

        # 1) echte classMember zuverlässig einsammeln
        members = []
        try:
            members = body.classMember() or []
        except Exception:
            members = []
        if not isinstance(members, list):
            members = [members]

        for ch in members:
            if ch is None:
                continue
            if hasattr(ch, "propertyDecl") and ch.propertyDecl() is not None:
                self._handle_property_decl(ch.propertyDecl(), cdef)
                continue
            if hasattr(ch, "methodDecl") and ch.methodDecl() is not None:
                mctx = ch.methodDecl()
                mname = self._method_name(mctx).upper()
                cdef.methods[mname] = mctx
                continue
            if hasattr(ch, "assignStmt") and ch.assignStmt() is not None:
                cdef.inits.append(ch.assignStmt())
                continue
            if hasattr(ch, "withStmt") and ch.withStmt() is not None:
                cdef.inits.append(ch.withStmt())
                continue

        # 2) zusätzliche normale statements im Klassenrumpf (z.B. WRITE ...)
        stmts = []
        try:
            stmts = body.statement() or []
        except Exception:
            stmts = []
        if not isinstance(stmts, list):
            stmts = [stmts]
        for st in stmts:
            if st is not None:
                cdef.inits.append(st)

        # 3) Zusätzlicher robuster Scan des gesamten Klassenknotens.
        #    Wichtig: methodDecl kann je nach Tree-Form nicht immer sauber in
        #    body.classMember() auftauchen. Darum Methoden immer zusätzlich
        #    rekursiv einsammeln; Properties/Inits nur ergänzend.
        self._collect_methods_from_node(body, cdef)

        seen_init_ids = {id(x) for x in cdef.inits}
        for ch in list(getattr(body, "children", []) or []):
            tname = type(ch).__name__
            if hasattr(ch, "propertyDecl") and ch.propertyDecl():
                self._handle_property_decl(ch.propertyDecl(), cdef)
            elif hasattr(ch, "assignStmt") and ch.assignStmt():
                sub = ch.assignStmt()
                if id(sub) not in seen_init_ids:
                    cdef.inits.append(sub)
                    seen_init_ids.add(id(sub))
            elif hasattr(ch, "withStmt") and ch.withStmt():
                sub = ch.withStmt()
                if id(sub) not in seen_init_ids:
                    cdef.inits.append(sub)
                    seen_init_ids.add(id(sub))
            elif tname.endswith("StatementContext"):
                if id(ch) not in seen_init_ids:
                    cdef.inits.append(ch)
                    seen_init_ids.add(id(ch))

        self.classes[class_name] = cdef
        return None

    # Basisklasse -> Kind-Reihenfolge, damit Kind überschreiben könnte (später).
    def collect_props(self, class_name: str) -> list[str]:
        out = []
        seen = set()

        c = class_name.upper()
        chain = []

        while c:
            if c not in self.classes:
                break
            chain.append(c)
            parent = self.classes[c].parent
            c = parent.upper() if parent else None

        for cname in reversed(chain):  # base zuerst
            for p in self.classes[cname].get("props", set()):
                if p not in seen:
                    seen.add(p)
                    out.append(p)

        return out
 
    def _method_name(self, ctx):
        # Label: name=IDENT
        if hasattr(ctx, "name") and ctx.name is not None:
            return ctx.name.text

        # Token getter: IDENT() oder ID()
        for tok in ("IDENT", "ID"):
            fn = getattr(ctx, tok, None)
            if callable(fn):
                t = fn()
                if t:
                    return t.getText()

        # Rule getter: identifier()
        fn = getattr(ctx, "identifier", None)
        if callable(fn):
            sub = fn()
            if sub:
                return sub.getText()

        # Fallback
        return ctx.getText()

    def visitMethodDecl(self, ctx):
        method_name = ctx.name.text.upper()

        params = []
        pl = ctx.paramList()
        if pl is not None:
            params = [t.getText().upper() for t in pl.IDENT()]

        body = ctx.block()
        self.methods[method_name] = MethodDef(params=params, block_ctx=body)
        return None

    def visitMemberExpr(self, ctx):
        idents = [t.getText() for t in ctx.IDENT()]

        # THIS vorkommt
        if ctx.THIS() is not None:
            parts = ["THIS"] + idents
        else:
            parts = idents

        # Sonderfall: einzelner Name (z.B. "Font" oder "Sender")
        # -> MUSS über _get_name laufen, damit WITH-Context/Props funktionieren
        if len(parts) == 1 and parts[0].upper() != "THIS":
            return self._get_name(parts[0])

        # Sonderfall: nur "THIS"
        if parts == ["THIS"]:
            if self.this_stack:
                return self.cur_this()
            return self.get_var("THIS", ctx)

        # Optional: schneller Pfad THIS.Method => Delegate
        if len(parts) == 2 and parts[0].upper() == "THIS":
            this_obj = self.get_var("THIS", ctx)
            if isinstance(this_obj, Instance):
                key = parts[1].upper()
                if self.resolve_method_silent(this_obj.class_name.upper(), key) is not None:
                    return Delegate(target=this_obj, method_name=key, runner=self)

        return self.get_chain(parts, ctx)

    
    def visitPostfixExpr(self, ctx):
        # Basis auswerten
        cur = self.visit(ctx.primary())
        expr_list = []
        #_debug_print("===> ", cur)
        # Alle argLists einsammeln (für jeden '(' ... ')'-Call)
        arglists = ctx.argList() or []
        if not isinstance(arglists, list):
            arglists = [arglists]
        call_i = 0
        #_debug_print("--> ", ctx.argList())
        
        pending_member = None  # merkt sich den Namen nach '.'

        i = 1  # child(0) ist primary
        while i < ctx.getChildCount():
            t = ctx.getChild(i).getText()

            # Member-Start: ".Name"
            if t == '.':
                pending_member = ctx.getChild(i + 1).getText()
                i += 2
                continue

            # Call: "( ... )"
            if t == '(':
                # Argumente zur passenden argList
                if call_i < len(arglists):
                    al = arglists[call_i]

                    exprs = al.expr()
                    if exprs is None:
                        expr_list = []
                    elif isinstance(exprs, list):
                        expr_list = exprs
                    else:
                        # WICHTIG: einzelner ExprContext ist iterierbar -> sonst "Child-Liste"
                        expr_list = [exprs]
                        
                args = [self.visit(e) for e in expr_list]

                call_i += 1

                # Call ausführen
                if pending_member is None:
                    # direkter Call: Foo(...)
                    # dBase-Methoden-Objekte auch aufrufbar machen
                    if isinstance(cur, Delegate):
                        cur = self.invoke_method(cur.target, cur.method_name, args, ctx)
                    elif isinstance(cur, BoundMethod):
                        cur = self.invoke_method(cur.target, cur.name, args, ctx)
                    elif callable(cur):
                        cur = cur(*args)
                    else:
                        raise Exception(
                            f"{ctx.start.line}:{ctx.start.column}: Ausdruck ist nicht aufrufbar: {ctx.getText()}"
                        )
                else:
                    # Methoden-/Membercall: obj.Member(...)
                    name = pending_member
                    pending_member = None

                    if isinstance(cur, Instance):
                        # resolve_method NICHT separat aufrufen (Altlast / falscher Zugriff bei ClassDef)
                        cur = self.invoke_method(cur, name, args, ctx)
                    else:
                        fn = self.get_member(cur, name, ctx)
                        if callable(fn):
                            cur = fn(*args)
                        else:
                            raise Exception(
                                f"{ctx.start.line}:{ctx.start.column}: Member '{name}' ist nicht aufrufbar"
                            )

                i += 1
                continue

            # Falls noch ein Member "steht" und kein '(' folgt: obj.Member
            if pending_member is not None:
                cur = self.get_member(cur, pending_member, ctx)
                pending_member = None
                continue

            i += 1

        # falls am Ende noch ".X"
        if pending_member is not None:
            cur = self.get_member(cur, pending_member, ctx)

        return cur

    def visitLvalue(self, ctx):
        pe = ctx.postfixExpr()

        # Basis (primary) als Text
        base = pe.primary().getText()

        # Suffixe iterieren: children enthalten '.' IDENT oder '(' ... ')'
        parts = [base]
        i = 1  # child 0 ist primary
        while i < pe.getChildCount():
            ch = pe.getChild(i).getText()

            if ch == '.':
                ident = pe.getChild(i + 1).getText()
                parts.append(ident)
                i += 2
                continue

            if ch == '(':
                # Call in LHS ist nicht erlaubt
                raise Exception(f"{ctx.start.line}:{ctx.start.column}: LVALUE darf keinen Call enthalten: {pe.getText()}")

            i += 1

        # z.B. "THIS.width" -> ["THIS","width"]
        return parts
    
    def _lvalue_chain_from_postfix(self, pe, ctx):
        # pe ist postfixExpr-Context
        chain = [pe.primary().getText()]

        i = 1  # child 0 ist primary
        while i < pe.getChildCount():
            ch = pe.getChild(i).getText()

            if ch == '.':
                chain.append(pe.getChild(i + 1).getText())
                i += 2
                continue

            if ch == '(':
                raise Exception(
                    f"{ctx.start.line}:{ctx.start.column}: "
                    f"Assignment-Ziel darf keinen Call enthalten: {pe.getText()}"
                )

            i += 1

        return [s.upper() for s in chain]
    
    def set_chain_on_object(self, base_obj, chain: list[str], value, ctx):
        if base_obj is None:
            raise RuntimeError("WITH base object is None")

        if not chain:
            raise RuntimeError("empty chain in assignment")

        obj = base_obj
        # bis vor die letzte Property laufen
        for name in chain[:-1]:
            # hier brauchst du irgendeine Art get_member (oder du nutzt fields direkt)
            obj = self.get_member(obj, name, ctx)  # <- falls du das hast
            if obj is None:
                raise RuntimeError(f"WITH chain member '{name}' is None")

        return self.set_member(obj, chain[-1], value, ctx)
    
    def visitAssignment(self, ctx):
        value = self.visit(ctx.expr())
        self.set_chain(ctx.dottedRef(), value)
        return value
        
    def _set_chain_parts(self, parts, value, ctx):
        head = parts[0].upper()

        if head == "THIS":
            cur = self.get_var("THIS", ctx)
            if cur is None:
                raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: THIS ist nicht gesetzt")
        else:
            cur = self.get_var(parts[0], ctx)  # z.B. Sender, obj, etc.

        if cur is None:
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{parts[0]}' ist nicht definiert")

        # Merker: wenn wir gerade Font.* ändern, brauchen wir den "Besitzer" (z.B. Sender)
        font_container = None

        # bis zum vorletzten auflösen
        for name in parts[1:-1]:
            # Wenn das nächste Segment "Font" ist und cur ein Instance ist,
            # dann ist cur der Container (z.B. Sender), dessen Font wir später neu anwenden müssen.
            if name.upper() == "FONT" and isinstance(cur, Instance):
                font_container = cur

            cur = self.get_member(cur, name, ctx)

        last = parts[-1]  # NICHT uppern, set_member macht eh upper intern (oder du machst's dort)

        # 1) normales Instance-Property setzen (Sender.Text = ..., Sender.Font = NEW FONT(...))
        if isinstance(cur, Instance):
            self.set_prop(cur, last.upper(), value, ctx)  # aktualisiert props + Qt (setText etc.)
            return

        # 2) Unter-Property auf "value object" setzen (z.B. Sender.Font.bold = .T.)
        #    -> cur ist dann z.B. FontValue
        self.set_member(cur, last, value, ctx)

        # Wenn wir Font.* geändert haben: Font erneut auf den Container anwenden,
        # damit Qt das wirklich übernimmt.
        if font_container is not None:
            try:
                fv = self.get_member(font_container, "FONT", ctx)  # liefert FontValue
            except Exception:
                fv = font_container.props.get("FONT")

            if fv is not None:
                # set_prop sorgt bei dir dafür, dass Qt aktualisiert wird
                self.set_prop(font_container, "FONT", fv, ctx)

        return
        
    def assign_lvalue(self, lctx, value, ctx):
        # häufig: lvalue : IDENT ('.' IDENT)* ;
        if hasattr(lctx, "IDENT") and lctx.IDENT():
            toks = lctx.IDENT()
            parts = [t.getText() for t in (toks if isinstance(toks, list) else [toks])]

            # nur X = ...
            if len(parts) == 1:
                self._set_name(parts[0], value, ctx)   # WITH-aware: setzt Var oder Property
                return

            # THIS.PushButton1 = ...
            self._set_chain_parts(parts, value, ctx)
            return
        
        # fallback: Text parsen (quick&dirty, aber funktioniert)
        text = lctx.getText()  # z.B. THIS.PushButton1
        parts = text.split(".")
        if len(parts) == 1:
            self._set_name(parts[0], value, ctx)
        else:
            self._set_chain_parts(parts, value, ctx)
            
    def visitAssignStmt(self, ctx):
        value = self.visit(ctx.expr())
        pe = ctx.lvalue().postfixExpr()
        idents_u = self._lvalue_chain_from_postfix(pe, ctx)

        # ✅ WITH zuerst behandeln, bevor du returnst
        base = self.current_with_base
        if base is not None:
            # relative Zuweisung im WITH: "watch = 123" oder "a.b = 1"
            if len(idents_u) >= 1 and idents_u[0] != "THIS":
                return self.set_chain_on_object(base, idents_u, value, ctx)

        # danach normaler Assign
        if ctx.lvalue():
            self.assign_lvalue(ctx.lvalue(), value, ctx)
            return None
    
    def visitForStmt(self, ctx):
        var_name = ctx.IDENT().getText()
        start = float(ctx.numberExpr(0).getText())
        end = float(ctx.numberExpr(1).getText())

        # klassisch inklusiv (wie in vielen Basics/xBase)
        step = 1.0
        i = start
        
        # STEP optional
        if ctx.STEP() is not None:
            step = float(self.visit(ctx.numberExpr(2)))
            if step == 0:
                raise RuntimeError(f"{self.loc(ctx)}: STEP darf nicht 0 sein")
        else:
            # sinnvoller Default: Richtung automatisch
            step = 1.0 if end >= start else -1.0

        def cond(x):
            return x <= end if step > 0 else x >= end

        while cond(i):
            self.set_var(var_name.upper(), i)

            try:
                # block ausführen: statement*
                for st in ctx.block().statement():
                    self.visit(st)
            except BreakSignal:
                break

            i += step

        return None
        
    def visitWriteStmt(self, ctx):
        # Im Collect-Pass nichts ausführen/ausgeben, sonst doppelte Ausgabe
        if getattr(self, "_mode", "exec") != "exec":
            return None

        parts = [self.eval_writeArg(a) for a in ctx.writeArg()]
        _emit_runtime_output_line("".join(parts))
        return None

    def eval_writeArg(self, arg_ctx):
        if arg_ctx.STRING():
            s = arg_ctx.STRING().getText()
            return s[1:-1]

        if arg_ctx.dottedRef():
            val = self.visit(arg_ctx.dottedRef())
            return "" if val is None else self._format_value(val)

        if arg_ctx.expr():
            val = self.visit(arg_ctx.expr())
            return "" if val is None else self._format_value(val)

        raise RuntimeError("writeArg enthält weder STRING noch dottedRef noch expr")

    def visitDottedRef(self, ctx):
        # dottedRef : (THIS | IDENT) (DOT IDENT)+ ;
        idents = [t.getText() for t in ctx.IDENT()]

        if ctx.THIS() is not None:
            head = "THIS"
        else:
            head = idents[0]  # erster IDENT ist der Kopf

        # ✅ Startobjekt über _get_name holen (kennt WITH + Variablen)
        if head.upper() == "THIS":
            cur = self.get_var("THIS", ctx)
            tail = idents
        else:
            cur = self._get_name(head)      # <-- wichtig!
            tail = idents[1:]               # Rest nach dem Kopf

        # Restliche Member auflösen
        for name in tail:
            cur = self.get_member(cur, name, ctx)

        return cur

        
    def _format_value(self, val):
        # optional hübscher: 3.0 -> "3"
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        if isinstance(val, Instance):
            return repr(val)
        if isinstance(val, Delegate):
            return repr(val)
        return str(val)

    def visitIfStmt(self, ctx):
        cond_val = self.visit(ctx.expr())
        cond_true = (cond_val != 0)

        blocks = ctx.block()
        then_block = blocks[0]
        else_block = blocks[1] if len(blocks) > 1 else None

        if cond_true:
            self.visit(then_block)
        elif else_block is not None:
            self.visit(else_block)

        return None

    def visitBlock(self, ctx):
        for st in ctx.statement():
            self.visit(st)
        return None

    # ---------- Expression Evaluation ----------
    def visitAddExpr(self, ctx):
        value = self.visit(ctx.mulExpr(0))
        for i in range(1, len(ctx.mulExpr())):
            op = ctx.getChild(2*i-1).getText()
            rhs = self.visit(ctx.mulExpr(i))
            value = value + rhs if op == '+' else value - rhs
        return value

    def visitMulExpr(self, ctx):
        value = self.visit(ctx.unaryExpr(0))
        for i in range(1, len(ctx.unaryExpr())):
            op = ctx.getChild(2*i-1).getText()
            rhs = self.visit(ctx.unaryExpr(i))
            value = value * rhs if op == '*' else value / rhs
        return value

    def visitUnaryExpr(self, ctx):
        if ctx.getChildCount() == 2:
            op = ctx.getChild(0).getText()
            val = self.visit(ctx.unaryExpr(0))
            return +val if op == '+' else -val
        return self.visit(ctx.primary())

    def visitLiteral(self, ctx):
        if ctx.TRUE():
            return True
        if ctx.FALSE():
            return False
        if ctx.NUMBER():
            return float(ctx.NUMBER().getText())
        if ctx.STRING():
            s = ctx.STRING().getText()
            return s[1:-1] if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'") else s
        raise Exception(f"{ctx.start.line}:{ctx.start.column}: Unbekanntes literal")

    def visitPrimary(self, ctx):
        if hasattr(ctx, "handlerList") and ctx.handlerList():
            return self.visit(ctx.handlerList())
            
        if ctx.literal():
            return self.visit(ctx.literal())
            
        if ctx.newExpr():
            return self.visit(ctx.newExpr())

        if ctx.memberExpr():
            return self.visit(ctx.memberExpr())
        
        if ctx.THIS():
            return self.get_var("THIS", ctx)
        
        if ctx.SUPER():
            return "SUPER"
            
        if ctx.FLOAT():
            return float(ctx.FLOAT().getText())

        if ctx.NUMBER():
            return float(ctx.NUMBER().getText())

        if ctx.STRING():
            s = ctx.STRING().getText()
            return s[1:-1] if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'") else s

        if ctx.IDENT():
            name = ctx.IDENT().getSymbol().text  # Token-Text
            return self._get_name(name)       # <-- HIER ist der Lookup!
        
        if getattr(ctx, "BRACKET_STRING", None) and ctx.BRACKET_STRING():
            return self._unescape_bracket_string(ctx.BRACKET_STRING().getText())
            
        # ( expr )
        if ctx.expr():
            return self.visit(ctx.expr())
        
        raise Exception(f"{ctx.start.line}:{ctx.start.column}: Unbekanntes primary")
    
    def visitExprStmt(self, ctx):
        # expr ausführen, Ergebnis ignorieren
        # Parser-Recovery kann Teile eines CLASS-Headers als nackte exprStmt liefern
        # (z.B. "ParentForm" oder native Basen wie "FORM"). Diese sollen im
        # Exec-Pass keine Laufzeitwirkung haben.
        try:
            pe = ctx.postfixExpr()
            txt = pe.getText() if pe is not None else ""
            up = txt.upper()
            if up in self.classes or up in NATIVE_BASES:
                return None
        except Exception:
            pass

        self.visit(ctx.postfixExpr())
        return None

    def _get_name(self, name: str):
        key = name.upper()

        # 1) normale Variablen (aus _scopes!)
        try:
            return self.get_var(key, None)
        except Exception:
            pass

        # 2) WITH-Kontext: als Property des aktuellen WITH-Objekts behandeln
        if self.with_stack:
            base = self.with_stack[-1]
            if isinstance(base, Instance):
                if key in base.props:
                    return base.props[key]
                try:
                    return self.get_member(base, key, None)
                except Exception:
                    raise RuntimeError(f"Unbekanntes WITH-Property '{name}'")
            if isinstance(base, dict):
                # case-insensitive
                for k, v in base.items():
                    if k.upper() == key:
                        return v
                raise RuntimeError(f"Unbekanntes WITH-Property '{name}'")

        # 3) Aktiver Arbeitsbereich: EOF / Feldnamen
        try:
            ws = self._current_workarea()
            if key == 'EOF':
                return bool(ws.get('eof', True))
            if key == 'RECNO':
                return int(ws.get('pointer', 1) or 1)

            rec = self._current_record()
            if rec is not None:
                if key == 'DELETED':
                    return bool(rec.get('__deleted__'))
                if key in rec:
                    return rec[key]

            # Feldnamen auch dann erkennen, wenn aktuell kein gültiger Datensatz
            # im Zugriff ist (z.B. EOF/leer/pointer außerhalb). In diesem Fall
            # liefern wir einen leeren Wert statt "Unbekannter Name".
            fields = list(ws.get('fields', []) or [])
            for spec in fields:
                try:
                    if str(getattr(spec, 'name', '') or '').upper() == key:
                        return '' if rec is None else rec.get(key, '')
                except Exception:
                    continue
        except Exception:
            pass

        # 4) Klassenname oder native Basisklasse als Symbol tolerieren.
        # Das verhindert, dass versehentlich im Exec-Pass ankommende Teile eines
        # CLASS-Headers (z.B. "ParentForm" oder "FORM") als unbekannter
        # Variablenname abstürzen. Für NEW <Class>(...) wird dieser Pfad nicht
        # benutzt, daher ist das hier nur ein harmloser Fallback.
        if key in self.classes:
            return key
        if key in NATIVE_BASES:
            return key

        # 4) nicht gefunden
        raise RuntimeError(f"Unbekannter Name '{name}'")


    def _set_name(self, name: str, value, ctx=None):
        key = name.upper()

        # 1) wenn Variable irgendwo existiert -> updaten (in _scopes)
        for s in reversed(self._scopes):
            if key in s:
                s[key] = value
                return

        # 2) WITH aktiv? -> Property setzen
        if self.with_stack:
            base = self.with_stack[-1]
            if isinstance(base, Instance):
                base.props[key] = value
                self.set_prop(base, key, value, ctx)
                return
            if isinstance(base, dict):
                # vorhandenen key (case-insensitiv) treffen oder neu anlegen
                for k in list(base.keys()):
                    if k.upper() == key:
                        base[k] = value
                        return
                base[name] = value
                return

        # 3) sonst: neue Variable im aktuellen Scope anlegen
        self._scopes[-1][key] = value

    def visitWithStmt(self, ctx):
        # WITH ( withTarget ) withBody ENDWITH
        obj = self.visit(ctx.withTarget())
        
        if obj is None:
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: WITH target ist None")
        
        owner = None
        if isinstance(obj, FontValue) and self.with_stack and isinstance(self.with_stack[-1], Instance):
            owner = self.with_stack[-1]
        
        self.with_stack.append(obj)
        self.with_stack_owner.append(owner)
        try:
            self.visit(ctx.withBody())
        finally:
            self.with_stack_owner.pop()
            self.with_stack.pop()
        
        return None

    def set_child(self, owner: Instance, name: str, child: Instance):
        owner.children[name.upper()] = child
        owner.props[name.upper()] = child  # damit THIS.PushButton1 als Property funktioniert

    def visitWithTarget(self, ctx):
        # withTarget
        #   : THIS
        #   | dottedRef
        #   | IDENT
        #   | postfixExpr
        #   ;

        if ctx.THIS():
            if ctx.THIS():
                return self.get_var("THIS", ctx)   # oder self.cur_this() wenn du das nutzt

        if ctx.dottedRef():
            return self.visit(ctx.dottedRef())

        if ctx.IDENT():
            # Variable/Objektname (case-insensitiv handled by _get_name)
            return self._get_name(ctx.IDENT().getText())

        if ctx.postfixExpr():
            return self.visit(ctx.postfixExpr())

        return None

    def visitCompareExpr(self, ctx):
        left = self.visit(ctx.addExpr(0))

        # kein Vergleich, nur Zahl -> direkt zurück
        if ctx.getChildCount() == 1:
            return left

        op = ctx.getChild(1).getText()
        right = self.visit(ctx.addExpr(1))

        if op == "==": return 1 if left == right else 0
        if op == "!=": return 1 if left != right else 0
        if op == "<":  return 1 if left <  right else 0
        if op == "<=": return 1 if left <= right else 0
        if op == ">":  return 1 if left >  right else 0
        if op == ">=": return 1 if left >= right else 0

        raise ValueError(f"Unknown comparison operator: {op}")

    # ---------- Helpers ----------
    def _unescape_string(self, raw: str) -> str:
        quote = raw[0]
        s     = raw[1:-1]  # äußere Quotes weg
        out   = []
        i     = 0
        while i < len(s):
            if s[i] == '\\' and i + 1 < len(s):
                c = s[i+1]
                if c == 'n':
                    out.append('\n')
                elif c == 't':
                    out.append('\t')
                elif c == '\\':
                    out.append('\\')
                elif c == '"':
                    out.append('"')
                elif c == "'":
                    out.append("'")
                else:
                    out.append(c)
                i += 2
            else:
                out.append(s[i])
                i += 1
        return ''.join(out)
        
    def _unescape_bracket_string(self, tok_text: str) -> str:
        # tok_text enthält inklusive [ ... ]
        s = tok_text[1:-1]           # äußere Klammern weg
        s = s.replace("]]", "]")     # Escape wieder zurück
        return s
        
    def visitClassBody(self, ctx):
        # NUR member besuchen
        for m in ctx.classMember():
            self.visit(m)
        return None

    def _methoddef_from_methoddecl(self, decl_ctx):
        # 1) Parameterliste finden
        params = []

        # Häufig: decl_ctx.paramList() -> hat IDENT()
        if hasattr(decl_ctx, "paramList") and decl_ctx.paramList() is not None:
            pl = decl_ctx.paramList()
            if hasattr(pl, "IDENT"):
                params = [t.getText() for t in pl.IDENT()]

        # Alternativ: decl_ctx.IDENT() enthält [methodName, p1, p2, ...]
        if not params and hasattr(decl_ctx, "IDENT"):
            idents = [t.getText() for t in decl_ctx.IDENT()]
            if len(idents) >= 2:
                params = idents[1:]  # erstes ist meist der Methodenname

        # 2) Block/Body finden (je nach Grammar-Namen)
        block_ctx = None
        for cand in ("block", "stmtBlock", "compoundStmt", "methodBlock"):
            if hasattr(decl_ctx, cand):
                fn = getattr(decl_ctx, cand)
                try:
                    tmp = fn()
                except TypeError:
                    tmp = None
                if tmp is not None:
                    block_ctx = tmp
                    break

        # Wenn nix gefunden: nimm notfalls den decl_ctx selbst (und visit() muss damit klarkommen)
        if block_ctx is None:
            block_ctx = decl_ctx

        return MethodDef(params=params, block_ctx=block_ctx)

    def _get_method_params(self, method_ctx):
        if isinstance(method_ctx, MethodDef):
            return list(method_ctx.params or [])

        # method_ctx ist MethodDeclContext
        pl = method_ctx.paramList()
        if not pl:
            return []

        # Häufige Fälle:
        # 1) paramList : IDENT (',' IDENT)* ;
        if hasattr(pl, "IDENT"):
            toks = pl.IDENT()
            if toks:
                if isinstance(toks, list):
                    return [t.getText() for t in toks]
                return [toks.getText()]

        # 2) paramList : identifier (',' identifier)* ;
        if hasattr(pl, "identifier"):
            ids = pl.identifier()
            if ids:
                if isinstance(ids, list):
                    return [x.getText() for x in ids]
                return [ids.getText()]

        # Fallback (zur Not): Text parsen
        txt = pl.getText()  # z.B. "a,c" oder "a,c,d"
        return [p.strip() for p in txt.split(",") if p.strip()]
        
    def invoke_method(self, target, method_name: str, args: list, ctx):
        mname = method_name.upper()

        # Native OPEN
        if mname == "OPEN" and self.is_descendant_of(target.class_name.upper(), "FORM"):
            return form_open(target)

        # resolve_method liefert (owner_class, method_ctx)
        owner_class, mctx = self.resolve_method(target.class_name, mname, ctx)

        self.push_this(target)
        self.push_scope()
        try:
            self._scopes[-1]["THIS"] = target
            self._scopes[-1]["SELF"] = target

            # ✅ Parameter binden (DAS fehlt!)
            params = self._get_method_params(mctx)
            for i, pname in enumerate(params):
                self.set_var(pname, args[i] if i < len(args) else None)

            try:
                block_ctx = mctx.block_ctx if isinstance(mctx, MethodDef) else mctx.block()
                self.visit(block_ctx)
                return None
            except ReturnSignal as rs:
                return rs.value

        finally:
            self.pop_scope()
            self.pop_this()
        
    # für Events ... -> FireClick(button)
    def invoke_delegate(self, d: Delegate, args: list, ctx):
        res = self.resolve_method(d.target.class_name.upper(), d.method_name, ctx)
        owner_class, method_ctx = res
        return self.execute_method(owner_class, method_ctx, args, this_obj=d.target)

    def visitCondition(self, ctx):
        return self.visit(ctx.logicalOr())

    def _strip_program_target(self, target: str) -> str:
        s = (target or "").strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()

    def _do_program_extensions(self) -> list[str]:
        return [".prg", ".wfm", ".frm"]

    def _iter_program_candidates(self, target: str):
        s = self._strip_program_target(target)
        if not s:
            return []
        if s.upper().startswith("PROGRAM "):
            s = s.split(None, 1)[1].strip()

        root, ext = os.path.splitext(s)
        names = [s] if ext else [s + ex for ex in self._do_program_extensions()]

        candidates = []
        cur = getattr(self, "_current_filename", "") or ""
        if cur:
            base_dir = os.path.dirname(os.path.abspath(cur))
            for name in names:
                candidates.append(os.path.join(base_dir, name))
        for name in names:
            candidates.append(os.path.abspath(name))
            candidates.append(os.path.join(os.getcwd(), name))

        seen = set()
        ordered = []
        for cand in candidates:
            full = os.path.abspath(cand)
            if full in seen:
                continue
            seen.add(full)
            ordered.append(full)
        return ordered

    def looks_like_program(self, target: str) -> bool:
        s = self._strip_program_target(target)
        if not s:
            return False
        if s.upper().startswith("PROGRAM "):
            return True
        _root, ext = os.path.splitext(s)
        if ext:
            return ext.lower() in tuple(self._do_program_extensions())
        # DO test: Datei zuerst versuchen
        for cand in self._iter_program_candidates(target):
            if os.path.exists(cand):
                return True
        # expliziter Pfad/quoted path ohne Extension -> ebenfalls dateiartig behandeln
        return any(sep in s for sep in ("/", "\\"))

    def try_resolve_program_path(self, target: str) -> str | None:
        for cand in self._iter_program_candidates(target):
            if os.path.exists(cand):
                return cand
        return None

    def resolve_program_path(self, target: str, ctx=None) -> str:
        path = self.try_resolve_program_path(target)
        if path:
            return path
        s = self._strip_program_target(target)
        if s.upper().startswith("PROGRAM "):
            s = s.split(None, 1)[1].strip()
        where = self.loc(ctx) if ctx is not None else "<unknown>"
        raise RuntimeError(f"{where}: DO-Datei '{s}' wurde nicht gefunden")

    def _parse_external_program(self, filename: str):
        pp = Preprocessor(include_paths=[Path("includes")])
        pre = pp.process(filename)
        if pre and not pre.endswith("\n"):
            pre += "\n"
        parser_input = _build_parser_input(pre)
        if parser_input and not parser_input.endswith("\n"):
            parser_input += "\n"
        source = InputStream(parser_input)
        lexer = dBaseLexer(source)
        tokens = CommonTokenStream(lexer)
        tokens.fill()
        parser = dBaseParser(tokens)
        listener = _attach_silent_antlr_errors(lexer, parser)
        tree = parser.input_()
        if parser.getNumberOfSyntaxErrors() > 0:
            msg = listener.messages[0] if listener.messages else "Syntaxfehler im Quelltext"
            raise RuntimeError(msg)
        return tree, pre

    def run_program(self, target: str, args: list[Any] | None = None):
        path = self.resolve_program_path(target)
        tree, pre = self._parse_external_program(path)

        old_mode = self._mode
        old_pre_source = getattr(self, "_pre_source", "")
        old_ranges = self._class_line_ranges
        old_file = getattr(self, "_current_filename", "")

        self.push_frame(os.path.basename(path), list(args or []))
        try:
            self._current_filename = path
            self._pre_source = pre
            self._class_line_ranges = None

            self._mode = "collect"
            self.visit(tree)

            self._mode = "exec"
            for it in tree.item():
                st = it.statement() if hasattr(it, "statement") else None
                if st is None:
                    continue
                if hasattr(st, "classDecl") and st.classDecl() is not None:
                    continue
                try:
                    st_line = getattr(getattr(st, "start", None), "line", 0) or 0
                except Exception:
                    st_line = 0
                if self._is_line_inside_class_block(st_line):
                    continue
                self.visit(st)
        finally:
            self.pop_frame()
            self._mode = old_mode
            self._pre_source = old_pre_source
            self._class_line_ranges = old_ranges
            self._current_filename = old_file

    def has_procedure(self, target: str) -> bool:
        name = self._strip_program_target(target).upper()
        return name in self.methods

    def call_procedure(self, target: str, args: list[Any] | None = None):
        name = self._strip_program_target(target).upper()
        mdef = self.methods.get(name)
        if mdef is None:
            raise RuntimeError(f"{self.loc(None)}: Prozedur/Methode '{name}' ist nicht definiert")

        self.push_frame(name, list(args or []))
        self.push_scope()
        try:
            params = self._get_method_params(mdef)
            for i, pname in enumerate(params):
                self.set_var(pname, args[i] if args and i < len(args) else None)
            try:
                block_ctx = mdef.block_ctx if isinstance(mdef, MethodDef) else mdef.block()
                self.visit(block_ctx)
                return None
            except ReturnSignal as rs:
                return rs.value
        finally:
            self.pop_scope()
            self.pop_frame()

    def _call_do_target_as_method(self, target: str, args: list[Any] | None, ctx=None):
        raw = self._strip_program_target(target)
        if not raw:
            return False, None

        expr = raw.strip()
        if expr.endswith('()'):
            expr = expr[:-2].strip()
        expr = re.sub(r'\s*::\s*', '.', expr)
        expr = re.sub(r'\s*\.\s*', '.', expr)
        parts = [p for p in expr.split('.') if p]
        if not parts:
            return False, None

        # Expliziter Methodenaufruf auf Objekt: THIS.testProcer / obj.method
        if len(parts) >= 2:
            try:
                owner = self.get_chain(parts[:-1], ctx)
            except Exception:
                owner = None
            if isinstance(owner, Instance):
                return True, self.invoke_method(owner, parts[-1], list(args or []), ctx)

        # Impliziter Methodenaufruf auf THIS: DO testProcer
        this_obj = None
        try:
            this_obj = self.this_obj or self.get_var("THIS", ctx)
        except Exception:
            this_obj = self.this_obj
        if isinstance(this_obj, Instance):
            mname = parts[-1].upper()
            if self.resolve_method_silent(this_obj.class_name.upper(), mname) is not None:
                return True, self.invoke_method(this_obj, mname, list(args or []), ctx)

        return False, None

    def visitDoStmt(self, ctx):
        target = ctx.doTarget().getText()
        args = []
        if ctx.argList():
            for e in ctx.argList().expr():
                args.append(self.eval_expr(e))

        # 1) Datei im Quellverzeichnis / Pfad / CWD suchen (.prg, .wfm, .frm)
        path = self.try_resolve_program_path(target)
        if path is not None:
            self.run_program(path, args)
            return None

        # 2) Objekt-/Instanzmethode: DO THIS.testProcer() / DO obj.method()
        handled, method_result = self._call_do_target_as_method(target, args, ctx)
        if handled:
            return method_result

        # 3) Falls keine Datei existiert: lokale/top-level METHOD aufrufen
        if self.has_procedure(target):
            return self.call_procedure(target, args)

        # 4) Explizite Dateiangabe mit Extension/Pfad soll einen klaren Fehler liefern
        if self.looks_like_program(target):
            self.run_program(target, args)
            return None

        # 5) Letzter Versuch: implizite Methode auf THIS auch dann noch probieren,
        #    wenn der Methodenaufruf keinen Rückgabewert liefert (None).
        handled, tried = self._call_do_target_as_method(target, args, ctx)
        if handled:
            return tried

        # 6) Sonst wie klassische Prozedur behandeln -> Fehlermeldung aus call_procedure
        return self.call_procedure(target, args)

    def visitDoCaseStmt(self, ctx):
        branches = ctx.doCaseBranch() or []
        if not isinstance(branches, list):
            branches = [branches]

        for br in branches:
            try:
                cond = self.visit(br.expr())
            except Exception:
                cond = False
            if bool(cond):
                self.visit(br.block())
                return None

        ob = ctx.doOtherwiseBranch()
        if ob is not None:
            self.visit(ob.block())
        return None

    def visitParameterStmt(self, ctx):
        names = [t.getText() for t in ctx.paramNames().IDENT()]
        incoming = self.current_frame.args if self.current_frame.args else []

        for i, name in enumerate(names):
            self.current_frame.vars[name.upper()] = incoming[i] if i < len(incoming) else None
    
    def visitReturnStmt(self, ctx):
        val = self.visit(ctx.expr()) if ctx.expr() else None
        raise ReturnSignal(val)

    def visitHandlerList(self, ctx):
        # ctx.expr() ist eine Liste: erstes expr + alle (SEMI expr)*
        items = []
        for e in ctx.expr():
            items.append(self.eval_expr(e))
        return items
        
    def is_descendant_of(self, class_name: str, base_name: str) -> bool:
        cn = class_name.upper()
        base = base_name.upper()
        while True:
            if cn == base:
                return True
            cdef = self.classes.get(cn)
            if not cdef or not cdef.parent:
                return False
            cn = cdef.parent.upper()

    def _bool_arg(self, args, idx, default=False):
        if idx >= len(args):
            return default
        v = args[idx]
        # robust: akzeptiere auch 0/1, "true"/"false"
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.strip().upper() in ("TRUE", "T", ".T.", "1", "YES", "Y")
        return default

    def fire_event(self, inst, event_name: str, qt_event=None):
        # event_name z.B. "ONMOUSEDOWN"
        handler = inst.props.get(event_name)
        if handler is None:
            return False

        # 1) Delegate-Fall (dein System)
        #    z.B. Delegate(target=thisObj, method_name="PUSHBUTTON1_ONMOUSEDOWN", runner=self)
        if isinstance(handler, Delegate):
            # Signatur: METHOD ... (Sender)   oder (Sender, Event)
            try:
                return handler.call([inst])  # minimal: Sender
            except TypeError:
                return handler.call([inst, qt_event])  # optional: Qt-Event durchreichen

        # 2) Wenn du Handler als MethodDef / Callable speicherst:
        if callable(handler):
            return handler(inst, qt_event)

        return False

    def attach_events_to_widget(self, inst):
        w = inst.backend
        if w is None:
            return

        # MouseMove kommt nur, wenn MouseTracking an ist
        if hasattr(w, "setMouseTracking"):
            w.setMouseTracking(True)

        # Focus events kommen nur, wenn das Widget Fokus bekommen darf
        # PushButton kann das, aber sicher ist sicher:
        try:
            from PyQt5.QtCore import Qt
            w.setFocusPolicy(Qt.StrongFocus)
        except Exception:
            pass

        filt = WidgetEventFilter(self, inst)
        inst._qt_event_filter = filt      # <-- Referenz halten!
        w.installEventFilter(filt)

    def call_method(self, inst: Instance, name: str, args):
        name = name.upper()

        # native OPEN
        if name == "OPEN" and self.is_descendant_of(inst.class_name.upper(), "FORM"):
            return form_open(inst)

        cdef = self.classes.get(inst.class_name.upper())
        if not cdef or name not in cdef.methods:
            raise RuntimeError(f"Methode {name} nicht gefunden")

        mctx = cdef.methods[name]

        self.push_this(inst)
        self.push_scope()
        try:
            self._scopes[-1]["THIS"] = inst
            self._scopes[-1]["SELF"] = inst

            params = self._get_method_params(mctx)
            for i, pname in enumerate(params):
                self.set_var(pname, args[i] if i < len(args) else None)

            block_ctx = mctx.block_ctx if isinstance(mctx, MethodDef) else mctx.block()
            self.visit(block_ctx)
        finally:
            self.pop_scope()
            self.pop_this()

    def visitCreateFileStmt(self, ctx):
        # Beispiel: CREATE FILE oder CREATE FILE <expr>
        path = ""
        if hasattr(ctx, "expr") and ctx.expr():
            path = str(self.eval_expr(ctx.expr()))
        
        self.open_file_editor(path=path, text="")
        return None
        
    def open_file_editor(self, path: str = "", text: str = ""):
        text = ""
        # wenn path gesetzt ist und text leer: Datei laden
        if path and text == "":
            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
            except FileNotFoundError:
                _debug_print("file not found.")
                pass
        try:
            win = FileEditorWindow(parent=MAINAPP, initial_path=path, initial_text=text)
            win.resize(600, 500)
            sub = MAINAPP.mdi.addSubWindow(win)
            
            # 1) immer sichtbar + Vordergrund
            win.show()
            win.raise_()
            win.activateWindow()

            # 2) falls minimiert: wieder herstellen
            win.setWindowState(win.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)

            # 3) optional: "Always on top"
            win.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            win.show()  # nach setWindowFlag nochmal show()!
            win.raise_()
            win.activateWindow()
            
            # Referenz halten (gegen GC)
            self._open_windows = getattr(self, "_open_windows", [])
            self._open_windows.append(win)
        except Exception as e:
            _debug_print(e)

if __name__ == "__main__":
    sys.exit(run_language_app("dbase"))
