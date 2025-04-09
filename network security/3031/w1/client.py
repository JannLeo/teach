import socket
IP = 'x.x.x.x' #Server IP here
PORT = 5037
ADDR = (IP, PORT)
SIZE = 1024
FILENAME = "secret.txt"

def main():
    # Staring a TCP socket. 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to the server. 
    client.connect(ADDR)

    # Sending the filename to the server. 
    client.send(FILENAME.encode("utf-8"))

    # Receive data from server
    msg = client.recv(SIZE).decode("utf-8")
    print(f"[SERVER]: {msg}")

    # Opening and reading the file data in binary 


    # Sending the file data to the server. 


    # Closing the file. 


    # Receive data from server
    msg = client.recv(SIZE).decode("utf-8")
    print(f"[SERVER]: {msg}")

    # Closing the connection from the server. 
    client.close()
if __name__ == "__main__":
    main()