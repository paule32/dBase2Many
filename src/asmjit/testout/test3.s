dbl_10_5_0 equ 4622100592565682176 ; 10.5
dbl_20_0_1 equ 4626322717216342016 ; 20.0

extern _str_0
extern _str_1
extern _str_2
extern _str_3
extern _str_4
extern _jit_print_text
extern _jit_print_newline

section .text
global main
main:
	push	r12
	mov 	r12, rcx
	mov 	eax, 20
	mov 	rax, qword [r12]
	mov 	dword [rax], eax
	mov 	rax, dbl_10_5_0
	movq 	xmm0, rax
	mov 	rax, qword [r12+8]
	movsd	qword [rax], xmm0
	mov 	rcx, _str_0
	mov 	rax, _jit_print_text
	sub 	rsp, 32
	call 	rax
	add 	rsp, 32
	mov 	rax, _jit_print_newline
	sub 	rsp, 32
	call 	rax
	add 	rsp, 32
	mov 	rax, qword [r12]
	mov 	eax, dword [rax]
	push  	rax
	mov 	eax, 10
	mov 	ebx, eax
	pop 	rax
	cmp 	eax, ebx
	jle 	L0
	mov 	rcx, _str_1
	mov 	rax, _jit_print_text
	sub 	rsp, 32
	call	rax
	add 	rsp, 32
	mov 	rax, _jit_print_newline
	sub 	rsp, 32
	call	rax
	add 	rsp, 32
	jmp 	L1
L0:
	mov 	rcx, _str_2
	mov 	rax, _jit_print_text
	sub 	rsp, 32
	call 	rax
	add 	rsp, 32
	mov 	rax, _jit_print_newline
	sub 	rsp, 32
	call 	rax
	add 	rsp, 32
L1:
	mov 	rax, qword [r12+8]
	movsd 	xmm0, qword [rax]
	push 	rax
	mov 	rax, dbl_20_0_1
	movq	xmm0, rax
	mov 	ebx, eax
	pop 	rax
	cmp 	eax, ebx
	jnl 	L2
	mov 	rcx, _str_3
	mov 	rax, _jit_print_text
	sub 	rsp, 32
	call	rax
	add 	rsp, 32
	mov 	rax, _jit_print_newline
	sub 	rsp, 32
	call	rax
	add 	rsp, 32
L2:
	mov 	rcx, _str_4
	mov 	rax, _jit_print_text
	sub 	rsp, 32
	call 	rax
	add 	rsp, 32
	mov 	rax, _jit_print_newline
	sub 	rsp, 32
	call	rax
	add 	rsp, 32
	pop 	r12
	ret
