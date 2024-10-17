; ECS 154A loading.asm 
; Just executes immediate values
MAIN: ; Entry point to program
    LI x1, DATA
    LW x2, 0(x1)
    LW x3, 1(x1)
    LW x4, 2(x1)
    LW x5, 3(x1)
    NOP
    NOP
    NOP
DATA:
    DAT 0x048C
    DAT 0x159D
    DAT 0x26AE
    DAT 0x37BF
; LI x1, DATA: 这条指令将 DATA 标签对应的地址加载到寄存器 x1 中。
; LI 是一个伪指令，用于将一个立即数加载到寄存器中。
; 在这个例子中，DATA 标签指向内存中的一个位置，所以 x1 会存储这个地址。

; LW x2, 0(x1): 这条指令将从 x1 指向的内存地址（即 DATA 标签指向的地址）
; 加载一个字（16 位数据）到寄存器 x2 中。

; LW x3, 1(x1): 这条指令将从 x1 指向的地址加上 1（即 DATA 地址 + 1）加载一个字到寄存器 x3 中。

; LW x4, 2(x1): 这条指令将从 x1 指向的地址加上 2（即 DATA 地址 + 2）加载一个字到寄存器 x4 中。

; LW x5, 3(x1): 这条指令将从 x1 指向的地址加上 3（即 DATA 地址 + 3）加载一个字到寄存器 x5 中。

; NOP: 空操作指令，不执行任何操作，只是占用一个 CPU 周期。这里插入了三个 NOP，
; 可能是为了给内存加载指令一些时间来完成。