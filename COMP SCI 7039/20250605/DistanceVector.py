import sys

INF = 9999  # "Infinity" for unreachable routes

DEBUG = True  # Set to False to disable debug prints
def debug(msg):
    if DEBUG:
        print("[DEBUG]", msg)

class Router:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}  # direct neighbors and link cost
        self.dist_table = {}  # distance table: who told what about whom
        self.routes = {}  # current best route {dest: (nexthop, cost)}

    def initialize(self, all_nodes):
        self.dist_table = {}
        self.routes = {}
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
        for neighbor in self.neighbors:
            self.dist_table[neighbor] = {}
            for dest in all_nodes:
                if dest != self.name:
                    self.dist_table[neighbor][dest] = INF

    def get_poisoned_vector(self, to_neighbor):
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
        debug(f"{self.name} 从 {neighbor} 接收到向量: {vector}")
        if neighbor not in self.dist_table:
            self.dist_table[neighbor] = {}
        for dest in vector:
            self.dist_table[neighbor][dest] = vector[dest]

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
        for dest in self.routes:
            if dest not in self.neighbors:
                self.dist_table[self.name][dest] = self.routes[dest][1]
        return updated

    def print_distance_table(self, t, all_nodes):
        dests = sorted(n for n in all_nodes if n != self.name)
        neighbors = sorted(self.dist_table.keys())
        print(f"Distance Table of router {self.name} at t={t}:")
        print("     " + "    ".join(dests))
        for n in neighbors:
            row = [n]
            for d in dests:
                val = self.dist_table[n].get(d, INF)
                row.append("INF" if val >= INF else str(val))
            print("    ".join(row))
        print("")

    def print_routing_table(self):
        print(f"Routing Table of router {self.name}:")
        for dest in sorted(self.routes.keys()):
            hop, cost = self.routes[dest]
            cost_str = "INF" if cost >= INF else str(cost)
            print(f"{dest},{hop},{cost_str}")
        print("")

def parse_input():
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
        a, b, c = lines[i].split()
        links.append((a, b, int(c)))
        i += 1
    i += 1
    updates = []
    while i < len(lines) and lines[i] != "END":
        a, b, c = lines[i].split()
        updates.append((a, b, int(c)))
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
        for r in sorted(nodes.values(), key=lambda r: r.name):
            r.print_distance_table(t, nodes.keys())
        changed = False
        vectors = {}
        for r in nodes.values():
            vectors[r.name] = {}
            for n in r.neighbors:
                vectors[r.name][n] = r.get_poisoned_vector(n)
        for r in nodes.values():
            for neighbor in r.neighbors:
                r.receive(neighbor, vectors[neighbor][r.name])
        for r in nodes.values():
            if r.update_routes():
                changed = True
        if not changed:
            break
        t += 1
    for r in sorted(nodes.values(), key=lambda r: r.name):
        r.print_routing_table()

def apply_updates(nodes, updates):
    for a, b, cost in updates:
        if cost == -1:
            nodes[a].neighbors.pop(b, None)
            nodes[b].neighbors.pop(a, None)
        else:
            nodes[a].neighbors[b] = cost
            nodes[b].neighbors[a] = cost
    for r in nodes.values():
        r.initialize(nodes.keys())

if __name__ == '__main__':
    routers, links, updates = parse_input()
    net = build_network(routers, links)
    simulate_dv(net)
    if updates:
        apply_updates(net, updates)
        simulate_dv(net)

