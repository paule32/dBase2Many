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
	mov	rcx, _str_0
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	jmp	exitproc_Test_3
	mov	rcx, _str_1
	mov	rax, _jit_print_text
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
	sub	rsp, 32
	call	proc_Test_1
	add	rsp, 32
	add	rsp, 8
	pop	rbx
	pop	r12
	ret

section .data
_str_0 db "A", 0
_str_1 db "B", 0
