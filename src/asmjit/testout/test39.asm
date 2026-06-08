; -----------------------------------------------------------------------------
; GENERATED WITH PYTHON 3.14 ON: 2026-06-08
; Copyright (c) 2026 by Jens Kallup - paule32
; all rights reserved.
; -----------------------------------------------------------------------------

struc JitContext
    .int_vars:         resq 1
    .double_vars:      resq 1
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

section .text
global _main
_main:
    push    r12
    push    rbx
    sub     rsp, 8
    mov     r12, rcx
    mov     eax, 10
    movsxd  rdx, eax
    mov     r8, 8
    mov     rax, qword [r12+40]
    mov     rax, qword [rax]
    mov     rcx, rax
    mov     rax, _jit_dynarray_setlength
    sub     rsp, 32
    call    rax
    add     rsp, 32
    mov     r11, qword [r12+40]
    mov     qword [r11], rax
    mov     eax, 100
    mov     dword [r12+48], eax
    mov     eax, 0
    mov     r10d, eax
    mov     rax, qword [r12+40]
    mov     rax, qword [rax]
    movsxd  r11, r10d
    imul    r11, r11, 8
    add     r11, rax
    mov     eax, dword [r12+48]
    mov     dword [r11], eax
    mov     eax, 200
    mov     dword [r12+48], eax
    mov     eax, 0
    mov     r10d, eax
    mov     rax, qword [r12+40]
    mov     rax, qword [rax]
    movsxd  r11, r10d
    imul    r11, r11, 8
    add     r11, rax
    mov     eax, dword [r12+48]
    mov     dword [r11+4], eax
    mov     eax, 0
    mov     r10d, eax
    mov     rax, qword [r12+40]
    mov     rax, qword [rax]
    movsxd  r11, r10d
    imul    r11, r11, 8
    add     r11, rax
    mov     eax, dword [r11]
    mov     ecx, eax
    mov     rax, _jit_print_int
    sub     rsp, 32
    call    rax
    add     rsp, 32
    mov     rax, _jit_print_newline
    sub     rsp, 32
    call    rax
    add     rsp, 32
    mov     eax, 0
    mov     r10d, eax
    mov     rax, qword [r12+40]
    mov     rax, qword [rax]
    movsxd  r11, r10d
    imul    r11, r11, 8
    add     r11, rax
    mov     eax, dword [r11+4]
    mov     ecx, eax
    mov     rax, _jit_print_int
    sub     rsp, 32
    call    rax
    add     rsp, 32
    mov     rax, _jit_print_newline
    sub     rsp, 32
    call    rax
    add     rsp, 32
    add     rsp, 8
    pop     rbx
    pop     r12
    ret

section .data
