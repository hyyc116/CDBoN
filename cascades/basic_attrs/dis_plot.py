#coding:utf-8
'''
@author: hy@tTt
最基本属性的分布图

'''
from basic_config import *

# 统计指标的分布图
def stats_plot():
    logging.info('plot data ...')
    #### node size 
    logging.info('plot node size ...')
    cnum_dict = json.loads(open('data/nodes_size.json').read())
    xs=[]
    ys=[]
    total = float(sum(cnum_dict.values()))
    _80_total = float(0)
    _80_x = 0
    _80_y = 0
    _max_y = 0
    _min_y = 1
    for num in sorted([int(num) for num in cnum_dict.keys()]):
        v = cnum_dict[str(num)]
        xs.append(num)
        ys.append(v/float(total))


        if _80_total/total<0.8 and (_80_total+v)/total>0.8:
            _80_x = num
            _80_y = v/float(total)

        _80_total+= v

        if v/float(total)>_max_y:
            _max_y = v/float(total)

        if v/float(total) < _min_y:
            _min_y = v/float(total)

    cd_start,cd_end = paras_square(xs,ys,'aminer_cd',total)
    cd_xs,cd_ys,cd_80_x,cd_min_y,cd_max_y = xs,ys,_80_x,_min_y,_max_y

    logging.info('plotting edge size ...')
    enum_dict = json.loads(open('data/cascade_size.json').read())
    total = float(sum(enum_dict.values()))
    _80_total = float(0)
    _80_x = 0
    _80_y = 0
    _max_y = 0
    _min_y = 1
    xs=[]
    ys=[]
    for num in sorted([int(num) for num in enum_dict.keys()]):
        xs.append(num)
        v = enum_dict[str(num)]
        ys.append(v/total)

        if _80_total/total<0.8 and (_80_total+v)/total>0.8:
            _80_x = num
            _80_y = v/total

        _80_total+= v

        if v/total>_max_y:
            _max_y = v/total

        if v/total < _min_y:
            _min_y = v/total

    sd_start,sd_end = paras_square(xs,ys,'aminer_sd',total)
    sd_xs,sd_ys,sd_80_x,sd_min_y,sd_max_y = xs,ys,_80_x,_min_y,_max_y

    fig,axes = plt.subplots(4,1,figsize=(6,20))
    ax1 = axes[0]
    xs,ys,_80_x,_min_y,_max_y = cd_xs,cd_ys,cd_80_x,cd_min_y,cd_max_y
    start,end = cd_start,cd_end
    popt,pcov = curve_fit(power_low_func,xs[start:end],ys[start:end])
    ax1.plot(xs,ys,'o',fillstyle='none')
    ax1.plot(np.linspace(start, end, 10), power_low_func(np.linspace(start, end, 10), *popt)*10,label='$\\alpha={:.2f}$'.format(popt[0]))
    ax1.set_title('Cascade size distribution')
    ax1.set_xlabel('$x=$cascade size\n(a)')
    ax1.set_ylabel('$N_{size}(x)/N$')
    # plot the 80%
    ax1.plot([_80_x]*10,np.linspace(_min_y,_max_y,10),'--',label='$x={:}$'.format(_80_x))
    # ax1.text(_80_x-5,_80_y,'({:},{:})'.format(_80_x,_80_y))
    ax1.legend()
    ax1.text(1,0.001,'AMiner',color='k',fontweight='bold',size=25)
    ax1.set_yscale('log')
    ax1.set_xscale('log')

    #### cascade size
    ax2 = axes[1]
    xs,ys,_80_x,_min_y,_max_y = sd_xs,sd_ys,sd_80_x,sd_min_y,sd_max_y
    start,end = sd_start,sd_end
    ax2.plot(xs,ys,'o',fillstyle='none')
    popt,pcov = curve_fit(power_low_func,xs[start:end],ys[start:end])
    ax2.plot(np.linspace(start, end, 10), power_low_func(np.linspace(start, end, 10), *popt)*10,label='$\\alpha={:.2f}$'.format(popt[0]))
    ax2.plot([_80_x]*10,np.linspace(_min_y,_max_y,10),'--',label='$x={:}$'.format(_80_x))
    ax2.set_title('Edge count distribution')
    ax2.set_xlabel('$x=$edge count\n(b)')
    ax2.set_ylabel('$N_{edge}(x)/N$')

    ax2.set_yscale('log')
    ax2.set_xscale('log') 
    ax2.legend()
    ## 画 para space
    sd_xs = xs
    sd_ys = ys
    sd_total = int(total)

    ####depth
    logging.info('plotting cascade depth ...')
    depth_dict = json.loads(open('data/depth.json').read())
    ax3=axes[2]
    xs=[]
    ys=[]
    total = float(sum(depth_dict.values()))
    _80_total = float(0)
    _80_x = 0
    _80_y = 0
    _max_y = 0
    _min_y = 1
    for depth in sorted([int(i) for i in depth_dict.keys()]):
        xs.append(int(depth))
        v = depth_dict[str(depth)]
        ys.append(v/total)

        if _80_total/total<0.8 and (_80_total+v)/total>0.8:
            _80_x = depth
            _80_y = v/total

        _80_total+= v

        if v/total>_max_y:
            _max_y = v/total

        if v/total < _min_y:
            _min_y = v/total

    # use exponential func to fit the distribution

    popt,pcov = curve_fit(exponential_func,xs[5:],ys[5:])

    print xs
    print ys
    ax3.plot(xs,ys,'o',fillstyle='none')
    mean  = 1/popt[0]
    ax3.plot(np.linspace(1, 26, 26), exponential_func(np.linspace(1, 26, 26), *popt)*1.5,label='$\\lambda={:.2f}$'.format(popt[0]))
    ax3.set_xlabel('$x=$cascade depth\n(c)')
    ax3.set_ylabel('$N_{depth}(x)/N$')
    ax3.plot([_80_x]*10,np.linspace(_min_y,_max_y,10),'--',label='x={:}'.format(_80_x))
    # ax3.plot([mean]*10,np.linspace(10,100000,10),'--',label='mean={:.2f}'.format(mean))
   
    ax3.set_title('Cascade depth distribution')
    ax3.set_yscale('log')
    # ax3.set_xlim(0,13)
    ax3.set_xticks(range(14),[str(i) for i in range(14)])
    ax3.set_xlim(0,40)
    ax3.legend()

    #### In and out degree
    logging.info('plotting degree ...')
    in_degree_dict=json.loads(open('data/in_degree.json').read())
    out_degree_dict=json.loads(open('data/out_degree.json').read())
    ax4 = axes[3]
    xs=[]
    ys=[]
    total = float(sum(in_degree_dict.values()))
    _80_total = float(0)
    _80_x = 0
    _80_y = 0
    _max_y = 0
    _min_y = 1
    for ind in sorted([int(i) for i in in_degree_dict.keys()]):
            
        xs.append(ind+1)
        v = in_degree_dict[str(ind)]
        ys.append(v/total)

        if _80_total/total<0.8 and (_80_total+v)/total>0.8:
            _80_x = ind+1
            _80_y = v/total

        _80_total+= v

        if v/total>_max_y:
            _max_y = v/total

        if v/total<_min_y:
            _min_y = v/total


    

    popt,pcov = curve_fit(power_low_func,xs[10:100],ys[10:100])
    ax4.plot(xs,ys,'o',fillstyle='none',label='In-degree')
    ax4.set_xlabel('$x = degree$\n(d)')
    ax4.set_ylabel('$N_{degree}(x)/N$')
    
    ax4.plot(np.linspace(20, 200, 10), power_low_func(np.linspace(20, 200, 10), *popt)*10,label='$\\alpha={:.2f}$'.format(popt[0]),c=color_sequence[9])
    ax4.plot([_80_x]*10,np.linspace(_min_y,_max_y,10),'--',label='$x={:}$'.format(_80_x),c='g')


    popt,pcov = curve_fit(power_low_func,xs[:10],ys[:10])
    ax4.plot(np.linspace(1, 10, 10), power_low_func(np.linspace(1, 10, 10), *popt)*10,label='$\\alpha={:.2f}$'.format(popt[0]),c=color_sequence[2],marker='^')

    ax4.set_title('Degree distribution')
    ax4.set_yscale('log')
    ax4.set_xscale('log')
    ax4.legend()

    # ax2=axes[1]
    # ax2.scatter(cascade_sizes,cascade_depths,marker='.')

    ax5=axes[3]
    xs=[]
    ys=[]
    total = float(sum(out_degree_dict.values()))
    _80_total = float(0)
    _80_x = 0
    _80_y = 0
    _max_y = 0
    _min_y = 1
    for od in sorted([int(i) for i in out_degree_dict.keys()]):
        xs.append(od)
        v = out_degree_dict[str(od)]
        ys.append(v/total)

        if _80_total/total<0.8 and (_80_total+v)/total>0.8:
            _80_x = od
            _80_y = v/total

        _80_total+= v

        if v/total>_max_y:
            _max_y = v/total

        if v/total < _min_y:
            _min_y = v/total

    popt,pcov = curve_fit(power_low_func,xs[10:40],ys[10:40]) 
    ax5.plot(xs,ys,'o',fillstyle='none',label='Out-degree',c='r')


    ax5.plot(np.linspace(10, 30, 10), power_low_func(np.linspace(10, 30, 10), *popt)/10,label='$\\alpha={:.2f}$'.format(popt[0]),c=color_sequence[7])
    # ax5.plot([_80_x]*10,np.linspace(_min_y,_max_y,10),'--',label='$x={:}$'.format(_80_x))

    # ax5.set_title('out degree distribution')
    # ax5.set_xlabel('$x = deg^{+}(v)$\n(e)')
    # ax5.set_ylabel('$N(x)$')
    # ax5.set_xscale('log')
    # ax5.set_yscale('log')
    ax5.legend()

    plt.tight_layout()
    plt.savefig('pdf/statistics.pdf',dpi=300)
    logging.info('figures saved to pdf/statistics.pdf.')




### centrality
def plot_centrality():
    num = len(plt.get_fignums())
    # plt.figure(num)
    fig,axes = plt.subplots(1,5,figsize=(25,5))
    #### node size 
    # logging.info('plot node size ...')sz 
    centrality_dict = json.loads(open('data/centrality.json').read())

    # degree 
    indegree_list = centrality_dict['indegree']
    ax1 = axes[0]
    plot_cumulative_dis(ax1,indegree_list,'in degree centrality','$x$','$P_x$',False,False)

    outdegree_list = centrality_dict['outdegree']
    ax2 = axes[1]
    plot_cumulative_dis(ax2,outdegree_list,'out degree centrality','$x$','$P_x$',False,True)
    # closeness 
    closeness_list = centrality_dict['closeness']
    ax3 = axes[2]
    plot_cumulative_dis(ax3,closeness_list,'closeness','$x$','$P_x$',False,False)
    # betweenness
    betweenness_list = centrality_dict['betweenness']
    ax4 = axes[3]
    plot_cumulative_dis(ax4,betweenness_list,'betweenness','$x$','$P_x$',False,False)
    # katz
    katz_list = centrality_dict['katz']
    ax5= axes[4]
    plot_cumulative_dis(ax5,katz_list,'katz','$x$','$P_x$',False,False)


    plt.tight_layout()
    plt.savefig('pdf/centrality.pdf',dpi=200)

# plot one kind of centrality
def plot_cumulative_dis(ax,alist,title,xlabel,ylabel,isxlog=True,isylog=True):
    acounter = Counter(alist)
    total = float(len(alist))
    last_num = len(alist)
    xs = []
    ys = []
    for a in sorted(acounter.keys()):
        xs.append(a)
        ys.append(last_num/total)
        last_num = last_num-acounter[a]

    # xs = np.array(xs)+0.000001
    ax.plot(xs,ys)
    if isxlog:
        ax.set_xscale('log')
    if isylog:
        ax.set_yscale('log')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


if __name__ == '__main__':
    stats_plot()