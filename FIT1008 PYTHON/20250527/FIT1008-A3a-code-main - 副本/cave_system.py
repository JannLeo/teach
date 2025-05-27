当然可以，以下是你提供的 `CaveNode` 和 `CaveSystem` 类的代码，已经**逐行添加中文注释**，并将所有英文注释/说明转换为中文说明：

---

```python
from __future__ import annotations  # 允许使用前向引用，即可以在类中使用尚未定义的类型

from data_structures import List, ArrayList  # 导入课程自定义的数据结构
from minecraft_block import MinecraftBlock  # 导入矿石类

class CaveNode:
    """
    表示一个矿洞节点的类。
    """

    def __init__(self, blocks: ArrayList[MinecraftBlock] = None, name: str = None) -> None:
        """
        初始化一个 CaveNode 实例，包含矿石的列表。

        参数:
            blocks (list): 节点中包含的矿石列表。
            name (str): 节点名称。

        时间复杂度:
            最好情况：O(1)
            最坏情况：O(1)

        复杂度说明:
            初始化过程不依赖于输入大小，因此复杂度为常数。
        """
        self.name = name  # 节点名称，用于调试或识别
        self.blocks = blocks if blocks else ArrayList()  # 节点中的矿石列表，若无传入则初始化为空
        self.neighbours = ArrayList()  # 存储该节点连接的邻居节点

    def connect(self, other_node: 'CaveNode') -> None:
        """
        将当前节点与另一个节点连接（无向连接）。

        参数:
            other_node (CaveNode): 要连接的另一个 CaveNode 节点。

        时间复杂度:
            最好情况：O(1)
            最坏情况：O(N)，其中 N 是邻接节点数量

        复杂度说明:
            添加操作本身是常数时间，
            但如果邻居列表需要扩容（如使用动态数组），则最坏为 O(N)。
        """
        self.neighbours.append(other_node)  # 添加邻居
        other_node.neighbours.append(self)  # 双向连接（无向图）

    def __str__(self) -> str:
        """
        返回 CaveNode 的字符串表示。

        返回:
            str: 字符串表示形式。

        时间复杂度:
            最好情况：O(1)
            最坏情况：O(1)

        复杂度说明:
            格式化字符串过程不依赖于 blocks 或 neighbours 的具体大小。
        """
        return f"CaveNode(name={self.name}, blocks={self.blocks}, neighbours={len(self.neighbours)})"


class CaveSystem:
    """
    表示整个矿洞系统的类。
    """

    def __init__(self, cave_node: CaveNode, number_of_nodes: int) -> None:
        """
        初始化矿洞系统。

        参数:
            cave_node (CaveNode): 矿洞系统的入口节点。
            number_of_nodes (int): 系统中独立节点的总数。
        """
        self.entrance = cave_node  # 矿洞入口（起点）
        self.number_of_nodes = number_of_nodes  # 总节点数

    def __len__(self) -> int:
        """
        返回矿洞系统中的节点总数。

        返回:
            int: 节点数。

        时间复杂度:
            最好情况：O(1)
            最坏情况：O(1)
        """
        return self.number_of_nodes

    def __str__(self) -> str:
        """
        返回矿洞系统的字符串表示。

        返回:
            str: 字符串表示形式。

        时间复杂度:
            最好情况：O(1)
            最坏情况：O(1)
        """
        return f"CaveSystem(entrance={self.entrance}, number_of_nodes={self.number_of_nodes})"
```

---

这段代码的功能已经非常清晰了，并且符合你作业中的 `CaveSystem` 与 `CaveNode` 结构说明。如果你还需要我帮你实现遍历（例如 DFS）、矿石收集、排序过滤等操作，也可以告诉我下一步的目标。是否继续？
