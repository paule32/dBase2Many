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
	jmp	endfunc_Add_2
func_Add_1:
	push	rbp
	mov	rbp, rsp
	push	rcx
	push	rdx
	sub	rsp, 256
	jmp	endfunc_Add_Add2_4
func_Add_Add2_3:
	push	rbp
	mov	rbp, rsp
	push	rcx
	push	rdx
	sub	rsp, 256
	mov	eax, dword [rbp-8]
	push	rax
	mov	eax, dword [rbp-16]
	mov	ebx, eax
	pop	rax
	add	eax, ebx
	mov	ebx, eax
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	dword [rax], ebx
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	eax, dword [rax]
	mov	rsp, rbp
	pop	rbp
	ret
endfunc_Add_Add2_4:
	mov	eax, dword [rbp-8]
	mov	ecx, eax
	mov	eax, dword [rbp-16]
	mov	edx, eax
	sub	rsp, 32
	call	func_Add_Add2_3
	add	rsp, 32
	mov	ebx, eax
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	dword [rax], ebx
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	eax, dword [rax]
	push	rax
	mov	eax, 10
	mov	ebx, eax
	pop	rax
	add	eax, ebx
	mov	ebx, eax
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	dword [rax+4], ebx
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	eax, dword [rax+4]
	mov	rsp, rbp
	pop	rbp
	ret
endfunc_Add_2:
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
	call	func_Add_1
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
_str_0 db "Add result: ", 0
