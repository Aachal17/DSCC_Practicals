import socket

# Define calculator functions
def add(x, y): 
    return x + y

def sub(x, y): 
    return x - y

def mul(x, y): 
    return x * y

def div(x, y): 
    return x / y if y != 0 else "Error: Division by zero"

# Map function names to actual functions
operations = {
    'add': add,
    'sub': sub,
    'mul': mul,
    'div': div
}

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8888))
server_socket.listen(5)

print("[SERVER] Calculator RPC Server is running on port 8888...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"[SERVER] Connected to client {client_address}")

    # Receive the RPC request
    request = client_socket.recv(1024).decode().strip()
    print(f"[SERVER] Received RPC request: {request}")

    try:
        # Parse the request, e.g., "add 3 5"
        parts = request.split()
        func_name = parts[0]
        arg1 = float(parts[1])
        arg2 = float(parts[2])

        # Check if the function exists
        if func_name in operations:
            result = operations[func_name](arg1, arg2)
            response = f"Result: {result}"
        else:
            response = "Error: Unknown function"

    except Exception as e:
        response = f"Error: {str(e)}"

    # Send back the result
    client_socket.send(response.encode())
    client_socket.close()
