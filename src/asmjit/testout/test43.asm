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
    mov     dword [r12+48], eax
    xor     ebx, ebx
    mov     eax, 0
    mov     r10d, eax
    cmp     eax, 0
    jl      array_bounds_fail_2
    cmp     eax, 3
    jnle    array_bounds_fail_2
    jmp     array_bounds_ok_1
array_bounds_fail_2:
    mov     rcx, _str_0
    mov     edx, r10d
    mov     r8d, 0
    mov     r9d, 3
    mov     rax, _jit_array_bounds_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
array_bounds_ok_1:
    mov     eax, r10d
    add     ebx, eax
    mov     eax, ebx
    imul    eax, eax, 4
    add     eax, 0
    mov     r11, qword [r12+32]
    movsxd  rax, eax
    add     r11, rax
    mov     eax, dword [r12+48]
    mov     dword [r11], eax
    mov     eax, 0
    mov     dword [r12+48], eax
    xor     ebx, ebx
    mov     eax, 1
    mov     r10d, eax
    cmp     eax, 0
    jl      array_bounds_fail_4
    cmp     eax, 3
    jnle    array_bounds_fail_4
    jmp     array_bounds_ok_3
array_bounds_fail_4:
    mov     rcx, _str_0
    mov     edx, r10d
    mov     r8d, 0
    mov     r9d, 3
    mov     rax, _jit_array_bounds_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
array_bounds_ok_3:
    mov     eax, r10d
    add     ebx, eax
    mov     eax, ebx
    imul    eax, eax, 4
    add     eax, 0
    mov     r11, qword [r12+32]
    movsxd  rax, eax
    add     r11, rax
    mov     eax, dword [r12+48]
    mov     dword [r11], eax
    xor     ebx, ebx
    mov     eax, 1
    mov     r10d, eax
    cmp     eax, 0
    jl      array_bounds_fail_6
    cmp     eax, 3
    jnle    array_bounds_fail_6
    jmp     array_bounds_ok_5
array_bounds_fail_6:
    mov     rcx, _str_0
    mov     edx, r10d
    mov     r8d, 0
    mov     r9d, 3
    mov     rax, _jit_array_bounds_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
array_bounds_ok_5:
    mov     eax, r10d
    add     ebx, eax
    mov     eax, ebx
    imul    eax, eax, 4
    add     eax, 0
    mov     r11, qword [r12+32]
    movsxd  rax, eax
    add     r11, rax
    mov     eax, dword [r11]
    cmp     eax, 0
    setnz   al
    movzx   eax, al
    xor     eax, 1
    mov     dword [r12+48], eax
    xor     ebx, ebx
    mov     eax, 2
    mov     r10d, eax
    cmp     eax, 0
    jl      array_bounds_fail_8
    cmp     eax, 3
    jnle    array_bounds_fail_8
    jmp     array_bounds_ok_7
array_bounds_fail_8:
    mov     rcx, _str_0
    mov     edx, r10d
    mov     r8d, 0
    mov     r9d, 3
    mov     rax, _jit_array_bounds_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
array_bounds_ok_7:
    mov     eax, r10d
    add     ebx, eax
    mov     eax, ebx
    imul    eax, eax, 4
    add     eax, 0
    mov     r11, qword [r12+32]
    movsxd  rax, eax
    add     r11, rax
    mov     eax, dword [r12+48]
    mov     dword [r11], eax
    xor     ebx, ebx
    mov     eax, 0
    mov     r10d, eax
    cmp     eax, 0
    jl      array_bounds_fail_10
    cmp     eax, 3
    jnle    array_bounds_fail_10
    jmp     array_bounds_ok_9
array_bounds_fail_10:
    mov     rcx, _str_0
    mov     edx, r10d
    mov     r8d, 0
    mov     r9d, 3
    mov     rax, _jit_array_bounds_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
array_bounds_ok_9:
    mov     eax, r10d
    add     ebx, eax
    mov     eax, ebx
    imul    eax, eax, 4
    add     eax, 0
    mov     r11, qword [r12+32]
    movsxd  rax, eax
    add     r11, rax
    mov     eax, dword [r11]
    cmp     eax, 0
    setnz   al
    movzx   eax, al
    push    rax
    xor     ebx, ebx
    mov     eax, 2
    mov     r10d, eax
    cmp     eax, 0
    jl      array_bounds_fail_21
    cmp     eax, 3
    jnle    array_bounds_fail_21
    jmp     array_bounds_fail_20
array_bounds_fail_21:
    mov     rcx, _str_0
    mov     edx, r10d
    mov     r8d, 0
    mov     r9d, 3
    mov     rax, _jit_array_bounds_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
array_bounds_fail_20:
    mov     eax, r10d
    add     ebx, eax
    mov     eax, ebx
    imul    eax, eax, 4
    add     eax, 0
    mov     r11, qword [r12+32]
    movsxd  rax, eax
    add     r11, rax
    mov     eax, dword [r11]
    cmp     eax, 0
    setnz   al
    movzx   eax, al
    pop     rbx
    xor     eax, ebx
    cmp     eax, 0
    setnz   al
    movzx   eax, al
    mov     dword [r12+48], eax
    xor     ebx, ebx
    mov     eax, 3
    mov     r10d, eax
    cmp     eax, 0
    jl      array_bounds_fail_23
    cmp     eax, 3
    jnle    array_bounds_fail_23
    jmp     array_bounds_fail_22
array_bounds_fail_23:
    mov     rcx, _str_0
    mov     edx, r10d
    mov     r8d, 0
    mov     r9d, 3
    mov     rax, _jit_array_bounds_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
array_bounds_fail_22:
    mov     eax, r10d
    add     ebx, eax
    mov     eax, ebx
    imul    eax, eax, 4
    add     eax, 0
    mov     r11, qword [r12+32]
    movsxd  rax, eax
    add     r11, rax
    mov     eax, dword [r12+48]
    mov     dword [r11], eax
    xor     ebx, ebx
    mov     eax, 0
    mov     r10d, eax
    cmp     eax, 0
    jl      array_bounds_fail_25
    cmp     eax, 3
    jnle    array_bounds_fail_25
    jmp     array_bounds_fail_24
array_bounds_fail_25:
    mov     rcx, _str_0
    mov     edx, r10d
    mov     r8d, 0
    mov     r9d, 3
    mov     rax, _jit_array_bounds_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
array_bounds_fail_24:
    mov     eax, r10d
    add     ebx, eax
    mov     eax, ebx
    imul    eax, eax, 4
    add     eax, 0
    mov     r11, qword [r12+32]
    movsxd  rax, eax
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
    xor     ebx, ebx
    mov     eax, 1
    mov     r10d, eax
    cmp     eax, 0
    jl      array_bounds_fail_27
    cmp     eax, 3
    jnle    array_bounds_fail_27
    jmp     array_bounds_fail_26
array_bounds_fail_27:
    mov     rcx, _str_0
    mov     edx, r10d
    mov     r8d, 0
    mov     r9d, 3
    mov     rax, _jit_array_bounds_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
array_bounds_fail_26:
    mov     eax, r10d
    add     ebx, eax
    mov     eax, ebx
    imul    eax, eax, 4
    add     eax, 0
    mov     r11, qword [r12+32]
    movsxd  rax, eax
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
    xor     ebx, ebx
    mov     eax, 2
    mov     r10d, eax
    cmp     eax, 0
    jl      array_bounds_fail_29
    cmp     eax, 3
    jnle    array_bounds_fail_29
    jmp     array_bounds_fail_28
array_bounds_fail_29:
    mov     rcx, _str_0
    mov     edx, r10d
    mov     r8d, 0
    mov     r9d, 3
    mov     rax, _jit_array_bounds_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
array_bounds_fail_28:
    mov     eax, r10d
    add     ebx, eax
    mov     eax, ebx
    imul    eax, eax, 4
    add     eax, 0
    mov     r11, qword [r12+32]
    movsxd  rax, eax
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
    xor     ebx, ebx
    mov     eax, 3
    mov     r10d, eax
    cmp     eax, 0
    jl      array_bounds_ok_31
    cmp     eax, 3
    jnle    array_bounds_ok_31
    jmp     array_bounds_ok_30
array_bounds_ok_31:
    mov     rcx, _str_0
    mov     edx, r10d
    mov     r8d, 0
    mov     r9d, 3
    mov     rax, _jit_array_bounds_error
    sub     rsp, 32
    call    rax
    add     rsp, 32
array_bounds_ok_30:
    mov     eax, r10d
    add     ebx, eax
    mov     eax, ebx
    imul    eax, eax, 4
    add     eax, 0
    mov     r11, qword [r12+32]
    movsxd  rax, eax
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
_str_0 db "flags", 0
