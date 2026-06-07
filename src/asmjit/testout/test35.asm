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
	mov	rcx, 12
	mov	rax, _jit_new_memory
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	r11, qword [r12+40]
	mov	qword [r11+16], rax
	mov	eax, dword [rbp-16]
	mov	ebx, eax
	mov	rax, qword [r12+40]
	mov	rax, qword [rax+16]
	mov	dword [rax], ebx
	mov	r11, qword [rbp-8]
	mov	rax, qword [r11]
	push	rax
	mov	rax, qword [r12+40]
	mov	rax, qword [rax+16]
	add	rax, 4
	pop	r11
	mov	qword [rax], r11
	mov	rax, qword [r12+40]
	mov	rax, qword [rax+16]
	mov	r11, qword [rbp-8]
	mov	qword [r11], rax
exitproc_Push_3:
	mov	rsp, rbp
	pop	rbp
	ret
skipproc_Push_2:
	jmp	skipproc_Pop_5
proc_Pop_4:
	push	rbp
	mov	rbp, rsp
	push	rcx
	mov	r11, qword [rbp-8]
	mov	rax, qword [r11]
	push	rax
	xor	rax, rax
	mov	r11, rax
	pop	rax
	cmp	rax, r11
	jnz	else_7
	jmp	exitproc_Pop_6
else_7:
	mov	r11, qword [rbp-8]
	mov	rax, qword [r11]
	mov	r11, qword [r12+40]
	mov	qword [r11+24], rax
	mov	rax, qword [r12+40]
	mov	rax, qword [rax]
	mov	rax, qword [rax+4]
	mov	r11, qword [rbp-8]
	mov	qword [r11], rax
	mov	rax, qword [r12+40]
	mov	rax, qword [rax+24]
	mov	rcx, rax
	mov	rax, _jit_dispose_memory
	sub	rsp, 32
	call	rax
	add	rsp, 32
	xor	rax, rax
	mov	r11, qword [r12+40]
	mov	qword [r11+24], rax
exitproc_Pop_6:
	mov	rsp, rbp
	pop	rbp
	ret
skipproc_Pop_5:
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
	sub	rsp, 32
	call	proc_Pop_4
	add	rsp, 32
	mov	rax, qword [r12+40]
	mov	rax, qword [rax]
	mov	r11, qword [r12+40]
	mov	qword [r11+8], rax
while_9:
	mov	rax, qword [r12+40]
	mov	rax, qword [rax+8]
	push	rax
	xor	rax, rax
	mov	r11, rax
	pop	rax
	cmp	rax, r11
	jz	endwhile_10
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
	jmp	 while_9
endwhile_10:
	add	rsp, 8
	pop	rbx
	pop	r12
	ret

section .data
