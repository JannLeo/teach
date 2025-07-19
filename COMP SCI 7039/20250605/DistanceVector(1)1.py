INF = 9999  # Represents unreachable routes

class Router:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}  # 直接邻居及代价
        self.dist_table = {}  # 距离表：来源 -> 目的地 -> 距离
        self.routes = {}  # 路由表：目的地 -> (下一跳, 总代价)

    def initialize(self, all_nodes):
        # 初始化距离表和路由表
        self.dist_table = {}
        self.routes = {}
        # 初始化距离表中的当前节点
        self.dist_table[self.name] = {}
        # 遍历所有节点
        for dest in all_nodes:
            # 如果当前节点是目标节点，则跳过
            if dest == self.name:
                continue
            # 如果当前节点是邻居节点，则将距离表中的距离设置为邻居节点的距离
            if dest in self.neighbors:
                self.dist_table[self.name][dest] = self.neighbors[dest]
                # 将路由表中的路由设置为邻居节点
                self.routes[dest] = (dest, self.neighbors[dest])
            else:
                # 如果当前节点不是邻居节点，则将距离表中的距离设置为无穷大
                self.dist_table[self.name][dest] = INF
                # 将路由表中的路由设置为None
                self.routes[dest] = (None, INF)
        # 遍历所有邻居节点
        for neighbor in self.neighbors:
            # 初始化邻居节点的距离表
            self.dist_table[neighbor] = {}
            # 遍历所有节点
            for dest in all_nodes:
                # 如果当前节点不是当前节点，则将距离表中的距离设置为无穷大
                if dest != self.name:
                    self.dist_table[neighbor][dest] = INF

    def get_poisoned_vector(self, to_neighbor):
        # 获取被毒化的向量
        vector = {}
        for dest, (nexthop, cost) in self.routes.items():
            # 遍历路由表中的每个目的地址
            if dest == to_neighbor:
                # 如果目的地址等于传入的邻居地址，则将成本设置为传入的邻居地址
                vector[dest] = cost
            elif nexthop == to_neighbor:
                vector[dest] = INF  # 毒化逆转处理
            else:
                vector[dest] = cost
        return vector

    # 接收邻居节点的距离向量
    def receive(self, neighbor, vector):
        # 如果邻居节点不在距离表中，则添加该节点
        if neighbor not in self.dist_table:
            self.dist_table[neighbor] = {}
        # 遍历距离向量中的每个节点
        for dest in vector:
            # 将邻居节点的距离向量添加到距离表中
            self.dist_table[neighbor][dest] = vector[dest]

    def update_routes(self):
        # 初始化updated为False
        updated = False
        # 遍历路由表中的每个目的地
        for dest in self.routes:
            # 初始化最小成本和最小跳数为无穷大
            min_cost = INF
            min_hop = None
            # 遍历邻居节点，按名称排序
            for neighbor in sorted(self.neighbors):
                # 获取到邻居节点的成本
                cost_to_neighbor = self.neighbors[neighbor]
                # 获取邻居节点到目的地的成本
                if dest == neighbor:
                    cost_from_neighbor = 0
                else:
                    neighbor_router = self.network[neighbor]
                    cost_from_neighbor = min(self.dist_table.get(neighbor, {}).get(dest, INF),neighbor_router.routes.get(dest, INF)[1])
                # 计算总成本
                total = cost_to_neighbor + cost_from_neighbor
                # 如果总成本小于最小成本，或者总成本等于最小成本且邻居节点名称小于最小跳点名称，则更新最小成本和最小跳点
                if total < min_cost or (total == min_cost and (min_hop is None or neighbor < min_hop)):
                    min_cost = total
                    min_hop = neighbor
            # 如果最小跳点和最小成本与路由表中的跳点和成本不同，则更新路由表，并将updated设为True
            if (min_hop, min_cost) != self.routes[dest]:
                self.routes[dest] = (min_hop, min_cost)
                updated = True
        # 遍历路由表中的每个目的地
        for dest in self.routes:
            # 如果目的地不在邻居节点中，则将目的地的成本更新到距离表中
            if dest not in self.neighbors:
                self.dist_table[self.name][dest] = self.routes[dest][1]
        # 返回updated的值
        return updated

    def print_distance_table(self, t, all_nodes):
        # 对所有节点进行排序，除了当前节点
        dests = sorted(n for n in all_nodes if n != self.name)
        # 对邻居节点进行排序
        neighbors = sorted(n for n in self.dist_table.keys() if n != self.name)
        # 打印距离表标题
        print(f"Distance Table of router {self.name} at t={t}:")
        # 打印节点名称
        print("     " + "    ".join(dests))
        # 遍历邻居节点
        for n in neighbors:
            row = [n]
            # 遍历所有节点
            for d in dests:
                # 获取距离表中的值
                if d == n:
                    val = self.dist_table[self.name].get(d, INF)
                else:
                    row_d = self.dist_table.get(d)
                    if row_d is None:
                        val = INF
                    else:
                        val = self.dist_table[self.name].get(d, INF) + self.dist_table[d].get(n, INF)
                # 如果值大于等于无穷大，则打印INF，否则打印值
                row.append("INF" if val >= INF else str(val))
            # 打印行
            print("    ".join(row))
        # 打印空行
        print("")

    def print_routing_table(self):
        # 打印路由表
        print(f"Routing Table of router {self.name}:")
        # 遍历路由表中的所有目的地址
        for dest in sorted(self.routes.keys()):
            # 获取目的地址对应的下一跳和花费
            hop, cost = self.routes[dest]
            # 如果下一跳不为空且花费小于无穷大，则打印目的地址、下一跳和花费
            if hop is not None and cost < INF:
                print(f"{dest},{hop},{cost}")
        # 打印空行
        print("")


def parse_input():
    # 打开输入文件，读取所有行
    with open("input.txt", "r", encoding="utf-8") as f:
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
    # 创建一个字典，键为路由器名称，值为Router对象
    nodes = {name: Router(name) for name in routers}
    
    # 把“整个网络（名字→Router实例）”存到每个 Router 里
    for r in nodes.values():
        r.network = nodes

    # 遍历链接列表
    for a, b, cost in links:
        # 如果链接的代价不为-1
        if cost != -1:
            # 将路由器a的邻居设置为路由器b，并将代价设置为cost
            nodes[a].neighbors[b] = cost
            # 将路由器b的邻居设置为路由器a，并将代价设置为cost
            nodes[b].neighbors[a] = cost
    # 遍历节点字典的值
    for r in nodes.values():
        # 初始化每个路由器的邻居列表
        r.initialize(nodes.keys())
    # 返回节点字典
    return nodes


def simulate_dv(nodes, start_t=0):
    # 初始化时间t为起始时间start_t
    t = start_t
    # 无限循环，直到网络稳定
    while True:
        # 遍历所有节点，按节点名称排序
        for r in sorted(nodes.values(), key=lambda r: r.name):
            # 打印每个节点的距离表
            r.print_distance_table(t, nodes.keys())
        # 初始化changed为False，表示网络是否稳定
        changed = False
        # 初始化vectors为空字典，用于存储每个节点的 poisoned vector
        vectors = {r.name: {} for r in nodes.values()}
        # 遍历所有节点，计算每个节点的 poisoned vector
        for r in nodes.values():
            for n in r.neighbors:
                vectors[r.name][n] = r.get_poisoned_vector(n)
        # 遍历所有节点，接收邻居节点的 poisoned vector
        for r in nodes.values():
            for neighbor in r.neighbors:
                r.receive(neighbor, vectors[neighbor][r.name])
        # 遍历所有节点，更新路由表
        for r in nodes.values():
            if r.update_routes():
                # 如果路由表发生变化，将changed设置为True
                changed = True
        # 如果网络稳定，跳出循环
        if not changed:
            break
        # 时间t加1
        t += 1
    # 遍历所有节点，按节点名称排序，打印每个节点的路由表
    for r in sorted(nodes.values(), key=lambda r: r.name):
        r.print_routing_table()
    # 返回时间t+1
    return t + 1


def apply_updates(nodes, updates):
    # 遍历updates中的每一个三元组
    for a, b, cost in updates:
        # 如果cost为-1，则删除a和b之间的边
        if cost == -1:
            nodes[a].neighbors.pop(b, None)
            nodes[b].neighbors.pop(a, None)
        # 否则，更新a和b之间的边为cost
        else:
            nodes[a].neighbors[b] = cost
            nodes[b].neighbors[a] = cost
    # 遍历nodes中的每一个节点，初始化其neighbors
    for r in nodes.values():
        r.initialize(nodes.keys())


if __name__ == '__main__':
    routers, links, updates = parse_input()
    net = build_network(routers, links)
    t = simulate_dv(net)
    if updates:
        apply_updates(net, updates)
        simulate_dv(net, start_t=t)
