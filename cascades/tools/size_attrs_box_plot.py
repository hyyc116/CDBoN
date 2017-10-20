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

        # ### citation  count数量为10以下的都抛弃，只看中高被引的论文
        # if cascade_size<900:
        #     continue 

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
    attr_box_plot(ax2,direct_cp_size_dict,'$k$',True)
    ax3 = axes[2]
    attr_box_plot(ax3,year_size_dict,'publishing year')
    ax4 = axes[3]
    attr_box_plot(ax4,age_size_dict,'Citation Age')
    plt.tight_layout()
    fig_path = 'pdf/{:}_attr_box_plot.png'.format(dataset.lower())
    plt.savefig(fig_path,dpi=200)
    logging.info('saved to {:}.'.format(fig_path))

    surface_plot(depth_size_dict,'depth')



def surface_plot(data_dict,xlabel,scale=False):
    logging.info('Plotting {:} ...'.format(xlabel))
    logging.info('Sizes of X-axis:{:}'.format(len(data_dict.keys())))
    rxs = []
    rys = []
    rzs = []
    ## 首先获得所有的attr的值
    unique_attrs = data_dict.keys()
    unique_counts = []
    attr_count_num = defaultdict(dict)
    for attr in sorted(data_dict.keys()):
        count_list = data_dict[attr]
        count_dict = Counter(count_list)
        unique_counts.extend(count_list)
        for count in count_dict.keys():
            attr_count_num[attr][count]=count_dict[count]


    unique_counts = list(set(unique_counts))
    # print sorted(unique_counts)

    ROWS = len(unique_attrs)
    COLS = len(unique_counts)

    for attr in sorted(unique_attrs):
        for count in sorted(unique_counts):
            num = attr_count_num[attr].get(count,0)+10
            if num < 0:
                print '..'
            rxs.append(attr)
            rys.append(count)
            rzs.append(num)

    print rxs[:100]
    print rys[:100]
    print rzs[:100]

    X = np.reshape(rxs,(ROWS,COLS))
    Y = np.reshape(rys,(ROWS,COLS))
    Z = np.reshape(rzs,(ROWS,COLS))

    fig=plt.figure(figsize=(14,10))
    ax = Axes3D(fig)
    ax.view_init(60, 240)
    ax.set_title(xlabel)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('cascade_size')
    ax.set_zlabel('#papers')
    # if scale:
        # ax.set_xscale('log')
    ax.set_xscale('log')
    ax.set_zscale('log')


    surf = ax.plot_surface(Y,X,Z, rstride=1, cstride=1, cmap=CM.coolwarm)
    fig.colorbar(surf, shrink=0.5, aspect=10)
    plt.savefig('pdf/{:}.pdf'.format(xlabel),dpi=100)


def attr_box_plot(ax,data_dict,xlabel,scale=False):
    logging.info('Plotting {:} ...'.format(xlabel))
    logging.info('Sizes of X-axis:{:}'.format(len(data_dict.keys())))
    data = []

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


    ax.set_xlabel(xlabel)
    ax.set_ylabel('Cascade size')
    if scale:
        ax.set_xscale('log')

    ax.set_yscale('log')

    ax.legend()



if __name__ == '__main__':
    plot_relation_size_attr(sys.argv[1])



