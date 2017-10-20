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

    plot_dict = json.loads(open(data_path).read())

    cxs = plot_dict['cxs']
    eys = plot_dict['eys']
    dys = plot_dict['dys']
    citation_ages = plot_dict['age']
    n_direct_citations = plot_dict['direct'] 
    n_indirect_citations = plot_dict['indirect']
    n_owner_years = plot_dict['year']

    logging.info('length of cascade size {:}, edge size {:}, depth {:}, citation ages {:}, direct citations {:}, owner years {:}, n_indirect_citations {:}'.format(len(csx),len(eys),len(dys),len(citation_ages),len(n_direct_citations),len(n_owner_years),len(n_indirect_citations)))

    
    depth_size_dict = defaultdict(list)
    direct_cp_size_dict = defaultdict(list)
    year_size_dict = defaultdict(list)
    age_size_dict = defaultdict(list)

    ## 对 n_direct_citations 是一个比例列表
    # 使用最大的值进行归一化
    normed_direct_cps = np.array(n_direct_citations)/np.max(n_direct_citations)

    direct_citation_size_dict = defaultdict(list)
    for i,depth in enumerate(dys):
        # cascade 的大小
        cascade_size = cxs[i]
        # owner 直接引文, 是一个比例，如何归一化呢
        n_direct_cps = normed_direct_cps[i]
        # owner 的发布时间
        owner_year = n_owner_years[i]
        # owner diffusion的时间
        diff_age = citation_ages[i]


        # 深度与大小的关系
        depth_size_dict[depth].append(cascade_size)
        direct_cp_size_dict[n_direct_citations].append(cascade_size)
        year_size_dict[owner_year].append(cascade_size)
        age_size_dict[owner_year].append(diff_age)


    ## 对上述图画 画箱式图
    fig,axes  = plt.subplots(4,1,figsize=(7,20))
    ax1 = axes[0]
    attr_box_plot(ax1,depth_size_dict,'Depth')
    ax2 = axes[1]
    attr_box_plot(ax2,direct_cp_size_dict,'Direct Citation')
    ax3 = axes[2]
    attr_box_plot(ax3,year_size_dict,'publishing year')
    ax4 = axes[3]
    attr_box_plot(ax4,age_size_dict,'Citation Age')
    plt.tight_layout()
    plt.savefig('pdf/{:}_attr_box_plot.pdf'.format(dataset),dpi=200)

def attr_box_plot(ax,data_dict,title):
    data = []
    for key in sorted(data_dict.keys()):
        data.append(data_dict[key])

    ax.box_plot(data)
    ax.set_title(title)

if __name__ == '__main__':
    plot_relation_size_attr(sys.argv[1])



