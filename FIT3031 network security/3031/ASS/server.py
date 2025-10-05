import socket
import random
import argparse
import threading

# Function to generate a set of random ports based on the seed
def generate_ports(seed, count=5):
    random.seed(seed)
    ports = set()
    while len(ports) < count:
        port = random.randint(10000, 60000)  # Port range typically usable by applications
        ports.add(port)
    return list(ports)

# Function to handle TCP connections
def handle_tcp_connection(tcp_socket):
    while True:
        client_conn, client_addr = tcp_socket.accept()
        print(f"TCP connection established with {client_addr}")
        client_conn.sendall(b"Hello from TCP server!\n")
        client_conn.close()

# Function to handle UDP communication
def handle_udp_connection(udp_socket):
    while True:
        data, addr = udp_socket.recvfrom(1024)
        print(f"Received UDP message from {addr}: {data.decode('utf-8')}")
        udp_socket.sendto(b"Hello from UDP server!\n", addr)

# Main function to set up sockets and handle arguments
def main():
    parser = argparse.ArgumentParser(description="Open 5 random TCP and 5 random UDP ports based on a seed.")
    parser.add_argument("seed", type=int, help="Seed to generate the same set of random ports.")
    args = parser.parse_args()

    # Generate 5 random TCP and 5 random UDP ports
    tcp_ports = generate_ports(args.seed, count=5)
    udp_ports = generate_ports(args.seed + 1, count=5)  # Slightly different seed for UDP ports

    print(f"TCP Ports: {tcp_ports}")
    print(f"UDP Ports: {udp_ports}")

    # Create TCP sockets
    tcp_sockets = []
    for port in tcp_ports:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.bind(("0.0.0.0", port))
        tcp_socket.listen(5)
        tcp_sockets.append(tcp_socket)
        threading.Thread(target=handle_tcp_connection, args=(tcp_socket,), daemon=True).start()
        print(f"TCP socket open on port {port}")


    # Create UDP sockets
    udp_sockets = []
    for port in udp_ports:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_socket.bind(("0.0.0.0", port))
        udp_sockets.append(udp_socket)
        threading.Thread(target=handle_udp_connection, args=(udp_socket,), daemon=True).start()
        print(f"UDP socket open on port {port}")

    # Keep the program running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down sockets...")
        for tcp_socket in tcp_sockets:
            tcp_socket.close()
        for udp_socket in udp_sockets:
            udp_socket.close()

if __name__ == "__main__":
    main()
