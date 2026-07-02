bits 32
extern _dummy
global _add
section .text
_add:
	mov eax, [esp+4]
	add eax, [esp+8]
	push eax
	call _dummy
	pop eax
	ret

section .data
dummy: db 'dummy text', 0
        