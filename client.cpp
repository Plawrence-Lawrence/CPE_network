#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <string.h>
#include <string>
#include <sys/time.h>

int main()
{
    int port;
    int clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if(clientSocket == -1)
    {
        return 1;
    }

    std::cout << "Type the port address you want to connect : " << std::endl;
    std::cin >> port;
    std::string ipAddress = "127.0.0.1";

    sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port);
        inet_pton(AF_INET,ipAddress.c_str(), &addr.sin_addr);
    
    int connectRes = connect(clientSocket, (sockaddr*)&addr, sizeof(addr));

    if(connectRes == 0)
    {
        std::cout << "You have conected to server |" << std::endl;
    }
    if(connectRes == -1)
        return 1;
    
    char buf[4096];
    std::string userInput;

    do{
        getline(std::cin, userInput);
        int sendRes = send(clientSocket, userInput.c_str(), userInput.size() + 1, 0);
        if(sendRes = -1)
        {
            std::cout << "Could not send to server! Whoops!\r\n";
            continue;
        }

    }while(true);
}