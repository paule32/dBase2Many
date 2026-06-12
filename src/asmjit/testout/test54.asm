; -----------------------------------------------------------------------------
; GENERATED WITH PYTHON 3.14 ON: 2026-06-12
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

section .text
global _main
_main:
    jmp         skip_class_TObject_Create_6
class_TObject_Create_1:
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
skip_class_TObject_Create_6:
    jmp         skip_class_TObject_Destroy_7
class_TObject_Destroy_2:
    push        rbp
    mov         rbp, rsp
    push        rcx
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
skip_class_TObject_Destroy_7:
    jmp         skip_class_TFoo_Create_8
class_TFoo_Create_3:
    push        rbp
    mov         rbp, rsp
    push        rcx
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
class_TFoo_Create_4:
    push        rbp
    mov         rbp, rsp
    push        rcx
    push        rdx
    push        r8
    sub         rsp, 256
    mov         rcx, _str_3
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
    mov         rcx, _str_4
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
    mov         rsp, rbp
    pop         rbp
    ret
skip_class_TFoo_Create_9:
    jmp         skip_class_TFoo_Destroy_10
class_TFoo_Destroy_5:
    push        rbp
    mov         rbp, rsp
    push        rcx
    sub         rsp, 256
    mov         rcx, _str_5
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
skip_class_TFoo_Destroy_10:
    push        r12
    push        rbx
    sub         rsp, 8
    lea         r12, [rel ctx]
    mov         eax, 12
    movsxd      rax, eax
    push        rax
    mov         rax, _str_6
    mov         rcx, rax
    mov         rax, _jit_dynstring_from_cstr
    sub         rsp, 32
    call        rax
    add         rsp, 32
    push        rax
    mov         rcx, 4
    mov         rax, _jit_new_memory
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rcx, rax
    pop         rdx
    pop         r8
    push        rcx
    sub         rsp, 32
    call        class_TFoo_Create_4
    add         rsp, 32
    pop         rax
    mov         r11, qword [r12 + JitContext.pointr_vars]
    mov         qword [r11], rax
    mov         eax, 42
    mov         ebx, eax
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax]
    test        rax, rax
    jnz         class_TObject_Destroy_20
    mov         rcx, _str_8
    mov         rax, _jit_runtime_error
    sub         rsp, 32
    call        rax
    add         rsp, 32
class_TObject_Destroy_20:
    mov         dword [rax], ebx
    mov         rcx, _str_9
    mov         rax, _jit_print_text
    sub         rsp, 32
    call        rax
    add         rsp, 32
    mov         rax, qword [r12 + JitContext.pointr_vars]
    mov         rax, qword [rax]
    test        rax, rax
    jnz         class_TObject_Destroy_21
    mov         rcx, _str_8
    mov         rax, _jit_runtime_error
    sub         rsp, 32
    call        rax
    add         rsp, 32
class_TObject_Destroy_21:
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
    mov         rax, qword [rax]
    test        rax, rax
    jz          class_TObject_Destroy_22
    push        rax
    mov         rcx, rax
    sub         rsp, 32
    call        class_TFoo_Destroy_5
    add         rsp, 32
    pop         rcx
    mov         rax, _jit_dispose_memory
    sub         rsp, 32
    call        rax
    add         rsp, 32
    xor         rax, rax
    mov         r11, qword [r12 + JitContext.pointr_vars]
    mov         qword [r11], rax
    jmp         class_TObject_Destroy_23
class_TObject_Destroy_22:
class_TObject_Destroy_23:
    add         rsp, 8
    pop         rbx
    pop         r12
    xor         ecx, ecx
    sub         rsp, 32
    mov         rax, _jit_ExitProcess
    call        rax
    ret

section .data
_str_0 db "TObject: Create", 0
_str_1 db "TObject: Destroy", 0
_str_2 db "TFoo: Create", 0
_str_3 db "str: ", 0
_str_4 db "int: ", 0
_str_5 db "TFoo: Destroy", 0
_str_6 db "test", 0
_str_7 db "foo", 0
_str_8 db "Nil pointer error: foo", 0
_str_9 db "field: ", 0
