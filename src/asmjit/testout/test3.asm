dbl_10_5_0 equ 4622100592565682176 ; 10.5
dbl_20_0_1 equ 4626322717216342016 ; 20.0
public 1
main:
	push	r12
	mov	r12, rcx
	mov	eax, 20
	mov	rax, dword ptr [r12]
	mov	dword ptr [rax], eax
	mov	rax, dbl_10_5_0
	movq	xmm0, rax
	mov	rax, qword ptr [r12+8]
	movsd	qword ptr [rax], xmm0
	mov	rcx, _str_0
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, dword ptr [r12]
	mov	eax, dword ptr [rax]
	push	rax
	mov	eax, 10
	mov	ebx, eax
	pop	rax
	cmp	eax, ebx
	jle	L0
	mov	rcx, _str_1
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
	mov	rcx, _str_2
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	L1:
	mov	rax, qword ptr [r12+8]
	movsd	xmm0, qword ptr [rax]
	push	rax
	mov	rax, dbl_20_0_1
	movq	xmm0, rax
	mov	ebx, eax
	pop	rax
	cmp	eax, ebx
	jnl	L2
	mov	rcx, _str_3
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	L2:
	mov	rcx, _str_4
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	pop	r12
	ret
