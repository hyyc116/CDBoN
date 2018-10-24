from para_config import *
from Citation_friction import *
from scipy import stats
import matplotlib.pylab as pylab
import math

def plot_ten_delta_ti():

    low_json = 'data/low_selected_papers.json'
    medium_json = 'data/medium_selected_papers.json'
    high_json = 'data/high_selected_papers.json'
    xyfunc_name = 'co_delta_ti'
    i=10
    is_scale=1
    low=0.8
    up=40


    if xyfunc_name=='co_ti_i':
        xyfunc = co_ti_i
        yls = 'Length of Time'
        xls = '$i^{th}$ citation'
        low = int(low)
        up = int(up)

    elif xyfunc_name=='co_delta_ti':
        xyfunc = co_delta_ti
        yls = '$T_i$'
        xls = '$i^{th}$ citation'
        low = float(low)
        up = int(up)

    elif xyfunc_name=='co_ti_di':
        xyfunc = co_ti_di
        yls = '$t_i/i$'
        xls = 'citation order $i$'
    elif xyfunc_name=='cy_cyi_yi':
        xyfunc = cy_cyi_yi
        xls='t'
        yls='Number of citations'
        low = -1
        up = -1

    elif xyfunc_name=='cy_cyi_dyi':
        xyfunc = cy_cyi_dyi
        xls='t'
        yls='Average Speed'
        low = int(low)
        up = int(up)

    elif xyfunc_name=='cy_yi_dcyi':
        xyfunc = cy_yi_dcyi
        xls='t'
        yls='$Average time$'
        low = float(low)
        up = float(up)

    elif xyfunc_name=='cy_delta_cyi_yi':
        xyfunc = cy_delta_cyi_yi
        xls='t'
        yls='Number of citation'
        low = -1
        up = -1

    elif xyfunc_name=='cy_delta_yi':
        xyfunc = cy_delta_yi
        xls='citation year $y_i$'
        yls='$\Delta y_i$'
    elif xyfunc_name=='cy_delta_cyi_ddelta_yi':
        xyfunc = cy_delta_cyi_ddelta_yi
        xls='citation year $y_i$'
        yls='$\Delta C_{y_i}/\Delta y_i$'

    elif xyfunc_name=='cy_delta_yi_ddelta_cyi':
        xyfunc = cy_delta_yi_ddelta_cyi
        xls='citation year $y_i$'
        yls='$\Delta y_i/\Delta C_{y_i}$'

    print xyfunc_name,'with i=',i,'low',low,'up',up

    params = {'legend.fontsize': 15,
         'axes.labelsize': 15,
         'axes.titlesize':20,
         'xtick.labelsize':15,
         'ytick.labelsize':15,
         'font.family':'Times New Roman'}
    pylab.rcParams.update(params)

    fig,((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(2,3,figsize=(15,10))
    
    
    print 'low cited papers'
    low_xy_dict = citation_order(low_json,xyfunc,i)
    title = 'Low cited papers'
    xlabels,means,medians,modes,lr_report = boxplot_level(ax1,low_xy_dict,title,xls+"\n(a)",yls,is_scale,low,up)
    ax4.plot(xlabels,means,'-o',label='Low')
    ax5.plot(xlabels,medians,'-o',label='Low')
    ax6.plot(xlabels,modes,'-o',label='Low')
    open('regression/ten_low_report.txt','w').write(lr_report)

    print 'Medium cited papers'
    medium_xy_dict = citation_order(medium_json,xyfunc,i)
    title = 'Medium cited papers'
    xlabels,means,medians,modes,lr_report = boxplot_level(ax2,medium_xy_dict,title,xls+"\n(b)",yls,is_scale,low,up)
    ax4.plot(xlabels,means,'-^',label='Medium')
    ax5.plot(xlabels,medians,'-^',label='Medium')
    ax6.plot(xlabels,modes,'-^',label='Medium')
    open('regression/ten_medium_report.txt','w').write(lr_report)


    print 'high cited papers'
    high_xy_dict = citation_order(high_json,xyfunc,i)
    title = 'High cited papers'
    xlabels,means,medians,modes,lr_report = boxplot_level(ax3,high_xy_dict,title,xls+"\n(c)",yls,is_scale,low,up)
    ax4.plot(xlabels,means,'-*',label='High')
    ax5.plot(xlabels,medians,'-*',label='High')
    ax6.plot(xlabels,modes,'-*',label='High')
    open('regression/ten_high_report.txt','w').write(lr_report)

    ax3.legend()
    ax4.set_title('Comparison of Means')
    ax5.set_title('Comparison of Medians')
    ax6.set_title('Comparison of Modes')
    ax4.set_xlabel('$i^{th}$ citation\n(d)')
    ax5.set_xlabel('$i^{th}$ citation\n(e)')
    ax6.set_xlabel('$i^{th}$ citation\n(f)')
    ax4.set_ylabel('$T_i$')
    ax5.set_ylabel('$T_i$')
    ax6.set_ylabel('$T_i$')
    ax1.set_ylabel('$T_i$')
    ax4.set_ylim(-0.2,3)
    ax5.set_ylim(-0.2,3)
    ax6.set_ylim(-0.2,3)
    ax4.legend()
    ax5.legend()
    ax6.legend()

    # fig.subplots_adjust(wspace=0)

    # yticklabels = ax2.get_yticklabels() + ax3.get_yticklabels()
    # plt.setp(yticklabels, visible=False)
    plt.tight_layout()
    namepath = 'pdf/one_more_three_levels.pdf'
    plt.savefig(namepath,dpi=300)
    print 'Result saved to',namepath


def boxplot_level(ax,xs_ys_dict,title,xls,yls,is_scale=0,low=0,up=60):
    # last_ys = []
    box_data_dict=defaultdict(list)
    lr_xs = []
    lr_ys = []
    for key in xs_ys_dict.keys():
        xs,ys = xs_ys_dict[key]
        for i,x in enumerate(xs):
            if x>1:
                box_data_dict[x].append(ys[i]+1)
            else:
                box_data_dict[x].append(ys[i])

            lr_xs.append(x)
            if x>1:
                lr_ys.append(ys[i])
            else:
                lr_ys.append(ys[i]-1)

    box_data = []
    xlabels = []
    means = []
    medians = [] 
    modes = []
    for label in sorted(box_data_dict.keys()):
        xlabels.append(label)
        box_data.append(box_data_dict[label])
        means.append(sum(box_data_dict[label])/float(len(box_data_dict[label])))
        medians.append(np.median(box_data_dict[label]))
        modes.append(stats.mode(np.array(box_data_dict[label]))[0][-1])

    print modes
    ax.violinplot(box_data,showmeans=False,showmedians=False) 
    ax.set_xticks(np.arange(1, len(xlabels) + 1))
    ax.set_xticklabels(xlabels)
    ax.plot(xlabels,means,c='r',label='mean')
    ax.plot(xlabels,medians,c='#ff7f0e',label='median')
    ax.plot(xlabels,modes,c='g',label='mode')
    ax.set_title(title)
    ax.set_xlabel(xls)
    ax.set_ylabel(yls)

    if is_scale==1:
        ax.set_yscale('log')
    if low!=-1:
        ax.set_ylim(low,up)
    # ax.set_xlim(0,50)
    # ax.set_ylim(0,ylims_up)
    # return last_ys
    return xlabels,np.array(means)-1,np.array(medians)-1,np.array(modes)-1,','.join(LR(lr_xs,lr_ys))

def plot_zone_delta_ti():

    low_json = 'data/low_selected_papers.json'
    medium_json = 'data/medium_selected_papers.json'
    high_json = 'data/high_selected_papers.json'
    xyfunc = co_delta_ti
    i='all'
    is_scale=1
    low=0.8
    up=40

    yls = 'average $T_i$'
    xls = '$i^{th}$ zone'
    low = float(low)
    up = int(up)


    params = {'legend.fontsize': 15,
         'axes.labelsize': 15,
         'axes.titlesize':20,
         'xtick.labelsize':15,
         'ytick.labelsize':15,
         'font.family':'Times New Roman'}
    pylab.rcParams.update(params)

    fig,((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(2,3,figsize=(15,10))
    
    
    print 'low cited papers'
    low_xy_dict = citation_order(low_json,xyfunc,i)
    title = 'lowly cited papers'
    xlabels,means,medians,modes,lr_report = boxplot_zone(ax1,low_xy_dict,title,xls+"\n(a)",yls,is_scale,low,up)
    ax4.plot(xlabels,means,'-o',label='Low')
    ax5.plot(xlabels,medians,'-o',label='Low')
    ax6.plot(xlabels,modes,'-o',label='Low')
    open('regression/zone_low_report.txt','w').write(lr_report)

    print 'Medium cited papers'
    medium_xy_dict = citation_order(medium_json,xyfunc,i)
    title = 'medium cited papers'
    xlabels,means,medians,modes,lr_report = boxplot_zone(ax2,medium_xy_dict,title,xls+"\n(b)",yls,is_scale,low,up)
    ax4.plot(xlabels,means,'-^',label='Medium')
    ax5.plot(xlabels,medians,'-^',label='Medium')
    ax6.plot(xlabels,modes,'-^',label='Medium')
    open('regression/zone_medium_report.txt','w').write(lr_report)


    print 'highly cited papers'
    high_xy_dict = citation_order(high_json,xyfunc,i)
    title = 'highly cited papers'
    xlabels,means,medians,modes,lr_report = boxplot_zone(ax3,high_xy_dict,title,xls+"\n(c)",yls,is_scale,low,up)
    ax4.plot(xlabels,means,'-*',label='High')
    ax5.plot(xlabels,medians,'-*',label='High')
    ax6.plot(xlabels,modes,'-*',label='High')
    open('regression/zone_high_report.txt','w').write(lr_report)

    ax3.legend()
    ax4.set_title('comparison of means')
    ax5.set_title('comparison of medians')
    ax6.set_title('comparison of modes')
    ax4.set_xlabel('$i^{th}$ zone\n(d)')
    ax5.set_xlabel('$i^{th}$ zone\n(e)')
    ax6.set_xlabel('$i^{th}$ zone\n(f)')
    ax4.set_ylim(-0.2,3)
    ax5.set_ylim(-0.2,3)
    ax6.set_ylim(-0.2,3)
    ax4.set_ylabel('average $T_i$')
    ax4.set_ylabel('average $T_i$')
    ax5.set_ylabel('average $T_i$')
    ax6.set_ylabel('average $T_i$')
    ax4.legend()
    ax5.legend()
    ax6.legend()

    # fig.subplots_adjust(wspace=0)

    # yticklabels = ax2.get_yticklabels() + ax3.get_yticklabels()
    # plt.setp(yticklabels, visible=False)
    plt.tight_layout()
    namepath = 'pdf/zone_three_levels.jpg'
    plt.savefig(namepath,dpi=300)
    print 'Result saved to',namepath


def boxplot_zone(ax,xs_ys_dict,title,xls,yls,is_scale=0,low=0,up=60):
    # last_ys = []
    box_data_dict=defaultdict(list)
    lr_xs = []
    lr_ys = []
    for key in xs_ys_dict.keys():
        xs,ys = xs_ys_dict[key]
        size = float(len(xs))
        paper_zone=defaultdict(list)
        for i,x in enumerate(xs):
            zone = int(math.ceil((i+1)*5/size))
            if x>1:
                paper_zone[zone].append(ys[i]+1)
            else:
                paper_zone[zone].append(ys[i])
        
        for zone in sorted(paper_zone.keys()):
            zone_mean = np.mean(paper_zone[zone])
            box_data_dict[zone].append(zone_mean)
            lr_xs.append(zone)
            lr_ys.append(zone_mean-1)


    box_data = []
    xlabels = []
    means = []
    medians = [] 
    modes = []
    for label in sorted(box_data_dict.keys()):
        xlabels.append(label)
        box_data.append(box_data_dict[label])
        means.append(sum(box_data_dict[label])/float(len(box_data_dict[label])))
        medians.append(np.median(box_data_dict[label]))
        modes.append(stats.mode(np.array(box_data_dict[label]))[0][-1])

    print xlabels
    ax.violinplot(box_data,showmeans=False,showmedians=False) 
    ax.set_xticks(np.arange(1, len(xlabels) + 1))
    ax.set_xticklabels(xlabels)
    ax.plot(xlabels,means,c='r',label='mean')
    ax.plot(xlabels,medians,c='#ff7f0e',label='median')
    ax.plot(xlabels,modes,c='g',label='mode')
    ax.set_title(title)
    ax.set_xlabel(xls)
    ax.set_ylabel(yls)

    if is_scale==1:
        ax.set_yscale('log')
    if low!=-1:
        ax.set_ylim(low,up)
    # ax.set_xlim(0,50)
    # ax.set_ylim(0,ylims_up)
    # return last_ys
    return xlabels,np.array(means)-1,np.array(medians)-1,np.array(modes)-1,','.join(LR(lr_xs,lr_ys))

def LR(xs,ys):
    X=np.array(xs)
    # X=np.column_stack((xs, xs**2))
    y=np.array(ys)
    X=sm.add_constant(X)
    est=sm.OLS(y,X).fit()
    print 'params',est.params
    print 'R2',est.rsquared
    print 'pvalues',est.pvalues
    print 'Numbers', est.nobs
    return '{:.5f}({:.5f})'.format(est.params[0],est.pvalues[0]),'{:.5f}({:.5f})'.format(est.params[1],est.pvalues[1]),str(int(est.nobs)),'{:.5f}'.format(est.rsquared)


def first_citation(cited_papers_json):
    cited_papers = json.loads(open(cited_papers_json).read())

    time_internals = []
    for k in cited_papers.keys():
        paper_dict  = cited_papers[k]
        pid  = paper_dict['pid']
        year = paper_dict['year']
        citations = [(cit.split(',')[0],int(cit.split(',')[1])) for cit in paper_dict['citations']]
        
        cpid, cyear = sorted(citations,key=lambda x:x[1])[0]
        time_internals.append(cyear-year+1)

    internal_counter = Counter(time_internals)
    return internal_counter,np.array(time_internals)


def plot_three_level_first_citations(low,medium,high):
    # fig,axes = plt.subplots(1,3,figszie=(15,5))
    logging.info('plot first citations....')

    # ax1 = axes[0]
    logging.info('Low cited papers ...')

    xlabels  = ['Low','Medium','High']
    box_data = []
    means = []

    internal_dict,time_internals = first_citation(low)
    xs = []
    ys = []
    for i in sorted(internal_dict.keys()):
        xs.append(i)
        ys.append(internal_dict[i])
    ys = np.array(ys)/float(sum(ys))
    plt.plot(xs,ys,label ='low cited papers')
    box_data.append(time_internals)
    means.append(np.mean(time_internals))

    logging.info('Medium cited papers ...')
    internal_dict,time_internals = first_citation(medium)
    xs = []
    ys = []
    for i in sorted(internal_dict.keys()):
        xs.append(i)
        ys.append(internal_dict[i])
    ys = np.array(ys)/float(sum(ys))
    plt.plot(xs,ys,label ='medium cited papers')
    box_data.append(time_internals)
    means.append(np.mean(time_internals))


    logging.info('High cited papers ...')
    internal_dict,time_internals = first_citation(high)
    xs = []
    ys = []
    for i in sorted(internal_dict.keys()):
        xs.append(i)
        ys.append(internal_dict[i])
    ys = np.array(ys)/float(sum(ys))

    plt.plot(xs,ys,label='high cited papers')
    box_data.append(time_internals)
    means.append(np.mean(time_internals))

    plt.legend()
    
    plt.xlim(0,10)
    plt.savefig('pdf/first_citation.pdf',dpi=300)

    logging.info('saved to pdf/first_citation.pdf')

    fig,ax = plt.subplots()
    ax.violinplot(box_data,
                   showmeans=True,
                   showmedians=False)
    ax.set_xticks(np.arange(1, len(xlabels) + 1))
    ax.set_xticklabels(xlabels)
    ax.set_yscale('log')
    ax.set_xlabel('Cited Levels')
    ax.set_ylabel('Response Time')
    ax.text(2.3,20,'mean of low:{:.3f}\nmean of medium:{:.3f}\nmean of high:{:.3f}\n'.format(means[0],means[1],means[2]))
    plt.savefig('pdf/first_citation_box.pdf',dpi=300)
    
    logging.info('saved to pdf/first_citation_box.pdf')





if __name__ == '__main__':
    # plot_three_level_first_citations(sys.argv[1],sys.argv[2],sys.argv[3])
    # plot_ten_delta_ti()
    plot_zone_delta_ti()
