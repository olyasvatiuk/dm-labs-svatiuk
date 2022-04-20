import numpy as np
from tabulate import tabulate

class Graph():
    def __init__(self, G, size):
        self.G = G
        self.size = size
        self.ROW = 0
        
    def print_graph(self):
        print("Вхідна матриця суміжності:")
        print(np.array(self.G))
        print()
    
    def start_algorithm(self):
        edges = []
        for i in range(self.size):
            for j in range(0, self.size):
                if self.G[i][j] != 0:
                    edges.append([i, j])
        
        self.ROW = len(self.G)
        parent = [-1] * (self.ROW)
        if self.searching_algo_BFS(0, len(self.G)-1, parent) == True:
            print("В графі є потік з вершини 1 в вершину " + str(self.size) + ":")
            print()
            self.ford_fulkerson(0, self.size-1)
            
            flow_mat = []
            for i in range(len(self.G)):
                temp = []
                for j in range(0, len(self.G[i])):
                    if [i, j] in edges:
                        temp.append(str(self.G[i][j]) + "/" + str(self.G[j][i]))
                    else:
                        temp.append(str(0))
                flow_mat.append(temp)
            
            print("\nМатриця потоків:")
            print(tabulate(flow_mat, tablefmt="grid"))
                        
        else:
            print("В графі немає потоку з вершини 1 в вершину " + str(self.size) + ", змініть граф!!!")
        print()
    
    def searching_algo_BFS(self, s, t, parent):
        visited = [False] * (self.ROW)
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(self.G[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
        return True if visited[t] else False

    def ford_fulkerson(self, source, destination):
        parent = [-1] * (self.ROW)
        max_flow = 0

        ctr = 1
        while self.searching_algo_BFS(source, destination, parent):
            path_flow = float("Inf")
            s = destination
            path = []
            path_weight = []
            while(s != source):
                path.append([parent[s]+1, s+1])
                path_weight.append(self.G[parent[s]][s])
                path_flow = min(path_flow, self.G[parent[s]][s])
                s = parent[s]
            
            temp = "1"
            for i in range(len(path)-1, -1, -1):
                temp += " - (" + str(path_weight[i]) + ") - " + str(path[i][1])
            temp += " - Мінімальне: " + str(path_flow)
            print("Потік №" + str(ctr) + ": ")
            print(temp)
            
            max_flow += path_flow
            ctr += 1
            
            v = destination
            while(v != source):
                u = parent[v]
                self.G[u][v] -= path_flow
                self.G[v][u] += path_flow
                v = parent[v]
        print("\nЗначення максимального потоку: " + str(max_flow))

if __name__ == "__main__":
    G = []
    size = 0
    with open('l4-1.txt') as file:
        for n, line in enumerate(file):
            if n == 0:
                size = int(line.strip())
            else:
                b = line.strip()
                b = b.split(' ')
                b = [int(i) for i in b]
                G.append(b)
    
    graph = Graph(G, size)
    graph.print_graph()
    graph.start_algorithm()