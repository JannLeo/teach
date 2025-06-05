import sys

INF = 9999  # "Infinity" for unreachable routes

DEBUG = True  # Set to False to disable debug prints
# 定义一个debug函数，用于打印调试信息
def debug(msg):
    # 如果DEBUG为True，则打印调试信息
    if DEBUG:
        print("[DEBUG]", msg)

class Router:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}  # direct neighbors and link cost
        self.dist_table = {}  # distance table: who told what about whom
        self.routes = {}  # current best route {dest: (nexthop, cost)}

    def initialize(self, all_nodes):
        # 初始化距离表和路由表
        self.dist_table = {}
        self.routes = {}
        self.dist_table[self.name] = {}
        # 遍历所有节点
        for dest in all_nodes:
            # 如果节点是自身，则跳过
            if dest == self.name:
                continue
            # 如果节点是邻居节点，则更新距离表和路由表
            if dest in self.neighbors:
                self.dist_table[self.name][dest] = self.neighbors[dest]
                self.routes[dest] = (dest, self.neighbors[dest])
            # 如果节点不是邻居节点，则将距离表和路由表初始化为无穷大
            else:
                self.dist_table[self.name][dest] = INF
                self.routes[dest] = (None, INF)
        # 遍历所有邻居节点
        for neighbor in self.neighbors:
            self.dist_table[neighbor] = {}
            # 遍历所有节点
            for dest in all_nodes:
                # 如果节点不是自身，则将距离表初始化为无穷大
                if dest != self.name:
                    self.dist_table[neighbor][dest] = INF

    def get_poisoned_vector(self, to_neighbor):
        # 获取被毒化的向量
        vector = {}
        for dest, (nexthop, cost) in self.routes.items():
            if dest == to_neighbor:
                vector[dest] = cost  # direct neighbor, must send valid info
            elif nexthop == to_neighbor:
                vector[dest] = INF  # poison reverse
            else:
                vector[dest] = cost
        return vector

    def receive(self, neighbor, vector):
        # 接收向量
        debug(f"{self.name} 从 {neighbor} 接收到向量: {vector}")
        # 如果邻居不在距离表中，则添加邻居
        if neighbor not in self.dist_table:
            self.dist_table[neighbor] = {}
        # 遍历向量中的每个目的节点
        for dest in vector:
            # 将邻居和目的节点添加到距离表中
            self.dist_table[neighbor][dest] = vector[dest]

    def update_routes(self):
        # 更新路由表
        updated = False
        for dest in self.routes:
            min_cost = INF
            min_hop = None
            # 遍历邻居节点
            for neighbor in sorted(self.neighbors):
                cost_to_neighbor = self.neighbors[neighbor]
                # 获取邻居节点到目的地的距离
                cost_from_neighbor = self.dist_table.get(neighbor, {}).get(dest, INF)
                # 计算总距离
                total = cost_to_neighbor + cost_from_neighbor
                # 如果总距离小于最小距离，或者总距离等于最小距离且邻居节点小于最小跳数
                if total < min_cost or (total == min_cost and (min_hop is None or neighbor < min_hop)):
                    min_cost = total
                    min_hop = neighbor
            # 如果最小跳数和最小距离与当前路由表中的不同
            if (min_hop, min_cost) != self.routes[dest]:
                # 打印更新信息
                debug(f"{self.name} 更新路由: {dest} 从 {self.routes[dest]} → ({min_hop},{min_cost})")
                # 更新路由表
                self.routes[dest] = (min_hop, min_cost)
                updated = True
        # 遍历路由表中的目的地
        for dest in self.routes:
            # 如果目的地不在邻居节点中
            if dest not in self.neighbors:
                # 更新距离表
                self.dist_table[self.name][dest] = self.routes[dest][1]
        # 返回是否更新了路由表
        return updated

    def print_distance_table(self, t, all_nodes):
        # 打印距离表
        dests = sorted(n for n in all_nodes if n != self.name)  # 对所有节点进行排序，除了自己
        neighbors = sorted(self.dist_table.keys())  # 对邻居节点进行排序
        print(f"Distance Table of router {self.name} at t={t}:")  # 打印距离表标题
        print("     " + "    ".join(dests))  # 打印目标节点
        for n in neighbors:  # 遍历邻居节点
            row = [n]  # 将邻居节点作为行首
            for d in dests:  # 遍历目标节点
                val = self.dist_table[n].get(d, INF)  # 获取邻居节点到目标节点的距离
                row.append("INF" if val >= INF else str(val))  # 如果距离大于等于无穷大，则打印INF，否则打印距离
            print("    ".join(row))  # 打印行
        print("")  # 打印空行

    def print_routing_table(self):
        # 打印路由表
        print(f"Routing Table of router {self.name}:")
        for dest in sorted(self.routes.keys()):
            hop, cost = self.routes[dest]
            cost_str = "INF" if cost >= INF else str(cost)
            print(f"{dest},{hop},{cost_str}")
        print("")

def parse_input():
    # 打开input.txt文件，以只读模式读取，编码格式为utf-8
    with open("input.txt", "r", encoding="utf-8") as f:
        # 将文件中的每一行去除首尾空格，并去除空行
        lines = [line.strip() for line in f if line.strip()]
    i = 0
    routers = []
    # 读取路由器信息，直到遇到"START"关键字
    while i < len(lines) and lines[i] != "START":
        routers.append(lines[i])
        i += 1
    i += 1
    links = []
    # 读取链接信息，直到遇到"UPDATE"关键字
    while i < len(lines) and lines[i] != "UPDATE":
        a, b, c = lines[i].split()
        links.append((a, b, int(c)))
        i += 1
    i += 1
    updates = []
    # 读取更新信息，直到遇到"END"关键字
    while i < len(lines) and lines[i] != "END":
        a, b, c = lines[i].split()
        updates.append((a, b, int(c)))
        i += 1
    # 返回路由器信息、链接信息和更新信息
    return routers, links, updates

# 定义一个函数，用于构建网络
def build_network(routers, links):
    # 创建一个字典，用于存储路由器节点
    nodes = {name: Router(name) for name in routers}
    # 遍历链接列表
    for a, b, cost in links:
        # 如果链接的代价为-1，则跳过
        if cost == -1:
            continue
        # 将链接的代价存储到节点a和节点b的邻居字典中
        nodes[a].neighbors[b] = cost
        nodes[b].neighbors[a] = cost
    # 遍历节点字典中的每个节点
    for r in nodes.values():
        # 初始化每个节点的邻居列表
        r.initialize(nodes.keys())
    # 返回节点字典
    return nodes

def simulate_dv(nodes):
    # 初始化时间t为0
    t = 0
    # 无限循环，直到网络稳定
    while True:
        # 对每个节点按照名称排序
        for r in sorted(nodes.values(), key=lambda r: r.name):
            # 打印每个节点的距离表
            r.print_distance_table(t, nodes.keys())
        # 初始化changed为False
        changed = False
        vectors = {}
        # 对每个节点，初始化其邻居节点的向量表
        for r in nodes.values():
            vectors[r.name] = {}
            for n in r.neighbors:
                vectors[r.name][n] = r.get_poisoned_vector(n)
        # 对每个节点，接收其邻居节点的向量表
        for r in nodes.values():
            for neighbor in r.neighbors:
                r.receive(neighbor, vectors[neighbor][r.name])
        # 对每个节点，更新其路由表
        for r in nodes.values():
            if r.update_routes():
                changed = True
        # 如果没有节点更新了路由表，则网络稳定，跳出循环
        if not changed:
            break
        t += 1
    # 打印每个节点的路由表
    for r in sorted(nodes.values(), key=lambda r: r.name):
        r.print_routing_table()

def apply_updates(nodes, updates):
    # 遍历updates中的每一个三元组(a, b, cost)
    for a, b, cost in updates:
        # 如果cost为-1，则删除a和b之间的边
        if cost == -1:
            nodes[a].neighbors.pop(b, None)
            nodes[b].neighbors.pop(a, None)
        # 否则，将a和b之间的边设置为cost
        else:
            nodes[a].neighbors[b] = cost
            nodes[b].neighbors[a] = cost
    # 遍历nodes中的每一个节点r
    for r in nodes.values():
        # 初始化节点r的邻居列表
        r.initialize(nodes.keys())

if __name__ == '__main__':
    routers, links, updates = parse_input()
    net = build_network(routers, links)
    simulate_dv(net)
    if updates:
        apply_updates(net, updates)
        simulate_dv(net)

