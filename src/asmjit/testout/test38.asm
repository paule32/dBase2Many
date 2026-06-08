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
    mov     r8, 4
    mov     rax, qword [r12+40]
    mov     rax, qword [rax]
    mov     rcx, rax
    mov     rax, _jit_dynarray_setlength
    sub     rsp, 32
    call    rax
    add     rsp, 32
    mov     r11, qword [r12+40]
    mov     qword [r11], rax
    mov     eax, 10
    movsxd  rdx, eax
    mov     rax, qword [r12 + JitContext.print_int_tmp]
    mov     rax, qword [rax]
    mov     rcx, rax
    mov     rax, _jit_dynstring_setlength
    sub     rsp, 32
    call    rax
    add     rsp, 32
    mov     rdx, qword [r12 + JitContext.print_int_tmp]
    mov     qword [rdx], rax
    mov     eax, 123
    mov     dword [r12+48], eax
    mov     eax, 0
    imul    eax, eax, 4
    mov     r10d, eax
    mov     rax, qword [r12+40]
    mov     rax, qword [rax]
    movsxd  r11, r10d
    add     r11, rax
    mov     eax, dword [r12+48]
    mov     dword [r11], eax
    mov     eax, 456
    mov     dword [r12+48], eax
    mov     eax, 1
    imul    eax, eax, 4
    mov     r10d, eax
    mov     rax, qword [r12+40]
    mov     rax, qword [rax]
    movsxd  r11, r10d
    add     r11, rax
    mov     eax, dword [r12+48]
    mov     dword [r11], eax
    mov     rax, _str_0
    movzx   ebx, byte [rax]
    mov     eax, 1
    sub     eax, 1
    mov     r10d, eax
    mov     rax, qword [r12 + JitContext.print_int_tmp]
    mov     rax, qword [rax]
    test    rax, rax
    jnz     string_not_nil_1
    mov     rax, _jit_string_range_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
string_not_nil_1:
    mov     r11, rax
    sub     r11, 16
    mov     r11, qword [r11]
    cmp     r10d, 0
    jl      string_index_fail_3
    cmp     r10, r11
    jb      string_index_ok_2
string_index_fail_3:
    mov     rax, _jit_string_range_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
string_index_ok_2:
    movsxd  r11, r10d
    add     r11, rax
    mov     byte [r11], bl
    mov     rax, _str_1
    movzx   ebx, byte [rax]
    mov     eax, 2
    sub     eax, 1
    mov     r10d, eax
    mov     rax, qword [r12 + JitContext.print_int_tmp]
    mov     rax, qword [rax]
    test    rax, rax
    jnz     string_not_nil_4
    mov     rax, _jit_string_range_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
string_not_nil_4:
    mov     r11, rax
    sub     r11, 16
    mov     r11, qword [r11]
    cmp     r10d, 0
    jl      string_index_fail_6
    cmp     r10, r11
    jb      string_index_ok_5
string_index_fail_6:
    mov     rax, _jit_string_range_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
string_index_ok_5:
    movsxd  r11, r10d
    add     r11, rax
    mov     byte [r11], bl
    mov     rax, _str_2
    movzx   ebx, byte [rax]
    mov     eax, 3
    sub     eax, 1
    mov     r10d, eax
    mov     rax, qword [r12 + JitContext.print_int_tmp]
    mov     rax, qword [rax]
    test    rax, rax
    jnz     string_not_nil_7
    mov     rax, _jit_string_range_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
string_not_nil_7:
    mov     r11, rax
    sub     r11, 16
    mov     r11, qword [r11]
    cmp     r10d, 0
    jl      string_index_fail_9
    cmp     r10, r11
    jb      string_index_ok_8
string_index_fail_9:
    mov     rax, _jit_string_range_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
string_index_ok_8:
    movsxd  r11, r10d
    add     r11, rax
    mov     byte [r11], bl
    mov     rax, qword [r12 + JitContext.print_int_tmp]
    mov     rax, qword [rax]
    mov     rcx, rax
    mov     rax, _jit_print_text
    sub     rsp, 32
    call    rax
    add     rsp, 32
    mov     rax, _jit_print_newline
    sub     rsp, 32
    call    rax
    add     rsp, 32
    mov     eax, 1
    sub     eax, 1
    mov     r10d, eax
    mov     rax, qword [r12 + JitContext.print_int_tmp]
    mov     rax, qword [rax]
    movsxd  r11, r10d
    add     r11, rax
    movzx   eax, byte [r11]
    mov     ecx, eax
    mov     rax, 140700408944776
    sub     rsp, 32
    call    rax
    add     rsp, 32
    mov     rax, _jit_print_newline
    sub     rsp, 32
    call    rax
    add     rsp, 32
    mov     eax, 0
    imul    eax, eax, 4
    mov     r10d, eax
    mov     rax, qword [r12+40]
    mov     rax, qword [rax]
    movsxd  r11, r10d
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
    mov     eax, 1
    imul    eax, eax, 4
    mov     r10d, eax
    mov     rax, qword [r12+40]
    mov     rax, qword [rax]
    movsxd  r11, r10d
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
    add     rsp, 8
    pop     rbx
    pop     r12
    ret

section .data
_str_0 db "O", 0
_str_1 db "P", 0
_str_2 db "A", 0
