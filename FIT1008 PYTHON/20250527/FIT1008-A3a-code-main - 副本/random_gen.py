以下是你提供的 `RandomGen` 随机数生成类的代码，我已经为你**逐行添加中文注释**，并将所有英文文档字符串（docstring）翻译为中文，适合用于作业提交或进一步学习使用：

---

````python
"""
随机数生成器类。使用线性同余生成器（LCG）方法，并进行了合理的初始化。
"""
__author__ = "Jackson Goerner"

import time  # 用于生成默认种子值（当前时间）

class RandomGen:
    """
    这个类用于生成（可设定种子）随机数，适用于测试中可重复的结果。

    使用的是线性同余生成器（LCG）算法。
    除非特别说明，所有方法的时间复杂度都是 O(1)。

    用法示例：
    ```
    RandomGen.set_seed(123)
    RandomGen.random()             # 返回一个 0 到 2^32-1 的随机整数
    RandomGen.randint(1, 10)       # 返回一个 1 到 10（包含）的随机整数
    RandomGen.random_chance(0.33)  # 以 33% 概率返回 True，67% 概率返回 False
    ```
    """

    MOD: int = pow(2, 48)  # 模数，用于保持种子在合理范围内
    A: int = 25214903917   # 乘数
    C: int = 11            # 增量项（常数项）

    seed = time.time_ns()  # 默认使用当前时间（纳秒）作为初始种子

    @classmethod
    def set_seed(cls, seed: int = None) -> None:
        """
        设置随机数生成的种子。
        若不提供参数，则默认使用当前时间戳（纳秒）作为种子。
        """
        seed = time.time_ns() if seed is None else seed
        cls.seed = seed

    @classmethod
    def random(cls) -> int:
        """
        返回一个范围在 0 到 2^32-1 的随机整数。
        本质上是生成新的种子并右移 16 位得到 32 位整数。
        """
        cls.seed = (cls.A * cls.seed + cls.C) % cls.MOD
        return cls.seed >> 16  # 使用高位部分提高随机性

    @classmethod
    def random_float(cls) -> float:
        """
        返回一个 [0, 1) 区间的浮点随机数。
        """
        return cls.random() / (1 << 32)

    @classmethod
    def randint(cls, lo: int, hi: int) -> int:
        """
        返回一个 [lo, hi] 区间的随机整数（闭区间）。
        """
        return (cls.random() % (hi - lo + 1)) + lo

    @classmethod
    def random_chance(cls, ratio: float) -> bool:
        """
        返回 True 的概率为 ratio，例如 ratio=0.3 表示 30% 概率返回 True。
        本质是比较随机小数与 ratio 的大小。
        """
        return cls.random_float() < ratio

    @classmethod
    def random_choice(cls, collection) -> None:
        """
        从一个支持 __getitem__ 和 __len__ 的容器中随机返回一个元素。
        例如列表、元组等。
        """
        return collection[cls.randint(0, len(collection) - 1)]

    @classmethod
    def random_shuffle(cls, collection) -> None:
        """
        随机打乱一个集合中的元素顺序（支持 __getitem__、__setitem__、__len__）

        时间复杂度：
            O(len(collection)) — 由于每个元素都要重排一次
        """
        # 为每个元素生成一个随机数，并和其索引配对
        positions = [(RandomGen.random(), i) for i in range(len(collection))]
        positions.sort()  # 按随机值排序 — 这里允许使用内置 sort（其他地方禁止）

        # 根据排序后的索引构建新的排列
        tmp = [collection[p[1]] for p in positions]

        # 用新顺序覆盖原集合
        for x in range(len(collection)):
            collection[x] = tmp[x]
````

---

这个类会在整个作业中用于生成伪随机行为（比如鸡骑士打乱顺序），它用 LCG 算法模拟随机性，可设置种子确保测试可重复。

如你需要我继续帮你实现使用它的代码（如 `dfs_explore_cave` 或 `objective_mining`），欢迎继续发起。需要我补全其它部分吗？
