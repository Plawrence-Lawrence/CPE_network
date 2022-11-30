#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <string.h>
#include <string>
#include <sys/time.h>

#define TRUE 1

int main(int argc, char* argv[])
{
    int clientSocket[30];
    int PORT;
    int max_sd;
    int max_clients = 30;
    int sd;
    int activity;
    int newSocket;
    int valread;
    int i;
    int addrlen;
    int opt = TRUE;

    fd_set readfds;
    char buffer[8192];
    char* message;
    std::cout << "[-->] Please Enter the port number for server to select:" << std::endl;
    std::cin >> PORT;

    for(i = 0; i < max_clients; i++)
    {
        clientSocket[i] = 0;
    }

    int serverSocket = socket(AF_INET, SOCK_STREAM, 0);

    if(serverSocket == -1)
    {
        std::cerr << "Could not create a socket |" << std::endl;
    }
    if(setsockopt(serverSocket, SOL_SOCKET, SO_REUSEADDR, (char *)&opt, sizeof(opt)) < 0)
    {
        std::cerr << "setsockopt" << std::endl;
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    inet_pton(AF_INET, "0.0.0.0", &addr.sin_addr);

    if(bind(serverSocket, (sockaddr*)&addr, sizeof(addr)) < 0)
    {
        std::cerr << "bind failed" << std::endl;
        exit( EXIT_FAILURE);
    }

    if(listen(serverSocket, 3) == 0)
    {
        std::cout << "[+]Server is ready for clients to connect on port number " << PORT << std::endl;
    }

    addrlen = sizeof(addr);

    while(TRUE)
    {
        //Clear the socket set
        FD_ZERO(&readfds);

        //add master socket to set
        FD_SET(serverSocket, &readfds);
        max_sd = serverSocket;

        //add child sockets to set
        for(i = 0; i < max_clients; i++)
        {
            sd = clientSocket[i];

            //if valid socket descriptor then add to read list
            if(sd > 0)
                FD_SET(sd, &readfds);

            if(sd > max_sd)
                max_sd = sd;
            
        }

        activity = select(max_sd + 1, &readfds, NULL, NULL, NULL);

        if((activity < 0) && (errno != EINTR))
        {
            std::cout << "select error" << std::endl;
        }

        if(FD_ISSET(serverSocket, &readfds))
        {
            if((newSocket = accept(serverSocket, (struct sockaddr*)&addr, (socklen_t*)&addrlen)) < 0)
            {
                std::cerr << "Accept" << std::endl;
            }
            std::cout << "New connection, socket fd : " << newSocket << " ip is : " << inet_ntoa(addr.sin_addr)
            << " port : " << ntohs(addr.sin_port) << std::endl;

            if( send(newSocket, message, strlen(message), 0) != strlen(message))
            {
                std::cerr << "Send Error";
            }

            for(i = 0; i < max_clients; i++)
            {
                if(clientSocket[i] == 0)
                {
                    clientSocket[i] = newSocket;
                    break;
                }
            }
        }
        for(i = 0; i < max_clients; i++)
        {
            sd = clientSocket[i];
            if(FD_ISSET(sd, &readfds))
            {
                memset(buffer, 0, 8192);
                int bytesRecieved = recv(sd, buffer, 8192, 0);
                if(bytesRecieved == -1)
                {
                    std::cerr << "Error in recv(). Quitting" << std::endl;
                    break;
                }
                if(bytesRecieved == 0)
                {
                   close(sd);
                   clientSocket[i] = 0;
                   std::cout << "Client disconnected" << std::endl;
                   break;
                }
                else
                {
                    if(bytesRecieved > 0)
                    {
                        std::cout << " Client[" << i << "]:" << std::string(buffer, 0, bytesRecieved) << std::endl;
                    }

                    for(i = 0; i < max_clients; i++)
                    {
                        sd = clientSocket[i];
                        if(sd != 0)
                        {
                            send(sd, buffer, strlen(buffer), 0);
                        }
                    }
                }
            }

        }
    }

    return 0;
}