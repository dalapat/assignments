		.arch armv6
		.fpu vfp
		.align 2
		.global main
		.data
vars:		.space 4
format:		.asciz "%d\n"
		.text
main:
		ldr r11, =vars
		add r2, r11, #0
		push {r2}
		ldr r2, =0
		push {r2}
		pop {r3}
		pop {r2}
		str r3, [r2]
loop1:
		add r2, r11, #0
		push {r2}
		pop {r2}
		ldr r2, [r2]
		push {r2}
		pop {r2}
		ldr r0, =format
		mov r1, r2
		bl printf
		add r2, r11, #0
		push {r2}
		add r2, r11, #0
		push {r2}
		pop {r2}
		ldr r2, [r2]
		push {r2}
		ldr r2, =1
		push {r2}
		pop {r2}
		pop {r3}
		@plus
		add r2, r2, r3
		push {r2}
		pop {r3}
		pop {r2}
		str r3, [r2]
		add r2, r11, #0
		push {r2}
		pop {r2}
		ldr r2, [r2]
		push {r2}
		ldr r2, =10
		push {r2}
		pop {r2}
		pop {r3}
		cmp r3, r2
		movge r2, #1
		movlt r2, #0
		push {r2}
		pop {r2}
		cmp r2, #0
		beq loop1
		bl exit

