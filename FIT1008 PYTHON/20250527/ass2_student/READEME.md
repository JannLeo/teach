你列出的五个问题在数据库开发中都非常重要，下面我将逐一分析你提供的 **T3-rm-dm.sql** 文件，确认是否真的存在这些问题，并提出如何改进。

------

## ✅ 文件检查结果（T3-rm-dm.sql）

### 1️⃣ **事务管理：❌ 未正确使用单一事务**

**分析：**
 你的代码在 `(a)` 到 `(d)` 中多次使用 `COMMIT;`，例如：

```sql
commit;
--(b)
...
commit;
--(d)
...
commit;
```

**问题：**
 这确实会将多个操作分成了**多个独立的事务**，如果中途出错（比如插入失败），前面的操作就**已经永久提交**，从而导致数据不一致。

**改进建议：**

- 最后统一写一个 `COMMIT;`
- 中间不要分段 `COMMIT;`
- 使用事务控制：如 `SAVEPOINT` 或回滚（如果涉及 DML 复杂流程）

------

### 2️⃣ **主键约束：❌ 硬编码 `entry_no` 违反复合主键唯一性**

**分析：**
 你写了：

```sql
entry_no = 99
...
entry_no = 77
```

而你的主键定义是：

```sql
PRIMARY KEY (event_id, entry_no)
```

这就意味着 **entry_no 在同一个 event_id 下必须唯一**。如果你在 **同一个 event_id 下重复用 99 或 77**，就违反了主键。

**是否有问题？**

- 如果你**确认 `entry_no` 在某 `event_id` 下是唯一的**，就没问题。
- 但建议不要硬编码，应使用如下逻辑生成：

```sql
(select NVL(MAX(entry_no),0) + 1 from ENTRY where event_id = ...)
```

✅ **你在 `(c)` 部分已经用对了！**
 但 `(b)` 插入新 entry 时，仍然硬编码 `entry_no = 99`，应改为动态生成。

------

### 3️⃣ **数据一致性：❌ 直接更新主键字段 `entry_no`**

**分析：**
 你在 `(c)` 中有如下代码：

```sql
update ENTRY
set event_id = ..., entry_no = ...
```

其中 `entry_no` 是主键的一部分，**不推荐直接更新**，因为：

- 容易引发外键失效
- 可能违反唯一性约束
- 如果别的表依赖它，会造成 referential integrity 问题

**建议：**

- 如果一定要修改主键，优先采用：**删除旧记录 + 插入新记录** 的方式更安全。

------

### 4️⃣ **子查询冗余：❌ 多处重复子查询影响性能**

**分析：**
 你多次写了重复查询，如：

```sql
(select event_id from EVENT
    where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = ...)
    and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = ...)
)
```

**问题：**

- 相同的子查询重复写多次，会严重影响性能，特别是在大型数据库中。
- 查询计划也会重复解析相同内容。

**建议：**

- 使用 `WITH` 子句提前定义这些子查询，提高可读性与效率：

```sql
WITH winter_event AS (
  SELECT event_id
  FROM EVENT
  WHERE carn_date = (SELECT carn_date FROM CARNIVAL WHERE upper(carn_name) = '...')
  AND eventtype_code = (SELECT eventtype_code FROM EVENTTYPE WHERE lower(eventtype_desc) = '...')
)
...
SELECT * FROM ENTRY WHERE event_id = (SELECT event_id FROM winter_event);
```

------

### 5️⃣ **异常处理：❌ 未处理可能的查询空结果**

**分析：**
 你有这样的查询：

```sql
(SELECT char_id FROM CHARITY WHERE char_name = 'Salvation Army')
```

如果 `CHARITY` 表中不存在该名字，会导致插入失败：

> ORA-01403: no data found (when used in PL/SQL block)
>  或者
>  ORA-01427: single-row subquery returns more than one row

**建议：**

- 加 `EXISTS` 检查
- 或使用 `MERGE`, `UPSERT`, 或带默认值的子查询

示例：

```sql
(SELECT COALESCE((SELECT char_id FROM CHARITY WHERE char_name = 'Salvation Army'), 0) FROM dual)
```

------

## ✅ 总结是否存在这些问题：

| 问题编号 | 问题描述                 | 是否存在 | 改进建议                          |
| -------- | ------------------------ | -------- | --------------------------------- |
| 1        | 多次 `COMMIT` 非单一事务 | ✅ 是     | 只使用一次 `COMMIT`，最后执行     |
| 2        | 硬编码 `entry_no`        | ✅ 是     | 使用 `MAX(entry_no) + 1` 自动生成 |
| 3        | 更新主键字段             | ✅ 是     | 避免更新主键，改为删除+插入       |
| 4        | 重复子查询               | ✅ 是     | 用 `WITH` 子句提取复用逻辑        |
| 5        | 子查询无异常处理         | ✅ 是     | 加 `EXISTS`, `COALESCE`, 或判断空 |

------

如你需要，我可以帮你改写这些部分，使用更安全和优化的写法。是否需要我帮你做这一步？

当然可以，我会逐条指出你的 T3 脚本中需要修改的地方，然后给出**改进建议和重写后的代码片段**，你可以直接替换到原 SQL 文件中。

------

## ✅ 改进点 1：多次 `COMMIT` → ✅ 统一事务提交

### 🛠 问题位置：

你在每个小节 `(a)` 到 `(d)` 后面都写了 `COMMIT;`

### ✅ 应该改为：

只保留**最末尾的一个 `COMMIT;`**

### ✅ 示例：

```sql
-- 删除所有中间的 commit;
-- 最后添加一个统一的 commit
COMMIT;
```

------

## ✅ 改进点 2：硬编码 `entry_no` → ✅ 自动生成 entry_no

### 🛠 问题位置：

```sql
entry_no = 99
entry_no = 77
```

这些 entry_no 是硬编码的，可能与其他记录冲突。

### ✅ 应该改为：

使用 `MAX(entry_no) + 1` 方式生成唯一编号（针对特定 event_id）

### ✅ 示例改写：

```sql
-- 定义新 entry_no 为当前 event 中最大值 + 1
WITH new_entry_no AS (
  SELECT NVL(MAX(entry_no), 0) + 1 AS next_no
  FROM ENTRY
  WHERE event_id = (
    SELECT event_id FROM EVENT
    WHERE carn_date = (SELECT carn_date FROM CARNIVAL WHERE upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
    AND eventtype_code = (SELECT eventtype_code FROM EVENTTYPE WHERE lower(eventtype_desc) = '10 km run')
  )
)
```

然后在 INSERT 中引用：

```sql
INSERT INTO ENTRY (
    event_id, entry_no, ..., comp_no, ...
)
SELECT
    e.event_id,
    n.next_no,
    TO_DATE('08:00:00','hh24:mi:ss'),
    NULL, NULL,
    competitor_seq.CURRVAL,
    NULL,
    (SELECT char_id FROM CHARITY WHERE char_name = 'Salvation Army')
FROM
    (SELECT event_id FROM EVENT
      WHERE carn_date = (SELECT carn_date FROM CARNIVAL WHERE upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
      AND eventtype_code = (SELECT eventtype_code FROM EVENTTYPE WHERE lower(eventtype_desc) = '10 km run')
    ) e,
    new_entry_no n;
```

------

## ✅ 改进点 3：不更新主键字段 → ✅ 删除再插入（或避免更新）

### 🛠 问题位置：

```sql
UPDATE ENTRY
SET event_id = ..., entry_no = ...
```

这会直接修改复合主键字段，不安全。

### ✅ 应该改为：

**删除原 ENTRY，重新插入到新 event 下**，或者只更新非主键字段。

### ✅ 建议重写：

```sql
-- 先删除原记录
DELETE FROM ENTRY
WHERE event_id = ... AND entry_no = 77;

-- 再插入一条新记录
INSERT INTO ENTRY (...)
VALUES (...);
```

------

## ✅ 改进点 4：重复子查询 → ✅ 用 WITH 表达式提取

### 🛠 问题位置：

你对 event_id 的获取出现了**5~10次重复代码**，结构如下：

```sql
(select event_id from EVENT
 where carn_date = ...
 and eventtype_code = ...)
```

### ✅ 应该改为：

使用 `WITH` 子句统一引用：

```sql
WITH event_10km AS (
  SELECT event_id FROM EVENT
  WHERE carn_date = (SELECT carn_date FROM CARNIVAL WHERE upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
  AND eventtype_code = (SELECT eventtype_code FROM EVENTTYPE WHERE lower(eventtype_desc) = '10 km run')
)
```

然后统一使用：

```sql
SELECT * FROM ENTRY WHERE event_id = (SELECT event_id FROM event_10km);
```

------

## ✅ 改进点 5：无异常处理 → ✅ 使用 `COALESCE` 或 `EXISTS`

### 🛠 问题位置：

```sql
(SELECT char_id FROM CHARITY WHERE char_name = 'Salvation Army')
```

如果该 charity 不存在，会抛出错误。

### ✅ 应该改为：

```sql
COALESCE((SELECT char_id FROM CHARITY WHERE char_name = 'Salvation Army'), default_char_id)
```

或提前判断是否存在：

```sql
-- 插入前验证
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM CHARITY WHERE char_name = 'Salvation Army'
    ) THEN
        RAISE_APPLICATION_ERROR(-20001, 'Charity not found');
    END IF;
END;
```

------

## 🧩 额外建议：团队创建逻辑也可优化

你目前团队创建是：

```sql
INSERT INTO TEAM (...) VALUES (...);
```

也可以使用 INSERT + SELECT 方式从 EVENT 和 CARNIVAL 直接查找 event_id，避免冗余子查询。

------

## ✅ 总结：修改点一览

| 类别     | 建议                       | 修改方式                  |
| -------- | -------------------------- | ------------------------- |
| 事务控制 | 使用单一 `COMMIT;`         | 删除所有中间 `commit`     |
| 主键控制 | 自动生成 `entry_no`        | 用 `MAX(entry_no)+1`      |
| 主键更新 | 避免更新主键字段           | 删除原记录再插入          |
| 查询优化 | 使用 `WITH` 子句统一子查询 | 避免 copy-paste 子查询    |
| 错误处理 | 使用 `COALESCE` 或异常检测 | 防止 charity 查不到时报错 |

------

如你需要，我可以把你整段 T3 文件替换为 **结构更清晰 + 安全性更高** 的版本。是否需要我直接帮你重写 T3？















你写的 `T4-rm-mods.sql` 脚本已经**基本正确**，并且逻辑清晰，能实现题目要求的两个功能。但仍然存在一些可**优化和改进的细节问题**，下面我逐条指出：

------

## ✅ 总体结构说明

| 部分 | 功能                           | 状态           |
| ---- | ------------------------------ | -------------- |
| (a)  | 给 COMPETITOR 表添加字段并更新 | ✅ 正确         |
| (b)  | 创建 ENTRY_CHARITY 表结构      | ✅ 正确         |
| (b)  | 插入分配比例数据               | ✅ 正确但需优化 |

------

## ✏️ 改进建议和修改点

------

### 🔧 **(a) 添加字段和更新逻辑**

#### ✅ 逻辑正确，但建议：

- 将 `UPDATE` 写成 `MERGE`（可选）
- 确保 `entry` 表中数据是最新的（前面步骤完成）
- `DESC COMPETITOR` 不推荐出现在脚本中，留在 SQL Plus 中执行即可

------

### 🔧 **(b) ENTRY_CHARITY 表设计问题**

#### ✅ 表结构设计合理，主键复合，外键设置也正确。

#### ❗**建议优化 INSERT 中重复复杂子查询**

你写了两条 INSERT，但里面重复了大量嵌套 `JOIN` 子查询，**不利于维护和性能**。

------

### ✅ 推荐改写方式（简洁、逻辑更清晰）

使用 `WITH` 子句避免重复查询：

```sql
WITH jackson_entry AS (
  SELECT e.event_id, e.entry_no
  FROM ENTRY e
  JOIN COMPETITOR c ON e.comp_no = c.comp_no
  JOIN EVENT ev ON e.event_id = ev.event_id
  JOIN EVENTTYPE et ON ev.eventtype_code = et.eventtype_code
  JOIN CARNIVAL ca ON ev.carn_date = ca.carn_date
  WHERE LOWER(c.comp_fname || ' ' || c.comp_lname) = 'jackson bull'
    AND UPPER(ca.carn_name) = 'RM WINTER SERIES CAULFIELD 2025'
    AND LOWER(et.eventtype_desc) = '5 km run'
)
INSERT INTO ENTRY_CHARITY (
  event_id, entry_no, char_id, percentage
)
SELECT je.event_id, je.entry_no,
       (SELECT char_id FROM CHARITY WHERE char_name = 'RSPCA'), 70
FROM jackson_entry je;

INSERT INTO ENTRY_CHARITY (
  event_id, entry_no, char_id, percentage
)
SELECT je.event_id, je.entry_no,
       (SELECT char_id FROM CHARITY WHERE char_name = 'Beyond Blue'), 30
FROM jackson_entry je;
```

------

### 🟡 可选增强功能（用于防错）：

#### ➕ 加入异常检查或 `EXISTS`：

```sql
-- 确保不会插入不存在的 charity
SELECT COUNT(*) FROM CHARITY WHERE char_name = 'RSPCA'; -- 应返回1
```

------

## ✅ 总结建议

| 项目                        | 状态    | 建议                                                |
| --------------------------- | ------- | --------------------------------------------------- |
| 字段添加与更新              | ✅       | `DESC` 可移除，建议使用 `MERGE` 优雅更新            |
| 表结构设计（ENTRY_CHARITY） | ✅       | 合理，标准范式结构                                  |
| 插入数据                    | 🟡       | 子查询太冗长，建议用 `WITH` 简化                    |
| 数据准确性验证              | ❗可增强 | 可添加 EXISTS 或 SELECT COUNT 检查 charity 是否存在 |

------

是否需要我将上面建议直接整理成你完整的 `T4-rm-mods.sql` 改写版本？你可以直接复制粘贴运行。