#Author: Richard Cao
#Date: 12/12/2022
#Purpose: The purpose of this file is to create functionality, enabling a program to create one of four premade network routing graphs, Randomly generate the distances 
#between nodes in said routing graphuse, and then Dijkstra's algorithm to find the path between two randomly selected nodes in the routing graph. Functionality
#Is meant to be returned as function calls elsewhere 
import random

class Graph():
 
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
 
    # A utility function to find the vertex with minimum distance value, from the set of vertices not yet included in shortest path tree
    def minDistance(self, dist, sptSet):
 
        # Initialize minimum distance for next node
        min = 1e7
 
        # Search not nearest vertex not in the shortest path tree
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index
 
    # Function that implements Dijkstra's single source shortest path algorithm for a graph represented using adjacency matrix representation
    def dijkstra(self, src, end):
 
        dist = [1e7] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
 
        for cout in range(self.V):
 
            # Pick the minimum distance vertex from the set of vertices not yet processed. u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)
 
            # Put the minimum distance vertex in the shortest path tree
            sptSet[u] = True
 
            # Update dist value of the adjacent vertices of the picked vertex only if the current distance is greater than new distance and the vertex in not in the shortest path tree
            for v in range(self.V):
                if (self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v] #Stores the current distance with the newly added distance
 
        return dist[end] #returns the distance from the start node to the end node

def genGraph(choice):
    node = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    if choice == 1:
        #Makes a matrix if the selection is the first graph
        start = random.randint(0,12)         #Generates the starting number from 0-12
        startNode = node[start]              #Stores the starting node based off of the starting number
        end = random.randint(0,12)           #Generates the ending number from 0-12
        while start == end:                  #Checks to see if the start is the same as the end
            end = random.randint(0,12)       #If it is the same then it finds a new number
        endNode = node[end]                  #Stores the ending node based off of the ending number
        adjMatrix = createMatrix(choice)     #Makes the adjacency Matrix
        g = Graph(13)                        #Makes a graph of 13 Nodes
        g.graph = adjMatrix                  #Sets the adjacency matrix of the graph to the randomly made adjacency matrix
        SPD =g.dijkstra(start, end)                 #Runs the algorithm to find the shortest distance from one node to another
        graph = storeDecision(choice, adjMatrix)    #Stores the graph in a string so that it will print in the terminal
        return startNode, endNode, graph, str(SPD)  #returns all the variables to send to the client
    if choice == 2:
        #Makes a matrix if the selection is the second graph
        start = random.randint(0,3)      #Gernerates the starting number from 0-3
        startNode = node[start]          #Stores the starting node based on the starting number
        end = random.randint(0,3)        #Generates the end number from 0-3
        while start == end:              #Checks to make sure that the starting number isn't the same as the ending number
            end = random.randint(0,3)    #Regenerates a random number from 0-3 to make sure the ending number is different
        endNode = node[end]              #Stores the ending node based on the end number
        adjMatrix = createMatrix(choice) #Makes the adhjacency matrix
        g = Graph(4)                     #Makes a graph of 4 nodes
        g.graph = adjMatrix              #Sets the graph adjacency matrix to the randomly made adjacency matrix
        SPD = g.dijkstra(start, end)               #Runs the algorithm to find the shortest distance from the start node to end node
        graph = storeDecision(choice, adjMatrix)   #Stores the graph in a string so that it will print in the terminal
        return startNode, endNode, graph, str(SPD) #returns all the variables to send to the client
    if choice == 3:
        #Makes a matrix if the selection is the third graph
        start = random.randint(0,6)         #Gernerates the starting number from 0-6
        startNode = node[start]             #Stores the starting node based on the starting number
        end = random.randint(0,6)           #Generates the end number from 0-6
        while start == end:                 #Checks to make sure that the starting number isn't the same as the ending number
            end = random.randint(0,6)       #Regenerates a random number from 0-6 to make sure the ending number is different
        endNode = node[end]                 #Stores the ending node based on the end number
        adjMatrix = createMatrix(choice)    #Makes the adhjacency matrix
        g = Graph(7)                        #Makes a graph of 7 nodes
        g.graph = adjMatrix                 #Sets the graph adjacency matrix to the randomly made adjacency matrix
        SPD = g.dijkstra(start, end)               #Runs the algorithm to find the shortest distance from the start node to end node
        graph = storeDecision(choice, adjMatrix)   #Stores the graph in a string so that it will print in the terminal
        return startNode, endNode, graph, str(SPD) #returns all the variables to send to the client
    if choice == 4:
        #Makes a matrix if the selection is the fourth graph
        start = random.randint(0,5)         #Gernerates the starting number from 0-5
        startNode = node[start]             #Stores the starting node based on the starting number
        end = random.randint(0,5)           #Generates the end number from 0-5
        while start == end:                 #Checks to make sure that the starting number isn't the same as the ending number
            end = random.randint(0,5)       #Regenerates a random number from 0-5 to make sure the ending number is different
        endNode = node[end]                 #Stores the ending node based on the end number
        adjMatrix = createMatrix(choice)    #Makes the adhjacency matrix
        g = Graph(6)                        #Makes a graph of 6 nodes
        g.graph = adjMatrix                 #Sets the graph adjacency matrix to the randomly made adjacency matrix
        SPD = g.dijkstra(start, end)                #Runs the algorithm to find the shortest distance from the start node to end node
        graph = storeDecision(choice, adjMatrix)    #Stores the graph in a string so that it will print in the terminal
        return startNode, endNode, graph, str(SPD)  #returns all the variables to send to the client
        
#Takes in a choice and makes a adjacency matrix of distance between nodes
def createMatrix(choice):
    if choice == 1:
        #Makes an array that stores 1 if there is a connection between nodes and 0 if there isn't
        #The matrix has indexes 0-12, these indexes correspond to the Nodes A-M respectively
        Matrix = [[0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                  [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                  [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                  [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                  [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                  [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                  [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                  [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                  [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
                  [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0]]
        #Generate random numbers between 1 and 9 to store into the one half of the adjacency matrix          
        for x in range(0,12):
            for y in range(0,12):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[x][y] = Matrix[x][y] * temp
        #Fill the other half with the same corresponding numbers
        for x in range(0,12):
            for y in range(0,12):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[y][x] = Matrix[x][y]

        return Matrix
    if choice == 2:
        #Makes an array that stores 1 if there is a connection between nodes and 0 if there isn't
        #The matrix has indexes 0-3, these indexes correspond to the nodes A-D respectively
        Matrix = [[0, 1, 1, 0],
                  [1, 0, 0, 1],
                  [1, 0, 0, 1],
                  [0, 1, 1, 0]]
        #Generate random numbers between 1 and 9 to store into the one half of the adjacency matrix
        for x in range(0,3):
            for y in range(0,3):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[x][y] = Matrix[x][y] * temp
        #Fill the other half with the same corresponding numbers
        for x in range(0,3):
            for y in range(0,3):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[y][x] = Matrix[x][y]
        return Matrix
    if choice == 3:
        #Makes an array that stores 1 if there is a connection between nodes and 0 if there isn't
        #The matrix has indexes 0-6, these indexes correspond to the nodes A-G respectively
        Matrix = [[0, 1, 0, 0, 0, 0, 0],
                  [1, 0, 1, 1, 0, 0, 0],
                  [0, 1, 0, 1, 0, 0, 0],
                  [0, 1, 1, 0, 1, 1, 0],
                  [0, 0, 0, 1, 0, 1, 0],
                  [0, 0, 0, 1, 1, 0, 1],
                  [0, 0, 0, 0, 0, 1, 0]]
        #Generate random numbers between 1 and 9 to store into the one half of the adjacency matrix
        for x in range(0,6):
            for y in range(0,6):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[x][y] = Matrix[x][y] * temp
        #Fill the other half with the same corresponding numbers
        for x in range(0,6):
            for y in range(0,6):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[y][x] = Matrix[x][y]
        return Matrix
    if choice == 4:
        #Makes an array that stores 1 if there is a connection between nodes and 0 if there isn't
        #The matrix has indexes 0-5, these indexes correspond to the nodes A-F respectively
        Matrix = [[0, 0, 1, 0, 1, 0],
                  [0, 0, 1, 1, 0, 0],
                  [1, 1, 0, 1, 1, 1],
                  [0, 1, 1, 0, 0, 1],
                  [1, 0, 1, 0, 0, 0],
                  [0, 0, 1, 1, 0, 0]]
        #Generate random numbers between 1 and 9 to store into the one half of the adjacency matrix
        for x in range(0,5):
            for y in range(0,5):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[x][y] = Matrix[x][y] * temp
        #Fill the other half with the same corresponding numbers
        for x in range(0,5):
            for y in range(0,5):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[y][x] = Matrix[x][y]
        return Matrix

#Makes a graph based on the adj matrix and the graph choice
def storeDecision(choice, Matrix):
    if choice == 1:
        #Develops a 13 node array of strings that store a graph with the distance based off the adjacency matrix
        graphArray = ["                 " + str(Matrix[0][1])  + "                      " + str(Matrix[1][2]) + "              ",
                      "       A--------------------B--------------------C",
                      "      /|\                   |                   /|\\",
                      "     / | \                  |                  / | \\",
                      "    /  |  \                 |                 /  |  \\",
                      "  " + str(Matrix[0][3]) + "/   |" + str(Matrix[0][4]) + "  \\"+ str(Matrix[0][5]) + "               |" + str(Matrix[1][6]) + "              " + str(Matrix[2][7])+"/   |"+str(Matrix[2][8])+"  \\"+str(Matrix[2][9]),
                      "  /    |    \               |               /    |    \\",
                      " /  "+str(Matrix[3][4])+"  |  "+str(Matrix[4][5])+"  \              |              /  "+str(Matrix[7][8])+"  |  "+str(Matrix[8][9])+"  \\",
                      "D------E------F             G             H------I------J",
                      " \     |     /              |              \     |     /",
                      "  \    |    /               |               \    |    /",
                      "   \   |   /                |                \   |   /",
                      "   "+str(Matrix[3][10])+"\  |"+str(Matrix[4][10])+" /"+str(Matrix[5][10])+"                |"+str(Matrix[6][11])+"               "+str(Matrix[7][12])+"\  |"+str(Matrix[8][12])+" /"+str(Matrix[9][12]),
                      "     \ | /                  |                  \ | /",
                      "      \|/                   |                   \|/",
                      "       K--------------------L--------------------M",
                      "                  "+str(Matrix[10][11])+"                    "+str(Matrix[11][12])+"         "]
        return graphArray
    elif choice == 2:
        #Develops a 4 node array of strings that store a graph with the distance based off the adjacency matrix
        graphArray = ["                A                \n", 
                      "               / \               \n", 
                      "              /   \              \n", 
                      "           "+ str(Matrix[0][1]) + " /     \ " + str(Matrix[0][2]) + "           \n", "            /       \            \n", 
                      "           /         \           \n", 
                      "          B           C          \n", 
                      "           \         /           \n", 
                      "            \       /            \n", 
                      "           " + str(Matrix[1][3]) + " \     / " + str(Matrix[2][3]) + "          \n", 
                      "              \   /              \n", 
                      "               \ /               \n", 
                      "                D                \n"]
        return graphArray
    elif choice == 3:
        #Develops a 7 node array of strings that store a graph with the the distance based off the adjacency matrix
        graphArray = ["A",
                      " \\",
                      " "+str(Matrix[0][1])+"\\",
                      "   \\      "+str(Matrix[1][2]),
                      "    B-----------C ",
                      "     \         / ",
                      "      \       / ",
                      "      "+str(Matrix[1][3])+"\     /"+str(Matrix[2][3]),
                      "        \   / ",
                      "         \ / ",
                      "          D ",
                      "         / \ ",
                      "        /   \ ",
                      "      "+str(Matrix[3][4])+"/     \\"+str(Matrix[3][5]),
                      "      /       \ ",
                      "     /         \ ",
                      "    E-----------F ",
                      "          "+str(Matrix[4][5])+"      \ ",
                      "                  \\"+str(Matrix[5][6]),
                      "                   \ ",
                      "                    G "]
        return graphArray
    else:
        #Develops an array of strings that have the 6 node graph with all the distances from the adjacency matrix
        graphArray = [" A             B ",
                      " |\           / \ ",
                      " | \         /   \ ",
                      " |  \\"+str(Matrix[0][2])+"     "+str(Matrix[1][2])+"/     \\"+str(Matrix[1][3]),
                      " |   \     /       \ ",
                      " |    \   /         \ ",
                      " |     \ /      "+str(Matrix[2][3])+"    \ ",
                      str(Matrix[0][4])+"|      C-------------D ",
                      " |     / \           / ",
                      " |    /   \         / ",
                      " |   /     \       / ",
                      " |  /"+str(Matrix[2][4])+"     "+str(Matrix[2][5])+"\     /"+str(Matrix[3][5]),
                      " | /         \   / ",
                      " |/           \ / ",
                      " E             F "]
        return graphArray
        