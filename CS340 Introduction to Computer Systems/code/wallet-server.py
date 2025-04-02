import threading
import socket
from wallet import Wallet

wallet = Wallet() # the only global variable you should use

def handle_client(client_socket):
    with client_socket:#management context
        buffer = ''
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.replace('\r', '').strip() 
                    if not line:
                        continue

                    parts = line.split()
                    cmd = parts[0]
                    #Call different methods of the wallet 
                    if cmd == 'GET':
                        resource = parts[1]
                        result = wallet.get(resource)
                        client_socket.sendall(f"{result}\n".encode())

                    elif cmd == 'MOD':
                        resource = parts[1]
                        delta = int(parts[2])
                        result = wallet.change(resource, delta)
                        client_socket.sendall(f"{result}\n".encode())

                    elif cmd == 'TRY':
                        resource = parts[1]
                        delta = int(parts[2])
                        result = wallet.try_change(resource, delta)
                        client_socket.sendall(f"{result}\n".encode())

                    elif cmd == 'TRAN':
                        args = {}
                        for i in range(1, len(parts), 2):
                            resource = parts[i]
                            delta = int(parts[i + 1])
                            args[resource] = delta
                        result = wallet.transaction(**args)
                        client_socket.sendall(f"{result}\n".encode())

                    elif cmd == 'EXIT':
                        return
            except Exception:
                break 
            
def create_wallet_server(local_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', local_port))
    server_socket.listen(100)
    print(f"Wallet server listening on port {local_port}")

    try:
        while True:
            client_socket, _ = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
    finally:
        server_socket.close()
if __name__ == '__main__':
    # parses command-line arguments, ensuring all implementations are invoked the same way
    import getopt
    import sys

    local_port = 34000
    optlist, args = getopt.getopt(sys.argv[1:], 'p:')
    for arg in optlist:
        if arg[0] == '-p': local_port = int(arg[1])
    print("Launching wallet server on :"+str(local_port))
    create_wallet_server(local_port)
