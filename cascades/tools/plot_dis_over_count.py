#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *

def plot_heatmap(x,y,ax,bins,fig,gridsize=50):
    hb = ax.hexbin(x, y, gridsize=gridsize, cmap=CM.Blues, bins='log',xscale=bins[0] ,yscale=bins[1])

# 随着citation count的增加，各个指标的变化
def plot_dis_over_count(is_heat=False):

    plot_dict = json.loads(open('data/plot_dict.json').read())
    ###plot the comparison figure
    cxs= plot_dict['cxs']
    eys= plot_dict['eys']
    dys= plot_dict['dys']
    dcxs=plot_dict['dcx']
    od_ys = plot_dict['od_ys']
    id_ys = plot_dict['id_ys']

    for ii,indgree in enumerate(id_ys):
        if indgree==1:
            print cxs[ii],indgree

    num = len(plt.get_fignums())
    # plt.figure(num)
    fig,axes = plt.subplots(1,5,figsize=(25,5))

    print 'length of cxs:{:},eys:{:},dcxs:{:},dys:{:},od_ys:{:},id_ys:{:}'.format(len(cxs),len(eys),len(dcxs),len(dys),len(od_ys),len(id_ys))

    
    rys=[]
    max_dict = defaultdict(int)
    equal_dict=defaultdict(list)

    for i in range(len(cxs)):
        y  = eys[i]/float(cxs[i])-1
        rys.append(y)
        if y> max_dict[cxs[i]]:
            max_dict[cxs[i]] = y

        if eys[i]==cxs[i]:
            equal_dict[cxs[i]].append(1)
        else:
            equal_dict[cxs[i]].append(0)

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
    ## ratio of cascade size/ ciattion count vs citation count
    ax1 = axes[1]
    fit_x = []
    fit_y = []
    for key in sorted(max_dict.keys()):
        fit_x.append(key)
        fit_y.append(max_dict[key])

    if is_heat:
        plot_heatmap(cxs,rys,ax1,['log','linear'],fig)
    else:
        ax1.scatter(cxs,rys)
    
    ax1.plot(fit_x,fit_y,c=color_sequence[3],alpha=0.8)
    fit_z = [i for i in zip(*lowess(fit_y,np.log(fit_x),frac= 0.08))[1]]
    ax1.plot(fit_x,fit_z,c='r')
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
    if is_heat:
        plt.savefig('pdf/compare_heat.png',dpi=200)
        print 'figure saved to pdf/compare_heat.png'
    else:
        plt.savefig('pdf/compare.png',dpi=200)
        print 'figure saved to pdf/compare.png'


if __name__ == '__main__':

    if len(sys.argv) < 2:
        is_heat = False
    else:
        is_heat = True
        
    plot_dis_over_count(is_heat)