#coding:utf-8
'''
使用 Graphviz 可视化 graph
'''
import graphviz as gv
from graphviz import Digraph

def viz():
    graph = gv.Digraph(format='jpg')
    graph.attr('node', shape='circle',width='0.2',height='0.2',fixedwith='true')
    graph.attr('edge',arrowhead='open')
    graph.attr('graph',rankdir = 'RL')
    graph.edge('B','A')
    graph.edge('C','A')
    graph.edge('D','A')
    graph.edge('E','A') 
    graph.edge('F','A')
    graph.edge('G','A')
    graph.render('citation_count')

    p = Digraph(format='jpg')
    p.attr('graph',rankdir = 'RL')
    p.attr('edge',arrowhead='open')
    p.attr('node', shape='circle',width='0.2',height='0.2',fixedwith='true')
    p.edge('B','A')
    p.edge('C','A')
    p.edge('D','A')
    p.edge('E','A') 
    p.edge('F','A')
    p.edge('G','A')
    p.edge('C','B',style='dashed')
    p.edge('C','D',style='dashed')
    p.edge('E','D',style='dashed')
    p.edge('F','E',style='dashed')

    # p.subgraph(graph)

    p.render('citation_cascade')

def subcascade():
    p = gv.Digraph(format='jpg')
    p.attr('node', shape='circle',width='0.2',height='0.2',fixedwith='true')
    p.attr('edge',arrowhead='open')
    p.attr('graph',rankdir = 'BT')
    p.edge('B','A')
    p.edge('C','A')
    p.edge('D','A')
    p.edge('E','A') 
    p.edge('F','A')
    p.edge('G','A')
    p.edge('H','A')
    p.edge('I','A')
    p.edge('J','A')
    p.edge('D','E',style='dashed')
    p.edge('B','C',style='dashed')
    p.edge('F','E',style='dashed')
    p.edge('I','H',style='dashed')
    p.edge('I','G',style='dashed')
    p.edge('K','J',style='dashed')
    p.edge('L','J',style='dashed')
    p.render('subcascade')

    p = gv.Digraph(format='pdf')
    p.attr('node', shape='circle',width='0.2',height='0.2',fixedwith='true')
    p.attr('edge',arrowhead='open')
    p.attr('graph',rankdir = 'BT')
    p.edge('B','C',style='dashed')
    p.edge('D','E',style='dashed')
    p.edge('F','E',style='dashed')
    p.edge('I','H',style='dashed')
    p.edge('I','G',style='dashed')
    p.edge('K','J',style='dashed')
    p.edge('L','J',style='dashed')
    p.render('subcascade2')

    p = gv.Digraph(format='pdf')
    p.attr('node', shape='circle',width='0.2',height='0.2',fixedwith='true')
    p.attr('edge',arrowhead='open')
    p.attr('graph',rankdir = 'BT')
    p.edge('B','C',style='dashed')
    p.edge('D','E',style='dashed')
    p.edge('F','E',style='dashed')
    p.edge('I','H',style='dashed')
    p.edge('I','G',style='dashed')
    p.render('subcascade3')

def plot_a_subcascade(edges,name):
    p = gv.Digraph(format='pdf')
    p.attr('node', shape='point',width='0.2',height='0.2',fixedwith='true')
    p.attr('edge',arrowhead='open')
    p.attr('graph',rankdir = 'RL')
    for e in edges:
        p.edge(e[0],e[1],style='dashed')

    p.render(name)

def depth():
    p = gv.Digraph(format='jpg')
    p.attr('node', shape='circle',width='0.2',height='0.2',fixedwith='true')
    p.attr('edge',arrowhead='open')
    p.attr('graph',rankdir = 'RL')
    p.edge('B','A')
    p.edge('C','A')
    p.edge('D','A')
    p.edge('E','A') 
    p.edge('F','A')
    p.edge('G','A')
    p.edge('H','A')
    p.edge('I','A')
    p.edge('J','A')
    p.edge('C','B',style='dashed')
    p.edge('D','C',style='dashed')
    p.edge('E','D',style='dashed')
    p.edge('F','E',style='dashed')
    p.edge('G','F',style='dashed')
    p.edge('H','G',style='dashed')
    p.edge('I','H',style='dashed')
    p.edge('J','I',style='dashed')
    p.render('depth')


if __name__ == '__main__':
    # viz()
    # subcascade()
    depth()
