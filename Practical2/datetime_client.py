import socket

# Server address
SERVER_IP = 'localhost'
SERVER_PORT = 9999

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# RPC Request: simulate calling remote procedure
rpc_request = "get_datetime"
client_socket.sendto(rpc_request.encode(), (SERVER_IP, SERVER_PORT))

# Receive response from server
response_data, _ = client_socket.recvfrom(1024)
print("[CLIENT] Server Response:", response_data.decode())

# Close the socket
client_socket.close()
