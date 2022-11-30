import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.56.1", 1233))

msg = s.recv(1024)
print(msg.decode("utf-8"))