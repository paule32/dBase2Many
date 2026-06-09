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
    push    r12
    push    rbx
    sub     rsp, 8
    mov     r12, rcx
    mov     eax, 1
    mov     r11, qword [r12 + JitContext.print_double_tmp]
    mov     dword [r11], eax
    mov     eax, 0
    mov     r11, qword [r12 + JitContext.print_double_tmp]
    mov     dword [r11+4], eax
    mov     r11, qword [r12 + JitContext.print_double_tmp]
    mov     eax, dword [r11]
    cmp     eax, 0
    setnz   al
    movzx   eax, al
    push    rax
    mov     r11, qword [r12 + JitContext.print_double_tmp]
    mov     eax, dword [r11+4]
    cmp     eax, 0
    setnz   al
    movzx   eax, al
    xor     eax, 1
    cmp     eax, 0
    setnz   al
    movzx   eax, al
    pop     rbx
    and     eax, ebx
    cmp     eax, 0
    setnz   al
    movzx   eax, al
    cmp     eax, 0
    setnz   al
    movzx   eax, al
    cmp     eax, 0
    jz      else_1
    mov     rcx, _str_0
    mov     rax, _jit_print_text
    sub     rsp, 32
    call    rax
    add     rsp, 32
    mov     rax, _jit_print_newline
    sub     rsp, 32
    call    rax
    add     rsp, 32
else_1:
    add     rsp, 8
    pop     rbx
    pop     r12
    ret

section .data
_str_0 db "User active", 0
