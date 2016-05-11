		.arch armv6
		.fpu vfp
		.align 2
		.global main
		.data
vars:		.space 0
format:		.asciz "%d\n"
		.text
main:
		ldr r11, =vars
		ldr r2, =10
		push {r2}
		pop {r2}
		ldr r2, [r2]
		push {r2}
		pop {r2}
		ldr r0, =format
		mov r1, r2
		bl printf
		bl exit

