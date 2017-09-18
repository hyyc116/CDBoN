#coding:utf-8

from basic_config import *


## average degree connectivity
def avg_connectivity(G):
    return nx.average_node_connectivity(G)

def avg_clustering(G):
    return nx.average_clustering(G.to_undirected())

def structural_varality(G):
    node_size = len(G.nodes())
    return nx.wiener_index(G.to_undirected())/(node_size-1)/node_size



if __name__ == '__main__':
    dig = nx.DiGraph()
    dig.add_edge(0,1)
    dig.add_edge(0,2)
    dig.add_edge(0,3)
    dig.add_edge(2,4)   
    dig.add_edge(3,5)
    dig.add_edge(2,1)
    dig.add_edge(3,1)
    print 'avg_connectivity',avg_connectivity(dig)
    print 'avg_clustering',avg_clustering(dig)
    print 'structural_varality',structural_varality(dig)
