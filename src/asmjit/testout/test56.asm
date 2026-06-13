; -----------------------------------------------------------------------------
; GENERATED WITH PYTHON 3.14 ON: 2026-06-13
; Copyright (c) 2026 by Jens Kallup - paule32
; all rights reserved.
; -----------------------------------------------------------------------------

struc JitContext
.int_vars:         resq 1
.double_vars:      resq 1
.string_vars:      resq 1
.record_vars:      resq 1
.arrays_vars:      resq 1
.pointr_vars:      resq 1
.print_int_tmp:    resd 1
.print_double_tmp: resq 1
endstruc



extern _jit_print_text
extern _jit_print_int
extern _jit_print_double
extern _jit_print_newline

extern _jit_new_memory
extern _jit_dispose_memory

extern _jit_dynarray_setlength

extern _jit_dynstring_from_cstr
extern _jit_dynstring_setlength
extern _jit_dynstring_length
extern _jit_dynstring_concat
extern _jit_dynstring_copy
extern _jit_dynstring_pos

extern _jit_set_exception
extern _jit_runtime_error

extern _jit_nil_pointer_error
extern _jit_out_of_memory_error
extern _jit_array_bounds_error
extern _jit_string_range_error

extern _jit_ExitProcess

section .data
ctx:
    istruc      JitContext
    at          JitContext.int_vars,         dq int_vars
    at          JitContext.double_vars,      dq double_vars
    at          JitContext.string_vars,      dq string_vars
    at          JitContext.record_vars,      dq record_vars
    at          JitContext.arrays_vars,      dq arrays_vars
    at          JitContext.pointr_vars,      dq pointr_vars
    at          JitContext.print_int_tmp,    dd 0
    at          JitContext.print_double_tmp, dq 0
    iend

int_vars:    times 1 dd 0
double_vars: times 1 dq 0
string_vars: times 1 dq 0
record_vars: times 1 db 0
arrays_vars: times 1 db 0
pointr_vars: times 1 dq 0

    dbase2many_module_kind    dq 3
dbase2many_module_kind_program equ 1
dbase2many_module_kind_unit equ 2
dbase2many_module_kind_library equ 3


section .text
global _main
global _ADD$INTEGER$INTEGER
global _TEST56$$_$$_TFOO_$$_CREATE
global _TEST56$$_$$_TFOO_$$_CREATE$ANSISTRING
global _TEST56$$_$$_TFOO_$$_CREATE$INTEGER$INTEGER

_main:
    jmp         L5
_ADD$INTEGER$INTEGER:
    push        rbp
    mov         rbp, rsp
    push        rbx
    push        rcx
    push        rdx
    sub         rsp, 8
    sub         rsp, 256
    mov         eax, dword [rbp-16]
    push        rax
    mov         eax, dword [rbp-24]
    mov         ebx, eax
    pop         rax
    add         eax, ebx
    mov         rbx, qword [rbp-8]
    mov         rsp, rbp
    pop         rbp
    ret
L5:
    jmp         endfunc_Add_6
class_TFoo_Create_1:
    push        rbp
    mov         rbp, rsp
    push        rcx
    sub         rsp, 256
    mov         rcx, _str_0
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rsp, rbp
    pop         rbp
    ret
endfunc_Add_6:
    jmp         skip_class_TFoo_Create_7
class_TFoo_Create_2:
    push        rbp
    mov         rbp, rsp
    push        rcx
    push        rdx
    sub         rsp, 256
    mov         rcx, _str_1
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rsp, rbp
    pop         rbp
    ret
skip_class_TFoo_Create_7:
    jmp         skip_class_TFoo_Create_8
class_TFoo_Create_3:
    push        rbp
    mov         rbp, rsp
    push        rcx
    push        rdx
    push        r8
    sub         rsp, 256
    mov         rcx, _str_2
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rsp, rbp
    pop         rbp
    ret
skip_class_TFoo_Create_8:
    jmp         skip_class_TFoo_Create_9
class_TFoo_Destroy_4:
    push        rbp
    mov         rbp, rsp
    push        rcx
    sub         rsp, 256
    mov         rcx, _str_3
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rsp, rbp
    pop         rbp
    ret
skip_class_TFoo_Create_9:
    push        r12
    push        rbx
    sub         rsp, 8
    lea         r12, [rel ctx]
    add         rsp, 8
    pop         rbx
    pop         r12
    xor         ecx, ecx
    sub         rsp, 32
    mov         rax, _jit_ExitProcess
    call        rax
    ret

section .data
_str_0 db "TFoo: Create", 0
_str_1 db "TFoo: Create(S: String)", 0
_str_2 db "TFoo: Create(I1, I2: Integer)", 0
_str_3 db "TFoo: Destroy", 0
