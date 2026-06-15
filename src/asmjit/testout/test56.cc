; -----------------------------------------------------------------------------
; AUTOMATIC GENERATED WITH Python 3.14 SCRIPT ON: 2026-06-15
;
; DON'T MODIFIED THIS CODE. ALL CHANGES WILL BE LOST BY NEXT RUN !
; Copyright (c) 2026 by Jens Kallup - paule32
; all rights reserved.
; -----------------------------------------------------------------------------


  add rsp, 8  ; undo alignment
  pop rbx
  pop r12

  xor ecx, ecx
  sub rsp, 32
  mov rax, &_jit_ExitProcess
  call rax
  ret      ; never reach

section .data
ctx:
istruc JitContext
  at JitContext.int_vars,         dq int_vars
  at JitContext.double_vars,      dq double_vars
  at JitContext.string_vars,      dq string_vars
  at JitContext.record_vars,      dq record_vars
  at JitContext.arrays_vars,      dq arrays_vars
  at JitContext.pointr_vars,      dq pointr_vars
  at JitContext.print_int_tmp,    dd 0
  at JitContext.print_double_tmp, dq 0
iend


int_vars:    times 1 dd 0
double_vars: times 1 dq 0
string_vars: times 1 dq 0
record_vars: times 1 db 0
arrays_vars: times 1 db 0
pointr_vars: times 1 dq 0


extern _jit_print_text
extern _jit_print_int
extern _jit_print_double
extern _jit_print_newline
extern _jit_new_memory
extern _jit_dispose_memory
extern _jit_dynarray_setlength
extern _jit_dynstring_from_cstr
extern _jit_dynstring_setlength
extern _jit_dynstring_length
extern _jit_dynstring_concat
extern _jit_dynstring_copy
extern _jit_dynstring_pos
extern _jit_set_exception
extern _jit_runtime_error
extern _jit_nil_pointer_error
extern _jit_out_of_memory_error
extern _jit_array_bounds_error
extern _jit_string_range_error
extern _jit_debug_break
extern _jit_ExitProcess

DBASE2MANY_MODULE_KIND: db 1

