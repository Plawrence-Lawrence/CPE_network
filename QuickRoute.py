
#Author: Pearson Lawrence
#Finished: 12/10/2022
#The main executable file that runs the game state machine
import gameStateManager  #Custom file

State = gameStateManager.LAUNCHSTATE    #Default state for the gameStateManager state machine to start in
players = 2                             #Default players allowed in a match
score = 3                               #Default max score that players play to

#State Machine Loop. Run until told to stop
while State != gameStateManager.EXITSTATE:
    
    #Variables are created to pass into state machine to ensure state machine is updated properly
    State, players, score = gameStateManager.stateMachine(State, players, score)