import networkx as nx
import numpy as np

class Graph():
    def __init__(self, G, size):
        self.G = G
        self.size = size
    
    def print_graph(self):
        print("Вхідна матриця суміжності:")
        print(np.array(self.G))
        print()
    
    def start_algorithm(self):
        edges = []
        for i in range(self.size):
            for j in range(i, self.size):
                if self.G[i][j] != 0:
                    edges.append([i, j])
        oddness, odd_node = self.get_odd()
        print("Вузли та їх степінь: ")
        for i in range(len(oddness)):
            print("Вершина " + str(i+1) + " - її степінь " + str(oddness[i]))
        print()
        
        if not odd_node:
            print("Граф є Ейлеровим та має Ейлерів цикл!")
            print()
            res_path = self.find_eulerian_tour(edges)
            for el in res_path:
                print(str(el+1), end=" -> ")
            print(" його сума рівна: " + str(int(np.sum(np.array(self.G))/2)))
        else:
            print("Граф не є Ейлеровим та немає Ейлеровів цикл!")
            print()
            repeated = self.Chinese_Postman(odd_node, edges)

            for el in edges:
                if el[0] > el[1]:
                    temp = el[1]
                    el[1] = el[0]
                    el[0] = temp
            all_edges = edges + repeated
            
            res = self.find_eulerian_tour(all_edges)
            print("Маршрут листоноші:")
            for el in res:
                print(str(el+1), end=" -> ")
            sum_res = np.sum(np.array(self.G)) / 2
            for el in repeated:
                sum_res += self.G[el[0]-1][el[1]-1]
            print("Загальна довжина цього маршруту дорівнює: " + str(int(sum_res)))
    
    def get_odd(self):
        degrees = [0 for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if(self.G[i][j]!=0):
                    degrees[i]+=1                
        odds = [i for i in range(len(degrees)) if degrees[i]%2!=0]
        return degrees, odds
    
    def gen_pairs(self, odds):
        pairs = []
        for i in range(len(odds)-1):
            pairs.append([])
            for j in range(i+1,len(odds)):
                pairs[i].append([odds[i],odds[j]])    
        return pairs
    
    def find_eulerian_tour(self, all_edges):
        S = all_edges[0]
        all_edges.remove(S)
        C = []
        while len(all_edges) != 0:
            for el in all_edges:
                if S[-1] in el:
                    temp = el
                    all_edges.remove(el)
                    all_edges = [el] + all_edges
                    break
            if all_edges[0][0] == S[-1]:
                S.append(all_edges[0][1])
                all_edges.remove(all_edges[0])
            elif all_edges[0][1] == S[-1]:
                S.append(all_edges[0][0])
                all_edges.remove(all_edges[0])
            elif all_edges[0][0] != S[-1] and  all_edges[0][1] != S[-1]:
                C.append(S[-1])
                S = S[:-1]
        for i in range(len(C)-1, -1, -1):
            S.append(C[i])
        return S
    
    def dijktra(self, start, end):
        distArray = [0 for i in range(self.size)]
        vistSet = [0 for i in range(self.size)]
        V = self.size
        INF = float("inf")
        graph = self.G
        for i in range(V):
            distArray[i] = INF
            vistSet[i] = False
            
        distArray[start] = 0
        for i in range(V):
            u = self.minDistance(distArray, vistSet, INF, V) 
            vistSet[u] = True
            for v in range(V): 
                if graph[u][v] > 0 and vistSet[v] == False and distArray[v] > distArray[u] + graph[u][v]:
                    distArray[v] = distArray[u] + graph[u][v]
        return distArray[end]
      
    def minDistance(self, distArray, vistSet, INF, V): 
        min = INF
        min_index = 0
        for v in range(V): 
            if distArray[v] < min and vistSet[v] == False: 
                min = distArray[v] 
                min_index = v 
        return min_index
    
    def get_repeated_edges(self, edges, graph, start, end):
        G = nx.Graph()
        for i in range(len(edges)):
            G.add_edge(edges[i][0], edges[i][1], weight = graph[edges[i][0]][edges[i][1]])
        min_dist = nx.shortest_path(G,source=start,target=end, weight='weight')
        return min_dist
    
    def Chinese_Postman(self, odds, edges):
        pairs = self.gen_pairs(odds)
        l = (len(pairs)+1)//2
            
        pairings_sum = []
            
        def get_pairs(pairs, done = [], final = []):
            
            if(pairs[0][0][0] not in done):
                done.append(pairs[0][0][0])
                
                for i in pairs[0]:
                    f = final[:]
                    val = done[:]
                    if(i[1] not in val):
                        f.append(i)
                    else:
                        continue
                    
                    if(len(f)==l):
                        pairings_sum.append(f)
                        return 
                    else:
                        val.append(i[1])
                        get_pairs(pairs[1:],val, f)
            else:
                get_pairs(pairs[1:], done, final)
            
        get_pairs(pairs)
        min_sums = []
        sum_between_pairs = []
        
        for el in pairings_sum:
            s = 0
            temp = []
            for i in range(len(el)):
                t = self.dijktra(el[i][0], el[i][1])
                s += t
                temp.append(t)
            min_sums.append(s)
            sum_between_pairs.append(temp)

        print("Кроки розв'язку за алгоритмом листоноші:")
        print()
        print("Паросполучення та їх ваги:")
        str_temp = []
        for i in range(0, len(pairings_sum)):
            temp = str(i+1) + ") Вузли "
            for j in range(0,len(pairings_sum[i])):
                temp += "[" + str(pairings_sum[i][j][0] + 1) + "; " + str(pairings_sum[i][j][1] + 1) + "] та "
            temp = temp[:-3]
            temp += "--> "
            for j in range(0,len(pairings_sum[i])):
                temp += str(sum_between_pairs[i][j]) + " + "
            temp = temp[:-3]
            temp += " = " + str(min_sums[i])
            str_temp.append(temp)
            print(temp)
        print()
        
        added_dis = min(min_sums)
        min_pair = pairings_sum[min_sums.index(added_dis)]
        print("Вибране паросполучення:")
        print(str_temp[min_sums.index(added_dis)])
        print()
        
        temp = 0
        repeated_edges = []
        for el in min_pair:
            temp = self.get_repeated_edges(edges ,G, el[0], el[1])
            for i in range(0, len(temp)-1):
                repeated_edges.append([temp[i]+1, temp[i+1]+1])
                
        print("Ребра, які при обході листоноші будуть повторюватися:")
        for i in range(len(repeated_edges)):
            print(str(i+1) + ") " + str(repeated_edges[i]) + " --> " +
                  str(self.G[repeated_edges[i][0]-1][repeated_edges[i][1]-1]))
        print()
            
        return repeated_edges
            
if __name__ == "__main__":
    G = []
    size = 0
    with open('l2-1.txt') as file:
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
    
