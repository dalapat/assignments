		.arch armv6
		.fpu vfp
		.align 2
		.global main
		.data
vars:		.space 20
format:		.asciz "%d\n"
		.text
main:
		ldr r11, =vars
		add r2, r11, #0
		push {r2}
		ldr r2, =3
		push {r2}
		ldr r3, =4
		pop {r2}
		mul r2, r2, r3
		push {r2}
		pop {r3}
		pop {r2}
		add r2, r2, r3
		push {r2}
		ldr r2, =3
		push {r2}
		pop {r3}
		pop {r2}
		str r3, [r2]
		add r2, r11, #0
		push {r2}
		ldr r2, =3
		push {r2}
		ldr r3, =4
		pop {r2}
		mul r2, r2, r3
		push {r2}
		pop {r3}
		pop {r2}
		add r2, r2, r3
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
		ldr r2, =3
		push {r2}
		ldr r3, =4
		pop {r2}
		mul r2, r2, r3
		push {r2}
		pop {r3}
		pop {r2}
		add r2, r2, r3
		push {r2}
		add r2, r11, #0
		push {r2}
		ldr r2, =3
		push {r2}
		ldr r3, =4
		pop {r2}
		mul r2, r2, r3
		push {r2}
		pop {r3}
		pop {r2}
		add r2, r2, r3
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
		ldr r2, =3
		push {r2}
		ldr r3, =4
		pop {r2}
		mul r2, r2, r3
		push {r2}
		pop {r3}
		pop {r2}
		add r2, r2, r3
		push {r2}
		pop {r2}
		ldr r2, [r2]
		push {r2}
		pop {r2}
		ldr r0, =format
		mov r1, r2
		bl printf
		bl exit
