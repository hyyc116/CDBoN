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
        # if y> max_dict[sx]:
        #     max_dict[sx] = y

        if eys[i]==cxs[i]:
            equal_dict[sx].append(1)
        else:
            equal_dict[sx].append(0)

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
        ax1.plot(avg_xs,avg_ys,c=color_sequence[4],alpha=0.8)
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
        plot_heatmap(dcxs,id_ys,ax2,['log','linear'],fig)
    else:
        ax2.scatter(dcxs,id_ys)
        
    ax2.set_xlabel('Citation Count\n(c)')
    ax2.set_ylabel('$P(v=connector)$')
    ax2.set_xscale('log')
    ax2.set_title('Percentage of connectors')
    sdxcs = np.array([float(i) for i in sorted(dcxs) if i>1])
    ax2.plot(sdxcs,1/sdxcs,'--',c=color_sequence[4])
    ax2.plot(sdxcs,1-1/sdxcs,'--',c=color_sequence[4])

    max_dict = defaultdict(int)
    for i,xv in enumerate(dcxs):
        if id_ys[i] > max_dict[xv]:
            max_dict[xv] = id_ys[i]

    xs = []
    ys = []
    for x in sorted(max_dict.keys()):
        xs.append(x)
        ys.append(max_dict[x])

    ax2.plot(xs,ys,c=color_sequence[3],alpha=0.8)
    fit_z = [i for i in zip(*lowess(ys,np.log(xs),frac=0.05,it=1,is_sorted =True))[1]]
    # fit_z.extend(fit_z_2)
    ax2.plot(xs,fit_z,c='r')


    print 'percentage of out-degree > 1'
    ### out degree > 1 over citation count
    ax3 = axes[3]
    if is_heat:
        plot_heatmap(dcxs,od_ys,ax3,['log','linear'],fig)
    else:
        ax3.scatter(dcxs,od_ys)

    ax3.set_xlabel('Citation Count\n(d)')
    ax3.set_ylabel('$P(deg^+(v)>1)$')
    ax3.set_xscale('log')
    ax3.set_title('Out degree > 1')
    ax3.plot(sdxcs,1/sdxcs,'--',c=color_sequence[4])
    ax3.plot(sdxcs,1-1/sdxcs,'--',c=color_sequence[4])

    max_dict = defaultdict(int)
    for i,xv in enumerate(dcxs):
        if od_ys[i] > max_dict[xv]:
            max_dict[xv] = od_ys[i]

    xs = []
    ys = []
    for x in sorted(max_dict.keys()):
        xs.append(x)
        ys.append(max_dict[x])

    ax3.plot(xs,ys,c=color_sequence[3],alpha=0.8)
    fit_z = [i for i in zip(*lowess(ys,np.log(xs),frac=0.05,it=1,is_sorted =True))[1]]
    ax3.plot(xs,fit_z,c='r')


    print 'plot acmv..'
    ### average connector marginal value
    ax4 = axes[4]

    xs = []
    ys = []
    for i,idy in enumerate(id_ys):
        
        if idy==0:
            continue

        xs.append(dcxs[i])
        ys.append(od_ys[i]/id_ys[i])

    if is_heat:
        plot_heatmap(xs,ys,ax4,['log','linear'],fig)
    else:
        ax4.scatter(xs,ys)

    ax4.set_xscale('log')
    ax4.set_xlabel('citation count\n(e)')
    ax4.set_ylabel('ACMV')
    ax4.set_title('ACMV distribution')

    max_dict = defaultdict(int)
    for i,xv in enumerate(xs):
        if ys[i] > max_dict[xv]:
            max_dict[xv] = ys[i]

    xs = []
    ys = []
    for x in sorted(max_dict.keys()):
        xs.append(x)
        ys.append(max_dict[x])

    ax4.plot(xs,ys,c=color_sequence[3],alpha=0.8)
    fit_z = [i for i in zip(*lowess(ys,np.log(xs),frac=0.05,it=1,is_sorted =True))[1]]
    ax4.plot(xs,fit_z,c='r')

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
    plt.savefig(outpath,dpi=300)
    print 'figure saved to {:}'.format(outpath)




if __name__ == '__main__':

    if len(sys.argv) < 2:
        is_heat = False
    else:
        is_heat = True
        
    plot_dis_over_count(is_heat)