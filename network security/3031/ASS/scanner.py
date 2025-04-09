import socket
import argparse
import concurrent.futures

# Function to scan a TCP port
def scan_tcp_port(target_ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target_ip, port))
        sock.close()
        if result == 0:
            return f"TCP Port {port}: Open"
        else:
            return None  # Don't return anything for closed ports
    except Exception as e:
        return None  # Don't return errors either

# Function to scan a UDP port
def scan_udp_port(target_ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        # Send an empty datagram
        sock.sendto(b'', (target_ip, port))
        try:
            # Wait for a response (not always reliable for UDP)
            data, _ = sock.recvfrom(1024)
            sock.close()
            return f"UDP Port {port}: Open"
        except socket.timeout:
            return None  # Don't return anything for closed ports
    except Exception as e:
        return None  # Don't return errors

# Main function to scan both TCP and UDP ports
def port_scanner(target_ip, port_range, scan_udp=False, timeout=1):
    start_port, end_port = port_range

    print(f"Starting scan on {target_ip} for ports {start_port} to {end_port}...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # TCP scan
        tcp_futures = {executor.submit(scan_tcp_port, target_ip, port, timeout): port for port in range(start_port, end_port+1)}

        if scan_udp:
            udp_futures = {executor.submit(scan_udp_port, target_ip, port, timeout): port for port in range(start_port, end_port+1)}
        else:
            udp_futures = {}

        print("\n--- TCP Scan Results ---")
        for future in concurrent.futures.as_completed(tcp_futures):
            result = future.result()
            if result:  # Only print if there's a valid result (i.e., port is open)
                print(result)

        if scan_udp:
            print("\n--- UDP Scan Results ---")
            for future in concurrent.futures.as_completed(udp_futures):
                result = future.result()
                if result:  # Only print if there's a valid result (i.e., port is open or filtered)
                    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP and UDP Port Scanner")
    parser.add_argument("target", help="Target IP address or hostname to scan")
    parser.add_argument("--start-port", type=int, default=1, help="Start of the port range (default: 1)")
    parser.add_argument("--end-port", type=int, default=65535, help="End of the port range (default: 65535)")
    parser.add_argument("--udp", action="store_true", help="Enable UDP scanning (default: only TCP)")
    parser.add_argument("--timeout", type=int, default=1, help="Socket timeout in seconds (default: 1)")
    args = parser.parse_args()

    # Run the port scanner
    port_scanner(args.target, (args.start_port, args.end_port), scan_udp=args.udp, timeout=args.timeout)
