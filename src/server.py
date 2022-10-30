import socketserver
import threading
import time
from typing import Any


# It receives data from the client, processes it, and sends it back
class Server(socketserver.BaseRequestHandler):
    def handle(self):
        """
        It receives data from the client, processes it, and sends it back
        """
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class Server:
    def __init__(self, PORT: int, HOST: str, ThreadedTCPInstace: ThreadedTCPServer) -> None:
        """
        A constructor for the class.

        :param PORT: The port you want to use for the server
        :type PORT: int
        :param HOST: The IP address of the server
        :type HOST: str
        :param ThreadedTCPInstace: This is the class that will handle the client connections
        :type ThreadedTCPInstace: ThreadedTCPServer
        """
        self.PORT = PORT
        self.HOST = HOST
        self.ThreadedTCPInstace = ThreadedTCPInstace
        self.server = ThreadedTCPServer((self.HOST, self.PORT), self.ThreadedTCPInstace)

    def run(self):
        """
        The function starts a server thread that runs in the background and listens for
        requests
        """
        with self.server:
            server_thread = threading.Thread(target=self.server.serve_forever)
            server_thread.daemon = True
            server_thread.start()

    def getIpAndHost(self):
        """
        It returns the IP address and hostname of the server
        :return: The ip and host of the server.
        """
        with self.server:
            """
            It shuts down the server
            """
            ip, host = self.server.server_address
            return (ip, host)

    def shutdown(self):
        """
        It shuts down the server
        """
        self.server.shutdown()
