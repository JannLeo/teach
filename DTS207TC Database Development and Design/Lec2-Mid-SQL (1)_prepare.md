

---

## 第 1 页

![第 1 页](Lec2-Mid-SQL (1)_assets/page-001.png)

**提问：** 什么意思 详细解释

这是这门课第2次课（Lecture 2）的封面页。逐行解释如下：

- **左上角横线 + 右上角校徽**：右上是西交利物浦大学（Xi’an Jiaotong–Liverpool University）的校徽与英文校名，表示课程所属学校。
- **“DTS207TC Database Development and Design”**：这是课程代码和课程名称。
  - **DTS207TC**：课程代码（DTS 可能指 Data/Database/IT 方向，207 表示大二层级，TC 可能是教学单元/班级代号）。
  - **Database Development and Design**：课程名“数据库开发与设计”。
- **“Lecture 2 — Mid-level SQL”**：第2讲，主题是**中阶 SQL**。
  - “中阶”通常介于入门与高级之间，意味着不会停留在最基础的 `SELECT ... FROM ... WHERE ...`，会进入实际开发常用但又不是最尖端的SQL技能。
- **“Di Zhang, Autumn 2025”**：授课教师（Di Zhang）与学期（2025年秋季）。
- **“Page titles with \* will not be assessed”**：带星号（*）的页面标题不计入考核范围（不会考试或评分），用来提示哪些内容是扩展/参考。

### “Mid-level SQL” 一般会学什么？

不同老师侧重点会略有差异，但典型中阶SQL包含以下模块（供你对齐预期）：

1. **连接（JOIN）高级用法**
   - `INNER/LEFT/RIGHT/FULL JOIN` 的差异与选择
   - 多表连接、别名、连接条件优化
2. **分组与聚合**
   - `GROUP BY`、`HAVING` 与常见聚合函数（`COUNT/SUM/AVG/MAX/MIN`）
   - 按多列分组、汇总与过滤顺序（从句执行顺序）
3. **子查询与相关子查询**
   - `IN/EXISTS/NOT EXISTS`、标量子查询
   - 相关子查询的性能与可替代的写法（如用JOIN或窗口函数）
4. **集合运算**
   - `UNION/UNION ALL/INTERSECT/EXCEPT` 的差异与使用场景
5. **窗口函数（如果纳入中阶）**
   - `OVER(PARTITION BY ... ORDER BY ...)`
   - 排名/移动聚合（`ROW_NUMBER/RANK/DENSE_RANK/LAG/LEAD`）
6. **条件表达式与数据转换**
   - `CASE WHEN`、`COALESCE/NULLIF`、类型/日期函数
7. **约束与数据一致性（与“设计”关联）**
   - 主键/外键/唯一约束/检查约束的查询与影响
8. **性能与可读性初步**
   - 索引对查询的影响（入门级别）
   - 避免常见反模式（如在可索引列上大量函数运算）

> 上面是“中阶SQL”常见内容的**通用范畴**，实际讲义以老师为准；带 `*` 的标题出现时表示该页主题不考试。

### 你需要/可以提前做的准备

- 复习**基础SQL**：SELECT 基础、WHERE 条件、ORDER BY、LIMIT、基本函数。
- 了解**主键/外键**和**范式**的基本概念（配合“开发与设计”理解表结构）。
- 安装或准备一个可运行SQL的环境（如 PostgreSQL、MySQL、SQLite、SQL Server 或在线SQL平台），方便边学边练。

如果你把接下来的讲义页也发来，我可以逐页给你中文讲解与示例查询。

---

## 第 2 页

![第 2 页](Lec2-Mid-SQL (1)_assets/page-002.png)

**提问：** 什么意思 详细解释

这是讲义里标注了“*Office hours”（带*号，表示**不计入考核**）的一页，主要告诉你**老师/助教的联系信息与接待时间（Office hours）**。逐项说明如下：



## 核心意思



* **Office hours**：老师固定的接待时段；学生可在这个时间段到办公室当面提问（无需预约，通常先到先谈）。

* **Preferred means of contact**：首选联系方式（本页均为 Email）。

* **Room number**：办公室房间号与所在楼栋。

* **Office telephone number**：办公室座机（如有）。



## 本页具体信息（从表格读取）



* **课程负责人（Module Leader）：Di Zhang**



  * **办公室**：D-5026（TC Campus – Building D）

  * **接待时间**：**周四 & 周五 10:00–12:00**（地点 D5026）

  * **邮箱**：[Di.Zhang@xjtlu.edu.cn](mailto:Di.Zhang@xjtlu.edu.cn)

  * **座机**：051289167604

  * **首选联系**：Email



* **联合授课教师（co-lecturer）**



  * **Hejia Qiu**



    * 办公室：D-5020（TC Campus – Building D）
    
    * 接待时间：**周二 & 周四 14:00–16:00**
    
    * 邮箱：[Hejia.Qiu@xjtlu.edu.cn](mailto:Hejia.Qiu@xjtlu.edu.cn)
    
    * 首选联系：Email

  * **Xiaowu Sun**



    * 办公室：**D-5076**
    
    * 接待时间：**周二 14:00–16:00；周四 10:00–12:00**
    
    * 邮箱：[Xiaowu.Sun@xjtlu.edu.cn](mailto:Xiaowu.Sun@xjtlu.edu.cn)
    
    * 首选联系：Email

  * **Affan Yasin**



    * 办公室：D-5021（TC Campus – Building D）
    
    * 接待时间：**周二 13:30–15:30；周四 13:30–15:30**
    
    * 邮箱：[Affan.Yasin@xjtlu.edu.cn](mailto:Affan.Yasin@xjtlu.edu.cn)
    
    * 首选联系：Email

  * **Hengyan Liu**



    * 办公室：D-5005（TC Campus – Building D）
    
    * 接待时间：**周三 13:00–15:00；周五 13:00–15:00**
    
    * 邮箱：[Hengyan.Liu@xjtlu.edu.cn](mailto:Hengyan.Liu@xjtlu.edu.cn)
    
    * 首选联系：Email



* **助教（TA）**：BiwEN MENG、ZHEPENG LI、HAORAN ZHAO、FEI REN（表中给出姓名与学邮，但**未列出固定 office hours**；联系请用 Email）



## 下面的提示（Tips）



* **“You can come to ML’s office without sending emails in office hours.”**

  含义：在**课程负责人的接待时间**里，你**可以直接去办公室**，**不需要**提前发邮件预约。



## 你可以怎么用



* 想当面请教：对应老师/负责人在其 office hours 直接去指定房间。

* 不在接待时间或需发资料：发邮件（页面已给出邮箱）。

* 助教没有固定接待时间：建议先邮件沟通再约时间。



如果你需要，我可以把这些时间汇总成你手机日历的事件提醒格式给你。


---

## 第 3 页

![第 3 页](Lec2-Mid-SQL (1)_assets/page-003.png)

**提问：** 什么意思 详细解释

这是“\*SQL Interview Questions Website”（带 \* 号，说明这一页内容**不计入考试/评分**）的说明页，给出**面试常见的 SQL 题库网站**并提醒真实面试通常**不允许使用 AI 或上网**。



## 列出的站点（做什么、适合谁）



* **China Big Company（国内大厂）**



  * **nowcoder（牛客网）/ta/sql**：国内求职最常见的刷题平台之一，按公司/难度/标签筛选 SQL 题，题型贴近国内校招与社招笔试。

  * **mianshiya（面试鸭）/tag/SQL**：聚合各公司面经与题目，SQL 标签页里有真题与解析，适合了解出题风格与频率。

* **International Company（海外/外企）**



  * **LeetCode（数据库题库）**：经典 SQL 练习集合，数据表设计规范、测点清晰，覆盖从基础到中高阶（JOIN、子查询、窗口函数等）。

  * **StrataScratch**：偏数据分析/数据科学岗的 SQL 面试题，很多题出自真实公司（如 Airbnb、Amazon），数据更贴近业务场景。



## 下面的提示



> **“You will be asked to be tested without AI and Internet in real interview…”**

> 意思是：**真实面试中做 SQL 题通常不允许使用 AI 或联网搜索**，要靠你**当场独立完成**。



## 建议怎么用这些资源高效备战



1. **分层刷题**



   * 基础：过滤/排序、`GROUP BY/HAVING`、常用聚合。

   * 进阶：多表 `JOIN`、子查询（`IN/EXISTS`）、集合运算（`UNION/INTERSECT/EXCEPT`）。

   * 中高阶：**窗口函数**（`ROW_NUMBER/RANK/LAG/LEAD`）、条件表达式（`CASE WHEN`）、日期与字符串处理。

2. **离线训练**

   面试不让上网 → 建议在本地装个 **SQLite/MySQL/PostgreSQL**，把题目 CSV/建表语句导入后**本地写并跑**。

3. **刻意练“可读性 + 正确性 + 性能常识”**



   * 先写出能 AC 的版本，再考虑是否能用窗口函数/更优 JOIN 改写。

   * 熟悉空值处理：`NULL`、`COALESCE/IFNULL/NULLIF`。

4. **模拟白板/纸笔**

   定时 20–30 分钟，在纸上写出 SQL；结束后再到数据库验证。

5. **对标岗位**



   * 数据分析/BI：StrataScratch + LeetCode 数据库题。

   * 国内校招后端/数据：牛客网 + 面试鸭真题更贴近用人方。



如果你告诉我你的目标岗位和当前水平，我可以给你做一个**两周刷题清单**（每天 5–8 题、附必会知识点与复盘模板）。


---

## 第 4 页

![第 4 页](Lec2-Mid-SQL (1)_assets/page-004.png)

**提问：** 什么意思 详细解释

这是“\*Tips on CW”的说明页——**CW = Coursework（课程作业）**。带星号 \* 的页通常表示**不计入考试**，只是给你完成作业的建议与评分关注点。四个关键词分别代表评作业最常看的维度：



## 1) Correctness（正确性）



* 含义：你的解答是否**逻辑正确、输出符合题目要求**。

* 对 SQL 作业的典型要求



  * 结果集的**行数、列名、数据类型**与题目一致。

  * 充分处理 **NULL、重复值、边界日期、大小写** 等。

  * 测试多组用例（而不是只对样例数据有效）。

* 自检：用老师给的测试数据或自己构造反例去验证；与期望输出逐列对比。



## 2) Efficiency（效率）



* 含义：方案是否**高效、可扩展**，在真实数据量下不会拖垮性能。

* 对 SQL 的常见做法



  * 优先用合适的 **JOIN** 与过滤条件，避免不必要的笛卡尔积。

  * 只取需要的列（避免 `SELECT *`）；尽量在**过滤前聚合**。

  * 能用 **窗口函数** 就不要写低效的相关子查询。

  * 注意可利用索引的写法（在可索引列上避免函数包裹）。

* 自检：看执行计划（`EXPLAIN`），关注是否走索引、是否全表扫描、临时表是否过多。



## 3) Completeness（完整性）



* 含义：是否**按要求交全**，每个问题都回答，**输入/输出/假设**都明确。

* 对 SQL 作业



  * 每题都有 SQL 与**结果说明/截图**；多问多答的题要逐项编号。

  * 如果有数据建模/ER 图/约束，需**同步提交**且与 SQL 一致。

  * 说明任何必要的**假设**（如时区、去重口径）。

* 自检：用题目清单做勾选；复核“文件是否缺失、路径是否对”。



## 4) Document quality（文档质量）



* 含义：**可读性、结构化、规范性**。让阅卷人快读、易复现。

* 对 SQL/数据类作业



  * 代码有**模块化与注释**（解释业务口径、难点 SQL 的思路）。

  * 统一格式：缩进、别名、命名（`snake_case`/`camelCase`）一致。

  * 提交 **README**：数据来源与预处理、运行步骤、依赖、结果解读。

  * 图表/表格**标题、单位、结论**齐全；结论先行，证据随后。



---



### 交付前 1 分钟清单（可直接照着对）



* [ ] 结果与题意 100% 对齐：列名/顺序/口径一致，边界样例通过

* [ ] 复杂查询至少有一版 `EXPLAIN` 检查，无明显全表扫/相关子查询爆炸

* [ ] 每问均有答案与必要说明，文件不缺、可直接运行

* [ ] 代码与文档排版整齐、注释清楚；README 说明如何复现



如果你把作业题目或 SQL 发我，我可以按这四条给你逐项打分并指出能加分的改进点。


---

## 第 5 页

![第 5 页](Lec2-Mid-SQL (1)_assets/page-005.png)

**提问：** 什么意思 详细解释

这页讲的是**连接（JOIN）**——把两张表按某种规则“拼在一起”，返回一张**新表**（关系代数里依然是一个“关系”）。



## 核心要点逐条解释



* **Join operations take two relations and return another relation**

  JOIN 操作以两张表（关系）为输入，输出还是一张表。你可以继续在这张“新表”上再做筛选/分组/再连接。



* **Join = 受条件限制的笛卡尔积**

  两表做**笛卡尔积**会得到“所有可能的行组合”（m×n 行）。JOIN 的本质是在此基础上**加一个匹配条件**（如主外键相等），并**选择需要保留的列**，从而得到有意义的行配对。

  例：`A JOIN B ON A.id = B.a_id` 只保留 `A.id == B.a_id` 的配对行。



* **JOIN 常作为 FROM 子句里的子查询使用**

  你可以在 `FROM (子查询/已连接的结果) AS t` 上继续写 `WHERE/GROUP BY/HAVING/SELECT` 等，让查询结构化、分步骤完成。



* **三类 JOIN（本页罗列）**



  1. **Natural join（自然连接）**



     * 自动按**同名列**做等值匹配，并且**只保留一份同名列**。
    
     * 风险：列名一改或同名但语义不同，会产生错误匹配；实际生产中一般**不建议使用**。
    
     * SQL：`SELECT * FROM A NATURAL JOIN B;`

  2. **Inner join（内连接）**



     * 只返回**两边都匹配**的行（交集）。最常用。
    
     * SQL：`SELECT ... FROM A INNER JOIN B ON A.id = B.a_id;`

  3. **Outer join（外连接）**



     * 在内连接基础上，**保留未匹配的一侧**（用 `NULL` 填充另一侧列）。
    
     * 分为：



       * **LEFT OUTER JOIN**：保留左表全部；
    
       * **RIGHT OUTER JOIN**：保留右表全部；
    
       * **FULL OUTER JOIN**：左右都保留（并集，非匹配端用 `NULL`）。



## 一个极简示例



表 A（用户）：



| id | name |

| -- | ---- |

| 1  | Ann  |

| 2  | Bob  |

| 3  | Cat  |



表 B（订单）：



| a\_id | amount |

| ----- | ------ |

| 1     | 100    |

| 1     | 80     |

| 4     | 50     |



* **INNER JOIN**（`A.id = B.a_id`）：

  只要匹配到就返回 → 行：`(1, Ann, 100)`, `(1, Ann, 80)`；`Bob/Cat`无订单被过滤；`a_id=4`无对应用户也被过滤。

* **LEFT JOIN**：

  在 INNER 的基础上，还保留左表未匹配的 `Bob(2), Cat(3)`，它们右侧列为 `NULL`。

* **RIGHT JOIN**：

  在 INNER 的基础上，还保留右表未匹配的 `a_id=4` 这一行，左侧列为 `NULL`。

* **FULL JOIN**：

  LEFT + RIGHT 的并集：既保留 `Bob/Cat`，也保留 `a_id=4`。



## 写法与小技巧



* **显式列出连接条件**：



  ```sql

  SELECT A.id, A.name, B.amount

  FROM A

  JOIN B ON A.id = B.a_id;       -- 推荐显式 ON；避免 USING/NATURAL 的隐式匹配陷阱

  ```

* **避免 `SELECT *`**：只取需要的列，减少宽表与歧义。

* **多个条件/多表连接**：



  ```sql

  FROM A

  JOIN B ON A.id = B.a_id AND B.status = 'paid'

  JOIN C ON B.c_id = C.id

  ```

* **自然连接的坑**：同名列自动匹配 —— 列名变化就会“悄悄改语义”；不熟不要用。



## 何时选哪种 JOIN？



* 仅要“匹配到的记录” → **INNER**

* 以左表为主做覆盖、右表只是补充 → **LEFT**

* 以右表为主 → **RIGHT**（或调换左右写 LEFT）

* 需要“并集视角”→ **FULL**（注意有些数据库不支持 FULL，可用 `UNION` + 反连接模拟）



如果你把题目或表结构贴出来，我可以给出最合适的 JOIN 写法和可视化结果示意。


---

## 第 6 页

![第 6 页](Lec2-Mid-SQL (1)_assets/page-006.png)

**提问：** 什么意思 详细解释

这页在讲 **Natural Join（自然连接）** 的概念、语法与等价写法。



## 这页文字在说什么



* **Natural join 会自动用两表中“同名列”的相等关系做匹配**（等值连接），并且**在结果里只保留一份同名列**。

  也就是说你不用写 `ON A.id = B.id`，数据库会自己找出同名列（如 `id`），并用它们做连接条件。

* 下面给了一个查询例子：



  ```

  select name, course_id

  from students, takes

  where students.ID = takes.ID;

  ```



  这是一种**显式条件**的写法（旧式逗号连接 + WHERE 条件）。

* 同样逻辑可以用 **NATURAL JOIN** 来写：



  ```

  select name, course_id

  from students natural join takes;

  ```



  这里假设 `students` 与 `takes` 都有名为 `ID` 的列，于是自然连接会自动用 `ID` 做等值匹配，并且结果集中 `ID` 只保留一份。



> 备注：幻灯片第二条的英文叙述可能有小口误（写了 instructors），但代码示例用的是 `students` 与 `takes`，以代码为准即可。



## 和其它写法的对照



* `NATURAL JOIN` 等价于 “用所有同名列做 `=` 连接，并只保留一份这些同名列”。

* 许多数据库里，你也可以用更可控的：



  ```sql

  -- 更推荐：明确指定列名

  SELECT name, course_id

  FROM students

  JOIN takes USING (ID);      -- 只用 ID 连接，且结果只保留一份 ID



  -- 或者完全显式

  SELECT s.name, t.course_id

  FROM students s

  JOIN takes t ON s.ID = t.ID; -- 结果会保留 s.ID 和 t.ID 两列，除非你在 SELECT 里不取

  ```



## 自然连接的优点与风险



**优点**



* 语法简短，写起来省事。

* 自动去重同名列，结果更“干净”。



**风险（面试与生产中常考/常见）**



1. **脆弱性**：只要任一表改了列名、或多出一个同名列，`NATURAL JOIN` 的含义就**悄悄改变**，容易出错。

2. **意外多条件**：如果两表有**多个同名列**（比如 `id`、`year` 都同名），自然连接会**同时用这两列匹配**，可能导致结果变少或为空。

3. **可读性差**：查看 SQL 时，很难一眼看出到底用哪几列做了连接。



> 因此在实际项目中，**不太推荐使用 `NATURAL JOIN`**。更安全的做法是 `JOIN ... ON ...` 或 `JOIN ... USING (...)`，把连接列**写清楚**。



## 一个小例子帮助记忆



* `students(id, name)`

* `takes(id, course_id)`



三种写法都能得到“学生姓名与其课程 ID”：



```sql

-- 旧式：逗号 + WHERE

SELECT name, course_id

FROM students, takes

WHERE students.id = takes.id;



-- NATURAL JOIN（自动用同名 id）

SELECT name, course_id

FROM students NATURAL JOIN takes;



-- 推荐：显式 USING / ON

SELECT s.name, t.course_id

FROM students s

JOIN takes t USING (id);

-- 或

SELECT s.name, t.course_id

FROM students s

JOIN takes t ON s.id = t.id;

```



## 结论（怎么用）



* **学习/作业**：知道 `NATURAL JOIN` 的语义与等价写法即可。

* **实战/面试**：优先使用 **`JOIN ... ON ...`** 或 **`JOIN ... USING (...)`**，明确列名，避免隐式陷阱。

* **检查点**：当结果“突然变少”或“全空”时，留意是否被多余的同名列影响了连接条件。


---

## 第 7 页

![第 7 页](Lec2-Mid-SQL (1)_assets/page-007.png)

**提问：** 什么意思 详细解释

这页是“**Natural Join in SQL（续）**”，讲的是：

在 **FROM 子句** 里可以把**多张表**用 `NATURAL JOIN` **链式地**连在一起。



---



## 幻灯片公式化写法



```sql

SELECT A1, A2, ... An

FROM   r1 NATURAL JOIN r2 NATURAL JOIN ... NATURAL JOIN rn

WHERE  P;

```



含义：从 `r1`、`r2`、…、`rn` 这些表中，**凡是同名列相等的行**都会被配对连接；同名列在结果里**只保留一份**；再用 `WHERE P` 做筛选。



---



## 关键点与注意事项



1. **每一步都是“按同名列等值连接”**



   * `r1 NATURAL JOIN r2` 会找出两表所有**同名列**组成连接条件；

   * 结果再和 `r3` 做 `NATURAL JOIN`，继续按**结果集与 r3 的同名列**匹配。



2. **连接顺序对语义可能有影响**

   因为每一步都会**产生或消失列**（同名列只保留一份），后续与下一张表的“同名列集合”可能不同；所以虽然 `JOIN` 在等值条件下常可交换/结合，但 **`NATURAL JOIN` 链式使用时要小心**：列名的变化会让条件集合发生变化，进而影响结果。



3. **易踩坑：出现多个同名列**

   如果三表都有 `id`、`year` 等同名列，`NATURAL JOIN` 会**同时**用这些列做匹配，导致结果被“过度收紧”（匹配条件比你预期更多）。



4. **可读性与可维护性较差**

   只看 SQL 很难知道到底用了**哪些列**在连；一旦某个表**新增/改名**了同名列，语义会**悄悄改变**。



---



## 推荐做法（更安全、可控）



* 用 **`JOIN ... USING (...)`** 明确指定同名列：



  ```sql

  SELECT ...

  FROM r1

  JOIN r2 USING (student_id)       -- 只用 student_id

  JOIN r3 USING (student_id);      -- 继续只用 student_id

  ```

* 或者完全显式 **`JOIN ... ON ...`**（即使列名不同也清晰）：



  ```sql

  SELECT ...

  FROM r1

  JOIN r2 ON r1.student_id = r2.sid

  JOIN r3 ON r2.sid        = r3.stu_id;

  ```



---



## 小例子（对比 `NATURAL JOIN` 与显式写法）



表结构（都有同名 `id` 列，`r3` 还多了同名 `year`）：



* `students(id, name, year)`

* `takes(id, course_id)`

* `scores(id, course_id, year, score)`



### 用 `NATURAL JOIN`



```sql

SELECT name, course_id, score

FROM   students

NATURAL JOIN takes

NATURAL JOIN scores;

```



这会**自动**用所有同名列做匹配：



* 第一步（students ↔ takes）：按 `id`；

* 第二步（结果 ↔ scores）：按 `id` **和** `course_id` **和** `year`（因为结果里还带有 `year`，而 `scores` 也有 `year`）。

  如果你原本只想按 `id` + `course_id` 连，结果就会被 `year` **额外限制**。



### 更可控写法



```sql

SELECT s.name, t.course_id, sc.score

FROM students s

JOIN takes   t  ON s.id = t.id

JOIN scores  sc ON t.id = sc.id AND t.course_id = sc.course_id;  -- 明确列出

-- 如果需要按年限制，再额外加 AND s.year = sc.year

```



---



## 结论



* 这页想表达：**FROM 子句中可以连续使用 `NATURAL JOIN` 连接多表**。

* 但在实战/作业中，为了**稳定与可读**，强烈建议用 `USING(...)` 或 `ON ...` **明确写出连接列**，减少隐式同名列带来的意外。

* 一旦结果“突然很少/为空”，要检查是否被 `NATURAL JOIN` **多匹配了额外同名列**。


---

## 第 8 页

![第 8 页](Lec2-Mid-SQL (1)_assets/page-008.png)

**提问：** 什么意思 详细解释

这是一个示例数据表，名字可以理解为 **`student`（学生关系/表）**。图里展示的是**关系的一次实例**：多行记录（元组）+ 多个字段（属性）。



## 表结构含义



* **ID**：学号/主键（唯一标识每位学生）。

* **name**：学生姓名。

* **dept\_name**：所在院系（如 *Comp. Sci.*、*Physics*、*Elec. Eng.* 等）。通常会是到院系表 `department(dept_name, …)` 的**外键**。

* **tot\_cred**：学生已修读并通过的**总学分**（整数）。



> 主键约束：同一个 `ID` 只能出现一次；

> 典型完整性约束：`tot_cred >= 0`；`dept_name` 必须出现在 `department` 表中。



## 读表的方法



* 每一行 = 一位学生；例如：



  * `ID=00128, name=Zhang, dept_name=Comp. Sci., tot_cred=102`

  * `ID=70557, name=Snow, dept_name=Physics, tot_cred=0`



## 可能的典型查询（举例）



* 选出计算机学院学生的姓名与学分



  ```sql

  SELECT name, tot_cred

  FROM student

  WHERE dept_name = 'Comp. Sci.';

  ```

* 学分 ≥ 100 的学生



  ```sql

  SELECT id, name

  FROM student

  WHERE tot_cred >= 100;

  ```

* 按学院统计平均学分



  ```sql

  SELECT dept_name, AVG(tot_cred) AS avg_cred

  FROM student

  GROUP BY dept_name;

  ```

* 与 `department` 表连接（若存在）取院系楼名



  ```sql

  SELECT s.name, s.dept_name, d.building

  FROM student s

  JOIN department d ON s.dept_name = d.dept_name;

  ```



## 在课程中的作用



这张表通常用来配合其它表（如 `course`、`takes`、`instructor`）讲解 **JOIN/分组/约束** 等概念；你会看到以 `ID` 或 `dept_name` 为连接键与其他表进行查询。


---

## 第 9 页

![第 9 页](Lec2-Mid-SQL (1)_assets/page-009.png)

**提问：** 什么意思 详细解释

这是示例表 **`takes`（选课记录）**。每一行代表“某个学生在某学期选了某门课的某个班，并得到一个成绩”。



## 字段含义



* **ID**：学生学号（对应 `student.id`）。

* **course\_id**：课程编号（对应 `course.course_id`，如 *CS-101*）。

* **sec\_id**：**班号/节次**，同一课程在同一学期可能开多个班，用它区分（如 1 班、2 班）。

* **semester**：学期（Fall/Spring/Summer）。

* **year**：年份。

* **grade**：成绩（A、A-、B+ …），有的行为 `null` 表示**尚未出分/退课无成绩**等。



## 典型键与约束（根据教材/经典模式）



* **主键（复合主键）**：`(ID, course_id, sec_id, semester, year)`



  * 含义：同一学生在同一学年学期、同一门课的同一**班**只会出现一次。

* **外键**：



  * `ID → student(ID)`

  * `(course_id, sec_id, semester, year) → section(course_id, sec_id, semester, year)`

    （有时也会建 `course(course_id)` 的外键）

* **grade** 可能允许 `NULL`；具体取值通常受检查约束（如只能在 {A, A-, B+, …, F} 或 NULL）。



## 如何与其他表配合



* 和 **`student`** 通过 `ID` 连接，得到学生姓名、院系等。

* 和 **`section`** 通过 `(course_id, sec_id, semester, year)` 连接，得到上课教室、时间、授课教师编号等。

* 再与 **`instructor`**、**`course`** 连接可拿到教师姓名、课程名称与学分。



## 从图中能读到的几行示例



* `00128, CS-101, 1, Fall, 2017, A`：学号 00128 的学生在 2017 秋季上了 CS-101 的 1 班，成绩 A。

* `45678, CS-101, 1, Fall, 2017, F`：该生 2017 秋 CS-101 1 班成绩 F。

* `98988, BIO-301, 1, Summer, 2018, null`：2018 夏 BIO-301 1 班，**成绩未定/缺失**。



## 常见查询示例



* 某学生所有课程与成绩



  ```sql

  SELECT t.course_id, t.semester, t.year, t.grade

  FROM takes t

  WHERE t.id = '00128'

  ORDER BY t.year, t.semester, t.course_id;

  ```

* 2018 年春季 CS-319 的选课学生名单与成绩



  ```sql

  SELECT s.id, s.name, t.grade

  FROM takes t

  JOIN student s ON s.id = t.id

  WHERE t.course_id = 'CS-319' AND t.sec_id = 2

    AND t.semester = 'Spring' AND t.year = 2018;

  ```

* 统计每门课本学期的通过率（不含 NULL，F 为不通过）



  ```sql

  SELECT course_id,

         AVG(CASE WHEN grade NOT IN ('F') THEN 1.0 ELSE 0 END) AS pass_rate

  FROM takes

  WHERE semester = 'Fall' AND year = 2017 AND grade IS NOT NULL

  GROUP BY course_id;

  ```



> 小结：`takes` 是“学生—班级（课程开课实例）—成绩”的关系表，连接其他表即可回答“谁在哪个学期学了哪门课、在哪个班、成绩是什么”等问题。


---

## 第 10 页

![第 10 页](Lec2-Mid-SQL (1)_assets/page-010.png)

**提问：** 什么意思 详细解释

这页展示的是把两张表 **`student`** 与 **`takes`** 做

**`NATURAL JOIN`（自然连接）** 后得到的结果示例。



## 在这里发生了什么？



* `student` 与 `takes` 的**同名列只有 `ID`**，因此



  ```sql

  FROM student NATURAL JOIN takes

  ```



  等价于



  ```sql

  FROM student JOIN takes USING (ID)

  ```



  ——按 `ID` 相等来配对两表的行，并且在结果里**只保留一份 `ID` 列**。



* 结果表的列由两部分组成：



  * 来自 **student**：`ID, name, dept_name, tot_cred`

  * 来自 **takes**：`course_id, sec_id, semester, year, grade`



* 每个学生会出现**多行**：学生选了几门课，就有几条记录（每条对应一门课/一个班级/一个学期）。



* 这是**内连接**的语义：**只有**在 `takes` 里有选课记录的学生才会出现在结果中；没有选课记录的学生不会出现（若想保留，可用 `LEFT JOIN`）。



## 如何读这张表



以前几行为例：



* `00128  Zhang  Comp. Sci.  102  CS-101  1  Fall 2017  A`

  → 学号 00128 的 Zhang（计科，已修 102 学分）在 2017 秋上了 CS-101 1 班，成绩 A。

* `45678  Levy  Physics  46  CS-101  1  Fall 2017  F`

  → Levy 在 2017 秋 CS-101 1 班不及格（F）。

* `98988  Tanaka Biology 120 BIO-301 1 Summer 2018 NULL`

  → Tanaka 2018 夏 BIO-301 1 班**成绩未出/缺失**（NULL）。



## 小结与提示



* `NATURAL JOIN` 省事，但**隐式按所有同名列连接**；本例只有 `ID`，所以安全。若两表还有别的同名列（如 `year`），就会**同时**用作匹配条件，可能意外缩小结果集。

* 实战更推荐写清楚：



  ```sql

  SELECT s.id, s.name, s.dept_name, s.tot_cred,

         t.course_id, t.sec_id, t.semester, t.year, t.grade

  FROM student AS s

  JOIN takes  AS t USING (id);        -- 或 ON s.id = t.id

  ```



需要的话，我可以把“LEFT/RIGHT/FULL JOIN”在这两张表上的结果差异也做成对照给你看。


---

## 第 11 页

![第 11 页](Lec2-Mid-SQL (1)_assets/page-011.png)

**提问：** 什么意思 详细解释

这页在说明 **Natural Join（自然连接）有“隐式连错列”的风险**，因为它会把**所有同名列**都当成连接条件。

一旦出现**同名但语义并不该相等**的列，就会把本来应该匹配的行给“过滤掉”。



---



## 例子在说什么？



目标：**列出学生姓名与他们所修课程的标题**。



相关表（典型教材结构）：



* `student(id, name, dept_name, …)`

* `takes(id, course_id, sec_id, semester, year, grade)`

* `course(course_id, title, dept_name, …)`



注意：`student` 和 `course` 都有 **`dept_name`** 同名列，但它们**不一定相等**（学生可以跨院系选课）。



### ✅ 正确写法（显式只按 `course_id` 连接 `course`）



```sql

SELECT name, title

FROM student NATURAL JOIN takes, course

WHERE takes.course_id = course.course_id;

```



解释：



* `student NATURAL JOIN takes` 只会用 **`id`** 连接（因为两表同名列是 `id`）。

* 再和 `course` **用 `course_id` 显式连接**。此时**不会**把 `dept_name` 当作条件，因此**跨院系选课**也能被正确返回。



### ❌ 错误写法（完全用 NATURAL JOIN 链接三表）



```sql

SELECT name, title

FROM student NATURAL JOIN takes NATURAL JOIN course;

```



问题：



* 第二步与 `course` 自然连接时，结果集里和 `course` 都有 **`course_id` 与 `dept_name`** 两个同名列，

  NATURAL JOIN 会**同时**用它们当连接条件。

* 于是只保留“**学生所在院系** 与 **课程院系** **相同**”的记录，**跨院系选课的记录全被过滤掉**。

* 这就是“同名但无关的属性被错误地相等化”的典型坑。



---



## 更安全的推荐写法



明确写出要用哪些列连接，避免隐式同名列参与：



```sql

SELECT s.name, c.title

FROM student s

JOIN takes  t ON s.id = t.id

JOIN course c ON t.course_id = c.course_id;  -- 只按 course_id 连接

```



或：



```sql

FROM student s

JOIN takes  t USING (id)

JOIN course c ON t.course_id = c.course_id

```



---



> 你其实已经抓住了问题的核心，只是还差最后一步“**看到结果**”，所以觉得“没懂”。  
> 下面把“为什么跨院系选课会被过滤掉”用一步一步**看得见的方式**展开，你就能亲眼看到记录是怎么丢的。
>
> ------------------------------------------------
> 1. 三张表先各给 1～2 行样本（只看相关列）
>
> student  
> | id   | name  | dept_name |
> | ---- | ----- | --------- |
> | 01   | Zhang | CS        |
>
> takes  
> | id | course_id | dept_name |  
> |--|--|--|  
> | 01 | CS-101  | CS |   ← 本院课  
> | 01 | EE-200  | EE |   ← 外院课（跨院系）  
>
> course  
> | course_id | dept_name | title    |
> | --------- | --------- | -------- |
> | CS-101    | CS        | Database |
> | EE-200    | EE        | Circuits |
>
> ------------------------------------------------
> 2. 先做第一步自然连接（student ⋈ takes）
>
> 自然连接只看**同名列值相等**。  
> 两表同名列是 `(id, dept_name)`，所以连接条件是  
> `student.id = takes.id AND student.dept_name = takes.dept_name`
>
> 结果：  
>
> | id | name | dept_name | course_id |  
> |--|--|--|--|  
> | 01 | Zhang | CS | CS-101 |   ← 本院课保留  
> | 01 | Zhang | CS | EE-200 |   ← 外院课**被丢弃**（因为 student.dept_name=CS ≠ EE）  
>
> **已经丢了跨院系选课！**  
> 但此时你还没注意到，因为还没用到 title。
>
> ------------------------------------------------
> 3. 第二步再做“自然连接 course”
>
> 现在把上一步结果与 course 自然连接。  
> 上一步结果只有一行：  
> | id   | name  | dept_name | course_id |
> | ---- | ----- | --------- | --------- |
> | 01   | Zhang | CS        | CS-101    |
>
> course 表两行：  
> | course_id | dept_name | title    |
> | --------- | --------- | -------- |
> | CS-101    | CS        | Database |
> | EE-200    | EE        | Circuits |
>
> 自然连接的同名列是 `(course_id, dept_name)`，于是  
> `结果.dept_name = course.dept_name AND 结果.course_id = course.course_id`  
>
> 只有 (CS-101, CS) 这一条满足，最终输出  
>
> | name  | title    |
> | ----- | -------- |
> | Zhang | Database |
>
> ------------------------------------------------
> 4. 回头看“跨院系选课”那条 EE-200
>
> 它在第 2 步就被**提前过滤掉了**，根本走不到第 3 步。  
> **过滤的元凶**正是第二步多出来的那个同名但**语义无关**的列 `dept_name`：
>
> - 学生表的 `dept_name` 表示“学生所属院系”  
> - course 表的 `dept_name` 表示“课程开设院系”  
>
> 二者**名字相同，含义不同**，但 NATURAL JOIN 一视同仁地把它们当成连接条件，于是  
> “学生所在院系 ≠ 课程院系” 的记录被全部剔除，也就是**跨院系选课全丢**。
>
> ------------------------------------------------
> 5. 一句话总结
>
> > NATURAL JOIN 看到同名就“强行相等”，  
> > 把“学生院系”与“课程院系”当成同一个东西，  
> > 于是跨院系选课因为“院系不等”被默默扔掉，  
> > 这就是“同名但无关属性被错误相等化”的坑。
>
> 改用显式条件 `takes.course_id = course.course_id` 就能避开这个坑，因为**只拿真正相关的列**当连接条件，其它同名却无关的列不再参与。



* **NATURAL JOIN 会用“所有同名列”作等值连接**，而不仅是你心里想的那一两列。

* 多表链式 **NATURAL JOIN** 特别危险，因为前一次连接会改变“有哪些同名列”。

* 实战与作业中，**优先 `JOIN ... ON ...` 或 `USING(...)`**，把连接列写清楚。


---

## 第 12 页

![第 12 页](Lec2-Mid-SQL (1)_assets/page-012.png)

**提问：** 什么意思 详细解释

这页讲：为避免 **NATURAL JOIN** 把**无关但同名的列**也当作连接条件，改用 **`USING (...)`** 明确指定“只用哪些同名列来等值连接”。



---



## 核心意思



* **问题**：`NATURAL JOIN` 会用**所有**同名列做连接，容易把结果“连少/连错”。

* **解决**：在 `JOIN` 后面写 `USING (列1, 列2, …)`，只用这些列当连接键，其它同名列**不会**参与匹配，也不会被去重误合并。

* **效果**：`USING` 指定的列在结果中**只保留一份**（比 `ON` 更简洁）。



---



## 幻灯片示例解读



```sql

SELECT name, title

FROM   (student NATURAL JOIN takes)

JOIN   course USING (course_id);

```



* `student NATURAL JOIN takes`：两表唯一同名列为 `id`，所以此处按 `id` 连接是安全的。

* 再与 `course` 连接时，**明确**用 `course_id`，避免把 `dept_name`（student、course 也同名）也拉来做条件。

* 因此可以正确得到“学生姓名 + 课程标题”，包含跨院系选课的记录。



---



## 与 `ON` 的对比



两者语义等价，`USING` 只是更简洁，且会把使用的列合并为一列：



```sql

-- 等价写法（更通用，列名可不同）

SELECT s.name, c.title

FROM   student s

JOIN   takes   t ON s.id = t.id

JOIN   course  c ON t.course_id = c.course_id;

```



* `ON`：不会自动合并列名；`t.course_id` 和 `c.course_id` 都存在（除非你不选出）。

* `USING(course_id)`：结果集中只有一列 `course_id`。



---



## 常用用法与注意点



1. **可指定多个列**



```sql

JOIN section USING (course_id, sec_id, semester, year)

```



2. **列名必须在两表中都存在**（否则 `USING` 不成立）。

3. **结果列顺序**：`USING` 中的列先于其它列（不同数据库细节略有差异）。

4. **可读性**：`USING` 清晰表达“我只按这些键连”，比 `NATURAL JOIN` 安全、比 `ON` 简短。

5. **跨库兼容**：PostgreSQL、MySQL、SQLite 支持 `USING`；SQL Server 没有 `USING`，需用 `ON`。



---



## 小结



* **不要链式 `NATURAL JOIN`**（容易被额外同名列“夹带私货”）。

* **推荐**：`JOIN ... USING (明确的键)` 或 `JOIN ... ON ...`。

* 记忆法：**USING = 指定连接键 + 合并键列**，既安全又简洁。


---

## 第 13 页

![第 13 页](Lec2-Mid-SQL (1)_assets/page-013.png)

**提问：** 什么意思 详细解释

> ⚠️ 未能复制为 Markdown，以下为纯文本回退：

这页总结了 **“连接（JOIN）的类型与条件”** 两个维度，说明：  
“怎么连” 与 “按什么条件连” 是两件**相互独立**的事。

---

## 1️⃣ Join Operation 是什么

**Join operation**：把两张表作为输入，返回一张新表。  
常放在 `FROM` 子句里，供后续的筛选、分组等操作使用。

---

## 2️⃣ Join Condition（连接条件）—— 用什么规则匹配行

连接条件决定两表“**哪些行算匹配**”。

三种写法（选其一）：

- **`NATURAL`**  
  自动用两表所有**同名列**做等值匹配，并在结果中只保留一份同名列。  
  ⚠️ **风险**：可能误把无关的同名列当作连接条件。

- **`ON <predicate>`**  
  显式写出布尔条件（最通用）。  
  例：`ON s.id = t.id AND t.year = 2018`

- **`USING (A1, A2, …, An)`**  
  只用括号里的**同名列**匹配，并在结果中把这些列**合并为一列**。  
  ✅ 可读、简洁。

---

## 3️⃣ Join Type（连接类型）—— 对“不匹配的行”如何处理

- **`INNER JOIN`**：只保留两边都匹配的行（交集）。  
- **`LEFT OUTER JOIN`**：保留左表全部行；右侧未匹配的列用 `NULL` 填充。  
- **`RIGHT OUTER JOIN`**：保留右表全部行；左侧未匹配的列用 `NULL` 填充。  
- **`FULL OUTER JOIN`**：左右两边都保留（并集），未匹配的一侧以 `NULL` 补齐。  
  （部分数据库不支持，可用 `UNION` 变通实现。）

---

## ✳️ 关键总结

- “**类型（Type）**” 决定是否保留未匹配行。  
- “**条件（Condition）**” 决定哪些行算匹配。  
- 两者可以**自由组合**使用。

---

## 组合示例

```sql
student INNER JOIN takes USING (id)
student LEFT JOIN  takes ON student.id = takes.id
-- （谨慎）student NATURAL JOIN takes
```

------

## 小例子对照

### INNER + USING

```sql
SELECT s.name, t.course_id
FROM student s
JOIN takes t USING (id);
-- 只返回选过课的学生
```

### LEFT + ON

```sql
SELECT s.name, t.course_id
FROM student s
LEFT JOIN takes t ON s.id = t.id;
-- 所有学生都保留；没选课的 course_id 为 NULL
```

------

## ⚠️ 避免 NATURAL 的坑

当两表中存在**同名但无关的列**时，`NATURAL JOIN` 会误把它们当条件。
 👉 建议使用 `USING` 或 `ON` 明确指定连接键。

------

## 🧭 思维导图式理解

| 维度                       | 作用             | 示例                        |
| -------------------------- | ---------------- | --------------------------- |
| **Join Type（类型）**      | 是否保留未匹配行 | INNER / LEFT / RIGHT / FULL |
| **Join Condition（条件）** | 规定哪些行匹配   | ON / USING / NATURAL        |

因此，可以先决定“保不保留未匹配行”，再决定“用什么规则匹配”。

------

```

```


---

## 第 14 页

![第 14 页](Lec2-Mid-SQL (1)_assets/page-014.png)

**提问：** 什么意思 详细解释

> ⚠️ 未能复制为 Markdown，以下为纯文本回退：

这页解释 **JOIN 的条件（Join Condition）** —— 用 **ON** 指定两表如何匹配。

---

## 关键点

**ON 条件**：在 `JOIN` 后写一个布尔表达式，描述两表行何时算“匹配”。  
写法与 `WHERE` 很像，只是放在 `JOIN` 之后，用关键字 `ON`。

---

## 示例

```sql
SELECT *
FROM student
JOIN takes ON student.id = takes.id;
```

**含义**：当 `student.id` 等于 `takes.id` 时，两表的那两行配对，出现在结果里。

------

### 等价的旧式写法（不推荐）

```sql
SELECT *
FROM student, takes
WHERE student.id = takes.id;
```

这是“**逗号连接 + WHERE 条件**”，和
 `INNER JOIN ... ON ...` 语义相同，但可读性差、容易漏条件。

------

## 进阶补充

### 多条件连接

`ON` 可以写多个条件，例如连接课程表的四元组键：

```sql
... JOIN section s
     ON  t.course_id = s.course_id
     AND t.sec_id    = s.sec_id
     AND t.semester  = s.semester
     AND t.year      = s.year;
```

------

### 外连接注意事项

外连接时，`ON` 与 `WHERE` 的位置会影响结果：

- **过滤写在 ON 里**：影响“是否匹配”。
- **过滤写在 WHERE 里**：是在连接后再筛选，可能把外连接补出的 `NULL` 行也过滤掉，从而把 `LEFT/RIGHT JOIN` 变相变回 `INNER JOIN`。

------

## 实战建议

- 优先使用

  ```sql
  JOIN ... ON ...
  ```

  或

  ```sql
  JOIN ... USING(...)
  ```

  明确连接键。

- 避免逗号连接。

- 把“**用于匹配的条件**”写在 `ON`；
   把“**匹配后还要筛的条件**”写在 `WHERE`。

```

```


---

## 第 15 页

![第 15 页](Lec2-Mid-SQL (1)_assets/page-015.png)

**提问：** 什么意思 详细解释

> ⚠️ 未能复制为 Markdown，以下为纯文本回退：

这页是前一页 **Join Condition（连接条件）** 的继续说明，核心还是：用 **ON** 明确写出两表的匹配规则。

---

## 关键点

**ON 条件**：在 `JOIN` 后写一个布尔表达式，决定两表的哪些行“匹配”。  
写法形式和 `WHERE` 的谓词很像，只是关键字改为 `ON`，位置在 `JOIN` 后面。

---

## 示例

```sql
SELECT *
FROM student
JOIN takes ON student_ID = takes_ID;
```

**含义**：当 `student_ID` 与 `takes_ID` 相等时，将两行配对输出。

------

### 等价的旧式写法（不推荐）

```sql
SELECT *
FROM student, takes
WHERE student_ID = takes_ID;
```

与 `INNER JOIN ... ON ...` 语义相同，但可读性差、易漏写连接条件。

------

## 实战提示

- `ON` 可写多个条件（比如课程四元组：`course_id/sec_id/semester/year`）。
- **外连接注意：**
  - 放在 `ON` 里的条件影响“是否匹配”；
  - 放在 `WHERE` 里的条件是连接后再过滤，可能把 `LEFT/RIGHT JOIN` 补出来的 `NULL` 行也筛掉，等于把外连接变成内连接。

------

## 结论

优先使用

```sql
JOIN ... ON ...
```

（或 `USING(...)`）明确连接键；
 少用逗号连接。

```

```


---

## 第 16 页

![第 16 页](Lec2-Mid-SQL (1)_assets/page-016.png)

**提问：** 什么意思 详细解释

> ⚠️ 未能复制为 Markdown，以下为纯文本回退：

这页在讲 **Outer Join（外连接）**：  
它是在普通连接（内连接）的基础上做了**“不丢信息”**的扩展——  
先按连接条件做匹配，再把某一侧没有匹配到的行也保留下来，  
把另一侧的列用 `NULL` 补齐。

---

## 🌐 外连接的三种形式

### **1️⃣ LEFT OUTER JOIN（左外连接）**
- 保留左表的所有行；
- 右表匹配不到时，右表列填 `NULL`。

### **2️⃣ RIGHT OUTER JOIN（右外连接）**
- 保留右表的所有行；
- 左表匹配不到时，左表列填 `NULL`。  
💡 实际中很多人直接通过**交换表顺序**用 `LEFT JOIN` 代替。

### **3️⃣ FULL OUTER JOIN（全外连接）**
- 左右两表的并集都保留：  
  - 匹配成功的部分按内连接输出；  
  - 未匹配的一侧用 `NULL` 填充。  
⚠️ **提示**：部分数据库（如 MySQL）不支持 `FULL OUTER JOIN`，  
通常用 `LEFT JOIN … UNION … RIGHT JOIN` 模拟。

---

## 🔍 与内连接的区别

| 类型           | 保留行                     | 未匹配行处理           |
| -------------- | -------------------------- | ---------------------- |
| **INNER JOIN** | 仅匹配成功的行（交集）     | 未匹配的行被丢弃       |
| **OUTER JOIN** | 保留未匹配的一侧（或两侧） | 未匹配侧用 `NULL` 占位 |

---

## 🧩 语法示例（以学生与选课为例）

```sql
-- 左外：所有学生都保留；没选课的学生，课程信息为 NULL
SELECT s.id, s.name, t.course_id
FROM student s
LEFT JOIN takes t ON s.id = t.id;

-- 右外：所有选课记录都保留；若学生表缺失对应 id，学生信息为 NULL
SELECT s.id, s.name, t.course_id
FROM student s
RIGHT JOIN takes t ON s.id = t.id;

-- 全外：两边都保留（某些库不支持）
SELECT COALESCE(s.id, t.id) AS id, s.name, t.course_id
FROM student s
FULL OUTER JOIN takes t ON s.id = t.id;
```

------

## 💼 常见场景

- **统计“有 / 无”类问题**：
   例如“所有学生及其是否选课”“所有课程及其是否被选”。
- **对账 / 找孤儿记录**：
   通过 `WHERE … IS NULL` 找出未匹配的一侧，用于定位异常数据。

------

## ⚠️ 重要坑点

**把条件放在 `WHERE` 会“吃掉”外连接的 NULL！**

```sql
-- ❌ 错误写法：WHERE 过滤掉 NULL，把 LEFT JOIN 变成 INNER JOIN
WHERE t.course_id = 'CS-101'
```

### ✅ 正确做法

- **方案 1：** 将条件写在 `ON` 中，保持外连接行为：

  ```sql
  FROM student s
  LEFT JOIN takes t ON s.id = t.id AND t.course_id = 'CS-101';
  ```

- **方案 2：** 在 `WHERE` 中显式允许 `NULL`：

  ```sql
  WHERE (t.course_id = 'CS-101' OR t.course_id IS NULL);
  ```

------

## 🧭 选择建议

| 目标           | 建议使用                          |
| -------------- | --------------------------------- |
| 只要交集       | `INNER JOIN`                      |
| 以左表为主兜底 | `LEFT JOIN`                       |
| 以右表为主兜底 | `RIGHT JOIN`（或调换顺序用 LEFT） |
| 两边都兜底     | `FULL OUTER JOIN`（注意兼容性）   |

------

## 🧠 一句话记忆

> **外连接 = 内连接结果 + 未匹配行（用 NULL 补齐）**

```

```


---

## 第 17 页

![第 17 页](Lec2-Mid-SQL (1)_assets/page-017.png)

**提问：** 什么意思 详细解释

> ⚠️ 未能复制为 Markdown，以下为纯文本回退：

这页用两个小表说明 **为什么要用外连接（Outer Join）**。

---

## 📘 两张表的含义

### **course（课程表）**
| course_id | title       | dept_name  | credits |
| --------- | ----------- | ---------- | ------- |
| BIO-301   | Genetics    | Biology    | 4       |
| CS-190    | Game Design | Comp. Sci. | 4       |
| CS-315    | Robotics    | Comp. Sci. | 3       |

### **prereq（先修课关系表）**
| course_id | prereq_id |
| --------- | --------- |
| BIO-301   | BIO-101   |
| CS-190    | CS-101    |
| CS-347    | CS-101    |

> 提示：“**course information is missing CS-347**”  
> 表示 `prereq` 中出现了 `CS-347`，但 `course` 表中没有对应课程信息。  
> 这是一种“左有右无 / 右有左无”的**不对称数据**场景。

---

## ❓ 为什么需要外连接

### 🔸 如果使用内连接（INNER JOIN）

```sql
SELECT c.course_id, c.title, p.prereq_id
FROM course c
JOIN prereq p ON c.course_id = p.course_id;
```

只会输出两表中**都有匹配的行**。
 结果中不会出现 `CS-347`，因为它在 `course` 中缺失。
 ➡️ **信息丢失：右表多出的行被舍弃。**

------

## ✅ 用外连接保留“缺失一侧”的行

### **1️⃣ RIGHT OUTER JOIN**（以 `prereq` 为主：保留所有先修关系）

```sql
SELECT c.course_id, c.title, p.prereq_id
FROM course c
RIGHT JOIN prereq p ON c.course_id = p.course_id;
```

输出示例：

| course_id | title       | prereq_id |
| --------- | ----------- | --------- |
| BIO-301   | Genetics    | BIO-101   |
| CS-190    | Game Design | CS-101    |
| NULL      | NULL        | CS-101    |

最后一行对应 `CS-347`，`course` 一侧缺失，用 `NULL` 补齐。

------

### **2️⃣ LEFT OUTER JOIN**（以 `course` 为主：找“有课但无先修”的课程）

```sql
SELECT c.course_id, c.title, p.prereq_id
FROM course c
LEFT JOIN prereq p ON c.course_id = p.course_id;
```

结果包含所有 `course` 中的课程：
 若某课程没有先修课，则 `prereq_id` 为 `NULL`。

示例：

| course_id | title       | prereq_id |
| --------- | ----------- | --------- |
| BIO-301   | Genetics    | BIO-101   |
| CS-190    | Game Design | CS-101    |
| CS-315    | Robotics    | NULL      |

------

### **3️⃣ FULL OUTER JOIN**（两边都保留）

```sql
SELECT COALESCE(c.course_id, p.course_id) AS course_id,
       c.title, p.prereq_id
FROM course c
FULL OUTER JOIN prereq p ON c.course_id = p.course_id;
```

输出既包含 `course` 独有行，也包含 `prereq` 独有行（如 `CS-347`），
 缺的一侧用 `NULL` 填充。

⚠️ **注意**：MySQL 不支持 `FULL OUTER JOIN`，可用
 `LEFT JOIN … UNION … RIGHT JOIN` 模拟。

------

## 🧮 典型用途

### 1️⃣ 数据核对 / 找“孤儿记录”

找出 `prereq` 中在 `course` 里**不存在**的课程：

```sql
SELECT p.course_id
FROM prereq p
LEFT JOIN course c ON c.course_id = p.course_id
WHERE c.course_id IS NULL;   -- 返回 CS-347
```

### 2️⃣ 全量报表

当需要“**有 / 无 都显示**”的列表时，用外连接避免丢行。
 例如：列出所有课程及其先修情况。

------

## 🧠 一句话总结

> 当两表存在“只在一边出现的键”（如 `CS-347`）时，
>  **外连接能保留这些记录并用 `NULL` 填另一侧**，
>  从而避免信息丢失。

```

```


---

## 第 18 页

![第 18 页](Lec2-Mid-SQL (1)_assets/page-018.png)

**提问：** 什么意思 详细解释

这页演示 **左外连接（LEFT OUTER JOIN）** 的效果，语句是：



```

course NATURAL LEFT OUTER JOIN prereq

```



## 这条语句在做什么？



* **NATURAL**：按两表的**同名列**做等值连接。`course` 和 `prereq` 的同名列只有 **`course_id`**，所以连接键就是 `course_id`（在结果里只保留一份）。

* **LEFT OUTER JOIN**：以**左表 `course`** 为主。

  先做连接，然后把 `course` 中**没有在 `prereq` 找到匹配**的课程也保留下来，右边（`prereq`）缺的列用 **`NULL`** 补齐。



## 为什么结果是这三行？



表 `course` 有：`BIO-301`、`CS-190`、`CS-315`

表 `prereq` 有：`BIO-301→BIO-101`，`CS-190→CS-101`，以及\*\*`CS-347→CS-101`\*\*（注意这门在 `course` 里不存在）



左外连接以 `course` 为主：



* `BIO-301` 匹配到 → `prereq_id = BIO-101`

* `CS-190` 匹配到 → `prereq_id = CS-101`

* `CS-315` **没有先修关系** → `prereq_id = NULL`

* `CS-347` **只在右表**，左外连接不会显示（如果要保留它，需要右外或全外连接）



## 等价、更安全的写法



```sql

-- 推荐显式指定键

SELECT c.course_id, c.title, c.dept_name, c.credits, p.prereq_id

FROM course c

LEFT JOIN prereq p USING (course_id);          -- 或：ON c.course_id = p.course_id

```



## 要点



* 左外：**保留左表所有行**，右表不匹配 → **NULL**。

* 本例用 `NATURAL` 是安全的（唯一同名列是 `course_id`）；一般更建议用 `USING/ON` 明确连接列，避免隐式同名列带来的风险。


---

## 第 19 页

![第 19 页](Lec2-Mid-SQL (1)_assets/page-019.png)

**提问：** 什么意思 详细解释

这页演示 **右外连接（RIGHT OUTER JOIN）** 的效果，语句是：



```

course NATURAL RIGHT OUTER JOIN prereq

```



## 在这里发生了什么？



* **NATURAL**：按两表的**同名列**连接。`course` 和 `prereq` 的同名列只有 **`course_id`**，所以连接键是 `course_id`（并且结果里只保留一份 `course_id`）。

* **RIGHT OUTER JOIN**：以**右表 `prereq`** 为主。

  先做连接，然后把 `prereq` 中**没有在 `course` 找到匹配**的行也**保留下来**，左边（`course`）缺失的列用 **`NULL`** 补齐。



## 为什么结果长这样？



`prereq` 有三行：`BIO-301→BIO-101`、`CS-190→CS-101`、`CS-347→CS-101`；

`course` 只有 `BIO-301`、`CS-190`、`CS-315`，**没有 `CS-347`**。



右外连接以 `prereq` 为主：



* `BIO-301`、`CS-190`：在 `course` 有记录 → 显示课程信息与先修课。

* **`CS-347`**：`course` 中不存在 → 课程信息列（`title/dept_name/credits`）为 **`NULL`**，但\*\*`prereq_id=CS-101`\*\* 仍保留。



所以表格第三行是：`course_id=CS-347, title=NULL, dept_name=NULL, credits=NULL, prereq_id=CS-101`。



## 等价、更安全的写法



```sql

-- 右外（部分数据库支持）

SELECT c.course_id, c.title, c.dept_name, c.credits, p.prereq_id

FROM course c

RIGHT JOIN prereq p USING (course_id);  -- 或 ON c.course_id = p.course_id



-- 若数据库不常用 RIGHT，可调换顺序用 LEFT：

SELECT c.course_id, c.title, c.dept_name, c.credits, p.prereq_id

FROM prereq p

LEFT JOIN course c ON c.course_id = p.course_id;

```



## 要点回顾



* **右外连接**：右表全保留；左表不匹配 → **`NULL`**。

* 本例用 `NATURAL` 是安全的（唯一同名列就是 `course_id`），但实际开发更推荐 **`USING`/`ON`** 明确指定连接列，避免隐式同名列带来的意外。


---

## 第 20 页

![第 20 页](Lec2-Mid-SQL (1)_assets/page-020.png)

**提问：** 什么意思 详细解释

这页演示 **全外连接（FULL OUTER JOIN）**，语句是：



```

course NATURAL FULL OUTER JOIN prereq

```



## 在这里发生了什么？



* **NATURAL**：按两表**同名列**连接。`course` 和 `prereq` 的同名列只有 `course_id`，因此连接键是 `course_id`（结果中 `course_id` 只保留一份）。

* **FULL OUTER JOIN**：**左右两表都保留**。

  先做匹配；能配上的输出“合并行”，**配不上的**也要输出，另一侧的列用 `NULL` 填充。



## 结果为何是这四行？



数据回顾：



* `course`：`BIO-301`、`CS-190`、`CS-315`（没有 `CS-347`）

* `prereq`：`BIO-301→BIO-101`、`CS-190→CS-101`、`CS-347→CS-101`



连接后：



* `BIO-301`、`CS-190`：两表都存在 → 正常合并，`prereq_id` 分别为 `BIO-101`、`CS-101`。

* `CS-315`：只在 `course` 有 → `prereq_id = NULL`。

* `CS-347`：只在 `prereq` 有 → 课程信息列（`title/dept_name/credits`）均为 `NULL`，`prereq_id = CS-101`。



## 等价写法（更安全/更通用）



```sql

-- 明确指定连接列

SELECT COALESCE(c.course_id, p.course_id) AS course_id,

       c.title, c.dept_name, c.credits, p.prereq_id

FROM course c

FULL OUTER JOIN prereq p ON c.course_id = p.course_id;

```



> **MySQL 不支持 `FULL OUTER JOIN`**，可用 `LEFT JOIN … UNION … RIGHT JOIN` 模拟：



```sql

SELECT c.course_id, c.title, c.dept_name, c.credits, p.prereq_id

FROM course c

LEFT JOIN prereq p ON c.course_id = p.course_id

UNION

SELECT c.course_id, c.title, c.dept_name, c.credits, p.prereq_id

FROM prereq p

RIGHT JOIN course c ON c.course_id = p.course_id;  -- 或把上一句换成：FROM prereq p LEFT JOIN course c ...

```



## 常见注意点



* **过滤位置**：在 `WHERE` 里加条件可能把 `NULL` 行过滤掉，从而把“全外连接”变成“内连接”。

  需要限制一侧时，优先写在 **`ON`** 里，或在 `WHERE` 中显式允许 `NULL`。

* **NATURAL 的风险**：本例只有 `course_id` 同名列较安全；实际更推荐 `USING(course_id)` 或 `ON c.course_id = p.course_id` 明确连接键。



**一句话**：`FULL OUTER JOIN` = **内连接结果** + **左表独有行** + **右表独有行**（独有行的另一侧列用 `NULL` 补齐）。


---

## 第 21 页

![第 21 页](Lec2-Mid-SQL (1)_assets/page-021.png)

**提问：** 什么意思 详细解释

这页讲的是：**同一个查询目标，用不同的 SQL 写法，性能差别可能巨大**——中间结果会“爆炸”，计算量暴涨，但最终答案一样。标题前的 \* 说明这页是提示性质，**不计入考试**。



## 主要信息



* 下面这个（课件中的）极简真实案例展示了：**写法不同 → 中间表大小不同 → 执行时间差很多**。

  提到的文件：`3_compare_join.txt`（里面有对比示例）。

* **大多数情况下 PostgreSQL 会自动优化**（改写连接顺序、下推过滤条件等）。

  但如果你把 **JOIN 条件写得过于复杂**，或把逻辑塞进 **视图 / CTE（WITH）** 里，优化器可能**看不见**可下推的过滤/连接条件，导致 **不能做谓词下推/连接重排**，性能会变差。



## 常见“慢”的写法



* 先把多表**全连接**成大宽表，再在外层 `WHERE` 过滤（中间结果巨大）。

* 在可索引列上套函数/表达式：如 `ON date_trunc('day', a.ts) = date_trunc('day', b.ts)`，阻断索引和下推。

* 复杂视图/CTE 层层包裹，把过滤条件放在最外层，**下推失败**。

* 滥用 `NATURAL JOIN` 导致额外同名列参与连接，结果集变小或连接路径不佳。



## 更高效的写法与原则



1. **尽早过滤**（让选择条件离数据源越近越好）



```sql

-- 差：先连后筛

FROM A JOIN B ON A.k=B.k

WHERE A.dt='2025-10-01';



-- 好：把条件提前到一侧子查询/ON 中

FROM (SELECT * FROM A WHERE dt='2025-10-01') A

JOIN B ON A.k=B.k;

-- 或直接：JOIN B ON A.k=B.k AND A.dt='2025-10-01'

```



2. **只做必要的 JOIN**：能在子查询里先聚合/去重，就先做，避免“乘法放大”。



3. **明确连接键（USING/ON）**，避免 `NATURAL JOIN` 引入多余列做匹配。



4. **避免在可索引列上包函数**

   把 `ON DATE(a.ts)=DATE(b.ts)` 改写为区间：



```sql

ON a.ts >= b.ts::date

AND a.ts <  b.ts::date + INTERVAL '1 day'

```



5. **CTE/视图谨慎使用**



* PostgreSQL 12+ 会对 CTE 做内联，但**不是所有情况**；

* 若发现优化器没有下推过滤，尝试把 CTE 展开到查询里，或把条件写进 `ON` / 子查询内部。



6. **观察执行计划**：`EXPLAIN (ANALYZE, BUFFERS)`

   看是否出现巨大的 Hash/Sort/Materialize、中间行数是否“指数级膨胀”、是否走到合适索引。



> 一句话：**写法影响优化器能看见什么**。让过滤条件“离数据近”、让连接条件**简单可推理**，能显著提升 JOIN 的效率。


---

## 第 22 页

![第 22 页](Lec2-Mid-SQL (1)_assets/page-022.png)

**提问：** 什么意思 详细解释

这页在讲：**数据库如何选择“执行 JOIN 的最优路径（计划）”**，用“下棋的 AI”作比喻。标题前的 \* 表明它是提示性质，不计入考试。



## 类比：像 AI 下棋一样找最优解



1. **Define legal moves：定义合法动作**

   在查询里就是“有哪些可选的执行方式”，例如



   * **连接顺序**：先 `(A ⋈ B)` 再与 `C`，还是先 `(B ⋈ C)` 再与 `A`（搜索空间巨大）。

   * **访问路径**：全表扫、索引范围扫、索引仅扫描等。

   * **连接算法**：嵌套循环（Nested Loop）、哈希连接（Hash Join）、排序合并（Merge Join）等。

   * **物理操作**：是否提前过滤/去重/聚合，是否物化中间结果，是否并行。



2. **Define an evaluation function：定义评估函数（成本模型）**

   优化器用 **Cost Model** 估算每个方案的代价，综合：



   * I/O（读写页数）、CPU（比较/哈希/排序开销）、内存（溢写到磁盘的代价）、网络（分布式场景），

   * **基数估计**（各步的行数/选择率）、数据分布、是否命中索引、是否能用顺序访问等。

     → 成本越低越好。



3. **Search for the best solution：在搜索空间里找最低成本的计划**



   * 经典方法：**Selinger 风格动态规划**（枚举子集、保留每个子集的最优计划）。

   * 变体：左深/右深/丛状（bushy）树枚举、贪心/启发式剪枝、遗传算法、基于规则或基于代价混合。

   * 现代系统还会用 **统计信息**（直方图、NDV、相关性）与 **反馈**（自适应执行）修正估计。



> 图中的棋盘线条，就是在众多可能“走法”（连接顺序/方法）里寻找一条\*\*通向将死（最优）\*\*的路径。



## 为什么同解不同速？



* 连接顺序不同会产生**中间结果大小**巨大差异（可能从几百行到上亿行），导致 I/O/CPU 爆炸；

* 连接算法选择不当（如对大表用 Nested Loop 而不是 Hash Join）；

* 访问路径不佳（错过索引/不能下推过滤）。



## 作为开发者你能做什么（配合优化器）



* **写清楚连接条件**：`JOIN ... ON / USING`，避免 `NATURAL JOIN` 的隐式陷阱。

* **尽早过滤/投影**：把限制条件放到能被下推的位置（`ON` 或子查询内），少用“大表先全连后过滤”。

* **为连接键建索引**；确保统计信息新鲜（`ANALYZE`）。

* 避免在可索引列上包函数（会阻断索引和谓词下推）。

* CTE/视图层层包裹时，注意有些系统**不能内联**导致下推失败；必要时展开写。

* 用 `EXPLAIN (ANALYZE)` 看计划与实际行数，定位基数估计错误和慢点。



**一句话**：优化 JOIN 的过程 = 定义可选方案 → 估成本 → 搜索最低成本计划。写出“优化器看得懂、能下推、能用索引”的 SQL，就更容易走到“最优路径”。


---

## 第 23 页

![第 23 页](Lec2-Mid-SQL (1)_assets/page-023.png)

**提问：** 什么意思 详细解释

这页讲 **视图（View）** —— 把一条 `SELECT` 查询“包装成一张虚拟表”，用来**隐藏不该给某些用户看的数据**，或**简化查询**。



## 关键信息



* **为什么要视图？**

  并非所有用户都应该看到数据库里“完整的逻辑模型/所有表与所有列”。

  例子：有人只需要知道老师的 **编号、姓名、所属院系**，但**不应该看到薪资**。

* **视图能做什么？**

  给特定用户展示**筛选后的列/行**，就像一张表一样可被查询，从而**实现按需可见**。

  幻灯片里的例子等价于一张只含 `ID, name, dept_name` 的“老师表”：



  ```sql

  SELECT ID, name, dept_name

  FROM instructor;

  ```

* **定义**

  “不是概念模型中真实存储的关系，但对用户可见的**虚拟关系**”，称为 **view**。



## 怎么创建与使用（标准写法）



```sql

-- 创建：把查询结果定义为视图

CREATE VIEW v_instructor_public AS

SELECT id, name, dept_name

FROM instructor;



-- 使用：像查表一样

SELECT * FROM v_instructor_public WHERE dept_name = 'Comp. Sci.';

```



## 权限与安全



* 给用户**授权访问视图**而不是底层表：



  ```sql

  GRANT SELECT ON v_instructor_public TO analyst_role;

  ```

* 这样用户看不到被隐藏的列（如 `salary`），也查不到被过滤掉的行（可以在视图里加 `WHERE`）。



## 可更新性（会考）



* **可更新视图**：简单直接映射到底层单表、无聚合/分组/去重/集合运算，通常可 `INSERT/UPDATE/DELETE`。

* **不可更新视图**：包含 `JOIN/AGGREGATE/DISTINCT/WITH ...` 等复杂操作；更新通常被禁止或需要 **INSTEAD OF 触发器**（SQL Server/Oracle）来接管。



## 性能提示



* 普通视图是**逻辑别名**，每次查询都会**重跑其 SELECT**。

* 若性能关键、且数据能容忍“延迟更新”，可用 **物化视图（Materialized View）**：把结果**持久化**并按计划刷新。



## 典型用法



* **列级脱敏/隐藏**：不暴露 `salary`、`phone` 等敏感列。

* **行级限制**：视图里加 `WHERE owner_id = current_user`（或配合行级安全 RLS）。

* **简化复杂查询**：把常用的多表 JOIN/聚合封装成视图，调用更简洁。



**一句话**：**View = 可授权的“查询别名/虚拟表”**。用它按需暴露数据、保护敏感信息，同时让使用者像查表一样简单。


---

## 第 24 页

![第 24 页](Lec2-Mid-SQL (1)_assets/page-024.png)

**提问：** 什么意思 详细解释

这页讲 **视图（View）的定义方式与本质**。



## 1) 基本语法



> **`CREATE VIEW v AS <query expression>`**



* `<query expression>`：任意合法的 SQL 查询（`SELECT …`，也可以包含 join/where/group by 等）。

* `v`：视图名。定义后，`v` 就像一张表一样可在 `FROM` 里被引用。



示例：



```sql

CREATE VIEW v_instructor_public AS

SELECT id, name, dept_name

FROM instructor

WHERE active = TRUE;

```



使用：



```sql

SELECT * FROM v_instructor_public WHERE dept_name = 'Comp. Sci.';

```



## 2) 逻辑本质（很重要）



* **创建视图 ≠ 真的创建并存储一张新表**。

* 视图**保存的是“查询表达式”**（一段 SQL）。当你查询视图时，数据库会把这段表达式**内联/替换**进你的查询再执行（就像“宏展开”或“别名”）。

* 因此，视图默认**不存数据**、每次使用都会重新计算结果（除非是物化视图）。



## 3) 好处



* **隐藏数据**：只暴露需要的列/行（如不暴露 salary）。

* **简化复杂查询**：把常用的多表 JOIN/聚合封装成一个“虚拟表”。

* **权限控制**：给用户授权视图而非底层表。



## 4) 常见延伸



* **更新性**：简单单表直通视图常可更新；含 `JOIN/AGG/DISTINCT` 等通常不可更新（部分数据库可用触发器/INSTEAD OF 实现）。

* **性能**：普通视图每次都会重算；若需要缓存结果，用**物化视图**（不同语法，如 PostgreSQL `CREATE MATERIALIZED VIEW`，需刷新）。

* **维护**：底表结构变化（删列/改名）可能导致视图失效，需要同步修改视图定义。


---

## 第 25 页

![第 25 页](Lec2-Mid-SQL (1)_assets/page-025.png)

**提问：** 什么意思 详细解释

这页演示**视图（View）的定义与使用**，给了两个常见场景：列级脱敏与聚合汇总。



## 1) 去掉敏感列：只暴露教师基本信息



```sql

CREATE VIEW faculty AS

SELECT id, name, dept_name

FROM instructor;

```



含义：把 `instructor` 表中**不含 salary** 的三列封装成一个名为 `faculty` 的“虚拟表”。之后任何人都可以像查表一样使用它，但看不到薪资。



查询示例（用视图筛选某院系教师）：



```sql

SELECT name

FROM faculty

WHERE dept_name = 'Biology';

```



## 2) 汇总视图：各院系的工资总额



```sql

CREATE VIEW departments_total_salary(dept_name, total_salary) AS

SELECT dept_name, SUM(salary)

FROM instructor

GROUP BY dept_name;

```



含义：把“按院系统计工资总和”的结果定义成视图，并**起了列别名** `(dept_name, total_salary)`，方便后续直接查询、联表或授权给只需要汇总结果的用户。



---



### 要点回顾



* `CREATE VIEW v AS <SELECT …>`：视图保存的是**查询表达式**，不是新表；查询视图时会**内联**这段 SQL 重新计算结果。

* 视图适合：



  * **隐藏列/行**（权限与脱敏）

  * **复用复杂查询**（多表 JOIN、聚合等）

* 若需更高性能且可接受延迟，可考虑**物化视图**；否则普通视图每次都会重算。


---

## 第 26 页

![第 26 页](Lec2-Mid-SQL (1)_assets/page-026.png)

**提问：** 什么意思 详细解释

这页在讲**视图之间的依赖关系**：一个视图可以用**另一个视图**来定义，由此产生“直接依赖、传递依赖、递归依赖”等概念。



## 关键术语



* **One view may be used in the expression defining another view**

  可以在 `CREATE VIEW v1 AS <SELECT ... FROM v2 ...>` 中**引用另一个视图 v2**。



* **depend directly（直接依赖）**

  若 `v2` **直接出现在** `v1` 的定义里（`FROM v2 ...`），则 `v1` **直接依赖** `v2`。

  例：



  ```sql

  CREATE VIEW v2 AS SELECT * FROM instructor;

  CREATE VIEW v1 AS SELECT id, name FROM v2;   -- v1 直接依赖 v2

  ```



* **depend on（依赖 / 传递依赖）**

  如果 `v1` 直接依赖 `v2`，**或者**存在一条依赖链 `v1 → … → v2`，都称 `v1` **依赖** `v2`。

  例：`v1 → v2 → base_table`，则 `v1` 依赖 `base_table`（传递的）。



* **recursive（递归）**

  若视图 `v` 的定义**直接或间接引用了自己**，称为**递归视图**。

  在支持递归的数据库（如 PostgreSQL/SQL Server/Oracle），通常用 **`WITH RECURSIVE`** CTE 实现，而**不是**普通 `CREATE VIEW` 的自引用。



## 为什么要关注依赖



* **变更影响**：底层表/视图结构改变（重命名/删列），会**级联影响**所有依赖它的视图。

* **刷新/编译**：物化视图或有缓存的系统需要按**依赖图**决定刷新/重建顺序。

* **权限与安全**：给用户开放上层视图即可，底层表可不授予权限；但一旦上层引用了更多底层对象，权限也要覆盖到这些**依赖**。

* **性能**：多层嵌套视图可能让优化器难以下推过滤/合并查询，导致性能下降。



## 小例子（串联视图）



```sql

CREATE VIEW base_public AS

SELECT id, name, dept_name, salary FROM instructor;



CREATE VIEW faculty AS

SELECT id, name, dept_name FROM base_public;      -- 直接依赖 base_public



CREATE VIEW cs_faculty AS

SELECT * FROM faculty WHERE dept_name = 'Comp. Sci.';  -- 依赖 faculty（传递依赖 base_public）

```



## 实务建议



* 控制**视图层级深度**，避免“视图套视图套视图”。

* 重要视图用 **注释/文档** 标出依赖图；变更前做影响评估。

* 遇到复杂多层视图性能问题，尝试**展开为单一查询**，或改为**物化视图**并定期刷新。


---

## 第 27 页

![第 27 页](Lec2-Mid-SQL (1)_assets/page-027.png)

**提问：** 什么意思 详细解释

这页示范\*\*“用视图定义其他视图”\*\*，给出两条 `CREATE VIEW`，第二个视图以第一个视图为数据源。



## 第一个视图：`physics_fall_2017`



```sql

CREATE VIEW physics_fall_2017 AS

SELECT course.course_id, sec_id, building, room_number

FROM   course, section

WHERE  course.course_id = section.course_id

  AND  course.dept_name = 'Physics'

  AND  section.semester = 'Fall'

  AND  section.year = 2017;   -- 若 year 是整数，最好不要加引号

```



含义：取\*\*物理系（Physics）\*\*在 **2017 年秋季（Fall 2017）**开课的各个**开课班**（`sec_id`）及其上课地点（`building, room_number`）。



* 这里用的是**旧式写法**（逗号 + `WHERE` 等值连接）；等价且更推荐：



  ```sql

  SELECT c.course_id, s.sec_id, s.building, s.room_number

  FROM   course c

  JOIN   section s USING (course_id)

  WHERE  c.dept_name = 'Physics'

    AND  s.semester  = 'Fall'

    AND  s.year      = 2017;

  ```



## 第二个视图：`physics_fall_2017_watson`



```sql

CREATE VIEW physics_fall_2017_watson AS

SELECT course_id, room_number

FROM   physics_fall_2017

WHERE  building = 'Watson';

```



含义：在**上面那个视图**的基础上，再筛选**楼名为 Watson** 的教室，并只保留 `course_id, room_number` 两列。

这体现了**视图可依赖视图**：`physics_fall_2017_watson` 直接依赖 `physics_fall_2017`，后者再依赖底层表 `course/section`。



## 为什么这样做？



* **复用与分层**：把“物理系 2017 秋的所有开课信息”抽成通用视图，再按楼宇筛选可复用。

* **权限与最小暴露**：给普通用户只开第二个视图的权限，可隐藏不需要的列/行。

* **可读性**：业务语义清晰，查询更短。



## 小提示（易错/优化）



* `year` 若为数值列，请写 `year = 2017`；若是字符列，统一单引号 `'2017'`（注意不要混入弯引号）。

* 多层视图**过深**可能影响优化器下推过滤的能力；若性能下降，考虑把查询**展开**或使用**物化视图**。

* 用现代 `JOIN ... ON/USING` 取代逗号连接，语义更清晰、也更利于优化器。


---

## 第 28 页

![第 28 页](Lec2-Mid-SQL (1)_assets/page-028.png)

**提问：** 什么意思 详细解释

这页讲 **View Expansion（视图展开）**：把“引用另一个视图”的定义**内联展开**成对底表的查询。目的是说明——**视图只是查询的别名**，数据库在执行时会把它“展开/替换”到你的 SQL 里。



## 幻灯片两段 SQL 的含义



### 原始定义（基于上页的视图）



```sql

CREATE VIEW physics_fall_2017_watson AS

SELECT course_id, room_number

FROM physics_fall_2017

WHERE building = 'Watson';

```



* 这里 `physics_fall_2017` 是**上一个视图**（筛出 2017 秋季、物理系课程及上课地点）。



### 展开后的等价形式（把上一个视图内联）



```sql

CREATE VIEW physics_fall_2017_watson AS

SELECT course_id, room_number

FROM (

  SELECT course.course_id, building, room_number

  FROM   course, section

  WHERE  course.course_id = section.course_id

    AND  course.dept_name = 'Physics'

    AND  section.semester = 'Fall'

    AND  section.year = '2017'

) AS physics_fall_2017

WHERE building = 'Watson';

```



* 这段把 `physics_fall_2017` 的**查询体**直接放进了 `FROM ( … )` 子查询里；

* 逻辑结果完全一样：最后只保留**Watson 楼**的课的 `course_id` 和 `room_number`。



> 注：如果 `section.year` 是数值型，建议写 `section.year = 2017`（不加引号）。



## 为什么要理解“视图展开”



* **执行本质**：大多数数据库对普通视图会做这种**内联替换**，然后再选计划（优化器据此进行谓词下推、连接重排等）；

* **性能影响**：如果多层视图嵌套、或写法阻碍了优化器（如复杂表达式/不可下推的 CTE），可能导致**过滤无法下推**、中间结果变大，性能变差；

* **调试可读**：遇到慢查询时，把视图**展开**能看清真实被执行的 SQL，便于定位问题。



## 实战小建议



* 视图可以用，但**层级别太深**；

* 优先用显式连接：



  ```sql

  FROM course c

  JOIN section s USING (course_id)

  ```



  而不是逗号连接；

* 过滤条件尽量放在**能下推**的位置（如 `ON` 或子查询内）；

* 性能关键且稳定的汇总结果，考虑改成**物化视图**并定期刷新。


---

## 第 29 页

![第 29 页](Lec2-Mid-SQL (1)_assets/page-029.png)

**提问：** 什么意思 详细解释

这页讲 **“视图展开（View Expansion）” 的机制**——当一个视图由**其他视图**定义时，数据库如何把它还原成对**底层表**的查询。



## 核心思想



把对视图的引用，**反复替换**成它的定义（那条 `SELECT`），直到查询里**不再出现任何视图名**为止。只要没有递归引用，这个过程一定会结束。



用伪代码表示就是幻灯片里的流程：



```

repeat

  在表达式 e1 中找到任意视图 vi

  用 vi 的定义（那条查询）替换 vi

until e1 中不再含有视图

```



## 结合前一页的例子



* 外层：`physics_fall_2017_watson` 引用了 `physics_fall_2017`

* 展开后：把 `physics_fall_2017` 的查询体嵌进去，得到对 `course/section` 的直接查询

  （这就解释了为什么“视图像查询别名/宏”，执行时会被**内联**。）



## 重要点



* **非递归就终止**：若视图之间不存在直接或间接“自引用”，展开有限次后结束；

  递归场景需用 `WITH RECURSIVE` 等专门机制处理。

* **语义等价**：展开只是**语义上的定义方式**；优化器在此基础上再做谓词下推、连接重排等优化。

* **性能启示**：多层视图会生成很长的展开式，可能阻碍优化器看见过滤条件；遇到慢查询时，尝试**手工展开**检查是否能把过滤提到更靠近数据的位置。



一句话：**视图展开 = 把“视图名”逐层替换为其定义的 SELECT，直到只剩底表为止**。


---

## 第 30 页

![第 30 页](Lec2-Mid-SQL (1)_assets/page-030.png)

**提问：** 什么意思 详细解释

这页讲 **物化视图（Materialized View, MV）**——把视图的查询结果**真的落地存成一张物理表**，以后查询直接读这份结果，因此更快；但底表一变，这份结果就**过期**，需要**维护/刷新**。



## 核心要点



* **普通视图**：只保存“查询语句”，每次使用都会重新计算结果（不存数据）。

* **物化视图**：在定义/刷新时，把查询结果**计算并存盘**（有索引、统计信息，可像表一样被扫描）。读查询时通常更快。



## 代价：需要维护



* 当底层表（relations）更新后，MV 会与真实数据**不一致**（stale）。

* 需要\*\*刷新（refresh/maintain）\*\*才能更新：可以是手动、定时任务、触发器或数据库内置的增量刷新。



## 常见刷新方式（不同数据库支持差异）



* **完全刷新**：重新跑一遍查询，替换整张 MV。简单但开销大。

* **增量刷新**（fast/refresh on change）：只把新增/变更部分合并到 MV（需要日志/触发器/物化视图日志等支持）。

* **按计划刷新**：例如每天 2:00、每小时一次；或手动在低峰期刷新。



## 何时使用物化视图



* 复杂聚合 / 大量 JOIN、但查询**读多写少**，且能接受**一定延迟**。

* 常用仪表盘、报表、排行榜、预计算宽表等。



## 何时不适合



* 数据更新非常频繁且必须**强一致**（每次都要最新）——维护成本高、延迟不可接受。

* 查询本身足够快，或有更好的索引/分区/缓存方案。



## 简例（以 PostgreSQL 为例，语法示意）



```sql

CREATE MATERIALIZED VIEW mv_dept_salary AS

SELECT dept_name, SUM(salary) AS total_salary

FROM instructor

GROUP BY dept_name;



-- 刷新

REFRESH MATERIALIZED VIEW mv_dept_salary;           -- 完全刷新

-- 一些系统支持增量刷新或带并发的刷新变体

```



## 小贴士



* 给 MV 建**索引**能显著加速查询。

* 设定**刷新策略**（触发、定时、手动）并监控**滞后性**。

* 变更底表结构时，要评估对 MV 的影响（可能需要重建）。

* 若数据库不支持物化视图，可用“**中间表 + 定时作业**”实现类似效果。



**一句话**：物化视图 = “把昂贵查询的结果缓存成表”，读快了，但要记得**刷新**以保持和底表同步。


---

## 第 31 页

![第 31 页](Lec2-Mid-SQL (1)_assets/page-031.png)

**提问：** 什么意思 详细解释

这页说明\*\*“通过视图进行更新（以插入为例）”\*\*会遇到的问题，以及系统可能采取的做法。



## 场景



我们之前定义了一个去掉薪资列的视图：



```sql

CREATE VIEW faculty AS

SELECT id, name, dept_name

FROM instructor;    -- 注意底表 instructor 还有 salary 列

```



现在用户想往视图里插一行：



```sql

INSERT INTO faculty VALUES ('30765', 'Green', 'Music');

```



## 问题的本质



* **视图本身不存数据**，插入视图必须**映射到底表** `instructor` 去插入。

* 但 `instructor` 有一列 **`salary`**，视图里**看不到也给不出**这个值。

* 因此系统必须决定：**没有提供 `salary` 时怎么办？**



## 两种处理思路（幻灯片上的两条）



1. **拒绝插入**（更安全、常见的默认行为）



   * 报错：缺少必须列（如 `salary` 非空/无默认值）。

2. **允许插入并补值**



   * 把 `('30765','Green','Music', NULL)` 插入到底表 `instructor`。

   * 仅当 **`salary` 允许为 NULL 或有默认值** 时可行；否则仍会失败。



> 幻灯片最后那行就是：把 `('30765','Green','Music', NULL)` 插入 `instructor`。



---



## 什么时候视图“可更新”



一个视图通常**可更新**（可 `INSERT/UPDATE/DELETE`）需要满足：



* 直接基于**单个底表**、无 `DISTINCT/AGGREGATE/GROUP BY/UNION`；

* 不含计算列、常量列或不可映射的表达式；

* 要更新的列在视图中**可见且可被唯一映射**到底表列；

* 底表的约束（非空/外键/检查）能被满足（例如 `salary` 非空就必须提供值或有默认）。



否则，多数数据库会**拒绝**更新；有的数据库可用：



* **`INSTEAD OF` 触发器**（SQL Server/Oracle/SQLite）：自定义“通过视图更新时到底表怎么写”。

* **带 `WITH CHECK OPTION` 的视图**：保证通过视图写入的数据，**仍满足视图条件**（防止“写进去却在视图里看不到”）。



---



## 实战建议



* 若希望允许通过 `faculty` 插入教师信息：



  1. 给 `instructor.salary` 设**默认值**或允许 `NULL`；或

  2. 提供另一个**输入视图**/存储过程，显式要求传入 `salary`；或

  3. 写 **`INSTEAD OF INSERT` 触发器**，在触发器里决定如何为 `salary` 赋值（默认、查表、规则）。



* 若不希望走偏，直接**禁止对该视图的写操作**（只授予 SELECT 权限），在应用层用表单/存储过程写底表更稳妥。



**一句话**：往视图里插数据，数据库最终要把它写到底表；**缺的列怎么处理**是关键——要么**拒绝**，要么**补默认/NULL**（前提是约束允许）。


---

## 第 32 页

![第 32 页](Lec2-Mid-SQL (1)_assets/page-032.png)

**提问：** 什么意思 详细解释

这页说明：**有些视图上的更新（特别是插入）无法唯一地翻译到底层表**，因此数据库通常会拒绝执行。



## 场景



```sql

CREATE VIEW instructor_info AS

SELECT i.ID, i.name, d.building

FROM instructor i

JOIN department d

  ON i.dept_name = d.dept_name;

```



在该视图上尝试插入：



```sql

INSERT INTO instructor_info VALUES ('69987','White','Taylor');

```



## 为什么“翻译不了”？



* 这个视图来自**两张表的连接**（`instructor` 与 `department`）。

* 插入一行到视图，必须能转换成对**底表的插入/更新**。这里至少要满足：



  * 在 `instructor` 插入 `ID='69987', name='White', dept_name = ?`

  * 同时还要有一行 `department` 记录其 `building='Taylor'`，并与上面的 `dept_name` 匹配

* 但视图里**没有 `dept_name`**，因此无法确定该把 `dept_name` 写成哪一个。



### 幻灯片提出的两个歧义



1. **Taylor 楼里有多个系** → “到底属于哪个系？”（`dept_name` 不唯一）

2. **Taylor 楼里没有任何系** → 无法满足连接条件，**根本插不进去**。



因此，这类 **JOIN 视图** 的插入**没有唯一、确定的翻译**，标准做法是**拒绝**。



## 结论与建议



* 一般而言，**只有基于单表且简单的视图**才可更新/可插入。含 `JOIN/AGGREGATE/DISTINCT` 的视图**不可更新**或高度受限。

* 需要在视图上插入时的可选做法：



  * **改为直接写底表**，并**显式提供 `dept_name`**；

  * 提供**存储过程**/API 强制传入所有必需字段并校验；

  * 在支持的数据库中为视图编写 **`INSTEAD OF INSERT` 触发器**，由你来决定如何把插入拆分到 `instructor`/`department`（但也要定义清楚选择哪个 `dept_name`）。



一句话：**联接视图缺乏把插入唯一映射到底层表的关键信息**，所以数据库无法安全执行，除非你额外提供规则或直接操作底表。


---

## 第 33 页

![第 33 页](Lec2-Mid-SQL (1)_assets/page-033.png)

**提问：** 什么意思 详细解释

这页在讲：**并不是所有视图上的更新都合理**。

视图定义：



```sql

CREATE VIEW history_instructors AS

SELECT *

FROM instructor

WHERE dept_name = 'History';

```



问题：如果我们往这个视图插入



```sql

INSERT INTO history_instructors

VALUES ('25566','Brown','Biology',100000);

```



会怎样？



## 关键点



* 该视图只显示 **dept\_name = 'History'** 的教师。

* 插入的行却是 **'Biology'**，**不满足视图条件**。



## 实际行为（取决于是否有检查选项）



1. **没有 `WITH CHECK OPTION`（默认）**

   多数数据库把此视图视为**可更新**并把插入**翻译到底表 `instructor`**：



   * 行会被成功插入为 `('25566','Brown','Biology',100000)`；

   * 但它**不满足视图条件**，所以**在视图里看不到**（“写进去就消失”）。这就是所谓的 *view anomaly*。



2. **加了 `WITH CHECK OPTION`**



   ```sql

   CREATE VIEW history_instructors AS

   SELECT * FROM instructor

   WHERE dept_name = 'History'

   WITH CHECK OPTION;

   ```



   * 数据库会**拒绝**这次插入（因为不满足 `dept_name='History'`），从而避免“看不见的写入”。



## 结论/建议



* 想通过带筛选条件的视图写数据，并保证写入后还能在该视图看到，**务必加 `WITH CHECK OPTION`**。

* 否则就直接对底表操作，或用存储过程/触发器校验业务规则。


---

## 第 34 页

![第 34 页](Lec2-Mid-SQL (1)_assets/page-034.png)

**提问：** 什么意思 详细解释

这页总结 **哪些视图可以被更新（INSERT/UPDATE/DELETE）**。大多数数据库只允许在**简单视图**上更新，满足这些条件时才“可更新”：



1. **FROM 只有一个表**

   视图必须直接来源于单个基础表，不能有 JOIN/UNION 等集合运算。



2. **SELECT 只包含该表的列名**

   不能有表达式/计算列（如 `salary*1.1`）、**聚合**（`SUM/COUNT`）、或 **`DISTINCT`**。



3. **未选出的列可以设为 NULL（或有默认值）**

   因为更新时要写回到底表，视图里没出现的列若在底表是非空且无默认值，就会导致插入失败。



4. **没有 `GROUP BY` / `HAVING`**

   这些会把多行折叠成一行，使得更新无法唯一映射到底表的某一行。



补充小贴士



* 若视图带筛选条件且希望“写入后在视图中可见”，请在定义时加 **`WITH CHECK OPTION`**。

* 复杂视图需要更新时，可改为：直接操作底表、用存储过程/触发器（如 `INSTEAD OF`）、或改造为物化视图并单独维护。


---

## 第 35 页

![第 35 页](Lec2-Mid-SQL (1)_assets/page-035.png)

**提问：** 什么意思 详细解释

这页在讲 **SQL 常见的内置时间类型** 以及它们的用法/运算。



## 4 种核心类型



1. **`DATE`（日期）**

   只包含“年-月-日”。

   例：`DATE '2005-07-27'`



   * 没有时区、小时分钟秒。



2. **`TIME`（一天内的时间）**

   只包含“时:分:秒（可带小数秒）”。

   例：`TIME '09:00:30'`、`TIME '09:00:30.75'`



   * 不含日期/时区。



3. **`TIMESTAMP`（日期 + 时间）**

   等于 `DATE` + `TIME`。

   例：`TIMESTAMP '2005-07-27 09:00:30.75'`



   * 有的数据库区分 `timestamp with time zone` / `without time zone`。



4. **`INTERVAL`（时间间隔/时长）**

   表示一段时间量，如天、小时、月等。

   例：`INTERVAL '1 day'`、`INTERVAL '3 hours'`、`INTERVAL '2 months'`



## 基本运算



* **加间隔**：`date/time/timestamp + interval` → 向后偏移



  ```sql

  DATE '2025-10-12' + INTERVAL '7 days'      -- 2025-10-19

  TIMESTAMP '2025-10-12 09:00' + INTERVAL '90 minutes'

  ```

* **减间隔**：`… - interval` → 向前偏移

* **相减求间隔**：`date/time/timestamp - date/time/timestamp` → 返回 `INTERVAL`



  ```sql

  TIMESTAMP '2025-10-12 10:00' - TIMESTAMP '2025-10-12 09:15'

  -- 结果 ~ INTERVAL '45 minutes'

  ```



## 易混点/实践提示



* **字面量写法**：用类型前缀+单引号更稳（如 `DATE 'YYYY-MM-DD'`）。

* **时区**：若涉及时区，使用支持的类型（如 PostgreSQL 的 `timestamptz`）并显式设置/转换。

* **精度**：`TIME/TIMESTAMP` 可指定小数秒精度（如 `timestamp(3)` 毫秒）。

* **月份间隔**：`INTERVAL '1 month'` 会考虑不同月份天数，和 `30 days` 不等价。

* **比较/排序**：`DATE < TIMESTAMP` 需同类型比较，通常把 `DATE` 转成 `TIMESTAMP` 或反之。


---

## 第 36 页

![第 36 页](Lec2-Mid-SQL (1)_assets/page-036.png)

**提问：** 什么意思 详细解释

这页介绍 **大对象（Large Object, LOB）类型**：用于存储体积很大的数据，如照片、视频、CAD 文件、长文档等。



## 两类大对象



* **BLOB**（Binary Large OBject）

  二进制大对象，数据库**不解释其含义**，原样保存。适合图片、音视频、压缩包等。

* **CLOB**（Character Large OBject）

  字符大对象，保存**很长的文本**（小说、日志、HTML 等）。在支持多字符集的库中也有 **NCLOB**（national character）。



## 结果返回方式



查询含有大对象的行时，很多数据库不会一次把整个大对象直接返回，而是返回一个**定位器/指针（locator/oid/handle）**，由客户端再按需**流式读取**，避免一次性把几百 MB 数据塞进内存。



## 实务要点



* 各库名称略有差异：



  * MySQL：`TINYBLOB/BLOB/MEDIUMBLOB/LONGBLOB` 与 `TEXT` 系列；

  * PostgreSQL：`bytea` 或专用 large object（OID）；

  * Oracle/DB2：`BLOB/CLOB/NCLOB`。

* **索引/查询**：BLOB 通常**不能全文索引**；CLOB 需配合**全文索引**功能（如 Oracle Text、MySQL/InnoDB FTS、PG 的 tsvector）才能检索内容。

* **读写方式**：使用**流式 API**（分块读写）更稳；避免 `SELECT *` 把大对象无意带出。

* **存储策略**：超大文件或频繁下载的资源，常放对象存储（S3、OSS）并在表中保存**URL/哈希/元数据**；只有确实需要强事务/统一备份时才放进数据库。

* **备份与迁移**：含 LOB 的表体积大、备份/恢复更慢，需规划窗口与压缩。


---

## 第 37 页

![第 37 页](Lec2-Mid-SQL (1)_assets/page-037.png)

**提问：** 什么意思 详细解释

> ⚠️ 未能复制为 Markdown，以下为纯文本回退：

这页讲 **用户自定义类型（User-Defined Type, UDT）**，  
用于给现有基础类型起一个更**语义化的名称**，并可附带约束或规则，  
让表设计更规范、更具表达力。

---

## 🧩 幻灯片在做什么

```sql
-- 定义一个“金额”类型：基于定点小数 numeric(12,2)
CREATE TYPE Dollars AS NUMERIC(12,2) FINAL;

-- 在表中直接使用
CREATE TABLE department (
  dept_name VARCHAR(20),
  building  VARCHAR(15),
  budget    Dollars        -- 用自定义类型表示预算
);
```

- `Dollars` 本质上以 `NUMERIC(12,2)` 为底层存储，
   但有了专属的类型名，表达了**“这是金额”**的语义。
- `FINAL`（来自 SQL 标准 / DB2 语法）表示**不允许再基于它创建子类型**，
   使类型层次结构保持稳定。

------

## 💡 为什么要用自定义类型

### 1️⃣ 语义清晰

看到 `budget Dollars`，就立刻知道这是金额字段，
 而不是随便的 `NUMERIC`。

### 2️⃣ 集中管理

若要调整金额精度，比如从 `(12,2)` 改为 `(14,2)`，
 只需修改类型定义即可，表结构保持不变。
 （不同数据库支持方式略有差异）

### 3️⃣ 类型安全

部分数据库（如标准 SQL 的 **DISTINCT TYPE** 模型）
 可阻止将 `Dollars` 与普通 `NUMERIC` 混用，
 必须显式转换，避免语义错误。

### 4️⃣ 可附带约束或默认值

在 **PostgreSQL** 中，更常用 `CREATE DOMAIN` 语法来定义：

```sql
CREATE DOMAIN dollars AS NUMERIC(12,2)
  CHECK (VALUE >= 0);   -- 不允许负数
```

这样，所有 `dollars` 列都会**自动继承约束**。

------

## 🧱 实务提示

- **金额类型**：应使用定点小数 `DECIMAL` / `NUMERIC`，不要用浮点。

- **货币符号与格式化**：属于显示层问题。
   若涉及多币种，应为金额与货币代码（如 ISO 4217 的 `currency_code`）单独建列。

- **不同数据库支持差异**：

  | 数据库         | 推荐方式                               | 说明                               |
  | -------------- | -------------------------------------- | ---------------------------------- |
  | PostgreSQL     | `CREATE DOMAIN` 或复合类型             | 支持完整约束与继承                 |
  | DB2 / 标准 SQL | `CREATE TYPE ... AS DECIMAL ... FINAL` | 支持 DISTINCT 类型语义             |
  | MySQL          | 无通用 UDT/Domain                      | 可用 `CHECK` 约束 + 视图或别名模拟 |

------

## 🧠 一句话总结

> **用户自定义类型（UDT）** = “语义化的基础类型”
>  让表结构更直观、统一管理、更安全。
>  尤其适用于金额、百分比、ID 等具有特定含义的字段。

```

```


---

## 第 38 页

![第 38 页](Lec2-Mid-SQL (1)_assets/page-038.png)

**提问：** 什么意思 详细解释

> ⚠️ 未能复制为 Markdown，以下为纯文本回退：

这页讲 **Domain（域）**：  
把“**基础类型 + 约束**”封装成一个可复用的**自定义数据类型模板**。  
使用域（Domain）能让多张表共享统一的取值规则（非空、范围、格式等）。

---

## 🧩 核心概念

**语法（SQL-92 标准）：**

```sql
CREATE DOMAIN person_name CHAR(20) NOT NULL;
```

**含义**：定义一个域 `person_name`，
 本质上是 `CHAR(20)` 类型，并**强制 `NOT NULL`**。

域（Domain）与类型（Type）类似，但更强大：
 可以在定义时内置约束（`NOT NULL`、`DEFAULT`、`CHECK` 等），
 以后每次使用该域的列都会**自动继承这些规则**。

------

## 🧱 示例：枚举约束

```sql
CREATE DOMAIN degree_level VARCHAR(10)
  CONSTRAINT degree_level_test
  CHECK (VALUE IN ('Bachelors','Masters','Doctorate'));
```

- `VALUE` 表示该域中每个值的取值。
- 使用此域的列，自动只能取 `'Bachelors'`、`'Masters'` 或 `'Doctorate'` 三个值。

------

## 🧾 在表中使用

```sql
CREATE TABLE student (
  id    CHAR(8)        PRIMARY KEY,
  name  person_name,    -- 继承 NOT NULL 约束
  level degree_level    -- 继承 CHECK 枚举规则
);
```

当插入或修改数据时，
 `name` 列不能为 `NULL`，`level` 列只能取指定枚举值。

------

## 🌟 好处

1. **一次定义，多处复用**
    修改域定义即可全库生效（不同数据库传播机制略有差异）。
2. **一致性**
    避免在每个表重复写相同的约束逻辑。
3. **可读性更高**
    列名与域名结合后更具语义，例如：
    `degree_level`、`email_addr`、`money_nonneg`。

------

## 💡 常见用法示例

统一邮箱格式、手机号长度、金额非负等规则：

```sql
CREATE DOMAIN money_nonneg NUMERIC(12,2)
  CHECK (VALUE >= 0);

CREATE DOMAIN email_addr TEXT
  CHECK (VALUE ~ '^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$');  -- PostgreSQL 正则示例
```

> 所有使用 `money_nonneg` 的列，都自动禁止负数。
>  所有使用 `email_addr` 的列，都必须符合邮箱正则格式。

------

## ⚙️ 兼容性提示

| 数据库           | 支持情况                           | 说明                                   |
| ---------------- | ---------------------------------- | -------------------------------------- |
| **PostgreSQL**   | ✅ 完整支持 `CREATE DOMAIN`（推荐） | 可配合正则、默认值等约束使用           |
| **Oracle / DB2** | ✅ 有域或类似机制                   | 写法略有差异                           |
| **MySQL**        | ⚠️ 无原生 Domain                    | 可用 `CHECK` 约束 + 视图 / 触发器 模拟 |

------

## 🧠 一句话总结

> **Domain = 可复用的 “类型 + 约束”**
>  让业务规则沉淀到数据层，
>  统一全库约束，提升一致性与可维护性。

```

```


---

## 第 39 页

![第 39 页](Lec2-Mid-SQL (1)_assets/page-039.png)

**提问：** 什么意思 详细解释

> ⚠️ 未能复制为 Markdown，以下为纯文本回退：

这页在讲：**用 VIEW（视图）做数据清洗** 的思路与好处。

---

## 🎯 主题

先了解 **ETL（Extract–Transform–Load）**：抽取 → 转换 → 加载。  
本页强调一种常用做法：**不改动原始表**，把清洗规则写在一层或多层**视图**里；  
当需要性能时，再把结果**物化**（生成物化视图 / 中间表）来提速。

---

## ✅ 好处（逐条解释）

1. **原表不动，随时可回滚**  
   原始“脏数据”仍在原表；你只是“投影”出一份干净视图。出问题删视图即可，数据不受影响。

2. **清洗逻辑集中在 SQL（视图定义）里，便于版本管理**  
   规则写在 `CREATE VIEW ... AS SELECT ...` 中，可直接纳入 Git，审计/回溯清晰。

3. **规则可迭代叠加**  
   需要新增校验或修复？**再包一层视图**即可；旧视图仍可用于历史任务。  
   典型分层：`v1_raw（初筛） → v2_valid（校验/修正） → v3_enriched（补充/标准化）`。

4. **需要性能时再“物化”**  
   当视图较慢时，创建**物化视图**（或落地中间表）缓存结果，按需刷新。

---

## ⚙️ 物化示例

```sql
CREATE MATERIALIZED VIEW mv_clean AS
SELECT * FROM v2_orders_valid;

-- 后续查询直接读 mv_clean
-- 定期刷新
REFRESH MATERIALIZED VIEW mv_clean;
```

------

## 🐘 PostgreSQL 常见模式

- 脏数据**保留**在库内；干净数据按需**投影（view）\**或\**缓存（materialized view）**。
- 既安全，又易迭代；性能瓶颈出现时再“物化 + 索引”。

------

## 🧪 小示例（示意）

```sql
-- v1：去掉空主键、类型修正
CREATE VIEW v1_orders_base AS
SELECT *
FROM   orders
WHERE  order_id IS NOT NULL;

-- v2：业务校验与标准化
CREATE VIEW v2_orders_valid AS
SELECT
  order_id,
  COALESCE(TRIM(email), '')      AS email,
  GREATEST(amount, 0)::numeric   AS amount,   -- 负数钳为 0
  order_ts::timestamp            AS order_ts
FROM v1_orders_base
WHERE email ~* '^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$';  -- 邮箱正则（PG）

-- 需要加速时：物化
CREATE MATERIALIZED VIEW mv_clean AS
SELECT * FROM v2_orders_valid;

-- 定期刷新
REFRESH MATERIALIZED VIEW mv_clean;
```

------

## 🛠️ 实务提示

- **先视图、后物化**：开发期以视图快速迭代；稳定后再物化提速。
- **步骤拆小、命名清晰**：有利于排错与回放（`v1_...` / `v2_...` / `v3_...`）。
- **物化视图要配刷新策略**（定时/触发），并考虑**索引**与**依赖关系**。
- 若数据库**不支持物化视图**：用**中间表 + 定时任务**替代（并在中间表上建索引）。

------

## 🧠 一句话

> **视图做清洗，物化提性能**：
>  清洗逻辑集中、可回滚、易版本化；需要时再缓存结果，兼顾**正确性**与**效率**。

```
::contentReference[oaicite:0]{index=0}
```


---

## 第 40 页

![第 40 页](Lec2-Mid-SQL (1)_assets/page-040.png)

**提问：** 什么意思 详细解释

> ⚠️ 未能复制为 Markdown，以下为纯文本回退：

这页在抛出一个问题：  
> **除了用 VIEW 做数据清洗，你还知道哪些清洗方法？**  

下面是一份 **“思路清单”**，按场景归类，可直接套用。

---

## 🧱 1) 写入即校验（源头把关）

- **强类型与约束**：`NOT NULL`、`CHECK`、`UNIQUE`、`FOREIGN KEY`、`ENUM/DOMAIN`，并使用正确的数据类型（金额用 `NUMERIC` 而非浮点）。  
- **视图写入保护**：`WITH CHECK OPTION` 的视图，防止写入不符合条件的记录。  
- **触发器 / 存储过程**：在 `BEFORE INSERT/UPDATE` 阶段统一清理空白、大小写标准化、默认值补齐、脏值拦截。

---

## 🧮 2) 库内批处理清洗（ELT）

- **分层模型**：  
  `stg_*（落地原始） → ods_*（格式化） → dwd/dim/fact（业务层）`  
  分层隔离，清洗步骤清晰。
- **暂存/对账表 + MERGE**：  
  新数据先落暂存表，再用 `MERGE` / `UPSERT` 去重、比对、更新。
- **窗口函数去重**：

  ```sql
  DELETE FROM t
  WHERE ctid IN (
    SELECT ctid FROM (
      SELECT ctid, ROW_NUMBER() OVER (PARTITION BY key ORDER BY updated_at DESC) rn
      FROM t
    ) x WHERE rn > 1
  );
  ```

- **物化视图 / 中间表**：
   把清洗结果落地并加索引，加快后续查询。

------

## ⚙️ 3) 管道式 ETL / ELT 编排

- **dbt**：SQL 变换 + 内置数据测试（唯一性、非空、外键）。
- **Airflow / Prefect**：编排多步清洗、重试与依赖关系。
- **云数仓原生功能**：
   Snowflake `tasks/streams`、BigQuery `scheduled queries` 等支持定时清洗。

------

## 🐍 4) 编程式清洗

- **Pandas / Polars**：中小数据集的快速处理与校验。
- **PySpark / SparkSQL**：适用于海量分布式数据清洗。
- **正则 / 标准化库**：邮箱、手机号、地址格式化；日期解析（`dateutil`、`arrow`）。

------

## ⚡ 5) 流式实时清洗

- **Kafka / Flink / Kafka Streams**：
   实时去重、补全、异常剔除。
- **Schema Registry（Avro / Protobuf）**：
   在消息层强制 schema，防止脏字段进入下游。

------

## 📊 6) 数据质量与治理

- **Great Expectations / Deequ**：
   可编程的数据质量断言与报告生成。
- **数据契约（Data Contracts）**：
   上游定义 schema 与质量 SLO，下游依据契约验收。
- **数据剖析与观测**：
   监控空值率、唯一性、分布漂移、异常检测与告警。

------

## 🗂️ 7) 参考与主数据

- **主数据管理（MDM）**：统一客户、商品等关键主数据。
- **参考维表**：
   合法值白名单、代码表（国家、货币等），通过外键或 `JOIN` 校验。

------

## 🔍 8) 记录链接与去重技巧

- **确定性匹配**：主键或多字段组合。
- **概率 / 模糊匹配**：编辑距离、指纹（fingerprint）、Soundex；
   PostgreSQL 可用 `pg_trgm` 模糊匹配扩展。

------

## 🧾 9) 审计与可回滚

- **原始数据只追加（immutable raw）**，清洗结果单独存放。
- **操作日志与血缘追踪**：记录每步清洗来源与变更。
- **慢变维（SCD）**：
   使用 `valid_from / valid_to` 字段版本化，避免“改历史”。

------

## 💡 选型建议

| 场景                | 推荐方案                        |
| ------------------- | ------------------------------- |
| 少量数据 / 快速迭代 | 视图 + 物化视图 / dbt           |
| 高并发 OLTP         | 约束 + 触发器把关               |
| 大规模离线处理      | Spark / 仓内 ELT                |
| 准实时 / 实时流     | Kafka / Flink + Schema Registry |
| 强监管 / 可追溯场景 | 原始落地 + 分层清洗 + 质量断言  |

------

## 🧠 一句话总结

> 数据清洗没有唯一解。
>  **从源头约束，到库内处理，到流式与质量管理**，
>  关键是：规则清晰、层次分明、可追踪、可复用。

```

```


---

## 第 41 页

![第 41 页](Lec2-Mid-SQL (1)_assets/page-041.png)

**提问：** 什么意思 详细解释

> ⚠️ 未能复制为 Markdown，以下为纯文本回退：

这页在做一个 **数据处理工具的对比**（易用性、性能、内存依赖、可扩展性），  
帮助你根据场景选择合适工具。

---

## 🧰 四类工具说明

| 工具类别               | 代表工具                                         | 典型特征               |
| ---------------------- | ------------------------------------------------ | ---------------------- |
| **Linux Command Line** | `grep` / `sed` / `awk` / `sort` / `join` / `cut` | 轻量、流式处理文本     |
| **Python / Pandas**    | `pandas`、`polars`                               | 内存数据帧分析         |
| **SQL / DB**           | PostgreSQL、MySQL、ClickHouse、Spark SQL、Trino  | 数据库存储与分布式计算 |
| **GUI Tools**          | DBeaver、Excel、Power Query、Tableau Prep        | 可视化界面操作         |

---

## 📊 各维度对比说明

### **1️⃣ 易用性（Easy to Use）**

| 工具         | 易用性      | 说明                       |
| ------------ | ----------- | -------------------------- |
| Linux 命令行 | ❌ Not good  | 学习曲线陡，命令组合复杂   |
| Pandas       | ⚙️ Not bad   | API 直观、社区丰富         |
| SQL / DB     | ✅ Good      | 语法统一、易上手、标准化强 |
| GUI          | 🎨 Very good | 拖拽式操作，对小任务友好   |

---

### **2️⃣ 性能（Performance）**

| 工具         | 性能表现  | 说明                                                         |
| ------------ | --------- | ------------------------------------------------------------ |
| Linux 命令行 | ✅ Good    | 流式 + 外部排序/哈希，处理文本 CSV 极快                      |
| Pandas       | 🐢 Slow    | 单机单进程、全内存计算，数据大就变慢                         |
| SQL / DB     | ⚖️ Medium  | 比 Pandas 快（索引、并行、向量化），但简单文本场景略慢于命令行 |
| GUI          | 🤷 Depends | 取决于底层引擎（多数仍在调 SQL 或脚本）                      |

---

### **3️⃣ 内存依赖（Memory）**

| 工具         | 是否依赖内存 | 说明                                           |
| ------------ | ------------ | ---------------------------------------------- |
| Linux 命令行 | ❌ 少依赖     | 可流式读写、磁盘外排                           |
| Pandas       | ✅ 高依赖     | 全量加载内存，易 OOM                           |
| SQL / DB     | ❌ 少依赖     | 基于磁盘、分页执行                             |
| GUI          | 🤷 Depends    | 取决于底层：连数据库则磁盘；导出到本地则占内存 |

---

### **4️⃣ 可扩展性（Scalability）**

| 工具         | 可扩展性   | 说明                                              |
| ------------ | ---------- | ------------------------------------------------- |
| Linux 命令行 | 🚫 不可扩展 | 单机为主                                          |
| Pandas       | 🚫 不可扩展 | 无分布式能力（除非转 Spark/Modin）                |
| SQL / DB     | 💪 最佳     | 分布式引擎（Hive/Spark/Trino/BigQuery）可水平扩展 |
| GUI          | 🤷 Depends  | 连接到可扩展后端即可扩展                          |

---

## 🧭 选型建议（按场景）

| 场景                             | 推荐工具                                                     | 原因                         |
| -------------------------------- | ------------------------------------------------------------ | ---------------------------- |
| 几 MB～几百 MB 的一次性文本清洗  | 🐚 **Linux 命令行** (`grep | awk | sort -u`)                  | 快速高效、无需部署           |
| 单机内存级分析 / 特征工程        | 🐍 **Pandas / Polars**                                        | 简便、生态丰富               |
| 结构化数据 / 多人共享 / 权限控制 | 🗃️ **数据库 + SQL**                                           | 事务支持、索引完备           |
| ≥ 几十 GB / TB 级批处理          | ⚙️ **分布式 SQL 引擎（Spark / Trino / BigQuery / Snowflake）** | 可横向扩展                   |
| 非技术同学 / 临时查看            | 🖱️ **GUI 工具（DBeaver / Power Query / Excel）**              | 上手快，但不建议用于复杂清洗 |

---

## 💡 实战经验贴士

- **超出内存 → 别勉强 Pandas**  
  改用 **分块处理**、**DuckDB/Polars lazy** 或 **数据库 / 分布式 SQL**。
- **重清洗要可重现**  
  优先 **SQL 脚本 / 视图 / dbt**，GUI 仅用于探索。
- **命令行很强大**  
  排序、去重、聚合、连接文本表（`sort | uniq -c | join`）常比脚本更快。
- **SQL 可两端通吃**  
  小数据在本地库跑，大数据同样 SQL 可迁移到分布式仓库，迁移成本极低。

---

## 🧠 一句话总结

> **小即命令行，表即 SQL，内存即 Pandas，分布式即 Spark。**  
> 根据数据量与协作需求选工具，才能在“速度—复用—稳定性”间取得平衡。