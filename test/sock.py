import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

a = s.connect(("localhost", 9000))

print(a)
