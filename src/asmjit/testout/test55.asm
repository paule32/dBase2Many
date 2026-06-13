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

    dbase2many_module_kind    dq 1
dbase2many_module_kind_program equ 1
dbase2many_module_kind_unit equ 2
dbase2many_module_kind_library equ 3


section .text
global _main
_main:
    jmp         endfunc_GetNumber_2
func_GetNumber_1:
    push        rbp
    mov         rbp, rsp
    push        rbx
    sub         rsp, 8
    sub         rsp, 256
    mov         eax, 100
    mov         rbx, qword [rbp-8]
    mov         rsp, rbp
    pop         rbp
    ret
endfunc_GetNumber_2:
    jmp         skip_unit_init_vcl_windows_4
unit_init_vcl_windows_3:
    mov         rcx, _str_0
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    ret
skip_unit_init_vcl_windows_4:
    jmp         endfunc_GetNumber_6
func_GetNumber_5:
    push        rbp
    mov         rbp, rsp
    push        rbx
    sub         rsp, 8
    sub         rsp, 256
    mov         eax, 200
    mov         rbx, qword [rbp-8]
    mov         rsp, rbp
    pop         rbp
    ret
endfunc_GetNumber_6:
    jmp         skip_unit_init_system_math_8
unit_init_system_math_7:
    mov         rcx, _str_1
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    ret
skip_unit_init_system_math_8:
    push        r12
    push        rbx
    sub         rsp, 8
    lea         r12, [rel ctx]
    sub         rsp, 32
    call        unit_init_vcl_windows_3
    add         rsp, 32
    sub         rsp, 32
    call        unit_init_system_math_7
    add         rsp, 32
    sub         rsp, 32
    call        func_GetNumber_5
    add         rsp, 32
    mov         ebx, eax
    mov         rax, qword [r12 + JitContext.int_vars]
    mov         dword [rax], ebx
    mov         rcx, _str_2
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, qword [r12 + JitContext.int_vars]
    mov         eax, dword [rax]
    mov         ecx, eax
    mov         rax, _jit_print_int
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    add         rsp, 8
    pop         rbx
    pop         r12
    xor         ecx, ecx
    sub         rsp, 32
    mov         rax, _jit_ExitProcess
    call        rax
    ret

section .data
_str_0 db "VCL.Windows init", 0
_str_1 db "System.Math init", 0
_str_2 db "x: ", 0
