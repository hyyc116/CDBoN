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
    elif dataset == 'AMiner':
        data_path = 'data/plot_dict.json'
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

    ## 对 n_direct_citations 是一个比例列表
    # 使用最大的值进行归一化

    normed_direct_cps = np.log(np.array(n_direct_citations)/np.max(n_direct_citations))
    print normed_direct_cps
    normed_direct_cps = [10**float('{:.1f}'.format(float(i))) for i in normed_direct_cps]
    direct_citation_size_dict = defaultdict(list)
    for i,depth in enumerate(dys):
        # cascade 的大小
        cascade_size = cxs[i]

        ### citation  count数量为10以下的都抛弃，只看中高被引的论文
        if cascade_size<10:
            continue 

        # owner 直接引文, 是一个比例，如何归一化呢
        n_direct_cps = normed_direct_cps[i]
        # owner 的发布时间
        owner_year = n_owner_years[i]
        # owner diffusion的时间
        diff_age = citation_ages[i]

        # 深度与大小的关系
        depth_size_dict[depth].append(cascade_size)
        direct_cp_size_dict[n_direct_cps].append(cascade_size)
        year_size_dict[owner_year].append(cascade_size)
        age_size_dict[diff_age].append(cascade_size)

    ## 对上述图画 画箱式图
    fig,axes  = plt.subplots(4,1,figsize=(7,20))
    ax1 = axes[0]
    attr_box_plot(ax1,depth_size_dict,'cascade depth')
    ax2 = axes[1]
    attr_box_plot(ax2,direct_cp_size_dict,'$k/k_{max}$',True)
    ax3 = axes[2]
    attr_box_plot(ax3,year_size_dict,'publishing year')
    ax4 = axes[3]
    attr_box_plot(ax4,age_size_dict,'Citation Age')
    plt.tight_layout()
    fig_path = 'pdf/{:}_attr_box_plot.png'.format(dataset.lower())
    plt.savefig(fig_path,dpi=200)
    logging.info('saved to {:}.'.format(fig_path))

def attr_box_plot(ax,data_dict,xlabel,scale=False):
    logging.info('Plotting {:} ...'.format(xlabel))
    logging.info('Sizes of X-axis:{:}'.format(len(data_dict.keys())))
    data = []
    xs = []
    ys = []
    for key in sorted(data_dict.keys()):
        xs.append(key)
        ys.append(np.mean(data_dict[key]))

    ax.plot(xs,ys)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Cascade size')
    if scale:
        ax.set_xscale('log')



if __name__ == '__main__':
    plot_relation_size_attr(sys.argv[1])



