"""
Client for introductory socket programming in a client-server environment.

This client initiates a negotiation with a server using a request code. If a 
valid request code is provided, the server replies with a random port for 
further TCP transactions. The client then sends a message to the server and 
waits for a reversed message as a reply.
"""

import sys
import socket


def establish_tcp_connection(s_address, n_port):
    """Establish a TCP connection to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((s_address, n_port))
    return client_socket


def negotiate_udp_port(client_socket, req_code):
    """Request a UDP port for transactions from the server."""
    print("Initializing negotiation using request code")
    client_socket.send(str(req_code).encode())
    r_port = int(client_socket.recv(1024).decode())
    
    if r_port == -1:
        print("Invalid request code")
        sys.exit(1)

    print(f'Random port: {r_port}')
    return r_port


def send_receive_udp_message(s_address, r_port, msg):
    """Send a message to the server over UDP and receive the reversed message."""
    print("Initiating transaction with server")
    r_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Sending message to server")
    r_socket.sendto(msg.encode(), (s_address, r_port))
    reversed_msg = r_socket.recvfrom(2048)[0].decode()
    return reversed_msg


def validate_and_extract_args():
    """Validate command-line arguments and extract their values."""
    if len(sys.argv) != 5:
        print('Enter valid number of arguments')
        sys.exit(1)

    try:
        s_address, n_port, req_code, msg = str(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), str(sys.argv[4])
        return s_address, n_port, req_code, msg
    except ValueError:
        print("Invalid parameter type, try again.")
        sys.exit(1)


def main():
    s_address, n_port, req_code, msg = validate_and_extract_args()

    client_socket = establish_tcp_connection(s_address, n_port)
    r_port = negotiate_udp_port(client_socket, req_code)
    reversed_msg = send_receive_udp_message(s_address, r_port, msg)
    
    print("Received reversed message:", reversed_msg)


if __name__ == '__main__':
    main()
