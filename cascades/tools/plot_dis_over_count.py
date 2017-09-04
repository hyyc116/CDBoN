#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *

def plot_heatmap(x,y,ax,bins,fig,gridsize=50):
    hb = ax.hexbin(x, y, gridsize=gridsize, cmap=CM.Blues, bins='log',xscale=bins[0] ,yscale=bins[1])

# 随着citation count的增加，各个指标的变化
def plot_dis_over_count(is_heat=False,is_smooth=False,is_average=False):

    plot_dict = json.loads(open('data/plot_dict.json').read())
    ###plot the comparison figure
    cxs= plot_dict['cxs']
    eys= plot_dict['eys']
    dys= plot_dict['dys']
    dcxs=plot_dict['dcx']
    od_ys = plot_dict['od_ys']
    id_ys = plot_dict['id_ys']

    num = len(plt.get_fignums())
    fig,axes = plt.subplots(1,5,figsize=(25,5))
    print 'length of cxs:{:},eys:{:},dcxs:{:},dys:{:},od_ys:{:},id_ys:{:}'.format(len(cxs),len(eys),len(dcxs),len(dys),len(od_ys),len(id_ys))

    ## 将数量少于一定值的citation count 向上靠近
    num_dict = Counter(cxs)
    count_mapping = {}
    last_count = 0
    for x in sorted(num_dict.keys()):
        if num_dict[x] > 5:
            count_mapping[x] = x
            last_count = x
        else:
            count_mapping[x] = last_count
    
    rxs = []
    rys = []
    # max_dict = defaultdict(int)
    equal_dict=defaultdict(list)
    #average dict
    cc_size_dict = defaultdict(list)
    # percentage of connector = id_ys
    pc_xs = []
    pc_ys = []
    cc_pc_dict = defaultdict(list)

    ## percentage of od>1
    po_xs=[]
    po_ys=[]
    cc_po_dict = defaultdict(list)


    for i in range(len(cxs)):

         #用于生成xs,ys是 将xs替代
        if is_smooth:
            sx = count_mapping[cxs[i]]
        else:
            sx = cxs[i]

        # 计算时citation count 还是按照原值计算
        y  = eys[i]/float(cxs[i])-1
        rxs.append(sx)
        rys.append(y)

        cc_size_dict[sx].append(y)

        if eys[i]==cxs[i]:
            equal_dict[sx].append(1)
        else:
            equal_dict[sx].append(0)

        #percentage of connectors
        pc_xs.append(sx)
        pc_y = id_ys[i]
        pc_ys.append(pc_y)
        cc_pc_dict[sx].append(pc_y)

        #percentage of out degree > 1
        po_xs.append(sx)
        po_y = od_ys[i]
        po_ys.append(y)
        cc_po_dict[sx].append(po_y)



    ## percentage of  cascade size = ciattion count vs citation count
    print 'percentage of cascade size = citation count'
    ax0 = axes[0]

    e_xs = []
    e_ys = []
    for cc in sorted(equal_dict.keys()):
        e_xs.append(cc)
        y = equal_dict[cc]
        e_ys.append(sum(y)/float(len(y)))

    ax0.plot(e_xs,e_ys)
    ax0.set_xscale('log')
    # ax0.set_yscale('log')
    ax0.set_title('citation count = cascade size')
    ax0.set_xlabel('citation count\n(a)')
    ax0.set_ylabel('percentage')

    print 'percentage of AMV'
    ax1 = axes[1]
    #max values
    max_xs = []
    max_ys = []
    ## average 
    avg_xs = []
    avg_ys = []
    for cc in sorted(cc_size_dict.keys()):
        size_list = cc_size_dict[cc]
        max_xs.append(cc)
        max_ys.append(max(size_list))

        avg_xs.append(cc)
        avg_ys.append(sum(size_list)/float(len(size_list)))

    if is_heat:
        plot_heatmap(rxs,rys,ax1,['log','linear'],fig)
    else:
        ax1.scatter(rxs,rys)
    if not is_average:
        ##最大值图
        ax1.plot(max_xs,max_ys,c=color_sequence[3],alpha=0.8)
        max_zs = [i for i in zip(*lowess(max_ys,np.log(max_xs),frac= 0.08))[1]]
        ax1.plot(max_xs,max_zs,c='r')
    else:
        ##均值图
        ax1.plot(avg_xs,avg_ys,c=color_sequence[5],alpha=0.8)
        avg_zs = [i for i in zip(*lowess(avg_ys,np.log(avg_xs),frac= 0.08))[1]]
        ax1.plot(avg_xs,avg_zs,c='r')


    ax1.set_xlabel('Citation Count\n(b)')
    ax1.set_ylabel('Average Marginal Value')
    ax1.set_xscale('log')
    ax1.set_title('Average Marginal Value')


    #### percentage of connectors over citation count
    print 'percentage of connectors'
    ax2 = axes[2]
    if is_heat:
        plot_heatmap(pc_xs,pc_ys,ax2,['log','linear'],fig)
    else:
        ax2.scatter(pc_xs,pc_ys)
        
    ax2.set_xlabel('Citation Count\n(c)')
    ax2.set_ylabel('$P(v=connector)$')
    ax2.set_xscale('log')
    ax2.set_title('Percentage of connectors')
    np_pc_xs = np.array([float(i) for i in sorted(pc_xs) if i>1])
    ax2.plot(np_pc_xs,1/np_pc_xs,'--',c=color_sequence[4])
    ax2.plot(np_pc_xs,1-1/np_pc_xs,'--',c=color_sequence[4])

    max_xs = []
    max_ys = []

    #avg
    avg_xs = []
    avg_ys = []
    for cc in sorted(cc_pc_dict.keys()):
        pc_list = cc_pc_dict[cc]

        max_xs.append(cc)
        max_ys.append(max(pc_list))

        avg_xs.append(cc)
        avg_ys.append(sum(pc_list)/float(len(pc_list)))

    if not is_average:
        ax2.plot(max_xs,max_ys,c=color_sequence[3],alpha=0.8)
        max_zs = [i for i in zip(*lowess(max_ys,np.log(max_xs),frac=0.05,it=1,is_sorted =True))[1]]
        ax2.plot(max_xs,max_zs,c='r')
    else:
        ax2.plot(avg_xs,avg_ys,c=color_sequence[5],alpha=0.8)
        avg_zs = [i for i in zip(*lowess(avg_ys,np.log(avg_xs),frac=0.05,it=1,is_sorted =True))[1]]
        ax2.plot(avg_xs,avg_zs,c='r')

    print 'percentage of out-degree > 1'
    ### out degree > 1 over citation count

    ax3 = axes[3]
    if is_heat:
        plot_heatmap(po_xs,po_ys,ax3,['log','linear'],fig)
    else:
        ax3.scatter(po_xs,po_ys)

    ax3.set_xlabel('Citation Count\n(d)')
    ax3.set_ylabel('$P(deg^+(v)>1)$')
    ax3.set_xscale('log')
    ax3.set_title('Out degree > 1')
    ax3.plot(po_xs,1/np.array(po_xs),'--',c=color_sequence[4])
    ax3.plot(po_xs,1-1/np.array(po_xs),'--',c=color_sequence[4])


    max_xs = []
    max_ys = []
    #avg
    avg_xs = []
    avg_ys = []

    for cc in sorted(cc_po_dict.keys()):
        max_xs.append(cc)
        po_list = cc_po_dict[cc]
        max_ys.append(max(po_list))

        avg_xs.append(cc)
        avg_ys.append(sum(po_list)/float(len(po_list)))

    if not is_average:
        ax3.plot(max_xs,max_ys,c=color_sequence[3],alpha=0.8)
        max_zs = [i for i in zip(*lowess(max_ys,np.log(max_xs),frac=0.05,it=1,is_sorted =True))[1]]
        ax3.plot(max_xs,max_zs,c='r')
    else:
        ax3.plot(avg_xs,avg_ys,c=color_sequence[5],alpha=0.8)
        avg_zs = [i for i in zip(*lowess(avg_ys,np.log(avg_xs),frac=0.05,it=1,is_sorted =True))[1]]
        ax3.plot(avg_xs,avg_zs,c='r')


    print 'plot acmv..'
    ### average connector marginal value
    ax4 = axes[4]

    xs = []
    ys = []
    for i,idy in enumerate(id_ys):

        if idy==0:
            continue

        if is_smooth:
            sx = count_mapping[dcxs[i]]
        else:
            sx = dcxs[i]
        
        xs.append(sx)
        ys.append(od_ys[i]/id_ys[i])

    if is_heat:
        plot_heatmap(xs,ys,ax4,['log','linear'],fig)
    else:
        ax4.scatter(xs,ys)

    ax4.set_xscale('log')
    ax4.set_xlabel('citation count\n(e)')
    ax4.set_ylabel('ACMV')
    ax4.set_title('ACMV distribution')

    max_dict = defaultdict(list)
    for i,xv in enumerate(xs):
        max_dict[xv].append(ys[i])
        # if ys[i] > max_dict[xv]:
            # max_dict[xv] = ys[i]

    max_xs = []
    max_ys = []

    #avg
    avg_xs = []
    avg_ys = []

    for x in sorted(max_dict.keys()):
        max_xs.append(x)
        max_ys.append(max(max_dict[x]))

        avg_xs.append(x)
        avg_ys.append(sum(max_dict[x])/float(len(max_dict[x])))


    # if not is_average:
    #     ax4.plot(max_xs,max_ys,c=color_sequence[3],alpha=0.8)
    #     max_zs = [i for i in zip(*lowess(max_ys,np.log(max_xs),frac=0.05,it=1,is_sorted =True))[1]]
    #     ax4.plot(max_xs,max_zs,c='r')
    # else:
    #     ax4.plot(avg_xs,avg_ys,c=color_sequence[5],alpha=0.8)
    #     avg_zs = [i for i in zip(*lowess(avg_ys,np.log(avg_xs),frac=0.05,it=1,is_sorted =True))[1]]
    #     ax4.plot(avg_xs,avg_zs,c='r')

    if is_smooth:
        for ax in axes:
            ax.set_xlim(0.9,1100)



    plt.tight_layout()
    # save output
    heat = 0
    average = 0 
    smooth = 0

    if is_heat:
        heat=1
    if is_average:
        average = 1
    if is_smooth:
        smooth = 1

    outpath = 'pdf/compare_{:}_{:}_{:}.png'.format(heat,smooth,average)
    plt.savefig(outpath,dpi=200)
    print 'figure saved to {:}'.format(outpath)




if __name__ == '__main__':

    if len(sys.argv) != 4:
        print 'parameter error! python {:} is_heat is_smooth is_avg'.format(sys.argv[0])
    else:
        heat = int(sys.argv[1])
        if heat>0:
            is_heat = True
        else:
            is_heat = False

        smooth = int(sys.argv[2])
        if smooth>0:
            is_smooth = True
        else:
            is_smooth = False

        avg = int(sys.argv[3])
        if avg>0:
            is_avg = True
        else:
            is_avg = False

        plot_dis_over_count(is_heat,is_smooth,is_avg)












