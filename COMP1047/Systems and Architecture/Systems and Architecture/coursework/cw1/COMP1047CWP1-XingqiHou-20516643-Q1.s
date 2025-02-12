.data
prompt1: .asciiz "Enter the value of M: "
prompt2: .asciiz "Enter the value of N: "
overflow: .asciiz "Error: Overflow occurred!"
unexpected: .asciiz "Error: Unexpected character!"
noninteger: .asciiz "Error: Please enter an integer other than decimal!"
newline: .asciiz "\n"
buffer: .space 32
.text
.globl main

main:
#set flag value $t0 as 0
li $t0,0

#load MN value section, use $t0 as flag, $t0=0 set M value, $t0=1 set N value.
loadMN:
beq $t0, 0, loadM
beq $t0, 1, loadN

loadM:
#show prompt for user to load M
li $v0, 4
la $a0, prompt1
syscall

#load M into the buffer, set $t1=0 as initial state of the buffer.
li $v0, 8
li $a1,32
la $a0, buffer
syscall
li $t1,0
j check

loadN:
#show prompt for user to load M.
li $v0, 4
la $a0, prompt2
syscall

#load N into the buffer, set $t1=0 as initial state of the buffer.
li $v0, 8
li $a1,32
la $a0, buffer
syscall
li $t1,0
j check


check:
#initialize all arguments used in the checking process
li $t2,10 #ascii for line break
li $t3,'0'
li $t4,'9'
li $t6,'-'
li $t7,'.'

#go to StringtoInteger when finish checking the whole string
lb $t5, buffer($t1)
beq $t5, $t2, StringtoInteger

#cases when '-' or '.' occurred
beq $t5, $t6,Negative
beq $t5, $t7,Decimal

#cases when not number character occurred
blt $t5,$t3 Unexpected
bgt $t5,$t4 Unexpected

#accumulation
addi $t1, $t1, 1
j check

StringtoInteger:

#set $t1 to store the integer
li $t1,0
li $t2,10
li $t3,'-'

#check if  is a negative number
lb $t4,buffer
beq $t4,$t3,Negatecase
move $t5,$zero

loop:
lb $t4,buffer($t5)
li $t3,10
beq $t4,$t3,Done
li $t3,'0'
sub $t4,$t4,$t3
mul $t1,$t1,$t2
add $t1,$t1,$t4
addi $t5,$t5,1
j loop

Negatecase:
#set negative checking flag $t6 as 1, ignore '-' and continue
move $t5,$zero
addi $t5, $t5, 1 
li $t6,1
j loop


Negate:
#negate the integer and clear the flag $t6
neg $t1,$t1
li $t6,0


Done:
#if flag $t6 equals to 1, negate the integer
li $t7,1
beq $t6,$t7,Negate

#check which number is stored(M/N)
li $t3,1
beq $t0,$zero,Mdone
beq $t0,$t3,Ndone

Mdone:
#store M to $s0
move $s0, $t1

#set $t0 flag to 1, jump back to load N
li $t0,1
j loadMN


Ndone:
#store N to $s1, begin calculation
move $s1, $t1
li $t0,1
j Calculate

Calculate:
# M^3
mul $t0, $s0, $s0
bge $t0, 0x10000000, Overflow
mul $t0, $t0, $s0 
bge $t0, 0x10000000, Overflow 
   
#3M^2N
mul $t1, $s0, $s0 
bge $t1, 0x10000000, Overflow
mul $t1, $t1, $s1  
bge $t1, 0x10000000, Overflow
mul $t1, $t1, 3 
bge $t1, 0x10000000, Overflow
    
#3MN^2
mul $t2, $s0, $s1
bge $t2, 0x10000000, Overflow
mul $t2, $t2, $s1
bge $t2, 0x10000000, Overflow
mul $t2, $t2, 3
bge $t2, 0x10000000, Overflow
    
#9N^3
mul $t3, $s1, $s1 
bge $t3, 0x10000000, Overflow
mul $t3, $t3, $s1
bge $t3, 0x10000000, Overflow
mul $t3, $t3, 9
bge $t3, 0x10000000, Overflow
    
# Add
add $t4, $t0, $t1
bge $t4, 0x10000000, Overflow
add $t5, $t2, $t3
bge $t5, 0x10000000, Overflow
add $t6, $t4, $t5 
bge $t6, 0x10000000, Overflow

j print

Negative:
bne $t1, $zero,Unexpected
addi $t1,$t1,1
j check

Decimal:
#Print noninteger error message
li $v0,4
la $a0,noninteger
syscall

# Print newline
li $v0, 4
la $a0, newline
syscall

# Exit
li $v0, 10
syscall


Unexpected:
#Print unexpected character error message
li $v0,4
la $a0,unexpected
syscall

# Print newline
li $v0, 4
la $a0, newline
syscall

# Exit
li $v0, 10
syscall


Overflow:
#Print overflow error message
li $v0,4
la $a0,overflow
syscall

# Print newline
li $v0, 4
la $a0, newline
syscall

# Exit
li $v0, 10
syscall

print:
move $a0, $t6
li $v0, 1
syscall
    
# Print newline
li $v0, 4
la $a0, newline
syscall
    
# Exit
li $v0, 10
syscall


