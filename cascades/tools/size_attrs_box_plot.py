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
        x_min = 47
        x_max = 2086

    elif dataset == 'AMiner':
        data_path = 'data/plot_dict.json'
        x_min = 23
        x_max = 988
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
        ## indirect links的数量
        n_indirect_links = float('{:.1f}'.format((eys[i]-cascade_size)/float(cascade_size)))

        # owner 的发布时间
        owner_year = n_owner_years[i]
        # owner diffusion的时间
        diff_age = citation_ages[i]

        # 深度与大小的关系
        depth_size_dict[depth].append(cascade_size)
        direct_cp_size_dict[n_direct_cps].append(cascade_size)
        year_size_dict[owner_year].append(cascade_size)
        age_size_dict[diff_age].append(cascade_size)

        indirect_dict[n_indirect_links].append(cascade_size)

    ## 对上述图画 画箱式图
    fig,axes  = plt.subplots(3,1,figsize=(7,15))
    ax1 = axes[0]
    attr_size_plots(ax1,fig,x_min,x_max,depth_size_dict,'cascade depth')
    ax2 = axes[1]
    attr_size_plots(ax2,fig,x_min,x_max,indirect_dict,'indirect links',True)
    ax3 = axes[2]
    attr_size_plots(ax3,fig,x_min,x_max,year_size_dict,'publishing year')
    # ax4 = axes[3]
    # attr_size_plots(ax4,fig,x_min,x_max,age_size_dict,'Citation Age')
    plt.tight_layout()
    fig_path = 'pdf/{:}_attr_size_plots.png'.format(dataset.lower())
    plt.savefig(fig_path,dpi=200)
    logging.info('saved to {:}.'.format(fig_path))

    # surface_plot(depth_size_dict,'depth')

def attr_size_plots(ax,fig,x_min,x_max,data_dict,xlabel,scale=False):
    logging.info('Plotting {:} ...'.format(xlabel))
    logging.info('Sizes of X-axis:{:}'.format(len(data_dict.keys())))

    data = []

    ## 1<x<23
    xs = []
    ys = []
    for key in sorted(data_dict.keys()):
        for y in data_dict[key]:
            xs.append(key)
            ys.append(y)

    plot_heat_scatter(xs,ys,ax,fig)


    ## 画两条线
    ax.plot(np.linspace(np.min(xs),np.max(xs),10),[x_min]*10,'--',c='r')
    ax.plot(np.linspace(np.min(xs),np.max(xs),10),[x_max]*10,'--',c='r')

    data = []
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Cascade size')
    # if scale:
        # ax.set_xscale('log')

    ax.set_yscale('log')

    ax.legend()

    if scale:
        return

    ## 1<x<23
    xs = []
    ys = []
    for key in sorted(data_dict.keys()):
        xs.append(key)
        ys.append(np.mean([i for i in data_dict[key] if i<23 ]))

    ax.plot(xs,ys,label='Low cited papers')

    # 23 < x <988
    xs = []
    ys = []
    for key in sorted(data_dict.keys()):
        xs.append(key)
        ys.append(np.mean([i for i in data_dict[key] if i>=23 and i <988 ]))
        

    ax.plot(xs,ys,label='Medium cited papers')

    # x> 988
    xs = []
    ys = []
    for key in sorted(data_dict.keys()):
        mean = np.mean([i for i in data_dict[key] if i>=988 ])
        if mean > 0:
            xs.append(key)
            ys.append(mean)

    print xs
    print ys
    ax.plot(xs,ys,label='High cited papers')


   


if __name__ == '__main__':
    plot_relation_size_attr(sys.argv[1])



