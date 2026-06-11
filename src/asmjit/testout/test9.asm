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

extern _jit_dynstring_from_cstr
extern _jit_dynstring_length
extern _jit_dynstring_concat

extern _jit_set_exception
extern _jit_nil_pointer_error
extern _jit_out_of_memory_error
extern _jit_array_bounds_error
extern _jit_string_range_error

extern _jit_dynarray_setlength
extern _jit_dynstring_setlength

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

section .text
global _main
_main:
    jmp         skipproc_TestInteger_2
proc_TestInteger_1:
    push        rbp
    mov         rbp, rsp
    push        rcx
    push        rdx
    push        r8
    push        r9
    sub         rsp, 512
    mov         rcx, _str_0
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         eax, dword [rbp-8]
    mov         ecx, eax
    mov         rax, _jit_print_int
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
    mov         rcx, qword [rbp-16]
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rcx, _str_2
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         eax, dword [rbp-24]
    mov         ecx, eax
    mov         rax, _jit_print_int
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rcx, _str_3
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         eax, dword [rbp-32]
    mov         ecx, eax
    mov         rax, _jit_print_int
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
exitproc_TestInteger_3:
    mov         rsp, rbp
    pop         rbp
    ret
skipproc_TestInteger_2:
    jmp         skipproc_TestProc_5
proc_TestProc_4:
    push        rbp
    mov         rbp, rsp
    push        rcx
    push        rdx
    sub         rsp, 512
    mov         rcx, _str_4
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rcx, qword [rbp-8]
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rcx, _str_5
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rcx, qword [rbp-16]
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         eax, 74
    movsxd      rax, eax
    push        rax
    mov         eax, 42
    movsxd      rax, eax
    push        rax
    mov         rax, _str_6
    mov         rcx, rax
    mov         rax, _jit_dynstring_from_cstr
    sub         rsp, 32
    call        rax
    add         rsp, 32
    push        rax
    mov         eax, 1234
    movsxd      rax, eax
    push        rax
    pop         rcx
    pop         rdx
    pop         r8
    pop         r9
    sub         rsp, 32
    call        proc_TestInteger_1
    add         rsp, 32
exitproc_TestProc_6:
    mov         rsp, rbp
    pop         rbp
    ret
skipproc_TestProc_5:
    jmp         skipproc_Hallo_8
proc_Hallo_7:
    push        rbp
    mov         rbp, rsp
    sub         rsp, 512
    mov         rcx, _str_7
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _jit_print_newline
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, _str_8
    mov         rcx, rax
    mov         rax, _jit_dynstring_from_cstr
    sub         rsp, 32
    call        rax
    add         rsp, 32
    push        rax
    mov         rax, _str_9
    mov         rcx, rax
    mov         rax, _jit_dynstring_from_cstr
    sub         rsp, 32
    call        rax
    add         rsp, 32
    push        rax
    pop         rcx
    pop         rdx
    sub         rsp, 32
    call        proc_TestProc_4
    add         rsp, 32
exitproc_Hallo_9:
    mov         rsp, rbp
    pop         rbp
    ret
skipproc_Hallo_8:
    push        r12
    push        rbx
    sub         rsp, 8
    lea         r12, [rel ctx]
    sub         rsp, 32
    call        proc_Hallo_7
    add         rsp, 32
    add         rsp, 8
    pop         rbx
    pop         r12
    xor         ecx, ecx
    sub         rsp, 32
    mov         rax, 140713733003248
    call        rax
    ret

section .data
_str_0 db "integer: ", 0
_str_1 db "string: ", 0
_str_2 db "t3: ", 0
_str_3 db "t4: ", 0
_str_4 db "sub caller: ", 0
_str_5 db "more text: ", 0
_str_6 db "Hallo", 0
_str_7 db "Hallo aus Procedure", 0
_str_8 db "more text", 0
_str_9 db "text", 0
