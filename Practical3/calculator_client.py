import socket

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8888))

# Simulate an RPC request
# Example inputs: 'add 10 20', 'div 10 0', 'mul 4 5'
rpc_call = input("Enter RPC call (e.g., add 3 5): ")
client_socket.send(rpc_call.encode())

# Receive and display the response
response = client_socket.recv(1024).decode()
print("[CLIENT] Server Response:", response)

client_socket.close()
