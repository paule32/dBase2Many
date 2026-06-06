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
	jmp	endfunc_Fak_2
func_Fak_1:
	push	rbp
	mov	rbp, rsp
	push	rbx
	push	rcx
	sub	rsp, 256
	mov	eax, dword [rbp-16]
	push	rax
	mov	eax, 1
	mov	ebx, eax
	pop	rax
	cmp	eax, ebx
	jnle	else_3
	mov	eax, 1
	jmp	endif_4
else_3:
	mov	eax, dword [rbp-16]
	push	rax
	mov	eax, dword [rbp-16]
	push	rax
	mov	eax, 1
	mov	ebx, eax
	pop	rax
	sub	eax, ebx
	mov	ecx, eax
	sub	rsp, 32
	call	func_Fak_1
	add	rsp, 32
	mov	ebx, eax
	pop	rax
	imul	eax, ebx
endif_4:
	mov	rbx, qword [rbp-8]
	mov	rsp, rbp
	pop	rbp
	ret
endfunc_Fak_2:
	push	r12
	push	rbx
	sub	rsp, 8
	mov	r12, rcx
	mov	rcx, _str_0
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, 5
	mov	ecx, eax
	sub	rsp, 32
	call	func_Fak_1
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
	add	rsp, 8
	pop	rbx
	pop	r12
	ret

section .data
_str_0 db "Fak 5: ", 0
