#!/usr/bin/env python3
import argparse  # 导入 argparse 模块，用于处理命令行参数
import time  # 导入 time 模块，用于时间操作
import threading  # 导入 threading 模块，用于多线程
import sys  # 导入 sys 模块，用于与 Python 解释器交互
import json  # 导入 json 模块，用于处理 JSON 数据
from datetime import datetime  # 从 datetime 模块导入 datetime，用于获取当前日期和时间
from scapy.all import IP, TCP, send, conf, RandShort, AsyncSniffer  # 从 scapy 库导入相关工具函数

# --------------------------------
# SCAPY CONFIG
# --------------------------------
conf.verb = 0  # 配置 Scapy，设置为 0 表示静默模式（不输出调试信息）

# 强制行缓冲输出，使得实时打印能够在被管道传输时也能显示
try:
    sys.stdout.reconfigure(line_buffering=True)  # 尝试在支持的系统中启用行缓冲
except Exception:  # 如果不支持，则捕获异常
    pass  # 不做处理，继续执行

# --------------------------------
# Helpers
# --------------------------------
def now_iso():
    # 获取当前的 UTC 时间，并转换为 ISO 格式
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"  # 获取当前时间，并以 ISO 8601 格式输出

def make_rst(dst_ip, sport, dport, seq, ack):
    # 创建一个 RST 包，用于主动关闭 TCP 连接
    return IP(dst=dst_ip) / TCP(sport=sport, dport=dport, flags="R", seq=ack, ack=seq + 1)

# --------------------------------
# Scanner (1 batch/sec, continuous sniffer, live output)
# --------------------------------
def paced_tcp_scan(
    target_ip: str,  # 目标 IP 地址
    start_port: int,  # 起始端口号
    end_port: int,  # 结束端口号
    conns_per_batch: int = 200,  # 每秒发送的端口连接数
    tail_wait: float = 2.0,  # 扫描结束后等待的时间，以捕捉遗漏的回复
    iface: str | None = None,  # 网络接口
    ndjson: bool = False,  # 是否输出 NDJSON 格式（默认为 False）
    progress: bool = False,  # 是否显示进度条（默认为 False）
):
    """
    该函数执行带有实时输出的批量扫描，每秒扫描一个批次。使用单独的异步嗅探器以确保不会错过快速回复。
    """
    if iface:
        conf.iface = iface  # 设置使用的网络接口

    src_port = int(RandShort())  # 生成一个随机源端口，用于保持连接的一致性
    ports = list(range(start_port, end_port + 1))  # 创建要扫描的端口范围
    total = len(ports)  # 获取端口总数
    batches = [ports[i:i + conns_per_batch] for i in range(0, total, conns_per_batch)]  # 将端口划分为多个批次

    open_ports = set()  # 存储发现的开放端口
    seen_synacks = set()  # 存储已收到的 SYN+ACK 响应，避免重复处理
    lock = threading.Lock()  # 创建锁，防止并发时的竞态条件

    if progress:
        # 如果需要显示进度，则打印详细信息
        print(f"[{now_iso()}] Starting scan target={target_ip} range={start_port}-{end_port} "
              f"ports={total} batch_size={conns_per_batch} iface={iface or '(auto)'} src_port={src_port}",
              flush=True)
        print("--- TCP Scan (live results) ---", flush=True)
    else:
        # 如果不需要进度条，只输出基本信息
        print("--- TCP Scan Results (live) ---", flush=True)

    # 数据包处理函数（由嗅探器线程调用）
    def on_packet(pkt):
        # 判断数据包是否有 IP 和 TCP 层
        if not pkt.haslayer(IP) or not pkt.haslayer(TCP):
            return

        ip = pkt[IP]  # 获取 IP 层
        tcp = pkt[TCP]  # 获取 TCP 层

        # 仅考虑从目标 IP 发回的数据包，且目标端口必须是我们选定的源端口
        if ip.src != target_ip or tcp.dport != src_port:
            return

        flags = tcp.flags  # 获取 TCP 标志位
        if (flags & 0x12) == 0x12:  # 判断是否为 SYN+ACK 标志位
            dport = tcp.sport  # 目标端口是源端口
            with lock:
                if dport in seen_synacks:
                    return  # 如果该端口已经处理过，则跳过
                seen_synacks.add(dport)  # 记录该端口
                open_ports.add(dport)  # 将端口加入开放端口集合

            # 实时打印开放端口的信息
            if ndjson:
                print(json.dumps({
                    "ts": now_iso(),
                    "event": "open_port",
                    "target": target_ip,
                    "port": int(dport),
                    "proto": "tcp"
                }), flush=True)
            else:
                print(f"TCP Port {dport}: Open", flush=True)

            try:
                # 构造一个 RST 包以主动关闭连接
                rst = make_rst(target_ip, src_port, dport, tcp.seq, tcp.ack)
                send(rst, verbose=0)  # 发送 RST 包
            except Exception:
                pass  # 忽略发送错误

        # 如果是 RST+ACK 包，表示端口关闭，但不做任何处理

    # 启动单独的嗅探器线程，捕获所有与目标 IP 和端口相关的 TCP 数据包
    bpf = f"tcp and host {target_ip}"  # 设置过滤器，仅捕获与目标主机相关的 TCP 数据包
    sniffer = AsyncSniffer(filter=bpf, prn=on_packet, store=False, iface=iface)  # 创建嗅探器
    sniffer.start()  # 启动嗅探器
    time.sleep(0.05)  # 等待嗅探器准备就绪

    start_time = time.monotonic()  # 记录扫描开始时间
    next_release = start_time  # 计划的下一个批次发送时间

    try:
        # 遍历每个批次，按计划发送
        for idx, batch in enumerate(batches, 1):
            # 确保每秒钟发送一个批次
            now = time.monotonic()
            if now < next_release:
                time.sleep(next_release - now)  # 等待直到计划的时间

            if progress:
                # 如果需要显示进度，则输出当前批次的信息
                first = batch[0]
                last = batch[-1]
                print(f"[{now_iso()}] Batch {idx}/{len(batches)} send: ports {first}-{last} "
                      f"(count={len(batch)})", flush=True)

            # 构建待发送的 SYN 包列表
            pkts = [IP(dst=target_ip)/TCP(sport=src_port, dport=p, flags="S") for p in batch]
            send(pkts, verbose=0)  # 发送 SYN 包

            # 确保每个批次之间的时间间隔是严格的一秒
            next_release += 1.0

        # 在最后一个批次之后继续等待，捕捉剩余的回复
        if tail_wait > 0:
            if progress:
                print(f"[{now_iso()}] Tail wait {tail_wait:.2f}s for late replies", flush=True)
            time.sleep(tail_wait)
    finally:
        # 停止嗅探器线程
        try:
            sniffer.stop()
        except Exception:
            pass

    elapsed = time.monotonic() - start_time  # 计算扫描的总时长
    # 扫描结束后输出总结信息
    if ndjson:
        print(json.dumps({
            "ts": now_iso(),
            "event": "summary",
            "target": target_ip,
            "ports_scanned": total,
            "open_count": len(open_ports),
            "elapsed_sec": round(elapsed, 2),
            "open_ports": sorted(int(p) for p in open_ports),
        }), flush=True)
    else:
        # 否则以普通文本格式输出扫描结果
        print(f"\nScan finished in {elapsed:.2f} seconds.")
        print(f"Ports scanned: {total} (TCP)")
        print(f"Open ports found: {len(open_ports)} TCP")
        if open_ports:
            print("Open port list:", ", ".join(str(p) for p in sorted(open_ports)))

# --------------------------------
# CLI
# --------------------------------
def main():
    # 配置命令行参数
    parser = argparse.ArgumentParser(description="Paced TCP Port Scanner (live output)")
    parser.add_argument("target", help="Target IPv4 address or hostname to scan")  # 目标 IP 或主机名
    parser.add_argument("--start-port", type=int, default=1, help="Start of port range")  # 起始端口号
    parser.add_argument("--end-port", type=int, default=65535, help="End of port range")  # 结束端口号
    parser.add_argument("--conns-per-batch", type=int, default=1000,  # 每秒扫描多少个端口
                        help="How many ports to scan per second (batch size)")
    parser.add_argument("--tail-wait", type=float, default=2.0,  # 扫描结束后继续等待的时间
                        help="Seconds to keep listening after the last batch")
    args = parser.parse_args()  # 解析命令行参数

    # 调用扫描函数
    paced_tcp_scan(
        args.target,
        args.start_port,
        args.end_port,
        conns_per_batch=args.conns_per_batch,
        tail_wait=args.tail_wait,
        iface=None,  # 使用默认网络接口
        ndjson=False,  # 不输出 NDJSON 格式
        progress=False,  # 不显示进度条
    )

if __name__ == "__main__":
    main()  # 执行主函数
