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
	jmp	skipproc_Test_2
proc_Test_1:
	push	rbp
	mov	rbp, rsp
	push	rcx
	push	rdx
	push	r8
	push	r9
	mov	eax, dword [rbp-8]
	mov	ecx, eax
	mov	rax, _jit_print_int
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, dword [rbp-16]
	mov	ecx, eax
	mov	rax, _jit_print_int
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, dword [rbp-24]
	mov	ecx, eax
	mov	rax, _jit_print_int
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, dword [rbp-32]
	mov	ecx, eax
	mov	rax, _jit_print_int
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, dword [rbp+48]
	mov	ecx, eax
	mov	rax, _jit_print_int
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, dword [rbp+56]
	mov	ecx, eax
	mov	rax, _jit_print_int
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, dword [rbp+64]
	mov	ecx, eax
	mov	rax, _jit_print_int
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, dword [rbp+72]
	mov	ecx, eax
	mov	rax, _jit_print_int
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
exitproc_Test_3:
	mov	rsp, rbp
	pop	rbp
	ret
skipproc_Test_2:
	push	r12
	push	rbx
	sub	rsp, 8
	mov	r12, rcx
	mov	eax, 8
	movsxd	rax, eax
	push	rax
	mov	eax, 7
	movsxd	rax, eax
	push	rax
	mov	eax, 6
	movsxd	rax, eax
	push	rax
	mov	eax, 5
	movsxd	rax, eax
	push	rax
	mov	eax, 1
	mov	ecx, eax
	mov	eax, 2
	mov	edx, eax
	mov	eax, 3
	mov	r8d, eax
	mov	eax, 4
	mov	r9d, eax
	sub	rsp, 32
	call	proc_Test_1
	add	rsp, 32
	add	rsp, 32
	add	rsp, 8
	pop	rbx
	pop	r12
	ret

section .data
