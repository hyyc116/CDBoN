#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *

def plot_series_of_graph(citation_network,citation_cascasde):

    ## plot paper node with in graph by the year of paper
    # 首先加载出来 load two networks
    cn = json.loads(open(citation_network).read())
    cc = json.loads(open(citation_cascasde).read())
    logging.info('citation network loaded with {:} papers, and citation cascade loaded with {:} papers.'.format(len(cn.keys()),len(cc.keys())))

    ## 随机选择一篇引文数量为200的文章
    chosen_pid = -1
    for pid in cc.keys():
        # 判断这个文章的引文数量以及边的数量
        node_count = cc[pid]['cnum']
        edge_count = cc[pid]['enum']

        if node_count==50 and float(edge_count)/node_count>4:
            chosen_pid = pid

            break

    if chosen_pid!=-1:
        logging.info('selected paper id : {:}, with {:} nodes and {:} edges.'.format(chosen_pid,cc[chosen_pid]['cnum'],cc[chosen_pid]['enum']))
    else:
        logging.info('no paper under constraint.')
        return -1

    ## 选择完毕之后

    ''' 根据citation network中 这篇文章的citation的年份 在坐标轴中画圆 '''
    fig,ax = plt.subplots(figsize=(15,3))
    ax.set_xlabel('index of citation')
    ax.set_ylabel('depth of node')

    ax.spines['top'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.spines['left'].set_visible(False)

    #定义两种颜色
    connector_color = color_sequence[8]
    supporter_color = color_sequence[2]

    ## 这篇文章的citation 列表
    citations = cn[chosen_pid]['citations']
    ## 获得这篇文章的cascade图
    edges = cc[chosen_pid]['edges']
    diG = nx.DiGraph()
    diG.add_edges_from(edges)
    
    diG.in_degree()

    m_h = 0
    # citations是一个字典，每一个引证文献的id对应其publication_year
    # 按照发表时间排序
    for i,(pid,year) in enumerate(sorted(citations.items(),key=lambda x:x[1])):
        # index of citation
        x = i+1
        # depth of ciattion
        y= max_depth(diG,pid,chosen_pid)
        if y>m_h:
            m_h=y
        # 这篇文章的被引数量
        nc = number_of_citation(cc,pid)+1
        outer_radius = nc*5
        # 这篇文章在citation cascade中的入度
        od = diG.out_degree(pid)
        ind = diG.in_degree(pid)
        inner_radius = ind/float(nc)*outer_radius
        # 这篇文章的出度
        line_width = od

        ax.scatter(x,y,s=outer_radius,c=supporter_color,alpha=0.8)
        if ind>0:
            ax.scatter(x,y,s=inner_radius,c=connector_color)

    outname = 'pdf/series_{:}_dis.pdf'.format(chosen_pid)
    ax.set_ylim(-5,m_h+5)
    ax.set_yticks([],[])
    # plt.axis('off')

    plt.tight_layout()
    plt.savefig(outname,dpi=200)
    logging.info('pdf saved to {:}'.format(outname))

def max_depth(G,source,target):
    max_d = 0
    for path in nx.all_simple_paths(G, source=source, target=target):
        if len(path)>max_d:
            max_d = len(path)

    return max_d

def number_of_citation(cc,pid):
    pid_dict = cc.get(pid,'-1')
    if pid_dict=='-1':
        return 0
    else:
        return cc[pid]['cnum']


if __name__ == '__main__':
    plot_series_of_graph(sys.argv[1],sys.argv[2])








    