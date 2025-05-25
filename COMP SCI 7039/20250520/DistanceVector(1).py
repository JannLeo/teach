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
        self.dist_table = {}
        self.routes = {}

        # 初始化自身行（到每个节点的初始估计）
        self.dist_table[self.name] = {}
        for dest in all_nodes:
            if dest == self.name:
                continue
            if dest in self.neighbors:
                self.dist_table[self.name][dest] = self.neighbors[dest]
                self.routes[dest] = (dest, self.neighbors[dest])
            else:
                self.dist_table[self.name][dest] = INF
                self.routes[dest] = (None, INF)

        # 初始化邻居行为空（尚未接收到它们的 vector）
        for neighbor in self.neighbors:
            self.dist_table[neighbor] = {}
            for dest in all_nodes:
                if dest != self.name:
                    self.dist_table[neighbor][dest] = INF

    def receive(self, neighbor, neighbor_vector):
        debug(f"{self.name} 从 {neighbor} 接收到向量: {neighbor_vector}")
        if neighbor not in self.dist_table:
            self.dist_table[neighbor] = {}
        for dest in neighbor_vector:
            self.dist_table[neighbor][dest] = neighbor_vector[dest]

    def update_routes(self):
        updated = False
        for dest in self.routes:
            min_cost = INF
            min_hop = None
            for neighbor in sorted(self.neighbors):
                cost_to_neighbor = self.neighbors[neighbor]
                cost_from_neighbor = self.dist_table.get(neighbor, {}).get(dest, INF)
                total = cost_to_neighbor + cost_from_neighbor
                if total < min_cost or (total == min_cost and (min_hop is None or neighbor < min_hop)):
                    min_cost = total
                    min_hop = neighbor
            if (min_hop, min_cost) != self.routes[dest]:
                debug(f"{self.name} 更新路由: {dest} 从 {self.routes[dest]} → ({min_hop},{min_cost})")
                self.routes[dest] = (min_hop, min_cost)
                updated = True

        # 仅更新非邻居目标的自我行（邻居成本固定）
        for dest in self.routes:
            if dest not in self.neighbors:
                self.dist_table[self.name][dest] = self.routes[dest][1]

        return updated

    def get_distance_vector(self):
        return {dest: cost for dest, (hop, cost) in self.routes.items()}

    def print_distance_table(self, t, all_nodes):
        dests = sorted(n for n in all_nodes if n != self.name)
        neighbors = sorted(self.dist_table.keys())
        print("Distance Table of router {} at t={}:".format(self.name, t))
        print("     " + "    ".join(dests))
        for n in neighbors:
            row = [n]
            for d in dests:
                val = self.dist_table[n].get(d, INF)
                row.append("INF" if val >= INF else str(val))
            print("    ".join(row))
        print("")

    def print_routing_table(self):
        print("Routing Table of router {}:".format(self.name))
        for dest in sorted(self.routes.keys()):
            hop, cost = self.routes[dest]
            cost_str = "INF" if cost >= INF else str(cost)
            print("{},{},{}".format(dest, hop, cost_str))
        print("")


def parse_input():
    #lines = [line.strip() for line in sys.stdin if line.strip()]
    with open("input.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    i = 0
    routers = []
    while i < len(lines) and lines[i] != "START":
        routers.append(lines[i])
        i += 1
    i += 1

    links = []
    while i < len(lines) and lines[i] != "UPDATE":
        parts = lines[i].split()
        if len(parts) == 3:
            links.append((parts[0], parts[1], int(parts[2])))
        i += 1
    i += 1

    updates = []
    while i < len(lines) and lines[i] != "END":
        parts = lines[i].split()
        if len(parts) == 3:
            updates.append((parts[0], parts[1], int(parts[2])))
        i += 1
    return routers, links, updates


def build_network(routers, links):
    nodes = {name: Router(name) for name in routers}
    for a, b, cost in links:
        if cost == -1:
            continue
        nodes[a].neighbors[b] = cost
        nodes[b].neighbors[a] = cost
    for r in nodes.values():
        r.initialize(nodes.keys())
    return nodes


def simulate_dv(nodes):
    t = 0
    while True:
        for r in sorted(nodes.values(), key=lambda x: x.name):
            r.print_distance_table(t, nodes.keys())
        changed = False

        distance_vectors = {r.name: r.get_distance_vector() for r in nodes.values()}

        for r in nodes.values():
            for neighbor in r.neighbors:
                r.receive(neighbor, distance_vectors[neighbor])

        for r in nodes.values():
            if r.update_routes():
                changed = True

        if not changed:
            break
        t += 1

    for r in sorted(nodes.values(), key=lambda x: x.name):
        r.print_routing_table()


def apply_updates(nodes, updates):
    for a, b, cost in updates:
        if a not in nodes:
            nodes[a] = Router(a)
        if b not in nodes:
            nodes[b] = Router(b)
        if cost == -1:
            # 删除边和相关邻居信息
            nodes[a].neighbors.pop(b, None)
            nodes[b].neighbors.pop(a, None)
            nodes[a].dist_table.pop(b, None)
            nodes[b].dist_table.pop(a, None)
        else:
            nodes[a].neighbors[b] = cost
            nodes[b].neighbors[a] = cost
    for r in nodes.values():
        r.initialize(nodes.keys())


if __name__ == '__main__':
    routers, links, updates = parse_input()
    net = build_network(routers, links)
    simulate_dv(net)
    if updates and len(updates) > 0:
        apply_updates(net, updates)
        simulate_dv(net)
