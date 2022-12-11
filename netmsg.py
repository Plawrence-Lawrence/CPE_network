#Author: Pearson Lawrence
#finished: 12/10/2022
#this program stores the defanition for connecting to sockets, opening sockets, sending and receiving from sockets using TCP
import socket

#receive_message: Takes in a socket to receive message from.
def receive_message(client_socket):
    
    try: #Try to receive
        message = client_socket.recv(1024).decode('utf-8') #receive message on client socket of size 1024 bytes chunks at a time, decode bytes as utf-8 bytes
                                                           #Store in message variable
    except:#Otherwise throw exception
        print("message could not be received")
        return "error" #Return error to propgate string value to avoid crash
    return message #Return message received
    
#send_to_one: Takes in a socket (receiver), and a string (message), calls send on the socket and cast the string to bytes of type utf-8
#Sends message to desired socket.
#Uses Unicasting
def send_to_one(receiver, message):
    try: #Try to send
        receiver.send(bytes(message, 'utf-8'))  #Sends message casted to utf-8 bytes
        return True
    except:#If failed to send then close socket
        print("message could not be sent")
        receiver.close()
        return False
        
#send_to_all: This function takes in the "server" (the one to multicast), a message to send, and a list of sockets
# The server should be in the list of sockets so it needs to be passed in to send message to all clients besides server
# Uses multicasting to send the same message to multiple users
def send_to_all(server, message, client_list):
    for socket in client_list: #For each socket in client list
        if (socket != server): #Only if not server socket
            try: #Try to send message as utf-8 bytes to current socket in loop
                socket.send(bytes(message, 'utf-8')) 
            except: #If msg could not be sent, close the current socket
                print("message could not be sent")
                socket.close()

#open_host_socket: takes in a queue size for clients joining, and a port to open on the host machine
# Opens socket on port and listens for connections of queue size
def open_host_socket(queuSize, port):
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
                                                                      # socket.AF_INET = IPV4
                                                                      # socket.SOCK_STREAM = TCP

    
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Sets socket option REUSEADDR to 1 on socket
                                                                        # SO_ = socket option, SOL_ = socket option level
                                                                        # Reauseaddr allows server to start listening and bundling well know ports
    
    server_socket.bind((socket.gethostname(), port)) # Binds port so server knows to listen for connections on specific port, and use specific ip
     
   
    server_socket.listen(queuSize) #makes bound socket listen for connections for allowed connection queue size
    return server_socket #returns out the opened socket


#connect_to_socket: Connects to a host socket based on IP and PORT
# Will return out the socket that has been connected to
def sonnect_to_socket(IP, PORT):

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
                                                                     # socket.AF_INET = address family IPV4
                                                                     # socket.SOCK_STREAM - TCP
    #Try taking new socket and connecting it to a remote socket
    try:
        serversocket.connect((IP, PORT)) #Connects socket to socket with IP and PORT number
    except: #If fail, then could not connect to remote socket (Check IP and PORT, make sure remote host allows connections)
        print("CAN'T CONNECT! (Check IP and PORT, make sure remote host allows connections)")
        return serversocket, False #Return out socket, and False for the connection failing
	
    serversocket.setblocking(False) # Connection = non-blocking state.
                                    # So .recv() call won't block and will return an only return an exception

    return serversocket, True #Return the socket connected to, and True for successful connection