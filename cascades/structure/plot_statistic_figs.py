#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *
from gini import gini

def plot_statistics():

    cc_labels = ['[1,10)','[10,20)','[20,50)','[50,100)','[100,200)','[200,500)','[500,1000)','1000+']

    logging.info('plot statistics figures of sub-cascades')
    ## [citation_count][[subcascade_size1,subcascade_size2, ...],[],[]]
    remaining_subgraphs_dis = json.loads(open('data/remaining_subgraphs_dis.json').read()) 
    ## component 数量
    cc_amount = defaultdict(list)
    ## component 大小
    cc_size = defaultdict(list)
    cc_size_diveristy = defaultdict(list)
    ## 最大的conponent的
    cc_maxnode = defaultdict(list)

    for cc in remaining_subgraphs_dis.keys():
        for subgraph_sizes in remaining_subgraphs_dis[cc]:

            cc = int(cc)

            if cc==0:
            	continue

            cc_amount[cc].append(len(subgraph_sizes))
            nodesizes = []
            for esize,nsize in subgraph_sizes:
                cc_amount[cc].append(nsize)
                nodesizes.append(nsize)

            cc_size_diveristy[cc].append(gini(nodesizes))
            cc_size[cc].extend(nodesizes)
            # cc_maxnode[cc].append(float(np.max(nodesizes)/cc))

    print 0,0
    fig,axes = plt.subplots(2,4,figsize=(20,10))
    ##最基础的统计图
    ## component的数量分布图
    ## 总体分布图
    ax = axes[0,0]

    cc_xs = []
    
    mean_amount = []
    amount_diversities = []
    amount_dict = defaultdict(int)
    cc_bin_dict = defaultdict(list)
    for cc in sorted(cc_amount.keys()):

        cc_xs.append(cc)
        # cc_bin_xs.append()
        mean_amount.append(np.mean(cc_amount[cc]))
        amount_diversities.append(gini(cc_amount[cc]))
        cc_bin_dict[bin_cc(cc)].extend(cc_amount[cc])

        for amount in cc_amount[cc]:

            amount_dict[amount]+=1

    t_cc_xs = []
    t_num_ys = [] 

    for amout in sorted(amount_dict.keys()):
        t_cc_xs.append(amout)
        t_num_ys.append(amount_dict[amout])

    print t_cc_xs,t_num_ys
    ax.plot(t_cc_xs,t_num_ys,'o',fillstyle='none')

    ax.set_xlabel('number of sub-cascades')
    ax.set_ylabel('number of papers')

    ax.set_yscale('log')


    print cc_xs,mean_amount
    ax1 = axes[0,1]

    ax1.plot(cc_xs,mean_amount)

    ax1.set_xlabel('number of citations')
    ax1.set_xscale('log')

    ax1.set_ylabel('average number of sub-cascades')


    data = []
    cc_bin_xs = []
    for cc_bin in sorted(cc_bin_dict.keys()):
        cc_bin_xs.append(cc_bin)
        data.append(cc_bin_dict[cc_bin])


    ax3 = axes[0,2]
    print cc_xs,amount_diversities
    ax3.plot(cc_xs,amount_diversities)
    ax3.set_xlabel('number of citations')
    ax3.set_ylabel('diveristy of number of sub-cascades')
    ax3.set_xscale('log')

    ax2 = axes[0,3]

    print cc_bin_xs,cc_labels
    ax2.boxplot(data)
    ax2.set_xticks(cc_bin_xs)
    ax2.set_xticklabels([cc_labels[i] for i in cc_bin_xs])

    ax2.set_xlabel('number of citations')
    ax2.set_ylabel('number of sub-cascades')
    ax2.set_xscale('log')


    ## compnent的size分布图
    cc_xs = []
    size_ys = []
    ccbin_size = defaultdict(list)
    # diversities = []

    size_dict = defaultdict(int)
    for cc in sorted(cc_size.keys()):
        cc_xs.append(cc)
        size_ys.append(np.mean(cc_size[cc]))


        ccbin_size[bin_cc(cc)].extend(cc_size[cc])

        for size in cc_size[cc]:

            size_dict[size]+=1


    size_xs = []
    all_size_ys = []

    ax10 = axes[1,0]

    for x in sorted(size_dict.keys()):
        size_xs.append(x)
        all_size_ys.append(size_dict[x])


    ax10.plot(size_xs,all_size_ys,'o',fillstyle='none')
    ax10.set_xlabel('size of sub-cascades')
    ax10.set_ylabel('number of papers')

    ax10.set_xscale('log')
    ax10.set_yscale('log')


    ## 平均曲线图
    ax11 = axes[1,1]

    ax11.plot(cc_xs,size_ys)

    ax11.set_xlabel('number of citations')

    ax11.set_xscale('log')
    ax11.set_ylabel('average size of sub-cascades')

    bin_cc_xs = []
    data = []

    for bincc in sorted(ccbin_size.keys()):
        bin_cc_xs.append(bincc)
        data.append(ccbin_size[bincc])

    ## bin之后的桶图
    print bin_cc_xs,cc_labels

    ax12 = axes[1,3]
    ax12.boxplot(data)
    ax12.set_xticks(bin_cc_xs)
    ax12.set_xticklabels([cc_labels[i] for i in bin_cc_xs])
    ax12.set_ylabel('size of sub-cascades')

    ## Size的diverisity

    # cc_xs = []
    # size_dives = []

    # for cc in sorted(cc_size_diveristy.keys()):

    #     cc_xs.append(cc)
    #     size_dives.append(np.mean(cc_size_diveristy[cc]))

    # ax13 = axes[1,2]

    # ax13.plot(cc_xs,size_dives)

    # ax13.set_xlabel('number of citations')
    # ax13.set_xscale('log')
    # ax13.set_ylabel('average size diversity')


    plt.tight_layout()

    plt.savefig('pdf/aminer_subcas_statistics.png',dpi=200)

    logging.info('saved to pdf/aminer_subcas_statistics.png')

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



if __name__ == '__main__':
    plot_statistics()











