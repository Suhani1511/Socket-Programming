"""
Server for introductory socket programming in a client-server environment.

This server:
    1. Creates a TCP negotiation socket and waits for clients to initiate a negotiation.
    2. Verifies client request code.
    3. If verified, establishes a UDP transaction socket and informs the client.
    4. Waits for the client's message on the UDP socket, reverses it, and sends it back.
    5. Continues to listen for new client negotiation requests.
"""

import sys
import socket


def reverse(s):
    """Return the reversed version of the input string.
    
    Args:
        s (str): String to reverse.

    Returns:
        str: Reversed string.
    """
    return s[::-1]


def tcp_negotiation(n_socket, req_code):
    """
    Process client request and create a transaction socket if verified.

    Args:
        n_socket (socket): TCP negotiation socket to listen for client requests.
        req_code (int): Request code to verify against.

    Returns:
        socket: UDP transaction socket for communication with client.
    """
    n_socket.listen(1)
    print('Server is ready to receive requests.')

    while True:
        connectionSocket, client_addr = n_socket.accept()
        code = connectionSocket.recv(1024).decode()
        
        print(f"Client request code received: {code}")
        
        if int(code) == req_code:
            print("Request code verified.")
            t_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            t_socket.bind(("", 0))
            r_port = t_socket.getsockname()[1]
            print(f"Random Port: {r_port}")
            connectionSocket.sendto(str(r_port).encode(), client_addr)
            return t_socket
        else:
            print("Request code invalid.")
            connectionSocket.sendto("-1".encode('utf-8'), client_addr)


def udp_transaction(t_socket):
    """Reverse client's message and send it back.

    Args:
        t_socket (socket): UDP socket for transaction.
    """
    print("UDP server is ready to receive.")
    message, client_addr = t_socket.recvfrom(2048)
    message = message.decode()

    print(f"Message received: {message}")

    modified_message = reverse(message)
    t_socket.sendto(modified_message.encode(), client_addr)

    print("Sent message to client. Closing connection.")
    t_socket.close()


def main():
    """Main function to manage the server operations.

    Raises:
        ValueError: If the provided port or request code is not an integer.
    """
    if len(sys.argv) != 3:
        print('Please provide valid number of arguments: <n_port> <req_code>')
        sys.exit(1)
    
    try:
        n_port = int(sys.argv[1])
        req_code = int(sys.argv[2])
    except ValueError:
        print("Invalid parameter type. Both n_port and req_code must be integers.")
        sys.exit(1)

    n_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    n_socket.bind(("", n_port))

    while True:
        t_socket = tcp_negotiation(n_socket, req_code)
        udp_transaction(t_socket)


if __name__ == '__main__':
    main()
