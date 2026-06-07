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

dbl_10_5_0 equ 4622100592565682176 ; 10.5
dbl_20_0_1 equ 4626322717216342016 ; 20.0
extern _jit_print_text
extern _jit_print_int
extern _jit_print_double
extern _jit_print_newline
extern _jit_new_memory
extern _jit_dispose_memory

section .text
global _main
_main:
	push	r12
	push	rbx
	sub	rsp, 8
	mov	r12, rcx
	mov	eax, 20
	mov	ebx, eax
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	dword [rax], ebx
	mov	rax, dbl_10_5_0
	movq	xmm0, rax
	mov	r11, qword [r12 + JitContext.double_vars]
	movsd	qword [r11], xmm0
	mov	rcx, _str_0
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	eax, dword [rax]
	push	rax
	mov	eax, 10
	mov	ebx, eax
	pop	rax
	cmp	eax, ebx
	jle	else_1
	mov	rcx, _str_1
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	jmp	endif_2
else_1:
	mov	rcx, _str_2
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
endif_2:
	mov	rax, qword [r12 + JitContext.double_vars]
	movsd	xmm0, qword [rax]
	sub	rsp, 8
	movsd	qword [rsp], xmm0
	mov	rax, dbl_20_0_1
	movq	xmm0, rax
	movapd	xmm1, xmm0
	movsd	xmm0, qword [rsp]
	add	rsp, 8
	ucomisd	xmm0, xmm1
	jnb	else_3
	mov	rcx, _str_3
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
else_3:
	mov	rcx, _str_4
	mov	rax, _jit_print_text
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
_str_0 db "start", 0
_str_1 db "x ist groesser als 10", 0
_str_2 db "x ist kleiner oder gleich 10", 0
_str_3 db "d ist kleiner als 20", 0
_str_4 db "ende", 0
