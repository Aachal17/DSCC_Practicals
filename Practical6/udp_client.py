# File: udp_client.py

import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("localhost", 9999)

    try:
        a = int(input("Enter value of a: "))
        b = int(input("Enter value of b: "))

        message = f"a={a};b={b}"
        client_socket.sendto(message.encode(), server_address)

        data, _ = client_socket.recvfrom(1024)
        print("Server response:", data.decode())

    except Exception as e:
        print("Error:", str(e))

    finally:
        client_socket.close()

# Run the client
if __name__ == "__main__":
    start_client()
