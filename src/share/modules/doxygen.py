# ---------------------------------------------------------------------------
# File:   doxygen.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
#
# die Datei erwartet die .mo-Datei standardmäßig unter
# src/data/po/locales/<sprache>/LC_MESSAGES/doxygen.mo
# ---------------------------------------------------------------------------
from   __future__   import annotations

import os
import html

from   share.common import *

# -----------------------------------------------------------------------
# c++ documenting interpreter lexer + parser ...
# -----------------------------------------------------------------------
from parse.cc.CppDocLexer          import CppDocLexer
from parse.cc.CppDocParser         import CppDocParser
from parse.cc.CppDocParserListener import CppDocParserListener
from parse.cc.CppDocParserVisitor  import CppDocParserVisitor

# -----------------------------------------------------------------------
# pascal documenting interpreter lexer + parser ...
# -----------------------------------------------------------------------
from parse.pascal.PasDocLexer          import PasDocLexer
from parse.pascal.PasDocParser         import PasDocParser
from parse.pascal.PasDocParserListener import PasDocParserListener
from parse.pascal.PasDocParserVisitor  import PasDocParserVisitor

DOXYGEN_PROJECT_PAGES = {}
DOXYGEN_ITEMS = []

DOXYGEN_EXPERT_ITEMS = [
    "Project",
    "Build",
    "Messages",
    "Input",
    "Source Browser",
    "Index",
    "HTML",
    "LaTeX",
    "RTF",
    "Man",
    "XML",
    "DocBook",
    "AutoGen",
    "SQLite3",
    "PerlMod",
    "Preprocessor",
    "External",
    "Dot"
]

SUPPORTED_LANGUAGES = [
    "Afrikans",
    "Arabic",
    "Armeniam",
    "Brazilian",
    "Bulgarian",
    "Catalan",
    "Chinese",
    "Chinese Traditional",
    "Croatian",
    "Czech",
    "Danish",
    "Dutch",
    "English",
    "Esperanto",
    "Farsil",
    "Finnish",
    "French",
    "German",
    "Greek",
    "Hindi",
    "Hungarian",
    "Indonesian",
    "Italian",
    "Japanese",
    "Japanese-en",
    "Korean",
    "Korean-en",
    "Latvian",
    "Lithuanian",
    "Macedonian",
    "Norwegian",
    "Persian",
    "Polish",
    "Portuguese",
    "Romanian",
    "Russian",
    "Serbian",
    "Serbian-Cyrillic",
    "Slovak",
    "Slovene",
    "Spanish",
    "Swedish",
    "Turkish",
    "Ukrainian",
    "Vietnamese",
 ]

HEADER_FORMAT   = "dBase2Many Project File"
HEADER_TOOL     = "doxygen-dialog"
HEADER_KIND     = "doxygen-project"
HEADER_VERSION  = 1

# ---------------------------------------------------------------------------
# \brief global definition to write the css styles for dark mode html
# ---------------------------------------------------------------------------
def _write_css(output_dir):
    filename = os.path.join(output_dir, "style.css")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(""":root {
--bg: #1f1f1f;
--panel: #202020;
--line: #343434;
--line-soft: #2a2a2a;
--text: #eeeeee;
--muted: #b8b8b8;
--green: #36d67a;
}
* {
box-sizing: border-box;
}
body {
margin: 0;
background:
radial-gradient(circle at top left, #2b2b2b 0, #1f1f1f 360px),
var(--bg);
color: var(--text);
font-family: Arial, Helvetica, sans-serif;
font-size: 15px;
}
.page {
position: relative;
width: 100%;
padding: 18px 26px 28px 26px;
}
.version {
position: absolute;
right: 26px;
top: 20px;
color: var(--text);
font-size: 14px;
}
h1 {
margin: 0 0 8px 0;
font-size: 34px;
font-weight: 400;
letter-spacing: -0.5px;
}
h2 {
margin: 28px 0 10px 0;
font-size: 26px;
font-weight: 600;
}
.breadcrumb {
display: flex;
gap: 10px;
align-items: center;
padding-bottom: 14px;
border-bottom: 1px solid var(--line);
color: var(--green);
font-weight: 600;
}
.breadcrumb a {
color: var(--green);
text-decoration: none;
}
.breadcrumb span {
color: var(--green);
}
a {
color: #ffffff;
text-decoration: none;
}
a:visited {
color: #e6e6e6;
}
a:hover {
color: var(--green);
text-decoration: underline;
}
a:active {
color: #ffffff;
}
.inherits {
color: var(--muted);
margin: 16px 0 0 0;
}
.func-table {
width: 100%;
border-collapse: collapse;
background: rgba(32, 32, 32, 0.88);
border: 1px solid var(--line);
}
.func-table tr {
border-bottom: 1px solid var(--line-soft);
}
.func-table tr:last-child {
border-bottom: none;
}
.func-table td {
padding: 6px 12px;
vertical-align: middle;
}
.func-table .ret {
width: 245px;
color: var(--text);
text-align: right;
border-right: 1px solid var(--line);
white-space: nowrap;
}
.func-table .sig {
color: var(--text);
}
.func-name,
.linklike {
color: var(--green);
font-weight: 700;
}
.member-docs {
margin-top: 36px;
}
.member-doc {
margin-top: 28px;
max-width: 1100px;
}
.member-doc h3 {
font-size: 18px;
font-weight: 400;
margin: 0;
color: var(--text);
}
.member-line {
height: 1px;
background: var(--line);
margin: 12px 0 20px 0;
}
.member-doc p {
margin: 0 0 18px 0;
line-height: 1.55;
color: var(--text);
}
section p {
line-height: 1.55;
}
footer {
margin-top: 28px;
padding-top: 14px;
border-top: 1px solid var(--line);
color: #999999;
text-align: center;
font-size: 13px;
}
footer span {
color: var(--green);
font-weight: 700;
}
""")

def set_tooltip_if_text(widget, text):
    text = (text or "").strip()
    widget.setToolTip(text)

# ---------------------------------------------------------------------------
# \brief get the default documents home directory for the current user login
# ---------------------------------------------------------------------------
def _default_project_dir() -> Path:
    base = Path.home() / "Documents" / "dBase2Many" / "DoxygenProjects"
    base.mkdir(parents=True, exist_ok=True)
    return base


class CppClassInfo:
    def __init__(self, name):
        self.name    = name
        self.kind    = "class"
        self.bases   = []
        self.methods = []
        self.fields  = []

class CppMemberInfo:
    def __init__(self, access, signature):
        self.access    = access
        self.signature = signature


class PasClassInfo:
    def __init__(self, name):
        self.name       = name
        self.kind       = "class"
        self.bases      = []
        self.methods    = []
        self.fields     = []
        self.properties = []


class PasMemberInfo:
    def __init__(self, access, signature):
        self.access    = access
        self.signature = signature

# ---------------------------------------------------------------------------
# \brief definition to generate the html code (depend on file extension)
# ---------------------------------------------------------------------------
def generate_html(source_file, output_dir="html"):
    name, ext = os.path.splitext(source_file)
    ext       = ext[1:].lower()

    try:
        if ext in ["pas", "pp"]:
            output_dir.join("/pas")
            
            input_stream = FileStream(source_file, encoding="utf-8")
            lexer   = PasDocLexer(input_stream)
            tokens  = CommonTokenStream(lexer)
        
            parser  = PasDocParser(tokens)
            tree    = parser.unitFile()
        
            visitor = PasDocHtmlVisitor(output_dir)
            visitor.visit(tree)
            
        elif ext in ["c", "c++", "cc", "cpp"]:
            output_dir.join("/cpp")
            
            input_stream = FileStream(source_file, encoding="utf-8")
            lexer   = CppDocLexer(input_stream)
            tokens  = CommonTokenStream(lexer)
        
            parser  = CppDocParser(tokens)
            tree    = parser.translationUnit()
        
            visitor = CppDocHtmlVisitor(output_dir)
            visitor.visit(tree)
            
    except Exception as e:
        print(e)
    
    print(f"HTML-Dokumentation erstellt in: {output_dir}")

# ---------------------------------------------------------------------------
# \brief pascal documentation visitor to generate the pascal html help ...
# ---------------------------------------------------------------------------
class PasDocHtmlVisitor(PasDocParserVisitor):
    def __init__(self, output_dir = "html" ):
        super().__init__()
        
        self.output_dir     = output_dir
        self.classes        = []

        self.current_class  = None
        self.current_access = "public"
    
    def visitUnitFile(self, ctx: PasDocParser.UnitFileContext):
        self.visitChildren(ctx)
        self.write_index()
        self.write_classes()
        return self.classes
    
    def visitClassDeclaration(self, ctx: PasDocParser.ClassDeclarationContext):
        class_name = ctx.IDENT().getText()
        
        old_class  = self.current_class
        old_access = self.current_access
        
        info       = PasClassInfo(class_name)
        info.kind  = "class"
        
        class_type = ctx.classType()
        
        if class_type and class_type.classInheritance():
            for t in class_type.classInheritance().typeName():
                info.bases.append(self.text_from_ctx(t))
        
        self.current_class  = info
        self.current_access = "public"

        self.visit(class_type.classBody())
        self.classes.append(info)
        
        self.current_class  = old_class
        self.current_access = old_access
        
        return info
    
    def visitVisibilitySection(self, ctx: PasDocParser.VisibilitySectionContext):
        self.current_access = ctx.visibility().getText().lower()
        return None
    
    def visitMethodDeclaration(self, ctx: PasDocParser.MethodDeclarationContext):
        if self.current_class is None:
            return None
        signature = self.text_from_ctx(ctx)
        self.current_class.methods.append(PasMemberInfo(self.current_access, signature))
        return None
    
    def visitPropertyDeclaration(self, ctx: PasDocParser.PropertyDeclarationContext):
        if self.current_class is None:
            return None
        signature = self.text_from_ctx(ctx)
        self.current_class.properties.append(PasMemberInfo(self.current_access, signature))
        return None
    
    def visitFieldDeclaration(self, ctx: PasDocParser.FieldDeclarationContext):
        if self.current_class is None:
            return None
        signature = self.text_from_ctx(ctx)
        self.current_class.fields.append(PasMemberInfo(self.current_access, signature))

    def text_from_ctx(self, ctx):
        tokens = []
        for child in ctx.getChildren():
            if hasattr(child, "symbol"):
                tokens.append(child.getText())
            else:
                sub_text = self.text_from_ctx(child)
                if sub_text:
                    tokens.extend(sub_text.split(" "))
        return self.join_pascal_tokens(tokens)
    
    def join_pascal_tokens(self, tokens):
        result = ""
        no_space_before = { ")", "]", ",", ".", ":" }
        no_space_after  = { "(", "[", ".", "^"      }

        for token in tokens:
            if not token:
                continue
            if not result:
                result = token
                continue
            prev = result[-1]
            if token in no_space_before:
                result += token
            elif prev in "([.^":
                result += token
            else:
                result += " " + token
        result = result.strip()
        
        if result.endswith(";"):
            result = result[:-1].strip()
        
        return result
    
    def html_escape(self, text):
        return html.escape(text, quote=True)
    
    def safe_filename(self, name):
        result = []
        for ch in name:
            if ch.isalnum() or ch in "_-":
                result.append(ch)
            else:
                result.append("_")
        return "".join(result)
    
    def write_index(self):
        filename = os.path.join(self.output_dir, "pascal\\index.html")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write("  <meta charset=\"utf-8\">\n")
            f.write("  <title>Pascal Documentation</title>\n")
            f.write("  <link rel=\"stylesheet\" href=\"style.css\">\n")
            f.write("</head>\n")
            f.write("<body>\n")
            f.write("  <main class=\"page\">\n")
            f.write("    <div class=\"version\">Pascal Doc</div>\n")
            f.write("    <h1>Pascal Documentation</h1>\n")
            f.write("    <div class=\"breadcrumb\">\n")
            f.write("      <span>Overview</span>\n")
            f.write("    </div>\n")
            f.write("    <section>\n")
            f.write("      <h2>Classes</h2>\n")
            f.write("      <ul class=\"class-list\">\n")
            
            for cls in self.classes:
                html_name = self.safe_filename(cls.name) + ".html"
                f.write(
                    f"        <li><a href=\"{html_name}\">{self.html_escape(cls.name)}</a></li>\n"
                )
            
            f.write("      </ul>\n")
            f.write("    </section>\n")
            f.write("    <footer>\n")
            f.write("      Generated by <span>dBase Lexer + Parser</span> | Pascal Documentation Generator\n")
            f.write("    </footer>\n")
            f.write("  </main>\n")
            f.write("</body>\n")
            f.write("</html>\n")
        
        _write_css(os.path.join(self.output_dir, "pascal"))
    
    def write_classes(self):
        os.makedirs(os.path.join(self.output_dir, "pascal" ), exist_ok=True)
        for cls in self.classes:
            filename = os.path.join(
                self.output_dir, "pascal",
                self.safe_filename(cls.name) + ".html")
            with open(filename, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html>\n")
                f.write("<html>\n")
                f.write("<head>\n")
                f.write("  <meta charset=\"utf-8\">\n")
                f.write(f"  <title>{self.html_escape(cls.name)} Class</title>\n")
                f.write("  <link rel=\"stylesheet\" href=\"style.css\">\n")
                f.write("</head>\n")
                f.write("<body>\n")
                
                f.write("  <main class=\"page\">\n")
                f.write("    <div class=\"version\">Pascal Doc</div>\n")
                f.write(f"    <h1>{self.html_escape(cls.name)} Class</h1>\n")
                
                f.write("    <div class=\"breadcrumb\">\n")
                f.write("      <a href=\"index.html\">Overview</a>\n")
                f.write("      <span>›</span>\n")
                f.write(f"      <span>{self.html_escape(cls.name)}</span>\n")
                f.write("    </div>\n")
                
                if cls.bases:
                    f.write("    <p class=\"inherits\">Inherits: ")
                    f.write(", ".join(self.html_escape(b) for b in cls.bases))
                    f.write("</p>\n")
                
                self.write_member_table(f, "Public Methods", cls.methods, "public")
                self.write_member_table(f, "Protected Methods", cls.methods, "protected")
                self.write_member_table(f, "Private Methods", cls.methods, "private")
                self.write_member_table(f, "Published Methods", cls.methods, "published")
                
                self.write_member_table(f, "Public Properties", cls.properties, "public")
                self.write_member_table(f, "Protected Properties", cls.properties, "protected")
                self.write_member_table(f, "Private Properties", cls.properties, "private")
                self.write_member_table(f, "Published Properties", cls.properties, "published")
                
                self.write_member_table(f, "Public Fields", cls.fields, "public")
                self.write_member_table(f, "Protected Fields", cls.fields, "protected")
                self.write_member_table(f, "Private Fields", cls.fields, "private")
                self.write_member_table(f, "Published Fields", cls.fields, "published")
                
                f.write("    <section>\n")
                f.write("      <h2>Detailed Description</h2>\n")
                f.write(f"      <p>The <span class=\"linklike\">{self.html_escape(cls.name)}</span> class.</p>\n")
                f.write("    </section>\n")
                
                self.write_member_function_docs(f, cls)
                
                f.write("    <footer>\n")
                f.write("      Generated by <span>dBase Lexer + Parser</span> | Pascal Documentation Generator\n")
                f.write("    </footer>\n")
                
                f.write("  </main>\n")
                f.write("</body>\n")
                f.write("</html>\n")
    
    def write_member_table(self, f, title, members, access_filter=None):
        items = []
        
        for member in members:
            if access_filter is None or member.access == access_filter:
                items.append(member)
        
        if not items:
            return
        
        f.write("    <section>\n")
        f.write(f"      <h2>{self.html_escape(title)}</h2>\n")
        f.write("      <table class=\"func-table\">\n")
        
        for member in items:
            left, right = self.split_pascal_signature(member.signature)
            
            f.write("        <tr>\n")
            f.write(f"          <td class=\"ret\">{self.html_escape(left)}</td>\n")
            f.write(f"          <td class=\"sig\">{self.highlight_signature(right)}</td>\n")
            f.write("        </tr>\n")
        
        f.write("      </table>\n")
        f.write("    </section>\n")

    def split_pascal_signature(self, signature):
        text = signature.strip()
        if text.lower().startswith("property "):
            body = text[len("property "):].strip()
            return "property", body
        lower_text = text.lower()
        for prefix in ["constructor", "destructor", "procedure", "function"]:
            if lower_text.startswith(prefix + " "):
                body = text[len(prefix):].strip()
                return prefix, body
        if ":" in text:
            left, right = text.split(":", 1)
            return right.strip(), left.strip()
        parts = text.rsplit(" ", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return "", text

    def highlight_signature(self, signature):
        text = self.html_escape(signature)
        pos = text.find("(")
        colon_pos = text.find(":")
        end_pos = -1
        if pos >= 0 and colon_pos >= 0:
            end_pos = min(pos, colon_pos)
        elif pos >= 0:
            end_pos = pos
        elif colon_pos >= 0:
            end_pos = colon_pos
        if end_pos > 0:
            name = text[:end_pos]
            rest = text[end_pos:]
            return f"<span class=\"func-name\">{name}</span>{rest}"
        parts = text.split(" ", 1)
        if len(parts) == 2:
            return f"<span class=\"func-name\">{parts[0]}</span> {parts[1]}"
        return f"<span class=\"func-name\">{text}</span>"

    def write_member_function_docs(self, f, cls):
        if not cls.methods:
            return
        
        f.write("    <section class=\"member-docs\">\n")
        f.write("      <h2>Member Function Documentation</h2>\n")
        
        msg = share.locales.tr("No documentation for this member")
        for member in cls.methods:
            full_signature = self.make_qualified_signature(cls.name, member.signature)
            
            f.write("      <article class=\"member-doc\">\n")
            f.write(f"        <h3>{self.highlight_signature(full_signature)}</h3>\n")
            f.write("        <div class=\"member-line\"></div>\n")
            f.write("        <p>\n")
            f.write(f"          {msg}.\n")
            f.write("        </p>\n")
            f.write("      </article>\n")
        
        f.write("    </section>\n")

    def make_qualified_signature(self, class_name, signature):
        text = signature.strip()
        lower_text = text.lower()
        for prefix in ["constructor", "destructor", "procedure", "function"]:
            if lower_text.startswith(prefix + " "):
                body      = text[len(prefix):].strip()
                pos       = body.find("(")
                colon_pos = body.find(":")
                if pos >= 0 and colon_pos >= 0:
                    end_pos = min(pos, colon_pos)
                elif pos >= 0:
                    end_pos = pos
                elif colon_pos >= 0:
                    end_pos = colon_pos
                else:
                    end_pos = len(body)
                name = body[:end_pos].strip()
                rest = body[end_pos:].strip()
                return f"{prefix} {class_name}.{name}{rest}"
        return text

# ---------------------------------------------------------------------------
# \brief c++ documentation visitor to generate the c++ html help ...
# ---------------------------------------------------------------------------
class CppDocHtmlVisitor(CppDocParserVisitor):
    def __init__(self, output_dir="html"):
        super().__init__()
        
        self.output_dir = output_dir
        self.classes = []
        self.current_class = None
        self.current_access = "private"
    
    def visitTranslationUnit(self, ctx: CppDocParser.TranslationUnitContext):
        self.visitChildren(ctx)
        self.write_index()
        self.write_classes()
        return self.classes
    
    def visitClassDeclaration(self, ctx: CppDocParser.ClassDeclarationContext):
        class_name = ctx.IDENT().getText()
        
        old_class  = self.current_class
        old_access = self.current_access
        
        info = CppClassInfo(class_name)
        info.kind = ctx.classKind().getText()

        if info.kind == "struct":
            self.current_access = "public"
        else:
            self.current_access = "private"

        if ctx.inheritance():
            for item in ctx.inheritance().inheritanceItem():
                info.bases.append(self.text_from_ctx(item))

        self.current_class = info
        self.visit(ctx.classBody())
        self.classes.append(info)

        self.current_class  = old_class
        self.current_access = old_access

        return info

    def visitAccessSection(self, ctx: CppDocParser.AccessSectionContext):
        self.current_access = ctx.accessSpecifier().getText()
        return None

    def visitMethodDeclaration(self, ctx: CppDocParser.MethodDeclarationContext):
        if self.current_class is None:
            return None

        signature = self.text_from_ctx(ctx)

        self.current_class.methods.append(
            CppMemberInfo(self.current_access, signature)
        )

        return None

    def visitFieldDeclaration(self, ctx: CppDocParser.FieldDeclarationContext):
        if self.current_class is None:
            return None

        signature = self.text_from_ctx(ctx)

        self.current_class.fields.append(
            CppMemberInfo(self.current_access, signature)
        )

        return None

    def format_signature(self, text):
        text = text.replace(";", "")
        text = text.replace(",", ", ")
        text = text.replace("(", "(")
        text = text.replace(")", ")")
        text = text.replace("*", " *")
        text = text.replace("&", " &")
        return text.strip()
    
    def text_from_ctx(self, ctx):
        tokens = []
        for child in ctx.getChildren():
            if hasattr(child, "symbol"):
                tokens.append(child.getText())
            else:
                sub_text = self.text_from_ctx(child)
                if sub_text:
                    tokens.extend(sub_text.split(" "))
        return self.join_cpp_tokens(tokens)

    def join_cpp_tokens(self, tokens):
        result = ""
        no_space_before = { ")", "]", "}", ";", ",", "::" }
        no_space_after  = { "(", "[", "{", "::", "~"      }
        
        space_around    = { "*", "&", "=", "+", "-", "/", "%", "<", ">" }

        for token in tokens:
            if not token:
                continue
            if not result:
                result = token
                continue
            prev = result[-1]
            if token in no_space_before:
                result += token
            elif prev in "([{~":
                result += token
            elif token in space_around:
                result += " " + token
            elif prev in "*&=+-/%<>":
                result += " " + token
            else:
                result += " " + token
        return result.strip()
    
    def pretty_cpp_text(self, text):
        text = text.strip()
        
        text = text.replace(" *", " *")
        text = text.replace("* ", "* ")
        text = text.replace(" &", " &")
        text = text.replace("& ", "& ")

        text = text.replace(" (", "(")
        text = text.replace("( ", "(")
        text = text.replace(" )", ")")
        text = text.replace(" ,", ",")
        text = text.replace(", ", ", ")

        text = text.replace(" ;", "")

        while "  " in text:
            text = text.replace("  ", " ")

        return text
    
    def safe_filename(self, name):
        result = []

        for ch in name:
            if ch.isalnum() or ch in "_-":
                result.append(ch)
            else:
                result.append("_")

        return "".join(result)

    def html_escape(self, text):
        return html.escape(text, quote=True)

    def write_index(self):
        os.makedirs(os.path.join(self.output_dir, "cpp"), exist_ok=True)
        filename  = os.path.join(self.output_dir, "cpp\\index.html")

        with open(filename, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write("  <meta charset=\"utf-8\">\n")
            f.write("  <title>C++ Documentation</title>\n")
            f.write("  <link rel=\"stylesheet\" href=\"style.css\">\n")
            f.write("</head>\n")
            f.write("<body>\n")
            f.write("  <h1>C++ Documentation</h1>\n")
            f.write("  <h2>Classes</h2>\n")
            f.write("  <ul>\n")

            for cls in self.classes:
                html_name = self.safe_filename(cls.name) + ".html"
                f.write(
                    f"    <li><a href=\"{html_name}\">{self.html_escape(cls.name)}</a></li>\n"
                )

            f.write("  </ul>\n")
            f.write("</body>\n")
            f.write("</html>\n")

        _write_css(os.path.join(self.output_dir, "cpp"))

    def write_classes(self):
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "cpp" ), exist_ok=True)
        for cls in self.classes:
            filename = os.path.join(
                self.output_dir, "cpp",
                self.safe_filename(cls.name) + ".html")
            with open(filename, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html>\n<html>\n<head>\n")
                f.write("  <meta charset=\"utf-8\">\n")
                f.write(f"  <title>{self.html_escape(cls.name)} Class</title>\n")
                f.write("  <link rel=\"stylesheet\" href=\"style.css\">\n")
                f.write("</head>\n<body>\n")

                f.write("  <main class=\"page\">\n")
                f.write(f"    <div class=\"version\">C++ Doc</div>\n")
                f.write(f"    <h1>{self.html_escape(cls.name)} Class</h1>\n")

                f.write("    <div class=\"breadcrumb\">\n")
                f.write("      <a href=\"index.html\">Overview</a>")
                f.write("      <span>›</span>")
                f.write(f"      <span>{self.html_escape(cls.name)}</span>\n")
                f.write("    </div>\n")

                if cls.bases:
                    f.write("    <p class=\"inherits\">Inherits: ")
                    f.write(", ".join(self.html_escape(b) for b in cls.bases))
                    f.write("</p>\n")

                self.write_member_table(f, "Public Functions", cls.methods, "public")
                self.write_member_table(f, "Protected Functions", cls.methods, "protected")
                self.write_member_table(f, "Private Functions", cls.methods, "private")

                self.write_member_table(f, "Public Fields", cls.fields, "public")
                self.write_member_table(f, "Protected Fields", cls.fields, "protected")
                self.write_member_table(f, "Private Fields", cls.fields, "private")
                
                
                f.write("    <section>\n")
                f.write("      <h2>Detailed Description</h2>\n")
                f.write(f"      <p>The <span class=\"linklike\">{self.html_escape(cls.name)}</span> class.</p>\n")
                f.write("    </section>\n")
                
                self.write_member_function_docs(f, cls)
                
                f.write("    <footer>\n")
                f.write("      Generated by <span>dBase Lexer + Parser</span> | C++ Documentation Generator\n")
                f.write("    </footer>\n")

                f.write("  </main>\n")
                f.write("</body>\n</html>\n")

    def write_member_function_docs(self, f, cls):
        if not cls.methods:
            return

        f.write("    <section class=\"member-docs\">\n")
        f.write("      <h2>Member Function Documentation</h2>\n")

        msg = share.locales.tr("No documentation for this member")
        for member in cls.methods:
            full_signature = self.make_qualified_signature(cls.name, member.signature)

            f.write("      <article class=\"member-doc\">\n")
            f.write(f"        <h3>{self.highlight_signature(full_signature)}</h3>\n")
            f.write("        <div class=\"member-line\"></div>\n")

            f.write("        <p>\n")
            f.write(f"          {msg}.\n")
            f.write("        </p>\n")

            f.write("      </article>\n")

        f.write("    </section>\n")


    def make_qualified_signature(self, class_name, signature):
        text = signature.strip()

        pos = text.find("(")
        if pos <= 0:
            return text

        before = text[:pos].strip()
        rest = text[pos:].strip()

        parts = before.rsplit(" ", 1)

        if len(parts) == 2:
            left = parts[0]
            name = parts[1]

            if name.startswith("~"):
                return f"{left} {class_name}::{name}{rest}"

            if name == class_name:
                return f"{class_name}::{name}{rest}"

            return f"{left} {class_name}::{name}{rest}"

        name = before

        if name.startswith("~"):
            return f"{class_name}::{name}{rest}"

        return f"{class_name}::{name}{rest}"
    
    def write_member_table(self, f, title, members, access_filter=None):
        items = []

        for member in members:
            if access_filter is None or member.access == access_filter:
                items.append(member)

        if not items:
            return

        f.write("    <section>\n")
        f.write(f"      <h2>{self.html_escape(title)}</h2>\n")
        f.write("      <table class=\"func-table\">\n")

        for member in items:
            left, right = self.split_signature(member.signature)

            f.write("        <tr>\n")
            f.write(f"          <td class=\"ret\">{self.html_escape(left)}</td>\n")
            f.write(f"          <td class=\"sig\">{self.highlight_signature(right)}</td>\n")
            f.write("        </tr>\n")

        f.write("      </table>\n")
        f.write("    </section>\n")

    def split_signature(self, signature):
        text = self.pretty_cpp_text(signature)
        pos  = text.find("(")
        if pos > 0:
            before = text[:pos].strip()
            rest = text[pos:].strip()
            parts = before.rsplit(" ", 1)
            if len(parts) == 2:
                return parts[0], parts[1] + rest
            return "", text
        parts = text.rsplit(" ", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return "", text

    def highlight_signature(self, signature):
        text = self.html_escape(signature)

        pos = text.find("(")
        if pos > 0:
            name = text[:pos]
            rest = text[pos:]
            return f"<span class=\"func-name\">{name}</span>{rest}"

        return f"<span class=\"func-name\">{text}</span>"


class DoxyScrollPage:
    def __init__(self, owner, area, widget, layout):
        self.owner = owner
        self.area = area
        self.widget = widget
        self.layout = layout


class ProjectListItemWidget(QWidget):
    def __init__(self, filename: str, dt_text: str, parent=None):
        super().__init__(parent)
        
        lay = QVBoxLayout(self)
        lay.setContentsMargins(6, 4, 6, 4)
        lay.setSpacing(0)

        self.lbl_name = QLabel(filename)
        self.lbl_name.setStyleSheet("QLabel { font: 10pt Arial; color: white; }")
        lay.addWidget(self.lbl_name)

        self.lbl_dt = QLabel(dt_text)
        self.lbl_dt.setStyleSheet("QLabel { font: 8pt Arial; color: #c0c0c0; }")
        lay.addWidget(self.lbl_dt)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QHBoxLayout to reduce code space.
# \param parent - QWidget as the parent, default: None.
# ---------------------------------------------------------------------------
class DoxyHBoxLayout(QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)


# ---------------------------------------------------------------------------
# \brief line number helper class for QPlainTextEdit.
# ---------------------------------------------------------------------------
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
    
    def sizeHint(self):
        return self.editor.lineNumberAreaWidth(), 0
    
    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class DoxyCodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    # Breite des linken Randes berechnen
    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        space = 10 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        )

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#2b2b2b"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.lightGray)
                painter.drawText(
                    0,
                    top,
                    self.lineNumberArea.width() - 4,
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    number
                )

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor("#333333"))
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        
        self.setExtraSelections(extraSelections)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QPushButton to reduce code space.
# \param help_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyButton(QPushButton):
    def __init__(self,
        owner             = None,
        help_str  : str   =   "",
        icon_norm : QIcon = None,
        icon_hovr : QIcon = None,
        flag      : int   =   0):
        
        super().__init__()
        
        self.help_str   = help_str
        self.owner      = owner
        self.flag       = flag
        self.filename   = ""
        
        self.icon_norm  = icon_norm
        self.icon_hovr  = icon_hovr
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
        
        self.setIconSize(QSize(22, 22))
        self.setProperty("help", self.help_str)
        
        self.setMaximumWidth (26)
        self.setMaximumHeight(26)
        
        self.clicked.connect(self.on_click)
        
        if self.icon_norm is not None:
            self.setIcon(self.icon_norm)
    
    def open_file(self) -> str:
        try:
            text = share.locales.tr("All Files")
            self.filename, _ = QFileDialog.getOpenFileName(
                self, share.locales.tr(share.locales.tr("Open File...")),
                "", f"{text} (*.*)")
            if self.filename:
                return self.filename
            return str("")
        except FileNotFoundError as e:
            msg = share.locales.tr("The requested file")
            txt = share.locales.tr("could not be found")
            fxt = share.locales.tr("File not found Error")
            
            dlg = ErrorMessage(ftxt, f"{msg}: {self.filename} {txt}.")
            dlg.exec_()
            return ""
        except PermissionError as e:
            msg = share.locales.tr("You have not enough permissions to open file")
            fxt = share.locales.tr("File Permission Error")
            
            dlg = ErrorMessage(ftxt, f"{msg}:\n{self.filename}.")
            dlg.exec_()
            return ""
        except RuntimeError as e:
            msg = share.locales.tr("Runtime Error")
            fxt = share.locales.tr("The Python Library throws a Runtime Error on opening file")
            
            dlg = ErrorMessage(msg, f"{fxt}:\n{self.filename}.")
            dlg.exec_()
            return ""
        except OSError as e:
            msg = share.locales.tr("Operation System Error")
            fxt = share.locales.tr("The System is not able to open file")
            
            dlg = ErrorMessage(msg, f"{fxt}:\n{self.filename}.")
            dlg.exec_()
            return ""
        except Exception as e:
            msg = share.locales.tr("Common Exception Error")
            fxt = share.locales.tr("Common Exception throwed during open file")
            
            dlg = ErrorMessage(msg, f"{fxt}:\n{self.filename}.")
            dlg.exec_()
            return ""
    
    def delete_current_line(self, edit):
        cursor = edit.textCursor()
        
        # 1-basierte Zeilennummer
        line_no = cursor.blockNumber() + 1
        
        text = edit.toPlainText()
        lines = text.splitlines()
        
        index = line_no - 1
        
        if 0 <= index < len(lines):
            removed_line = lines.pop(index)
            edit.setPlainText("\n".join(lines))
            
            # Cursor auf die neue Position setzen
            cursor = edit.textCursor()
            cursor.movePosition(cursor.Start)
            
            for _ in range(min(index, len(lines) - 1)):
                cursor.movePosition(cursor.Down)
            
            edit.setTextCursor(cursor)
            return line_no, removed_line

        return line_no, ""
    
    def on_click(self, b):
        found = False
        if self.owner is not None:
            if isinstance(self.owner, DoxyLineBtn1):
                if self.flag == 1:
                    if self.open_file():
                        self.owner.input.input.setText(self.filename)
            elif isinstance(self.owner, DoxyLineBtn3):
                if self.flag == 1:
                    if self.open_file():
                        self.owner.input.input.setText(self.filename)
                elif self.flag == 2:
                    if  (DOXYGEN_EXPERT_ITEMS  is not None)\
                    and (DOXYGEN_PROJECT_PAGES is not None):
                        for res in DOXYGEN_EXPERT_ITEMS:
                            page  = DOXYGEN_PROJECT_PAGES.get(res)
                            item1 = page.area.findChild(DoxyTextEdit, self.help_str)
                            item2 = page.area.findChild(DoxyLineBtn3, self.help_str)
                            if (item1 is not None) and (item1.help_str == item2.help_str):
                                item1.edit.appendPlainText(item2.input.input.text())
                                break
                elif self.flag == 3:
                    if  (DOXYGEN_EXPERT_ITEMS  is not None)\
                    and (DOXYGEN_PROJECT_PAGES is not None):
                        for res in DOXYGEN_EXPERT_ITEMS:
                            page = DOXYGEN_PROJECT_PAGES.get(res)
                            if page is not None:
                                item = page.area.findChild(DoxyTextEdit, self.help_str)
                                if item is not None:
                                    line, text = self.delete_current_line(item.edit)
                                    self.owner.input.input.setText(text)
                                    break
            elif isinstance(self.owner, DoxyLineBtn4):
                if self.flag == 1:
                    if self.open_file():
                        self.owner.input.input.setText(self.filename)
                elif self.flag == 2:
                    if  (DOXYGEN_EXPERT_ITEMS  is not None)\
                    and (DOXYGEN_PROJECT_PAGES is not None):
                        for res in DOXYGEN_EXPERT_ITEMS:
                            page = DOXYGEN_PROJECT_PAGES.get(res)
                            if page is not None:
                                item = page.area.findChild(DoxyTextEdit, self.help_str)
                                if item is not None:
                                    text = self.owner.input.input.text().strip()
                                    item.edit.appendPlainText(text)
                                    break
                elif self.flag == 3:
                    if  (DOXYGEN_EXPERT_ITEMS  is not None)\
                    and (DOXYGEN_PROJECT_PAGES is not None):
                        for res in DOXYGEN_EXPERT_ITEMS:
                            page = DOXYGEN_PROJECT_PAGES.get(res)
                            if page is not None:
                                item = page.area.findChild(DoxyTextEdit, self.help_str)
                                if item is not None:
                                    line, text = self.delete_current_line(item.edit)
                                    self.owner.input.input.setText(text)
                                    break
                elif self.flag == 4:
                    text = self.owner.input.input.text().strip()
                    print("refresh:", text)
        else:
            QMessageBox.warning(self,
                share.locales.tr("No button binding"),
                share.locales.tr("The button have no binding component."))
    
    def enterEvent(self, event):
        if self.icon_hovr is not None:
            self.setIcon(self.icon_hovr)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        if self.icon_norm is not None:
            self.setIcon(self.icon_norm)
        super().leaveEvent(event)


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
class LinkLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        
        self.web_url = "https://www.doxygen.nl/manual/config.html#cfg_"
        self.hlp_txt = text.lower()
        self.web_url = f"{self.web_url}{self.hlp_txt}"
        
        self.setFont(QFont("Consolas", 10))
        self.setMinimumWidth(164)
        self.setStyleSheet("color: white;")
        self.setText(text)
        
        self.setCursor(Qt.PointingHandCursor)
        set_tooltip_if_text(self, self.web_url)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            QDesktopServices.openUrl(QUrl(self.web_url))
        super().mousePressEvent(event)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QLabel to reduce code space.
# \param help_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyLabel(LinkLabel):
    def __init__(self,
        parent         = None,
        help_str : str =  "" ,
        flag     : int =  0 ):
        
        super().__init__(help_str, parent.owner)
        
        self.parent   = parent
        self.owner    = parent.owner
        self.help_str = help_str
        self.flag     = flag
        
        self.setObjectName(self.help_str)
       
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
        
        self.setProperty("help", self.help_str)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QPlainTextEdit to reduce code space.
# \param help_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyTextEdit(QWidget):
    def __init__(self,
        parent          = None,
        help_str : str  =  "" ,
        text     : list =  []):
        
        super().__init__(parent.owner)
        
        self.help_str = help_str
        self.text_str = text
        self.link_str = help_str
        
        self.setProperty("help", self.help_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.edit   = DoxyCodeEditor()
        
        self.label  = DoxyLabel(self.parent, self.help_str)
        self.label.setStyleSheet("color: rgba(0,0,0,0);")
        
        self.edit.setProperty("help", self.help_str)
        self.edit.setProperty("text", self.text_str)
        self.edit.setProperty("link", self.link_str)
        
        self.edit.setStyleSheet("background-color: #303030;")
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
            
        for line in text:
            self.edit.appendPlainText(line)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief construct a QCheckBox as a helper class to reduce code space.
# ---------------------------------------------------------------------------
class DoxyCheckBox(QWidget):
    def __init__(self,
        parent         = None,
        help_str : str =  ""):
        
        super().__init__(parent.owner)
        
        self.help_str = help_str
        self.text_str = ""
        self.link_str = help_str
        
        self.setProperty("help", self.help_str)
        self.setProperty("text", self.text_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(self, self.help_str, 1)
        self.check  = QCheckBox(share.locales.tr("NO"))
        
        self.label.setProperty("help", self.help_str)
        self.label.setProperty("text", self.help_str)
        self.label.setProperty("link", self.link_str)
        
        self.check.setProperty("help", self.help_str)
        #self.check.setProperty("text", self.text_str)
        self.check.setProperty("link", self.link_str)
            
        self.check.setStyleSheet("color: red;")
        self.check.toggled.connect(self.on_changed)
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
            
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.check)
        self.layout.addStretch(1)
    
    def on_changed(self, checked):
        if checked:
            self.check.setText(share.locales.tr("YES"))
            self.check.setStyleSheet("color: yellow;")
        else:
            self.check.setText(share.locales.tr("NO"))
            self.check.setStyleSheet("color: red;")
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief construct a QSpinBox as a helper class to reduce code space.
# ---------------------------------------------------------------------------
class DoxySpinEdit(QWidget):
    def __init__(self ,
        parent       = None,
        help_str:str =   "",
        v_min : int  =    0,
        v_max : int  =  100,
        v_def : int  =   0):
            
        super().__init__(None)

        self.help_str = help_str
        self.text_str = ""
        self.link_str = help_str
        
        self.setProperty("help", self.help_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(self, self.help_str, 1)
        self.spin   = QSpinBox()
        
        self.spin.setMinimum(v_min)
        self.spin.setMaximum(v_max)
        self.spin.setValue  (v_def)
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
            
        self.spin .setProperty("help", self.help_str)
        self.spin .setProperty("link", self.link_str)
        
        self.label.setProperty("help", self.help_str)
        self.label.setProperty("link", self.link_str)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spin)
        self.layout.addStretch(1)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief construct a QLineEdit with a label
# \param parent   - QWidget as the parent
# \param help_str - string for the label and help id, default: "".
# \param text_str - string for the input content, default: "".
# ---------------------------------------------------------------------------
class DoxyLineEdit(QWidget):
    def __init__(self,
        parent=None,
        help_str : str = "",
        text_str : str = "",
        flag     : int = 0):
        
        super().__init__(parent.owner)
        
        self.help_str = help_str
        self.text_str = text_str
        self.link_str = help_str
        
        self.setProperty("help", self.help_str)
        self.setProperty("text", self.text_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = flag
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(self, self.link_str)
        self.input  = QLineEdit()
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
            
        self.input.setProperty("help", self.help_str)
        self.input.setProperty("text", self.text_str)
        self.input.setProperty("link", self.link_str)
        
        self.input.setFont(QFont("Consolas", 10))
        self.input.setText(text_str)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QLineEdit with a Button to reduce code.
# ---------------------------------------------------------------------------
class DoxyLineBtn1(QWidget):
    def __init__(self,
        parent   = None,
        help_str : str = "",
        text_str : str = "",
        item     = None):
        
        super().__init__(parent.owner)
        
        self.help_str = help_str
        self.text_str = text_str
        self.link_str = help_str
        
        self.setProperty("help", self.help_str)
        self.setProperty("text", self.text_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.input  = DoxyLineEdit(self, self.help_str, self.text_str)
        
        self.input.setProperty("help", self.help_str)
        self.input.setProperty("text", self.text_str)
        self.input.setProperty("link", self.link_str)
        
        self.buttn  = DoxyButton(self  , self.help_str, QIcon(":/icons/doc.ico"), QIcon(":/icons/doc_hov.ico"), 1)
        
        self.buttn.setProperty  ("help", self.help_str)
        self.buttn.setProperty  ("text", self.text_str)
        self.buttn.setProperty  ("link", self.link_str)
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
            
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.buttn)
        
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


class DoxyLineBtn3(QWidget):
    def __init__(self,
        parent         = None,
        help_str : str =  "" ,
        text_str : str =  ""):
            
        super().__init__(parent.owner)
        
        self.help_str = help_str
        self.text_str = text_str
        self.link_str = help_str
        
        self.setProperty("help", self.help_str)
        self.setProperty("text", self.text_str)
        self.setProperty("link", self.link_str)

        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.input  = DoxyLineEdit(self, self.help_str, self.text_str)
        
        self.layout.addWidget(self.input)
        
        self.butt1  = DoxyButton(self, self.help_str, QIcon(":/icons/add.ico"), QIcon(":/icons/add_hov.ico"), 2)
        self.butt2  = DoxyButton(self, self.help_str, QIcon(":/icons/sub.ico"), QIcon(":/icons/sub_hov.ico"), 3)
        self.butt3  = DoxyButton(self, self.help_str, QIcon(":/icons/doc.ico"), QIcon(":/icons/doc_hov.ico"), 1)
        
        for item in [self.butt1, self.butt2, self.butt3]:
            item.setProperty("help", self.help_str)
            item.setProperty("text", self.text_str)
            item.setProperty("link", self.link_str)
            self.layout.addWidget(item)
            
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


class DoxyLineBtn4(QWidget):
    def __init__(self,
        parent         = None,
        help_str : str = "",
        text_str : str = "",
        flag     : int = 0):
        
        super().__init__(None)
        
        self.help_str = help_str
        self.text_str = text_str
        self.link_str = help_str
        
        self.setProperty("help", self.help_str)
        self.setProperty("text", self.text_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = flag
        
        self.layout = DoxyHBoxLayout(self)
        self.input  = DoxyLineEdit(parent, self.help_str, self.text_str, 1)
        
        self.layout.addWidget(self.input)
        
        self.butt1  = DoxyButton(self, self.help_str, QIcon(":/icons/add.ico"), QIcon(":/icons/add_hov.ico"), 2)
        self.butt2  = DoxyButton(self, self.help_str, QIcon(":/icons/sub.ico"), QIcon(":/icons/sub_hov.ico"), 3)
        self.butt3  = DoxyButton(self, self.help_str, QIcon(":/icons/frs.ico"), QIcon(":/icons/frs_hov.ico"), 4)
        self.butt4  = DoxyButton(self, self.help_str, QIcon(":/icons/doc.ico"), QIcon(":/icons/doc_hov.ico"), 1)
        
        for item in [self.butt1, self.butt2, self.butt3, self.butt3]:
            item.setProperty("help", self.help_str)
            item.setProperty("text", self.text_str)
            item.setProperty("link", self.link_str)
            self.layout.addWidget(item)
            
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QLabel with a image to reduce code space.
# \param help_str - string for the label and help id, default: "".
# \param text_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyImage(QWidget):
    def __init__(self,
        parent         = None,
        help_str : str =  "" ,
        text_str : str =  ""):
        
        super().__init__(parent.owner)
        
        self.setMinimumHeight(74)
        
        self.help_str = help_str
        self.text_str = text_str
        self.link_str = help_str
        
        self.setProperty("help", self.help_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.label2 = QLabel(self.text_str)
        
        self.label1 = DoxyLabel(self, self.help_str, 1)
        self.label1.setStyleSheet("color: rgba(0,0,0,0);")
        self.label2.setAlignment(Qt.AlignLeft)
        
        self.label2.setProperty("help", self.help_str)
        self.label2.setProperty("text", self.text_str)
        self.label2.setProperty("link", self.link_str)
        
        self.label2.setFont(QFont("Arial", 9))
        self.label2.setStyleSheet("color:yellow;")
        
        self.layout.addWidget(self.label1, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.label2, alignment=Qt.AlignLeft)
        self.layout.addStretch(1)
        
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
class DoxyComboBox(QWidget):
    def __init__(self,
        parent          = None,
        help_str : str  =   "",
        items    : list =  []):
        
        super().__init__(parent.owner)
        
        self.help_str = help_str
        self.text_str = ""
        self.link_str = help_str
        
        self.setProperty("help", self.help_str)
        self.setProperty("text", self.text_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(self, self.help_str)
        self.combo  = QComboBox()
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
        
        for item in items:
            self.combo.addItem(share.locales.tr(item))
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        self.layout.addStretch(1)
        
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


class WizardSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.pages = [
            share.locales.tr("Project"),
            share.locales.tr("Mode"),
            share.locales.tr("Output"),
            share.locales.tr("Diagrams")
        ]
        
        self.list_view = QListView(self)
        self.model     = QStringListModel(self.pages, self)
        self.list_view.setModel(self.model)
        
        self.stack = QStackedWidget(self)
        
        self.stack.addWidget(self.create_page_project ("Project Page"))
        self.stack.addWidget(self.create_page_mode    ("Mode Page"))
        self.stack.addWidget(self.create_page_output  ("Output Page"))
        self.stack.addWidget(self.create_page_diagrams("Diagrams Page"))
        
        splitter = QSplitter(Qt.Horizontal, self)
        splitter.addWidget(self.list_view)
        splitter.addWidget(self.stack)
        splitter.setSizes([160, 500])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)
        
        self.list_view.clicked.connect(self.on_page_selected)
        self.list_view.setCurrentIndex(self.model.index(0, 0))
        self.stack.setCurrentIndex(0)
    
    def create_page_project(self, title):
        page = QWidget(self)
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0,0,0,0)
        
        scroll = QScrollArea(page)
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(4,4,4,4)
        content_layout.setSpacing(4)

        label = QLabel(share.locales.tr(
            "Provide some information about "
            "the project you are documenting"),
            page)
        content_layout.addWidget(label)
        
        hlay  = QHBoxLayout()
        label = QLabel(share.locales.tr("Project name:"))
        label.setStyleSheet("color:white;weight:normal;")
        label.setFont(QFont("Arial", 9))
        label.font().setBold(False)
        label.setMinimumWidth(130)
        lined = QLineEdit()
        
        hlay.addWidget(label)
        hlay.addWidget(lined)
        content_layout.addLayout(hlay)
        
        hlay  = QHBoxLayout()
        label = QLabel(share.locales.tr("Project synopsis:"))
        label.setStyleSheet("color:white;")
        label.setFont(QFont("Arial", 9))
        label.font().setBold(False)
        label.setMinimumWidth(130)
        lined = QLineEdit()
        
        hlay.addWidget(label)
        hlay.addWidget(lined)
        content_layout.addLayout(hlay)
        
        hlay  = QHBoxLayout()
        label = QLabel(share.locales.tr("Project version or id:"))
        label.setStyleSheet("color:white;")
        label.setFont(QFont("Arial", 9))
        label.font().setBold(False)
        label.setMinimumWidth(130)
        lined = QLineEdit()
        
        hlay.addWidget(label)
        hlay.addWidget(lined)
        content_layout.addLayout(hlay)
        
        hlay  = QHBoxLayout()
        label = QLabel(share.locales.tr("Project logo:"))
        label.setStyleSheet("color:white;")
        label.setFont(QFont("Arial", 9))
        label.font().setBold(False)
        label.setMinimumWidth(130)
        lined = QLineEdit()
        lbbtn = QPushButton(share.locales.tr("Select..."))
        
        hlay.addWidget(label)
        hlay.addWidget(lined)
        hlay.addWidget(lbbtn)
        content_layout.addLayout(hlay)
        
        skipper = QLabel("")
        skipper.resize(120, 22)
        content_layout.addWidget(skipper)
        
        label = QLabel(share.locales.tr("Specify the directory to scan for source code"))
        content_layout.addWidget(label)
        
        hlay  = QHBoxLayout()
        label = QLabel(share.locales.tr("Source code directory:"))
        label.setStyleSheet("color:white;")
        label.setFont(QFont("Arial", 9))
        label.font().setBold(False)
        label.setMinimumWidth(130)
        lined = QLineEdit()
        lbbtn = QPushButton(share.locales.tr("Select..."))
        self.on_button_clicked(lbbtn, lined, 1)
        
        hlay.addWidget(label)
        hlay.addWidget(lined)
        hlay.addWidget(lbbtn)
        content_layout.addLayout(hlay)
        
        skipper = QWidget()
        skipper.resize(120, 22)
        content_layout.addWidget(skipper)
        
        hlay  = QHBoxLayout()
        label = QLabel(share.locales.tr("Destination directory:"))
        label.setStyleSheet("color:white;weight:normal;")
        label.setFont(QFont("Arial", 9))
        label.font().setBold(False)
        label.setMinimumWidth(130)
        lined = QLineEdit()
        lbbtn = QPushButton(share.locales.tr("Select..."))
        self.on_button_clicked(lbbtn, lined, 2)
        
        hlay.addWidget(label)
        hlay.addWidget(lined)
        hlay.addWidget(lbbtn)
        content_layout.addLayout(hlay)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        page_layout.addWidget(scroll)
        
        lbl_layout = QHBoxLayout()
        btn_prev   = QPushButton(share.locales.tr("Prev"))
        btn_next   = QPushButton(share.locales.tr("Next"))
        
        lbl_layout.addWidget(btn_prev)
        lbl_layout.addStretch()
        lbl_layout.addWidget(btn_next)
        
        page_layout.addLayout(lbl_layout)
        return page
        
    def on_button_clicked(self, btn, edit, mode=0):
        if mode == 1:
            self.button_src  = btn
            self.button_edit = edit
            btn.clicked.connect(self.on_button_clicked_src)
        elif mode == 2:
            self.button_dst  = btn
            self.button_edit = edit
            btn.clicked.connect(self.on_button_clicked_dst)
    
    def on_button_clicked_src(self):
        print("src")
        
    def on_button_clicked_dst(self):
        print("dst")
        
    def create_page_mode(self, title):
        page = QWidget(self)
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0,0,0,0)
        
        scroll = QScrollArea(page)
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(4,4,4,4)
        content_layout.setSpacing(4)

        group1 = QGroupBox(share.locales.tr("Select the desired extraction mode"), content)
        group2 = QGroupBox(share.locales.tr("Select programming language to optimize the result for"), content)
        
        group1_layout = QVBoxLayout(group1)
        group2_layout = QVBoxLayout(group2)
        
        group1_layout.setContentsMargins(4,4,4,4)
        group2_layout.setContentsMargins(4,4,4,4)
        
        group1_layout.setSpacing(4)
        group2_layout.setSpacing(4)
        
        g1rbt1 = QRadioButton(share.locales.tr("Documented entities only"))
        g1rbt2 = QRadioButton(share.locales.tr("All Entities"))
        g1chk1 = QCheckBox   (share.locales.tr("Include cross-referenced source code"))
        
        group1_layout.addWidget(g1rbt1)
        group1_layout.addWidget(g1rbt2)
        group1_layout.addWidget(g1chk1)
        
        txt1   = share.locales.tr("Optimize for")
        txt2   = share.locales.tr("output")
        
        font   = QFont("Consolas", 10)
        self.setStyleSheet("""
        QRadioButton {
            font-family: "Consolas";
            font-size: 10pt;
        }
        """)
        g2rbt1 = QRadioButton(f"{txt1} C++        {txt2}")
        g2rbt2 = QRadioButton(f"{txt1} C++ CLI    {txt2}")
        g2rbt3 = QRadioButton(f"{txt1} Java or C# {txt2}")
        g2rbt4 = QRadioButton(f"{txt1} C or PHP   {txt2}")
        g2rbt5 = QRadioButton(f"{txt1} Fortan     {txt2}")
        g2rbt6 = QRadioButton(f"{txt1} VHDL       {txt2}")
        g2rbt7 = QRadioButton(f"{txt1} SLICE      {txt2}")
        
        for item in [g2rbt1, g2rbt2, g2rbt3, g2rbt4, g2rbt5, g2rbt6, g2rbt7]:
            item.setFont(QFont("Consolas", 1))
            group2_layout.addWidget(item)
        
        content_layout.addWidget(group1)
        content_layout.addWidget(group2)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        page_layout.addWidget(scroll)
        
        lbl_layout = QHBoxLayout()
        btn_prev   = QPushButton(share.locales.tr("Prev"))
        btn_next   = QPushButton(share.locales.tr("Next"))
        
        lbl_layout.addWidget(btn_prev)
        lbl_layout.addStretch()
        lbl_layout.addWidget(btn_next)
        
        page_layout.addLayout(lbl_layout)
        
        return page
    
    def create_page_output(self, title):
        page = QWidget(self)
        page.setFont(QFont("Arial", 10))
        
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0,0,0,0)
        
        scroll = QScrollArea(page)
        scroll.setFont(QFont("Arial", 10))
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content.setFont(QFont("Arial", 10))
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(4,4,4,4)
        content_layout.setSpacing(4)

        label = QLabel(share.locales.tr("Select the output format(s) to generate"), page)
        content_layout.addWidget(label)
        
        group1 = QGroupBox(share.locales.tr("HTML" ), content)
        group2 = QGroupBox(share.locales.tr("LaTeX"), content)
        
        group1.setCheckable(True)
        group1.setChecked(True)
        
        group2.setCheckable(True)
        group2.setChecked(True)
        
        group1.toggled.connect(lambda checked: self.set_group_content_enabled(group1, checked))
        group2.toggled.connect(lambda checked: self.set_group_content_enabled(group2, checked))
        
        group1_layout = QVBoxLayout(group1)
        group2_layout = QVBoxLayout(group2)
        
        group1_layout.setContentsMargins(4,4,4,4)
        group2_layout.setContentsMargins(4,4,4,4)
        
        group1_layout.setSpacing(4)
        group2_layout.setSpacing(4)
        
        g1btn1 = QRadioButton(share.locales.tr("plain HTML"))
        g1btn2 = QRadioButton(share.locales.tr("with navigation panel"))
        g1btn3 = QRadioButton(share.locales.tr("prepare for compressed HTML (.chm)"))
        chkbox = QCheckBox   (share.locales.tr("with search function"))
        
        for item in [g1btn1, g1btn1, g1btn2, g1btn3, chkbox]:
            group1_layout.addWidget(item)
            
        txtmsg = share.locales.tr("as intermediate format")
        g2btn1 = QRadioButton(f"{txtmsg} hyperlinked PDF")
        g2btn2 = QRadioButton(f"{txtmsg} PDF")
        g2btn3 = QRadioButton(f"{txtmsg} PostSctipt")
        
        group2_layout.addWidget(g2btn1)
        group2_layout.addWidget(g2btn2)
        group2_layout.addWidget(g2btn3)
        
        content_layout.addWidget(group1)
        content_layout.addWidget(group2)
        
        chk1 = QCheckBox(share.locales.tr("Man page"))
        chk2 = QCheckBox(share.locales.tr("Richt Text Format (RTF)"))
        chk3 = QCheckBox(share.locales.tr("XML"))
        chk4 = QCheckBox(share.locales.tr("Docbook"))
        
        for item in [chk1, chk2, chk3, chk4]:
            content_layout.addWidget(item)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        page_layout.addWidget(scroll)
        
        lbl_layout = QHBoxLayout()
        btn_prev   = QPushButton(share.locales.tr("Prev"))
        btn_next   = QPushButton(share.locales.tr("Next"))
        
        lbl_layout.addWidget(btn_prev)
        lbl_layout.addStretch()
        lbl_layout.addWidget(btn_next)
        
        page_layout.addLayout(lbl_layout)
        
        return page
    
    def create_page_diagrams(self, title):
        page = QWidget(self)
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0,0,0,0)
        
        scroll = QScrollArea(page)
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(4,4,4,4)
        content_layout.setSpacing(4)
        
        group1 = QGroupBox(share.locales.tr("Diagrams to generate" ), content)
        group2 = QGroupBox(share.locales.tr("Dot graphs to generate"), content)

        group1_layout = QVBoxLayout(group1)
        group2_layout = QVBoxLayout(group2)
        
        group1_layout.setContentsMargins(4,4,4,4)
        group2_layout.setContentsMargins(4,4,4,4)
        
        group1_layout.setSpacing(4)
        group2_layout.setSpacing(4)
        
        radio1 = QRadioButton(share.locales.tr("No diagrams"))
        radio2 = QRadioButton(share.locales.tr("Text only"))
        radio3 = QRadioButton(share.locales.tr("Use built-in class diagram generator"))
        radio4 = QRadioButton(share.locales.tr("Use dot tool from the GraphWiz package"))
        
        for item in [radio1, radio2, radio3, radio4]:
            group1_layout.addWidget(item)
        
        check1 = QCheckBox(share.locales.tr("Class graphs"))
        check2 = QCheckBox(share.locales.tr("Collaboration Class Hierarchy"))
        check3 = QCheckBox(share.locales.tr("Overall Class Hierarchy"))
        check4 = QCheckBox(share.locales.tr("Include dependency graphs"))
        check5 = QCheckBox(share.locales.tr("Included by dependency graphs"))
        check6 = QCheckBox(share.locales.tr("Call Graphs"))
        check7 = QCheckBox(share.locales.tr("Called by graphs"))
        
        for item in [check1, check2, check3, check4, check5, check6, check7]:
            group2_layout.addWidget(item)
        
        content_layout.addWidget(group1)
        content_layout.addWidget(group2)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        page_layout.addWidget(scroll)
        
        lbl_layout = QHBoxLayout()
        btn_prev   = QPushButton(share.locales.tr("Prev"))
        btn_next   = QPushButton(share.locales.tr("Next"))
        
        lbl_layout.addWidget(btn_prev)
        lbl_layout.addStretch()
        lbl_layout.addWidget(btn_next)
        
        page_layout.addLayout(lbl_layout)
        
        return page

    def on_page_selected(self, index):
        self.stack.setCurrentIndex(index.row())
    
    def set_group_content_enabled(self, group, checked):
        for child in group.findChildren(QWidget):
            child.setEnabled(checked)

# ---------------------------------------------------------------------------
# \brief this is the doxygen tool window for help / documenting the source.
# ---------------------------------------------------------------------------
class DoxyGenToolWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.owner       = self
        self.config      = {}
        self.state       = {}
        
        self.project_dir = _default_project_dir()
        self.propath     = self.project_dir / "doxygen_project.json"
        
        self.current_project_path = ""

        #self.lang = share.locales.get_default_lang().split("_")[0].lower()
        #self.trmo = share.locales.load_mo_from_resource(f":/locales/{self.lang}/doxygen.mo")
            
        self._build_ui()
        self._reload_project_list()
        
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(4, 4, 4, 4)

        self.main_splitter = QSplitter(Qt.Horizontal)
        root.addWidget(self.main_splitter)

        self.left_host = QWidget()
        left_lay = QVBoxLayout(self.left_host)
        left_lay.setContentsMargins(0, 0, 0, 0)

        self.project_list = QListWidget()
        self.project_list.itemDoubleClicked.connect(self._load_selected_project)
        left_lay.addWidget(self.project_list, 1)

        btn_row = QHBoxLayout()
        self.btn_save   = QPushButton(share.locales.tr("Save"))
        self.btn_delete = QPushButton(share.locales.tr("Delete"))
        self.btn_load   = QPushButton(share.locales.tr("Open"))
        
        btn_row.addWidget(self.btn_save)
        btn_row.addWidget(self.btn_delete)
        btn_row.addWidget(self.btn_load)
        
        left_lay.addLayout(btn_row)
        
        self.btn_save  .clicked.connect(self.save_project_as)
        self.btn_delete.clicked.connect(self._delete_selected_project)
        self.btn_load  .clicked.connect(self._load_selected_project)
        
        self.main_splitter.addWidget(self.left_host)
        
        self.right_host = QWidget()
        right_lay = QVBoxLayout(self.right_host)
        right_lay.setContentsMargins(0, 0, 0, 0)
        
        hlay = QHBoxLayout()
        self.lineCWD = QLineEdit()
        self.btn_CWD = QPushButton(share.locales.tr("Select"))
        self.txt_CWD = QLabel(share.locales.tr("Specify the working directory from which doxygen will run"))
        
        self.btn_CWD.clicked.connect(self.on_cwd_click)
        
        hlay.addWidget(self.lineCWD)
        hlay.addWidget(self.btn_CWD)
        
        right_lay.addWidget(self.txt_CWD)
        right_lay.addLayout(hlay)
        
        self.tabs = QTabWidget()
        right_lay.addWidget(self.tabs)
        
        self.main_splitter.addWidget(self.right_host)
        self.main_splitter.setSizes([260, 940])
        
        
        self.tabs.addTab(self._build_wizard_tab(), share.locales.tr("Wizard"))
        self.tabs.addTab(self._build_expert_tab(), share.locales.tr("Expert"))
        self.tabs.addTab(self._build_run_tab   (), share.locales.tr("Run"))

    def on_cwd_click(self):
        file_name = share.drives.open_share_file_dialog(self)
        print(file_name)
        generate_html(file_name, "html")
        
    def _build_wizard_tab(self):
        page = WizardSettings()
        return page

    def _create_scroll_page(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_owner  = self
        scroll_widget = QWidget()
        
        scroll_lay    = QVBoxLayout(scroll_widget)
        scroll_lay.setContentsMargins(2, 2, 2, 2)
        scroll_lay.setSpacing(2)

        scroll_area.setWidget(scroll_widget)

        return scroll_owner, scroll_area, scroll_widget, scroll_lay
    
    def _build_expert_tab(self):
        page     = QWidget()
        page_lay = QVBoxLayout(page)
        page_lay.setContentsMargins(0, 0, 0, 0)
        
        self.expert_splitter_v = QSplitter(Qt.Vertical)
        page_lay.addWidget(self.expert_splitter_v)
        
        top_host = QWidget()
        top_lay  = QVBoxLayout(top_host)
        top_lay.setContentsMargins(0, 0, 0, 0)
        
        self.expert_splitter_h = QSplitter(Qt.Horizontal)
        top_lay.addWidget(self.expert_splitter_h)
        
        self.list_categories = QListWidget()
        
        for item in DOXYGEN_EXPERT_ITEMS:
            self.list_categories.addItem(item)
        
        self.list_categories.currentTextChanged.connect(self._on_expert_item_changed)
        self.expert_splitter_h.addWidget(self.list_categories)
        
        # -----------------------------------------------------------
        self.expert_pages = QStackedWidget()
        self.expert_splitter_h.addWidget(self.expert_pages)
        
        for name in DOXYGEN_EXPERT_ITEMS:
            scroll_owner, scroll_area, scroll_widget, scroll_lay = self._create_scroll_page()
            DOXYGEN_PROJECT_PAGES[str(name)] = DoxyScrollPage(
                scroll_owner,
                scroll_area,
                scroll_widget,
                scroll_lay
            )
            self.expert_pages.addWidget(scroll_area)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.scroll_lay = QVBoxLayout(self.expert_pages)
        self.scroll_lay.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay.setSpacing(2)
        
        # -------------------------------------------------------------------------
        self.par1 = DOXYGEN_PROJECT_PAGES["Project"]
        self.project_items = [
            DoxyLineEdit (self.par1, "DOXYFILE_ENCODING", "UTF-8"),
            
            DoxyLineEdit(self.par1, "PROJECT_NAME", share.locales.tr("MyProject")),
            DoxyLineEdit(self.par1, "PROJECT_NUMBER"),
            DoxyLineEdit(self.par1, "PROJECT_BRIEF"),
            DoxyLineBtn1(self.par1, "PROJECT_LOGO"),
            DoxyImage   (self.par1, "PROJECT_LOGO", "No Project Logo selected."),
            DoxyLineBtn1(self.par1, "PROJECT_ICON"),
            DoxyImage   (self.par1, "PROJECT_ICON", "No Project Icon selected."),
            
            DoxyLineBtn1(self.par1, "OUTPUT_DIRECTORY"),
            DoxyCheckBox(self.par1, "CREATE_SUBDIRS"),
            DoxySpinEdit(self.par1, "CREATE_SUBDIRS_LEVEL", 0, 64, 4),
            
            DoxyCheckBox(self.par1, "ALLOW_UNICODE_NAMES"),
            DoxyComboBox(self.par1, "OUTPUT_LANGUAGE", SUPPORTED_LANGUAGES),
            
            DoxyCheckBox(self.par1, "BRIEF_MEMBER_DESC"),
            DoxyCheckBox(self.par1, "REPEAT_BRIEF"),
            
            DoxyLineBtn3(self.par1, "ABBREVIATE_BRIEF"),
            DoxyTextEdit(self.par1, "ABBREVIATE_BRIEF", []),
            
            DoxyCheckBox(self.par1, "ALWAYS_DETAILED_SEC"),
            DoxyCheckBox(self.par1, "INLINE_INHERITED_MEMB"),
            
            DoxyCheckBox(self.par1, "FULL_PATH_NAMES"),
            
            DoxyLineBtn4(self.par1, "STRIP_FROM_PATH"),
            DoxyTextEdit(self.par1, "STRIP_FROM_PATH", []),
            
            DoxyLineBtn4(self.par1, "STRIP_FROM_INC_PATH"),
            DoxyTextEdit(self.par1, "STRIP_FROM_INC_PATH", []),
            
            DoxyCheckBox(self.par1, "SHORT_NAMES"),
            
            DoxyCheckBox(self.par1, "JAVADOC_AUTOBRIEF"),
            DoxyCheckBox(self.par1, "JAVADOC_BANNER"),
            
            DoxyCheckBox(self.par1, "QT_AUTOBRIEF"),
            DoxyCheckBox(self.par1, "PYTHON_DOCSTRING"),
            DoxyCheckBox(self.par1, "INHERIT_DOCS"),
            
            DoxyCheckBox(self.par1, "SEPARATE_MEMBER_PAGES"),
            DoxySpinEdit(self.par1, "TAB_SIZE", 2, 16, 2),
            
            DoxyLineBtn3(self.par1, "ALIASES"),
            DoxyTextEdit(self.par1, "ALIASES", []),
            
            DoxyCheckBox(self.par1, "OPTIMIZE_OUTPUT_C"),
            DoxyCheckBox(self.par1, "OPTIMIZE_OUTPUT_JAVA"),
            DoxyCheckBox(self.par1, "OPTIMIZE_OUTPUT_FORTRAN"),
            DoxyCheckBox(self.par1, "OPTIMIZE_OUTPUT_VHDL"),
            DoxyCheckBox(self.par1, "OPTIMIZE_OUTPUT_SLICE"),
            
            DoxyLineBtn3(self.par1, "EXTENSION_MAPPING"),
            DoxyTextEdit(self.par1, "EXTENSION_MAPPING", []),
            
            DoxyCheckBox(self.par1, "MARKDOWN_SUPPORT"),
            DoxyCheckBox(self.par1, "MARKDOWN_STRICT"),
            DoxyComboBox(self.par1, "MARKDOWN_ID_STYLE", ["DOXYGEN", "GITHUB"]),
            
            DoxySpinEdit(self.par1, "TOC_INCLUDE_HEADINGS"),
            
            DoxyCheckBox(self.par1, "AUTOLINK_SUPPORT"),
            DoxyLineBtn3(self.par1, "AUTOLINK_IGNORE_WORDS"),
            DoxyTextEdit(self.par1, "AUTOLINK_IGNORE_WORDS", []),
            
            DoxyCheckBox(self.par1, "BUILTIN_STL_SUPPORT"),
            DoxyCheckBox(self.par1, "CPP_CLI_SUPPORT"),
            DoxyCheckBox(self.par1, "SIP_SUPPORT"),
            DoxyCheckBox(self.par1, "IDL_PROPERTY_SUPPORT"),
            DoxyCheckBox(self.par1, "DISTRIBUTE_GROUP_DOC"),
            DoxyCheckBox(self.par1, "GROUP_NESTED_COMPOUNDS"),
            
            DoxyCheckBox(self.par1, "SUBGROUPING"),
            DoxyCheckBox(self.par1, "INLINE_GROUPED_CLASSES"),
            DoxyCheckBox(self.par1, "INLINE_SIMPLE_STRUCTS"),
            
            DoxyCheckBox(self.par1, "TYPEDEF_HIDES_STRUCT"),
            DoxySpinEdit(self.par1, "LOOKUP_CACHE_SIZE"),
            
            DoxySpinEdit(self.par1, "NUM_PROC_THREADS"),
            DoxyComboBox(self.par1, "TIMESTAMP", ["YES", "NO", "DATETIME", "DATE"]),
        ]
        project_lay = DOXYGEN_PROJECT_PAGES["Project"].layout
        for item in self.project_items:
            project_lay.addWidget(item)
        project_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par2 = DOXYGEN_PROJECT_PAGES["Build"]
        self.build_items = [
            DoxyCheckBox(self.par2, "EXTRACT_ALL"),
            DoxyCheckBox(self.par2, "EXTRACT_PRIVATE"),
            DoxyCheckBox(self.par2, "EXTRACT_PRIV_VIRTUAL"),
            DoxyCheckBox(self.par2, "EXTRACT_PACKAGE"),
            DoxyCheckBox(self.par2, "EXTRACT_STATIC"),
            
            DoxyCheckBox(self.par2, "EXTRACT_LOCAL_CLASSES"),
            DoxyCheckBox(self.par2, "EXTRACT_LOCAL_METHODS"),
            
            DoxyCheckBox(self.par2, "EXTRACT_ANON_NSPACES"),
            DoxyCheckBox(self.par2, "RESOLVE_UNNAMED_PARAMS"),
            
            DoxyCheckBox(self.par2, "HIDE_UNDOC_MEMBERS"),
            DoxyCheckBox(self.par2, "HIDE_UNDOC_CLASSES"),
            DoxyCheckBox(self.par2, "HIDE_UNDOC_NAMESPACES"),
            
            DoxyCheckBox(self.par2, "HIDE_FRIEND_COMPOUNDS"),
            DoxyCheckBox(self.par2, "HIDE_IN_BODY_DOCS"),
            
            DoxyCheckBox(self.par2, "INTERNAL_DOCS"),
            DoxyComboBox(self.par2, "CASE_SENSE_NAMES", [
                "SYSTEM",
                "YES",
                "NO"
            ]),
            
            DoxyCheckBox(self.par2, "HIDE_UNDOC_MEMBERS"),
            DoxyCheckBox(self.par2, "HIDE_SCOPE_NAMES"),
            DoxyCheckBox(self.par2, "HIDE_COMPOUND_REFERENCE"),
            
            DoxyCheckBox(self.par2, "SHOW_HEADERFILE"),
            DoxyCheckBox(self.par2, "SHOW_INCLUDE_FILES"),
            
            DoxyCheckBox(self.par2, "FORCE_LOCAL_INCLUDES"),
            DoxyCheckBox(self.par2, "INLINE_INFO"),
            
            DoxyCheckBox(self.par2, "SORT_MEMBER_DOCS"),
            DoxyCheckBox(self.par2, "SORT_BRIEF_DOCS"),
            DoxyCheckBox(self.par2, "SORT_MEMBER_CTORS_1ST"),
            DoxyCheckBox(self.par2, "SORT_GROUP_NAMES"),
            DoxyCheckBox(self.par2, "SORT_BY_SCOPE_NAME"),
            
            DoxyCheckBox(self.par2, "STRICT_PROTO_MATCHING"),
            
            DoxyCheckBox(self.par2, "GENERATE_TODOLIST"),
            DoxyCheckBox(self.par2, "GENERATE_TESTLIST"),
            DoxyCheckBox(self.par2, "GENERATE_BUGLIST"),
            DoxyCheckBox(self.par2, "GENERATE_DEPRECATEDLIST"),
            DoxyCheckBox(self.par2, "GENERATE_REQUIREMENTS"),
            
            DoxyComboBox(self.par2, "REQ_TRACEABILITY_INFO", [
                "YES",
                "NO",
                "UNSATISFIED_ONLY",
                "UNVERIFIED_ONLY"
            ]),
            
            DoxyLineBtn3(self.par2, "ENABLED_SECTIONS"),
            DoxyTextEdit(self.par2, "ENABLED_SECTIONS", []),
            
            DoxySpinEdit(self.par2, "MAX_INITIALIZER_LINES"),
            
            DoxyCheckBox(self.par2, "SHOW_USED_FILES"),
            DoxyCheckBox(self.par2, "SHOW_FILES"),
            DoxyCheckBox(self.par2, "SHOW_NAMESPACES"),
            
            DoxyLineBtn1(self.par2, "FILE_VERSION_FILTER"),
            DoxyLineBtn1(self.par2, "LAYOUT_FILE"),
            DoxyLineBtn4(self.par2, "CITE_BIB_FILES"),
            DoxyTextEdit(self.par2, "CITE_BIB_FILES", []),
            
            DoxyLineBtn4(self.par2, "EXTERNAL_TOOL_PATH"),
            DoxyTextEdit(self.par2, "EXTERNAL_TOOL_PATH", [])
        ]
        build_lay = DOXYGEN_PROJECT_PAGES["Build"].layout
        for item in self.build_items:
            build_lay.addWidget(item)
        build_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par3 = DOXYGEN_PROJECT_PAGES["Messages"]
        #self.par3 = self.par3.owner
        self.messages_items = [
            DoxyCheckBox(self.par3, "QUIET"),
            DoxyCheckBox(self.par3, "WARNINGS"),
            DoxyCheckBox(self.par3, "WARN_IF_UNDOCUMENTED"),
            DoxyCheckBox(self.par3, "WARN_IF_DOC_ERROR"),
            DoxyCheckBox(self.par3, "WARN_IF_INCOMPLETE_DOC"),
            DoxyCheckBox(self.par3, "WARN_NO_PARAMDOC"),
            DoxyCheckBox(self.par3, "WARN_IF_UNDOC_ENUM_VAL"),
            DoxyCheckBox(self.par3, "WARN_LAYOUT_FILE"),
            DoxyComboBox(self.par3, "WARN_AS_ERROR", [
                "NO",
                "YES",
                "FAIL_ON_WARNINGS",
                "FAIL_ON_WARNINGS_PRINT"]),
            DoxyLineEdit(self.par3, "WARN_FORMAT"),
            DoxyLineEdit(self.par3, "WARN_LINE_FORMAT"),
            DoxyLineBtn1(self.par3, "WARN_LOGFILE"),
        ]
        messages_lay = DOXYGEN_PROJECT_PAGES["Messages"].layout
        for item in self.messages_items:
            messages_lay.addWidget(item)
        messages_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par4 = DOXYGEN_PROJECT_PAGES["Input"]
        #self.par4.owner
        self.input_items = [
            DoxyLineBtn4(self.par4, "INPUT"),
            DoxyTextEdit(self.par4, "INPUT", []),
            DoxyLineEdit(self.par4, "INPUT_ENCODING"),
            DoxyLineBtn3(self.par4, "INPUT_FILE_ENCODING"),
            DoxyTextEdit(self.par4, "INPUT_FILE_ENCODING", []),
            
            DoxyLineBtn3(self.par4, "FILE_PATTERNS"),
            DoxyTextEdit(self.par4, "FILE_PATTERNS", ["*.c", "*.cc"]),
            
            DoxyCheckBox(self.par4, "RECURSIVE"),
            
            DoxyLineBtn4(self.par4, "EXCLUDE"),
            DoxyTextEdit(self.par4, "EXCLUDE", []),
            
            DoxyLineBtn3(self.par4, "EXCLUDE_PATTERNS"),
            DoxyTextEdit(self.par4, "EXCLUDE_PATTERNS", []),
            DoxyLineBtn3(self.par4, "EXCLUDE_SYMBOLS"),
            DoxyTextEdit(self.par4, "EXCLUDE_SYMBOLS", []),
            
            DoxyLineBtn4(self.par4, "EXAMPLE_PATH"),
            DoxyTextEdit(self.par4, "EXAMPLE_PATH", []),
            DoxyLineBtn3(self.par4, "EXAMPLE_PATTERNS"),
            DoxyTextEdit(self.par4, "EXAMPLE_PATTERNS", ["*"]),
            DoxyCheckBox(self.par4, "EXAMPLE_RECURSIVE"),
            
            DoxyLineBtn4(self.par4, "IMAGE_PATH"),
            DoxyTextEdit(self.par4, "IMAGE_PATH", []),
            
            DoxyLineBtn1(self.par4, "INPUT_FILTER"),
            
            DoxyLineBtn3(self.par4, "FILTER_PATTERNS"),
            DoxyTextEdit(self.par4, "FILTER_PATTERNS", []),
            
            DoxyCheckBox(self.par4, "FILTER_SOURCE_FILES"),
            DoxyLineBtn3(self.par4, "FILTER_SOURCE_PATTERNS"),
            DoxyTextEdit(self.par4, "FILTER_SOURCE_PATTERNS", []),
            
            DoxyLineEdit(self.par4, "USE_MDFILE_AS_MAINPAGE"),
            
            DoxyCheckBox(self.par4, "IMPLICIT_DIR_DOCS"),
            DoxySpinEdit(self.par4, "FORTRAN_COMMENT_AFTER", 0, 128, 72)
        ]
        input_lay = DOXYGEN_PROJECT_PAGES["Input"].layout
        for item in self.input_items:
            input_lay.addWidget(item)
        input_lay.addStretch()

        # -------------------------------------------------------------------------
        self.par5 = DOXYGEN_PROJECT_PAGES["Source Browser"]
        self.browser_items = [
            DoxyCheckBox(self.par5, "SOURCE_BROWSER"),
            DoxyCheckBox(self.par5, "INLINE_SOURCES"),
            DoxyCheckBox(self.par5, "STRIP_CODE_COMMENTS"),
            
            DoxyCheckBox(self.par5, "REFERENCED_BY_RELATION"),
            DoxyCheckBox(self.par5, "REFERENCES_RELATION"),
            DoxyCheckBox(self.par5, "REFERENCES_LINK_SOURCE"),
            
            DoxyCheckBox(self.par5, "SOURCE_TOOLTIPS"),
            DoxyCheckBox(self.par5, "USE_HTAGS"),
            DoxyCheckBox(self.par5, "VERBATIM_HEADERS"),
            
            DoxyCheckBox(self.par5, "CLANG_ASSISTED_PARSING"),
            DoxyCheckBox(self.par5, "CLANG_ADD_INC_PATHS"),
            DoxyLineBtn3(self.par5, "CLANG_OPTIONS"),
            DoxyTextEdit(self.par5, "CLANG_OPTIONS", []),
            DoxyLineBtn1(self.par5, "CLANG_DATABASE_PATH")
        ]
        browser_lay = DOXYGEN_PROJECT_PAGES["Source Browser"].layout
        for item in self.browser_items:
            browser_lay.addWidget(item)
        browser_lay.addStretch()

        # -------------------------------------------------------------------------
        self.par6 = DOXYGEN_PROJECT_PAGES["Index"]
        self.index_items = [
            DoxyCheckBox(self.par6, "ALPHABETICAL_INDEX"),
            DoxyLineBtn3(self.par6, "IGNORE_PREFIX"),
            DoxyTextEdit(self.par6, "IGNORE_PREFIX", [])
        ]
        index_lay = DOXYGEN_PROJECT_PAGES["Index"].layout
        for item in self.index_items:
            index_lay.addWidget(item)
        index_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par7 = DOXYGEN_PROJECT_PAGES["HTML"]
        self.html_items = [
            DoxyCheckBox(self.par7, "GENERATE_HTML"),
            DoxyLineBtn1(self.par7, "HTML_OUTPUT"),
            DoxyLineEdit(self.par7, "HTML_FILE_EXTENSION"),
            
            DoxyLineBtn1(self.par7, "HTML_HEADER"),
            DoxyLineBtn1(self.par7, "HTML_FOOTER"),
            
            DoxyLineBtn1(self.par7, "HTML_STYLESHEET"),
            DoxyLineBtn4(self.par7, "HTML_EXTRA_STYLESHEET"),
            DoxyTextEdit(self.par7, "HTML_EXTRA_STYLESHEET", []),
            DoxyLineBtn4(self.par7, "HTML_EXTRA_FILES"),
            DoxyTextEdit(self.par7, "HTML_EXTRA_FILES", []),
            
            DoxyComboBox(self.par7, "HTML_COLORSTYLE", [
                "LIGHT",
                "DARK",
                "AUTO_LIGHT",
                "AUTP_DARK",
                "TOGGLE"
            ]),
            
            DoxySpinEdit(self.par7, "HTML_COLOR_STYLE_HUE"  , 0, 255, 220),
            DoxySpinEdit(self.par7, "HTML_COLOR_STYLE_SAT"  , 0, 255, 100),
            DoxySpinEdit(self.par7, "HTML_COLOR_STYLE_GAMMA", 0, 255,  80),
            
            DoxyCheckBox(self.par7, "HTML_DYNAMIC_MENUS"),
            DoxyCheckBox(self.par7, "HTML_DYNAMIC_SECTIONS"),
            
            DoxyCheckBox(self.par7, "HTML_CODE_FOLDING"),
            DoxyCheckBox(self.par7, "HTML_COPY_CLIPBOARD"),
            DoxyLineEdit(self.par7, "HTML_PROJECT_COOKIE"),
            DoxySpinEdit(self.par7, "HTML_INDEX_NUM_ENTRIES", 0, 255, 100),
            
            DoxyCheckBox(self.par7, "GENERATE_DOCSET"),
            DoxyLineEdit(self.par7, "DOCSET_FEEDNAME"),
            DoxyLineEdit(self.par7, "DOCSET_FEEDURL"),
            DoxyLineEdit(self.par7, "DOCSET_BUNDLE_ID"),
            DoxyLineEdit(self.par7, "DOCSET_PUBLISHER_ID"),
            DoxyLineEdit(self.par7, "DOCSET_PUBLISHER_NAME"),
            
            DoxyCheckBox(self.par7, "GENERATE_HTMLHELP"),
            DoxyLineBtn1(self.par7, "CHM_FILE"),
            DoxyLineBtn1(self.par7, "HHC_LOCATION"),
            
            DoxyCheckBox(self.par7, "GENERATE_CHI"),
            DoxyLineEdit(self.par7, "CHM_INDEX_ENCODING"),
            DoxyCheckBox(self.par7, "BINARY_TOC"),
            DoxyCheckBox(self.par7, "TOC_EXPAND"),
            DoxyLineEdit(self.par7, "SITEMAP_URL"),
            
            DoxyCheckBox(self.par7, "GENERATE_QHP"),
            DoxyLineBtn1(self.par7, "QCH_FILE"),
            
            DoxyLineEdit(self.par7, "QHP_NAMESPACE"),
            DoxyLineEdit(self.par7, "QHP_VIRTUAL_FOLDER"),
            DoxyLineEdit(self.par7, "QHP_CUST_FILTER_NAME"),
            DoxyLineEdit(self.par7, "QHP_CUST_FILTER_ATTRS"),
            DoxyLineEdit(self.par7, "QHP_SECT_FILTER_ATTRS"),
            
            DoxyLineBtn1(self.par7, "QHG_LOCATION"),
            
            DoxyCheckBox(self.par7, "GENERATE_ECLIPSE_HELP"),
            DoxyLineEdit(self.par7, "ECLIPSE_DOC_ID"),
            DoxyCheckBox(self.par7, "DISABLE_INDEX"),
            
            DoxyCheckBox(self.par7, "GENERATE_TREEVIEW"),
            DoxyCheckBox(self.par7, "PAGE_OUTLINE_PANEL"),
            DoxyCheckBox(self.par7, "FULL_SIDEBAR"),
            
            DoxySpinEdit(self.par7, "ENUM_VALUES_PER_LINE", 1, 200, 4),
            DoxyCheckBox(self.par7, "SHOW_ENUM_VALUES"),
            
            DoxySpinEdit(self.par7, "TREEVIEW_WIDTH", 50, 800, 250),
            
            DoxyCheckBox(self.par7, "EXT_LINKS_IN_WINDOW"),
            DoxyCheckBox(self.par7, "OBFUSCATE_EMAILS"),
            
            DoxyComboBox(self.par7, "HTML_FORMULA_FORMAT", ["png", "svg"]),
            
            DoxySpinEdit(self.par7, "FORMULA_FONTSIZE", 9, 74, 10),
            DoxyLineBtn1(self.par7, "FORMULA_MACROFILE"),
            
            DoxyCheckBox(self.par7, "USE_MATHJAX"),
            
            DoxyComboBox(self.par7, "MATHJAX_VERSION", ["MathJax2", "MathJax3", "MathJax4"]),
            DoxyComboBox(self.par7, "MATHJAX_FORMAT", ["HTML-CSS", "NativeHtml", "chtml", "SVG"]),
            DoxyLineEdit(self.par7, "MATHJAX_RELPATH"),
            DoxyLineBtn3(self.par7, "MATHJAX_EXTENSIONS"),
            DoxyTextEdit(self.par7, "MATHJAX_EXTENSIONS", []),
            DoxyLineEdit(self.par7, "MATHJAX_CODEFILE"),
            
            DoxyCheckBox(self.par7, "SEARCHENGINE"),
            DoxyCheckBox(self.par7, "SERVER_BASED_SEARCH"),
            DoxyCheckBox(self.par7, "EXTERNAL_SEARCH"),
            DoxyLineEdit(self.par7, "SEARCHENGINE_URL"),
            DoxyLineBtn1(self.par7, "SEARCHDATA_FILE"),
            DoxyLineEdit(self.par7, "EXTERNAL_SEARCH_ID"),
            DoxyLineBtn3(self.par7, "EXTRA_SEARCH_MAPPINGS"),
            DoxyTextEdit(self.par7, "EXTRA_SEARCH_MAPPINGS", []),
        ]
        html_lay = DOXYGEN_PROJECT_PAGES["HTML"].layout
        for item in self.html_items:
            html_lay.addWidget(item)
        html_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par8 = DOXYGEN_PROJECT_PAGES["LaTeX"]
        self.latex_items = [
            DoxyCheckBox(self.par8, "GENERATE_LATEX"),
            DoxyLineBtn1(self.par8, "LATEX_OUTPUT"),
            DoxyLineBtn1(self.par8, "LATEX_CMD_NAME"),
            DoxyLineBtn1(self.par8, "MAKEINDEX_CMD_NAME"),
            DoxyLineEdit(self.par8, "LATEX_MAKEINDEX_CMD"),
            DoxyCheckBox(self.par8, "COMPACT_LATEX"),
            DoxyComboBox(self.par8, "PAPER_TYPE", ["a4", "letter", "legal", "executive"]),
            DoxyLineBtn3(self.par8, "EXTRA_PACKAGES"),
            DoxyTextEdit(self.par8, "EXTRA_PACKAGES", []),
            DoxyLineBtn1(self.par8, "LATEX_HEADER"),
            DoxyLineBtn1(self.par8, "LATEX_FOOTER"),
            DoxyLineBtn4(self.par8, "LATEX_EXTRA_STYLESHEET"),
            DoxyTextEdit(self.par8, "LATEX_EXTRA_STYLESHEET", []),
            DoxyLineBtn4(self.par8, "LATEX_EXTRA_FILES"),
            DoxyTextEdit(self.par8, "LATEX_EXTRA_FILES", []),
            DoxyCheckBox(self.par8, "PDF_HYPERLINKS"),
            DoxyCheckBox(self.par8, "USE_PDFLATEX"),
            DoxyComboBox(self.par8, "LATEX_BATCHMODE", [
                "NO",
                "YES",
                "BATCH",
                "NON_STOP",
                "SCROLL",
                "ERROR_STOP"
                ]),
            DoxyCheckBox(self.par8, "LATEX_HIDE_INDICES"),
            DoxyLineEdit(self.par8, "LATEX_BIB_STYLE"),
            DoxyLineBtn1(self.par8, "LATEX_EMOJI_DIRECTORY")
        ]
        latex_lay = DOXYGEN_PROJECT_PAGES["LaTeX"].layout
        for item in self.latex_items:
            latex_lay.addWidget(item)
        latex_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par9 = DOXYGEN_PROJECT_PAGES["RTF"]
        self.rtf_items = [
            DoxyCheckBox(self.par9, "GENERATE_RTF"),
            DoxyLineBtn1(self.par9, "RTF_OUTPUT"),
            DoxyCheckBox(self.par9, "COMPACT_RTF"),
            DoxyCheckBox(self.par9, "RTF_HYPERLINKS"),
            DoxyLineBtn1(self.par9, "RTF_STYLESHEET_FILE"),
            DoxyLineBtn1(self.par9, "RTF_EXTENSIONS_FILE"),
            DoxyLineBtn4(self.par9, "RTF_EXTRA_FILES")
        ]
        rtf_lay = DOXYGEN_PROJECT_PAGES["RTF"].layout
        for item in self.rtf_items:
            rtf_lay.addWidget(item)
        rtf_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par10 = DOXYGEN_PROJECT_PAGES["Man"]
        self.man_items = [
            DoxyCheckBox(self.par10, "GENERATE_MAN"),
            DoxyLineBtn1(self.par10, "MAN_OUTPUT"),
            DoxyLineEdit(self.par10, "MAN_EXTENSION"),
            DoxyLineEdit(self.par10, "MAN_SUBDIR"),
            DoxyCheckBox(self.par10, "MAN_LINKS")
        ]
        man_lay = DOXYGEN_PROJECT_PAGES["Man"].layout
        for item in self.man_items:
            man_lay.addWidget(item)
        man_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par11 = DOXYGEN_PROJECT_PAGES["XML"]
        self.xml_items = [
            DoxyCheckBox(self.par11, "GENERATE_XML"),
            DoxyLineBtn1(self.par11, "XML_OUTPUT"),
            DoxyCheckBox(self.par11, "XML_PROGRAMLISTING"),
            DoxyCheckBox(self.par11, "XML_NS_MEMB_FILE_SCOPE")
        ]
        xml_lay = DOXYGEN_PROJECT_PAGES["XML"].layout
        for item in self.xml_items:
            xml_lay.addWidget(item)
        xml_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par12 = DOXYGEN_PROJECT_PAGES["DocBook"]
        self.docbook_items = [
            DoxyCheckBox(self.par12, "GENERATE_DOCBOOK"),
            DoxyLineBtn1(self.par12, "DOCBOOK_OUTPUT")
        ]
        docbook_lay = DOXYGEN_PROJECT_PAGES["DocBook"].layout
        for item in self.docbook_items:
            docbook_lay.addWidget(item)
        docbook_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par13 = DOXYGEN_PROJECT_PAGES["AutoGen"]
        self.autogen_items = [
            DoxyCheckBox(self.par13, "GENERATE_AUTOGEN_DEF"),
        ]
        autogen_lay = DOXYGEN_PROJECT_PAGES["AutoGen"].layout
        for item in self.autogen_items:
            autogen_lay.addWidget(item)
        autogen_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par14 = DOXYGEN_PROJECT_PAGES["SQLite3"]
        self.sqlite3_items = [
            DoxyCheckBox(self.par14, "GENERATE_SQLITE3"),
            DoxyLineBtn1(self.par14, "SQLITE3_OUTPUT"),
            DoxyCheckBox(self.par14, "SQLITE3_RECREATE_DB")
        ]
        sqlite3_lay = DOXYGEN_PROJECT_PAGES["SQLite3"].layout
        for item in self.sqlite3_items:
            sqlite3_lay.addWidget(item)
        sqlite3_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par15 = DOXYGEN_PROJECT_PAGES["PerlMod"]
        self.perlmod_items = [
            DoxyCheckBox(self.par15, "GENERATE_PERLMOD"),
            DoxyCheckBox(self.par15, "PERLMOD_LATEX"),
            DoxyCheckBox(self.par15, "PERLMOD_PRETTY"),
            DoxyLineEdit(self.par15, "PERLMOD_MAKEVAR_PREFIX")
        ]
        perlmod_lay = DOXYGEN_PROJECT_PAGES["PerlMod"].layout
        for item in self.perlmod_items:
            perlmod_lay.addWidget(item)
        perlmod_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par16 = DOXYGEN_PROJECT_PAGES["Preprocessor"]
        self.preproc_items = [
            DoxyCheckBox(self.par16, "ENABLE_PREPROCESSING"),
            DoxyCheckBox(self.par16, "MACRO_EXPANSION"),
            DoxyCheckBox(self.par16, "EXPAND_ONLY_PREDEF"),
            DoxyCheckBox(self.par16, "SEARCH_INCLUDES"),
            DoxyLineBtn4(self.par16, "INCLUDE_PATH"),
            DoxyTextEdit(self.par16, "INCLUDE_PATH", []),
            DoxyLineBtn3(self.par16, "INCLUDE_FILE_PATTERNS"),
            DoxyTextEdit(self.par16, "INCLUDE_FILE_PATTERNS"),
            DoxyLineBtn3(self.par16, "PREDEFINED"),
            DoxyTextEdit(self.par16, "PREDEFINED", []),
            DoxyLineBtn3(self.par16, "EXPAND_AS_DEFINED"),
            DoxyTextEdit(self.par16, "EXPAND_AS_DEFINED", []),
            DoxyCheckBox(self.par16, "SKIP_FUNCTION_MACROS")
        ]
        preproc_lay = DOXYGEN_PROJECT_PAGES["Preprocessor"].layout
        for item in self.preproc_items:
            preproc_lay.addWidget(item)
        preproc_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par17 = DOXYGEN_PROJECT_PAGES["External"]
        self.external_items = [
            DoxyLineBtn4(self.par17, "TAGFILES"),
            DoxyTextEdit(self.par17, "TAGFILES", []),
            DoxyLineBtn1(self.par17, "GENERATE_TAGFILE"),
            DoxyCheckBox(self.par17, "ALLEXTERNALS"),
            DoxyCheckBox(self.par17, "EXTERNAL_GROUPS"),
            DoxyCheckBox(self.par17, "EXTERNAL_PAGES")
        ]
        external_lay = DOXYGEN_PROJECT_PAGES["External"].layout
        for item in self.external_items:
            external_lay.addWidget(item)
        external_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par18 = DOXYGEN_PROJECT_PAGES["Dot"]
        self.dot_items = [
            DoxyCheckBox(self.par18, "HIDE_UNDOC_RELATIONS"),
            DoxyCheckBox(self.par18, "HAVE_DOT"),
            DoxySpinEdit(self.par18, "DOT_NUM_THREADS", 0,  64,  0),
            DoxySpinEdit(self.par18, "DOT_BATCH_SIZE", 0, 100, 50),
            DoxyLineEdit(self.par18, "DOT_COMMON_ATTR"),
            DoxyLineEdit(self.par18, "DOT_EDGE_ATTR"),
            DoxyLineEdit(self.par18, "DOT_NODE_ATTR"),
            DoxyLineBtn1(self.par18, "DOT_FONTPATH"),
            DoxyComboBox(self.par18, "CLASS_GRAPH", [
                "YES",
                "NO",
                "TEXT",
                "GRAPH",
                "BUILTIN"]),
            DoxyCheckBox(self.par18, "COLLABORATION_GRAPH"),
            DoxyCheckBox(self.par18, "GROUP_PATHS"),
            DoxyCheckBox(self.par18, "UML_LOOK"),
            DoxySpinEdit(self.par18, "UML_LIMIT_NUM_FIELDS", 0, 100, 10),
            DoxySpinEdit(self.par18, "UML_MAX_EDGE_LABELS" , 0, 100, 10),
            DoxyComboBox(self.par18, "DOT_UML_DETAILS", ["NO", "YES", "NONE"]),
            DoxySpinEdit(self.par18, "DOT_WRAP_THRESHOLD", 0, 100, 17),
            DoxyCheckBox(self.par18, "TEMPLATE_RELATIONS"),
            DoxyCheckBox(self.par18, "INCLUDE_GRAPH"),
            DoxyCheckBox(self.par18, "INCLUDEED_BY_GRAPH"),
            DoxyCheckBox(self.par18, "CALL_GRAPH"),
            DoxyCheckBox(self.par18, "CALLER_GRAPH"),
            DoxyCheckBox(self.par18, "GRAPHICAL_HIEARCHY"),
            DoxyCheckBox(self.par18, "DIRECTORY_GRAPH"),
            DoxySpinEdit(self.par18, "DIR_GRAPH_MAX_DEPTH", 1, 100, 1),
            DoxyComboBox(self.par18, "DOT_IMAGE_FORMAT", [
                "png",
                "jpg",
                "gif",
                "svg",
                
                "png:cairo",
                "png:cairo:cairo",
                "png:cairo:gd",
                "png:cairo:gdiplus",
                
                "png:gd",
                "png:gd:gd",
                
                "png:gdiplus",
                "png:gdiplus:gdiplus",
                
                "svg:cairo",
                "svg:cairo:cairo",
                
                "svg:svg",
                "svg:svg:core",
                
                "gif:cairo",
                "gif:cairo:gd",
                "gif:cairo:gdiplus",
                
                "gif:gd",
                "gif:gd:gd",
                
                "gif:gdiplus",
                "gif:gdiplus:gdiplus",
                
                "jpg:cairo",
                "jpg:cairo:gd",
                "jpg:cairo:gdiplus",
                
                "jpg:gd",
                "jpg:gd:gd",
                
                "jpg:gdiplus",
                "jpg:gdiplus:gdiplus"]),
            DoxyCheckBox(self.par18, "INTERACTIVE_SVG"),
            DoxyLineBtn1(self.par18, "DOT_PATH"),
            DoxyLineBtn4(self.par18, "DOTFILE_DIRS"),
            DoxyTextEdit(self.par18, "DORFILE_DIRS", []),
            DoxyLineBtn1(self.par18, "DIA_PATH"),
            DoxyLineBtn4(self.par18, "DIAFILE_DIRS"),
            DoxyTextEdit(self.par18, "DIAFILE_DIRS", []),
            DoxyLineBtn1(self.par18, "PLANTUM_JAR_PATH"),
            DoxyLineBtn1(self.par18, "PLANTIM_CFG_FILE"),
            DoxyLineBtn4(self.par18, "PLANTUM_INCLUDE_PATH"),
            DoxyTextEdit(self.par18, "PLANTUM_INCLUDE_PATH", []),
            DoxyLineBtn4(self.par18, "PLANTUMFILE_DIRS"),
            DoxyTextEdit(self.par18, "PLANTUMFILE_DIRS", []),
            DoxyLineBtn1(self.par18, "MERMAID_PATH"),
            DoxyLineBtn1(self.par18, "MERMAID_CONFIG_FILE"),
            DoxyComboBox(self.par18, "MERMAID_RENDER_MODE", [
                "AUTO",
                "CLI",
                "CLIENT_SIDE"]),
            DoxyLineEdit(self.par18, "MERMAID_JS_URL"),
            DoxyLineBtn4(self.par18, "MERMAIDFILE_DIRS"),
            DoxyTextEdit(self.par18, "MERMAIDFILE_DIRS", []),
            DoxySpinEdit(self.par18, "DOT_GRAPH_MAX_NODES", 0, 100, 50),
            DoxySpinEdit(self.par18, "MAX_DOT_GRAPH_DEPTH", 0, 100,  0),
            DoxyCheckBox(self.par18, "GENERATE_LEGEND"),
            DoxyCheckBox(self.par18, "DOT_CLEANUP"),
            DoxyLineBtn1(self.par18, "MSCGEN_TOOL"),
            DoxyLineBtn4(self.par18, "MSCFILE_DIRS"),
            DoxyTextEdit(self.par18, "MSCFILE_DIRS", [])
        ]
        dot_lay = DOXYGEN_PROJECT_PAGES["Dot"].layout
        for item in self.dot_items:
            dot_lay.addWidget(item)
        dot_lay.addStretch()
        
        # -----------------------------------------------------------
        self.scroll_area.setWidget(self.expert_pages)
        self.expert_splitter_h.addWidget(self.scroll_area)
        self.expert_splitter_h.setSizes([220, 700])

        self.html_preview = QTextEdit()
        self.html_preview.setAcceptRichText(True)
        self.html_preview.setHtml(
            "<b>Project</b><br><p>Hier erscheinen einfache HTML-formatierte Texte. "
            "Zum Beispiel ist <b>foo</b> fett.</p>"
        )
        self.expert_splitter_v.addWidget(top_host)
        self.expert_splitter_v.addWidget(self.html_preview)
        self.expert_splitter_v.setSizes([420, 180])

        self.list_categories.setCurrentRow(1)
        self.list_categories.setCurrentRow(0)
        return page
        
    def _on_expert_item_changed(self, text):
        if not text:
            return
        page = DOXYGEN_PROJECT_PAGES.get(text)
        if page:
            self.expert_pages.setCurrentWidget(page.area)
    
    def _build_run_tab(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        txt = QTextEdit()
        txt.setReadOnly(False)
        txt.setHtml("<b>DoxyGen Run</b><br><p>Hier können Lauf-Ausgaben und Hinweise stehen.</p>")
        lay.addWidget(txt)
        self.run_text = txt
        return page
                
    def _locales_dir(self) -> Path:
        return Path(__file__).resolve().parents[2] / "data" / "po" / "locales"
    
    def show_help_for_key(self, help_key: str, title: str = ""):
        translated = share.locales.tr(help_key)
        self.html_preview.clear()
        self.html_preview.setHtml(translated)
    
    def _project_payload(self, path: str) -> dict:
        now = datetime.now()
        p = Path(path)
        return {
            "header": {
                "format"        : HEADER_FORMAT,
                "tool"          : HEADER_TOOL,
                "kind"          : HEADER_KIND,
                "version"       : HEADER_VERSION,
            },
            "meta": {
                "date"          : now.strftime("%Y-%m-%d"),
                "time"          : now.strftime("%H:%M:%S"),
                "filename"      : p.name,
                "filepath"      : str(p),
            },
        }

    def _validate_payload(self, data: dict):
        if not isinstance(data, dict):
            return False, share.locales.tr("The JSON-File is not a valid project file.")
        header = data.get("header")
        if not isinstance(header, dict):
            return False, share.locales.tr("missing Header-Information's.")
        if header.get("format") != HEADER_FORMAT:
            return False, share.locales.tr("project format is invalid.")
        if header.get("tool") != HEADER_TOOL:
            return False, share.locales.tr(f"the JSON-File does not cover the DoxyGen-Dialog: {header.get('tool', 'unknown')}).")
        if header.get("kind") != HEADER_KIND:
            return False, share.locales.tr("invalid project type.")
        return True, ""

    def _reload_project_list(self):
        self.project_list.clear()
        files = sorted(self.project_dir.glob("*.json"), key=lambda p: p.stat().st_mtime)
        for path in files:
            dt_text = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            item = QListWidgetItem(self.project_list)
            item.setData(Qt.UserRole, str(path))
            item.setSizeHint(QSize(220, 42))
            widget = ProjectListItemWidget(path.name, dt_text)
            self.project_list.addItem(item)
            self.project_list.setItemWidget(item, widget)

    def save_project_as(self):
        start = self.project_dir / "doxygen_project.json"
        path, _ = QFileDialog.getSaveFileName(self,
            share.locales.tr("Save DoxyGen-Project"),
            str(start),
            "JSON (*.json)")
        if not path:
            return
        if not path.lower().endswith(".json"):
            path += ".json"
        self.propath = path
        payload = self._project_payload(path)
        try:
            msg = share.locales.tr("Save Project As ...")
            fxt = share.locales.tr("Did you realy want to overwrite the file")
            
            reply = QMessageBox.question(self, msg, f"{fxt}:\n\n{Path(path).name}",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return
            
            self.state  = {
                "current_tab": self.tabs.currentIndex(),
                "expert_item": self.list_categories.currentRow()
            }
            
            self.save_items(self.project_items)
            self.save_items(self.build_items)
            self.save_items(self.messages_items)
            self.save_items(self.input_items)
            self.save_items(self.browser_items)
            self.save_items(self.index_items)
            self.save_items(self.html_items)
            self.save_items(self.latex_items)
            self.save_items(self.rtf_items)
            self.save_items(self.man_items)
            self.save_items(self.xml_items)
            self.save_items(self.docbook_items)
            self.save_items(self.autogen_items)
            self.save_items(self.sqlite3_items)
            self.save_items(self.perlmod_items)
            self.save_items(self.preproc_items)
            self.save_items(self.external_items)
            self.save_items(self.dot_items)
            
            
            payload["state" ] = self.state
            payload["config"] = self.config
            
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
                 
        except Exception as e:
            QMessageBox.critical(self, share.locales.tr("Save"), str(e))

    def _selected_project_path(self):
        item = self.project_list.currentItem()
        if item is None:
            return ""
        return item.data(Qt.UserRole) or ""

    def _load_selected_project(self):
        path = self._selected_project_path()
        if not path:
            path, _ = QFileDialog.getOpenFileName(self,
                share.locales.tr("Load DoxyGen-Project"),
                str(self.project_dir), "JSON (*.json)")
            if not path:
                return
        try:
            self.propath = path
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            ok, err = self._validate_payload(data)
            if not ok:
                QMessageBox.critical(self,
                    share.locales.tr("Invalide project file"),
                    err)
                return
            
            self.state = data.get("state", {})
            self.tabs.setCurrentIndex(int(self.state.get("current_tab", 0)))
            self.list_categories.setCurrentRow(int(self.state.get("expert_item", 0)))
            
            # ------------------------
            # set new item values ...
            # ------------------------
            self.config = data.get("config",{})
            
            self.load_items(self.project_items)
            self.load_items(self.build_items)
            self.load_items(self.messages_items)
            self.load_items(self.input_items)
            self.load_items(self.browser_items)
            self.load_items(self.index_items)
            self.load_items(self.html_items)
            self.load_items(self.latex_items)
            self.load_items(self.rtf_items)
            self.load_items(self.man_items)
            self.load_items(self.xml_items)
            self.load_items(self.docbook_items)
            self.load_items(self.autogen_items)
            self.load_items(self.sqlite3_items)
            self.load_items(self.perlmod_items)
            self.load_items(self.preproc_items)
            self.load_items(self.external_items)
            self.load_items(self.dot_items)
            
        except RuntimeError as e:
            QMessageBox.critical(self, share.locales.tr("Open"), str(e))
        except Exception as e:
            QMessageBox.critical(self, share.locales.tr("Open"), str(e))
    
    def save_items(self, items):
        for item in items:
            if isinstance(item, DoxyLineEdit):
                if not item.flag:
                    text = item.input.text()
                    self.config[item.help_str] = text
            elif isinstance(item, DoxyLineBtn1):
                text = item.input.input.text()
                self.config[item.help_str] = text
            elif isinstance(item, DoxyLineBtn3):
                text = item.input.input.text()
                self.config[item.help_str] = text
            elif isinstance(item, DoxyLineBtn4):
                text = item.input.input.text()
                self.config[item.help_str] = text
            elif isinstance(item, DoxySpinEdit):
                value = item.spin.value()
                self.config[item.help_str] = value
            elif isinstance(item, DoxyCheckBox):
                if item.check.isChecked():
                    self.config[item.help_str] = 1
                else:
                    self.config[item.help_str] = 0
            elif isinstance(item, DoxyTextEdit):
                text = item.edit.toPlainText()
                self.config[item.help_str] = text
            elif isinstance(item, DoxyComboBox):
                text = item.combo.currentText()
                self.config[item.help_str] = text
    
    def _to_int(self, value, default=0):
        try:
            if value is None:
                return default
            if isinstance(value, str):
                value = value.strip()
                if value == "":
                    return default
            return int(value)
        except Exception:
            return default
    
    def load_items(self, items):
        for item in items:
            if   isinstance(item, DoxyLineEdit): item.input.      setText(str(self.config.get(item.help_str, "")))
            elif isinstance(item, DoxyLineBtn1): item.input.input.setText(str(self.config.get(item.help_str, "")))
            elif isinstance(item, DoxyLineBtn3):
                if not item.input.flag:
                    item.input.input.setText(str(self.config.get(item.help_str, "")))
                else:
                    item.input.input.setText("")
            elif isinstance(item, DoxyLineBtn4):
                if not item.input.flag:
                    item.input.input.setText(str(self.config.get(item.help_str, "")))
                else:
                    item.input.input.setText("")
            elif isinstance(item, DoxyCheckBox):
                check = self._to_int(self.config.get(item.help_str, 0), 0)
                if check:
                    item.check.setChecked(True)
                else:
                    item.check.setChecked(False)
            elif isinstance(item, DoxyTextEdit):
                item.edit.clear()
                item.edit.appendPlainText(str(self.config.get(item.help_str, "")))
            elif isinstance(item, DoxySpinEdit): item.spin.setValue(self._to_int(self.config.get(item.help_str, 0), 0))
            elif isinstance(item, DoxyComboBox):
                index = item.combo.findText(str(self.config.get(item.help_str, "English")))
                if index >= 0:
                    item.combo.setCurrentIndex(index)
    
    def _delete_selected_project(self):
        path = self._selected_project_path()
        if not path:
            return
        msg = share.locales.tr("Would you realy delte the Project?")
        fxt = share.locales.tr("Delete Project")
        
        reply = QMessageBox.question(self, fxt, f"{msg}\n\n{Path(path).name}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  )
        if reply != QMessageBox.Yes:
            return
        try:
            os.remove(path)
            if self.current_project_path == path:
                self.current_project_path = ""
            self._reload_project_list()
        except Exception as e:
            QMessageBox.critical(self, share.locales.tr("Delete"), str(e))
