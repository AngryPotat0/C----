	.file	"t.c"
	.text
	.def	__main;	.scl	2;	.type	32;	.endef
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
	pushq	%rbp
	.seh_pushreg	%rbp
	movq	%rsp, %rbp
	.seh_setframe	%rbp, 0
	subq	$48, %rsp
	.seh_stackalloc	48
	.seh_endprologue
	call	__main
	movl	$0, -8(%rbp)
	cmpl	$8, -8(%rbp)
	jle	.L2
	addl	$1, -8(%rbp)
.L2:
	movl	$0, -4(%rbp)
	jmp	.L3
.L4:
	movl	$0, -8(%rbp)
	addl	$1, -4(%rbp)
.L3:
	cmpl	$9, -4(%rbp)
	jle	.L4
	movl	$10, -8(%rbp)
	movl	$0, %eax
	addq	$48, %rsp
	popq	%rbp
	ret
	.seh_endproc
	.ident	"GCC: (x86_64-posix-sjlj-rev0, Built by MinGW-W64 project) 8.1.0"
