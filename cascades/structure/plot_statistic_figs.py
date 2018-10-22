#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *

def plot_statistics():
	logging.info('plot statistics figures of sub-cascades')
	## [citation_count][[subcascade_size1,subcascade_size2, ...],[],[]]
    remaining_subgraphs_dis = json.loads(open('data/remaining_subgraphs_dis.json').read()) 
    ## component 数量
    cc_amount = defaultdict(list)
    ## component 大小
    cc_size = defaultdict(lambda:defaultdict(int))
    ## 最大的conponent的
    cc_maxnode = defaultdict(list)

    for cc in remaining_subgraphs_dis.keys():
    	for subgraph_sizes in remaining_subgraphs_dis[cc]:
    		cc_amount[cc].append(len(subgraph_sizes))
    		nodesizes = []
    		for esize,nsize in subgraph_sizes:
    			cc_amount[cc][esize]+=1
    			nodesizes.append(nsize)

    		cc_maxnode[cc].append(float(np.max(nodesizes)/cc))



	##最基础的统计图
	## component的数量分布图






	## compnent的size分布图





	## 最大的团的比例





	## Size的diverisity