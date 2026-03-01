# -------------------------------------------------------------------------------
# File:   build.py - create customized chm help
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
#         all rights reserved
#
# Merge multiple decompiled CHM source folders into one CHM project,
# preserving folder structure and merging existing .hhc / .hhk.
#
# It will:
# - Copy each source folder into OUT/<source_name>/... (structure preserved)
# - Find one .hhc and one .hhk per source (optional per source)
# - Merge TOCs into one Merged.hhc (each source becomes a top-level "book")
# - Merge Indexes into one Merged.hhk (concatenate entries)
# - Generate Merged.hhp referencing Merged.hhc / Merged.hhk
# - Optionally compile with hhc.exe
#
# Usage (Windows):
# python merge_chm_keep_structure.py ^
#     --sources "T:\\help\\chmA_src" "T:\\help\\chmB_src" ^
#     --out "T:\\help\\merged_build" ^
#     --project-name "MergedHelp" ^
#     --default-topic "index.html" ^
#     --compile ^
#     --hhc "C:\\Program Files (x86)\\HTML Help Workshop\\hhc.exe" ^
#     --clean
# -------------------------------------------------------------------------------
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Tuple, Dict, List

HTML_EXTS = {".html", ".htm"}

HHC_HEADER = """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<HTML>
<HEAD>
<meta name="GENERATOR" content="build.py">
<!-- Sitemap 1.0 -->
</HEAD><BODY>
<UL>
"""
HHC_FOOTER = """</UL>
</BODY></HTML>
"""
HHK_HEADER = HHC_HEADER
HHK_FOOTER = HHC_FOOTER


# -------------------------
# Basic helpers
# -------------------------

def safe_name(s: str) -> str:
    s = s.strip()
    s = re.sub(r"[^\w\-\.]+", "_", s, flags=re.UNICODE)
    return s[:60] if len(s) > 60 else s


def to_win_sep(s: str) -> str:
    return s.replace("/", "\\")


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return p.read_text(encoding="cp1252", errors="replace")


def write_text(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def parse_source_arg(s: str) -> Tuple[Path, str]:
    # "path|Deutsch" / "path|English" / "path"
    if "|" in s:
        path_str, label = s.split("|", 1)
        return Path(path_str).resolve(), label.strip()
    return Path(s).resolve(), ""


def find_first_file(root: Path, exts: Tuple[str, ...]) -> Optional[Path]:
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts:
            return p
    return None


def iter_html_files(root: Path) -> List[Path]:
    res: List[Path] = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in HTML_EXTS:
            res.append(p)
    return res


# -------------------------
# Copy logic that preserves dark/<lang>/...
# -------------------------
def detect_src_base_for_dark(src_root: Path) -> Path:
    parts = [p.lower() for p in src_root.parts]
    if "dark" in parts:
        i = parts.index("dark")
        # base = path up to before "dark"
        return Path(*src_root.parts[:i]) if i > 0 else src_root
    return src_root


def copy_tree_preserve_base(src_root: Path, out_dir: Path, src_base: Path) -> None:
    for p in src_root.rglob("*"):
        if p.is_file() and p.suffix.lower() == ".chm":
            continue
        rel = p.relative_to(src_base)
        target = out_dir / rel
        if p.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)


# -------------------------
# HHC/HHK parsing helpers
# -------------------------

def extract_first_ul_inner(html: str) -> str:
    m = re.search(r"(?is)<ul\b[^>]*>(.*?)</ul>", html)
    return m.group(1).strip() if m else ""


def make_book_node(title: str, inner_ul_html: str) -> str:
    title_esc = (
        title.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
    )
    inner = inner_ul_html.strip()
    if inner:
        return f"""<LI> <OBJECT type="text/sitemap">
    <param name="Name" value="{title_esc}">
</OBJECT>
<UL>
{inner}
</UL>
"""
    return f"""<LI> <OBJECT type="text/sitemap">
    <param name="Name" value="{title_esc}">
</OBJECT>
"""


_TAG_RE = re.compile(r"(?is)<(/?)(ul|li)\b")


def split_top_level_li_blocks(inner_ul_html: str) -> List[str]:
    s = inner_ul_html.strip()
    if not s:
        return []

    blocks: List[str] = []
    current_start: Optional[int] = None
    ul_depth = 0

    for m in _TAG_RE.finditer(s):
        closing = (m.group(1) == "/")
        tag = m.group(2).lower()
        idx = m.start()

        if tag == "ul":
            ul_depth = max(0, ul_depth - 1) if closing else ul_depth + 1
            continue

        if tag == "li":
            if not closing and ul_depth == 0:
                if current_start is None:
                    current_start = idx
                else:
                    blocks.append(s[current_start:idx].strip())
                    current_start = idx

    if current_start is not None:
        blocks.append(s[current_start:].strip())

    return [b for b in blocks if b]


def extract_name_from_li(li_block: str) -> str:
    m = re.search(
        r'(?is)<param\b[^>]*\bname\s*=\s*["\']Name["\']\s*\bvalue\s*=\s*["\']([^"\']+)["\']',
        li_block
    )
    return m.group(1).strip() if m else ""


def extract_child_ul_inner_from_li(li_block: str) -> str:
    m = re.search(r"(?is)<ul\b[^>]*>(.*?)</ul>", li_block)
    return m.group(1).strip() if m else ""


def _norm_name(v: str) -> str:
    return re.sub(r"\s+", " ", v.strip()).casefold()


def _norm_local(v: str) -> str:
    v = v.strip().replace("/", "\\")
    v = re.sub(r'(?i)^[.\\]+', "", v)
    v = v.split("#", 1)[0].split("?", 1)[0]
    v = re.sub(r"\\{2,}", r"\\", v)
    return v.casefold()


def toc_item_key(li_block: str) -> str:
    m_local = re.search(
        r'(?is)<param\b[^>]*\bname\s*=\s*["\']Local["\']\s*\bvalue\s*=\s*["\']([^"\']+)["\']',
        li_block
    )
    if m_local:
        return "local:" + _norm_local(m_local.group(1))

    m_name = re.search(
        r'(?is)<param\b[^>]*\bname\s*=\s*["\']Name["\']\s*\bvalue\s*=\s*["\']([^"\']+)["\']',
        li_block
    )
    if m_name:
        return "name:" + _norm_name(m_name.group(1))

    return ("raw:" + re.sub(r"\s+", " ", li_block.strip())[:160]).casefold()


def dedup_children(inner_ul_html: str) -> str:
    blocks = split_top_level_li_blocks(inner_ul_html)
    out: List[str] = []
    seen: set[str] = set()
    for b in blocks:
        k = toc_item_key(b)
        if k in seen:
            continue
        seen.add(k)
        out.append(b)
    return "\n".join(out)


def merge_children(existing_inner: str, new_inner: str) -> str:
    a = split_top_level_li_blocks(existing_inner)
    b = split_top_level_li_blocks(new_inner)
    out: List[str] = []
    seen: set[str] = set()

    for blk in a:
        k = toc_item_key(blk)
        if k not in seen:
            seen.add(k)
            out.append(blk)

    for blk in b:
        k = toc_item_key(blk)
        if k not in seen:
            seen.add(k)
            out.append(blk)

    return "\n".join(out)


def strip_self_child_root(children_inner_ul: str, book_title: str) -> str:
    blocks = split_top_level_li_blocks(children_inner_ul)
    if not blocks:
        return children_inner_ul

    first = blocks[0]
    first_name = extract_name_from_li(first)

    if _norm_name(first_name) != _norm_name(book_title):
        return children_inner_ul

    inner = extract_child_ul_inner_from_li(first)
    return inner.strip() if inner else children_inner_ul


def extract_root_name_and_children(inner_ul_html: str) -> Tuple[str, str]:
    s = inner_ul_html.strip()
    if not s:
        return "", ""

    top = split_top_level_li_blocks(s)
    if not top:
        return "", s

    root_li = top[0]
    root_name = extract_name_from_li(root_li)
    children = extract_child_ul_inner_from_li(root_li) or s

    # peel duplicated root layers
    for _ in range(3):
        if not root_name:
            break
        top2 = split_top_level_li_blocks(children)
        if len(top2) != 1:
            break
        n2 = extract_name_from_li(top2[0])
        if _norm_name(n2) != _norm_name(root_name):
            break
        c2 = extract_child_ul_inner_from_li(top2[0])
        if not c2:
            break
        children = c2

    return root_name, children


# -------------------------
# Rewrite Local keeping #anchor
# -------------------------

def split_url_suffix(v: str) -> Tuple[str, str]:
    # keep first occurrence of ? or # as suffix start
    for sep in ("?", "#"):
        idx = v.find(sep)
        if idx != -1:
            return v[:idx], v[idx:]
    return v, ""


def rewrite_local_params_by_relpath(html_text: str, *, src_root: Path, src_base: Path, out_dir: Path, project_dir: Path) -> str:
    """
    Rewrites <param name="Local" value="..."> to correct relpath from project_dir
    to the copied target under out_dir, preserving #anchors.
    """
    pattern = re.compile(
        r'(?is)(<param\b[^>]*\bname\s*=\s*["\']Local["\'][^>]*\bvalue\s*=\s*["\'])([^"\']+)(["\'][^>]*>)'
    )

    def repl(m: re.Match) -> str:
        before, val, after = m.group(1), m.group(2), m.group(3)
        v = val.strip()
        v_norm = v.replace("\\", "/")

        if re.match(r"(?i)^(https?://|mailto:|ftp://|file://)", v_norm):
            return m.group(0)
        if v_norm.startswith(("/", "#")):
            return m.group(0)

        path_part, suffix = split_url_suffix(v_norm)
        path_part = path_part.strip()

        # Resolve file relative to src_root (TOC paths are typically relative to the manual root)
        src_candidate = (src_root / path_part).resolve()
        if not src_candidate.exists():
            # don't break if not found
            return m.group(0)

        # Destination keeps path relative to src_base (so we preserve dark\de\...)
        rel_under_base = src_candidate.relative_to(src_base)
        dst_target = (out_dir / rel_under_base).resolve()

        rel_from_project = os.path.relpath(dst_target, start=project_dir)
        newv = to_win_sep(rel_from_project) + suffix  # KEEP #anchor / ?query
        return f"{before}{newv}{after}"

    return pattern.sub(repl, html_text)


# -------------------------
# HHP generation: [FILES] relative to project_dir
# -------------------------

def generate_hhp(project_name: str,
                 out_dir: Path,
                 project_dir: Path,
                 default_topic: Optional[str],
                 title: Optional[str],
                 language: str = "0x409 English (United States)") -> Path:
    project_safe = safe_name(project_name)
    hhp_path = project_dir / f"{project_safe}.hhp"
    chm_name = f"{project_safe}.chm"

    if not title:
        title = project_name

    # Default topic
    if not default_topic:
        # prefer dark\de\html\index.html if exists, else first index.html
        idx = None
        preferred = out_dir / "dark" / "de" / "html" / "index.html"
        if preferred.exists():
            idx = preferred
        else:
            for p in out_dir.rglob("index.html"):
                if p.is_file():
                    idx = p
                    break
            if not idx:
                for p in out_dir.rglob("index.htm"):
                    if p.is_file():
                        idx = p
                        break
        if idx:
            default_topic = to_win_sep(os.path.relpath(idx, start=project_dir))
        else:
            htmls = sorted(iter_html_files(out_dir), key=lambda p: p.as_posix().lower())
            default_topic = to_win_sep(os.path.relpath(htmls[0], start=project_dir)) if htmls else "index.html"
    else:
        dt = Path(default_topic)
        if not dt.is_absolute():
            dt = (out_dir / dt).resolve()
        default_topic = to_win_sep(os.path.relpath(dt, start=project_dir))

    merged_hhc = f"{project_safe}.hhc"
    merged_hhk = f"{project_safe}.hhk"

    files = sorted(iter_html_files(out_dir), key=lambda p: p.as_posix().lower())
    rel_files = [to_win_sep(os.path.relpath(p, start=project_dir)) for p in files]

    lines: List[str] = []
    lines.append("[OPTIONS]")
    lines.append(f"Compiled file={chm_name}")
    lines.append(f"Default topic={default_topic}")
    lines.append(f"Contents file={merged_hhc}")
    lines.append(f"Index file={merged_hhk}")
    lines.append(f"Title={title}")
    lines.append(f"Language={language}")
    lines.append("Binary TOC=Yes")
    lines.append("Compatibility=1.1 or later")
    lines.append("")
    lines.append("[FILES]")
    lines.extend(rel_files)
    lines.append("")

    write_text(hhp_path, "\n".join(lines))
    return hhp_path


# -------------------------
# Main
# -------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Merge CHM sources and generate HHP/HHC/HHK with correct relative paths.")
    ap.add_argument("--sources", nargs="+", required=True,
                    help='Source folders, optionally "path|Deutsch" or "path|English".')
    ap.add_argument("--out", required=True, help="Output folder (build root).")
    ap.add_argument("--project-name", required=True, help="Base name for .hhp/.hhc/.hhk/.chm.")
    ap.add_argument("--project-subdir", default="chm", help="Subdir under OUT for project files.")
    ap.add_argument("--default-topic", default=None, help="Default topic (optional).")
    ap.add_argument("--title", default=None, help="CHM title (optional).")
    ap.add_argument("--hhc", default=None, help="Path to hhc.exe (needed for --compile).")
    ap.add_argument("--compile", action="store_true", help="Compile after generating.")
    ap.add_argument("--clean", action="store_true", help="Delete OUT folder first.")
    args = ap.parse_args()

    out_dir = Path(args.out).resolve()
    if args.clean and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    project_dir = (out_dir / args.project_subdir).resolve()
    project_dir.mkdir(parents=True, exist_ok=True)

    project_safe = safe_name(args.project_name)
    merged_hhc_path = project_dir / f"{project_safe}.hhc"
    merged_hhk_path = project_dir / f"{project_safe}.hhk"

    manuals: Dict[str, Dict[str, Dict[str, str]]] = {"Deutsch": {}, "English": {}}
    idx_entries: List[str] = []

    for src in args.sources:
        src_root, lang_label = parse_source_arg(src)
        if not src_root.exists():
            raise SystemExit(f"Source folder does not exist: {src_root}")

        lang = lang_label if lang_label in ("Deutsch", "English") else "Deutsch"

        # Ensure we preserve "dark\\<lang>\\..." if present
        src_base = detect_src_base_for_dark(src_root)

        # Copy into OUT preserving relpath from src_base
        copy_tree_preserve_base(src_root, out_dir, src_base)

        src_hhc = find_first_file(src_root, (".hhc",))
        src_hhk = find_first_file(src_root, (".hhk",))

        if src_hhc and src_hhc.is_file():
            hhc_html = read_text(src_hhc)
            hhc_html = rewrite_local_params_by_relpath(
                hhc_html, src_root=src_root, src_base=src_base, out_dir=out_dir, project_dir=project_dir
            )
            inner = extract_first_ul_inner(hhc_html)

            root_name, children = extract_root_name_and_children(inner)
            book_title = root_name if root_name else safe_name(src_root.name)

            children = dedup_children(children)
            children = strip_self_child_root(children, book_title)
            children = dedup_children(children)

            title_key = _norm_name(book_title)
            if title_key not in manuals[lang]:
                manuals[lang][title_key] = {"title": book_title, "children": children}
            else:
                manuals[lang][title_key]["children"] = merge_children(
                    manuals[lang][title_key]["children"],
                    children
                )

        if src_hhk and src_hhk.is_file():
            hhk_html = read_text(src_hhk)
            hhk_html = rewrite_local_params_by_relpath(
                hhk_html, src_root=src_root, src_base=src_base, out_dir=out_dir, project_dir=project_dir
            )
            inner_idx = extract_first_ul_inner(hhk_html)
            if inner_idx.strip():
                idx_entries.append(inner_idx)

    # Build merged TOC
    def manuals_inner(lang: str) -> str:
        items = sorted(manuals[lang].values(), key=lambda d: _norm_name(d["title"]))
        return "\n".join(make_book_node(d["title"], d["children"]) for d in items)

    de_inner = manuals_inner("Deutsch")
    en_inner = manuals_inner("English")

    root_inner = "\n".join([
        make_book_node("Deutsch / Überblick", de_inner),
        make_book_node("English / Overview", en_inner),
    ])

    merged_hhc = HHC_HEADER + make_book_node("Benutzer-Handbuch", root_inner) + HHC_FOOTER
    write_text(merged_hhc_path, merged_hhc)

    # Build merged Index
    merged_hhk = HHK_HEADER + ("\n".join(idx_entries) if idx_entries else "") + "\n" + HHK_FOOTER
    write_text(merged_hhk_path, merged_hhk)

    # Generate HHP with correct [FILES]
    hhp_path = generate_hhp(
        project_name=args.project_name,
        out_dir=out_dir,
        project_dir=project_dir,
        default_topic=args.default_topic,
        title=args.title,
    )

    print(f"Created: {hhp_path}")
    print(f"Created: {merged_hhc_path}")
    print(f"Created: {merged_hhk_path}")

    # Optional compile
    if args.compile:
        if not args.hhc:
            raise SystemExit("To compile, provide --hhc path to hhc.exe")
        hhc = Path(args.hhc).resolve()
        if not hhc.exists():
            raise SystemExit(f"hhc.exe not found: {hhc}")

        print(f"Compiling with: {hhc}")
        proc = subprocess.run(
            [str(hhc), str(hhp_path.name)],
            cwd=str(project_dir),
            capture_output=True,
            text=True
        )

        if proc.stdout.strip():
            print(proc.stdout)
        if proc.returncode != 0:
            if proc.stderr.strip():
                print(proc.stderr)
            return proc.returncode

        chm_path = project_dir / (safe_name(args.project_name) + ".chm")
        print(f"CHM created: {chm_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
    
"""
+-- html / C/C++ Überblick
|   +-- C/C++ Überblick
|   |   +-- Einstieg
|   |   +-- Navigation
|   +-- html / C/C++ Overview
|       +-- C/C++ Overview
|           +-- Basis
|           +-- Navigation

+-- Deutsch / Überblick
|   +-- C/C++ Überblick
|   |   +-- Einstieg
|   |   |
|   |   +-- Navigation
|   |   ...
|   ...
|   +-- Pascal Überlick
|   |   +-- Einstieg
|   |   |
|   |   +-- Navigation
|   |   ...
|   ...
|   +-- Python Überblick
|   |   +-- Einstieg
|   |   |
|   |   +-- Navigation
|   |   ...
|   ...
+-- English / Overview
|   +-- C/C++ Overview
|   |   +-- Basis
|   |   |
|   |   +-- Navigation
|   |   ...
|   ...
|   +-- Pascal Overview
|   |   +-- Basis
|   |   |
|   |   +-- Navigation
|   |   ...
|   ...
|   +-- Python Overview
|   |   +-- Basis
|   |   |
|   |   +-- Navigation
|   |   ...
|   ...
|
"""
