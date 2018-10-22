#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *

def plot_statistics():

	cc_labels = ['[1,10)','[10,20)','[20,50)','[50,100)','[100,200)','[200,500)','[500,1000)','1000+']

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
    			cc_amount[cc][nsize]+=1
    			nodesizes.append(nsize)

    		cc_maxnode[cc].append(float(np.max(nodesizes)/cc))

    fig,axes = plt.subplots(2,3,figsize=(15,10))
	##最基础的统计图
	## component的数量分布图
	## 总体分布图
	ax = axes[0,0]

	cc_xs = []
	
	mean_amount = []

	amount_dict = defaultdict(int)
	cc_bin_dict = defaultdict(list)
	for cc in sorted(cc_amount.keys()):

		cc_xs.append(cc)
		# cc_bin_xs.append()
		mean_amount.append(np.mean(cc_amount[cc]))
		cc_bin_dict[bin_cc[cc]].extend(cc_amount[cc])

		for amount in cc_amount[cc]:

			amount_dict[amount]+=1

	t_cc_xs = []
	t_num_ys = [] 

	for amout in sorted(amount_dict.keys()):
		t_cc_xs.append(amout)
		t_num_ys.append(amount_dict[amout])


	ax.plot(t_cc_xs,t_num_ys,'o',fillstyle='none')

	ax.set_xlabel('number of sub-cascades')
	ax.set_ylabel('number of papers')

	ax.set_yscale('log')


	ax1 = axes[0,1]

	ax1.plot(cc_xs,mean_amount)

	ax1.set_xscale('number of citations')
	ax1.set_yscale('average number of sub-cascades')


	data = []
	cc_bin_xs = []
	for cc_bin in sorted(cc_bin_dict.keys()):
		cc_bin_xs.append(cc_bin)
		data.append(cc_bin_dict[cc_bin])


	ax2 = axes[0,2]

	ax2.boxplot(data)
	ax2.set_xticks(cc_bin_xs)
	ax2.set_xticklabels(cc_labels)

	ax2.set_xlabel('number of citations')
	ax2.set_ylabel('number of sub-cascades')



	## compnent的size分布图
	




	## 最大的团的比例





	## Size的diverisity


def bin_cc(cc):

	if cc<10:
		return 0
	elif cc<20:
		return 1
	elif cc<50:
		return 2
	elif cc < 100:
		return 3
	elif cc <200:
		return 4
	elif cc < 500:
		return 5
	elif cc < 1000:
		return 6
	else:
		return 7















