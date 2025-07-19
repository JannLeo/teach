#!/usr/bin/env python3

import sys

class Router:
    def __init__(self, name):
        # 初始化节点名称
        self.name = name
        # 初始化邻居节点字典
        self.neighbors = {}
        # 初始化距离表字典
        self.distance_table = {}
        # 初始化路由表字典
        self.routing_table = {}
        # 初始化最小成本字典
        self.min_costs = {}
    
    def initialize_distance_table(self, all_routers):
        # 初始化距离表
        self.distance_table = {}
        self.min_costs = {}
        for dest in all_routers:
            # 遍历所有路由器
            if dest != self.name:
                # 如果目标路由器不是自己
                self.distance_table[dest] = {}
                # 初始化距离表
                for neighbor in self.neighbors:
                    # 遍历邻居路由器
                    if dest == neighbor:
                        # 如果目标路由器是邻居路由器
                        self.distance_table[dest][neighbor] = self.neighbors[neighbor]
                        # 设置距离为邻居路由器的距离
                    else:
                        self.distance_table[dest][neighbor] = float('inf')
                        # 否则设置距离为无穷大
                if self.distance_table[dest].values():
                    self.min_costs[dest] = min(self.distance_table[dest].values())

    # 获取距离向量
    def get_distance_vector(self):
        # 返回最小成本列表的副本
        return self.min_costs.copy()

    # 更新距离表
    def update_distance_table(self, neighbor, neighbor_dv):
        # 如果邻居不在邻居列表中，返回False
        if neighbor not in self.neighbors:
            return False
        changed = False
        # 遍历距离表中的每个目的地
        for dest in self.distance_table:
            # 如果目的地在邻居的距离向量中
            if dest in neighbor_dv:
                # 计算新的成本
                new_cost = self.neighbors[neighbor] + neighbor_dv[dest]
                # 获取旧的成本
                old_cost = self.distance_table[dest].get(neighbor, float('inf'))
                # 更新距离表中的成本
                self.distance_table[dest][neighbor] = new_cost
                # 如果新的成本和旧的成本不同，设置changed为True
                if new_cost != old_cost:
                    changed = True
                # 获取旧的最小成本
                old_min = self.min_costs[dest]
                # 更新最小成本
                self.min_costs[dest] = min(self.distance_table[dest].values())
                # 如果最小成本发生变化，设置changed为True
                if old_min != self.min_costs[dest]:
                    changed = True
        # 返回changed
        return changed

    def compute_routing_table(self):
        # 计算路由表
        self.routing_table = {}
        # 遍历距离表中的每个目的地
        for dest in self.distance_table:
            min_cost = float('inf')
            best_via = None
            # 遍历邻居节点
            for via in sorted(self.neighbors.keys()):
                # 如果邻居节点在距离表中，并且距离小于当前最小距离
                if via in self.distance_table[dest] and self.distance_table[dest][via] < min_cost:
                    min_cost = self.distance_table[dest][via]
                    best_via = via
            # 如果找到了最佳邻居节点，并且最小距离小于无穷大
            if best_via and min_cost < float('inf'):
                # 将目的地、最佳邻居节点和最小距离添加到路由表中
                self.routing_table[dest] = (best_via, min_cost)

def print_distance_table(router, step, all_routers):
    # 获取所有路由器，除了当前路由器
    destinations = sorted([r for r in all_routers if r != router.name])
    # 如果有其他路由器
    if destinations:
        # 打印路由器距离表
        print(f"Distance Table of router {router.name} at t={step}:")
        # 打印表头
        header = "     " + "".join(f"{d}    " for d in destinations)
        print(header)
        # 遍历所有路由器
        for dest in destinations:
            row = f"{dest}    "
            # 遍历所有路由器
            for other in destinations:
                # 获取当前路由器到其他路由器的距离
                cost = router.distance_table.get(dest, {}).get(other, float('inf'))
                # 如果距离为无穷大，则打印INF，否则打印距离
                row += f"{('INF'.ljust(5)) if cost == float('inf') else str(int(cost)).ljust(5)}"
            # 打印当前路由器到其他路由器的距离
            print(row)
        # 打印空行
        print()

def print_routing_table(router):
    if router.routing_table.keys():
        # 打印路由表
        print(f"Routing Table of router {router.name}:")
    # 遍历路由表中的所有目的地址
    for dest in sorted(router.routing_table.keys()):
        # 获取目的地址对应的下一跳地址和花费
        via, cost = router.routing_table[dest]
        # 打印目的地址、下一跳地址和花费
        print(f"{dest},{via},{int(cost)}")

def main():
    # 读取输入文件或标准输入
    lines = []
    if len(sys.argv) > 1:
        # 如果有输入文件，则打开文件并读取内容
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f]
    else:
        # 如果没有输入文件，则从标准输入读取内容
        # for line in sys.stdin:
        #     lines.append(line.strip())
        with open("input.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

    # 初始化路由器和初始链接
    routers, initial_links, updates = [], [], []
    i = 0
    # 读取路由器名称
    while i < len(lines) and lines[i] != "START" and lines[i] != "END" and lines[i] != "UPDATE":
        if lines[i]: routers.append(lines[i])
        i += 1

    # 读取初始链接
    if i < len(lines) and lines[i] == "START":
        i += 1
        while i < len(lines) and lines[i] != "UPDATE":
            parts = lines[i].split()
            if len(parts) == 3 and int(parts[2]) > 0 and parts[0] in routers and parts[1] in routers:
                initial_links.append((parts[0], parts[1], int(parts[2])))
            i += 1

    # 读取更新链接
    if i < len(lines) and lines[i] == "UPDATE":
        i += 1
        while i < len(lines) and lines[i] != "END":
            parts = lines[i].split()
            if len(parts) == 3 and (int(parts[2]) > 0 or int(parts[2]) == -1) and parts[0] in routers and parts[1] in routers:
                updates.append((parts[0], parts[1], int(parts[2])))
            i += 1

    # 初始化网络
    network = {name: Router(name) for name in routers}
    for r1, r2, cost in initial_links:
        network[r1].neighbors[r2] = cost
        network[r2].neighbors[r1] = cost

    # 初始化路由表
    all_routers = sorted(network.keys())

    for router in network.values():
        router.initialize_distance_table(all_routers)

    # Initial print
    step = 0
    for name in all_routers:
        print_distance_table(network[name], step, all_routers)

    # Initial convergence
    prev_state = None
    while True:
        current_state = {
            name: {
                dest: dict(network[name].distance_table[dest])
                for dest in network[name].distance_table
            } for name in all_routers
        }

        dvs = {name: network[name].get_distance_vector() for name in all_routers}

        changed = False
        for name in all_routers:
            router = network[name]
            for neighbor in router.neighbors:
                if router.update_distance_table(neighbor, dvs[neighbor]):
                    changed = True

        if prev_state == current_state or not changed:
            break

        step += 1
        for router in network.values():
            router.compute_routing_table()
        for name in all_routers:
            print_distance_table(network[name], step, all_routers)
        prev_state = current_state

    for name in all_routers:
        print_routing_table(network[name])
        if(router.routing_table):
            print()

    # Topology update
    if updates:
        last_dvs = {name: network[name].get_distance_vector() for name in all_routers}

        for r1, r2, cost in updates:
            if cost == -1:
                if r1 in network and r2 in network[r1].neighbors:
                    del network[r1].neighbors[r2]
                if r2 in network and r1 in network[r2].neighbors:
                    del network[r2].neighbors[r1]

                for dest in network[r1].distance_table:
                    network[r1].distance_table[dest].pop(r2, None)
                for dest in network[r2].distance_table:
                    network[r2].distance_table[dest].pop(r1, None)
            else:
                network[r1].neighbors[r2] = cost
                network[r2].neighbors[r1] = cost
                if r2 in network[r1].distance_table:
                    network[r1].distance_table[r2][r2] = cost
                if r1 in network[r2].distance_table:
                    network[r2].distance_table[r1][r1] = cost

        for name in all_routers:
            for neighbor in network[name].neighbors:
                if neighbor in last_dvs:
                    network[name].update_distance_table(neighbor, last_dvs[neighbor])

        for router in network.values():
            router.compute_routing_table()

        step += 1
        for name in all_routers:
            print_distance_table(network[name], step, all_routers)

        # Second convergence
        while True:
            dvs = {name: network[name].get_distance_vector() for name in all_routers}

            changed = False
            for name in all_routers:
                router = network[name]
                for neighbor in router.neighbors:
                    if router.update_distance_table(neighbor, dvs[neighbor]):
                        changed = True

            if not changed:
                break

            step += 1
            for router in network.values():
                router.compute_routing_table()
            for name in all_routers:
                print_distance_table(network[name], step, all_routers)

        for name in all_routers:
            print_routing_table(network[name])
            print()

if __name__ == "__main__":
    main()
