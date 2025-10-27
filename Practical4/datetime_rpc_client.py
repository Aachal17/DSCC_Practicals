import socket

# Client setup
SERVER_IP = 'localhost'
SERVER_PORT = 9000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Simulate the RPC call
rpc_function = "get_datetime"
client_socket.send(rpc_function.encode())

# Receive and print the result
response = client_socket.recv(1024).decode()
print("[CLIENT] Server Response:", response)

client_socket.close()
