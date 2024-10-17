; ECS 154A rtype0.asm
; Just executes the r-type instructions on x0, esssentially NOP
MAIN: ; Entry point to program
    ADD x0, x0, x0		
    SUB x0, x0, x0
    AND x0, x0, x0
    OR  x0, x0, x0
    XOR x0, x0, x0
    SLL x0, x0, x0
    SRL x0, x0, x0
    SRA x0, x0, x0
; ADD x0, x0, x0: 计算 x0 + x0 的结果存储在 x0 中，结果仍为零。
; SUB x0, x0, x0: 计算 x0 - x0 的结果存储在 x0 中，结果仍为零。
; AND x0, x0, x0: 对 x0 与 x0 进行按位与操作，结果仍为零。
; OR x0, x0, x0: 对 x0 与 x0 进行按位或操作，结果仍为零。
; XOR x0, x0, x0: 对 x0 与 x0 进行按位异或操作，结果仍为零。
; SLL x0, x0, x0: 将 x0 的值左移 x0 位，结果仍为零。
; SRL x0, x0, x0: 将 x0 的值右移 x0 位（逻辑右移），结果仍为零。
; SRA x0, x0, x0: 将 x0 的值右移 x0 位（算术右移），结果仍为零。
