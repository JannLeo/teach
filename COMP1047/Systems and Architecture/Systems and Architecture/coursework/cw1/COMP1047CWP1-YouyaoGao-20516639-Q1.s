.data

promptM: .asciiz "Enter an integer for M: "
promptN: .asciiz "Enter an integer for N: "
overflowMsg: .asciiz "Error: Overflow occurred!\n"
unexpected: .asciiz "Error: Unexpected character!\n"
noninteger: .asciiz "Error: Please enter an integer other than decimal!\n"
newline: .asciiz "\n"
buffer: .space 32

.text
.globl main

main:
    # Initialize $t1 to 0
    li $t1, 0
    # Print "Enter an integer for M:\n "
    li $v0, 4
    la $a0, promptM
    syscall
    # Read string M
    li $v0, 8
    li $a1, 32
    la $a0, buffer
    syscall
    j CheckM

CheckM:
    # Initialize all arguments
    li $t2, 10  # ascii for line break
    li $t3, '0' # ascii for '0'
    li $t4, '9' # ascii for '9'
    li $t6, '-' # ascii for '-'
    li $t7, '.' # ascii for '.'

    # Go to StringtoIntegerM when finish checking
    lb $t5, buffer($t1)
    beq $t5, $t2, StringtoIntegerM

    # Cases when '-' occurred
    beq $t5, $t6, NegativeM
    # Cases when '.' occurred
    beq $t5, $t7, Decimal

    # Cases when not number character occurred
    blt $t5, $t3, Unexpected
    bgt $t5, $t4, Unexpected

    # Accumulation
    addi $t1, $t1, 1
    j CheckM

LoadandReadN:
    # Initialize $t1 to 0
    li $t1, 0
    # Print "Enter an integer for N:\n "
    li $v0, 4
    la $a0, promptN
    syscall
    # Read string N
    li $v0, 8
    li $a1,32
    la $a0, buffer
    syscall
    j CheckN
   
CheckN:
    # Initialize all arguments
    li $t2, 10  # ascii for line break
    li $t3, '0' # ascii for '0'
    li $t4, '9' # ascii for '9'
    li $t6, '-' # ascii for '-'
    li $t7, '.' # ascii for '.'

    # Go to StringtoIntegerN when finish checking
    lb $t5, buffer($t1)
    beq $t5, $t2, StringtoIntegerN

    # Cases when '-' occurred
    beq $t5, $t6, NegativeN
    # Cases when '.' occurred
    beq $t5, $t7, Decimal

    # Cases when not number character occurred
    blt $t5,$t3, Unexpected
    bgt $t5,$t4, Unexpected

    # Accumulation
    addi $t1, $t1, 1
    j CheckN

StringtoIntegerM:
    #  Set $t1 to store the integer
    li $t1, 0
    li $t2, 10
    li $t3, '-'

    # Check if  is a negative number
    lb $t4, buffer
    beq $t4, $t3, NegatecaseM
    move $t5, $zero

    loopM:
        lb $t4, buffer($t5)
        li $t3, 10
        beq $t4, $t3, DoneM
        li $t3, '0'
        sub $t4 ,$t4, $t3
        mul $t1, $t1, $t2
        add $t1, $t1, $t4
        addi $t5, $t5, 1
    j loopM

NegatecaseM:
    # Set negative checking flag $t6 as 1, ignore '-' and continue
    move $t5, $zero
    addi $t5, $t5, 1 
    li $t6, 1
    j loopM

NegatecaseN:
    # Set negative checking flag $t6 as 1, ignore '-' and continue
    move $t5, $zero
    addi $t5, $t5, 1 
    li $t6, 1
    j loopN

DoneM:
    # If flag $t6 equals to 1, negate the integer
    li $t7, 1
    beq $t6, $t7, NegateM

    # Store M to $s0
    move $s0, $t1
    
    j LoadandReadN

StringtoIntegerN:
    #  Set $t1 to store the integer
    li $t1, 0
    li $t2, 10
    li $t3, '-'

    # Check if  is a negative number
    lb $t4, buffer
    beq $t4, $t3, NegatecaseN
    move $t5, $zero

    loopN:
        lb $t4, buffer($t5)
        li $t3, 10
        beq $t4, $t3, DoneN
        li $t3, '0'
        sub $t4, $t4, $t3
        mul $t1, $t1, $t2
        add $t1, $t1, $t4
        addi $t5, $t5, 1
    j loopN

DoneN:
    # If flag $t6 equals to 1, negate the integer
    li $t7, 1
    beq $t6, $t7, NegateN

    # Store N to $s1
    move $s1, $t1
    
    j Calculate

Calculate:
    # Calculate 3N
    add $t2, $s1, $s1     # $t2 = N + N =2N
    bge $t2, 0x10000000, overflow   # Overflow check for 2N
    add $t2, $t2, $s1     # $t2 = 2N + N = 3N
    bge $t2, 0x10000000, overflow   # Overflow check for 3N

    # Calculate (M + 3N)
    add $t3, $s0, $t2     # $t3 = M + 3N
    # Overflow check for (M + 3N)
    bge $t3, 0x10000000, overflow   # Overflow check for M + 3N

    # Calculate M^2
    mul $t5, $s0, $s0     # $t5 = M^2
    bge $t5, 0x10000000, overflow   # Overflow check for M^2

    # Calculate N^2
    mul $t6, $s1, $s1     # $t6 = N^2
    bge $t6, 0x10000000, overflow   # Overflow check for N^2

    # Calculate 3N^2
    add $t7, $t6, $t6      # $t7 = N^2 + N^2 = 2N^2
    bge $t7, 0x10000000, overflow   # Overflow check for 2N^2
    add $t7, $t7, $t6      # $t7 = 2N^2 + N^2 = 3N^2
    bge $t7, 0x10000000, overflow   # Overflow check for 3N^2

    # Calculate M^2 + 3N^2
    add $t5, $t5, $t7     # $t5 = M^2 + 3N^2
    bge $t5, 0x10000000, overflow   # Overflow check for M^2 + 3N^2

    # Calculate (M + 3N) * (M^2 + 3N^2)
    mult $t3, $t5              # Perform multiplication (M + 3N) * (M^2 + 3N^2)
    mflo $t8                   # Move the lower 32 bits of the result to $t8
    mfhi $t9                   # Move the higher 32 bits of the result to $t9
    bnez $t9, overflow         

    # Print the result
    li $v0, 1
    move $a0, $t8
    syscall

    # Print newline
    li $v0, 4
    la $a0, newline
    syscall

    # Exit the program
    j exit

NegativeM:
    bne $t1, $zero, Unexpected
    addi $t1, $t1, 1
    j CheckM

NegativeN:
    bne $t1, $zero, Unexpected
    addi $t1, $t1, 1
    j CheckN

Decimal:
    # Print noninteger error message
    li $v0, 4
    la $a0, noninteger
    syscall
    # Exit the program
    j exit

Unexpected:
    # Print unexpected character error message
    li $v0, 4
    la $a0, unexpected
    syscall
    # Exit the program
    j exit

NegateM:
    # Negate the integer and clear the flag $t6
    neg $t1, $t1
    li $t6, 0
    j DoneM

NegateN:
    # Negate the integer and clear the flag $t6
    neg $t1, $t1
    li $t6, 0
    j DoneN

overflow:
    # Print overflow message
    li $v0, 4
    la $a0, overflowMsg
    syscall
    # Exit the program
    j exit

exit:
    # Exit the program
    li $v0, 10
    syscall