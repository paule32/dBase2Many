; -----------------------------------------------------------------------------
; GENERATED WITH PYTHON 3.14 ON: 2026-06-09
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
    jmp     endfunc_IsOk_2
func_IsOk_1:
    push    rbp
    mov     rbp, rsp
    push    rbx
    sub     rsp, 8
    sub     rsp, 256
    mov     eax, 1
    mov     rbx, qword [rbp-8]
    mov     rsp, rbp
    pop     rbp
    ret
endfunc_IsOk_2:
    jmp     endfunc_IsNotOk_4
func_IsNotOk_3:
    push    rbp
    mov     rbp, rsp
    push    rbx
    sub     rsp, 8
    sub     rsp, 256
    mov     eax, 0
    mov     rbx, qword [rbp-8]
    mov     rsp, rbp
    pop     rbp
    ret
endfunc_IsNotOk_4:
    push    r12
    push    rbx
    sub     rsp, 8
    mov     r12, rcx
    sub     rsp, 32
    call    func_IsOk_1
    add     rsp, 32
    mov     ecx, eax
    mov     rax, _jit_print_int
    sub     rsp, 32
    call    rax
    add     rsp, 32
    mov     rax, _jit_print_newline
    sub     rsp, 32
    call    rax
    add     rsp, 32
    sub     rsp, 32
    call    func_IsNotOk_3
    add     rsp, 32
    mov     ecx, eax
    mov     rax, _jit_print_int
    sub     rsp, 32
    call    rax
    add     rsp, 32
    mov     rax, _jit_print_newline
    sub     rsp, 32
    call    rax
    add     rsp, 32
    sub     rsp, 32
    call    func_IsNotOk_3
    add     rsp, 32
    cmp     eax, 0
    setnz   al
    movzx   eax, al
    xor     eax, 1
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
