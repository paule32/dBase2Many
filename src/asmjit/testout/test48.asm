; -----------------------------------------------------------------------------
; GENERATED WITH PYTHON 3.14 ON: 2026-06-10
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



extern _jit_array_bounds_error
extern _jit_string_range_error
extern _jit_dynarray_setlength
extern _jit_dynstring_setlength

extern _jit_print_text
extern _jit_print_int
extern _jit_print_double
extern _jit_print_newline
extern _jit_new_memory
extern _jit_dispose_memory
extern _jit_set_exception
extern _jit_nil_pointer_error
extern _jit_out_of_memory_error

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

section .text
global _main
_main:
    push        r12
    push        rbx
    sub         rsp, 8
    lea         r12, [rel ctx]
    xor         rax, rax
    mov         r11, qword [r12+40]
    mov         qword [r11], rax
    mov         rcx, _str_0
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rcx, _str_1
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         eax, 123
    mov         ebx, eax
    mov         rax, qword [r12+40]
    mov         rax, qword [rax]
    test        rax, rax
    jnz         ptr_not_nil_3
    mov         rcx, r12
    mov         rdx, _str_3
    mov         rax, _jit_set_exception
    sub         rsp, 32
    call        rax
    add         rsp, 32
    jmp         except_1
ptr_not_nil_3:
    mov         dword [rax], ebx
    mov         rcx, _str_4
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    jmp         endtry_2
except_1:
    mov         rcx, _str_5
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
endtry_2:
    mov         rcx, _str_6
    mov         rax, _jit_print_text
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
    ret

section .data
_str_0 db "start", 0
_str_1 db "before nil access", 0
_str_2 db "P", 0
_str_3 db "Nil pointer error: P", 0
_str_4 db "after nil access", 0
_str_5 db "except block", 0
_str_6 db "done", 0
