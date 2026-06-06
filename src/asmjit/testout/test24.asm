; -----------------------------------------------------------------------------
; GENERATED WITH PYTHON 3.14 ON: 2026-06-06
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
	push	rbx
	sub	rsp, 8
	mov	r12, rcx
	mov	eax, 10
	mov	dword [r12+48], eax
	mov	eax, 0
	mov	ebx, eax
	cmp	eax, 0
	jl	array_bounds_fail_2
	cmp	eax, 9
	jnle	array_bounds_fail_2
	jmp	array_bounds_ok_1
array_bounds_fail_2:
	mov	rcx, _str_0
	mov	edx, ebx
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140701642004448
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_1:
	mov	eax, ebx
	imul	eax, eax, 8
	add	eax, 0
	mov	r11, qword [r12+32]
	movsxd	rax, eax
	add	r11, rax
	mov	eax, dword [r12+48]
	mov	dword [r11], eax
	mov	eax, 20
	mov	dword [r12+48], eax
	mov	eax, 0
	mov	ebx, eax
	cmp	eax, 0
	jl	array_bounds_fail_4
	cmp	eax, 9
	jnle	array_bounds_fail_4
	jmp	array_bounds_ok_3
array_bounds_fail_4:
	mov	rcx, _str_1
	mov	edx, ebx
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140701642004448
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_3:
	mov	eax, ebx
	imul	eax, eax, 8
	add	eax, 0
	mov	r11, qword [r12+32]
	movsxd	rax, eax
	add	r11, rax
	add	r11, 4
	mov	eax, dword [r12+48]
	mov	dword [r11], eax
	mov	eax, 0
	mov	ebx, eax
	cmp	eax, 0
	jl	array_bounds_fail_6
	cmp	eax, 9
	jnle	array_bounds_fail_6
	jmp	array_bounds_ok_5
array_bounds_fail_6:
	mov	rcx, _str_2
	mov	edx, ebx
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140701642004448
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_5:
	mov	eax, ebx
	imul	eax, eax, 8
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
	mov	eax, 0
	mov	ebx, eax
	cmp	eax, 0
	jl	array_bounds_fail_8
	cmp	eax, 9
	jnle	array_bounds_fail_8
	jmp	array_bounds_ok_7
array_bounds_fail_8:
	mov	rcx, _str_3
	mov	edx, ebx
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140701642004448
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_7:
	mov	eax, ebx
	imul	eax, eax, 8
	add	eax, 0
	mov	r11, qword [r12+32]
	movsxd	rax, eax
	add	r11, rax
	add	r11, 4
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
	add	rsp, 8
	pop	rbx
	pop	r12
	ret

section .data
_str_0 db "points", 0
_str_1 db "points", 0
_str_2 db "points", 0
_str_3 db "points", 0
