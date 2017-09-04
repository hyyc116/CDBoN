#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *

def iso(subgraph_dict,graph):
    size = len(graph.edges())
    subgraphs  = subgraph_dict.get(size,{}).keys()
    logging.info('length of graph: {:}, of existing subgraphs number:{:}'.format(size,len(subgraphs)))
    # print 'length of graph',size,'existing subgraphs',len(subgraphs)
    is_iso = False
    if len(subgraphs)==0:
        is_iso = False
    else:
        for subgraph in subgraphs:
            # print '---'
            # print 'exists:',subgraph.edges()
            # print 'new:',graph.edges()
            # print 'result:',nx.is_isomorphic(graph,subgraph)
            if nx.is_isomorphic(graph,subgraph):
                is_iso=True
                subgraph_dict[size][subgraph] = subgraph_dict[size][subgraph]+1
                break

    if not is_iso:
        subgraph_dict[size][graph]=  1
    
    return subgraph_dict

## 将与根节点的链接的边去掉,相当于大出度小于2的点都去掉了
def unlinked_subgraph(citation_cascade):
    cc = json.loads(open(citation_cascade).read())
    logging.info('data loaded...')
    # 统计有多少图去掉与根节点直接相连的边只有还有图
    # 剩余边的比例 与前面统计的图 出度大于1的点的比例 是相同的
    remaining_statistics = defaultdict(list)

    # 剩余的边构成的图中，有多少不相互连通的子图
    remaining_subgraphs_dis = defaultdict(list)

    progress_index = 0
    total = len(cc.keys())

    ### 存储subgraph的字典
    subgraph_dict = defaultdict(dict)

    for pid in cc.keys():
        progress_index+=1

        if progress_index%1==0:
            logging.info('progress report:{:}/{:}'.format(progress_index,total))
        yes_count = 0

        edges = cc[pid]['edges']
        size_of_cascade = float(len(edges))
        citation_count = int(cc[pid]['cnum'])

        remaining_edges=[]
        for edge in edges:
            source = edge[0]
            target = edge[1]
            
            if int(target)==int(pid):
                yes_count+=1
            else:
                remaining_edges.append(edge)
        
        # 
        remaining_edges_size = len(remaining_edges)
        remaining_statistics[citation_count].append(remaining_edges_size/size_of_cascade)

        #如果剩余边的数量是0，无子图，原图形状为扇形
        if remaining_edges_size==0:
            continue

        # 根据剩余边创建图
        dig  = nx.DiGraph()
        dig.add_edges_from(remaining_edges)
        #根据创建的有向图，获得其所有弱连接的子图
        subgraphs =[] 
        for subgraph in nx.weakly_connected_component_subgraphs(dig):
            # 获得图像子图的边的数量
            edge_size = len(subgraph.edges())
            subgraphs.append(edge_size)

            # 如果边的数量小于于50，画出来
            # 判断是否同质
            if edge_size<20:
                subgraph_dict = iso(subgraph_dict,subgraph)

        remaining_subgraphs_dis[citation_count].append(subgraphs)

    # write output
    open('data/remaining_statistics.json','w').write(json.dumps(remaining_statistics))
    open('data/remaining_subgraphs_dis.json','w').write(json.dumps(remaining_subgraphs_dis))

    # 将已经同质化过的图形，画出来
    save_subgraphs = {}
    for size in sorted(subgraph_dict.keys()):
        subgraphs = subgraph_dict[size].keys()
        for i,graph in enumerate(subgraphs):
            count  = subgraph_dict[size][graph]
            ## 对于某一个size对应的子图，画出来
            # plt.figure()
            # nx.draw(graph)
            # plt.text('{:}'.format(count))
            name = 'subgraph/{:}_{:}_{:}.png'.format(size,i,count)
            # plt.savefig(name,dpi=200)
            save_subgraphs[name] = [e for e in graph.edges()]

    open('data/subgraphs_mapping.json','w').write(json.dumps(save_subgraphs))


## unconnected subgraphs plot 
def plot_unconnected_subgraphs():
    remaining_statistics = json.loads(open('data/remaining_statistics.json').read()) 
    remaining_subgraphs_dis = json.loads(open('data/remaining_subgraphs_dis.json').read()) 

    # 在有剩余图的里面，找到的联通子图的分布
    total_dis = 0
    remain_edges_size = defaultdict(int)

    citation_counts_dict = defaultdict(list)
    lastk = 0

    seven_subcas_dis = defaultdict(list)

    for k in sorted([int(k) for k in remaining_subgraphs_dis.keys()]):
        k_count = len(remaining_subgraphs_dis[str(k)])
        for subgraphs in remaining_subgraphs_dis[str(k)]:
            ##  如果这个k对应的文章数量小于10，遇上一个k合并
            if k_count<5:
                k = lastk
            else:
                lastk = k
            
            citation_counts_dict[lastk].extend(subgraphs)
            
            seven_subcas_dis[lastk].append(subgraphs)

            for size in subgraphs:
                remain_edges_size[size]+=1
                total_dis+=1
    fig,axes = plt.subplots(1,3,figsize=(15,5))
    xs=[]
    ys=[]
    _80_dis = 0
    line_x = 0
    max_y = 0
    _20_percent = 0
    for size in sorted(remain_edges_size.keys()):
        xs.append(size)
        dis = remain_edges_size[size]
        if dis>max_y:
            max_y=dis
        ys.append(dis)

        if (_80_dis+dis)/float(total_dis)>0.9 and _80_dis/float(total_dis)<0.9:
            line_x = size

        _80_dis += dis

        if size ==20:
            _20_percent = _80_dis/float(total_dis)


    ax2 = axes[0]
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('$x=$ sub-cascade size\n(a)')
    ax2.set_ylabel('$N(x)$')
    ax2.set_title('size distribution')
    ax2.scatter(xs,ys)
    ax2.plot([line_x]*10,np.linspace(10,max_y,10),'--',label='P(X<x)= 80%, x={:}'.format(line_x))
    ax2.plot([20]*10,np.linspace(10,max_y,10),'-',label='P(x<20)={:.4f}'.format(_20_percent))
    ax2.legend()

    # 不同的cascade size 在不同的citation count中的比例
    ax1 = axes[1]
    for i in range(7):
        n = i+1
        plot_size_n(ax1,seven_subcas_dis,n)

    ax1.set_title('size N distribution')
    ax1.set_xlabel('citation count\n(b)')
    ax1.set_ylabel('Percentage of size N')
    ax1.set_xscale('log')
    ax1.legend(loc=2)
    ax1.set_yscale('log')

    ax3 = axes[2]
    plot_subgraph_pattern(ax3)
    ax3.set_title('pattern distribution')
    ax3.set_xlabel('Ranked patterns\n(c)')
    ax3.set_ylabel('Number of patterns')
    ax3.legend()
    plt.tight_layout()

    plt.savefig('pdf/cascade_remianing_graph_size.pdf',dpi=200)


def plot_subgraph_pattern(ax):

    name_num = defaultdict(int)
    subcacade_dict = json.loads(open('data/subgraphs_mapping.json').read())

    for name in subcacade_dict.keys():
        num = name.strip().split('/')[1].split('.')[0].split('_')[-1]
        name_num[name] = int(num)

    ns = []
    names = []
    for name,num in sorted(name_num.items(),key=lambda x:x[1],reverse=True):
        names.append(name)
        ns.append(num)

    total = float(sum(ns))
    xs = []
    acc_n = 0
    x =0
    y=0
    max_n = ns[0]
    per_20=0
    for i,n in enumerate(ns):
        xs.append(i+1)
        if acc_n/total<0.84 and (acc_n+n)/total>0.84:
            x=i
            y=n

        acc_n+=n

        if i==20:
            per_20  = acc_n/total*0.9581

    # x = np.array(range(len(ns)))+1
    ax.plot(xs,ns)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot([x]*10,np.linspace(10,max_n,10),'--',label='P(X<{:})>80%'.format(x))
    ax.plot([20]*10,np.linspace(10,max_n,10),'--',label='P(X<20)={:.4f}'.format(per_20))
    # ax.plot(np.linspace(10,1000,10),[y]*10,'--',c='r')
    # ax.text(300,1000,"({:},{:})".format(x,y))
    for name in  names[:20]:
        print name
        edges = subcacade_dict[name]
        s = name.split("/")[1].split('.')[0]
        new_name = "viz_subcascde/"+s
        plot_a_subcascade(edges,new_name)
        
    # print ks[:10]

def plot_size_n(ax,size_dict,n):

    xs = [] 
    ys = []
    for cc in sorted(size_dict.keys()):
        # paper list
        subgraphs_list = size_dict[cc]
        # percentage list
        percent_list = []
        for subs in subgraphs_list:
            # stat the subcascade size
            sub_counter = Counter(subs)
            n_percent = sub_counter.get(n,0)/float(len(subs))
            percent_list.append(n_percent)

        # print percent_list[:10]
        avg_percent = sum(percent_list)/len(percent_list)

        # number of size n 
        xs.append(cc)
        ys.append(avg_percent)

    # ax.plot(xs,ys,c=color_sequence[n-1],label='N={:}'.format(n))
    z = zip(*lowess(ys,np.log(np.array(xs)),frac= 0.2))[1]
    ax.plot(xs,z,label='size = {:}'.format(n),c=color_sequence[n-1])

if __name__ == '__main__':
    plot_unconnected_subgraphs()
    
