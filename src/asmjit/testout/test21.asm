; -----------------------------------------------------------------------------
; GENERATED WITH PYTHON 3.14 ON: 2026-06-06
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
	push	rbx
	sub	rsp, 8
	mov	r12, rcx
	mov	eax, 10
	mov	ebx, eax
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	dword [rax], ebx
	mov	rax, qword [r12 + JitContext.int_vars]
	add	rax, 0
	mov	r11, qword [r12+40]
	mov	qword [r11], rax
	mov	eax, 20
	mov	ebx, eax
	mov	rax, qword [r12+40]
	mov	rax, qword [rax]
	mov	dword [rax], ebx
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
	add	rsp, 8
	pop	rbx
	pop	r12
	ret

section .data
