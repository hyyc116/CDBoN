from para_config import *
from Citation_friction import *
from scipy import stats
import matplotlib.pylab as pylab
import math

def plot_ten_ti():

    low_json = 'data/low_selected_papers.json'
    medium_json = 'data/medium_selected_papers.json'
    high_json = 'data/high_selected_papers.json'
    xyfunc= co_ti_i
    i=10
    is_scale=0
    low=0.8
    up=60
    yls = 'Length of Total Time'
    xls = '$i^{th}$ citation'

    # print xyfunc_name,'with i=',i,'low',low,'up',up

    params = {'legend.fontsize': 15,
         'axes.labelsize': 20,
         'axes.titlesize':25,
         'xtick.labelsize':15,
         'ytick.labelsize':15,
         'font.family':'Times New Roman'}
    pylab.rcParams.update(params)

    fig,((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9)) = plt.subplots(3,3,sharex='row',sharey='row',figsize=(15,15))
    
    
    print 'low cited papers'
    low_xy_dict,low_papers = citation_order(low_json,xyfunc,i)
    title = 'Low cited papers'
    all_yss = plot_levels(ax1,low_xy_dict,title,xls+"\n(a)",yls,is_scale,low,up)
    (_1xs,_1ys),(_5xs,_5ys),(_10xs,_10ys) = three_points(all_yss)
    ax4.plot(_1xs,_1ys,'-o',label='Low',c='r')
    ax5.plot(_5xs,_5ys,'-o',label='Low',c='r')
    ax6.plot(_10xs,_10ys,'-o',label='Low',c='r')

    firsts, fives, tens = py_three(all_yss,low_papers)
    ax7.scatter(firsts[1],firsts[0],marker='o',c='r',label='Low',alpha=0.6)
    ax8.scatter(fives[1],fives[0],marker='o',c='r',label='Low',alpha=0.6)
    ax9.scatter(tens[1],tens[0],marker='o',c='r',label='Low',alpha=0.6)

    print 'Medium cited papers'
    medium_xy_dict,medium_papers = citation_order(medium_json,xyfunc,i)
    title = 'Medium cited papers'
    all_yss = plot_levels(ax2,medium_xy_dict,title,xls+"\n(b)",yls,is_scale,low,up)
    (_1xs,_1ys),(_5xs,_5ys),(_10xs,_10ys) = three_points(all_yss)
    ax4.plot(_1xs,_1ys,'-^',label='Medium',c='#ff7f0e')
    ax5.plot(_5xs,_5ys,'-^',label='Medium',c='#ff7f0e')
    ax6.plot(_10xs,_10ys,'-^',label='Medium',c='#ff7f0e')

    firsts, fives, tens = py_three(all_yss,medium_papers)
    ax7.scatter(firsts[1],firsts[0],marker='^',c='#ff7f0e',label='Medium',alpha=0.6)
    ax8.scatter(fives[1],fives[0],marker='^',c='#ff7f0e',label='Medium',alpha=0.6)
    ax9.scatter(tens[1],tens[0],marker='^',c='#ff7f0e',label='Medium',alpha=0.6)


    print 'high cited papers'
    high_xy_dict,high_papers = citation_order(high_json,xyfunc,i)
    title = 'High cited papers'
    all_yss = plot_levels(ax3,high_xy_dict,title,xls+"\n(c)",yls,is_scale,low,up)
    (_1xs,_1ys),(_5xs,_5ys),(_10xs,_10ys) = three_points(all_yss)
    ax4.plot(_1xs,_1ys,'-*',label='High',c='g')
    ax5.plot(_5xs,_5ys,'-*',label='High',c='g')
    ax6.plot(_10xs,_10ys,'-*',label='High',c='g')

    firsts, fives, tens = py_three(all_yss,high_papers)
    ax7.scatter(firsts[1],firsts[0],marker='*',c='g',label='High',alpha=0.6)
    ax8.scatter(fives[1],fives[0],marker='*',c='g',label='High',alpha=0.6)
    ax9.scatter(tens[1],tens[0],marker='*',c='g',label='High',alpha=0.6)


    ax3.legend()
    ax4.set_title('First Citation Distribution')
    ax5.set_title('$5^{th}$ Citation Distribution')
    ax6.set_title('$10^{th}$ Citation Distribution')
    ax4.set_xscale('log')
    ax5.set_xscale('log')
    ax6.set_xscale('log')
    ax4.set_xlabel('years\n(d)')
    ax5.set_xlabel('years\n(e)')
    ax6.set_xlabel('years\n(f)')
    ax4.set_ylabel('Percentage')
    ax1.set_ylabel('Total Time required')
    ax7.set_ylabel('years')
    ax7.set_xlabel('Publication Year\n(g)')
    ax8.set_xlabel('Publication Year\n(h)')
    ax9.set_xlabel('Publication Year\n(i)')
    ax7.set_yscale('log')
    ax8.set_yscale('log')
    ax9.set_yscale('log')
    # ax1.set_xlim(0,)
    ax4.legend()
    ax5.legend()
    ax6.legend()
    ax7.legend()
    ax8.legend()
    ax9.legend()
    # fig.subplots_adjust(wspace=0)

    yticklabels = ax2.get_yticklabels() + ax3.get_yticklabels()
    plt.setp(yticklabels, visible=False)
    plt.tight_layout()
    namepath = 'pdf/total_three_levels.pdf'
    plt.savefig(namepath,dpi=300)
    print 'Result saved to',namepath


def three_points(all_yss):
    firsts = [ys[1][0] for ys in all_yss]
    fives = [ys[1][4] for ys in all_yss]
    tens = [ys[1][-1] for ys in all_yss]

    return counter_xy(firsts),counter_xy(fives),counter_xy(tens)

def py_three(all_yss,cited_papers):
    firsts = [(ys[1][0],cited_papers[str(ys[0])]['year']) for ys in all_yss]
    fives = [(ys[1][4],cited_papers[str(ys[0])]['year']) for ys in all_yss]
    tens = [(ys[1][-1],cited_papers[str(ys[0])]['year']) for ys in all_yss]
    return zip(*firsts),zip(*fives),zip(*tens)

def counter_xy(data_list):
    counter = Counter(data_list)
    xs = []
    ys=[]
    for x in sorted(counter.keys()):
        xs.append(x)
        ys.append(counter[x])
    return xs,np.array(ys)/float(sum(ys))

def plot_levels(ax,xs_ys_dict,title,xls,yls,is_scale=0,low=0,up=60):
    all_yss = []
    for key in xs_ys_dict.keys():
        xs,ys = xs_ys_dict[key]
        ax.plot(xs,ys)
        # print len(ys)
        all_yss.append((key,ys))

    ax.set_title(title)
    ax.set_xlabel(xls)
    ax.set_xticks(np.arange(1, 11))
    ax.set_xticklabels(np.arange(1, 11))
    # ax.set_ylabel(yls)
    if is_scale==1:
        ax.set_yscale('log')
    if low!=-1:
        ax.set_ylim(low,up)
    # ax.set_xlim(0,50)
    # ax.set_ylim(0,ylims_up)
    return all_yss

#from perspective of citation order
def citation_order(cited_papers_json,xyfunc=co_ti_i,i='all'):
    cited_papers = json.loads(open(cited_papers_json).read())
    xs_ys_dict={}
    
    for k in cited_papers.keys():
        paper_dict = cited_papers[k]
        pid = paper_dict['pid']
        year = paper_dict['year']
        citations = [(cit.split(',')[0],int(cit.split(',')[1])) for cit in paper_dict['citations']]
        xs,ys = xyfunc(citations,year,i)
        xs_ys_dict[pid]=(xs,ys)

    return xs_ys_dict,cited_papers



if __name__ == '__main__':
    plot_ten_ti()