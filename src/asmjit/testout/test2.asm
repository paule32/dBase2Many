public 1
main:
	mov	r10, rcx
	mov	eax, 10
	sub	rsp, 8
	movsd	qword ptr [rsp], xmm0
	mov	rax, 4626382952861358096
	movq	xmm0, rax
	movsd	xmm1, qword ptr [rsp]
	add	rsp, 8
	addsd	xmm0, xmm1
	mov	rax, qword ptr [r10+8]
	movsd	qword ptr [rax], xmm0
	mov	rax, qword ptr [r10+8]
	movsd	xmm0, qword ptr [rax]
	movsd	qword ptr [r10+24], xmm0
	ret
