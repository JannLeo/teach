#!/usr/bin/env python3
from scapy.all import IP, UDP, sr1, ICMP
import argparse
import time

def scan_udp_port(target_ip, port, timeout=4, retries=1):
    """
    扫描单个UDP端口，增加重试机制减少误报
    """
    for attempt in range(retries):
        pkt = IP(dst=target_ip)/UDP(dport=port)
        resp = sr1(pkt, timeout=timeout, verbose=0)

        if resp is None:
            # 如果是最后一次尝试还没响应，才认为是 Open|Filtered
            if attempt == retries - 1:
                return f"UDP Port {port}: Open|Filtered"
        elif resp.haslayer(UDP):
            return f"UDP Port {port}: Open (UDP service replied)"
        elif resp.haslayer(ICMP):
            icmp_type = resp.getlayer(ICMP).type
            icmp_code = resp.getlayer(ICMP).code
            if icmp_type == 3 and icmp_code == 3:   # ICMP Port Unreachable
                return None  # Closed，不打印
            else:
                return f"UDP Port {port}: ICMP type={icmp_type} code={icmp_code}"
    return None

def positive_int_min5(value: str) -> int:
    ivalue = int(value)
    if ivalue < 5:
        raise argparse.ArgumentTypeError("batch-size must be at least 5")
    return ivalue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Improved UDP Port Scanner with retries")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("--start-port", type=int, default=1, help="Start port")
    parser.add_argument("--end-port", type=int, default=100, help="End port")
    parser.add_argument("--batch-size", type=positive_int_min5, default=20,
                        help="Number of ports to scan per batch (min 5)")
    parser.add_argument("--timeout", type=int, default=5,
                        help="Timeout in seconds for each port probe")
    parser.add_argument("--retries", type=int, default=2,
                        help="Number of retries for unanswered ports")
    args = parser.parse_args()

    print(f"Starting UDP scan on {args.target} from port {args.start_port} to {args.end_port}")
    print(f"Batch size: {args.batch_size}, Timeout: {args.timeout}s, Retries: {args.retries}")
    start_time = time.time()

    open_udp = 0
    filtered_udp = 0
    closed_udp = 0

    ports = list(range(args.start_port, args.end_port + 1))
    for i in range(0, len(ports), args.batch_size):
        batch = ports[i:i + args.batch_size]
        for port in batch:
            result = scan_udp_port(args.target, port, timeout=args.timeout, retries=args.retries)
            if result:
                print(result)
                if "Open (UDP service replied)" in result:
                    open_udp += 1
                elif "Open|Filtered" in result:
                    filtered_udp += 1
            else:
                closed_udp += 1

    elapsed = time.time() - start_time
    print("\n--- Scan Summary ---")
    print(f"Open UDP ports: {open_udp}")
    print(f"Open|Filtered UDP ports: {filtered_udp}")
    print(f"Closed UDP ports (ICMP replies): {closed_udp}")
    print(f"Scan finished in {elapsed:.2f} seconds.")