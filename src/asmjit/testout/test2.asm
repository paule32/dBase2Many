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

dbl_20_214_0 equ 4626382952861358096 ; 20.214
dbl_20_214_1 equ 4626382952861358096 ; 20.214
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
	mov	rcx, _str_0
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, 10
	push	rax
	mov	rax, dbl_20_214_0
	movq	xmm0, rax
	pop	rax
	cvtsi2sd	xmm1, eax
	sub	rsp, 8
	movsd	qword [rsp], xmm0
	mov	rax, dbl_20_214_0
	movq	xmm0, rax
	movsd	xmm1, qword [rsp]
	add	rsp, 8
	addsd	xmm0, xmm1
	mov	r11, qword [r12 + JitContext.double_vars]
	movsd	qword [r11], xmm0
	mov	rcx, _str_1
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
	add	rsp, 8
	pop	rbx
	pop	r12
	ret

section .data
_str_0 db "text", 0
_str_1 db "x = ", 0
