import socket
IP = 'x.x.x.x' #Listening IP on server
PORT = 5037
ADDR = (IP, PORT)
SIZE = 1024
def main():
    print("[STARTING] Server is starting.")
    # Staring a TCP socket. 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the IP and PORT to the server. 
    server.bind(ADDR)
    # Server is listening, i.e., server is now waiting for the client to connected. 
    server.listen()

    print("[LISTENING] Server is listening.")
    while True:
        # Server has accepted the connection from the client. 
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        # Receiving the filename from the client. 
        filename = conn.recv(SIZE).decode("utf-8")
        print(f"[RECV] Receiving the filename.")
        conn.send("Filename received.".encode("utf-8"))

        # Receiving the file data from the client. 
        data = conn.recv(SIZE)
        print(f"[RECV] Receiving the file data.")

        # Create a file to write in binary


        #Receive data from client


        # Closing the file. 


        # Closing the connection from the client. 
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

if __name__ == "__main__":
    main()