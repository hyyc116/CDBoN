#coding:utf-8
'''
使用 Graphviz 可视化 graph
'''
import graphviz as gv
from graphviz import Digraph

def viz():
    graph = gv.Digraph(format='pdf')
    graph.attr('node', shape='circle',width='0.2',height='0.2',fixedwith='true')
    graph.attr('edge',arrowhead='open')
    graph.attr('graph',rankdir = 'RL')
    graph.edge('B','A')
    graph.edge('C','A')
    graph.edge('D','A')
    graph.edge('E','A') 
    graph.edge('F','A')
    graph.render('citation_count')

    p = Digraph(format='pdf')
    p.attr('graph',rankdir = 'RL')
    p.attr('edge',arrowhead='open')
    p.attr('node', shape='circle',width='0.2',height='0.2',fixedwith='true')
    p.edge('B','A')
    p.edge('C','A')
    p.edge('D','A')
    p.edge('E','A') 
    p.edge('F','A')
    p.edge('C','D',style='dashed')
    p.edge('F','D',style='dashed')
    p.edge('C','B',style='dashed')

    # p.subgraph(graph)

    p.render('citation_cascade')
 
if __name__ == '__main__':
    viz()

