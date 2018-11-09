#coding:utf-8
'''
@author: hy@tTt
最基本的那些属性的分布图

'''
from basic_config import *


# 统计指标的分布图
def stats_plot(dirpath):
    dirpath = dirpath[:-1] if dirpath.endswith('/') else dirpath

    logging.info('plot data ...')

    logging.info('plot node size ...')
    cnum_dict = json.loads(open('{:}/citation_count.json'.format(dirpath)).read())
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

        if num==10:
            print 'cascade size:',10,'percentage:',v/float(total)

        if num==20:
            print 'cascade size:',20,'percentage:',v/float(total)

        if num==100:
            print 'cascade size:',100,'percentage:',v/float(total)

        if _80_total/total<0.8 and (_80_total+v)/total>0.8:
            _80_x = num
            _80_y = v/float(total)

        _80_total+= v

        if v/float(total)>_max_y:
            _max_y = v/float(total)

        if v/float(total) < _min_y:
            _min_y = v/float(total)

    # check_powlaw_exponential(xs,[y*int(total) for y in ys],'citation count')

    ## 画 para space
    cd_start,cd_end = paras_square(xs,ys,'mag_cd',total)
    cd_xs,cd_ys,cd_80_x,cd_min_y,cd_max_y = xs,ys,_80_x,_min_y,_max_y

    logging.info('plotting edge size ...')
    enum_dict = json.loads(open('{:}/cascade_size.json'.format(dirpath)).read())
    # plot_dict = json.loads(open('data/mag/stats/plot_dict.json').read())
    # enum_dict = Counter(plot_dict['eys'])
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

        if num==10:
            print 'edge size:',10,'percentage:',v/float(total)

        if num==20:
            print 'edge size:',20,'percentage:',v/float(total)

        if num==100:
            print 'edge size:',100,'percentage:',v/float(total)


        if _80_total/total<0.8 and (_80_total+v)/total>0.8:
            _80_x = num
            _80_y = v/total

        _80_total+= v

        if v/total>_max_y:
            _max_y = v/total

        if v/total < _min_y:
            _min_y = v/total

    # check_powlaw_exponential(xs,[y*int(total) for y in ys],'edge size')


    sd_start,sd_end = paras_square(xs,ys,'mag_sd',total)
    sd_xs,sd_ys,sd_80_x,sd_min_y,sd_max_y = xs,ys,_80_x,_min_y,_max_y


    fig,axes = plt.subplots(2,2,figsize=(10,10))
    #### node size
    ax1 = axes[0,0]
    xs,ys,_80_x,_min_y,_max_y = cd_xs,cd_ys,cd_80_x,cd_min_y,cd_max_y

    xs,ys = convert_pdf_2_ccdf(xs,ys)
    start,end = 100,1000
    popt,pcov = curve_fit(power_low_func,xs[start:end],ys[start:end])
    ax1.plot(xs,ys,'-')
    ax1.plot(np.linspace(start, end, 10), power_low_func(np.linspace(start, end, 10), *popt)*10,label='$\\alpha={:.2f}$'.format(popt[0]))
    ax1.set_title('cascade size distribution')
    ax1.set_xlabel('cascade size\n(a)')
    ax1.set_ylabel('$P(cascade$ $size)$')
    ax1.set_yscale('log')
    ax1.set_xscale('log')
    # ax1.text(1,0.001,'MAG',color='k',fontweight='bold',size=25)
    # ax1.plot([_80_x]*10,np.linspace(_min_y,_max_y,10),'--',label='$x={:}$'.format(_80_x))
    ax1.legend()

    #### cascade size
    ax2 = axes[0,1]
    xs,ys,_80_x,_min_y,_max_y = sd_xs,sd_ys,sd_80_x,sd_min_y,sd_max_y
    start,end = 500,5000
    xs,ys = convert_pdf_2_ccdf(xs,ys)

    ax2.plot(xs,ys,'-')
    popt,pcov = curve_fit(power_low_func,xs[start:end],ys[start:end])
    ax2.plot(np.linspace(start, end, 10), power_low_func(np.linspace(start, end, 10), *popt)*10,label='$\\alpha={:.2f}$'.format(popt[0]))
    # ax2.plot([_80_x]*10,np.linspace(_min_y,_max_y,10),'--',label='$x={:}$'.format(_80_x))
    ax2.set_title('edge count distribution')
    ax2.set_xlabel('edge count\n(b)')
    ax2.set_ylabel('$P(edge$ $count)$')

    ax2.set_yscale('log')
    ax2.set_xscale('log')
    ax2.legend()

    ####depth
    logging.info('plotting cascade depth ...')
    depth_dict = json.loads(open('{:}/depth.json'.format(dirpath)).read())
    ax3=axes[1,0]
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
    # check_powlaw_exponential(xs,[y*int(total) for y in ys],'depth')

    popt,pcov = curve_fit(exponential_func,xs[5:20],ys[5:20])

    ax3.plot(xs,ys,'o',fillstyle='none')
    mean  = 1/popt[0]
    ax3.plot(np.linspace(1, 26, 26), exponential_func(np.linspace(1, 26, 26), *popt)*1.5,label='$\\alpha={:.2f}$'.format(popt[0]))
    ax3.set_xlabel('depth\n(c)')
    ax3.set_ylabel('$P(depth)$')
    # ax3.plot([_80_x]*10,np.linspace(_min_y,_max_y,10),'--',label='x={:}'.format(_80_x))
    # ax3.plot([mean]*10,np.linspace(10,100000,10),'--',label='mean={:.2f}'.format(mean))

    ax3.set_title('cascade depth distribution')
    ax3.set_yscale('log')
    # ax3.set_xscale('log')

    # ax3.set_xlim(0,13)
    ax3.set_xticks(range(14),[str(i) for i in range(14)])
    ax3.legend()

    #### In and out degree
    logging.info('plotting degree ...')
    in_degree_dict=json.loads(open('{:}/in_degree.json'.format(dirpath)).read())
    out_degree_dict=json.loads(open('{:}/out_degree.json'.format(dirpath)).read())
    ax4 = axes[1,1]
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


    # check_powlaw_exponential(xs,[y*int(total) for y in ys],'in-degree')
    xs,ys = convert_pdf_2_ccdf(xs,ys)

    popt,pcov = curve_fit(power_low_func,xs[30:200],ys[30:200])
    ax4.plot(xs,ys,'-',label='In-degree')
    ax4.set_xlabel('degree\n(d)')
    ax4.set_ylabel('$P(degree)$')

    ax4.plot(np.linspace(50, 400, 10), power_low_func(np.linspace(50, 400, 10), *popt)*10,label='$\\alpha={:.2f}$'.format(popt[0]),c=color_sequence[9])
    # ax4.plot([_80_x]*10,np.linspace(_min_y,_max_y,10),'--',label='$x={:}$'.format(_80_x),c='g')


    popt,pcov = curve_fit(power_low_func,xs[:10],ys[:10])
    ax4.plot(np.linspace(1, 10, 10), power_low_func(np.linspace(1, 10, 10), *popt)*10,label='$\\alpha={:.2f}$'.format(popt[0]),c=color_sequence[2],marker='^')

    ax4.set_title('degree distribution')
    ax4.set_yscale('log')
    ax4.set_xscale('log')
    ax4.legend()

    # ax2=axes[1]
    # ax2.scatter(cascade_sizes,cascade_depths,marker='.')

    ax5=axes[1,1]
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

    # check_powlaw_exponential(xs,[y*int(total) for y in ys],'out degree')
    xs,ys = convert_pdf_2_ccdf(xs,ys)

    popt,pcov = curve_fit(power_low_func,xs[10:100],ys[10:100])
    ax5.plot(xs,ys,'-',label='Out-degree',c='r')


    ax5.plot(np.linspace(10, 100, 10), power_low_func(np.linspace(10, 100, 10), *popt)/10,label='$\\alpha={:.2f}$'.format(popt[0]),c=color_sequence[7])
    # ax5.plot([_80_x]*10,np.linspace(_min_y,_max_y,10),'--',label='$x={:}$'.format(_80_x))

    # ax5.set_title('out degree distribution')
    # ax5.set_xlabel('$x = deg^{+}(v)$\n(e)')
    # ax5.set_ylabel('$N(x)$')
    # ax5.set_xscale('log')
    # ax5.set_yscale('log')
    ax5.legend()

    plt.tight_layout()
    plt.savefig('pdf/mag_statistics.jpg',dpi=300)
    logging.info('figures saved to pdf/mag_statistics.png.')


def check_powlaw_exponential(xs,ys,label):
    data = []
    for i,x in enumerate(xs):
        data.extend([x]*int(ys[i]))

    fit = powerlaw.Fit(data,xmin=1)
    print 'xmin', fit.xmin
    print '============= power law check {:} =============='.format(label)
    print fit.distribution_compare('power_law', 'exponential', normalized_ratio = True)

    print '======================================='


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
    plt.savefig('pdf/mag_centrality.pdf',dpi=200)

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

#     ============= power law check citation count ==============
# (11.294904216533055, 1.3905557491778108e-29) citation count是一种显著的power law, p<0.05
# =======================================

# Calculating best minimal value for power law fit
# ============= power law check edge size ==============
# (0.24671177213646589, 0.80513129529321137)  edge size是两种都合适的分布，因为p>0.05
# =======================================

# ============= power law check depth ==============
# (9.2058672832144133, 3.3892306051537122e-20), depth分布也是显著的power law
# =======================================

# ============= power law check in-degree ==============
# (5.8081371871992289, 6.3171746170651354e-09), indegree 显著power law
# =======================================


# ============= power law check out degree ==============
# (29.564084267525804, 4.3288680764554347e-192), out degreee是显著power law



    ## python tools/mag_dis_plot.py data/mag/stats/
    stats_plot(sys.argv[1])