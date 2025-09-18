#!/usr/bin/env python3
import argparse
import time
import threading
import sys
import json
from datetime import datetime
from scapy.all import IP, TCP, send, conf, RandShort, AsyncSniffer

# --------------------------------
# SCAPY CONFIG
# --------------------------------
conf.verb = 0  # quiet Scapy; set to 1 if you want more logs

# Force line-buffered stdout so live prints show up even when piped
try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

# --------------------------------
# Helpers
# --------------------------------
def now_iso():
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"

def make_rst(dst_ip, sport, dport, seq, ack):
    return IP(dst=dst_ip) / TCP(sport=sport, dport=dport, flags="R", seq=ack, ack=seq + 1)

# --------------------------------
# Scanner (1 batch/sec, continuous sniffer, live output)
# --------------------------------
def paced_tcp_scan(
    target_ip: str,
    start_port: int,
    end_port: int,
    conns_per_batch: int = 200,
    tail_wait: float = 2.0,
    iface: str | None = None,
    ndjson: bool = False,
    progress: bool = False,
):
    """
    Sends one batch exactly once per second while a single AsyncSniffer runs for the
    entire duration to avoid missing fast replies. Prints results live as they arrive.
    """
    if iface:
        conf.iface = iface

    src_port = int(RandShort())  # fixed source port for correlation
    ports = list(range(start_port, end_port + 1))
    total = len(ports)
    batches = [ports[i:i + conns_per_batch] for i in range(0, total, conns_per_batch)]

    open_ports = set()
    seen_synacks = set()
    lock = threading.Lock()

    if progress:
        print(f"[{now_iso()}] Starting scan target={target_ip} range={start_port}-{end_port} "
              f"ports={total} batch_size={conns_per_batch} iface={iface or '(auto)'} src_port={src_port}",
              flush=True)
        print("--- TCP Scan (live results) ---", flush=True)
    else:
        print("--- TCP Scan Results (live) ---", flush=True)

    # Packet processor (called by sniffer thread)
    def on_packet(pkt):
        if not pkt.haslayer(IP) or not pkt.haslayer(TCP):
            return
        ip = pkt[IP]
        tcp = pkt[TCP]

        # Only consider replies from target to our chosen source port
        if ip.src != target_ip or tcp.dport != src_port:
            return

        flags = tcp.flags
        if (flags & 0x12) == 0x12:
            dport = tcp.sport
            with lock:
                if dport in seen_synacks:
                    return
                seen_synacks.add(dport)
                open_ports.add(dport)

            # Live print as soon as discovered
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
                rst = make_rst(target_ip, src_port, dport, tcp.seq, tcp.ack)
                send(rst, verbose=0)
            except Exception:
                pass  

        # RST+ACK => closed (ignored for output)

    # Start single sniffer for duration of scan
    bpf = f"tcp and host {target_ip}"
    sniffer = AsyncSniffer(filter=bpf, prn=on_packet, store=False, iface=iface)
    sniffer.start()
    time.sleep(0.05)  # give sniffer a moment to attach

    start_time = time.monotonic()
    next_release = start_time

    try:
        for idx, batch in enumerate(batches, 1):
            # Sleep until scheduled tick (strict cadence)
            now = time.monotonic()
            if now < next_release:
                time.sleep(next_release - now)

            if progress:
                first = batch[0]
                last = batch[-1]
                print(f"[{now_iso()}] Batch {idx}/{len(batches)} send: ports {first}-{last} "
                      f"(count={len(batch)})", flush=True)

            # Build list of packets and send at the tick
            pkts = [IP(dst=target_ip)/TCP(sport=src_port, dport=p, flags="S") for p in batch]
            send(pkts, verbose=0)

            # Schedule next tick exactly +1.0s from planned release (prevents drift)
            next_release += 1.0

        # Tail wait to catch stragglers after last batch
        if tail_wait > 0:
            if progress:
                print(f"[{now_iso()}] Tail wait {tail_wait:.2f}s for late replies", flush=True)
            time.sleep(tail_wait)
    finally:
        try:
            sniffer.stop()
        except Exception:
            pass

    elapsed = time.monotonic() - start_time
    # Final summary
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
        print(f"\nScan finished in {elapsed:.2f} seconds.")
        print(f"Ports scanned: {total} (TCP)")
        print(f"Open ports found: {len(open_ports)} TCP")
        if open_ports:
            print("Open port list:", ", ".join(str(p) for p in sorted(open_ports)))

# --------------------------------
# CLI
# --------------------------------
def main():
    parser = argparse.ArgumentParser(description="Paced TCP Port Scanner (live output)")
    parser.add_argument("target", help="Target IPv4 address or hostname to scan")
    parser.add_argument("--start-port", type=int, default=1, help="Start of port range")
    parser.add_argument("--end-port", type=int, default=65535, help="End of port range")
    parser.add_argument("--conns-per-batch", type=int, default=1000,
                        help="How many ports to scan per second (batch size)")
    parser.add_argument("--tail-wait", type=float, default=2.0,
                        help="Seconds to keep listening after the last batch")
    args = parser.parse_args()

    paced_tcp_scan(
        args.target,
        args.start_port,
        args.end_port,
        conns_per_batch=args.conns_per_batch,
        tail_wait=args.tail_wait,
        iface=None,       
        ndjson=False,     
        progress=False,   
    )

if __name__ == "__main__":
    main()
