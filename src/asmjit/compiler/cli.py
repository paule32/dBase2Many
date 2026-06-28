# ---------------------------------------------------------------------------
# File: cli.py - command line interface
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

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
        "-o",
        "--output",
        default = None,
        help    = tr("Output directory")
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
        "--backend",
        dest     =  "backend",
        nargs    =  "?",
        choices  = ["c++", "asmjit",
                    "asm", "nasm",
                    "obj", "objfile",
                    "exe", "exefile",
        ],
        default  =  "asmjit",
        help     =  tr("Code backend: asmjit, nasm, objfile.")
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
        dest    = "includepath",
        action  = "append",
        default = [],
        help    = tr("Add include file search path.")
    )
    
    # -------------------------------------------------------------
    # executable output path ...
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-FE",
        dest    = "exe_output_dir",
        default = ".",
        help    = tr("Set output directory for executables.")
    )
    
    # -------------------------------------------------------------
    # --info V  -> informations about the compiler
    # Example: pas.exe --info V
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-i",
        "--info",
        dest    =   "information",
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

def handle_args(args):
    if args.exe_output_dir is not None:
        CDATA.ExeOutputDir = args.exe_output_dir
        #print("==> ", CDATA.CurrentWorkingDir)

    result = validate_output_path(args.exe_output_dir)
    if result["kind"] == "directory":
        return args
    if result["kind"] == "file":
        CDATA.LastErrorCode = LastError.NO_DIRECTORY
        raise Exception(tr("executable output is not a directory or does not exists."))
            
    if args.info is not None:
        if args.info == "":
            print("Common Info")
        elif args.info == "V":
            print("Version")
        elif args.info == "W":
            print("Warning")
        elif args.info == "TP":
            print(tr("Target platform"))
    
    return args
