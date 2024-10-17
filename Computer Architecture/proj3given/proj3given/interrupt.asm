; ECS 154A interrupt.asm 
; Loads a sinwave into the LED matrix and repeatedly starts over
MAIN: ; Entry point to program
    ; Setup the stack at 32512 (I/O starts at 32736), not necessary 
    LI x1, 32512
    ; Load the data location address
    LI x5, ARRAY
    ; Load Buffer Tail Address
    LI x4, BUFTAIL
    ; Load Head Tail Address
    LI x3, BUFHEAD
    ; Load TTY addr
    LI x2, 0x7FF1
    ; Load IVECT Address
    LI x6, 0x7FFF
    ; Load ISR addr
    LI x7, ISR
    ; Set IVECT
    SW x7, 0(x6)

; Main loop
MAINLOOP:
    ; Disable interrupts
    SFI x0, 0x00
    ; Load BUFTAIL
    LW x6, 0(x4)
    ; Load BUFHEAD
    LW x7, 0(x3)
    ; Enable interrupts
    SFI x0, 0x20
    ; Compare values
    BEQ x6, x7, MAINLOOP
READCHAR:
    ; Calculate address ARRAY + BUFHEAD
    ADD x6, x5, x7
    ; Load char from array
    LW x6, 0(x6)
    ; Store char in TTY
    SW x6, 0(x2)
    ; Load mask
    LI x6, 0x001F
    ; Increment BUFHEAD
    ADDI x7, x7, 1
    ; Modulus of 16
    AND x7, x7, x6
    ; Store BUFHEAD
    SW x7, 0(x3)
    ; Jump back to beginning of loop
    J MAINLOOP
    ; Outer loop reinitializes the loop variable and starts inner loop
ISR:
    ; Push x7, x6, x5, x4, x3, x2, var
    ADDI x1, x1, -7
    SW x7, 6(x1)
    SW x6, 5(x1)
    SW x5, 4(x1)
    SW x4, 3(x1)
    SW x3, 2(x1)
    SW x2, 1(x1)
    ; Load the data location address
    LI x5, ARRAY
    ; Load Buffer Tail Address
    LI x4, BUFTAIL
    ; Load KB Address
    LI x3, 0x7FF0
    ; Load index mask 
    LI x2, 0x001F
ISRLOOP:
    ; Read from KB
    LW x7, 0(x3)
    ; Store in var on stack
    SW x7, 0(x1)
    ; Load Buffer Tail
    LW x6, 0(x4)
    ; Calculate target
    ADD x7, x5, x6
    ; Increment BUFTAIL
    ADDI x6, x6, 1
    ; Modulus of 16
    AND x6, x6, x2
    ; Store BUFTAIL
    SW x6, 0(x4)
    ; Load var from stack
    LW x6, 0(x1)
    ; Store in array
    SW x6, 0(x7)
    ; Compare I flag
    SF x7, x0
    SRLI x7, x7, 6 
    ; Jump back to loop
    BNE x7, x0, ISRLOOP

    ; Pop x7, x6, x5, x4, x3, x2
    LW x7, 6(x1)
    LW x6, 5(x1)
    LW x5, 4(x1)
    LW x4, 3(x1)
    LW x3, 2(x1)
    LW x2, 1(x1)
    ADDI x1, x1, 7
    ; Return from ISR
    RTI
BUFHEAD:
    DAT 0x0000
BUFTAIL:
    DAT 0x0000
; Array
ARRAY:
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000
    DAT 0x0000