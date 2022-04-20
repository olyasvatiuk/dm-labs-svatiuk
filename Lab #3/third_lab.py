import numpy as np
import math
from tabulate import tabulate

class Graph():
    def __init__(self, G, size):
        self.G = G
        self.size = size
        self.final_path = []
        self.visited = []
        self.final_res = 0
    
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
        
        odd_oddness = self.get_odd()
        for i in range(self.size):
            print("Вузол " + str(i+1) + " має " + str(odd_oddness[i]) + " степінь")
        print()
        
        temp_state = []
        for el in odd_oddness:
            if el > 1:
                temp_state.append(True)
            else:
                temp_state.append(False)        
        if all(temp_state) == False or self.size < 3:
            print("В графі немає Гамільтонового циклу!!!")
        else:
            print("В графі є Гамільтоновий цикл!!!")
            print()
            self.final_path = [None] * (self.size + 1)
            self.visited = [False] * self.size
            self.final_res = float('inf')
            
            self.TSP()            
            
            temp = ''
            for i in range(len(self.final_path)):
                temp += str(self.final_path[i]+1) + ' --> '
            temp = temp[:-5]
            print("Результати знаходження Гамільтонового цикл:")
            print(temp)
            print("\nСума ребер Гамільтонового циклу: " + str(self.final_res)) 
            
            final_path_nodes = []
            for i in range(len(self.final_path)-1):
                final_path_nodes.append([self.final_path[i], self.final_path[i+1]])
            
            matrix_cycle = []
            for i in range(self.size):
                temp = []
                for j in range(self.size):
                    if [i, j] in final_path_nodes:
                        temp.append(self.G[i][j])
                    elif [j, i] in final_path_nodes:
                        temp.append(self.G[j][i])
                    else:
                        temp.append(0)
                matrix_cycle.append(temp)
            
            print("\nМатриця Гамільтонового циклу:")
            print(tabulate(matrix_cycle, tablefmt="grid"))
    
    def TSPRec(self, curr_bound, curr_weight, level, curr_path):
        if level == self.size:
            if self.G[curr_path[level - 1]][curr_path[0]] != 0:
                curr_res = curr_weight + self.G[curr_path[level - 1]]\
                                            [curr_path[0]]
                if curr_res < self.final_res:
                    self.copyToFinal(curr_path)
                    self.final_res = curr_res
            return
      
        for i in range(self.size):
            if (self.G[curr_path[level-1]][i] != 0 and self.visited[i] == False):
                temp = curr_bound
                curr_weight += self.G[curr_path[level - 1]][i]
      
                if level == 1:
                    curr_bound -= ((self.firstMin(curr_path[level - 1]) + 
                                    self.firstMin(i)) / 2)
                else:
                    curr_bound -= ((self.secondMin(curr_path[level - 1]) +
                                     self.firstMin(i)) / 2)
      
                if curr_bound + curr_weight < self.final_res:
                    curr_path[level] = i
                    self.visited[i] = True
                      
                    self.TSPRec(curr_bound, curr_weight, level + 1, curr_path)
      
                curr_weight -= self.G[curr_path[level - 1]][i]
                curr_bound = temp
      
                self.visited = [False] * len(self.visited)
                for j in range(level):
                    if curr_path[j] != -1:
                        self.visited[curr_path[j]] = True
      
    def TSP(self):
        curr_bound = 0
        curr_path = [-1] * (self.size + 1)
        self.visited = [False] * self.size
      
        for i in range(self.size):
            curr_bound += (self.firstMin(i) + 
                           self.secondMin(i))
      
        curr_bound = math.ceil(curr_bound / 2)
      
        self.visited[0] = True
        curr_path[0] = 0
      
        self.TSPRec(curr_bound, 0, 1, curr_path)
        
    def copyToFinal(self, curr_path):
        self.final_path[:self.size + 1] = curr_path[:]
        self.final_path[self.size] = curr_path[0]
      
    def firstMin(self, i):
        min = float('inf')
        for k in range(self.size):
            if self.G[i][k] < min and i != k:
                min = self.G[i][k]      
        return min
      
    def secondMin(self, i):
        first, second = float('inf'), float('inf')
        for j in range(self.size):
            if i == j:
                continue
            if self.G[i][j] <= first:
                second = first
                first = self.G[i][j]
      
            elif(self.G[i][j] <= second and 
                 self.G[i][j] != first):
                second = self.G[i][j]      
        return second
    
    def get_odd(self):
        degrees = [0 for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                    if(self.G[i][j]!=0):
                        degrees[i]+=1
        return degrees

if __name__ == "__main__":
    G = []
    size = 0
    with open('l3-3.txt') as file:
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

