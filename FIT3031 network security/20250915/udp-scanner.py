#!/usr/bin/env python3
# 指定脚本使用 Python3 解释器运行

from scapy.all import IP, UDP, sr1, ICMP
# 导入scapy库的相关模块：IP、UDP、sr1（发送并接收数据包）、ICMP

import argparse  # 用于命令行参数解析
import time  # 用于计算扫描时间

def scan_udp_port(target_ip, port, timeout=4):
    """
    扫描目标IP的指定UDP端口，返回端口状态（开放、关闭或过滤）
    """
    pkt = IP(dst=target_ip)/UDP(dport=port)  # 构造目标IP的UDP数据包
    resp = sr1(pkt, timeout=timeout, verbose=0)  # 发送数据包，并等待响应，设置超时

    if resp is None:
        # 如果没有响应，表示端口可能被过滤或开放
        return f"UDP Port {port}: Open|Filtered"
    elif resp.haslayer(UDP):
        # 如果收到UDP响应，表示端口开放，UDP服务有回应
        return f"UDP Port {port}: Open (UDP service replied)"
    elif resp.haslayer(ICMP):
        # 如果收到ICMP响应，表示端口关闭或发生了其他网络错误
        icmp_type = resp.getlayer(ICMP).type  # 获取ICMP类型
        icmp_code = resp.getlayer(ICMP).code  # 获取ICMP代码
        if icmp_type == 3 and icmp_code == 3:  # ICMP类型为3，代码为3，表示端口不可达（关闭）
            return None  # 关闭的端口不输出结果
        else:
            # 如果收到其他ICMP类型和代码，表示网络问题或其他错误
            return f"UDP Port {port}: ICMP type={icmp_type} code={icmp_code}"
    return None  # 如果响应不符合预期，则返回None

def positive_int_min5(value: str) -> int:
    """
    用于命令行参数验证，确保batch-size至少为5
    """
    ivalue = int(value)
    if ivalue < 5:
        raise argparse.ArgumentTypeError("batch-size must be at least 5")  # 如果小于5，则报错
    return ivalue

if __name__ == "__main__":
    # 脚本主程序入口
    parser = argparse.ArgumentParser(description="UDP Port Scanner using Scapy and ICMP")
    # 创建解析器，定义脚本功能描述

    parser.add_argument("target", help="Target IP address")  # 目标IP地址
    parser.add_argument("--start-port", type=int, default=1, help="Start port")  # 起始端口，默认为1
    parser.add_argument("--end-port", type=int, default=100, help="End port")  # 结束端口，默认为100
    parser.add_argument("--batch-size", type=positive_int_min5, default=50,
                        help="Number of ports to scan per batch (min 5)")  # 每批次扫描的端口数，最小5个
    parser.add_argument("--timeout", type=int, default=4, help="Timeout in seconds for each port probe")  # 每个端口探测的超时时间，默认为4秒

    args = parser.parse_args()  # 解析命令行参数

    # 输出扫描开始的相关信息
    print(f"Starting UDP scan on {args.target} from port {args.start_port} to {args.end_port}")
    print(f"Batch size: {args.batch_size}, Timeout: {args.timeout}s")

    start_time = time.time()  # 记录扫描开始的时间

    open_udp = 0  # 统计开放的UDP端口数量
    filtered_udp = 0  # 统计开放|过滤的UDP端口数量
    closed_udp = 0  # 统计关闭的UDP端口数量

    ports = list(range(args.start_port, args.end_port + 1))  # 创建要扫描的端口范围列表
    for i in range(0, len(ports), args.batch_size):
        batch = ports[i:i + args.batch_size]  # 按批次扫描，每批次最多扫描args.batch_size个端口
        for port in batch:
            result = scan_udp_port(args.target, port, timeout=args.timeout)  # 扫描端口并获取结果
            if result:
                print(result)  # 输出扫描结果
                if "Open (UDP service replied)" in result:
                    open_udp += 1  # 如果端口开放，增加open_udp计数
                elif "Open|Filtered" in result:
                    filtered_udp += 1  # 如果端口开放或过滤，增加filtered_udp计数
            else:
                closed_udp += 1  # 如果没有响应（表示端口关闭），增加closed_udp计数

        # 在每批次扫描后增加延时，避免过快扫描
        time.sleep(0.5)  # 每批次扫描后增加0.5秒的延时，减少扫描压力

    elapsed = time.time() - start_time  # 计算扫描所用时间
    print("\n--- Scan Summary ---")
    print(f"Open UDP ports: {open_udp}")  # 输出开放的UDP端口数量
    print(f"Open|Filtered UDP ports: {filtered_udp}")  # 输出开放或被过滤的UDP端口数量
    print(f"Closed UDP ports (ICMP replies): {closed_udp}")  # 输出关闭的UDP端口数量
    print(f"Scan finished in {elapsed:.2f} seconds.")  # 输出扫描完成的总时间
