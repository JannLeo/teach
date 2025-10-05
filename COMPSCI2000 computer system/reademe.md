第一个ppt

![image-20250908114735176](reademe.assets/image-20250908114735176.png)

![image-20250908114916537](reademe.assets/image-20250908114916537.png)

![image-20250908114928478](reademe.assets/image-20250908114928478.png)

![image-20250908114944243](reademe.assets/image-20250908114944243.png)





![image-20250908114813219](reademe.assets/image-20250908114813219.png)

![image-20250908115001799](reademe.assets/image-20250908115001799.png)

![image-20250908115017263](reademe.assets/image-20250908115017263.png)









![image-20250908114844056](reademe.assets/image-20250908114844056.png)

![image-20250908115029022](reademe.assets/image-20250908115029022.png)

![image-20250908115042044](reademe.assets/image-20250908115042044.png)





![image-20250908115103313](reademe.assets/image-20250908115103313.png)

![image-20250908115246879](reademe.assets/image-20250908115246879.png)

![image-20250908115301607](reademe.assets/image-20250908115301607.png)



![image-20250908115312491](reademe.assets/image-20250908115312491.png)







![image-20250908115133451](reademe.assets/image-20250908115133451.png)

![image-20250908115328158](reademe.assets/image-20250908115328158.png)

> // push 511          ; 注释：对应虚拟机的"push 511"指令
> @511                ; 将常量511加载到A寄存器（A=511）
> D=A                 ; 将A寄存器的值（511）传送到D寄存器（D=511）
> @SP                 ; 将堆栈指针SP的值加载到A寄存器（A=SP的当前值）
> A=M                 ; 将SP指向的内存位置的值（即当前SP值）加载到A寄存器（A=内存[SP]）
> M=D                 ; 将D寄存器的值（511）存入A寄存器指向的内存位置（内存[A]=511）
> ; （注：此处省略了调整SP的步骤，通常push后需SP--，但图中注释为"M=M+1 // SP++"，可能是简化或约定差异）
>
> - `@511`：**加载地址/常量**。将数值 `511` 放入**A寄存器**（Hack计算机中，`@xxx` 用于指定内存地址或常量）。
> - `D=A`：**数据传送**。将A寄存器的值（511）复制到**D寄存器**（D是数据寄存器，用于暂存数据）。
> - `@SP`：**加载SP值**。将堆栈指针SP的当前值放入A寄存器（SP是专用寄存器，指向栈顶下一个位置）。
> - `A=M`：**间接寻址**。将SP指向的内存位置的值（即当前SP值）放入A寄存器（例如，若SP=256，则A=256）。
> - `M=D`：**内存写操作**。将D寄存器的值（511）存入A寄存器指向的内存位置（即内存[256]=511，完成了“压栈”操作）。
>
> ### **3. 为什么 `M=D` 等价于 `内存[A] = 511`？**
>
> 因为 `M` 在Hack汇编中是**A寄存器间接寻址的缩写**，即：
>
> M=memory[A]
>
> 所以 `M=D` 的本质是：
>
> memory[A]=D
>
> 而在前面的步骤中，`D` 已经被赋值为 `511`（来自 `D=A`），`A` 已经被赋值为 `SP` 指向的内存地址（比如 `256`）。因此，`M=D` 最终的结果就是：
>
> memory[A]=511

![image-20250908115339344](reademe.assets/image-20250908115339344.png)





![image-20250908115200163](reademe.assets/image-20250908115200163.png)

要理解图中**可执行文件（二进制代码）** 及其对应的指令行为，需要结合**计算机体系结构的基本组成**和**指令执行流程**。以下是对图中各组件及指令作用的详细解释：
### **一、图中计算机体系结构的核心组件**
图中展示了一个简化的**冯·诺依曼架构**计算机（类似Hack计算机的设计），主要由以下部分组成：
| 组件                                   | 功能                                                         |
| -------------------------------------- | ------------------------------------------------------------ |
| **Instruction Memory**（指令内存）     | 存储程序的二进制指令（如可执行文件中的代码）。               |
| **Program Counter (PC)**（程序计数器） | 存储当前要执行的指令地址，每次执行后自动递增（指向下一条指令）。 |
| **A寄存器**（地址寄存器）              | 存储内存地址（如要访问的变量地址、指令地址）。               |
| **D寄存器**（数据寄存器）              | 存储数据值（如计算结果、变量值）。                           |
| **ALU（算术逻辑单元）**                | 执行算术运算（加、减）和逻辑运算（与、或、非），输出结果（data out）。 |
| **Data Memory (M)**（数据内存）        | 存储程序运行时的数据（如变量、数组），可通过**A寄存器的值**（`RAM(A)`）访问。 |
| **M符号**                              | 表示**A寄存器指向的内存单元**（即 `M = memory[A]`），是间接寻址的缩写。 |
### **二、指令的执行流程**
计算机执行程序的过程遵循**“取指-译码-执行-写回”** 循环，具体步骤如下：
#### 1. 取指（Fetch）
- **Program Counter (PC)** 指向 `Instruction Memory` 中的某条指令地址。
- 从 `Instruction Memory` 中取出当前指令的二进制代码（如可执行文件中的 `1110110010001000`）。
#### 2. 译码（Decode）
- 解析指令类型（**A指令** 或 **C指令**）：
  - **A指令**：二进制代码的第16位（最高位）为 `0`，其余15位是**内存地址**（如 `@511` 对应二进制 `0b0_0000000001111111`，其中 `0` 是第16位，`0000000001111111` 是地址511）。
  - **C指令**：二进制代码的第16位为 `1`，其余15位分为三部分：
    - **comp（bits 15-12）**：指定ALU要执行的运算（如加法、减法、取反）。
    - **dest（bits 11-10）**：指定运算结果的存储目标（如存入D寄存器、A寄存器或内存）。
    - **jump（bits 9-8）**：指定是否跳转到其他指令（如条件跳转）。
#### 3. 执行（Execute）
- 根据译码结果，ALU执行相应运算：
  - 若为**A指令**（如 `@511`）：将地址 `511` 加载到**A寄存器**（`A = 511`）。
  - 若为**C指令**（如 `D = -M`）：ALU计算 `-M`（M是A寄存器指向的内存单元），并将结果存入**D寄存器**（`D = -memory[A]`）。
#### 4. 写回（Write Back）
- 若C指令的 `dest` 字段指定了存储目标（如D、A或M），则将ALU结果写入对应位置：
  - 例如，`D = -M` 会将结果存入D寄存器，而 `M = D` 会将D寄存器的值存入A寄存器指向的内存单元（`memory[A] = D`）。
### **三、可执行文件中的指令示例（以图中二进制代码为例）**
图中可执行文件包含两条指令（假设第一行是A指令，第二行是C指令）：
#### 1. 第一条指令：`0000000000000000`
- **类型**：A指令（第16位为 `0`）。
- **地址**：其余15位均为 `0`，因此是 `@0`（加载地址0到A寄存器）。
- **作用**：将A寄存器设为 `0`（`A = 0`），通常用于初始化或访问内存地址0处的变量。
#### 2. 第二条指令：`1110110010001000`
- **类型**：C指令（第16位为 `1`）。
- **分解**：
  - **comp（bits 15-12）**：`1110` → 对应ALU运算 `-M`（负的M，即 `-memory[A]`）。
  - **dest（bits 11-10）**：`01` → 指定将结果存入**D寄存器**（dest字段 `01` 表示D）。
  - **jump（bits 9-8）**：`00` → 无跳转（jump字段 `00` 表示继续执行下一条指令）。
- **作用**：计算 `-M`（M是A寄存器指向的内存单元，此时A=0，所以M是 `memory[0]`），并将结果存入D寄存器（`D = -memory[0]`）。
### **四、总结：指令的意义**
图中可执行文件的二进制代码对应**具体的硬件操作**：
- **A指令**：用于加载内存地址到A寄存器，为后续访问内存做准备。
- **C指令**：用于执行算术/逻辑运算，并将结果存入寄存器或内存。
整个体系结构的核心逻辑是：**指令通过控制寄存器和ALU，实现对内存数据的读写和运算**，从而完成程序的逻辑（如变量计算、分支判断等）。
### **关键 takeaway**
- 计算机的指令是**二进制代码**，直接控制硬件组件（寄存器、ALU、内存）的行为。
- 指令的执行是**顺序且循环**的（取指→译码→执行→写回），直到程序结束。
- 图中的体系结构是现代计算机的简化模型，理解其组件和流程是学习计算机组成原理的基础。

--------------------------------
以上内容由AI生成，仅供参考和借鉴



![image-20250908115429139](reademe.assets/image-20250908115429139.png)

这张图的核心是**解释“代码如何通过二进制指令指导处理器完成具体操作”**，分为**代码语法（Syntax）**和**代码语义（Semantics）**两个层面，重点展示了**Hack硬件平台对指令的解析逻辑**。以下是详细分解：
### **一、整体主题**
标题“The code directs elements of the processor in order to achieve results”意为：**代码通过按顺序指导处理器的各个组件（寄存器、ALU、内存等），最终实现程序的计算结果**。  
图中左侧是**代码语法**（程序员写的二进制指令），右侧是**代码语义**（硬件如何理解这些指令并转化为具体操作）。
### **二、代码语法（Code Syntax）**
左侧展示了**两条二进制指令**，对应Hack计算机的两种基本指令类型：
1. **第一条指令**：`0000000000000000`，标注为`@0`  
   这是**A指令（Address Instruction）**，用于加载内存地址到**A寄存器**（Hack中A寄存器专门存储内存地址）。
2. **第二条指令**：`11111110111001000`，标注为`M=M+1`  
   这是**C指令（Compute Instruction）**，用于执行算术/逻辑运算（如加法、减法），并将结果存入目标位置（寄存器或内存）。
### **三、代码语义（Code Semantics）**
右侧展示了**Hack硬件平台如何解析上述二进制指令**，将二进制位映射到具体的硬件操作。关键是通过**指令字段的划分**实现功能：
#### 1. A指令（`@0`）的解析
- **Instruction Code（指令码）**：`0` → 表示这是**A指令**（Hack规定：A指令的最高位为`0`）。  
- **Address（地址）**：剩余15位全为`0` → 表示要加载的内存地址是`0`。  
- **硬件操作**：将地址`0`加载到**A寄存器**（`A = 0`），为后续访问内存地址`0`做准备。
#### 2. C指令（`M=M+1`）的解析
C指令的二进制代码（`11111110111001000`）被划分为三个关键字段：
- **Instruction Code（指令码）**：`1` → 表示这是**C指令**（Hack规定：C指令的最高位为`1`）。  
- **ALU Operation Code（ALU运算码）**：`111111101` → 指定ALU要执行的运算。这里对应`M+1`（即“内存单元M的值加1”）。  
  - 注：`M`是**A寄存器间接寻址的缩写**（`M = memory[A]`），因此`M+1`等价于`memory[A] + 1`。  
- **Destination Code（目标码）**：`01` → 指定运算结果的存储位置。这里`01`对应`M`（即**A寄存器指向的内存单元**）。  
  - 因此，`M=M+1`的硬件操作是：`memory[A] = memory[A] + 1`（将A寄存器指向的内存单元的值加1，再存回原位置）。  
- **Jump Code（跳转码）**：`00` → 指定是否跳转。`00`表示**无跳转**（继续执行下一条指令）。
### **四、核心逻辑总结**
1. **代码语法的二进制指令**：是程序员或编译器生成的“原始命令”（如`@0`、`M=M+1`）。  
2. **代码语义的硬件解析**：Hack硬件通过**指令字段的划分**（Instruction Code、Address、ALU Operation Code、Destination Code、Jump Code），将二进制指令转化为具体的硬件操作（如加载寄存器、ALU运算、内存读写）。  
3. **指令执行流程**：  
   - A指令（`@0`）：将地址`0`加载到A寄存器（`A=0`）。  
   - C指令（`M=M+1`）：ALU计算`memory[0]+1`（因为A=0，所以`M=memory[0]`），然后将结果存回`memory[0]`（即`memory[0] = memory[0] + 1`）。  
   通过这种方式，代码一步步指导处理器完成“将内存地址0处的值加1”的操作，最终实现程序的功能。
### **关键 takeaway**
- **指令的字段划分**：A指令和C指令通过最高位（Instruction Code）区分，C指令进一步通过ALU运算码、目标码、跳转码细分功能。  
- **硬件与代码的关系**：代码的语义是硬件设计的核心——二进制指令的每一位都对应硬件组件的控制信号（如ALU选择加法、内存写入使能等）。  
- **顺序执行**：代码按顺序指导处理器，每条指令完成后，程序计数器（PC）自动指向下一条指令，确保操作有序进行。
这张图完美诠释了“代码如何从抽象的语法转化为具体的硬件动作”，是理解计算机底层工作机制的关键。

--------------------------------
以上内容由AI生成，仅供参考和借鉴





![image-20250908115448492](reademe.assets/image-20250908115448492.png)

![image-20250908115613903](reademe.assets/image-20250908115613903.png)

![image-20250908115623681](reademe.assets/image-20250908115623681.png)







![image-20250908115505193](reademe.assets/image-20250908115505193.png)

![image-20250908115635090](reademe.assets/image-20250908115635090.png)

![image-20250908115643101](reademe.assets/image-20250908115643101.png)







![image-20250908115654949](reademe.assets/image-20250908115654949.png)

![image-20250908115809323](reademe.assets/image-20250908115809323.png)











![image-20250908115716808](reademe.assets/image-20250908115716808.png)



![image-20250908115823839](reademe.assets/image-20250908115823839.png)

![image-20250908115832033](reademe.assets/image-20250908115832033.png)







![image-20250908115735873](reademe.assets/image-20250908115735873.png)

![image-20250908115842288](reademe.assets/image-20250908115842288.png)

![image-20250908115848778](reademe.assets/image-20250908115848778.png)







![image-20250908115907863](reademe.assets/image-20250908115907863.png)



![image-20250908115959056](reademe.assets/image-20250908115959056.png)





![image-20250908115930104](reademe.assets/image-20250908115930104.png)





![image-20250908120011987](reademe.assets/image-20250908120011987.png)





第二个PPT







![image-20250908120106041](reademe.assets/image-20250908120106041.png)



**![image-20250908120456255](reademe.assets/image-20250908120456255.png)**

![image-20250908120507935](reademe.assets/image-20250908120507935.png)





![image-20250908120127356](reademe.assets/image-20250908120127356.png)

![image-20250908120516419](reademe.assets/image-20250908120516419.png)









![image-20250908120148829](reademe.assets/image-20250908120148829.png)

![image-20250908120527661](reademe.assets/image-20250908120527661.png)

![image-20250908120542080](reademe.assets/image-20250908120542080.png)

![image-20250908120705474](reademe.assets/image-20250908120705474.png)

![image-20250908120715234](reademe.assets/image-20250908120715234.png)









![image-20250908120624812](reademe.assets/image-20250908120624812.png)

![image-20250908120749271](reademe.assets/image-20250908120749271.png)



![image-20250908120757039](reademe.assets/image-20250908120757039.png)





![image-20250908120644786](reademe.assets/image-20250908120644786.png)

![image-20250908120810898](reademe.assets/image-20250908120810898.png)

![image-20250908120821297](reademe.assets/image-20250908120821297.png)



![image-20250908120833789](reademe.assets/image-20250908120833789.png)

![image-20250908120957100](reademe.assets/image-20250908120957100.png)

![image-20250908121004660](reademe.assets/image-20250908121004660.png)







![image-20250908120859692](reademe.assets/image-20250908120859692.png)

![image-20250908121203687](reademe.assets/image-20250908121203687.png)









![image-20250908120922280](reademe.assets/image-20250908120922280.png)

![image-20250908121022890](reademe.assets/image-20250908121022890.png)

![image-20250908121038426](reademe.assets/image-20250908121038426.png)







![image-20250908121222352](reademe.assets/image-20250908121222352.png)

![image-20250908121322874](reademe.assets/image-20250908121322874.png)

![image-20250908121404214](reademe.assets/image-20250908121404214.png)











![image-20250908121345483](reademe.assets/image-20250908121345483.png)

### **二、通俗解释（用生活例子类比）**

为了更好理解，我们可以用日常场景举例：

#### **例子1：否定合取（¬(A ∧ B)）**

假设：

- A*A* = “今天下雨”
- B*B* = “今天刮风”

原命题：“今天既下雨又刮风”（A∧B）。
否定命题：“今天不是‘既下雨又刮风’”（¬(A∧B)）。

根据德摩根律，这等价于：“今天不下雨 **或** 今天不刮风”（¬A∨¬B）。

- 直观上，“不是两者都发生”意味着“至少有一个没发生”（不下雨或没刮风），符合我们的直觉。

#### **例子2：否定析取（¬(A ∨ B)）**

假设：

- A*A* = “今天吃火锅”
- B*B* = “今天吃烤肉”

原命题：“今天吃火锅 **或** 吃烤肉”（A∨B）。
否定命题：“今天不吃火锅 **且** 不吃烤肉”（¬(A∨B)）。

根据德摩根律，这等价于：“今天既不吃火锅 **也** 不吃烤肉”（¬A∧¬B）。

- 直观上，“不是‘吃其中一个’”意味着“两个都不吃”，完全符合逻辑。

### **三、德摩根律的本质：否定词的“穿透”效应**

德摩根律的核心是**否定词会“穿透”合取或析取，并将其转换为另一种联结词**：

- 否定合取（∧）会变成析取（∨）的否定；
- 否定析取（∨）会变成合取（∧）的否定。

这种转换类似于“反转”逻辑结构，使得复杂命题的否定更容易处理。

![image-20250908121445730](reademe.assets/image-20250908121445730.png)

![image-20250908121452402](reademe.assets/image-20250908121452402.png)

![image-20250908121511451](reademe.assets/image-20250908121511451.png)

![image-20250908121642758](reademe.assets/image-20250908121642758.png)



![image-20250908121655153](reademe.assets/image-20250908121655153.png)





![image-20250908121536321](reademe.assets/image-20250908121536321.png)

![image-20250908121708199](reademe.assets/image-20250908121708199.png)



![image-20250908121717567](reademe.assets/image-20250908121717567.png)



![image-20250908121559840](reademe.assets/image-20250908121559840.png)

![image-20250908121728029](reademe.assets/image-20250908121728029.png)







![image-20250908121746625](reademe.assets/image-20250908121746625.png)

![image-20250908121901028](reademe.assets/image-20250908121901028.png)







![image-20250908121803046](reademe.assets/image-20250908121803046.png)

![image-20250908121953123](reademe.assets/image-20250908121953123.png)

![image-20250908122003644](reademe.assets/image-20250908122003644.png)





![image-20250908121823263](reademe.assets/image-20250908121823263.png)

![image-20250908121925867](reademe.assets/image-20250908121925867.png)

![image-20250908121938408](reademe.assets/image-20250908121938408.png)





![image-20250908122105136](reademe.assets/image-20250908122105136.png)

![image-20250908122210492](reademe.assets/image-20250908122210492.png)



![image-20250908122219346](reademe.assets/image-20250908122219346.png)



![image-20250908122128002](reademe.assets/image-20250908122128002.png)

![image-20250908122230197](reademe.assets/image-20250908122230197.png)







第三个PPT







![image-20250908122916598](reademe.assets/image-20250908122916598.png)

![image-20250908123052389](reademe.assets/image-20250908123052389.png)





![image-20250908122959957](reademe.assets/image-20250908122959957.png)

![image-20250908123109210](reademe.assets/image-20250908123109210.png)



![image-20250908123117398](reademe.assets/image-20250908123117398.png)





![image-20250908123016080](reademe.assets/image-20250908123016080.png)



![image-20250908123125295](reademe.assets/image-20250908123125295.png)









![image-20250908123137211](reademe.assets/image-20250908123137211.png)

![image-20250908123250194](reademe.assets/image-20250908123250194.png)







![image-20250908123312946](reademe.assets/image-20250908123312946.png)

![image-20250908123330493](reademe.assets/image-20250908123330493.png)



![image-20250908123339053](reademe.assets/image-20250908123339053.png)









![image-20250908123214887](reademe.assets/image-20250908123214887.png)

![image-20250908123348884](reademe.assets/image-20250908123348884.png)





![image-20250908123402855](reademe.assets/image-20250908123402855.png)

![image-20250908123549755](reademe.assets/image-20250908123549755.png)

![image-20250908123557224](reademe.assets/image-20250908123557224.png)





![image-20250908123424346](reademe.assets/image-20250908123424346.png)

![image-20250908123611227](reademe.assets/image-20250908123611227.png)

![image-20250908123625682](reademe.assets/image-20250908123625682.png)



![image-20250908123439257](reademe.assets/image-20250908123439257.png)

![image-20250908123641172](reademe.assets/image-20250908123641172.png)

![image-20250908123649607](reademe.assets/image-20250908123649607.png)







![image-20250908123709265](reademe.assets/image-20250908123709265.png)

![image-20250908123908531](reademe.assets/image-20250908123908531.png)

![image-20250908123917772](reademe.assets/image-20250908123917772.png)









![image-20250908123817376](reademe.assets/image-20250908123817376.png)

![image-20250908123930895](reademe.assets/image-20250908123930895.png)



![image-20250908123944542](reademe.assets/image-20250908123944542.png)









![image-20250908123840579](reademe.assets/image-20250908123840579.png)



![image-20250908123955746](reademe.assets/image-20250908123955746.png)

![image-20250908124006403](reademe.assets/image-20250908124006403.png)





![image-20250908124029886](reademe.assets/image-20250908124029886.png)

![image-20250908124142555](reademe.assets/image-20250908124142555.png)



![image-20250908124156077](reademe.assets/image-20250908124156077.png)





![image-20250908124053747](reademe.assets/image-20250908124053747.png)

![image-20250908124214675](reademe.assets/image-20250908124214675.png)







![image-20250908124110307](reademe.assets/image-20250908124110307.png)

![image-20250908124230045](reademe.assets/image-20250908124230045.png)





![image-20250908124249140](reademe.assets/image-20250908124249140.png)

![image-20250908124421603](reademe.assets/image-20250908124421603.png)







![image-20250908124305629](reademe.assets/image-20250908124305629.png)



![image-20250908124432933](reademe.assets/image-20250908124432933.png)







![image-20250908124331088](reademe.assets/image-20250908124331088.png)



![image-20250908131305893](reademe.assets/image-20250908131305893.png)



![image-20250908131315960](reademe.assets/image-20250908131315960.png)







![image-20250908131242797](reademe.assets/image-20250908131242797.png)

![image-20250908131331432](reademe.assets/image-20250908131331432.png)

![image-20250908131338801](reademe.assets/image-20250908131338801.png)

![image-20250908131417753](reademe.assets/image-20250908131417753.png)



![image-20250908131542272](reademe.assets/image-20250908131542272.png)

![image-20250908131549415](reademe.assets/image-20250908131549415.png)











![image-20250908131443224](reademe.assets/image-20250908131443224.png)



![image-20250908131601135](reademe.assets/image-20250908131601135.png)





![image-20250908131458264](reademe.assets/image-20250908131458264.png)

![image-20250908131611182](reademe.assets/image-20250908131611182.png)

![image-20250908131617437](reademe.assets/image-20250908131617437.png)







![image-20250908131700277](reademe.assets/image-20250908131700277.png)

![image-20250908131758731](reademe.assets/image-20250908131758731.png)













![image-20250908131718936](reademe.assets/image-20250908131718936.png)

![image-20250908131809164](reademe.assets/image-20250908131809164.png)









![image-20250908131734366](reademe.assets/image-20250908131734366.png)

![image-20250908131822321](reademe.assets/image-20250908131822321.png)

![image-20250908131832310](reademe.assets/image-20250908131832310.png)







![image-20250908131851310](reademe.assets/image-20250908131851310.png)

![image-20250908131947228](reademe.assets/image-20250908131947228.png)







![image-20250908131907011](reademe.assets/image-20250908131907011.png)



![image-20250908132001584](reademe.assets/image-20250908132001584.png)



![image-20250908132027407](reademe.assets/image-20250908132027407.png)





![image-20250908131932462](reademe.assets/image-20250908131932462.png)

![image-20250908132040383](reademe.assets/image-20250908132040383.png)

![image-20250908132046467](reademe.assets/image-20250908132046467.png)







![image-20250908132109067](reademe.assets/image-20250908132109067.png)

![image-20250908132204510](reademe.assets/image-20250908132204510.png)









![image-20250908132128153](reademe.assets/image-20250908132128153.png)

![image-20250908132214315](reademe.assets/image-20250908132214315.png)











![image-20250908132147944](reademe.assets/image-20250908132147944.png)

![image-20250908132223290](reademe.assets/image-20250908132223290.png)







第四个PPT









![image-20250908132349823](reademe.assets/image-20250908132349823.png)

![image-20250908132516272](reademe.assets/image-20250908132516272.png)









![image-20250908132444717](reademe.assets/image-20250908132444717.png)



![image-20250908132524367](reademe.assets/image-20250908132524367.png)









![image-20250908132455303](reademe.assets/image-20250908132455303.png)

![image-20250908132535514](reademe.assets/image-20250908132535514.png)

![image-20250908132545356](reademe.assets/image-20250908132545356.png)









![image-20250908132611539](reademe.assets/image-20250908132611539.png)

![image-20250908132710003](reademe.assets/image-20250908132710003.png)











![image-20250908132634721](reademe.assets/image-20250908132634721.png)

![image-20250908132721201](reademe.assets/image-20250908132721201.png)











![image-20250908132653684](reademe.assets/image-20250908132653684.png)

**![image-20250908132742007](reademe.assets/image-20250908132742007.png)**







![image-20250908132758872](reademe.assets/image-20250908132758872.png)



![image-20250908132917944](reademe.assets/image-20250908132917944.png)







![image-20250908132838828](reademe.assets/image-20250908132838828.png)

![image-20250908132935878](reademe.assets/image-20250908132935878.png)









![image-20250908132854512](reademe.assets/image-20250908132854512.png)

![image-20250908133045695](reademe.assets/image-20250908133045695.png)











![image-20250908133028100](reademe.assets/image-20250908133028100.png)

![image-20250908133213507](reademe.assets/image-20250908133213507.png)









![image-20250908133106557](reademe.assets/image-20250908133106557.png)

![image-20250908133222772](reademe.assets/image-20250908133222772.png)







![image-20250908133149993](reademe.assets/image-20250908133149993.png)

![image-20250908133242758](reademe.assets/image-20250908133242758.png)





![image-20250908133249865](reademe.assets/image-20250908133249865.png)





![image-20250908133303715](reademe.assets/image-20250908133303715.png)











![image-20250908133334131](reademe.assets/image-20250908133334131.png)







![image-20250908133356520](reademe.assets/image-20250908133356520.png)





![image-20250908133747442](reademe.assets/image-20250908133747442.png)







![image-20250908133759838](reademe.assets/image-20250908133759838.png)

![image-20250908133935067](reademe.assets/image-20250908133935067.png)











![image-20250908133828327](reademe.assets/image-20250908133828327.png)

![image-20250908133957659](reademe.assets/image-20250908133957659.png)



![image-20250908134004848](reademe.assets/image-20250908134004848.png)





![image-20250908133905937](reademe.assets/image-20250908133905937.png)



![image-20250908134101427](reademe.assets/image-20250908134101427.png)





![image-20250908134034827](reademe.assets/image-20250908134034827.png)

![image-20250908134113556](reademe.assets/image-20250908134113556.png)







![image-20250908134128770](reademe.assets/image-20250908134128770.png)

![image-20250908134338872](reademe.assets/image-20250908134338872.png)









![image-20250908134200992](reademe.assets/image-20250908134200992.png)

![image-20250908134331621](reademe.assets/image-20250908134331621.png)







![image-20250908134219403](reademe.assets/image-20250908134219403.png)



![image-20250908134502216](reademe.assets/image-20250908134502216.png)









![image-20250908134413620](reademe.assets/image-20250908134413620.png)

![image-20250908134517993](reademe.assets/image-20250908134517993.png)

![image-20250908134526234](reademe.assets/image-20250908134526234.png)









![image-20250908134449165](reademe.assets/image-20250908134449165.png)

![image-20250908134610173](reademe.assets/image-20250908134610173.png)





![image-20250908134627387](reademe.assets/image-20250908134627387.png)

![image-20250908134658525](reademe.assets/image-20250908134658525.png)