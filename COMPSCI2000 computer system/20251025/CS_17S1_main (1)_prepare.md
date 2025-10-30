

---

## 第 1 页

![第 1 页](CS_17S1_main (1)_assets/page-001.png)

这张图片的内容是一个考试通知说明，标题为 **“NOTICE: Past Exams”**（“注意：往年试题”）。
下面我为你详细解释每一条内容的含义，并在最后附上一个口语化总结。

---

### 🔹逐条详细解释

1. **“Past exams are provided as-is for reference only.”**
往年考试题仅供参考使用，不会做任何修改或保证内容的准确性。

2. **“The content of this exam reflects course content and learning outcomes as they were at the time this exam was administered.”**
这份考试题反映的是考试当年课程的内容和学习目标，也就是说，它展示的是当时老师讲课的重点和考察方向。

3. **“This course’s content, structure, and/or focus may have changed since this past exam was administered.”**
课程的内容、结构或重点可能在之后发生了变化，也就是说现在的课程可能和当时不一样了。

4. **“As such, the content, structure and types of questions contained herein may differ from those in your final exam.”**
因此，这份往年试题里的题目内容、结构以及题型，可能与你现在要参加的期末考试不一样。
⚠️ 重点提醒：不能完全依赖往年试题复习。

5. **“If you plan on using this as a study resource, be sure to do so in conjunction with the current course’s syllabus and resources to ensure that your study covers the correct content.”**
如果你打算用这份往年试题来复习，一定要结合现在课程的**教学大纲（syllabus）**和**教材、讲义等资源**，确保复习内容是正确的，不要复习错方向。

---

### 🔹总结归纳

这整张图的意思是提醒学生：
往年试题只是一个**学习参考**，不能代表现在考试的内容。课程可能已经改动过，所以题目类型、结构和重点可能完全不同。如果要用旧试题复习，必须同时对照最新的课程大纲与教材，否则容易复习偏了。

---

### 🗣️\[口语化表达]

这张图其实就是说：“嘿，别太信旧试题啦！它只是以前的版本，老师和课程可能早就改了。现在考试的题型、内容都可能不一样。要是你想用它复习，就一定得对照现在的课程大纲和资料，不然复习错方向就糟了。”


---

## 第 2 页

![第 2 页](CS_17S1_main (1)_assets/page-002.png)

这张图是 **澳大利亚阿德莱德大学（The University of Adelaide）** 的一份考试说明页，是2017年第一学期的**期末考试（Primary Examination, Semester 1, 2017）**，课程名称是 **Computer Systems（计算机系统）**，课程代码 **COMP SCI 2000, 7081**。下面我来为你逐条详细解释。

---

### 🔹详细解释部分

#### 🕒考试时间安排

* **Official Reading Time: 10 mins**
正式阅读时间为10分钟，也就是说考试开始后前10分钟你只能看题，不能动笔答题。

* **Writing Time: 120 mins**
正式答题时间为120分钟，也就是2个小时。

* **Total Duration: 130 mins**
整个考试总时长为130分钟（包括10分钟的阅读时间）。

---

#### 🧾考试内容说明

* **Questions: Answer all 12 questions**
你必须回答全部12道题，没有选择题或跳题的选项。

* **Time: 120 mins, Marks: 120 marks (Total)**
总分是120分，时间是120分钟，也就是说平均每题大约10分钟、10分。

---

#### 📋考生须知（Instructions for Candidates）

1. **This is a Closed-book examination.**
这是一场**闭卷考试**，不能带书、笔记或电子资料进入考场。

2. **Begin each answer on a new page.**
每个题目的答案要从新的一页开始写，不能混在一页上。
👉 这是为了方便阅卷老师批改时能清楚分题、评分。

3. **Examination material must not be removed from the examination room.**
考试材料不得带出考场。
包括试卷、草稿纸、答题纸等，全部都必须留在教室内。

---

#### 📚允许携带物品（Materials）

* **Foreign Language Dictionaries are Permitted**
允许携带外语词典（例如英汉词典）。
⚠️ 注意：只能是纸质词典，不能带电子设备。

---

#### ⚠️特别提醒

* **DO NOT COMMENCE WRITING UNTIL INSTRUCTED TO DO SO**
在监考老师宣布可以开始之前，**不得动笔写字！**
如果提前书写，有可能被认为违规。

---

### 🗣️\[口语化表达]

这页其实就是说：“这场考试一共130分钟，前10分钟只能看题不能写，之后有两个小时答12道题，总共120分。是闭卷考试，不能带书，答题时每道题都要从新的一页写，考试材料不能带出教室。你可以带纸质词典，但不能带电子设备。最重要的是——别在老师说开始之前动笔，不然会被警告哦！”


---

## 第 3 页

![第 3 页](CS_17S1_main (1)_assets/page-003.png)

下面是这页试题（第2页）的逐题中文讲解与做法示范。

---

# 基本门电路与布尔逻辑（Basic Gates and Boolean Logic）

## Question 1（共9分）

题干给出表达式：**x ≠ y**
当布尔值 x 与 y 不相等时为真，否则为假。这其实就是 **异或 XOR**。

### (a) i. 画出 “≠” 的真值表（3分）

| x | y | x ≠ y |
| - | - | ----- |
| 0 | 0 | 0     |
| 0 | 1 | 1     |
| 1 | 0 | 1     |
| 1 | 1 | 0     |

说明：只有两者不同（01 或 10）时输出 1，其余为 0。

### (a) ii. 只用 And、Or、Not 门实现 “≠”（6分）

标准实现（等价于 XOR）：

$$
x \ne y \;=\; (x \land \lnot y)\; \lor\; (\lnot x \land y)
$$

实现思路：

1. 先各自取反得到 **¬x**、**¬y**（用 Not 门）。
2. 计算 **x ∧ ¬y** 与 **¬x ∧ y**（用 And 门）。
3. 再对这两个结果做 **Or**（用 Or 门）得到最终输出。
文本电路示意：

```
x ──┐        ┌─ AND ──┐
├─ NOT y ┤        │
y ──┘        └────────┤
├─ OR ── out = x≠y
x ── NOT ─┐            │
├─ AND ──────┘
y ────────┘
```

---

# 布尔算术与 ALU 设计（Boolean Arithmetic and ALU design）

## Question 2（共10分）

提示会参考附录中 Hack ALU 的真值表（图2），这里关注 **Or 运算** 那一行。

### (a) i. 用 And 芯片和一些连线实现 Or 的逻辑表达式（4分）

根据德摩根律，Or 可用 And 与 Not 表示：

$$
\text{Or}(x,y) \;=\; \lnot\big(\; \lnot x \;\land\; \lnot y \;\big)
$$

这里显式包含了 **And** 运算：先把 x、y 各自取反做一次 And，再把结果取反。

### (a) ii. 用真值表证明上式与 Or 等价（3分）

| x | y | ¬x | ¬y | (¬x ∧ ¬y) | ¬(¬x ∧ ¬y) | x ∨ y |
| - | - | -- | -- | --------- | ---------- | ----- |
| 0 | 0 | 1  | 1  | 1         | 0          | 0     |
| 0 | 1 | 1  | 0  | 0         | 1          | 1     |
| 1 | 0 | 0  | 1  | 0         | 1          | 1     |
| 1 | 1 | 0  | 0  | 0         | 1          | 1     |

观察最后两列完全一致，因此 **¬(¬x ∧ ¬y) ≡ x ∨ y**。

### (a) iii. 画出一个使用 16 位 And 芯片实现的 16 位 Or 芯片（3分）

按位实现思路（对16个比特并行）：

$$
\text{Or16}(A,B) \;=\; \text{Not16}\Big(\;\text{And16}\big(\text{Not16}(A),\ \text{Not16}(B)\big)\;\Big)
$$

文本连线示意（每个方块表示对16位总线的并行操作）：

```
A ── Not16 ┐
├─┐
B ── Not16 ┘ │
├─ And16 ── Not16 ── OUT   // OUT 即 Or16(A,B)
─┘
```

实现要点：

* 输入 A、B 各先过 **Not16**（逐位取反）。
* 两路取反后的 16 位总线进入 **And16**。
* And16 的输出再接 **Not16**，得到 16 位 Or 的结果。
* 若需要画门级图，只需标注三块芯片：Not16、And16、Not16，并画清 16 位总线。

---

## 小提示（答题策略）

* 第1题把 “≠” 识别为 XOR 是关键；若不会画电路，写出等价表达式即可得分。
* 第2题核心是用 **德摩根律** 把 Or 改写为 Not-And-Not，并能给出逐位的 16 位实现。

---

🗣️ **\[口语化表达]**
这页主要考两件事：第一题就是让你把 “x≠y” 当成 XOR 来做，先填个真值表（只有不同才为1），然后用基本门搭出来：`(x∧¬y) ∨ (¬x∧y)`。第二题围绕 ALU 的 Or 运算，要求你用 And 来实现 Or。套路就是德摩根律：`Or(x,y) = ¬(¬x ∧ ¬y)`，再用真值表验证一下就行。最后把它扩展成 16 位：先把 A、B 各自 Not16，再 And16，最后再 Not16，一进一出全是16位总线。整体就这么个思路，按这个写基本都能拿满分。


---

## 第 4 页

![第 4 页](CS_17S1_main (1)_assets/page-004.png)

下面是本页（第3页）题目的中文解读与解题步骤。

---

# 时序逻辑（Sequential Logic）

## Question 3（共10分）

题目给了教材图 3.5 的 **程序计数器 PC（16 位计数器）** 定义与时序语义（右侧灰框）：

* **Chip name**: `PC`（16-bit counter）
* **Inputs**: `in[16]`, `inc`, `load`, `reset`
* **Outputs**: `out[16]`
* **时序功能**（按上个周期的控制信号决定本周期输出）

* 若 `reset(t−1)=1`，则 `out(t)=0`
* 否则若 `load(t−1)=1`，则 `out(t)=in(t−1)`
* 否则若 `inc(t−1)=1`，则 `out(t)=out(t−1)+1`
* 否则 `out(t)=out(t−1)`
* 说明：`=` 是 16 位赋值，`+` 是 16 位算术加法。

> **要求**：画出一个 **没有 reset 线** 的 PC（即去掉复位功能），但仍需正确响应 `inc` 和 `load`。可以直接使用大规模芯片（如 `Inc16`、`Register16`、`Mux16`），不用原始门级（如 `Nand`）。

---

## 解题思路与实现（给可直接画图的文本连接说明）

去掉 `reset` 后，功能简化为：

$$
\text{next} =
\begin{cases}
\text{in} & \text{if } load=1\\
out + 1   & \text{else if } inc=1\\
out       & \text{else}
\end{cases}
$$

把“分支”改写成两级多路选择即可：

1. **寄存器**
使用 `Register16` 保存 PC 值：

* `Register16.in = next`
* `Register16.out = out`（同时作为反馈参与下一拍的计算）
* 时钟沿到来时把 `next` 装入，输出在下一个时刻生效。

2. **加一器**
用 `Inc16` 计算 `out+1`：

* `Inc16.in = out`
* `Inc16.out = out_plus_1`

3. **第一级选择（处理 inc）**
用 `Mux16` 在 “保持原值” 与 “加一” 间选择：

* `Mux16_inc.a = out`
* `Mux16_inc.b = out_plus_1`
* `Mux16_inc.sel = inc`
* `Mux16_inc.out = inc_result`

> 语义：`inc=1` 时选择 `out+1`，否则保持 `out`。

4. **第二级选择（处理 load 优先级高于 inc）**
再用一个 `Mux16` 在 “载入 in” 与 “上一步结果” 间选择：

* `Mux16_load.a = inc_result`
* `Mux16_load.b = in`
* `Mux16_load.sel = load`
* `Mux16_load.out = next`

> 语义：`load=1` 时直接装入 `in`，否则采用 inc 分支的结果。这样自然实现了 **load 优先，inc 次之** 的优先级。

5. **最终连线**

```
out ──> Inc16 ─────────────┐
└──────────────┐       │
│       v
└─> Mux16_inc (sel=inc) ──> Mux16_load (sel=load) ──> next
in  ────────────────────────────────────────────────^
next ────────────────────────────────> Register16.in
Register16.out ───────────────────────> out （反馈）
```

> 无 `reset` 引脚；其余保持与标准 PC 一致。若需要上电初值，可在系统层面由外部写一次 `load` 实现，而不是靠 `reset`。

6. **时序说明（与题面 t / t−1 一致）**

* 在时刻 `t−1` 采样控制信号 `inc, load` 和数据 `in`，组合逻辑产生 `next`；
* 时钟上升沿到来后，`Register16` 在时刻 `t` 输出 `out(t)=next(t−1)`；
* 满足题面“若 `load` 则装入 `in`，否则若 `inc` 则 `out+1`，否则保持”。

> 评分点：去掉 reset、保持 `load` 高优先级、`inc` 次优先级、用寄存器反馈实现状态保持、16 位并行连线清楚。

---

### 可选进一步优化（非必须）

* 如果需要显示优先级更直观的单级表达式：

$$
next = \text{Mux16}\big(\text{Mux16}(out,\ out\!+\!1,\ inc),\ in,\ load\big)
$$

外层 `sel=load`，内层 `sel=inc`。

---

🗣️ **\[口语化表达]**
这题就是要你把“PC 计数器”做出来，但**不要复位线**。逻辑很简单：`load=1` 就把 `in` 直接装进寄存器；否则如果 `inc=1` 就把当前 `out` 加一；都不是就原地不动。画图时用两个 `Mux16` 搭优先级：先用一个 `Mux16` 在 `out` 和 `out+1`（`Inc16` 出来）之间选，选择信号是 `inc`；再用另一个 `Mux16` 在“上一步结果”和 `in` 之间选，选择信号是 `load`（所以 load 优先）。选出来的 `next` 喂给 `Register16`，寄存器的输出就是 `out` 并回馈。这样就满足题意了。


---

## 第 5 页

![第 5 页](CS_17S1_main (1)_assets/page-005.png)

下面是这页（第4页）两道题的中文解读与做法步骤，一次性说清。

---

# Hack 汇编与机器码（Hack Assembler and Machine Code）

## Question 4（共10分）

给出的 7 行 **Hack 机器码**（每行 16 位）：

```
0000000000010000
1111110000010000
0000000000010001
1111000111001000
1111110000010000
0000000000000000
1110001100000001
```

### (a) i. 译成 Hack 汇编（7分）

按指令格式（A 指令以 0 开头；C 指令以 111 开头）逐行解码：

1. `0000000000010000` → `@16`
2. `1111110000010000` → `D=M`
3. `0000000000010001` → `@17`
4. `1111000111001000` → `M=M-D`
5. `1111110000010000` → `D=M`
6. `0000000000000000` → `@0`
7. `1110001100000001` → `D;JGT`

### (a) ii. 机器码做了什么（3分）

* `@16; D=M`：把 `RAM[16]` 读到 D。
* `@17; M=M-D`：执行 `RAM[17] = RAM[17] - RAM[16]`。
* `D=M`：D 取 `RAM[17]`（差值）。
* `@0; D;JGT`：若 D>0（即 `RAM[17] > RAM[16]`）则跳到地址 0（通常回到程序开始/死循环），否则顺序执行。
**结论**：比较 `RAM[17]` 与 `RAM[16]`，若前者更大则跳回 0。

---

# 计算机体系结构（Computer Architecture）

## Question 5（6分）

实现 C 指令中的 **JNE**（jump not equal，即“非零跳转”）逻辑盒。输入：`j1 j2 j3`（C 指令的跳转位）、`zr`（ALU 零标志）、`ng`（ALU 负标志）。输出：`load`（PC 的装载信号）。

* Hack 约定：`JNE` 的条件是 **!zr**，与 `ng` 无关。JNE 的跳转编码是 `j1 j2 j3 = 1 0 1`。
* 逻辑表达式：

$$
\text{isJNE} = (j1 \land \lnot j2 \land j3),\quad
load = \text{isJNE} \land \lnot zr
$$

**电路画法（文字示意）：**

```
j1 ──┐
j2 ─ NOT ─┼─ AND3 ── isJNE ─┐
j3 ──┘                     AND ── load
zr ─ NOT ────────────────────┘
```

不使用 `ng`。

---

🗣️ **\[口语化表达]**
这页就两件事：第一，把 7 条 16 位机器码翻成汇编，结果是 `@16, D=M, @17, M=M-D, D=M, @0, D;JGT`，作用是比较 `RAM[17]` 和 `RAM[16]`，要是前者大就跳回地址 0。第二，实现 JNE 的跳转逻辑：当跳转位是 `101` 且 ALU 的 `zr=0` 时给 PC 的 `load` 置 1，所以 `load = (j1 & ~j2 & j3) & (~zr)`，跟 `ng` 没关系。


---

## 第 6 页

![第 6 页](CS_17S1_main (1)_assets/page-006.png)

下面是本页（第5页）**Question 5(b)** 的中文解读与解题说明。

---

# Q5(b) 题意与解法

题目给出 Hack CPU 的结构图，并指出**A/M 选择线（图中有 X 标记）**：

* 该选择线决定 C-instruction 送入 ALU 的一个输入到底来自 **A 寄存器** 还是 **RAM\[A]（记为 M）**。
* **Hack 机器在同一条 C 指令里不能同时把 A 和 M 都作为输入**。
* 例如 `D = M + A` **不是合法**的 Hack 指令。

**问题**：即便硬件允许在同一条指令里同时访问 A 和 M，这样的访问为什么“也不太有用”？给出简要说明。

## 核心解释（如何作答）

1. **功能冗余：两条指令就能等价完成**

* 任何“同时用 A 和 M 做运算”的需求，都可以用**两条**合法 C 指令完成，而且不改变语义：

```
D = M        // 先把 RAM[A] 读到 D
D = D + A    // 再与 A 运算（A 未改变）
```

例如非法的 `D = M + A`，完全可由上面两句实现。
* 因为读取 `M` 不会修改 `A`，所以第二步仍能使用原来的 `A` 值。**因此允许“一条指令同时用 A 和 M”并不会带来表达能力上的新东西，只是最多省一条指令**。

2. **语义上也很少需要**

* 在 Hack 中，**A 通常用作地址寄存器**，而 **M 是该地址处的内存数据**。把“地址值”和“该地址的数据”混在同一条指令里做算术，语义上不常见（地址不是常规数据）。
* 真正常见的是“用内存数据和寄存器数据（如 D）”运算，或“用两个寄存器（D、A）”运算；这些在现有指令集下都能直接或两步完成。

3. **硬件代价与复杂度不值得**

* 同时把 A 与 M 都喂给 ALU，意味着**一次指令要两路来源（其中一路还是内存读取）**。这会增加硬件：需要额外的存储器读端口或暂存/时序，破坏 Hack 的**极简单周期**设计目标。
* 付出更高硬件复杂度，只换来极少的“省一条指令”的收益，**性价比很低**。

**一句话答案要点**：

> 因为任何“同时使用 A 和 M”的计算都可用两条现有合法指令轻松实现（先 `D=M` 再与 `A` 运算），而且把“地址(A)”和“数据(M)”混算并不常见；若硬件支持反而要付出更高复杂度但几乎没有实际收益。

---

🗣️ **\[口语化表达]**
这题想说的是：A 是地址、M 是这个地址里的数据；你要把它俩一起算，其实用两条正常指令就能搞定——先把 M 读进 D，再拿 D 跟 A 算就行了。硬件上要想一条指令同时喂 A 和 M 给 ALU，会增加内存读口/连线，复杂度上去了，但只换来“偶尔省一条指令”，不值当；而且地址和数据混着算本来也不常见。所以就算允许这么干，也没啥实际用处。


---

## 第 7 页

![第 7 页](CS_17S1_main (1)_assets/page-007.png)

下面是本页（第6页）两道题的逐条中文解析与标准写法。

---

# Assembler

## Question 6（12分）

### (a) 把给定 Hack 汇编**手工汇编**成二进制机器码

给定汇编：

```
@x
M=0
@y
M=0
(LOOP)
@x
MD=M+1
@y
M=M+D
@3
D=D-A
@LOOP
D;JLE
```

**符号与地址（两遍扫描要点）**

* 变量从 RAM16 起：`x=16`，`y=17`。
* 标签 `(LOOP)` 绑定到其后一条指令的 ROM 地址。数指令（不数标签）：

```
addr: 0  @x
1  M=0
2  @y
3  M=0
4  @x     <- LOOP 指向这里
5  MD=M+1
6  @y
7  M=M+D
8  @3
9  D=D-A
10  @LOOP
11  D;JLE
```

因此 **LOOP = 4**。

**逐条编码结果（A 指令：0vvvvvvvvvvvvvvv；C 指令：111 a c1..c6 d1 d2 d3 j1 j2 j3）**

```
@x        -> @16 -> 0000000000010000
M=0             -> 1110101010001000   // comp=0, dest=M
@y        -> @17 -> 0000000000010001
M=0             -> 1110101010001000
@x        -> @16 -> 0000000000010000
MD=M+1          -> 1111110111011000   // comp=M+1, dest=MD
@y        -> @17 -> 0000000000010001
M=M+D           -> 1111000010001000   // comp=D+M, dest=M
@3        -> @3  -> 0000000000000011
D=D-A           -> 1110010011010000   // comp=D-A, dest=D
@LOOP     -> @4  -> 0000000000000100
D;JLE           -> 1110001100000110   // comp=D, jump=JLE
```

> 以上 12 行即该程序的**二进制机器码**。

---

# Virtual Machine – Expressions

## Question 7（8分）

### (a) 将 Jack 语句翻译为 Hack VM 代码

Jack：`let d = (2 - x) * (y + 5)`
已知 `d,x,y` 在段 `local` 的索引分别为 `2,5,7`；有函数 `multiply` 接收 2 个实参并返回乘积。

**正确 VM 代码（注意 sub 的操作数顺序是“次顶 − 顶”）：**

```vm
// (2 - x)
push constant 2
push local 5
sub

// (y + 5)
push local 7
push constant 5
add

// 乘法并赋给 d
call multiply 2
pop local 2
```

---

## 速记与得分点

* 第6题先做**符号表**：`x=16，y=17，LOOP=4`；C 指令域：`dest` 顺序是 ADM，`JLE` 的跳码是 110。
* 第7题 `2 - x` 必须先 push 2 再 push x 再 `sub`，否则会变成 `x - 2`。

---

🗣️ **\[口语化表达]**
这一页其实就两件事：先把带变量和标签的那段汇编手动翻成 12 行二进制。变量从 16 开始，标签 `(LOOP)` 指到地址 4，然后按 comp/dest/jump 表把每条指令逐个编码就行；接着把 `let d = (2 - x) * (y + 5)` 写成 VM：先算 `2 - x`（`push 2; push local 5; sub`），再算 `y + 5`，然后 `call multiply 2`，最后 `pop local 2` 存回 d。照这个写基本稳拿分。


---

## 第 8 页

![第 8 页](CS_17S1_main (1)_assets/page-008.png)

下面是本页（第7页）的详细中文讲解，包括 Question 8 和 Question 9 的逐项分析与解答。

---

# Virtual Machine - Subroutines

## Question 8（共 10 分）

### (a) i. `function f n` 的参数含义（3 分）

Hack VM 中 `function f n` 指令的两个参数分别代表：

* **f**：函数名（包含类名的全称，如 `ClassName.FunctionName`）；
* **n**：该函数的局部变量（local variables）数量。
执行这条指令时，虚拟机会创建一个新的栈帧，并在函数开头自动为这些局部变量分配空间，每个都初始化为 0。

---

### (a) ii. 如果没有第二个参数 n，要如何实现 `function c.x 2`？（4 分）

如果 `function` 没有告诉编译器局部变量数，就必须手动生成初始化局部变量的 VM 指令。

等价代码为：

```vm
function c.x
push constant 0
pop local 0
push constant 0
pop local 1
```

解释：

* 原本 `function c.x 2` 会自动生成两次 `push constant 0` 初始化 local 段；
* 现在因为没有 n 参数，只能手动添加；
* 这保证了 local\[0] 和 local\[1] 都存在并被清零。

---

### (a) iii. 为什么 `call` 指令的第二个参数必须提供？（3 分）

因为：

* `call f m` 的第二个参数 **m** 表示要传递给函数的参数数量；
* 翻译器需要用它来计算 **ARG 指针的位置**，即：

```
ARG = SP - m - 5
```

（其中 5 表示返回地址、LCL、ARG、THIS、THAT 五个保存项）
* 如果省略 m，编译器无法正确移动栈指针，也就不能让被调用函数正确取到参数；
* 因此，这个参数是必须的。

---

# Jack

## Question 9（共 8 分）

### (a) nand2tetris 的 Jack 编译器如何确保“从其他类调用构造函数/函数/方法”是正确的？（3 分）

* Jack 编译器**不会跨类全局检查目标函数是否真实存在**，但会根据语法结构判断调用类型。
例如：

* `ClassName.func()` → 编译为**函数或构造函数调用**；
* `objectName.method()` → 编译为**方法调用**（并自动在参数前压入对象引用 `this`）。
* 编译器通过符号表（Symbol Table）识别 `ClassName` 与变量名的区别，生成正确的调用格式（带或不带隐式参数）。
* 这么做的原因是：项目教学目标是让学生理解虚拟机调用约定，而非构建完整链接器，所以编译器只保证语法合法，不检查跨文件定义。

---

### (b) 找出以下 Jack 类定义中的语法错误（5 分）

```jack
01 class x
02 {
03   function int xx(var int n)
04   {
05     if ( n <= 2 ) return 17 ;
06     return y.xxx(n--) ;
07   }
08 }
```

**逐项分析错误：**

1. **参数声明错误**：

* `var` 不能用于函数参数，只能用于函数体内局部变量声明。
* 正确写法：`function int xx(int n)`

2. **if 语句语法错误**：

* Jack 语言中 `if` 语句的语法是
`if (condition) { statements } [else { statements }]`
* 必须加花括号 `{}` 包围语句块。
* 正确：`if (n < 3) { return 17; }`

3. **比较运算符错误**：

* Jack 只支持 `<`, `>`, `=`，没有 `<=`。
* 可以改为：`if (n < 3)`。

4. **自减运算符错误**：

* Jack 不支持 `n--` 或 `++`。
* 应改成：`n = n - 1; return y.xxx(n);`

> 以上为语法错误。`y` 未声明属**语义错误**（符号未定义），非语法错误，因此不列入答案。

---

🗣️ **\[口语化表达]**
这页主要讲函数与子程序的 VM 机制，还有 Jack 的语法。
首先，`function f n` 里 f 是函数名，n 是局部变量数；如果没有 n，就得自己手动写几条 `push constant 0` 给 local 段占位。`call f m` 里的 m 也不能省，因为编译器要靠它算出 ARG 指针，否则参数会乱套。
接着是 Jack 部分：编译器不会真去查另一个类的函数存不存在，只靠符号表区分类名和对象名，按规则生成调用。最后那段 Jack 代码错了一堆：参数不能加 `var`，`if` 要有花括号 `{}`，不能写 `<=`，也不支持 `n--`。改好这几个就没问题啦。


---

## 第 9 页

![第 9 页](CS_17S1_main (1)_assets/page-009.png)

下面是本页（第8页）**Question 10** 的中文讲解与参考答案。

---

# Parsing

## Question 10（共8分）

### 题意

把下面这句 **Jack** 代码按照语法（只能为**每个非终结符**建一个 XML 节点）改写成 XML。
代码：`let x[ix] = y ;`
要求：从 `letStatement` 作为根节点开始；**关键词、标识符、符号**（如 `let`、`x`、`[`、`]`、`=`、`;` 等）可以省略节点。

Jack（nand2tetris）相关产生式（只取本题用到的）：

```
letStatement → 'let' varName ('[' expression ']')? '=' expression ';'
expression   → term (op term)*
term         → integerConstant | stringConstant | keywordConstant
| varName | varName '[' expression ']' | '(' expression ')' | unaryOp term
```

本题中：

* `varName` 是 **x**（终结符，不建节点）；
* 左侧是 **数组形式**，因此有一个 **index 的 expression**（即 `ix`，本质是一个 `term`/`varName`）；
* 右侧 **RHS** 是一个 **expression**（即 `y`，同样是一个 `term`/`varName`）。

### 参考 XML（**仅包含非终结符**，符合“每个非终结符一个节点”的要求）

```xml
<letStatement>
<!-- array index: x[ ix ] -->
<expression>        <!-- index expression -->
<term/>           <!-- varName: ix -->
</expression>

<!-- right-hand side: y -->
<expression>        <!-- RHS expression -->
<term/>           <!-- varName: y -->
</expression>
</letStatement>
```

> 说明：上面**不为** `let`、`x`、`[`、`]`、`=`、`;` 等终结符建节点；`ix` 与 `y` 作为标识符也不单独建节点，只以 `<term/>` 占位，满足“仅非终结符建节点”的要求。如果你想更直观，可在 `<term>` 里加上文字注释或属性标明是 `ix`、`y`（题目允许省略终结符节点）。

---

### 作答要点/评分点

* 根节点必须是 **`letStatement`**；
* 包含 **两个 `expression`**：一个代表数组 **索引**（来自 `x[ ... ]`），一个代表 **右值**（`= ...`）；
* 每个 `expression` 下至少有一个 **`term`**；
* 不为关键词/符号/标识符建立节点（或即便建了也不加分，题干允许省略，重点在**非终结符**齐全与结构正确）。

---

🗣️ **\[口语化表达]**
这题就是把 `let x[ix] = y;` 画成**语法树的 XML**，而且只给**非终结符**建节点。根是 `<letStatement>`，里面要有两个 `<expression>`：第一个是数组下标 `ix` 的表达式，第二个是右边 `y` 的表达式；每个表达式里面放一个 `<term>` 占位就行。像 `let`、`x`、`[`、`]`、`=`、`;`、以及标识符本身都算终结符，可以不建节点。按我给的那个 XML 抄就对了。


---

## 第 10 页

![第 10 页](CS_17S1_main (1)_assets/page-010.png)

下面是本页（第9页）**Question 11：Code Generation** 的逐题中文解析与标准答案。

---

# Question 11（总分 19）

## (a) 把给定 Jack 代码片段翻译成 Hack VM 代码

> 已知：`class Complex` 有 4 个实例字段，声明顺序 **aa, bb, cc, dd**（其中 **aa 为 Array**）。
> 当前方法头：`method Complex useful(Complex a, Complex b) { ... }`
> 方法调用约定：`argument 0` 为隐式 `this`，`a → argument 1`，`b → argument 2`；字段映射到 `this` 段：`aa→this 0`，`bb→this 1`，`cc→this 2`，`dd→this 3`。

### i. `let b = Complex.new(3,2);`（4 分）

```vm
push constant 3
push constant 2
call Complex.new 2
pop argument 2        // b ← new(3,2)
```

### ii. `aa[7] = a;`（6 分）

```vm
push this 0           // base = aa
push constant 7
add                   // base + 7
pop pointer 1         // THAT = base+7
push argument 1       // a
pop that 0            // *THAT = a
```

### iii. `return b;`（2 分）

```vm
push argument 2
return
```

### iv. `let bb = dd;`（3 分）

```vm
push this 3           // dd
pop this 1            // bb = dd
```

---

## (b) 画出符号表（4 分）

> 位置：在 **解析完 getSerial 方法里的变量声明** `var int ignore_me;` 之后。

给定代码（节选）：

```jack
class SerialNums {
static int id ;
field  int myid ;

constructor SerialsNums new(int key) {
let myid = id ;
return this ;
}

method int getSerial(int password) {
var int ignore_me ;
return myid ;
}
}
```

**类级符号表（Class Scope）**

| name | type | kind   | index |
| ---: | ---- | ------ | ----: |
|   id | int  | static |     0 |
| myid | int  | field  |     0 |

**子程序级符号表（Subroutine Scope；当前位于 `getSerial`）**

|       name | type | kind     | index |
| ---------: | ---- | -------- | ----: |
|   password | int  | argument |     0 |
| ignore\_me | int  | var      |     0 |

> 说明：方法的隐式 `this` 不作为符号表条目列出；构造器 `new(int key)` 的参数与本方法无关，属于另一个子程序作用域。

---

### 得分小贴士

* 方法参数与字段的段映射要写对：`argument` 与 `this`。
* 数组写入套路：`base+index → THAT`，再 `pop that 0`。
* 符号表分两张：类级（`static/field`）与子程序级（`argument/var`），索引从 0 递增。

---

🗣️ **\[口语化表达]**
这页要把几句 Jack 代码翻成 VM 并列出符号表。方法里 `a` 在 `argument 1`、`b` 在 `argument 2`，字段 `aa/bb/cc/dd` 对应 `this 0..3`。

* `b = Complex.new(3,2)`：`push 3; push 2; call Complex.new 2; pop argument 2`。
* `aa[7] = a`：先把 `aa` 的基址取出来加 7，写到 `THAT`，再把 `a` 存到 `that 0`。
* `return b`：`push argument 2; return`。
* `bb = dd`：`push this 3; pop this 1`。
符号表方面，类表有 `id(static0)`、`myid(field0)`；到了 `getSerial`，子程序表就是 `password(argument0)` 和 `ignore_me(var0)`。照这个写就稳了。


---

## 第 11 页

![第 11 页](CS_17S1_main (1)_assets/page-011.png)

下面是本页（第10页）**Question 12** 的中文解析与标准答题要点。

---

# Jack OS, Optimisation

## Question 12（共7分）

### (a) 为什么在 Hack 机器的 ALU中加入**16位乘法器**，会显著增加“把 A 和 D 置 0”这类简单指令的执行时间？（3分）

**核心原因：临界路径（critical path）变长 → 时钟周期被迫拉长。**

* Hack 的 ALU是**组合电路**，同一个数据通路要同时支持所有运算。
* 一旦把**乘法器**并入 ALU，为了在一拍内完成乘法，**乘法器的传播延迟**（远大于加法/常量输出）就会出现在可能的选择路径/多路复用器之后，使**最坏情况延迟**变大。
* 处理器时钟必须按**最慢的操作**设定（满足乘法的延迟），因此**即便执行“输出 0”这类本来很快的操作**，也要用更长的时钟周期。
* 结论：**添加乘法器会拖慢所有指令**（包括 `A=0`、`D=0`），因为它提高了全 ALU 的最坏路径延迟。

> 可顺带指出：若 ALU 通过更大的多路复用器统一选择结果，乘法器还会让**多路复用和扇出**更重，进一步加大延迟。

---

### (b) 处理器物理实现的**三**个方面决定功耗？如何计算？（4分）

聚焦 CMOS 数字电路的主功耗来源（动态功耗为主，辅以静态）：

1. **供电电压 V**
2. **时钟频率 f**
3. **等效开关电容 C\_eff**（由晶体管尺寸/连线负载/门数及**切换活动因子 α** 决定）

**动态功耗**（开关充放电）：

$$
P_{dyn} \approx \alpha \, C_{\text{eff}} \, V^2 \, f
$$

* 降低 V、f、C\_eff 或活动因子 α 都能降功耗。

**静态/泄漏功耗**（器件不切换也耗电）：

$$
P_{leak} \approx I_{leak} \cdot V
$$

* 由工艺、阈值电压、温度与晶体管数目决定。

**总功耗**：$P_{total} \approx \alpha C_{\text{eff}} V^2 f + I_{leak} V$。

---

🗣️ **\[口语化表达]**
这页就两问：第一，往 ALU 里塞了个16位乘法器，会把整条数据通路的**最慢延迟**拉长，时钟周期被迫加大，所以连“置0”这种本来很快的指令也要等更久。第二，功耗主要看三件事：**电压V、频率f、等效电容C\_eff（含切换率α）**，公式就是 **P≈α·C\_eff·V²·f**，再加上泄漏 **P\_leak=I\_leak·V**，两者相加就是总功耗。


---

## 第 12 页

![第 12 页](CS_17S1_main (1)_assets/page-012.png)

下面是本页（第11页，附录）内容的中文解读与使用方法说明。

---

# 这页在讲什么？

本页给了 **Hack ALU 的接口图（Figure 1）** 和 **ALU 真值表（Figure 2）**。

* **接口图**告诉你 ALU 的输入/输出：

* 数据输入：`x[16]`、`y[16]`
* 控制位输入：`zx nx zy ny f no`（6 个 1bit）
* 数据输出：`out[16]`
* 状态标志输出：`zr`（out 是否为 0），`ng`（out 的符号位是否为 1，即负数）
* **真值表**告诉你：给定 6 个控制位如何把 `x`、`y` 变换并组合成 `out`，以及能实现哪些常见操作（0、1、-1、x、y、!x、!y、-x、-y、x+1、y+1、x-1、y-1、x+y、x-y、y-x、x\&y、x|y）。

---

# 6 个控制位各自的作用

按硬件实现的顺序可以理解为“先预处理输入，再选择运算，再可能取反输出”：

1. **预置/改造 x**

* `zx`：若为1，则把 x 清零（送 0）；若为0，保留 x。
* `nx`：对“预置后的 x”按位取反（1→0，0→1）。

2. **预置/改造 y**

* `zy`：若为1，则把 y 清零；若为0，保留 y。
* `ny`：对“预置后的 y”按位取反。

3. **选择运算**

* `f`：为1用**加法**（`x + y`），为0用**按位与**（`x & y`）。

4. **后置处理**

* `no`：对上一步的结果 `out` 取反（为1时取反，为0时原样）。

> **标志位**：
>
> * `zr = 1` 当且仅当 `out == 0`；
> * `ng = 1` 当且仅当 `out` 的最高位（符号位）为 1（即负数）。

---

# 如何使用真值表（读表 + 例子）

真值表的每一行对应一组控制位，会标出得到的函数 `f(x,y)= ...`。使用时：

1. 先确定想要的运算（如 `x+y` / `x&y` / `0` / `-1` / `!x` 等）；
2. 在表里找到这一行；
3. 读出该行的 6 个控制位，即可驱动 ALU。

常见操作（给出**正确的一组**控制位，便于记忆和考试使用）：

* **`x + y`**：`zx=0 nx=0 zy=0 ny=0 f=1 no=0`
* **`x & y`**：`zx=0 nx=0 zy=0 ny=0 f=0 no=0`
* **`0`**：`zx=1 nx=0 zy=1 ny=0 f=1 no=0`
* **`1`**：`zx=1 nx=1 zy=1 ny=1 f=1 no=1`
* **`-1`**：`zx=1 nx=1 zy=1 ny=0 f=1 no=0`
* **`x`**：`zx=0 nx=0 zy=1 ny=1 f=0 no=0`（y 被清零并取反两次，相当于0）
* **`y`**：`zx=1 nx=1 zy=0 ny=0 f=0 no=0`
* **`!x`**：`zx=0 nx=1 zy=1 ny=1 f=0 no=1`（等价于把 x 取反输出）
* **`x-1`**、**`x+1`** 等自增/自减、取负 `-x` 等也都能在表中直接查到对应控制位。

> 小技巧：
>
> * 需要“把某一侧置 0”时，用 `z*`=1；需要“按位取反”时，用 `n*`=1。
> * `f=1` 走加法，`f=0` 走按位与；最后 `no` 再决定是否把结果整体取反。

---

# 标志位的用法（和跳转相关）

* 执行完 ALU，硬件会据 `out` 自动置位：

* `zr=1` ⇔ `out==0`；
* `ng=1` ⇔ `out` 为负（最高位=1）。
* Hack 的跳转（如 `JGT/JLT/JNE` 等）正是根据 **`zr`、`ng`** 判断的，例如 `JNE` 只看 `!zr`。

---

🗣️ **\[口语化表达]**
这页就是 ALU 的“使用手册”：6 个小开关（`zx nx zy ny f no`）先把 x、y 清零/取反，再选是加法还是与，最后再决定要不要把结果取反；输出除了 16 位结果外，还送出 `zr`（是否为0）和 `ng`（是否为负）。你要啥功能就去真值表找那一行，比如 `x+y` 就是 `0 0 0 0 1 0`，`x&y` 是 `0 0 0 0 0 0`，要常量 0 就把 x、y 都清零再选加法（`1 0 1 0 1 0`）。查到控制位，塞进 ALU，标志位也会自动给你算好，后面的跳转就能用了。


---

## 第 13 页

![第 13 页](CS_17S1_main (1)_assets/page-013.png)

这页（第12页）主要是 Hack 机器指令编码的**格式与二进制结构说明**，没有题目，但它是前几页汇编题（例如第6题）的关键参考资料。下面详细讲每一部分的意思和使用方法。

---

## 一、A-指令（@value）

### 格式说明

A 指令形如：

```
@value
```

其中 `value` 可以是：

* 非负整数（例如 `@21`）
* 或一个符号（例如 `@LOOP`、`@i`），汇编器会在符号表查到其对应地址。

### 二进制格式

A 指令的机器码是 **16位**，以 **0** 开头：

```
0 v v v v v v v v v v v v v v
```

* 第一位永远是 0（表示这是 A 指令）。
* 后 15 位是地址或常数的二进制值。

**例如：**

```
@21  →  0000000000010101
```

---

## 二、C-指令（dest = comp ; jump）

C 指令用来描述计算、存储与条件跳转。
一般形式如下：

```
dest = comp ; jump
```

三部分可任选：

* **comp**：计算部分（必须有）
* **dest**：可选，用来指定把结果存到哪个寄存器/内存（如 D、M、A、MD、AM、AD、AMD）
* **jump**：可选，用于控制跳转（如 JGT、JEQ、JMP 等）

**例子：**

```
D=M+1       // comp=M+1, dest=D
D;JGT       // comp=D, jump=JGT
M=D+1;JMP   // dest=M, comp=D+1, jump=JMP
```

---

## 三、C 指令的二进制格式

16 位格式如下：

```
1 1 1 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3
```

* **前三位固定为 111**（表明是 C 指令）
* **a c1\~c6**：共 7 位表示 comp（计算操作）
* **d1\~d3**：3 位表示 dest（目标寄存器）
* **j1\~j3**：3 位表示 jump（跳转条件）

---

## 四、comp 字段（Figure 5）

`comp` 字段（a, c1\~c6）决定 ALU 做什么计算。

* 当 `a=0` → 计算中使用 **A 寄存器**；
* 当 `a=1` → 使用 **M（内存\[A]）**。

| comp | 对应 c1\~c6（二进制） | 含义     |   |   |
| :--- | :------------- | :----- | - | - |
| 0    | 101010         | 常数 0   |   |   |
| 1    | 111111         | 常数 1   |   |   |
| -1   | 111010         | 常数 -1  |   |   |
| D    | 001100         | D      |   |   |
| A    | 110000         | A      |   |   |
| M    | 110000（a=1）    | M      |   |   |
| D+1  | 011111         | D+1    |   |   |
| A+1  | 110111         | A+1    |   |   |
| D-1  | 001110         | D-1    |   |   |
| A-1  | 110010         | A-1    |   |   |
| D+A  | 000010         | D+A    |   |   |
| D-A  | 010011         | D-A    |   |   |
| A-D  | 000111         | A-D    |   |   |
| D\&A | 000000         | D\&A   |   |   |
| D    | A              | 010101 | D | A |

---

## 五、dest 字段（存储目标）

三位二进制分别对应：

|  位  | 含义  | 1表示存储到    |
| :-: | :-- | :-------- |
|  d1 | A 位 | A 寄存器     |
|  d2 | D 位 | D 寄存器     |
|  d3 | M 位 | 内存地址 \[A] |

例如：
\| dest | d1 d2 d3 |
\|:-----|:--:|:--:|
\| null | 0 0 0 |
\| M | 0 0 1 |
\| D | 0 1 0 |
\| MD | 0 1 1 |
\| A | 1 0 0 |
\| AM | 1 0 1 |
\| AD | 1 1 0 |
\| AMD | 1 1 1 |

---

## 六、jump 字段（跳转条件）

| 跳转条件 | j1 j2 j3 | 含义      |
| :--- | :------: | :------ |
| null |    000   | 不跳转     |
| JGT  |    001   | 若 out>0 |
| JEQ  |    010   | 若 out=0 |
| JGE  |    011   | 若 out≥0 |
| JLT  |    100   | 若 out<0 |
| JNE  |    101   | 若 out≠0 |
| JLE  |    110   | 若 out≤0 |
| JMP  |    111   | 无条件跳转   |

---

## 七、完整例子

指令：

```
D=M+1;JGT
```

拆解：

* comp = M+1 → `a=1 c1~c6=110111`
* dest 无（=空）→ `d1d2d3=000`
* jump = JGT → `j1j2j3=001`

拼接：

```
111 1 110111 000 001
```

即：

```
1111110111000001
```

---

🗣️ **\[口语化表达]**
这一页其实是 Hack 机器指令的“说明书”。A 指令超简单，就是 `@` 开头，后面数值转成二进制放到 15 位里；C 指令稍复杂，是“111 + 运算 + 目的地 + 跳转”。要看运算怎么写，就查那个大表：如果用 A 就 a=0，用 M 就 a=1；D、A、M、+1、-1、|、& 全都有编码。存哪儿就改 dest 位，跳不跳就看 jump 位。比如 `D=M+1;JGT` 就是 `1111110111000001`。这页主要就是帮你在写 Hack 汇编题（像第6题那种）时查表转机器码的。


---

## 第 14 页

![第 14 页](CS_17S1_main (1)_assets/page-014.png)

下面是本页（第13页，附录）的中文解读与“怎么用”的说明。它包含三张表：**C 指令的目的地位（dest）**、**跳转位（jump）**、以及 **Hack 预定义符号**。

---

# Figure 6：C-instruction 的目的地位（dest）

* 三个位 **d1 d2 d3** 分别对应 **A、D、M** 三个目的寄存器/内存：

* **d1=1** → 结果写入 **A**
* **d2=1** → 写入 **D**
* **d3=1** → 写入 **M**（即 RAM\[A]）
* 组合即可同时写多处（如 AD、AM、MD、AMD）。
* 表中助记符（Mnemonic）就是我们写汇编时的 `dest=` 部分；右侧文字描述是“结果被存到哪里”。

**快速记忆**：dest 的位顺序固定是 **A D M**（从高到低：d1 d2 d3）。

**例子**

* `D=M+1` → dest=D → **d1d2d3 = 010**
* `AMD=D-1` → dest=AMD → **111**
* `M=D` → dest=M → **001**

---

# Figure 7：C-instruction 的跳转位（jump）

* 三个位 **j1 j2 j3** 描述跳转条件；它们和 ALU 输出的符号/零标志（`out<0`, `out=0`, `out>0`）对应。
* 助记符与含义：

* **000 null**：不跳转
* **001 JGT**：若 `out > 0` 跳
* **010 JEQ**：`out == 0`
* **011 JGE**：`out ≥ 0`
* **100 JLT**：`out < 0`
* **101 JNE**：`out ≠ 0`
* **110 JLE**：`out ≤ 0`
* **111 JMP**：无条件跳

**例子**

* `D;JLE` → comp=D，jump=JLE → **j1j2j3 = 110**
* `0;JMP` → 跳转恒真（常写成死循环）

**实操要点**：是否跳转由 ALU 的 `zr`、`ng` 决定；编译成机器码时把 jump 三位放到尾部。

---

# Figure 8：Hack 预定义符号（符号名 → RAM 地址）

| 符号         | 含义/段            | 地址    |
| ---------- | --------------- | ----- |
| **SP**     | 栈顶指针            | 0     |
| **LCL**    | 当前函数的 Local 段基址 | 1     |
| **ARG**    | Argument 段基址    | 2     |
| **THIS**   | THIS 段基址        | 3     |
| **THAT**   | THAT 段基址        | 4     |
| **R0–R15** | 通用寄存器别名         | 0–15  |
| **SCREEN** | 屏幕内存起始          | 16384 |
| **KBD**    | 键盘内存起始          | 24576 |

**使用规则**

* 在 A 指令中可直接写这些符号：如 `@SP`、`@SCREEN`，汇编器替换为相应地址。
* **变量符号**（非预定义、非标签）从 **RAM\[16]** 起自动分配：第一次出现的变量取 16，下一个 17，以此类推（这条不在本页，但与本表配套使用）。

---

## 汇编到机器码时怎么用这三张表？

1. **确定 comp**（见上一页 Figure 5），得到 `a c1..c6`。
2. **根据本页 Figure 6** 把目标写入位置转换成 **d1 d2 d3**。
3. **根据本页 Figure 7** 把跳转条件转换成 **j1 j2 j3**。
4. 拼出 16 位 C 指令：`111 a c1..c6 d1 d2 d3 j1 j2 j3`。
5. 若是 A 指令，若写 `@SP/@SCREEN` 等，直接代换地址后编码为 `0 + 15位地址`。

**完整例子**
`D=M+1;JGT` →

* comp `M+1` → `a=1, c=110111`
* dest 空 → `000`
* jump `JGT` → `001`
机器码：`111 1 110111 000 001` → **1111110111000001**

---

🗣️ **\[口语化表达]**
这页就是三张“速查表”：

* 第一张告诉你 C 指令要把结果存到哪（A/D/M），就把 **dest 的 ADM 三位**设成 1 或 0；
* 第二张告诉你 **jump 的三位**怎么写，对应 `out` 的大小关系（JGT/JEQ/JMP…）；
* 第三张列出了所有 **预定义符号**的内存地址（SP=0、LCL=1、SCREEN=16384、KBD=24576…）。
写汇编时，A 指令用这些符号很方便；C 指令则用这两张表把 `dest` 和 `jump` 变成二进制，和上一页的 `comp` 一起拼成 16 位机器码，妥妥的。


---

## 第 15 页

![第 15 页](CS_17S1_main (1)_assets/page-015.png)

这页（第14页）是 **Jack 语言的语法定义（grammar）**，用于说明 Jack 编译器如何解析源代码。它并没有题目，但为前面的题（比如 Parsing、Code Generation、Jack 语法分析相关）提供规则依据。
下面是详细解释每一部分的意思，以及在考试或编译器实现中该如何使用。

---

## 一、Lexical Elements（词法单元）

这一部分定义了 Jack 语言的基本“单词”，也就是**token 类型**。

| 项目                  | 含义                      | 举例                                                                                                     |              |
| ------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------ | ------------ |
| **keyword**         | Jack 保留字（系统关键字）         | `class`, `function`, `method`, `let`, `if`, `return`, `do`, `while`, `true`, `false`, `null`, `this` 等 |              |
| **symbol**          | 特殊符号                    | \`{ } ( ) \[ ] . , ; + - \* / &                                                                        | < > = \~\` 等 |
| **integerConstant** | 整型常数，范围 0–32767         | `0`, `100`, `32767`                                                                                    |              |
| **stringConstant**  | 字符串常数（双引号包裹，不含换行）       | `"Hello World"`                                                                                        |              |
| **identifier**      | 标识符，用于变量名、函数名、类名，不以数字开头 | `x`, `sum`, `_index`, `Point3D`                                                                        |              |

> **用途**：词法分析（Lexical Analysis）时，编译器扫描源文件并根据这些规则分割出 token。

---

## 二、Statements（语句）

定义了 Jack 程序由哪些语句组成及其结构。

### statements

表示由多个 `statement` 组成的语句块（即 `{ ... }` 里的内容）。

### statement

语句类型包括：

* `letStatement` → 赋值语句
* `ifStatement` → 条件语句
* `whileStatement` → 循环语句
* `doStatement` → 调用子程序语句
* `returnStatement` → 返回语句

### 各语句结构

1. **letStatement**

```
let varName (‘[’ expression ‘]’)? = expression ;
```

说明：赋值语句，可以对数组元素赋值。
例：`let x = 3;` 或 `let arr[i] = y;`

2. **ifStatement**

```
if ( expression ) { statements } (else { statements })?
```

可选 `else` 块。
例：

```jack
if (x < 5) {
let y = 0;
} else {
let y = 1;
}
```

3. **whileStatement**

```
while ( expression ) { statements }
```

例：`while (i < 10) { let i = i + 1; }`

4. **doStatement**

```
do subroutineCall ;
```

调用方法但不接收返回值。
例：`do Screen.drawLine();`

5. **returnStatement**

```
return expression? ;
```

可带返回值，也可以空返回。
例：`return;` 或 `return x;`

---

## 三、Expressions（表达式）

表达式定义如何构成值。

### expression

```
term (op term)*
```

表示一个或多个 `term` 由运算符连接组成。
例：`x + 5 * y`

### term

```
integerConstant | stringConstant | keywordConstant | varName |
varName [ expression ] | subroutineCall | ( expression ) | unaryOp term
```

说明一个最小的“项”，可能是：

* 常数（整型或字符串）
* 变量
* 数组元素
* 调用
* 括号表达式
* 单目运算（取负、按位非）

### subroutineCall（子程序调用）

有两种形式：

1. 直接调用：`subroutineName ( expressionList )`
2. 通过对象/类调用：`(className | varName) . subroutineName ( expressionList )`

例如：

```
do move();
do Math.multiply(x, y);
```

### expressionList（参数列表）

```
(expression (',' expression)*)?
```

逗号分隔的表达式序列，可为空。

### op（运算符）

`+ - * / & | < > =`
（注意：乘除最终会调用 OS 库函数 `Math.multiply` 与 `Math.divide`）

### unaryOp（单目运算）

`-` 或 `~`（负号、按位取反）

### keywordConstant（特殊常量）

`true`, `false`, `null`, `this`

---

## 四、用途总结

* 在**编译器的语法分析（Parsing）阶段**，Jack 代码按此规则生成 XML 树。
* 例如题目 “Turn `let x[ix] = y;` into XML” 就是用这些规则逐层展开：

```
<letStatement>
<keyword>let</keyword>
<identifier>x</identifier>
<symbol>[</symbol>
<expression>...</expression>
<symbol>]</symbol>
<symbol>=</symbol>
<expression>...</expression>
<symbol>;</symbol>
</letStatement>
```

---

🗣️ **\[口语化表达]**
这页其实就是 Jack 语言的“语法说明书”。上面先告诉你它有哪些关键词（像 class、function、let、if、return 这些），接着列出语句结构，比如 `let` 怎么写、`if` 要带括号和大括号、`do` 是子程序调用、`return` 可有可无表达式。下面那块讲表达式怎么构成，什么是 term、expression、subroutineCall。像 `x + 5`、`arr[i]`、`do Math.multiply(x, y)` 都是根据这套规则来的。
总结一句话：**这页是你写语法分析器或 XML 结构时的标准模板**，按照它的产生式定义去递归解析，整个 Jack 编译器的 Parser 就能跑通。
