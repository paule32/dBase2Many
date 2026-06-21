; -----------------------------------------------------------------------------
; AUTOMATIC GENERATED WITH Python 3.14 SCRIPT ON: 2026-06-21
;
; DON'T MODIFIED THIS CODE. ALL CHANGES WILL BE LOST BY NEXT RUN !
; Copyright (c) 2026 by Jens Kallup - paule32
; all rights reserved.
; -----------------------------------------------------------------------------

section .text



section .text
global _main
_main:
    jmp endfunc_Add_8
func_Add_7:
    push rbp  ; epilog
    mov rbp, rsp  ; stack frame
    push rbx  ; preserve non-volatile RBX
    push rcx  ; save function param a
    push rdx  ; save function param b
    sub rsp, 8  ; align stack in function
    sub rsp, 256  ; local variables
    mov eax, dword [rbp - 16]
    push rax
    mov eax, dword [rbp - 24]
    mov ebx, eax
    pop rax
    add eax, ebx
    mov rbx, qword [rbp - 8]
    mov rsp, rbp
    pop rbp
    ret
endfunc_Add_8:
    jmp skip_class_TFoo_Create_9
class_TFoo_Create_2:
    push rbp
    mov rbp, rsp
    push rcx  ; Self
    sub rsp, 256  ; class method locals
    mov rcx, str_0
    mov rax, _jit_print_text
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rax, _jit_print_newline
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rsp, rbp
    pop rbp
    ret
skip_class_TFoo_Create_9:
    jmp skip_class_TFoo_Create_10
class_TFoo_Create_3:
    push rbp
    mov rbp, rsp
    push rcx  ; Self
    push rdx  ; save class method param S
    sub rsp, 256  ; class method locals
    mov rcx, str_1
    mov rax, _jit_print_text
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rax, _jit_print_newline
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rsp, rbp
    pop rbp
    ret
skip_class_TFoo_Create_10:
    jmp skip_class_TFoo_Create_11
class_TFoo_Create_4:
    push rbp
    mov rbp, rsp
    push rcx  ; Self
    push rdx  ; save class method param I1
    push r8  ; save class method param I2
    sub rsp, 256  ; class method locals
    mov rcx, str_2
    mov rax, _jit_print_text
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rax, _jit_print_newline
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rsp, rbp
    pop rbp
    ret
skip_class_TFoo_Create_11:
    jmp skip_class_TFoo_Destroy_12
class_TFoo_Destroy_5:
    push rbp
    mov rbp, rsp
    push rcx  ; Self
    sub rsp, 256  ; class method locals
    mov rcx, str_3
    mov rax, _jit_print_text
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rax, _jit_print_newline
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rsp, rbp
    pop rbp
    ret
skip_class_TFoo_Destroy_12:
    jmp skip_class_TFoo_SetValue_13
class_TFoo_SetValue_1:
    push rbp
    mov rbp, rsp
    push rcx  ; Self
    push rdx  ; save class method param v
    sub rsp, 256  ; class method locals
    mov eax, dword [rbp - 16]
    mov ebx, eax
    mov rax, qword [rbp - 8]  ; Self
    mov dword [rax], ebx  ; Self.FValue :=
    mov rsp, rbp
    pop rbp
    ret
skip_class_TFoo_SetValue_13:
    jmp skip_class_TFoo_GetValue_14
class_TFoo_GetValue_6:
    push rbp
    mov rbp, rsp
    push rcx  ; Self
    sub rsp, 256  ; class method locals
    mov rax, qword [rbp - 8]  ; Self
    mov eax, dword [rax]  ; Self.FValue
    mov rsp, rbp
    pop rbp
    ret
skip_class_TFoo_GetValue_14:
    push r12
    push rbx
    sub rsp, 8  ; align stack
    mov r12, rcx  ; ctx
    mov rax, str_4
    mov rcx, rax
    mov rax, _jit_dynstring_from_cstr
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    push rax  ; ctor string arg
    mov rcx, 4
    mov rax, _jit_new_memory
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rcx, rax  ; self
    pop rdx  ; ctor arg {index + 1}
    push rcx  ; save constructor result object
    sub rsp, 32
    sub rsp, 32  ; Windows x64 shadow space
    call class_TFoo_Create_3
    add rsp, 32
    add rsp, 32
    pop rax  ; constructor result
    mov r11, qword [r12 + JitContext.pointr_vars]
    mov qword [r11], rax  ; object foo
    mov rcx, str_5
    mov rax, _jit_print_text
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rax, _jit_print_newline
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rax, _jit_debug_break
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rcx, str_6
    mov rax, _jit_print_text
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rax, _jit_print_newline
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    mov rax, qword [r12 + JitContext.pointr_vars]
    mov rax, qword [rax]  ; object foo
    test rax, rax
    jz free_nil_15
    push rax  ; save object for dispose
    mov rcx, rax  ; Self
    sub rsp, 32
    sub rsp, 32  ; Windows x64 shadow space
    call class_TFoo_Destroy_5
    add rsp, 32
    add rsp, 32
    pop rcx
    mov rax, _jit_dispose_memory
    sub rsp, 32  ; Windows x64 shadow space
    call rax
    add rsp, 32
    xor rax, rax
    mov r11, qword [r12 + JitContext.pointr_vars]
    mov qword [r11], rax  ; object foo
    jmp free_end_16
free_nil_15:
free_end_16:
  add rsp, 8  ; undo alignment
  pop rbx
  pop r12

  xor ecx, ecx
  sub rsp, 32
  lea rax, [rel _jit_ExitProcess]
  call rax
  ret      ; never reach

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

section .data
ctx:
istruc JitContext
  at JitContext.int_vars,         dq int_vars
  at JitContext.double_vars,      dq double_vars
  at JitContext.string_vars,      dq string_vars
  at JitContext.record_vars,      dq record_vars
  at JitContext.arrays_vars,      dq arrays_vars
  at JitContext.pointr_vars,      dq pointr_vars
  at JitContext.print_int_tmp,    dd 0
  at JitContext.print_double_tmp, dq 0
iend


int_vars:    times 1 dd 0
double_vars: times 1 dq 0
string_vars: times 1 dq 0
record_vars: times 1 db 0
arrays_vars: times 1 db 0
pointr_vars: times 1 dq 0



str_0: db "TFoo: Create", 0
str_1: db "TFoo: Create(S: String)", 0
str_2: db "TFoo: Create(I1, I2: Integer)", 0
str_3: db "TFoo: Destroy", 0
str_4: db "TFoo: String", 0
str_5: db "before break", 0
str_6: db "after break", 0


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
extern _jit_debug_break
extern _jit_ExitProcess

DBASE2MANY_MODULE_KIND: db 1
