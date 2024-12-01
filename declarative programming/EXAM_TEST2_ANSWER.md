### University of Computing Science  
Department of Computer Science  
**Functional and Logic Programming Exam**

**Duration**: 2 hours  
**Reading Time**: 15 minutes  
**Total Marks**: 100

**Instructions**:
1. Answer all questions on the exam paper itself.
2. The number of marks for each question is given; use it as a guide for the time to spend on each question.
3. No electronic devices or additional materials are permitted.

---

#### Question 1: Haskell List Operations [15 marks]

Define a Haskell function `removeDuplicates :: Eq a => [a] -> [a]` that removes all duplicate elements from a list, keeping only the first occurrence of each element.

For example:
```haskell
removeDuplicates [1, 2, 2, 3, 4, 4, 5] = [1, 2, 3, 4, 5]
removeDuplicates "mississippi" = "misp"
```

---

这个问题要求我们定义一个 Haskell 函数 `removeDuplicates`，它可以从一个列表中删除所有重复的元素，并保留每个元素的首次出现位置。

### 题目分析

- 函数 `removeDuplicates` 的类型签名是 `Eq a => [a] -> [a]`：
  - **`Eq a`**：意味着元素类型 `a` 必须支持相等性判断（可以使用 `==` 比较）。
  - **`[a] -> [a]`**：函数接受一个元素类型为 `a` 的列表，并返回一个去重后的新列表。

- **功能要求**：`removeDuplicates` 的目标是保留列表中元素的第一次出现，并删除后续的重复项。例如：
  - `removeDuplicates [1, 2, 2, 3, 4, 4, 5]` 应返回 `[1, 2, 3, 4, 5]`。
  - `removeDuplicates "mississippi"` 应返回 `"misp"`，即每个字符的首次出现。

### 解决方案

我们可以使用递归定义 `removeDuplicates` 函数。基本思路是：
1. 从左到右遍历列表。
2. 对于每个元素，检查它是否已经在结果列表中出现过。
3. 如果没有出现过，则将该元素添加到结果列表中。
4. 如果已经出现过，则跳过该元素，继续处理下一个元素。

以下是具体实现：

```haskell
removeDuplicates :: Eq a => [a] -> [a]
removeDuplicates [] = []
removeDuplicates (x:xs)
    | x `elem` xsResult = xsResult      -- 如果 x 已经在结果列表中，则跳过 x
    | otherwise = x : xsResult          -- 如果 x 不在结果列表中，则保留 x
    where xsResult = removeDuplicates xs
```

### 代码解释

- **`removeDuplicates [] = []`**：空列表没有重复元素，直接返回空列表。
- **`removeDuplicates (x:xs)`**：对于非空列表 `(x:xs)`，我们检查 `x` 是否在已经处理的结果 `xsResult` 中。
  - **`x \`elem\` xsResult`**：检查 `x` 是否在结果列表中。`elem` 用于检查当前元素是否已经在去重后的结果列表中出现过。
    
    - 如果 `x` 在结果列表 `xsResult` 中，直接返回 `xsResult`。
    - 如果 `x` 不在 `xsResult` 中，则将 `x` 添加到结果的开头。
    
  - ### 为什么不能用 `map`
  
    `map` 只能对每个元素进行相同的操作，无法根据**是否已存在于结果列表**来决定是添加还是跳过某个元素。而 `removeDuplicates` 需要在遍历列表的同时，动态维护一个不重复的结果列表，这不是 `map` 的用途和能力范围。
  
    ### `elem` 的作用
  
    在 `removeDuplicates` 的递归定义中，`elem` 的作用是**检查当前元素是否在结果列表中**。这一步是 `removeDuplicates` 的核心逻辑，用来决定是否将元素添加到结果中。由于 `elem` 可以检查列表中是否包含特定元素，因此它非常适合于去重操作。
  
  - **`where xsResult = removeDuplicates xs`**：定义了 `xsResult` 是 `removeDuplicates xs` 的结果，即对剩余元素的去重结果。

### 示例测试

```haskell
removeDuplicates [1, 2, 2, 3, 4, 4, 5]
-- 结果: [1, 2, 3, 4, 5]

removeDuplicates "mississippi"
-- 结果: "misp"
```

### 总结

- **`removeDuplicates`** 通过递归处理列表的每个元素，保留首次出现，跳过重复项。
- 这种方法的关键是使用 `elem` 检查元素是否已经在结果中，从而实现去重。























#### Question 2: Haskell Map and Filter [15 marks]

Define a Haskell function `squareOdds :: [Int] -> [Int]` that squares each odd number in a list and leaves even numbers unchanged.

For example:
```haskell
squareOdds [1, 2, 3, 4] = [1, 2, 9, 4]
squareOdds [2, 4, 6] = [2, 4, 6]
```

---



这个问题要求我们定义一个 Haskell 函数 `squareOdds`，它将列表中的奇数元素平方，保持偶数元素不变。

### 题目分析

- **`squareOdds :: [Int] -> [Int]`**：函数接受一个整数列表 `[Int]`，返回一个新的整数列表 `[Int]`。
- **功能要求**：对于每个元素，如果它是奇数，则将其平方；如果是偶数，则保持不变。

例如：
- `squareOdds [1, 2, 3, 4]` 的结果应该是 `[1, 2, 9, 4]`：
  - 1 是奇数，所以平方得到 1。
  - 2 是偶数，所以保持不变。
  - 3 是奇数，所以平方得到 9。
  - 4 是偶数，所以保持不变。
  
- `squareOdds [2, 4, 6]` 的结果是 `[2, 4, 6]`，因为所有元素都是偶数，没有变化。

### 解决方案

我们可以用 `map` 函数来实现，因为 `map` 可以对列表中的每个元素应用一个函数。在这里，我们将定义一个函数 `squareIfOdd`，它检查元素是否为奇数。如果是奇数，则返回该数的平方；否则，返回原值。

```haskell
squareOdds :: [Int] -> [Int]
squareOdds = map squareIfOdd
  where
    squareIfOdd x
      | odd x     = x * x  -- 如果 x 是奇数，则返回 x 的平方
      | otherwise = x      -- 如果 x 是偶数，则返回原值
```

### 代码解释

- **`squareOdds = map squareIfOdd`**：使用 `map` 将函数 `squareIfOdd` 应用到列表中的每个元素。
- **`squareIfOdd x`**：这是一个内部函数，用于检查 `x` 是否为奇数。
  - **`odd x`**：判断 `x` 是否为奇数。
  - 如果 `x` 是奇数，则返回 `x * x`，即 `x` 的平方。
  - 如果 `x` 是偶数，则返回原值 `x`。

### 示例测试

```haskell
squareOdds [1, 2, 3, 4]
-- 结果: [1, 2, 9, 4]

squareOdds [2, 4, 6]
-- 结果: [2, 4, 6]
```

### 进一步解释

在 `squareIfOdd` 中，我们使用了一个**守卫（guard）**来检查 `x` 是否为奇数。`odd x` 返回一个布尔值：
- 如果 `odd x` 为 `True`（即 `x` 是奇数），返回 `x * x`。
- 如果 `odd x` 为 `False`（即 `x` 是偶数），返回 `x`。

`map` 会对列表中的每个元素调用 `squareIfOdd`，因此整个列表中的奇数将被平方，而偶数保持不变。

---

### 总结

- `squareOdds` 使用 `map` 和一个内部函数 `squareIfOdd`，对列表中的每个元素进行检查。
- 奇数会被平方，偶数保持原值，从而实现题目要求的功能。

















#### Question 3: Haskell Trees [20 marks]

Using the following binary tree definition:
```haskell
data Tree a = Empty | Node a (Tree a) (Tree a)
```

Write a Haskell function `treeProduct :: Num a => Tree a -> a` that calculates the product of all values in the tree. Return 1 if the tree is empty.

For example:
```haskell
treeProduct (Node 2 (Node 3 Empty Empty) (Node 4 Empty Empty)) = 24
treeProduct Empty = 1
```

---

这道题目要求我们定义一个函数 `treeProduct`，用于计算二叉树中所有节点值的乘积，并在树为空时返回 1。

### 题目解析

- **`data Tree a = Empty | Node a (Tree a) (Tree a)`**：这段代码定义了一个二叉树数据类型 `Tree`，其中每个节点包含一个值和左右子树。
  - `Empty`：表示空树。
  - `Node a (Tree a) (Tree a)`：表示一个包含值 `a` 的节点，以及左子树和右子树（这两个子树本身也是 `Tree a` 类型）。
  
- **`treeProduct` 函数**：
  - 类型签名为 `Num a => Tree a -> a`，表示该函数接受一个类型为 `Tree a` 的树，并返回一个数值类型 `a`。
  - 目标是计算树中所有节点值的乘积。如果树是空的，返回 1。

### 示例

给定树结构 `Node 2 (Node 3 Empty Empty) (Node 4 Empty Empty)`，树的结构如下：

```
      2
     / \
    3   4
```

- `treeProduct` 应该计算所有节点值的乘积，即 `2 * 3 * 4 = 24`。
- 如果树是 `Empty`，则返回 1。

### 代码实现

我们可以使用递归实现 `treeProduct`。逻辑如下：

1. 如果树是 `Empty`，返回 1。
2. 如果树是一个 `Node`，则返回当前节点值乘以左右子树的乘积。

代码如下：

```haskell
treeProduct :: Num a => Tree a -> a
treeProduct Empty = 1
treeProduct (Node value left right) = value * treeProduct left * treeProduct right
```

### 代码解释

- **`treeProduct Empty = 1`**：如果树是空的，则乘积为 1。
- **`treeProduct (Node value left right) = value * treeProduct left * treeProduct right`**：
  - 如果树是一个节点 `Node`，我们递归地计算左右子树的乘积。
  - 将当前节点的值 `value` 与左右子树的乘积相乘，得到整个树的乘积。

### 示例测试

```haskell
treeProduct (Node 2 (Node 3 Empty Empty) (Node 4 Empty Empty))
-- 结果: 24，因为 2 * 3 * 4 = 24

treeProduct Empty
-- 结果: 1，因为空树的乘积定义为 1
```

### 总结

- `treeProduct` 通过递归遍历树的每个节点，将节点值相乘得到总乘积。
- 空树返回 1，非空树计算每个节点值的乘积。





















#### Question 4: Prolog List Membership [15 marks]

Define a Prolog predicate `contains_duplicates(L)` that succeeds if a list `L` contains any duplicate elements.

For example:
```haskell
?- contains_duplicates([1, 2, 3, 4]).
false.

?- contains_duplicates([1, 2, 2, 3]).
true.
```

---

这个题目要求我们在 Prolog 中定义一个谓词 `contains_duplicates(L)`，它的作用是**检查列表 `L` 中是否包含重复的元素**。如果 `L` 中存在任何重复元素，则谓词 `contains_duplicates(L)` 成功；否则，失败。

### 题目分析

- `contains_duplicates(L)` 的目标是判断列表 `L` 中是否有两个或更多相同的元素。
- **示例**：
  - `contains_duplicates([1, 2, 3, 4])` 应返回 `false`，因为所有元素都是唯一的。
  - `contains_duplicates([1, 2, 2, 3])` 应返回 `true`，因为列表中有两个 `2`，表示存在重复。

### 解决方案

在 Prolog 中，我们可以通过递归来实现这个谓词。基本逻辑是：
1. 对于列表中的每个元素，检查它是否出现在列表的其余部分中。
2. 如果元素存在于其余部分中，则列表包含重复项，谓词成功。
3. 如果当前元素没有出现在剩余部分中，则继续检查列表的下一个元素。

#### 实现步骤

1. 如果列表为空或只有一个元素，那么不可能有重复项。
2. 对于非空列表 `(H|T)`，检查 `H` 是否在 `T` 中：
   - 如果 `H` 在 `T` 中，则存在重复元素，谓词成功。
   - 如果 `H` 不在 `T` 中，递归调用 `contains_duplicates(T)` 检查 `T` 是否有重复项。

#### 代码实现

```haskell
% 基本情况：空列表或只有一个元素的列表不包含重复项
contains_duplicates([]) :- false.
contains_duplicates([_]) :- false.

% 检查列表的第一个元素 H 是否出现在 T 中
contains_duplicates([H|T]) :-
    member(H, T), !.                % 如果 H 在 T 中，则包含重复项
contains_duplicates([_|T]) :-
    contains_duplicates(T).         % 否则，递归检查 T
```

#### 代码解释

- **`contains_duplicates([]) :- false.`** 和 **`contains_duplicates([_]) :- false.`**：
  
- 如果列表为空或只有一个元素，则不可能有重复项，直接返回 `false`。
  
- **`contains_duplicates([H|T]) :- member(H, T), !.`**：
  
  - 对于非空列表 `[H|T]`，我们使用 `member(H, T)` 检查 `H` 是否出现在列表 `T` 中。

  - 如果 `member(H, T)` 成功，则表示 `H` 是重复元素，我们使用剪枝操作 `!` 来立即返回 `true`。
  
  - > 这行代码：
    >
    > ```prolog
    > contains_duplicates([H|T]) :- member(H, T), !.
    > ```
    >
    > 是 Prolog 中 `contains_duplicates` 谓词的一个规则，用于检查列表中是否包含重复元素。我们逐步解释其含义：
    >
    > ### 1. 模式匹配 `[H|T]`
    >
    > 在 Prolog 中，`[H|T]` 是一种**模式匹配**的表示法，用于将列表拆分为**头部元素** `H` 和**尾部列表** `T`。例如，对于列表 `[1, 2, 3]`：
    >
    > - `H` 匹配第一个元素 `1`。
    > - `T` 匹配剩余的列表 `[2, 3]`。
    >
    > 因此，`contains_duplicates([H|T])` 表示我们正在检查一个非空列表 `[H|T]` 是否包含重复元素，`H` 是当前元素，`T` 是剩余部分。
    >
    > ### 2. `member(H, T)`
    >
    > - `member/2` 是 Prolog 的一个内置谓词，用于检查一个元素是否属于某个列表。
    > - `member(H, T)` 的意思是**检查 `H` 是否出现在列表 `T` 中**。
    >   
    >
    > 如果 `H` 在 `T` 中，那么 `H` 就是一个重复元素，因为它在当前列表的其余部分中又出现了一次。
    >
    > ### 3. `!` （剪枝操作）
    >
    > - `!` 是 Prolog 中的**剪枝（cut）**操作符。
    > - `!` 的作用是：当程序执行到剪枝操作时，即使后续存在其他匹配的规则或解，Prolog 也会**停止回溯**，并直接返回当前结果。
    >
    > 在这里，`!` 表示**一旦找到重复元素 `H`，立即停止搜索并返回结果**，不用继续检查其他元素。
    >
    > ### 组合解释
    >
    > ```prolog
    > contains_duplicates([H|T]) :- member(H, T), !.
    > ```
    >
    > 的完整含义是：
    >
    > - 首先，将列表 `[H|T]` 拆分成头部元素 `H` 和尾部列表 `T`。
    > - 然后，使用 `member(H, T)` 检查 `H` 是否出现在 `T` 中。
    >   - 如果 `member(H, T)` 为 `true`（表示 `H` 在 `T` 中出现了），则表示列表包含重复元素。
    >   - 此时，执行剪枝 `!`，立即停止搜索并返回 `true`。
    >
    > ### 例子
    >
    > 假设我们调用 `contains_duplicates([1, 2, 2, 3])`：
    >
    > 1. `[H|T]` 匹配 `[1, 2, 2, 3]`，其中 `H = 1` 和 `T = [2, 2, 3]`。
    > 2. `member(1, [2, 2, 3])` 检查 `1` 是否在 `[2, 2, 3]` 中，返回 `false`，所以继续下一步。
    > 3. 下一次递归调用 `contains_duplicates([2, 2, 3])`，此时 `H = 2`，`T = [2, 3]`。
    > 4. `member(2, [2, 3])` 返回 `true`，因为 `2` 在 `T` 中找到了。
    > 5. 剪枝 `!` 执行，停止搜索，返回 `true`，表示列表中存在重复元素。
  
- **`contains_duplicates([_|T]) :- contains_duplicates(T).`**：
  
  - 如果 `H` 不在 `T` 中，则递归调用 `contains_duplicates(T)` 检查列表的其余部分 `T` 是否包含重复项。
  
  - > 这一行代码：
    >
    > ```prolog
    > contains_duplicates([_|T]) :- contains_duplicates(T).
    > ```
    >
    > 是 `contains_duplicates` 谓词的一个递归规则，用于在未找到重复元素时继续检查列表的其余部分。我们逐步解释其含义：
    >
    > ### 1. 模式匹配 `[_|T]`
    >
    > 在 Prolog 中，`[_|T]` 的模式匹配表示：
    > - 使用 `_` 匹配列表的第一个元素，但不关心该元素是什么（因此使用匿名变量 `_`）。
    > - `T` 是列表的尾部，即去掉第一个元素后的剩余部分。
    >
    > 因此，`contains_duplicates([_|T])` 的作用是：**当第一个元素检查完成且不包含重复时，递归地检查列表 `T` 是否包含重复元素**。
    >
    > ### 2. 递归调用 `contains_duplicates(T)`
    >
    > - `contains_duplicates(T)` 是对列表 `T` 的递归调用。
    > - 如果当前的第一个元素（在上一行代码中表示为 `H`）不重复（即不在 `T` 中），则 `contains_duplicates(T)` 会递归检查剩余列表 `T` 是否包含重复元素。
    >
    > ### 组合解释
    >
    > ```prolog
    > contains_duplicates([_|T]) :- contains_duplicates(T).
    > ```
    >
    > 的完整含义是：
    >
    > - 如果当前的第一个元素已经检查过且不包含重复，则忽略当前元素 `_`，递归检查剩余列表 `T` 是否包含重复元素。
    > - 这个规则只会在没有找到重复元素的情况下被执行。如果前面的规则 `contains_duplicates([H|T]) :- member(H, T), !.` 找到了重复元素，程序将不会执行这个递归规则。
    >
    > ### 例子
    >
    > 假设我们调用 `contains_duplicates([1, 2, 3, 4])`：
    >
    > 1. 首先，`[H|T]` 匹配 `[1, 2, 3, 4]`，其中 `H = 1`，`T = [2, 3, 4]`。
    > 2. 检查 `member(1, [2, 3, 4])`，结果是 `false`，所以没有找到重复元素。
    > 3. 执行 `contains_duplicates([_|T]) :- contains_duplicates(T)`，忽略当前元素 `1`，递归检查 `contains_duplicates([2, 3, 4])`。
    >    
    >    - 对 `[2, 3, 4]` 重复相同步骤，检查是否有重复元素。
    >    - 当 `T` 递归到 `[]` 或 `[_]` 时，表示没有重复元素，因此返回 `false`。
    >
    > 这条递归规则确保 `contains_duplicates` 在整个列表检查完之前不断地递归向下进行检查，以发现可能的重复项。

#### 示例测试

```prolog
?- contains_duplicates([1, 2, 3, 4]).
false.

?- contains_duplicates([1, 2, 2, 3]).
true.

?- contains_duplicates([a, b, c, a]).
true.
```

### 总结

- `contains_duplicates(L)` 使用递归来遍历列表 `L` 中的每个元素，检查是否有重复项。
- `member/2` 谓词用于检查元素是否出现在列表的其余部分中。
- 剪枝操作 `!` 用于一旦发现重复项立即返回。



















#### Question 5: Prolog List Manipulation [20 marks]

Define a Prolog predicate `split_even_odd(L, Evens, Odds)` that splits a list `L` into two lists: `Evens` for even numbers and `Odds` for odd numbers.

For example:
```prolog
?- split_even_odd([1, 2, 3, 4, 5, 6], Evens, Odds).
Evens = [2, 4, 6],
Odds = [1, 3, 5].
```

---

这道题目要求我们定义一个 Prolog 谓词 `split_even_odd(L, Evens, Odds)`，它的作用是将一个列表 `L` 拆分为两个列表：
- `Evens`：包含 `L` 中的所有偶数。
- `Odds`：包含 `L` 中的所有奇数。

### 题目分析

例如，调用：
```prolog
?- split_even_odd([1, 2, 3, 4, 5, 6], Evens, Odds).
```

应返回：
```prolog
Evens = [2, 4, 6],
Odds = [1, 3, 5].
```

在这个示例中，`split_even_odd` 将列表 `[1, 2, 3, 4, 5, 6]` 中的偶数（`2, 4, 6`）放到 `Evens` 列表中，将奇数（`1, 3, 5`）放到 `Odds` 列表中。

### 解决方案

我们可以通过递归来实现这个功能。基本逻辑如下：

1. **基准情况**：如果列表为空（`L = []`），那么 `Evens` 和 `Odds` 也都是空列表。
2. **递归情况**：
   - 对于非空列表 `[H|T]`：
     - 如果 `H` 是偶数，则将 `H` 添加到 `Evens` 列表的开头，递归处理尾部 `T`。
     - 如果 `H` 是奇数，则将 `H` 添加到 `Odds` 列表的开头，递归处理尾部 `T`。

### 判断偶数和奇数

我们可以使用 `0 is H mod 2` 判断 `H` 是否是偶数：
- `H mod 2` 是 `0` 表示 `H` 是偶数。
- 否则 `H` 是奇数。

### 代码实现

```prolog
% 基本情况：空列表的偶数和奇数列表都是空列表
split_even_odd([], [], []).

% 递归情况：处理非空列表 [H|T]
split_even_odd([H|T], [H|Evens], Odds) :-
    0 is H mod 2,              % 如果 H 是偶数
    split_even_odd(T, Evens, Odds). % 递归处理剩余部分

split_even_odd([H|T], Evens, [H|Odds]) :-
    1 is H mod 2,              % 如果 H 是奇数
    split_even_odd(T, Evens, Odds). % 递归处理剩余部分
```

### 代码解释

1. **基准情况**：
   - `split_even_odd([], [], [])`：如果列表 `L` 是空列表 `[]`，那么 `Evens` 和 `Odds` 也都是空列表。这是递归的终止条件。
- 符号 **`:-`** 是一个**定义规则的符号**，表示“如果”（类似于逻辑中的“蕴涵”符号）。它用于定义一个谓词的**条件**。
   
2. **递归情况**：
   - `split_even_odd([H|T], [H|Evens], Odds) :- 0 is H mod 2, split_even_odd(T, Evens, Odds)`：
     - 如果 `H` 是偶数（`0 is H mod 2`），则将 `H` 添加到 `Evens` 列表的开头，并递归处理剩余的列表 `T`。
   - `split_even_odd([H|T], Evens, [H|Odds]) :- 1 is H mod 2, split_even_odd(T, Evens, Odds)`：
     - 如果 `H` 是奇数（`1 is H mod 2`），则将 `H` 添加到 `Odds` 列表的开头，并递归处理剩余的列表 `T`。

### 示例测试

```prolog
?- split_even_odd([1, 2, 3, 4, 5, 6], Evens, Odds).
Evens = [2, 4, 6],
Odds = [1, 3, 5].

?- split_even_odd([7, 10, 15, 20], Evens, Odds).
Evens = [10, 20],
Odds = [7, 15].

?- split_even_odd([], Evens, Odds).
Evens = [],
Odds = [].
```

### 总结

- `split_even_odd` 使用递归和模式匹配将列表 `L` 中的元素分为偶数列表和奇数列表。
- `mod` 操作用于判断元素的奇偶性，将偶数添加到 `Evens` 列表，将奇数添加到 `Odds` 列表。















#### Question 6: Haskell Higher-Order Functions [15 marks]

Define a Haskell function `applyTwice :: (a -> a) -> a -> a` that applies a given function twice to an argument.

For example:
```haskell
applyTwice (+3) 7 = 13
applyTwice (*2) 4 = 16
```

---

这道题目要求我们定义一个 Haskell 函数 `applyTwice`，它接受一个函数和一个参数，然后将这个函数**应用两次**于该参数。

### 题目解析

- **函数类型**：`applyTwice :: (a -> a) -> a -> a`
  - **`(a -> a)`**：第一个参数是一个函数，该函数接受一个类型 `a` 的参数并返回一个相同类型 `a` 的值。
  - **`a`**：第二个参数是初始值，类型为 `a`。
  - 返回值类型是 `a`，表示对第二个参数应用两次给定函数后的结果。

- **功能要求**：
  - `applyTwice` 的作用是将给定函数 `f` 应用于初始值 `x` 两次，即 `f (f x)`。

### 示例分析

- `applyTwice (+3) 7`
  - 首先将 `+3` 应用于 `7`，得到 `10`。
  - 然后再次将 `+3` 应用于 `10`，得到 `13`。
  - 最终结果是 `13`。

- `applyTwice (*2) 4`
  - 首先将 `*2` 应用于 `4`，得到 `8`。
  - 然后再次将 `*2` 应用于 `8`，得到 `16`。
  - 最终结果是 `16`。

### 代码实现

我们可以直接用函数组合的方式实现 `applyTwice`：

```haskell
applyTwice :: (a -> a) -> a -> a
applyTwice f x = f (f x)
```

### 代码解释

- **`applyTwice f x = f (f x)`**：
  - 这个定义表示将 `f` 应用于 `x`，得到 `f x` 的结果，再将 `f` 应用一次，得到最终结果 `f (f x)`。
  - 整体上就是对 `x` 应用 `f` 两次。

### 示例测试

```haskell
applyTwice (+3) 7
-- 结果: 13，因为 (+3) 应用于 7 得到 10，再次应用得到 13

applyTwice (*2) 4
-- 结果: 16，因为 (*2) 应用于 4 得到 8，再次应用得到 16
```

### 总结

- **`applyTwice`** 是一个高阶函数，它接收一个函数和一个值，将该函数应用于值两次。
- 这种设计常用于函数的组合操作，提供了简洁的方式来处理需要多次应用同一函数的场景。















#### Question 7: Prolog Tree Depth [15 marks]

Using the following tree structure in Prolog:
```prolog
tree(nil).
tree(node(Left, Value, Right)) :- tree(Left), tree(Right).
```

Define a Prolog predicate `max_depth(Tree, Depth)` that calculates the maximum depth of a binary tree `Tree`.

For example:
```prolog
?- max_depth(node(node(nil, 1, nil), 2, node(nil, 3, nil)), Depth).
Depth = 2.
```

这道题目要求我们定义一个 Prolog 谓词 `max_depth(Tree, Depth)`，用于计算二叉树 `Tree` 的最大深度（高度），并将结果存储在 `Depth` 中。

### 题目分析

- 二叉树结构定义为：
  ```prolog
  tree(nil).
  tree(node(Left, Value, Right)) :- tree(Left), tree(Right).
  ```
  - `nil` 表示一个空树。
  - `node(Left, Value, Right)` 表示一个节点，包含：
    - `Left`：左子树。
    - `Value`：当前节点的值。
    - `Right`：右子树。

- **目标**：定义 `max_depth(Tree, Depth)`，计算树 `Tree` 的最大深度。
  - 最大深度是指从根节点到最远叶节点的路径长度（节点数）。
  - 空树的深度为 0。
  - 非空树的深度等于 1 加上左右子树的最大深度。

### 递归实现思路

可以用递归方法来计算树的深度：
1. **基准情况**：如果树是 `nil`（空树），深度为 0。
2. **递归情况**：如果树是 `node(Left, _, Right)`，则计算左子树和右子树的深度。
   - 树的最大深度是 `1 + max(LeftDepth, RightDepth)`，其中 `LeftDepth` 和 `RightDepth` 分别是左右子树的最大深度。

### 代码实现

我们可以定义 `max_depth` 谓词如下：

```prolog
% 空树的深度为 0
max_depth(nil, 0).

% 非空节点的深度为左右子树深度的最大值加 1
max_depth(node(Left, _, Right), Depth) :-
    max_depth(Left, LeftDepth),         % 计算左子树的深度
    max_depth(Right, RightDepth),       % 计算右子树的深度
    Depth is max(LeftDepth, RightDepth) + 1. % 当前节点的深度
```

### 代码解释

- **`max_depth(nil, 0)`**：定义空树的深度为 0。
- **`max_depth(node(Left, _, Right), Depth)`**：
  - 递归调用 `max_depth(Left, LeftDepth)` 计算左子树的深度。
  - 递归调用 `max_depth(Right, RightDepth)` 计算右子树的深度。
  - 使用 `max(LeftDepth, RightDepth) + 1` 来计算当前树的深度：
    - `max(LeftDepth, RightDepth)` 找出左右子树的较大深度。
    - `+ 1` 是为了包括当前节点的深度。

### 示例测试

```prolog
?- max_depth(node(node(nil, 1, nil), 2, node(nil, 3, nil)), Depth).
Depth = 2.

% 树的结构：
%       2
%      / \
%     1   3
% 最大深度为 2
```

### 总结

- `max_depth(Tree, Depth)` 使用递归计算树的深度：
  - 空树的深度为 0。
  - 非空树的深度为左右子树最大深度加 1。
- 这个递归定义确保了从根节点到底部的所有路径都被正确地计算出来，找到最大深度。