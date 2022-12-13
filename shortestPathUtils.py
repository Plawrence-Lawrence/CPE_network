import random

class Graph():
 
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
 
    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):
 
        # Initialize minimum distance for next node
        min = 1e7
 
        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index
 
    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src, end):
 
        dist = [1e7] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
 
        for cout in range(self.V):
 
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)
 
            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True
 
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                   sptSet[v] == False and
                   dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]
 
        return dist[end]

def genGraph(choice):
    node = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    if choice == 1:
        start = random.randint(0,12)
        startNode = node[start]
        end = random.randint(0,12)
        while start == end:
            end = random.randint(0,12)
        endNode = node[end]
        adjMatrix = createMatrix(choice)
        g = Graph(13)
        g.graph = adjMatrix
        SPD =g.dijkstra(start, end)
        graph = storeDecision(choice, adjMatrix)
        return startNode, endNode, graph, str(SPD)
    if choice == 2:
        start = random.randint(0,3)
        startNode = node[start]
        end = random.randint(0,3)
        while start == end:
            end = random.randint(0,3)
        endNode = node[end]
        adjMatrix = createMatrix(choice)
        print(adjMatrix)
        g = Graph(4)
        g.graph = adjMatrix
        SPD = g.dijkstra(start, end)
        graph = storeDecision(choice, adjMatrix)
        return startNode, endNode, graph, str(SPD)
    if choice == 3:
        start = random.randint(0,6)
        startNode = node[start]
        end = random.randint(0,6)
        while start == end:
            end = random.randint(0,6)
        endNode = node[end]
        adjMatrix = createMatrix(choice)
        g = Graph(7)
        g.graph = adjMatrix
        SPD = g.dijkstra(start, end)
        graph = storeDecision(choice, adjMatrix)
        return startNode, endNode, graph, str(SPD)
    if choice == 4:
        start = random.randint(0,5)
        startNode = node[start]
        end = random.randint(0,5)
        while start == end:
            end = random.randint(0,5)
        endNode = node[end]
        adjMatrix = createMatrix(choice)
        g = Graph(6)
        g.graph = adjMatrix
        SPD = g.dijkstra(start, end)
        graph = storeDecision(choice, adjMatrix)
        return startNode, endNode, graph, str(SPD)
        
#Takes in a choice and makes a adjacency matrix of distance between nodes
def createMatrix(choice):
    if choice == 1:
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
                  
        for x in range(0,12):
            for y in range(0,12):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[x][y] = Matrix[x][y] * temp
        
        for x in range(0,12):
            for y in range(0,12):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[y][x] = Matrix[x][y]

        return Matrix
    if choice == 2:
        Matrix = [[0, 1, 1, 0],
                  [1, 0, 0, 1],
                  [1, 0, 0, 1],
                  [0, 1, 1, 0]]
        for x in range(0,3):
            for y in range(0,3):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[x][y] = Matrix[x][y] * temp
        for x in range(0,3):
            for y in range(0,3):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[y][x] = Matrix[x][y]
        return Matrix
    if choice == 3:
        Matrix = [[0, 1, 0, 0, 0, 0, 0],
                  [1, 0, 1, 1, 0, 0, 0],
                  [0, 1, 0, 1, 0, 0, 0],
                  [0, 1, 1, 0, 1, 1, 0],
                  [0, 0, 0, 1, 0, 1, 0],
                  [0, 0, 0, 1, 1, 0, 1],
                  [0, 0, 0, 0, 0, 1, 0]]
        for x in range(0,6):
            for y in range(0,6):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[x][y] = Matrix[x][y] * temp
        for x in range(0,6):
            for y in range(0,6):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[y][x] = Matrix[x][y]
        return Matrix
    if choice == 4:
        Matrix = [[0, 0, 1, 0, 1, 0],
                  [0, 0, 1, 1, 0, 0],
                  [1, 1, 0, 1, 1, 1],
                  [0, 1, 1, 0, 0, 1],
                  [1, 0, 1, 0, 0, 0],
                  [0, 0, 1, 1, 0, 0]]
        for x in range(0,5):
            for y in range(0,5):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[x][y] = Matrix[x][y] * temp
        for x in range(0,5):
            for y in range(0,5):
                if x != y:
                    temp = random.randint(1,9)
                    Matrix[y][x] = Matrix[x][y]
        return Matrix
        
def storeDecision(choice, Matrix):
    if choice == 1:
        #print("                                                            \n")
        #print("                 A--------------------B--------------------C\n")
        #print("                /|\                   |                   /|\\n")
        #print("               / | \                  |                  / | \\n")
        #print("              /  |  \                 |                 /  |  \\n")
        #print("             /   |   \                |                /   |   \\n")
        #print("            /    |    \               |               /    |    \\n")
        #print("           /     |     \              |              /     |     \\n")
        #print("          D------E------F             G             H------I------J\n")
        #print("           \     |     /              |              \     |     /\n")
        #print("            \    |    /               |               \    |    /\n")
        #print("             \   |   /                |                \   |   /\n")
        #print("              \  |  /                 |                 \  |  /\n")
        #print("               \ | /                  |                  \ | /\n")
        #print("                \|/                   |                   \|/\n")
        #print("                 K--------------------L--------------------M")
        #print("                                                                \n")
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
        #print("                A                \n")
        #print("               / \               \n")
        #print("              /   \              \n")
        #print("             /     \             \n")
        #print("            /       \            \n")
        #print("           /         \           \n")
        #print("          B           C          \n")
        #print("           \         /           \n")
        #print("            \       /            \n")
        #print("             \     /             \n")
        #print("              \   /              \n")
        #print("               \ /               \n")
        #print("                D                \n")
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
        #print("A\n")
        #print(" \\n")
        #print("  \\n")
        #print("   \\n")
        #print("    B-----------C \n")
        #print("     \         / \n")
        #print("      \       / \n")
        #print("       \     / \n")
        #print("        \   / \n")
        #print("         \ / \n")
        #print("          D \n")
        #print("         / \ \n")
        #print("        /   \ \n")
        #print("       /     \ \n")
        #print("      /       \ \n")
        #print("     /         \ \n")
        #print("    E-----------F \n")
        #print("                 \ \n")
        #print("                  \ \n")
        #print("                   \ \n")
        #print("                    G \n")
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
        #print("A             B \n")
        #print("|\           / \ \n")
        #print("| \         /   \ \n")
        #print("|  \       /     \ \n")
        #print("|   \     /       \ \n")
        #print("|    \   /         \ \n")
        #print("|     \ /           \ \n")
        #print("|      C-------------D \n")
        #print("|     / \           / \n")
        #print("|    /   \         / \n")
        #print("|   /     \       / \n")
        #print("|  /       \     / \n")
        #print("| /         \   / \n")
        #print("|/           \ / \n")
        #print("E             F \n")
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
        