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
	jmp	endfunc_GetValue_2
func_GetValue_1:
	push	rbp
	mov	rbp, rsp
	mov	eax, 1234
	mov	rsp, rbp
	pop	rbp
	ret
endfunc_GetValue_2:
	mov	rcx, _str_0
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	sub	rsp, 32
	call	func_GetValue_1
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
_str_0 db "Function result: ", 0
