import socket
from datetime import datetime

# Function to return current date and time
def get_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Server setup
SERVER_IP = 'localhost'
SERVER_PORT = 9000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

print(f"[SERVER] Date-Time RPC Server is running on {SERVER_IP}:{SERVER_PORT}...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"[SERVER] Connected to {client_address}")

    # Receive the RPC call request
    request = client_socket.recv(1024).decode().strip()
    print(f"[SERVER] RPC Request received: {request}")

    if request == "get_datetime":
        result = get_datetime()
        response = f"Server Date and Time: {result}"
    else:
        response = "Error: Unknown RPC function"

    # Send response
    client_socket.send(response.encode())
    client_socket.close()
