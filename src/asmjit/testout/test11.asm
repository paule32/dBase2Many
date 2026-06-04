; -----------------------------------------------------------------------------
; GENERATED WITH PYTHON 3.14 ON: 2026-06-04
; Copyright (c) 2026 by Jens Kallup - paule32
; all rights reserved.
; -----------------------------------------------------------------------------

struc JitContext
    .int_vars:         resq 1
    .double_vars:      resq 1
    .print_int_tmp:    resd 1
    .print_double_tmp: resq 1
endstruc


extern _jit_print_text
extern _jit_print_int
extern _jit_print_double
extern _jit_print_newline

section .text
global _main
_main:
	push	r12
	mov	r12, rcx
	jmp	endfunc_Add1_2
func_Add1_1:
	push	rbp
	mov	rbp, rsp
	push	rcx
	push	rdx
	mov	eax, dword [rbp-8]
	push	rax
	mov	eax, dword [rbp-16]
	mov	ebx, eax
	pop	rax
	add	eax, ebx
	mov	rsp, rbp
	pop	rbp
	ret
endfunc_Add1_2:
	jmp	endfunc_Add2_4
func_Add2_3:
	push	rbp
	mov	rbp, rsp
	push	rcx
	push	rdx
	mov	eax, dword [rbp-8]
	push	rax
	mov	eax, dword [rbp-16]
	mov	ebx, eax
	pop	rax
	add	eax, ebx
	mov	rsp, rbp
	pop	rbp
	ret
endfunc_Add2_4:
	mov	rcx, _str_0
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, 10
	mov	ecx, eax
	mov	eax, 20
	mov	edx, eax
	sub	rsp, 32
	call	func_Add1_1
	add	rsp, 32
	mov	ecx, eax
	mov	rax, _jit_print_int
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rcx, _str_1
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, 10
	mov	ecx, eax
	mov	eax, 32
	mov	edx, eax
	sub	rsp, 32
	call	func_Add2_3
	add	rsp, 32
	mov	ecx, eax
	mov	rax, _jit_print_int
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
_str_0 db "Add1 result: ", 0
_str_1 db "Add2 result: ", 0
