# Is a clinet for testing server.py

import socket

def client(ip, port, message):
    """
    It creates a socket, connects to the server, sends a message, and receives a response
    
    :param ip: The IP address of the server
    :param port: The port number that the server is listening on
    :param message: The message to send to the server
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))
