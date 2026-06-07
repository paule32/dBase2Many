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
	jmp	skipproc_Push_2
proc_Push_1:
	push	rbp
	mov	rbp, rsp
	push	rcx
	push	rdx
	sub	rsp, 512
	mov	rcx, 12
	mov	rax, _jit_new_memory
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	qword [rbp-24], rax
	mov	eax, dword [rbp-16]
	mov	ebx, eax
	mov	rax, qword [rbp-24]
	mov	dword [rax], ebx
	mov	r11, qword [rbp-8]
	mov	rax, qword [r11]
	push	rax
	mov	rax, qword [rbp-24]
	add	rax, 4
	pop	r11
	mov	qword [rax], r11
	mov	rax, qword [rbp-24]
	mov	r11, qword [rbp-8]
	mov	qword [r11], rax
exitproc_Push_3:
	mov	rsp, rbp
	pop	rbp
	ret
skipproc_Push_2:
	jmp	skipproc_InsertAfter_5
proc_InsertAfter_4:
	push	rbp
	mov	rbp, rsp
	push	rcx
	push	rdx
	push	r8
	sub	rsp, 512
	mov	r11, qword [rbp-8]
	mov	rax, qword [r11]
	mov	qword [rbp-32], rax
while_7:
	mov	rax, qword [rbp-32]
	push	rax
	xor	rax, rax
	mov	r11, rax
	pop	rax
	cmp	rax, r11
	jz	endwhile_8
	mov	rax, qword [rbp-32]
	mov	eax, dword [rax]
	push	rax
	mov	eax, dword [rbp-16]
	mov	ebx, eax
	pop	rax
	cmp	eax, ebx
	jnz	else_9
	mov	rcx, 12
	mov	rax, _jit_new_memory
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	qword [rbp-40], rax
	mov	eax, dword [rbp-24]
	mov	ebx, eax
	mov	rax, qword [rbp-40]
	mov	dword [rax], ebx
	mov	rax, qword [rbp-32]
	mov	rax, qword [rax+4]
	push	rax
	mov	rax, qword [rbp-40]
	add	rax, 4
	pop	r11
	mov	qword [rax], r11
	mov	rax, qword [rbp-40]
	push	rax
	mov	rax, qword [rbp-32]
	add	rax, 4
	pop	r11
	mov	qword [rax], r11
	jmp	exitproc_InsertAfter_6
else_9:
	mov	rax, qword [rbp-32]
	mov	rax, qword [rax+4]
	mov	qword [rbp-32], rax
	jmp	while_7
endwhile_8:
exitproc_InsertAfter_6:
	mov	rsp, rbp
	pop	rbp
	ret
skipproc_InsertAfter_5:
	push	r12
	push	rbx
	sub	rsp, 8
	mov	r12, rcx
	xor	rax, rax
	mov	r11, qword [r12+40]
	mov	qword [r11], rax
	mov	rax, qword [r12+40]
	add	rax, 0
	mov	rcx, rax
	mov	eax, 10
	mov	edx, eax
	sub	rsp, 32
	call	proc_Push_1
	add	rsp, 32
	mov	rax, qword [r12+40]
	add	rax, 0
	mov	rcx, rax
	mov	eax, 20
	mov	edx, eax
	sub	rsp, 32
	call	proc_Push_1
	add	rsp, 32
	mov	rax, qword [r12+40]
	add	rax, 0
	mov	rcx, rax
	mov	eax, 30
	mov	edx, eax
	sub	rsp, 32
	call	proc_Push_1
	add	rsp, 32
	mov	rax, qword [r12+40]
	add	rax, 0
	mov	rcx, rax
	mov	eax, 20
	mov	edx, eax
	mov	eax, 25
	mov	r8d, eax
	sub	rsp, 32
	call	proc_InsertAfter_4
	add	rsp, 32
	mov	rax, qword [r12+40]
	mov	rax, qword [rax]
	mov	r11, qword [r12+40]
	mov	qword [r11+8], rax
skipproc_Push_20:
	mov	rax, qword [r12+40]
	mov	rax, qword [rax+8]
	push	rax
	xor	rax, rax
	mov	r11, rax
	pop	rax
	cmp	rax, r11
	jz	skipproc_Push_21
	mov	rax, qword [r12+40]
	mov	rax, qword [rax+8]
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
	mov	rax, qword [rax+4]
	mov	r11, qword [r12+40]
	mov	qword [r11+8], rax
	jmp	 skipproc_Push_20
skipproc_Push_21:
	add	rsp, 8
	pop	rbx
	pop	r12
	ret

section .data
