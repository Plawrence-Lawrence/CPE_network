
import gameStateManager
import os
import socket
import select

print("Server started!")
State = gameStateManager.LAUNCHSTATE
isRunning = False
players = 2
score = 3
print("Server started!")
#server_socket = server.openServerSocket(p)

while State != gameStateManager.EXITSTATE:
    
    State, players, score, isRunning = gameStateManager.stateMachine(State, players, score, isRunning)