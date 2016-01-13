import networkx as nx
import matplotlib.pyplot as plt
import pickle as p


def getdict(id2):
    with open(str(id2) + '.txt', 'r',encoding='utf-8') as f :
         dict = f.read()
         dict = eval(dict)
    return dict

def getrelations(id, id2):
    """receive two user id, If they are friends, return 1, otherwise 0."""
    dict_id1 = getdict(id2)
    if id in dict_id1:
        return 1
    else:
        return 0

def getgraph():
    """Get the Graph Object and return it.
    You must specify a Chinese font such as `SimHei` in ~/.matplotlib/matplotlibrc"""
    # Get root tree
    G = nx.Graph()  # Create a Graph object
    for id,name in dict.items():
        # Encode Chinese characters for matplotlib **IMPORTANT**
        # if you want to draw Chinese labels,
        G.add_node(id)
        print ('正在查询'+ name + '的关系谱')
        for id2,name2 in dict.items():
            if id == id2:
                continue
            if getrelations(id, id2):
                G.add_edge(id, id2)

    return G

def draw_graph( filename='graph.txt', label_flag=True, remove_isolated=True, different_size=True, iso_level=10, node_size=40):
    """Reading data from file and draw the graph.If not exists, create the file and re-scratch data from net"""
    print ("Generating graph...")
    G = getgraph()
    with open(filename, 'w') as f:
        p.dump(G, f)
    #nx.draw(G)
    # Judge whether remove the isolated point from graph
    if remove_isolated is True:
        H = nx.empty_graph()
        for SG in nx.connected_component_subgraphs(G):
            if SG.number_of_nodes() > iso_level:
                H = nx.union(SG, H)
        G = H
    # Ajust graph for better presentation
    if different_size is True:
        L = nx.degree(G)
        G.dot_size = {}
        for k, v in L.items():
            G.dot_size[k] = v
        node_size = [G.dot_size[v] * 10 for v in G]
    pos = nx.spring_layout(G, iterations=50)
    nx.draw_networkx_edges(G, pos, alpha=0.2)
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='r', alpha=0.3)
    # Judge whether shows label
    if label_flag is True:
        nx.draw_networkx_labels(G, pos, alpha=0.5)
    #nx.draw_graphviz(G)
    plt.show()

    return G

with open('friends_id_dict.txt', 'r',encoding = 'utf-8') as f:
     dict = f.read()
     dict = eval(dict)

with open('friends_id.txt', 'r') as f:
    friends_id = f.read()
    friends_id = friends_id.replace('\'','')
    friends_id = friends_id.replace(' ','')
    friends_id = friends_id.split(',')



draw_graph(filename='graph.txt', label_flag=True, remove_isolated=True, different_size=True, iso_level=10, node_size=40)

