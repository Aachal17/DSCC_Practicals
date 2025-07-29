import socket
from datetime import datetime

# Server address and port
SERVER_IP = 'localhost'
SERVER_PORT = 9999

# Create UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

print(f"[SERVER] Date-Time Server is running on {SERVER_IP}:{SERVER_PORT}...")

while True:
    # Receive request from client
    request_data, client_address = server_socket.recvfrom(1024)
    request_text = request_data.decode().strip()

    print(f"[SERVER] Received request: {request_text} from {client_address}")

    if request_text == "get_datetime":
        # Perform the RPC call simulation
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = f"Current Date and Time: {current_datetime}"
    else:
        response = "Error: Unknown RPC call"

    # Send response to client
    server_socket.sendto(response.encode(), client_address)
