; -----------------------------------------------------------------------------
; GENERATED WITH PYTHON 3.14 ON: 2026-06-03
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
	mov	eax, 0
	mov	ebx, eax
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	dword [rax], ebx
	mov	eax, 5
	mov	dword [r12 + JitContext.print_int_tmp], eax
for_1:
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	eax, dword [rax]
	cmp	eax, dword [r12 + JitContext.print_int_tmp]
	jnle	endfor_2
	mov	rcx, _str_0
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
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
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	eax, dword [rax]
	add	eax, 1
	mov	ebx, eax
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	dword [rax], ebx
	jmp	 for_1
endfor_2:
	mov	eax, 5
	mov	ebx, eax
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	dword [rax], ebx
	mov	eax, 0
	mov	dword [r12 + JitContext.print_int_tmp], eax
for_3:
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	eax, dword [rax]
	cmp	eax, dword [r12 + JitContext.print_double_tmp]
	jl	endfor_4
	mov	rcx, _str_1
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
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
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	eax, dword [rax]
	sub	eax, 1
	mov	ebx, eax
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	dword [rax], ebx
	jmp	 for_3
endfor_4:
	pop	r12
	ret

section .data
_str_0 db "x = ", 0
_str_1 db "x = ", 0
