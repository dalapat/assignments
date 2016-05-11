		.arch armv6
		.fpu vfp
		.align 2
		.global main
		.data
vars:		.space 8
format:		.asciz "%d\n"
		.text
main:
		ldr r11, =vars
		add r2, r11, #4
		push {r2}
		ldr r2, =1
		push {r2}
		pop {r3}
		pop {r2}
		str r3, [r2]
		ldr r2, =0
		push {r2}
		ldr r2, =0
		push {r2}
		pop {r2}
		pop {r3}
		cmp r3, r2
		moveq r2, #1
		movne r2, #0
		push {r2}
		pop {r2}
		cmp r2, #1
		beq itrue1
		bne ifalse1
itrue1:
loop1:
		add r2, r11, #0
		push {r2}
		ldr r2, =16807
		push {r2}
		add r2, r11, #4
		push {r2}
		pop {r2}
		ldr r2, [r2]
		push {r2}
		ldr r2, =127773
		push {r2}
		pop {r2}
		pop {r3}
		mod r2, r2, r3
		push {r2}
		pop {r2}
		pop {r3}
		mul r2, r2, r3
		push {r2}
		ldr r2, =2836
		push {r2}
		add r2, r11, #4
		push {r2}
		pop {r2}
		ldr r2, [r2]
		push {r2}
		ldr r2, =127773
		push {r2}
		pop {r2}
		pop {r3}
		sdiv r2, r2, r3
		push {r2}
		pop {r2}
		pop {r3}
		mul r2, r2, r3
		push {r2}
		pop {r2}
		pop {r3}
		sub r2, r2, r3
		push {r2}
		pop {r3}
		pop {r2}
		str r3, [r2]
		add r2, r11, #0
		push {r2}
		pop {r2}
		ldr r2, [r2]
		push {r2}
		ldr r2, =0
		push {r2}
		pop {r2}
		pop {r3}
		cmp r3, r2
		movgt r2, #1
		movle r2, #0
		push {r2}
		pop {r2}
		cmp r2, #1
		beq itrue2
		bne ifalse2
itrue2:
		add r2, r11, #4
		push {r2}
		add r2, r11, #0
		push {r2}
		pop {r3}
		ldr r3, [r3]
		pop {r2}
		str r3, [r2]
		bl endif2
ifalse2:
		add r2, r11, #4
		push {r2}
		add r2, r11, #0
		push {r2}
		pop {r2}
		ldr r2, [r2]
		push {r2}
		ldr r2, =2147483647
		push {r2}
		pop {r2}
		pop {r3}
		@plus
		add r2, r2, r3
		push {r2}
		pop {r3}
		pop {r2}
		str r3, [r2]
		bl endif2
endif2:
		add r2, r11, #4
		push {r2}
		pop {r2}
		ldr r2, [r2]
		push {r2}
		pop {r2}
		ldr r0, =format
		mov r1, r2
		bl printf
		ldr r2, =0
		push {r2}
		ldr r2, =0
		push {r2}
		pop {r2}
		pop {r3}
		cmp r3, r2
		movne r2, #1
		moveq r2, #0
		push {r2}
		pop {r2}
		cmp r2, #0
		beq loop1
		bl endif2
ifalse2:
		bl endif2
endif2:
		bl exit

