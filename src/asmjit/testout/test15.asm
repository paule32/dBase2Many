; -----------------------------------------------------------------------------
; GENERATED WITH PYTHON 3.14 ON: 2026-06-05
; Copyright (c) 2026 by Jens Kallup - paule32
; all rights reserved.
; -----------------------------------------------------------------------------

struc JitContext
    .int_vars:         resq 1
    .double_vars:      resq 1
    .print_int_tmp:    resd 1
    .print_double_tmp: resq 1
endstruc


dbl_3_1415926_0 equ 4614256656431372362 ; 3.1415926
dbl_12_34_1 equ 4623136420479977390 ; 12.34
extern _jit_print_text
extern _jit_print_int
extern _jit_print_double
extern _jit_print_newline

section .text
global _main
_main:
	jmp	endfunc_PiValue_2
func_PiValue_1:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 256
	mov	rax, dbl_3_1415926_0
	movq	xmm0, rax
	mov	rsp, rbp
	pop	rbp
	ret
endfunc_PiValue_2:
	jmp	endfunc_GetInteger_4
func_GetInteger_3:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 256
	mov	eax, 42
	mov	rsp, rbp
	pop	rbp
	ret
endfunc_GetInteger_4:
	jmp	endfunc_GetDouble_6
func_GetDouble_5:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 256
	mov	rax, dbl_12_34_1
	movq	xmm0, rax
	mov	rsp, rbp
	pop	rbp
	ret
endfunc_GetDouble_6:
	jmp	endfunc_GetString_8
func_GetString_7:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 256
	mov	rax, _str_0
	mov	rsp, rbp
	pop	rbp
	ret
endfunc_GetString_8:
	push	r12
	mov	r12, rcx
	sub	rsp, 32
	call	func_GetInteger_3
	add	rsp, 32
	mov	ebx, eax
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	dword [rax], ebx
	sub	rsp, 32
	call	func_GetDouble_5
	add	rsp, 32
	mov	r11, qword [r12 + JitContext.double_vars]
	movsd	qword [r11], xmm0
	sub	rsp, 32
	call	func_GetString_7
	add	rsp, 32
	mov	r11, qword [r12 + JitContext.print_int_tmp]
	mov	qword [r11], rax
	mov	rcx, _str_1
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	eax, dword [rax]
	mov	ecx, eax
	mov	rax, _jit_print_int
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rcx, _str_2
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, qword [r12 + JitContext.double_vars]
	movsd	xmm0, qword [rax]
	mov	rax, _jit_print_double
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rcx, _str_3
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, qword [r12 + JitContext.print_int_tmp]
	mov	rax, qword [rax]
	mov	rcx, rax
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rcx, _str_4
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	sub	rsp, 32
	call	func_PiValue_1
	add	rsp, 32
	mov	rax, _jit_print_double
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	pop	r12
	ret

section .data
_str_0 db "Foo Fuu", 0
_str_1 db "i : ", 0
_str_2 db "d : ", 0
_str_3 db "s : ", 0
_str_4 db "Pi: ", 0
