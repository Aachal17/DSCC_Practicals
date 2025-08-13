# File: udp_server.py

import socket

def calculate_expression(a, b):
    return (a * a) - (2 * a * b) + (b * b)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("localhost", 9999))
    print("UDP Server is running on port 9999...")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        message = data.decode()
        print(f"Received from client: {message}")

        try:
            # Expected message format: "a=5;b=2"
            parts = message.strip().split(";")
            a = int(parts[0].split("=")[1])
            b = int(parts[1].split("=")[1])

            result = calculate_expression(a, b)
            response = f"Result: {result}"
        except Exception as e:
            response = f"Error: {str(e)}"

        server_socket.sendto(response.encode(), client_address)
        print(f"Sent back to client: {response}")

# Run the server
if __name__ == "__main__":
    start_server()
