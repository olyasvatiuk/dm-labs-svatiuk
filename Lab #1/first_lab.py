import numpy as np

class Graph():
    def __init__(self, G, size, min_max):
        self.G = G
        self.size = size
        self.min_max = min_max
    
    def print_graph(self):
        print("Вхідна матриця суміжності:")
        print(np.array(self.G))
        print()
    
    def prim(self):
        edges = []
        for i in range(self.size):
            for j in range(i, self.size):
                if self.G[i][j] != 0:
                    edges.append([i, j])
        
        selected_nodes = [0]
        selected_weight = []
        selected_edges = []

        while len(selected_nodes) != self.size:
            compare = float("inf")
            temp_edge = []
            for el in edges:
                for i in range(len(selected_nodes)):
                    if selected_nodes[i] in el:
                        temp_edge.append(el)
            
            temp_weight = []
            for el in temp_edge:
                temp_weight.append(self.G[el[0]][el[1]])
            
            if self.min_max == "MAX":
                choosen_weight = max(temp_weight)
            elif self.min_max == "MIN":
                choosen_weight = min(temp_weight)
            
            index_of_min = temp_weight.index(choosen_weight)
            
            edges_add_in_tree = temp_edge[index_of_min]
            edges.remove(edges_add_in_tree)
            
            if edges_add_in_tree[0] not in selected_nodes:
                selected_nodes.append(edges_add_in_tree[0])
                selected_weight.append(choosen_weight)
                selected_edges.append(edges_add_in_tree)
            elif edges_add_in_tree[1] not in selected_nodes:
                selected_nodes.append(edges_add_in_tree[1])
                selected_weight.append(choosen_weight)
                selected_edges.append(edges_add_in_tree)
        
        self.print_res(selected_weight, selected_edges, edges)
        
    def print_res(self, selected_weight, selected_edges, edges):
        ctr = 1
        for i in range(len(selected_edges)):
            print("Крок " + str(ctr) + ": ")
            print("Додаємо ребро: ", end=" ")
            print(str(selected_edges[i][0]+1) + " -- > " + str(selected_edges[i][1]+1) + 
                  " його вага: ", end="")
            print(selected_weight[i])
            ctr +=1
        print()
        
        for el in edges:
            self.G[el[0]][el[1]] = 0
            self.G[el[1]][el[0]] = 0
            
        if self.min_max == "MAX":
            print("Вага максимального остового дерева: " + str(sum(selected_weight)))
            print()
            print("Матриця максимального остового дерева: ")
            print(np.array(self.G))
        elif self.min_max == "MIN":
            print("Вага мінімального остового дерева: " + str(sum(selected_weight)))
            print()
            print("Матриця мінімального остового дерева: ")
            print(np.array(self.G))            
            
            
if __name__ == "__main__":
    G = []
    size = 0
    with open('l1_1.txt') as file:
        for n, line in enumerate(file):
            if n == 0:
                size = int(line.strip())
            else:
                b = line.strip()
                b = b.split(' ')
                b = [int(i) for i in b]
                G.append(b)
    
    graph = Graph(G, size, 'MAX')
    graph.print_graph()
    graph.prim()

