public 1
main:
	push	r12
	mov	r12, rcx
	mov	rcx, 140696083788070
	mov	rax, 140696083765232
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, 140696083765104
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, 10
	sub	rsp, 8
	movsd	qword ptr [rsp], xmm0
	mov	rax, 4626382952861358096
	movq	xmm0, rax
	movsd	xmm1, qword ptr [rsp]
	add	rsp, 8
	addsd	xmm0, xmm1
	mov	rax, qword ptr [r12+8]
	movsd	qword ptr [rax], xmm0
	mov	rcx, 140696083788065
	mov	rax, 140696083765232
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, qword ptr [r12+8]
	movsd	xmm0, qword ptr [rax]
	mov	rax, 140696083765088
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, 140696083765104
	sub	rsp, 32
	call	rax
	add	rsp, 32
	pop	r12
	ret
