import networkx as nx

G1 = nx.Graph()
G1.add_nodes_from(['KA', 'TN', 'TL', 'AP', 'KL', 'GO'])
G1.add_edges_from([('KA', 'TN'), ('KA', 'TL'), ( 'KA', 'TL'), ( 'KA', 'AP'), ('KA', 'KL'), ('KA', 'GO')])
# nx.draw(G1,with_labels=1)

G2 = nx.star_graph(5)
# nx.draw(G2,with_labels=1)

start = nx.is_isomorphic(G1, G2)
