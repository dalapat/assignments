		.text
.Ltext0:
.LCO:
		.string "%d\n"
		.data
		.align 4
		.type   format, @object
		.size   format, 4
format:
		.long   .LC0
		.align 4
		.type   data, @object
		.size   data, 4
		.globl main
		.type main, @function
main:
		sub r2, r11, =0
		push r2
		ldr r2, =3
		push r2
		pop r2
		ldr r2, [r2]
		push r2
		pop r2
		pop r3
		str r2, [r3]
		sub r2, r11, =0
		push r2
		pop r2
		ldr r2, [r2]
		push r2
		pop r2
		ldr r0, format
		mov r1, r2
		bl printf
		sub r2, r11, =4
		push r2
		sub r2, r11, =0
		push r2
		pop r2
		ldr r2, [r2]
		push r2
		pop r2
		pop r3
		str r2, [r3]
		sub r2, r11, =4
		push r2
		pop r2
		ldr r2, [r2]
		push r2
		pop r2
		ldr r0, format
		mov r1, r2
		bl printf
