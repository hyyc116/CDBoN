#coding:utf-8
'''
@author: hy@tTt
对于几个重要的属性，depth, direct citations, age, publishing year 等的增加与cascade size的关系

'''
from basic_config import *

'''
mag:data/mag/stats/plot_dict.json
aminer:data/plot_dict.json

'''
def plot_relation_size_attr(dataset):

    if dataset =='MAG':
        data_path = 'data/mag/stats/plot_dict.json'
        x_min = 22
        x_max = 260

    elif dataset == 'AMiner':
        data_path = 'data/plot_dict.json'
        x_min = 10
        x_max = 165
    else:
        logging.info('No Such datasets, please type in MAG or AMiner')
        return

    plot_dict = json.loads(open(data_path).read())

    cxs = plot_dict['cxs']
    eys = plot_dict['eys']
    dys = plot_dict['dys']
    citation_ages = plot_dict['age']
    n_direct_citations = plot_dict['direct'] 
    n_indirect_citations = plot_dict['indirect']
    n_owner_years = plot_dict['year']

    sorted_cxs = sorted(cxs,reverse=True)

    plt.plot(np.arange(len(sorted_cxs))+1,sorted_cxs)
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('pdf/{:}_citation_PLE.pdf'.format(dataset),dpi=200)

    logging.info('length of cascade size {:}, edge size {:}, depth {:}, citation ages {:}, direct citations {:}, owner years {:}, n_indirect_citations {:}'.format(len(cxs),len(eys),len(dys),len(citation_ages),len(n_direct_citations),len(n_owner_years),len(n_indirect_citations)))
    
    depth_size_dict = defaultdict(list)
    direct_cp_size_dict = defaultdict(list)
    year_size_dict = defaultdict(list)
    age_size_dict = defaultdict(list)
    indirect_dict = defaultdict(list)
    year_indirect_dict = defaultdict(list)

    citation_direct_dict = defaultdict(list)
    citation_indirect_dict = defaultdict(list)

    ## citation n
    citation_direct_links = defaultdict(list)
    citation_indirect_links = defaultdict(list)

    ## 对 n_direct_citations 是一个比例列表
    # 使用最大的值进行归一化

    normed_direct_cps = n_direct_citations
    for i,depth in enumerate(dys):
        # cascade 的大小
        cascade_size = cxs[i]

        # ### citation  count数量为10以下的都抛弃，只看中高被引的论文
        # if cascade_size<900:
        #     continue 

        # owner 直接引文, 是一个比例，如何归一化呢
        n_direct_cps = normed_direct_cps[i]
        n_indirect_cps = n_indirect_citations[i]
        ## indirect links的数量
        n_indirect_links = float('{:.1f}'.format((eys[i]-cascade_size)/float(cascade_size)))

        # owner 的发布时间
        owner_year = n_owner_years[i]
        # owner diffusion的时间
        diff_age = citation_ages[i]

        ## citation 与 direct citations, indirect citations 的关系
        citation_direct_dict[cascade_size].append(n_direct_cps)
        citation_indirect_dict[cascade_size].append(n_indirect_cps)

        ### citation count 与 direct links, indirect links 的关系
        citation_direct_links[cascade_size].append(cascade_size/float(eys[i]))
        citation_indirect_links[cascade_size].append((eys[i]-cascade_size)/float(eys[i]))

        # 深度与大小的关系
        depth_size_dict[depth].append(cascade_size)
        direct_cp_size_dict[n_direct_cps].append(cascade_size)
        year_size_dict[owner_year].append(cascade_size)
        age_size_dict[diff_age].append(cascade_size)

        indirect_dict[n_indirect_links].append(cascade_size)

        year_indirect_dict[owner_year].append(n_indirect_links)

    ## 对上述图画 画箱式图
    fig,axes  = plt.subplots(2,1,figsize=(7,10))
    ax1 = axes[0]
    if dataset=='AMiner':
        t1 = 'cascade depth\n(a)'
        t2 = 'normalized indirect CRs\n(c)'
    elif dataset=='MAG':
        t1 = 'cascade depth\n(b)'
        t2 = 'normalized indirect CRs\n(d)'
    attr_size_plots(ax1,fig,x_min,x_max,depth_size_dict,t1,dataset=dataset)
    ax2 = axes[1]

    attr_size_plots(ax2,fig,x_min,x_max,indirect_dict,t2,dataset=dataset)
    plt.tight_layout()
    fig_path = 'pdf/{:}_attr_size_plots.png'.format(dataset.lower())
    plt.savefig(fig_path,dpi=200)
    logging.info('saved to {:}.'.format(fig_path))

    fig,axes = plt.subplots(4,1,figsize=(7,20))
    ax = axes[0]
    ax1 = axes[1]
    ax2 = axes[2]
    ax3 = axes[3]

    if dataset=='AMiner':
        t1 = 'publishing year\n(a)'
    elif dataset=='MAG':
        t1 = 'publishing year\n(b)'

    attr_size_plots(ax,fig,x_min,x_max,year_size_dict,t1,dataset=dataset)
    year_analysis(ax1,ax2,ax3,fig,cxs,eys,n_owner_years,dataset,x_min,x_max)
    fig_path = 'pdf/{:}_size_year_plots.png'.format(dataset.lower())
    plt.tight_layout()
    plt.savefig(fig_path,dpi=200)
    logging.info('saved to {:}.'.format(fig_path))

    citation_links(citation_direct_dict,citation_indirect_dict,dataset,'citations')
    citation_links(citation_direct_links,citation_indirect_links,dataset,'links')



def citation_links(direct_links,indirect_links,dataset,name):

    plt.subplots(figsize=(7,5))
    d_xs = []
    d_ys = []
    for size in sorted(direct_links.keys()):
        mean = np.mean(direct_links[size])
        d_xs.append(size)
        d_ys.append(mean)

    plt.plot(d_xs,d_ys,alpha=0.5,c=color_sequence[0])
    d_zs = [i for i in zip(*lowess(d_ys,np.log(d_xs),frac=0.5,it=1,is_sorted =True))[1]]
    
    xs = []
    ys = []
    for size in sorted(indirect_links.keys()):
        mean = np.mean(indirect_links[size])
        xs.append(size)
        ys.append(mean)

    plt.plot(xs,ys,alpha=0.5,c=color_sequence[2])
    zs = [i for i in zip(*lowess(ys,np.log(xs),frac=0.5,it=1,is_sorted =True))[1]]

    plt.plot(d_xs,d_zs,c=color_sequence[0],label='direct {:}'.format(name))
    plt.plot(xs,zs,c=color_sequence[2],label='indirect {:}'.format(name))

    plt.xlabel('citation count')
    plt.ylabel('percentage')
    plt.title(dataset)
    plt.xscale('log')
    plt.legend()
    plt.tight_layout()
    out_path = 'pdf/{:}_types_curves_{:}.pdf'.format(dataset.lower(),name)
    plt.savefig(out_path,dpi=200)
    logging.info('fig saved to {:}'.format(out_path))

def year_analysis(ax1,ax2,ax3,fig,cxs,eys,n_owner_years,dataset,x_min,x_max):
    ## 首先对于三种类别的文章进行分析
    high_xs =[] 
    high_ys = []

    medium_xs = []
    medium_ys = []

    low_xs = []
    low_ys = []

    for i,cc in enumerate(cxs):
        es = eys[i]
        year = n_owner_years[i]

        if cc>=x_max:
            high_xs.append(year)
            high_ys.append((es-cc)/float(cc))

        if cc>=x_min and cc<x_max:
            medium_xs.append(year)
            medium_ys.append((es-cc)/float(cc))

        if cc<x_min:
            low_xs.append(year)
            low_ys.append((es-cc)/float(cc))

    print 'high:',len(high_xs),', medium:',len(medium_xs),', low:',len(low_xs)
    
    

    plot_heat_scatter(low_xs,low_ys,ax1,fig)
    plot_heat_scatter(medium_xs,medium_ys,ax2,fig)
    plot_heat_scatter(high_xs,high_ys,ax3,fig)

    ## 1<x<23
    print 'low cited papers ...'
    xs = []
    ys = []
    data_dict = defaultdict(list)
    for i,x in enumerate(low_xs):
        y = low_ys[i]
        data_dict[x].append(y) 

    print 'length of data_dict:',len(data_dict.keys())
    for key in sorted(data_dict.keys()):
        mean = np.mean(data_dict[key])
        if not np.isnan(mean):
            xs.append(key)
            ys.append(mean)

    ax1.plot(xs,ys,c='r')
    ax1.set_title('Low cited papers')

    print 'Medium cited papers ...'
    xs = []
    ys = []
    data_dict = defaultdict(list)
    for i,x in enumerate(medium_xs):
        y = medium_ys[i]
        data_dict[x].append(y) 

    print 'length of data_dict:',len(data_dict.keys())
    for key in sorted(data_dict.keys()):
        mean = np.mean(data_dict[key])
        if not np.isnan(mean):
            xs.append(key)
            ys.append(mean)

    ax2.plot(xs,ys,'--',c='r')
    ax2.set_title('Medium cited papers')

    print 'low cited papers ...'
    xs = []
    ys = []
    data_dict = defaultdict(list)
    for i,x in enumerate(high_xs):
        y = high_ys[i]
        data_dict[x].append(y) 

    print 'length of data_dict:',len(data_dict.keys())
    for key in sorted(data_dict.keys()):
        mean = np.mean(data_dict[key])
        if not np.isnan(mean):
            xs.append(key)
            ys.append(mean)

    ax3.plot(xs,ys,'--',c='r')
    ax3.set_title('Highly cited papers')

    if dataset=='AMiner':
        t1 = 'publishing year\n(a)'
        t2 = 'publishing year\n(c)'
        t3 = 'publishing year\n(e)'
    elif dataset=='MAG':
        t1 = 'publishing year\n(b)'
        t2 = 'publishing year\n(d)'
        t3 = 'publishing year\n(e)'

    ax1.set_xlabel(t1)
    ax1.set_ylabel('indirect links')

    ax2.set_xlabel(t2)
    ax2.set_ylabel('indirect links')

    ax3.set_xlabel(t3)
    ax3.set_ylabel('indirect links')


def attr_size_plots(ax,fig,x_min,x_max,data_dict,xlabel,ylabel='cascade size',yscale='log',dataset='AMiner'):
    logging.info('Plotting {:} ...'.format(xlabel))
    logging.info('Sizes of X-axis:{:}'.format(len(data_dict.keys())))

    ## 1<x<23
    xs = []
    ys = []
    for key in sorted(data_dict.keys()):
        for y in data_dict[key]:
            xs.append(key)
            ys.append(y)

    plot_heat_scatter(xs,ys,ax,fig)


    ## 画两条线
    if ylabel=='cascade size':
        ax.plot(np.linspace(np.min(xs),np.max(xs),10),[x_min]*10,'--',c='r')
        ax.plot(np.linspace(np.min(xs),np.max(xs),10),[x_max]*10,'--',c='r')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_yscale(yscale)
    ax.set_title(dataset)
    ax.legend()

    ## 1<x<23
    xs = []
    ys = []
    for key in sorted(data_dict.keys()):
        mean = np.mean([i for i in data_dict[key] if i<x_min ])
        if mean > 0:
            xs.append(key)
            ys.append(mean)

    ax.plot(xs,ys,label='Low cited papers')

    # 23 < x <988
    xs = []
    ys = []
    for key in sorted(data_dict.keys()):
        mean = np.mean([i for i in data_dict[key] if i>=x_min and i < x_max ])
        if mean > 0:
            xs.append(key)
            ys.append(mean)

    ax.plot(xs,ys,label='Medium cited papers')

    # x> 988
    xs = []
    ys = []
    for key in sorted(data_dict.keys()):
        mean = np.mean([i for i in data_dict[key] if i>=x_max ])
        if mean > 0:
            xs.append(key)
            ys.append(mean)

    ax.plot(xs,ys,label='Highly cited papers')

if __name__ == '__main__':
    plot_relation_size_attr(sys.argv[1])



