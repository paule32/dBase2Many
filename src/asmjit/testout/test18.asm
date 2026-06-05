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
	mov	eax, 10
	mov	r11, qword [r12 + JitContext.print_double_tmp]
	mov	dword [r11], eax
	mov	eax, 10
	mov	r11, qword [r12 + JitContext.print_double_tmp]
	mov	dword [r11+8], eax
	mov	eax, 20
	mov	r11, qword [r12 + JitContext.print_double_tmp]
	mov	dword [r11+12], eax
	mov	r11, qword [r12 + JitContext.print_double_tmp]
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
	mov	rcx, _str_0
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	r11, qword [r12 + JitContext.print_double_tmp]
	mov	eax, dword [r11+8]
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
	mov	r11, qword [r12 + JitContext.print_double_tmp]
	mov	eax, dword [r11+12]
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
_str_0 db "rX: ", 0
_str_1 db "rY: ", 0
