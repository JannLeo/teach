#!/usr/bin/env python3
import socket
import random
import argparse
import threading

def generate_ports(seed, count, min_port, max_port):
    random.seed(seed)
    ports = set()
    while len(ports) < count:
        port = random.randint(min_port, max_port)
        ports.add(port)
    return list(ports)

def handle_tcp_connection(tcp_socket):
    while True:
        try:
            client_conn, client_addr = tcp_socket.accept()
            print(f"TCP connection established with {client_addr}")
            client_conn.sendall(b"Hello from TCP server!\n")
            client_conn.close()
        except OSError:
            break  # socket closed, exit thread

def handle_udp_connection(udp_socket):
    while True:
        try:
            data, addr = udp_socket.recvfrom(1024)
            msg = data.decode(errors="ignore")
            print(f"Received UDP message from {addr}: {msg}")
            # Reply back to the sender
            reply = f"Hello from UDP server! You sent: {msg}".encode()
            udp_socket.sendto(reply, addr)
        except OSError:
            break  # socket closed, exit thread

def main():
    parser = argparse.ArgumentParser(
        description="Open 10 random TCP and 5 random UDP ports on multiple IPs based on a seed."
    )
    parser.add_argument("seed", type=int, help="Seed to generate the same set of random ports.")
    args = parser.parse_args()

    tcp_ports = generate_ports(args.seed, count=10, min_port=1, max_port=65535)
    udp_ports = generate_ports(args.seed + 1, count=5, min_port=1, max_port=100)

    ips = ["200.2.4.10", "200.2.4.11", "200.2.4.12", "200.2.4.13"]
    print()
    print("IP Addresses:", ", ".join(ips))
    print(f"TCP Ports: {tcp_ports}")
    print(f"UDP Ports: {udp_ports}")

    tcp_sockets, udp_sockets = [], []

    # Create TCP sockets on all IPs
    for ip in ips:
        for port in tcp_ports:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            tcp_socket.bind((ip, port))
            tcp_socket.listen(5)
            tcp_sockets.append(tcp_socket)
            threading.Thread(target=handle_tcp_connection, args=(tcp_socket,), daemon=True).start()

    # Create UDP sockets on all IPs
    for ip in ips:
        for port in udp_ports:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            udp_socket.bind((ip, port))
            udp_sockets.append(udp_socket)
            threading.Thread(target=handle_udp_connection, args=(udp_socket,), daemon=True).start()

    # Keep the script alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[!] Exiting... (no cleanup)")

if __name__ == "__main__":
    main()
