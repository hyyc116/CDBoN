from para_config import *
from Citation_friction import *
from scipy import stats
import matplotlib.pylab as pylab
import math


def plot_0_1(label=1,isall=True):
    if not isall:
        low_json = 'data/low_selected_papers.json'
        medium_json = 'data/medium_selected_papers.json'
        high_json = 'data/high_selected_papers.json'
    else:
        low_json = 'data/all_low_cited_papers.json'
        medium_json = 'data/all_medium_cited_papers.json'
        high_json = 'data/all_high_cited_papers.json'

    xyfunc= co_ti_i
    i=10
    is_scale=0
    low=0.8
    up=60
    yls = 'Length of Total Time'
    xls = '$i^{th}$ citation'

    # print xyfunc_name,'with i=',i,'low',low,'up',up

    params = {'legend.fontsize': 15,
         'axes.labelsize': 15,
         'axes.titlesize':20,
         'xtick.labelsize':15,
         'ytick.labelsize':15,
         'font.family':'Times New Roman'}
    pylab.rcParams.update(params)

    # fig,((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9)) = plt.subplots(3,3,sharex='row',sharey='row',figsize=(15,15))
    fig,((ax1,ax2,ax3)) = plt.subplots(1,3,figsize=(15,5))
    
    
    print 'low cited papers'
    barx=['Low','Medium','High']
    bary = []
    low_xy_dict,low_papers = citation_order(low_json,xyfunc,i)
    title = 'Low cited papers'
    all_yss = get_all_yss(low_xy_dict)
    (_1xs,_1ys),(_5xs,_5ys),(_10xs,_10ys) = three_points(all_yss)
    
    if label==1:
        ax1.plot(_1xs,_1ys,'-o',label='Low')
        acc_xs,acc_ys = acc_xy(_1xs,_1ys)
    if label==5:
        ax1.plot(_5xs,_5ys,'-o',label='Low')
        acc_xs,acc_ys = acc_xy(_5xs,_5ys)

    if label==10:
        ax1.plot(_10xs,_10ys,'-o',label='Low')
        acc_xs,acc_ys = acc_xy(_10xs,_10ys)

    ax2.plot(acc_xs,acc_ys,'-o',label='Low')
    ax2.plot(acc_xs,[0.8]*len(acc_xs),'--',c='r')

    index,per = get_percentage(acc_ys)
    bary.append(acc_xs[index]*per)

    print 'Medium cited papers'
    medium_xy_dict,medium_papers = citation_order(medium_json,xyfunc,i)
    all_yss = get_all_yss(medium_xy_dict)
    (_1xs,_1ys),(_5xs,_5ys),(_10xs,_10ys) = three_points(all_yss)
    if label==1:
        ax1.plot(_1xs,_1ys,'-^',label='Medium',c='#ff7f0e')
        acc_xs,acc_ys = acc_xy(_1xs,_1ys)

    if label==5:
        ax1.plot(_5xs,_5ys,'-^',label='Medium',c='#ff7f0e')
        acc_xs,acc_ys = acc_xy(_5xs,_5ys)

    if label==10:
        ax1.plot(_10xs,_10ys,'-^',label='Medium',c='#ff7f0e')
        acc_xs,acc_ys = acc_xy(_10xs,_10ys)

    ax2.plot(acc_xs,acc_ys,'-^',label='Medium',c='#ff7f0e')
    index,per = get_percentage(acc_ys)
    bary.append(acc_xs[index]*per)

    print 'high cited papers'
    high_xy_dict,high_papers = citation_order(high_json,xyfunc,i)
    title = 'High cited papers'
    all_yss = get_all_yss(high_xy_dict)
    (_1xs,_1ys),(_5xs,_5ys),(_10xs,_10ys) = three_points(all_yss)

    if label==1:
        acc_xs,acc_ys = acc_xy(_1xs,_1ys)
        ax1.plot(_1xs,_1ys,'-*',label='High',c='g')

    if label==5:
        ax1.plot(_5xs,_5ys,'-*',label='High',c='g')
        acc_xs,acc_ys = acc_xy(_5xs,_5ys)

    if label ==10:
        acc_xs,acc_ys = acc_xy(_10xs,_10ys)
        ax1.plot(_10xs,_10ys,'-*',label='High',c='g')

    ax2.plot(acc_xs,acc_ys,'-*',label='High',c='g')
    index,per = get_percentage(acc_ys)
    bary.append(acc_xs[index]*per)

    rects = ax3.bar(np.arange(3),bary,align='center',width=0.3)
    ax3.set_xticks(np.arange(3))
    ax3.set_xticklabels(barx)
    autolabel(rects,ax3)

    ax1.legend()
    ax2.legend()
    if label==1:
        ax1.set_title('PD of 1st Citation')
        ax2.set_title('CD of 1st Citation')
        ax3.set_title('80% papers received 1st citation')
    else:
        ax1.set_title('PD of {:} Citations'.format(label))
        ax2.set_title('CD of {:} Citations'.format(label))
        ax3.set_title('80% papers received {:} citations'.format(label))
    # ax2.set_xscale('log')
    
    # ax5.set_title('$5^{th}$ Citation Distribution')
    # ax6.set_title('$10^{th}$ Citation Distribution')
    # ax1.set_xscale('log')
    # ax5.set_xscale('log')
    # ax6.set_xscale('log')
    if label==1:
        ax1.set_xlabel('Response Time (year)\n(a)')
        ax2.set_xlabel('Response Time (year)\n(b)')
        ax3.set_xlabel('Cited Levels\n(c)')

    elif label==5:
        ax1.set_xlabel('Time (year)\n(a)')
        ax2.set_xlabel('Time (year)\n(b)')
        ax3.set_xlabel('Cited Levels\n(c)')
    else:
        ax1.set_xlabel('Time (year)\n(d)')
        ax2.set_xlabel('Time (year)\n(e)')
        ax3.set_xlabel('Cited Levels\n(f)')
    # ax5.set_xlabel('years\n(e)')
    # ax6.set_xlabel('years\n(f)')
    ax1.set_ylabel('Probability')
    ax2.set_ylabel('Probability')

    ax3.set_ylabel('Years')
    ax3.set_ylim(0,20)
    # ax1.set_ylabel('Total Time required')
    # ax7.set_ylabel('years')
    # ax7.set_xlabel('Publication Year\n(g)')
    # ax8.set_xlabel('Publication Year\n(h)')
    # ax9.set_xlabel('Publication Year\n(i)')
    # ax7.set_yscale('log')
    # ax8.set_yscale('log')
    # ax9.set_yscale('log')
    # ax1.set_xlim(0,)
    # ax4.legend()
    # ax5.legend()
    # ax6.legend()
    # ax7.legend()
    # ax8.legend()
    # ax9.legend()
    # fig.subplots_adjust(wspace=0)

    # yticklabels = ax2.get_yticklabels() + ax3.get_yticklabels()
    # plt.setp(yticklabels, visible=False)
    plt.tight_layout()
    if not isall:
        namepath = 'pdf/f_0_{:}.pdf'.format(label)
    else:
        namepath = 'pdf/all_f_0_{:}.pdf'.format(label)
    plt.savefig(namepath,dpi=300)
    print 'Result saved to',namepath
 
def get_percentage(acc_ys):
    for i,y in enumerate(acc_ys):
        if y>0.8:
            return i,0.8/y

def acc_xy(xs,ys):
    print xs,ys
    acc_xs=[]
    acc_ys=[]
    total_ys=0

    for i,x in enumerate(xs):
        acc_xs.append(x)
        total_ys+=ys[i]
        acc_ys.append(total_ys)
    print acc_xs,acc_ys
    return acc_xs,acc_ys

def get_all_yss(xs_ys_dict):
    all_yss = []
    for key in xs_ys_dict.keys():
        xs,ys = xs_ys_dict[key]
        all_yss.append((key,ys))

    return all_yss


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

    # fig,((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9)) = plt.subplots(3,3,sharex='row',sharey='row',figsize=(15,15))
    fig,((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(3,3,sharex='row',sharey='row',figsize=(15,10))
    
    
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

def co_ti_i(citations,year,i='all'):
    if i=='all':
        i=len(citations)
    else:
        i=int(i)

    ti_list = []
    for cpid, cyear in sorted(citations,key=lambda x:x[1])[:i]:
        ti_list.append(cyear-year)
    
    xs = []
    ys = []

    for i, ti in enumerate(ti_list):
        order = i+1
        xs.append(order)
        ys.append(ti)

    return xs,ys

def plot_divergence():
    high_line = [0.854,1.816,2.660]
    medium_line = [0.932,2.902,4.723]
    low_line = [2.844,8.845,15.920]
    high_div = div(high_line)
    medium_div = div(medium_line)
    low_div = div(low_line)

    fig,ax = plt.subplots(figsize=(5,5))
    # ax.plot([1,5,10],high_div,label='High')
    ax.plot([1,5,10],low_div-high_div,label='Low')
    ax.plot([1,5,10],medium_div-high_div,label='Medium')
    
    ax.legend()
    ax.set_title('Divergence')
    plt.tight_layout()
    plt.savefig('pdf/divergence.pdf',dpi=300)



def div(lines):
    return np.array([lines[0],lines[1]-lines[0],lines[2]-lines[0]])

if __name__ == '__main__':
    # plot_ten_ti()
    plot_0_1()
    plot_0_1(label=5)
    plot_0_1(label=10)
    # plot_divergence()