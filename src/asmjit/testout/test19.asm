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


extern _jit_print_text
extern _jit_print_int
extern _jit_print_double
extern _jit_print_newline

section .text
global _main
_main:
	push	r12
	mov	r12, rcx
	mov	r11, qword [r12+32]
	mov	dword [r11], 1
	mov	dword [r11+4], 2
	mov	dword [r11+8], 3
	mov	dword [r11+12], 4
	mov	dword [r11+16], 5
	mov	dword [r11+20], 6
	mov	dword [r11+24], 7
	mov	dword [r11+28], 8
	mov	eax, 2
	imul	eax, eax, 4
	add	eax, 0
	mov	r11, qword [r12+32]
	movsxd	rax, eax
	add	r11, rax
	mov	eax, dword [r11]
	push	rax
	mov	eax, 10
	mov	ebx, eax
	pop	rax
	add	eax, ebx
	mov	ebx, eax
	mov	eax, 0
	imul	eax, eax, 4
	add	eax, 0
	mov	r11, qword [r12+32]
	movsxd	rax, eax
	add	r11, rax
	mov	dword [r11], ebx
	mov	eax, 0
	imul	eax, eax, 4
	add	eax, 0
	mov	r11, qword [r12+32]
	movsxd	rax, eax
	add	r11, rax
	mov	eax, dword [r11]
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
