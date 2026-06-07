; -----------------------------------------------------------------------------
; GENERATED WITH PYTHON 3.14 ON: 2026-06-07
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

extern _jit_print_text
extern _jit_print_int
extern _jit_print_double
extern _jit_print_newline
extern _jit_new_memory
extern _jit_dispose_memory

section .text
global _main
_main:
	push	r12
	push	rbx
	sub	rsp, 8
	mov	r12, rcx
	mov	rcx, 12
	mov	rax, _jit_new_memory
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	r11, qword [r12+40]
	mov	qword [r11], rax
	mov	rcx, 12
	mov	rax, _jit_new_memory
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	r11, qword [r12+40]
	mov	qword [r11+8], rax
	mov	eax, 10
	mov	ebx, eax
	mov	rax, qword [r12+40]
	mov	rax, qword [rax]
	mov	dword [rax], ebx
	mov	eax, 20
	mov	ebx, eax
	mov	rax, qword [r12+40]
	mov	rax, qword [rax+8]
	mov	dword [rax], ebx
	mov	rax, qword [r12+40]
	mov	rax, qword [rax+8]
	push	rax
	mov	rax, qword [r12+40]
	mov	rax, qword [rax]
	add	rax, 4
	pop	r11
	mov	qword [rax], r11
	mov	eax, 0
	xor	rax, rax
	push	rax
	mov	rax, qword [r12+40]
	mov	rax, qword [rax+8]
	add	rax, 4
	pop	r11
	mov	qword [rax], r11
	mov	rax, qword [r12+40]
	mov	rax, qword [rax]
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
	mov	rax, qword [r12+40]
	mov	rax, qword [rax]
	mov	rax, qword [rax+4]
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
	mov	rax, qword [r12+40]
	mov	rax, qword [rax+8]
	mov	rcx, rax
	mov	rax, _jit_dispose_memory
	sub	rsp, 32
	call	rax
	add	rsp, 32
	xor	rax, rax
	mov	r11, qword [r12+40]
	mov	qword [r11+8], rax
	mov	rax, qword [r12+40]
	mov	rax, qword [rax]
	mov	rcx, rax
	mov	rax, _jit_dispose_memory
	sub	rsp, 32
	call	rax
	add	rsp, 32
	xor	rax, rax
	mov	r11, qword [r12+40]
	mov	qword [r11], rax
	add	rsp, 8
	pop	rbx
	pop	r12
	ret

section .data
