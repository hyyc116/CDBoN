#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *
import math

color_map_name = 'Wistia'
bound_color=color_sequence[14]
maximal_bak = color_sequence[7]
maximal_smooth = color_sequence[6]

avg_bak = color_sequence[1]
avg_smooth = color_sequence[0]

def plot_heatmap(x,y,ax,bins,fig,gridsize=100):
    hb = ax.hexbin(x, y, gridsize=gridsize, cmap=plt.get_cmap('Wistia'), bins='log',xscale=bins[0] ,yscale=bins[1])

# 随着citation count的增加，各个指标的变化
def plot_dis_over_count():

    plot_dict = json.loads(open('data/mag/stats/plot_dict.json').read())
    ###plot the comparison figure
    cxs= plot_dict['cxs']
    eys= plot_dict['eys']
    dys= plot_dict['dys']
    dcxs=plot_dict['cxs']
    od_ys = plot_dict['od_ys']
    id_ys = plot_dict['id_ys']

    num = len(plt.get_fignums())
    fig,axes = plt.subplots(2,2,figsize=(11,10))
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

        if sx==10 and pc_y==0.5:
            print 'Percentage of connectors',sx,pc_y


        #percentage of out degree > 1
        po_xs.append(sx)
        po_y = od_ys[i]
        po_ys.append(po_y)
        cc_po_dict[sx].append(po_y)

    print 'percentage of AMV'
    # ax1 = axes[0]
    # #max values
    # max_xs = []
    # max_ys = []
    # ## average 
    # avg_xs = []
    # avg_ys = []
    # for cc in sorted(cc_size_dict.keys()):
    #     size_list = cc_size_dict[cc]
    #     max_xs.append(cc)
    #     max_ys.append(max(size_list))

    #     avg_xs.append(cc)
    #     avg_ys.append(sum(size_list)/float(len(size_list)))

    # plot_heat_scatter(rxs,rys,ax1,fig)
        
    # ax1.plot(avg_xs,avg_ys,c=avg_bak,alpha=1)
    # avg_zs = [i for i in zip(*lowess(avg_ys,np.log(avg_xs),frac= 0.08))[1]]

    # ax1.plot(max_xs,max_ys,c=maximal_bak,alpha=1)
    # max_zs = [i for i in zip(*lowess(max_ys,np.log(max_xs),frac= 0.08))[1]]

    # ax1.plot(max_xs,max_zs,c=maximal_smooth)
    # ax1.plot(avg_xs,avg_zs,c=avg_smooth)


    # ax1.set_xlabel('citation count\n(a)')
    # ax1.set_ylabel('Average Marginal Value')
    # ax1.set_xscale('log')
    # ax1.set_title('Average Marginal Value')


    #### percentage of connectors over citation count
    print 'percentage of connectors'
    ax2 = axes[0,0]
    plot_heat_scatter(pc_xs,pc_ys,ax2,fig)
        
    ax2.set_xlabel('citation count\n(a)')
    ax2.set_ylabel('$P(c)$')
    ax2.set_xscale('log')
    # ax2.set_title('Percentage of Connectors')
    np_pc_xs = np.array([float(i) for i in sorted(pc_xs) if i>1])
    ax2.plot(np_pc_xs,1/np_pc_xs,'--',c=bound_color)
    ax2.plot(np_pc_xs,1-1/np_pc_xs,'--',c=bound_color)

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

        
    ax2.plot(avg_xs,avg_ys,c=avg_bak,alpha=1)
    avg_zs = [i for i in zip(*lowess(avg_ys,np.log(avg_xs),frac=0.05,it=1,is_sorted =True))[1]]

    ax2.plot(max_xs,max_ys,c=maximal_bak,alpha=1)
    max_zs = [i for i in zip(*lowess(max_ys,np.log(max_xs),frac=0.05,it=1,is_sorted =True))[1]]

    ax2.plot(max_xs,max_zs,c=maximal_smooth)
    ax2.plot(avg_xs,avg_zs,c=avg_smooth)

    print 'percentage of out-degree > 1'
    ### out degree > 1 over citation count
    ax3 = axes[0,1]
    plot_heat_scatter(po_xs,po_ys,ax3,fig)

    ax3.set_xlabel('citation count\n(b)')
    ax3.set_ylabel('$P(deg^+(v)>1)$')
    ax3.set_xscale('log')
    # ax3.set_title('Out degree > 1')
    np_po_xs = np.array([float(i) for i in sorted(po_xs) if i>1])
    ax3.plot(np_po_xs,1/np.array(np_po_xs),'--',c=bound_color)
    ax3.plot(np_po_xs,1-1/np.array(np_po_xs),'--',c=bound_color)


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

    ax3.plot(avg_xs,avg_ys,c=avg_bak,alpha=1)
    avg_zs = [i for i in zip(*lowess(avg_ys,np.log(avg_xs),frac=0.05,it=1,is_sorted =True))[1]]

    ax3.plot(max_xs,max_ys,c=maximal_bak,alpha=1)
    max_zs = [i for i in zip(*lowess(max_ys,np.log(max_xs),frac=0.05,it=1,is_sorted =True))[1]]

    ax3.plot(max_xs,max_zs,c=maximal_smooth)
    ax3.plot(avg_xs,avg_zs,c=avg_smooth)


    print 'plot acmv..'
    ### average connector marginal value
    ax4 = axes[1,0]

    xs = []
    ys = []
    for i,idy in enumerate(id_ys):

        if idy==0:
            continue
        
        sx = dcxs[i]
        
        xs.append(sx)
        ys.append(od_ys[i]/id_ys[i])

    plot_heat_scatter(xs,ys,ax4,fig)

    ax4.set_xscale('log')
    ax4.set_xlabel('citation count\n(c)')
    ax4.set_ylabel('$ANLEC$')
    # ax4.set_title('ANLEC Distribution')

    max_dict = defaultdict(list)
    for i,xv in enumerate(xs):
        max_dict[xv].append(ys[i])

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

    ax4.plot(avg_xs,avg_ys,c=avg_bak,alpha=1)
    avg_zs = [i for i in zip(*lowess(avg_ys,np.log(avg_xs),frac=0.1,it=1,is_sorted =True))[1]]
    ax4.plot(max_xs,max_ys,c=maximal_bak,alpha=1)
    max_zs = [i for i in zip(*lowess(max_ys,np.log(max_xs),frac=0.1,it=1,is_sorted =True))[1]]

    ax4.plot(max_xs,max_zs,c=maximal_smooth)
    ax4.plot(avg_xs,avg_zs,c=avg_smooth)


    ### CR 
    mag_connector_obj = json.loads(open('data/mag/mag_connector.json').read())
    nc_list = mag_connector_obj['nc']
    cr_list = mag_connector_obj['cr']

    logging.info('plotting CR ... ')

    cc_pid_crs =defaultdict(lambda:defaultdict(list))
    for cr,depth,n_citation,pid in cr_list:
        cc_pid_crs[n_citation][pid].append(cr)

    cxs=[]
    acr=[]
    cc_crs = defaultdict(list)
    for cc in cc_pid_crs.keys():
        for pid in cc_pid_crs[cc].keys():
            cxs.append(cc)
            crm = np.mean(cc_pid_crs[cc][pid])
            acr.append(crm)

            cc_crs[cc].append(crm)

    ax = axes[1,1]
    plot_heat_scatter(cxs,acr,ax,fig)
    ax.set_xscale('log')
    ax.set_xlabel('citation count\n(V)')
    ax.set_ylabel('$ACR$')
    # ax.set_title('Average conversion rate')

    max_dict = defaultdict(list)
    for i,xv in enumerate(cxs):
        max_dict[xv].append(acr[i])

    max_xs = []
    max_ys = []

    #avg
    avg_xs = []
    avg_ys = []

    for x in sorted(max_dict.keys()):
        max_xs.append(x)
        max_ys.append(np.max(max_dict[x]))

        if x==40:
            print 'ACR max value',x, max_ys


        avg_xs.append(x)
        avg_ys.append(np.mean(max_dict[x]))

    ax.plot(avg_xs,avg_ys,c=avg_bak,alpha=1)
    avg_zs = [i for i in zip(*lowess(avg_ys,np.log(avg_xs),frac=0.1,it=1,is_sorted =True))[1]]
    ax.plot(max_xs,max_ys,c=maximal_bak,alpha=1)
    max_zs = [i for i in zip(*lowess(max_ys,np.log(max_xs),frac=0.1,it=1,is_sorted =True))[1]]

    ax.plot(max_xs,max_zs,c=maximal_smooth)
    ax.plot(avg_xs,avg_zs,c=avg_smooth)

    plt.tight_layout()
    # save output
    outpath = 'pdf/mag_compare.png'
    plt.savefig(outpath,dpi=400)
    print 'figure saved to {:}'.format(outpath)

if __name__ == '__main__':
    plot_dis_over_count()












