import sys

INF = 9999  # 表示“不可达”的大数值

def debug(msg):
    print("[DEBUG]", msg)  # 调试信息输出，可注释掉屏蔽日志

class Router:
    def __init__(self, name):
        self.name = name            # 路由器名称
        self.neighbors = {}         # 邻居列表及其成本 {邻居: 成本}
        self.dist_table = {}        # 距离表 {来源: {目标: 成本}}
        self.routes = {}            # 路由表 {目标: (下一跳, 最小代价)}

    def initialize(self, all_nodes):
        # 初始化距离表和路由表
        self.dist_table = {}
        self.routes = {}

        # 初始化自身行（到每个节点的初始估计）
        self.dist_table[self.name] = {}
        for dest in all_nodes:
            if dest == self.name:
                continue
            # 如果邻居节点是目标节点，则距离为邻居节点到目标节点的距离
            if dest in self.neighbors:
                self.dist_table[self.name][dest] = self.neighbors[dest]
                # 路由表记录目标节点和距离
                self.routes[dest] = (dest, self.neighbors[dest])
            else:
                # 如果邻居节点不是目标节点，则距离为无穷大
                self.dist_table[self.name][dest] = INF
                # 路由表记录目标节点和距离
                self.routes[dest] = (None, INF)

        # 初始化邻居行为空（尚未接收到它们的 vector）
        for neighbor in self.neighbors:
            self.dist_table[neighbor] = {}
            for dest in all_nodes:
                # 如果目标节点不是自身，则距离为无穷大
                if dest != self.name:
                    self.dist_table[neighbor][dest] = INF

    def receive(self, neighbor, neighbor_vector):
        # 打印调试信息，表示从邻居接收到向量
        debug(f"{self.name} 从 {neighbor} 接收到向量: {neighbor_vector}")
        # 如果邻居不在距离表中，则添加邻居到距离表
        if neighbor not in self.dist_table:
            self.dist_table[neighbor] = {}
        # 遍历邻居向量中的每个目的地
        for dest in neighbor_vector:
            # 将邻居向量中的距离值添加到距离表中
            self.dist_table[neighbor][dest] = neighbor_vector[dest]

    def update_routes(self):
        # 更新路由表
        updated = False
        for dest in self.routes:
            # 初始化最小成本和最小跳数
            min_cost = INF
            min_hop = None
            # 遍历邻居节点
            for neighbor in sorted(self.neighbors):
                # 计算到达邻居节点的成本
                cost_to_neighbor = self.neighbors[neighbor]
                # 计算从邻居节点到达目标节点的成本
                cost_from_neighbor = self.dist_table.get(neighbor, {}).get(dest, INF)
                # 如果邻居报告不可达，则跳过该路径（防止毒性逆转误用）
                if cost_from_neighbor >= INF:
                    continue
                # 计算总成本
                total = cost_to_neighbor + cost_from_neighbor
                # 如果总成本小于最小成本，或者总成本等于最小成本且邻居节点小于最小跳数，则更新最小成本和最小跳数
                if total < min_cost or (total == min_cost and (min_hop is None or neighbor < min_hop)):
                    min_cost = total
                    min_hop = neighbor
            # 如果最小跳数和最小成本与当前路由表中的不同，则更新路由表
            if (min_hop, min_cost) != self.routes[dest]:
                debug(f"{self.name} 更新路由: {dest} 从 {self.routes[dest]} → ({min_hop},{min_cost})")
                self.routes[dest] = (min_hop, min_cost)
                updated = True

        # 仅更新非邻居目标的自我行（邻居成本固定）
        for dest in self.routes:
            if dest not in self.neighbors:
                self.dist_table[self.name][dest] = self.routes[dest][1]

        return updated

    def get_distance_vector(self, to_neighbor=None):
        return {dest: cost for dest, (_, cost) in self.routes.items()}




    def print_distance_table(self, t, all_nodes):
        # 对all_nodes进行排序，排除自身节点
        dests = sorted(n for n in all_nodes if n != self.name)
        # 对邻居节点进行排序
        neighbors = sorted(self.dist_table.keys())
        # 打印距离表标题
        print("Distance Table of router {} at t={}:".format(self.name, t))
        # 打印目标节点
        print("     " + "    ".join(dests))
        # 遍历邻居节点
        for n in neighbors:
            row = [n]
            # 遍历目标节点
            for d in dests:
                # 获取距离表中的值，如果大于等于INF，则打印INF，否则打印值
                val = self.dist_table[n].get(d, INF)
                row.append("INF" if val >= INF else str(val))
            # 打印一行
            print("    ".join(row))
        # 打印空行
        print("")

    def print_routing_table(self):
        # 打印路由表
        print("Routing Table of router {}:".format(self.name))
        # 遍历路由表中的所有目的地址
        for dest in sorted(self.routes.keys()):
            # 获取目的地址对应的下一跳和花费
            hop, cost = self.routes[dest]
            # 如果花费大于等于无穷大，则打印INF，否则打印花费
            cost_str = "INF" if cost >= INF else str(cost)
            # 打印目的地址、下一跳和花费
            print("{},{},{}".format(dest, hop, cost_str))
        # 打印空行
        print("")


def parse_input():
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    i = 0
    routers = []
    # 读取路由器信息，直到遇到"START"关键字
    while i < len(lines) and lines[i] != "START":
        # 去除路由器信息中的BOM字符
        routers.append(lines[i].lstrip('\ufeff').strip())
        i += 1
    i += 1

    links = []
    # 读取链接信息，直到遇到"UPDATE"关键字
    while i < len(lines) and lines[i] != "UPDATE":
        parts = lines[i].split()
        # 如果链接信息包含三个部分，则将其添加到links列表中
        if len(parts) == 3:
            links.append((parts[0], parts[1], int(parts[2])))
        i += 1
    i += 1

    updates = []
    # 读取更新信息，直到遇到"END"关键字
    while i < len(lines) and lines[i] != "END":
        parts = lines[i].split()
        # 如果更新信息包含三个部分，则将其添加到updates列表中
        if len(parts) == 3:
            updates.append((parts[0], parts[1], int(parts[2])))
        i += 1
    # 打印调试信息
    print("[DEBUG] routers =", routers)
    # 返回路由器信息、链接信息和更新信息
    return routers, links, updates


# 定义一个函数，用于构建网络
def build_network(routers, links):
    # 创建一个字典，键为路由器名称，值为Router对象
    nodes = {name: Router(name) for name in routers}
    # 遍历链接列表
    for a, b, cost in links:
        # 如果链接代价为-1，则跳过
        if cost == -1:
            continue
        # 将链接代价添加到路由器的邻居列表中
        nodes[a].neighbors[b] = cost
        nodes[b].neighbors[a] = cost
    # 初始化每个路由器的邻居列表
    for r in nodes.values():
        r.initialize(nodes.keys())
    # 返回构建好的网络
    return nodes


def simulate_dv(nodes):
    # 初始化时间t为0
    t = 0
    # 无限循环，直到所有节点都收敛
    while True:
        # 对所有节点按照名称排序
        for r in sorted(nodes.values(), key=lambda x: x.name):
            # 打印每个节点的距离表
            r.print_distance_table(t, nodes.keys())
        # 初始化changed为False
        changed = False

        for r in nodes.values():
            for neighbor in r.neighbors:
                vector = r.get_distance_vector(to_neighbor=neighbor)
                nodes[neighbor].receive(r.name, vector)

        # 遍历所有节点
        for r in nodes.values():
            # 更新路由表
            if r.update_routes():
                # 如果路由表发生变化，将changed设置为True
                changed = True

        # 如果所有节点都收敛，跳出循环
        if not changed:
            break
        # 时间t加1
        t += 1

    # 打印所有节点的路由表
    for r in sorted(nodes.values(), key=lambda x: x.name):
        r.print_routing_table()


def apply_updates(nodes, updates):
    # 遍历更新列表
    for a, b, cost in updates:
        # 如果节点a不在nodes中，则创建一个Router对象
        if a not in nodes:
            nodes[a] = Router(a)
        # 如果节点b不在nodes中，则创建一个Router对象
        if b not in nodes:
            nodes[b] = Router(b)
        # 如果cost为-1，则删除边和相关邻居信息
        if cost == -1:
            # 删除边和相关邻居信息
            nodes[a].neighbors.pop(b, None)
            nodes[b].neighbors.pop(a, None)
            nodes[a].dist_table.pop(b, None)
            nodes[b].dist_table.pop(a, None)
        else:
            # 否则，更新邻居信息和距离表
            nodes[a].neighbors[b] = cost
            nodes[b].neighbors[a] = cost
    # 遍历nodes中的每个Router对象，初始化距离表
    for r in nodes.values():
        r.initialize(nodes.keys())


if __name__ == '__main__':
    routers, links, updates = parse_input()
    net = build_network(routers, links)
    simulate_dv(net)
    if updates and len(updates) > 0:
        apply_updates(net, updates)
        simulate_dv(net)
