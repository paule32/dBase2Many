struc JitContext
    .int_vars:         resq 1
    .double_vars:      resq 1
    .print_int_tmp:    resd 1
    .print_double_tmp: resq 1
endstruc


dbl_10_5_0 equ 4622100592565682176 ; 10.5
dbl_3_1415_1 equ 4614256447914709615 ; 3.1415
dbl_20_0_2 equ 4626322717216342016 ; 20.0
dbl_3_141_3 equ 4614255322014802772 ; 3.141
extern _jit_print_text
extern _jit_print_int
extern _jit_print_double
extern _jit_print_newline

section .text
global _main
_main:
	push	r12
	mov	r12, rcx
	mov	eax, 20
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	dword [rax], eax
	mov	rax, dbl_10_5_0
	movq	xmm0, rax
	mov	rax, qword [r12 + JitContext.double_vars]
	movsd	qword [rax], xmm0
	mov	eax, 42
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	dword [rax+4], eax
	mov	rax, dbl_3_1415_1
	movq	xmm0, rax
	mov	rax, qword [r12 + JitContext.double_vars]
	movsd	qword [rax+8], xmm0
	mov	rax, qword [r12 + JitContext.double_vars]
	movsd	xmm0, qword [rax]
	sub	rsp, 8
	movsd	qword [rsp], xmm0
	mov	rax, dbl_20_0_2
	movq	xmm0, rax
	movapd	xmm1, xmm0
	movsd	xmm0, qword [rsp]
	add	rsp, 8
	ucomisd	xmm0, xmm1
	jnb	L0
	mov	rcx, _str_0
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	jmp	L1
L0:
	mov	rcx, _str_1
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
L1:
	mov	rax, qword [r12 + JitContext.double_vars]
	movsd	xmm0, qword [rax+8]
	sub	rsp, 8
	movsd	qword [rsp], xmm0
	mov	rax, dbl_3_141_3
	movq	xmm0, rax
	movapd	xmm1, xmm0
	movsd	xmm0, qword [rsp]
	add	rsp, 8
	ucomisd	xmm0, xmm1
	jnz	L2
	mov	rcx, _str_2
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, qword [r12 + JitContext.double_vars]
	movsd	xmm0, qword [rax+8]
	mov	rax, _jit_print_double
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
L2:
	mov	rax, qword [r12 + JitContext.int_vars]
	mov	eax, dword [rax]
	push	rax
	mov	rax, qword [r12 + JitContext.double_vars]
	movsd	xmm0, qword [rax]
	movapd	xmm1, xmm0
	pop	rax
	cvtsi2sd	xmm0, eax
	ucomisd	xmm0, xmm1
	jnb	L4
	mov	rcx, _str_3
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	jmp	L5
L4:
	mov	rcx, _str_4
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
L5:
	pop	r12
	ret

section .data
_str_0 db "d ist kleiner als 20", 0
_str_1 db "d ist nicht kleiner als 20", 0
_str_2 db "PI ist PI: ", 0
_str_3 db "x ist kleiner als d", 0
_str_4 db "x ist nicht kleiner als d", 0
