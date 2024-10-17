; ECS 154A subroutine.asm 
; Loads a sinwave into the LED matrix and repeatedly starts over
MAIN: ; Entry point to program
    ; Setup the stack at 32512 (I/O starts at 32736), not necessary 
	; 设置堆栈指针：
    LI x2, 32512

	; 加载字符串地址并调用 PUTSTR 子程序：
    LI x3, STRING
    JAL x1, PUTSTR
    ; Main loop
MAINLOOP:
    ; Call GETCHAR
	; 调用 GETCHAR 子程序获取输入字符。
    JAL x1, GETCHAR
    ; Call PUTCHAR 
	; 调用 PUTCHAR 子程序将获取的字符显示在屏幕上
    JAL x1, PUTCHAR
    ; Branch always to loop
	; 循环回到 MAINLOOP，持续等待输入和显示字符。
    J MAINLOOP

; GETCHAR
; 从键盘获取一个字符。
; x1 - Return address
; x3 - Return character
GETCHAR:
    ; Push x7
	; 保存寄存器 x7 到堆栈。
    ADDI x2, x2, -1
    SW x7, 0(x2)
GETCHARLOOP:
    ; Loop until character
	; 进入循环等待键盘输入，检查 I 标志是否置位。
    ; Compare I flag
    SF x7, x0
    SRLI x7, x7, 6 
    ; Jump back to loop
    BEQ x7, x0, GETCHARLOOP
    ; Readchar
GETCHARREAD:
    ; Load keyboard address
	; 一旦检测到输入，加载键盘地址 0x7FF0 并读取字符。
    LI x7, 0x7FF0
    LW x3, 0(x7)
    ; Pop x7
	; 恢复寄存器 x7 并返回调用点。
    LW x7, 0(x2)
    ADDI x2, x2, 1
    ; Return
    JR x1

; PUTCHAR 
; 将一个字符输出到屏幕。
; x1 - Return address
; x3 - Holds char to put out
PUTCHAR:
    ; Push x7
	; 保存寄存器 x7 到堆栈。
    ADDI x2, x2, -1
    SW x7, 0(x2)
    ; Load screen address
	; 加载屏幕地址 0x7FF1 并将字符输出到屏幕。
    LI x7, 0x7FF1
    ; Write char to screen
    SW x3, 0(x7)
    ; Pop x2
	; 恢复寄存器 x7 并返回调用点。
    LW x7, 0(x2)
    ADDI x2, x2, 1
    ; Return 
    JR x1

; PUTSTR
; 将一个字符串输出到屏幕，直到遇到空字符（\0）。
; x1 - Return address
; x3 - Holds address of string
PUTSTR:
    ; Push x7
    ; Push x6
	; 保存寄存器 x7 和 x6 到堆栈。
    ADDI x2, x2, -2
    SW x7, 1(x2)
    SW x6, 0(x2)
    ; Load screen address
    LI x7, 0x7FF1
PUTSTROUTCHAR:
    ; Load charater from string
	; 加载字符串的每一个字符到 x6，检查是否是空字符。
    LW x6, 0(x3)
    ; Check  for null
	; 如果遇到空字符，子程序结束，恢复寄存器并返回调用点。
    BEQ x0, x6, PUTSTRDONE
    ; Write to screen
	; 如果不是空字符，将其输出到屏幕，然后继续处理下一个字符。
    SW x6, 0(x7)
    ; Increment pointer
    ADDI x3, x3, 1
    ; Loop
    J PUTSTROUTCHAR
PUTSTRDONE:
    ; Pop x7
    ; Pop x6
    LW x7, 1(x2)
    LW x6, 0(x2)
    ADDI x2, x2, 2
    ; Return 
    JR x1
; 包含字符串 "Hello World\n"，以 ASCII 码形式存储，
; 每个字符占用一个 DAT 指令。字符串以 0x0000 作为结束标志。
STRING:
    DAT 0x0048
    DAT 0x0065
    DAT 0x006C
    DAT 0x006C
    DAT 0x006F
    DAT 0x0020
    DAT 0x0057
    DAT 0x006F
    DAT 0x0072
    DAT 0x006C
    DAT 0x0064
    DAT 0x000A
    DAT 0x0000
