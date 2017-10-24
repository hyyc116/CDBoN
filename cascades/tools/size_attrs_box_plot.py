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
        x_min = 37
        x_max = 390

    elif dataset == 'AMiner':
        data_path = 'data/plot_dict.json'
        x_min = 23
        x_max = 270
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
    plt.savefig('pdf/citation_PLE.pdf',dpi=200)

    logging.info('length of cascade size {:}, edge size {:}, depth {:}, citation ages {:}, direct citations {:}, owner years {:}, n_indirect_citations {:}'.format(len(cxs),len(eys),len(dys),len(citation_ages),len(n_direct_citations),len(n_owner_years),len(n_indirect_citations)))
    
    depth_size_dict = defaultdict(list)
    direct_cp_size_dict = defaultdict(list)
    year_size_dict = defaultdict(list)
    age_size_dict = defaultdict(list)
    indirect_dict = defaultdict(list)
    year_indirect_dict = defaultdict(list)


    citation_direct_dict = defaultdict(list)
    citation_indirect_dict = defaultdict(list)

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

        ## citation 与 direct links, indirect links的关系
        citation_direct_dict[cascade_size].append(n_direct_cps)
        citation_indirect_dict[cascade_size].append(n_indirect_cps)


        # 深度与大小的关系
        depth_size_dict[depth].append(cascade_size)
        direct_cp_size_dict[n_direct_cps].append(cascade_size)
        year_size_dict[owner_year].append(cascade_size)
        age_size_dict[diff_age].append(cascade_size)

        indirect_dict[n_indirect_links].append(cascade_size)

        year_indirect_dict[owner_year].append(n_indirect_links)

    ## 对上述图画 画箱式图
    fig,axes  = plt.subplots(3,1,figsize=(7,15))
    ax1 = axes[0]
    attr_size_plots(ax1,fig,x_min,x_max,depth_size_dict,'cascade depth')
    ax2 = axes[1]
    attr_size_plots(ax2,fig,x_min,x_max,indirect_dict,'indirect links')
    ax3 = axes[2]
    attr_size_plots(ax3,fig,x_min,x_max,year_size_dict,'publishing year')
    # ax4 = axes[3]
    # attr_size_plots(ax4,fig,x_min,x_max,year_indirect_dict,'publishing year','indirect links',True,'linear')
    plt.tight_layout()
    fig_path = 'pdf/{:}_attr_size_plots.png'.format(dataset.lower())
    plt.savefig(fig_path,dpi=200)
    logging.info('saved to {:}.'.format(fig_path))

    year_analysis(cxs,eys,n_owner_years,dataset,x_min,x_max)

    citation_links(citation_direct_dict,citation_indirect_dict,dataset)


def citation_links(direct_links,indirect_links,dataset):

    plt.subplots(figsize=(6,5))
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

    plt.plot(d_xs,d_zs,c=color_sequence[0],label='direct citation')
    plt.plot(xs,zs,c=color_sequence[2],label='indirect citation')



    plt.xlabel('citation count')
    plt.ylabel('percentage')
    plt.title('citation changes over count')
    plt.xscale('log')
    plt.legend()
    plt.tight_layout()
    out_path = 'pdf/{:}_types_curves.pdf'.format(dataset.lower())
    plt.savefig(out_path,dpi=200)
    logging.info('fig saved to {:}'.format(out_path))




def year_analysis(cxs,eys,n_owner_years,dataset,x_min,x_max):
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
    
    fig,ax = plt.subplots(figsize=(6,5))
    ax.scatter(low_xs,low_ys, s=3, label='Low cited papers',alpha=0.7)
    ax.scatter(medium_xs,medium_ys, s=3, label='Medium cited papers',alpha=0.7)
    ax.scatter(high_xs,high_ys, s=3,label='Highly cited papers',alpha=0.7)

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

    ax.plot(xs,ys,c='r',label='Low cited papers')

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

    ax.plot(xs,ys,'--',c='r',label='Medium cited papers')

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

    ax.plot(xs,ys,label='High cited papers')

    plt.xlabel('publishing year')
    plt.ylabel('indirect links')
    ax.legend()
    plt.tight_layout()
    out_path = 'pdf/{:}_year_indirect.png'.format(dataset.lower())
    plt.savefig(out_path,dpi=300)
    logging.info('file saved to {:}'.format(out_path))



def attr_size_plots(ax,fig,x_min,x_max,data_dict,xlabel,ylabel='cascade size',yscale='log'):
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

    print xs
    print ys
    ax.plot(xs,ys,label='Highly cited papers')

if __name__ == '__main__':
    plot_relation_size_attr(sys.argv[1])



