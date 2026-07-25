# ---------------------------------------------------------------------------
# File: cli.py - command line interface
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations
from pathlib     import PureWindowsPath, Path

from compiler.common.types     import *
from compiler.common.locale    import *
from compiler.common.error     import *

import sys
import os

# ---------------------------------------------------------------------------
# console argument parser from overgiven application command arguments ...
# ---------------------------------------------------------------------------
def args_func():
    args_parser     = ThrowingArgumentParser(
        prog        = "pas2asmjit",
        description = tr("Pascal to AsmJit/NASM compiler")
    )
    
    args_parser.add_argument(
        "source",
        nargs   = "?",
        default = None,
        help    = tr("Pascal source file (.pas/.pp)")
    )
    
    args_parser.add_argument(
        "--codepage",
        dest    = "code_page",
        type    = int,
        default = 65001,
        help    = "source codepage; default: UTF-8 (65001)"
    )
    
    args_parser.add_argument(
        "-v",
        "--verbose",
        dest    = "verbose",
        default = False,
        action  = "store_true",
        help    = tr("force debug messages.")
    )
    
    args_parser.add_argument(
        "-Us",
        "--packed-runtime",
        dest    = "packed_runtime",
        action  = "store_true",
        help    = tr("compile a system unit.")
    )
    
    # -------------------------------------------------------------
    # force overwriten old files with new content ...
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--force",
        dest    = "forcewrite",
        action  = "store_true",
        help    = tr("Force writen output (no interaction)")
    )
    
    # -------------------------------------------------------------
    # emitter for nasm compatible assembly code
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--asm",
        action  = "store_true",
        dest    = "asmoutput",
        help    = tr("Generate NASM compatible assembly output")
    )
    
    # -------------------------------------------------------------
    # emitter for AsmJIT C++ code ...
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--asmjit",
        action  = "store_true",
        dest    = "asmjitoutput",
        help    = tr("Generate AsmJIT C++ output")
    )
    
    # -------------------------------------------------------------
    # emitter for creating a Windows dll ...
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--dll",
        action  = "store_true",
        dest    = "dlloutputt",
        help    = tr("Build as DLL")
    )
    
    # -------------------------------------------------------------
    # emitter for creating a Windows exe ...
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--exe",
        action  = "store_true",
        dest    = "exeoutput",
        help    = tr("Build EXE file")
    )
    
    # -------------------------------------------------------------
    # --define=<macro>
    # Example: pas.exe -D DLL_API test.pas
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-D",
        "--define",
        dest    = "define",
        action  = "append",
        default = [],
        help    = tr("Define preprocessor symbol, e.g. -D DLL_API")
    )

    # -------------------------------------------------------------
    # -T<target>
    # Common Target OS identifiers
    # Example: pas.exe -T       win64 test.pas
    #          pas.exe --target win64 test.pas
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-T",
        "--target",
        dest    = "target",
        choices = [ "dos"       , # compile for MS-Dos      16-bit
                    "dos16"     , # placeholder for "dos"
                    "win16"     , # compile for Windows    3.1 16-bit
                    "winnt"     , # compile for Windows NT 3.5 32-bit
                    "nt35"      , # compile for Windows NT 3.5 32-bit
                    "win32"     , # compile for Windows        32-bit
                    "win64"     , # compile for Windows        64-bit
        ],
        default = "win64",
        help    = tr("Target OS Platform")
    )
    
    # -------------------------------------------------------------
    # --fpcsignature=<str>
    # Beispiel: pas.exe --signature="MyApp 1.2.3 (build 4567)"
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--signature",
        default = "PAS 0.0.1 win64",
        dest    = "signature",
        help    = tr("Replace the ident string in the .fpc_version "
                     "section of produced object.")
    )
    
    # -------------------------------------------------------------
    # --linkerversion=<Major.Minor>
    # Beispiel: pas.exe --linkerversion=8
    #
    # Name    | Major | Minor
    # --------|-------|-------
    # 95      |    4  |  0
    # 98      |    4  | 10
    # NE      |    4  | 90
    # 2000    |    5  |  0
    # XP      |    5  |  1
    # 2003    |    5  |  2
    # Vista   |    6  |  0
    # 7       |    6  |  1
    # 8       |    6  |  2
    # 8.1     |    6  |  3
    # 10 / 11 |   10  |  0
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--linkerversion",
        dest    = "linkerversion",
        help    = tr("Sets the minimum OS version fields in the "
                     "PE optional header."),
        choices = [ "3"   , "3.1" , "3.11",
                    "4"   , "4.0" , "4.10", "4.90" ,
                    "5"   , "5.0" , "5.1" , "5.2"  ,
                    "6"   , "6.0" , "6.1" , "6.2"  , "6.3",
                    "7"   ,
                    "8"   , "8.1" ,
                    "10"  , "10.0",
                    "11"  ,
                    "95"  ,
                    "98"  , "ME"  ,
                    "2000", "XP"  ,
                    "2003", "Vista"
        ],
        default = "10"
    )
    
    # -------------------------------------------------------------
    # emitter backend ...
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-B",
        "--backend",
        dest     =  "backend",
        nargs    =  "?",
        choices  = ["c++", "asm", "obj", "res", "dll", "exe",
                    # ------ #
                    "asmjit",
                    "nasm",
                    "objfile",
                    "resfile",
                    "dllfile",
                    "exefile",
        ],
        default  =  "asmjit",
        help     =  tr("Code backend: asmjit, nasm, obj, dll, exe.")
    )
    
    # -------------------------------------------------------------
    # Compiler mode
    # Beispiel: -M pascal -T win32 test.c
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-M",
        "--mode",
        dest    = "compilermode",
        nargs   = "?",
        choices = ["pp", "pas", "pascal", "c", "cc", "cpp"],
        default = "pas",
        help    = tr("Specify the Compiler mode.")
    )
    
    # -------------------------------------------------------------
    # modules include path
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-Fi",
        "--include-path",
        dest    = "include_path",
        metavar = "DIRECTORY",
        action  = "append",
        default = [],
        help    = tr("Add include file search path.")
    )
    
    # -------------------------------------------------------------
    # search path for units ...
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-Fu",
        "--unit-path",
        dest    = "unit_paths",
        metavar = "DIRECTORY",
        action  = "append",
        default = [],
        help    = tr("Add Pascal unit search directory.")
    )
    
    # -------------------------------------------------------------
    # Ausgabeverzeichnis für alle erzeugten Compilerdateien:
    #
    #   .o
    #   .pui
    #   .exe
    #   .dll
    #   .asm
    #
    # Relative Pfade werden gegen das aktuelle Arbeitsverzeichnis
    # aufgelöst. Der angegebene Pfad wird unverändert verwendet;
    # es wird kein zusätzliches x32/x64-Unterverzeichnis angehängt.
    #
    # Beispiel:
    #
    #   -FE x32/Crypto
    #
    # ergibt:
    #
    #   <cwd>/x32/Crypto
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-FE",
        "--output-path",
        dest    = "output",
        default = ".",
        metavar = "DIRECTORY",
        help    = tr(
            "Set the output directory for generated compiler files."
        )
    )
    
    # -------------------------------------------------------------
    # Suchpfade für relocatable COFF-Objektdateien.
    #
    # Mehrfach verwendbar:
    #
    #   pas2asmjit -Fo obj -Fo thirdparty/obj test.pas
    #
    # Die resultierende Liste wird in:
    #
    #   CDATA.link_object_paths
    #
    # gespeichert und für folgende Direktiven verwendet:
    #
    #   {$L foo.o}
    #   {$link foo.o}
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-Fo",
        "--objpath",
        "--object-path",
        dest    = "objpath",
        action  = "append",
        default = [],
        metavar = "DIRECTORY",
        help    = tr(
            "Add COFF object file search directory. "
            "The option may be specified more than once."
        )
    )

    # -------------------------------------------------------------
    # Suchpfade für statische Archive.
    #
    # Mehrfach verwendbar:
    #
    #   pas2asmjit -Fl lib -Fl thirdparty/lib test.pas
    #
    # Die resultierende Liste wird in:
    #
    #   CDATA.link_library_paths
    #
    # gespeichert und für:
    #
    #   {$linklib libfoo.a}
    #
    # verwendet.
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-Fl",
        "--libpath",
        "--library-path",
        dest    = "libpath",
        action  = "append",
        default = [],
        metavar = "DIRECTORY",
        help    = tr(
            "Add archive/library search directory. "
            "The option may be specified more than once."
        )
    )
    
    # -------------------------------------------------------------
    # --info V  -> informations about the compiler
    # Example: pas.exe --info V
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-i",
        "--info",
        dest    =   "information",
        metavar =   "INFO",
        nargs   =   "?",
        const   =   "",
        choices = [ "",
                    "V",    # version information's
                    "W",
                    "TP"
        ],
        default = None,
        help    = tr("Help informations about the compiler")
    )
    
    return args_parser

# ---------------------------------------------------------------------------
#  Prüft und erzeugt das mit -FE angegebene Ausgabeverzeichnis.
#
#  Wichtig:
#
#    * Ein relativer Pfad ist unter Windows vollkommen gültig.
#    * Er wird gegen das aktuelle Arbeitsverzeichnis aufgelöst.
#    * Es wird kein Laufwerksbuchstabe vom Benutzer verlangt.
#    * Es wird kein automatisches x16/x32/x64-Unterverzeichnis
#      an einen expliziten -FE-Pfad angehängt.
#    * Der Pfad bezeichnet immer ein Verzeichnis, niemals eine Datei.
# ---------------------------------------------------------------------------
def validate_output_path(
    value
):
    if value is None:
        value = "."

    try:
        value = os.fspath(
            value
        )
    except TypeError:
        raise RuntimeError(
            tr("invalid output directory")
            + ": "
            + repr(value)
        ) from None

    value = value.strip()

    if not value:
        value = "."

    value = os.path.expandvars(
        os.path.expanduser(
            value
        )
    )

    # os.path.abspath() ergänzt unter Windows bei relativen Pfaden
    # automatisch das aktuelle Laufwerk und Arbeitsverzeichnis.
    #
    # Beispiel:
    #
    #   x32/Crypto
    #
    # wird zu:
    #
    #   T:\\GitHub\\dBase2Many\\src\\asmjit\\x32\\Crypto
    output_path = os.path.abspath(
        os.path.normpath(
            value
        )
    )

    path = Path(
        output_path
    )

    if path.exists():
        if not path.is_dir():
            CDATA.LastErrorCode = (
                LastError.PATH_NO_DIRECTORY
            )

            raise RuntimeError(
                f"{tr('output path is not a directory')}: "
                f"{output_path}"
            )
    else:
        try:
            path.mkdir(
                parents=True,
                exist_ok=True
            )
        except OSError as exc:
            CDATA.LastErrorCode = (
                LastError.DIRECTORY_DONT_EXISTS
            )

            raise RuntimeError(
                f"{tr('could not create output directory')}: "
                f"{output_path}: {exc}"
            ) from None

    if not os.access(
        output_path,
        os.R_OK
    ):
        CDATA.LastErrorCode = (
            LastError.DIRECTORY_NOT_READABLE
        )

        raise RuntimeError(
            f"{tr('output directory is not readable')}: "
            f"{output_path}"
        )

    if not os.access(
        output_path,
        os.W_OK
    ):
        CDATA.LastErrorCode = (
            LastError.DIRECTORY_NOT_WRITEABLE
        )

        raise RuntimeError(
            f"{tr('output directory is not writeable')}: "
            f"{output_path}"
        )

    # Einheitlicher absoluter Ausgabepfad für alle Compilerstufen.
    CDATA.CurrentWorkingDir = output_path
    CDATA.ExeOutputDir      = output_path
    CDATA.output_dir        = output_path
    CDATA.out_dir           = output_path

    # Kompatibilität mit vorhandenen Treiberversionen, die
    # CDATA.exe_file vorübergehend als Ausgabeverzeichnis behandeln.
    CDATA.exe_file = output_path

    if CDATA.debug_mode:
        print(
            "Compiler output directory:",
            output_path
        )

    return {
        "kind": "directory",
        "path": path,
        "absolute_path": output_path
    }

# ---------------------------------------------------------------------------
#  Normalisiert eine Folge von Suchverzeichnissen.
#
#  Eigenschaften:
#
#    * Umgebungsvariablen und "~" werden aufgelöst.
#    * Relative Pfade werden relativ zu base_directory interpretiert.
#    * Doppelte Pfade werden unabhängig von Groß-/Kleinschreibung entfernt.
#    * Die vom Benutzer angegebene Reihenfolge bleibt erhalten.
#    * Optional wird geprüft, ob jeder Eintrag ein Verzeichnis ist.
# ---------------------------------------------------------------------------
def normalize_search_paths(
    paths,
    base_directory=None,
    require_directory=True
):
    result = []
    seen = set()

    if base_directory is None:
        base_directory = os.getcwd()

    base_directory = os.path.abspath(
        os.path.expandvars(
            os.path.expanduser(
                os.fspath(base_directory)
            )
        )
    )

    for raw_path in paths or []:
        if raw_path is None:
            continue

        try:
            raw_path = os.fspath(
                raw_path
            )
        except TypeError:
            raise RuntimeError(
                tr("invalid search path")
                + ": "
                + repr(raw_path)
            ) from None

        raw_path = raw_path.strip()

        if not raw_path:
            continue

        expanded_path = os.path.expandvars(
            os.path.expanduser(
                raw_path
            )
        )

        if not os.path.isabs(
            expanded_path
        ):
            expanded_path = os.path.join(
                base_directory,
                expanded_path
            )

        absolute_path = os.path.abspath(
            expanded_path
        )

        normalized_path = os.path.normpath(
            absolute_path
        )

        key = os.path.normcase(
            normalized_path
        )

        if key in seen:
            continue

        if require_directory:
            if not os.path.exists(
                normalized_path
            ):
                raise FileNotFoundError(
                    tr("search directory does not exist")
                    + ": "
                    + normalized_path
                )

            if not os.path.isdir(
                normalized_path
            ):
                raise NotADirectoryError(
                    tr("search path is not a directory")
                    + ": "
                    + normalized_path
                )

            if not os.access(
                normalized_path,
                os.R_OK
            ):
                raise RuntimeError(
                    tr("search directory is not readable")
                    + ": "
                    + normalized_path
                )

        seen.add(
            key
        )

        result.append(
            normalized_path
        )

    return result


# ---------------------------------------------------------------------------
#  Erzeugt die endgültigen Suchpfadlisten für Objektdateien und Archive.
#
#  Suchreihenfolge für Objektdateien:
#
#    1. Verzeichnis der Pascal-Quelldatei
#    2. aktuelles Arbeitsverzeichnis
#    3. alle mehrfach angegebenen -Fo-Verzeichnisse
#
#  Suchreihenfolge für Archive:
#
#    1. Verzeichnis der Pascal-Quelldatei
#    2. aktuelles Arbeitsverzeichnis
#    3. alle -Fo-Verzeichnisse
#    4. alle mehrfach angegebenen -Fl-Verzeichnisse
#
#  Dadurch kann ein gemeinsames Verzeichnis sowohl .o- als auch .a-Dateien
#  enthalten. -Fl kann zusätzlich für reine Bibliotheksverzeichnisse benutzt
#  werden.
# ---------------------------------------------------------------------------
def collect_link_search_paths(
    args
):
    current_directory = os.path.abspath(
        os.getcwd()
    )

    source_directory = current_directory

    source_filename = getattr(
        args,
        "source",
        None
    )

    if source_filename:
        source_filename = os.path.expandvars(
            os.path.expanduser(
                os.fspath(
                    source_filename
                )
            )
        )

        if not os.path.isabs(
            source_filename
        ):
            source_filename = os.path.join(
                current_directory,
                source_filename
            )

        source_directory = os.path.dirname(
            os.path.abspath(
                source_filename
            )
        )

    object_candidates = [
        source_directory,
        current_directory
    ]

    object_candidates.extend(
        list(
            getattr(
                args,
                "objpath",
                []
            )
            or []
        )
    )

    library_candidates = list(
        object_candidates
    )

    library_candidates.extend(
        list(
            getattr(
                args,
                "libpath",
                []
            )
            or []
        )
    )

    object_paths = normalize_search_paths(
        object_candidates,
        base_directory=current_directory,
        require_directory=True
    )

    library_paths = normalize_search_paths(
        library_candidates,
        base_directory=current_directory,
        require_directory=True
    )

    return (
        object_paths,
        library_paths
    )
    
def handle_args(args):
    CDATA.IncludePaths = list(args.include_path or [])
    CDATA.Defines      = list(args.define       or [])
    
    CDATA.force_write  = args.forcewrite
    CDATA.code_page    = args.code_page
    
    CDATA.inc_dir      = list(args.include_path or [])
    
    # -FE bezeichnet immer ein Ausgabeverzeichnis. Die Funktion
    # normalisiert auch relative Pfade und schreibt den absoluten
    # Pfad nach CDATA.ExeOutputDir, CDATA.output_dir und
    # CDATA.CurrentWorkingDir.
    result = validate_output_path(
        args.output
    )

    args.output = result[
        "absolute_path"
    ]

    (
        object_search_paths,
        library_search_paths
    ) = collect_link_search_paths(
        args
    )

    # Wichtig:
    #
    # Nicht an möglicherweise vorhandene globale Listen anhängen. Ein
    # Compilerprozess kann mehrere Läufe ausführen; sonst würden Pfade aus
    # einem vorherigen Lauf erhalten bleiben.
    CDATA.link_object_paths = list(
        object_search_paths
    )

    CDATA.link_library_paths = list(
        library_search_paths
    )

    # Optionale Kompatibilitätsnamen für ältere Module.
    CDATA.ObjectPaths = list(
        object_search_paths
    )

    CDATA.LibraryPaths = list(
        library_search_paths
    )

    if CDATA.debug_mode:
        print("COFF object search paths:")

        for path in CDATA.link_object_paths:
            print("  ", path)

        print("Archive search paths:")

        for path in CDATA.link_library_paths:
            print("  ", path)

    CDATA.args_backend = args.backend
    CDATA.UnitPaths = normalize_search_paths(
        args.unit_paths
    )
    CDATA.packed_runtime = bool(
        args.packed_runtime
    )

    if args.verbose:
        CDATA.args_verbose = True
    else:
        CDATA.args_verbose = False

    #if args.info is not None:
    #    if args.info == "":
    #        print("Common Info")
    #    elif args.info == "V":
    #        print("Version")
    #    elif args.info == "W":
    #        print("Warning")
    #    elif args.info == "TP":
    #        print(tr("Target platform"))
    
    return args
