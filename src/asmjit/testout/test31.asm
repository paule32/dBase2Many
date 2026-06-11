; -----------------------------------------------------------------------------
; GENERATED WITH PYTHON 3.14 ON: 2026-06-11
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
pointr_vars: times 4 dq 0

section .text
global _main
_main:
    push        r12
    push        rbx
    sub         rsp, 8
    lea         r12, [rel ctx]
    mov         rcx, 12
    mov         rax, _jit_new_memory
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         r11, qword [r12 + JitContext.pointr_vars]
    mov         qword [r11], rax
    mov         rcx, 12
    mov         rax, _jit_new_memory
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         r11, qword [r12 + JitContext.pointr_vars]
    mov         qword [r11+8], rax
    mov         rcx, 12
    mov         rax, _jit_new_memory
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         r11, qword [r12 + JitContext.pointr_vars]
    mov         qword [r11+16], rax
    mov         eax, 10
    mov         ebx, eax
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax]
    test        rax, rax
    jnz         ptr_not_nil_1
    mov         rcx, _str_1
    mov         rax, _jit_runtime_error
    sub         rsp, 32
    call        rax
    add         rsp, 32
ptr_not_nil_1:
    mov         dword [rax], ebx
    mov         eax, 20
    mov         ebx, eax
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax+8]
    test        rax, rax
    jnz         ptr_not_nil_2
    mov         rcx, _str_3
    mov         rax, _jit_runtime_error
    sub         rsp, 32
    call        rax
    add         rsp, 32
ptr_not_nil_2:
    mov         dword [rax], ebx
    mov         eax, 30
    mov         ebx, eax
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax+16]
    test        rax, rax
    jnz         ptr_not_nil_3
    mov         rcx, _str_5
    mov         rax, _jit_runtime_error
    sub         rsp, 32
    call        rax
    add         rsp, 32
ptr_not_nil_3:
    mov         dword [rax], ebx
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax+8]
    push        rax
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax]
    add         rax, 4
    pop         r11
    mov         qword [rax], r11
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax+16]
    push        rax
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax+8]
    add         rax, 4
    pop         r11
    mov         qword [rax], r11
    xor         rax, rax
    xor         rax, rax
    xor         rax, rax
    push        rax
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax+16]
    add         rax, 4
    pop         r11
    mov         qword [rax], r11
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax]
    mov         r11, qword [r12 + JitContext.pointr_vars]
    mov         qword [r11+24], rax
while_4:
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax+24]
    push        rax
    xor         rax, rax
    mov         rbx, rax
    pop         rax
    cmp         rax, rbx
    jz          endwhile_5
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax+24]
    test        rax, rax
    jnz         ptr_not_nil_6
    mov         rcx, _str_7
    mov         rax, _jit_runtime_error
    sub         rsp, 32
    call        rax
    add         rsp, 32
ptr_not_nil_6:
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
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax+24]
    test        rax, rax
    jnz         ptr_not_nil_7
    mov         rcx, _str_7
    mov         rax, _jit_runtime_error
    sub         rsp, 32
    call        rax
    add         rsp, 32
ptr_not_nil_7:
    mov         rax, qword [rax+4]
    mov         r11, qword [r12 + JitContext.pointr_vars]
    mov         qword [r11+24], rax
    jmp         while_4
endwhile_5:
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax+16]
    mov         rcx, rax
    mov         rax, _jit_dispose_memory
    sub         rsp, 32
    call        rax
    add         rsp, 32
    xor         rax, rax
    mov         r11, qword [r12 + JitContext.pointr_vars]
    mov         qword [r11+16], rax
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax+8]
    mov         rcx, rax
    mov         rax, _jit_dispose_memory
    sub         rsp, 32
    call        rax
    add         rsp, 32
    xor         rax, rax
    mov         r11, qword [r12 + JitContext.pointr_vars]
    mov         qword [r11+8], rax
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax]
    mov         rcx, rax
    mov         rax, _jit_dispose_memory
    sub         rsp, 32
    call        rax
    add         rsp, 32
    xor         rax, rax
    mov         r11, qword [r12 + JitContext.pointr_vars]
    mov         qword [r11], rax
    add         rsp, 8
    pop         rbx
    pop         r12
    xor         ecx, ecx
    sub         rsp, 32
    mov         rax, _jit_ExitProcess
    call        rax
    ret

section .data
_str_0 db "n1", 0
_str_1 db "Nil pointer error: n1", 0
_str_2 db "n2", 0
_str_3 db "Nil pointer error: n2", 0
_str_4 db "n3", 0
_str_5 db "Nil pointer error: n3", 0
_str_6 db "p", 0
_str_7 db "Nil pointer error: p", 0
