#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *
from tools import *

def main():

    label = sys.argv[1]
    if label== 'gen_stat':
        gen_statistics_data(sys.argv[2])
    elif label == 'stat_plot':
        stats_plot()
    elif label == 'build_cascade':
        build_cascades(sys.argv[2])
    elif label =='compare_plot':
        plot_dict()
    elif label=='unlinked_subgraph':
        unlinked_subgraph(sys.argv[2])
    elif label == 'plot_subgraph':
        plot_unconnected_subgraphs()
    elif label == 'plot_centrality':
        plot_centrality()

    



