# ---------------------------------------------------------------------------
# File: constants.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

# ---------------------------------------------------------------------------
# we support the following backend's:
# - nasm
# - asmjit
# ---------------------------------------------------------------------------
BACKEND_ASMJIT  = "asmjit"
BACKEND_NASM    = "nasm"

BACKEND_OBJFILE = "objfile"
BACKEND_EXEFILE = "exefile"

# ---------------------------------------------------------------------------
# 16-bit register placeholder ...
# ---------------------------------------------------------------------------
REG_AL     = "al"       # low register
REG_AH     = "ah"       # high register

REG_AX     = "ax"       # alround / return code register
REG_BX     = "bx"       # backup register
REG_CX     = "cx"       # counter register
REG_DX     = "dx"       # decrement register
REG_BP     = "bp"       # base pointer register
REG_SP     = "sp"       # stack pointer register
REG_SI     = "si"       # source index register
REG_DI     = "di"       # destination index register
# ---------------------------------------------------------------------------
# 32-bit register placeholder ...
# ---------------------------------------------------------------------------
REG_EAX     = "eax"     # alround / return code register
REG_EBX     = "ebx"     # backup register
REG_ECX     = "ecx"     # counter register
REG_RDX     = "edx"     # decrement register
REG_EBP     = "ebp"     # extended base pointer register
REG_ESP     = "esp"     # extended stack pointer register
REG_ESI     = "esi"     # extended source index register
REG_EDI     = "edi"     # extended destination index register
# ---------------------------------------------------------------------------
# 64-bit register placeholder ...
# ---------------------------------------------------------------------------
REG_RAX     = "rax"     # alround / return code register
REG_RBX     = "rbx"     # backup register
REG_RCX     = "rcx"     # counter register
REG_RDX     = "rdx"     # decrement register
REG_RBP     = "rbp"     # 64-bit base pointer register
REG_RSP     = "rsp"     # stack pointer register
REG_RSI     = "rsi"     # source index register
REG_RDI     = "rdi"     # destination index register

# ---------------------------------------------------------------------------
# misc. placeholder's ...
# ---------------------------------------------------------------------------
ASM_OUT_PH  = "asm_out << "

# ---------------------------------------------------------------------------
# coff writer constants:
# ---------------------------------------------------------------------------
IMAGE_FILE_MACHINE_AMD64        = 0x8664
IMAGE_FILE_MACHINE_I386         = 0x014C

IMAGE_FILE_RELOCS_STRIPPED      = 0x0001
IMAGE_FILE_EXECUTABLE_IMAGE     = 0x0002
IMAGE_FILE_32BIT_MACHINE        = 0x0100
IMAGE_FILE_DLL                  = 0x2000

IMAGE_SCN_CNT_CODE              = 0x00000020
IMAGE_SCN_CNT_INITIALIZED_DATA  = 0x00000040

IMAGE_SCN_MEM_EXECUTE           = 0x20000000
IMAGE_SCN_MEM_READ              = 0x40000000
IMAGE_SCN_MEM_WRITE             = 0x80000000

IMAGE_SYM_CLASS_EXTERNAL        = 2
IMAGE_SYM_CLASS_STATIC          = 3

IMAGE_SYM_DTYPE_FUNCTION        = 0x20

IMAGE_REL_AMD64_ADDR64          = 0x0001
IMAGE_REL_AMD64_REL32           = 0x0004

IMAGE_REL_I386_DIR32            = 0x0006
IMAGE_REL_I386_REL32            = 0x0014

# ---------------------------------------------------------------------------
# variant types ...
# ---------------------------------------------------------------------------
JIT_VARIANT_EMPTY       = 0
JIT_VARIANT_INTEGER     = 1
JIT_VARIANT_BOOLEAN     = 2
JIT_VARIANT_CHAR        = 3
JIT_VARIANT_STRING      = 4
JIT_VARIANT_DOUBLE      = 5
JIT_VARIANT_POINTER     = 6

JIT_VARIANT_ARG_SIZE    = 12

JIT_VARIANT_KIND_OFFSET = 0
JIT_VARIANT_LOW_OFFSET  = 4
JIT_VARIANT_HIGH_OFFSET = 8

# ---------------------------------------------------------------------------
# Assembly JIT context offsets sizes ...
# ---------------------------------------------------------------------------
JIT_CONTEXT_OFFSETS = {
    "int_vars"          :  0,
    "double_vars"       :  8,
    "string_vars"       : 16,
    "record_vars"       : 24,
    "arrays_vars"       : 32,
    "pointr_vars"       : 40,
    "print_int_tmp"     : 48,
    "print_double_tmp"  : 56,
}
