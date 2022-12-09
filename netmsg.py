import socket
import select
import sys

HEADER_LENGTH = 10
MSG_LEN = 10
def receive_message(client_socket):
	message = client_socket.recv(1024).decode('utf-8')
	return message
    
def send_to_one(receiver, message):
    try:
        receiver.send(bytes(message, 'utf-8'))
    except:
        receiver.close()
        

def send_to_all(server, message, client_list):
    for socket in client_list:
        if (socket != server):
            try:
                socket.send(bytes(message, 'utf-8'))
            except:
                socket.close()

def openHostSocket(queuSize, port):
    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # SO_ - socket option
    # SOL_ - socket option level
    # Sets REUSEADDR (as a socket option) to 1 on socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind, so server informs operating system that it's going to use given IP and port
    # For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
    server_socket.bind((socket.gethostname(), port))

    # This makes server listen to new connections
    server_socket.listen(queuSize)
    return server_socket
# Handles message receiving