; -----------------------------------------------------------------------------
; GENERATED WITH PYTHON 3.14 ON: 2026-06-03
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
	mov	r12, rcx
	jmp	endproc_TestInteger_2
proc_TestInteger_1:
	push	rbp
	mov	rbp, rsp
	push	rcx
	push	rdx
	push	r8
	push	r9
	mov	rcx, _str_0
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, dword [rbp-8]
	mov	ecx, eax
	mov	rax, _jit_print_int
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rcx, _str_1
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rcx, qword [rbp-16]
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rcx, _str_2
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, dword [rbp-24]
	mov	ecx, eax
	mov	rax, _jit_print_int
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rcx, _str_3
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, dword [rbp-32]
	mov	ecx, eax
	mov	rax, _jit_print_int
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rsp, rbp
	pop	rbp
	ret
endproc_TestInteger_2:
	jmp	endproc_TestProc_4
proc_TestProc_3:
	push	rbp
	mov	rbp, rsp
	push	rcx
	push	rdx
	mov	rcx, _str_4
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rcx, qword [rbp-8]
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rcx, _str_5
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rcx, qword [rbp-16]
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	eax, 1234
	mov	ecx, eax
	mov	rdx, _str_6
	mov	eax, 42
	mov	r8d, eax
	mov	eax, 74
	mov	r9d, eax
	sub	rsp, 32
	call	proc_TestInteger_1
	add	rsp, 32
	mov	rsp, rbp
	pop	rbp
	ret
endproc_TestProc_4:
	jmp	endproc_Hallo_6
proc_Hallo_5:
	push	rbp
	mov	rbp, rsp
	mov	rcx, _str_7
	mov	rax, _jit_print_text
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rax, _jit_print_newline
	sub	rsp, 32
	call	rax
	add	rsp, 32
	mov	rcx, _str_8
	mov	rdx, _str_9
	sub	rsp, 32
	call	proc_TestProc_3
	add	rsp, 32
	mov	rsp, rbp
	pop	rbp
	ret
endproc_Hallo_6:
	sub	rsp, 32
	call	proc_Hallo_5
	add	rsp, 32
	pop	r12
	ret

section .data
_str_0 db "integer: ", 0
_str_1 db "string: ", 0
_str_2 db "t3: ", 0
_str_3 db "t4: ", 0
_str_4 db "sub caller: ", 0
_str_5 db "more text: ", 0
_str_6 db "Hallo", 0
_str_7 db "Hallo aus Procedure", 0
_str_8 db "text", 0
_str_9 db "more text", 0
