import socket

class Client:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.connecting()

    def connecting(self):
        global S
        S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        S.connect((self.host, self.port))
        print(S)

    # def sendMessage(self, message: str) -> None:
    #     self.s.sendall(bytes(message, 'ascii'))
    #     response = str(self.s.recv(1024), 'ascii')
    #     print(response)
