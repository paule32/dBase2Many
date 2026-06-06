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
	xor	ebx, ebx
	mov	eax, 0
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_fail_2
	cmp	eax, 9
	jnle	array_bounds_fail_2
	jmp	array_bounds_ok_1
array_bounds_fail_2:
	mov	rcx, _str_0
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_1:
	mov	eax, r10d
	imul	eax, eax, 10
	add	ebx, eax
	mov	eax, 0
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_fail_4
	cmp	eax, 9
	jnle	array_bounds_fail_4
	jmp	array_bounds_ok_3
array_bounds_fail_4:
	mov	rcx, _str_1
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_3:
	mov	eax, r10d
	add	ebx, eax
	mov	eax, ebx
	imul	eax, eax, 4
	add	eax, 0
	mov	r11, qword [r12+32]
	movsxd	rax, eax
	add	r11, rax
	mov	eax, dword [r12+48]
	mov	dword [r11], eax
	mov	eax, 20
	mov	dword [r12+48], eax
	xor	ebx, ebx
	mov	eax, 0
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_fail_6
	cmp	eax, 9
	jnle	array_bounds_fail_6
	jmp	array_bounds_ok_5
array_bounds_fail_6:
	mov	rcx, _str_2
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_5:
	mov	eax, r10d
	imul	eax, eax, 10
	add	ebx, eax
	mov	eax, 1
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_fail_8
	cmp	eax, 9
	jnle	array_bounds_fail_8
	jmp	array_bounds_ok_7
array_bounds_fail_8:
	mov	rcx, _str_3
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_7:
	mov	eax, r10d
	add	ebx, eax
	mov	eax, ebx
	imul	eax, eax, 4
	add	eax, 0
	mov	r11, qword [r12+32]
	movsxd	rax, eax
	add	r11, rax
	mov	eax, dword [r12+48]
	mov	dword [r11], eax
	mov	eax, 30
	mov	dword [r12+48], eax
	xor	ebx, ebx
	mov	eax, 1
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_fail_10
	cmp	eax, 9
	jnle	array_bounds_fail_10
	jmp	array_bounds_ok_9
array_bounds_fail_10:
	mov	rcx, _str_4
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_9:
	mov	eax, r10d
	imul	eax, eax, 10
	add	ebx, eax
	mov	eax, 0
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_fail_21
	cmp	eax, 9
	jnle	array_bounds_fail_21
	jmp	array_bounds_fail_20
array_bounds_fail_21:
	mov	rcx, _str_5
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_fail_20:
	mov	eax, r10d
	add	ebx, eax
	mov	eax, ebx
	imul	eax, eax, 4
	add	eax, 0
	mov	r11, qword [r12+32]
	movsxd	rax, eax
	add	r11, rax
	mov	eax, dword [r12+48]
	mov	dword [r11], eax
	mov	eax, 99
	mov	dword [r12+48], eax
	xor	ebx, ebx
	mov	eax, 2
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_fail_23
	cmp	eax, 9
	jnle	array_bounds_fail_23
	jmp	array_bounds_fail_22
array_bounds_fail_23:
	mov	rcx, _str_6
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_fail_22:
	mov	eax, r10d
	imul	eax, eax, 10
	add	ebx, eax
	mov	eax, 3
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_fail_25
	cmp	eax, 9
	jnle	array_bounds_fail_25
	jmp	array_bounds_fail_24
array_bounds_fail_25:
	mov	rcx, _str_7
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_fail_24:
	mov	eax, r10d
	add	ebx, eax
	mov	eax, ebx
	imul	eax, eax, 4
	add	eax, 0
	mov	r11, qword [r12+32]
	movsxd	rax, eax
	add	r11, rax
	mov	eax, dword [r12+48]
	mov	dword [r11], eax
	xor	ebx, ebx
	mov	eax, 0
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_fail_27
	cmp	eax, 9
	jnle	array_bounds_fail_27
	jmp	array_bounds_fail_26
array_bounds_fail_27:
	mov	rcx, _str_8
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_fail_26:
	mov	eax, r10d
	imul	eax, eax, 10
	add	ebx, eax
	mov	eax, 0
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_fail_29
	cmp	eax, 9
	jnle	array_bounds_fail_29
	jmp	array_bounds_fail_28
array_bounds_fail_29:
	mov	rcx, _str_9
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_fail_28:
	mov	eax, r10d
	add	ebx, eax
	mov	eax, ebx
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
	xor	ebx, ebx
	mov	eax, 0
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_ok_31
	cmp	eax, 9
	jnle	array_bounds_ok_31
	jmp	array_bounds_ok_30
array_bounds_ok_31:
	mov	rcx, _str_10
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_30:
	mov	eax, r10d
	imul	eax, eax, 10
	add	ebx, eax
	mov	eax, 1
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_ok_33
	cmp	eax, 9
	jnle	array_bounds_ok_33
	jmp	array_bounds_ok_32
array_bounds_ok_33:
	mov	rcx, _str_11
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_32:
	mov	eax, r10d
	add	ebx, eax
	mov	eax, ebx
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
	xor	ebx, ebx
	mov	eax, 1
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_ok_35
	cmp	eax, 9
	jnle	array_bounds_ok_35
	jmp	array_bounds_ok_34
array_bounds_ok_35:
	mov	rcx, _str_12
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_34:
	mov	eax, r10d
	imul	eax, eax, 10
	add	ebx, eax
	mov	eax, 0
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_ok_37
	cmp	eax, 9
	jnle	array_bounds_ok_37
	jmp	array_bounds_ok_36
array_bounds_ok_37:
	mov	rcx, _str_13
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_36:
	mov	eax, r10d
	add	ebx, eax
	mov	eax, ebx
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
	xor	ebx, ebx
	mov	eax, 2
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_ok_39
	cmp	eax, 9
	jnle	array_bounds_ok_39
	jmp	array_bounds_ok_38
array_bounds_ok_39:
	mov	rcx, _str_14
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_ok_38:
	mov	eax, r10d
	imul	eax, eax, 10
	add	ebx, eax
	mov	eax, 3
	mov	r10d, eax
	cmp	eax, 0
	jl	array_bounds_fail_41
	cmp	eax, 9
	jnle	array_bounds_fail_41
	jmp	array_bounds_fail_40
array_bounds_fail_41:
	mov	rcx, _str_15
	mov	edx, r10d
	mov	r8d, 0
	mov	r9d, 9
	mov	rax, 140699264358368
	sub	rsp, 32
	call	rax
	add	rsp, 32
array_bounds_fail_40:
	mov	eax, r10d
	add	ebx, eax
	mov	eax, ebx
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
	add	rsp, 8
	pop	rbx
	pop	r12
	ret

section .data
_str_0 db "m", 0
_str_1 db "m", 0
_str_2 db "m", 0
_str_3 db "m", 0
_str_4 db "m", 0
_str_5 db "m", 0
_str_6 db "m", 0
_str_7 db "m", 0
_str_8 db "m", 0
_str_9 db "m", 0
_str_10 db "m", 0
_str_11 db "m", 0
_str_12 db "m", 0
_str_13 db "m", 0
_str_14 db "m", 0
_str_15 db "m", 0
