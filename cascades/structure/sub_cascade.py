#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *

def iso(subgraph_dict,graph):
    size = len(graph.edges())
    subgraphs  = subgraph_dict.get(size,{}).keys()
    # logging.info('length of graph: {:}, of existing subgraphs number:{:}'.format(size,len(subgraphs)))
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

def iso_cc(subgraph_dict,graph,cc):
    size = len(graph.edges())
    subgraphs  = subgraph_dict.get(size,{}).keys()
    # logging.info('length of graph: {:}, of existing subgraphs number:{:}'.format(size,len(subgraphs)))
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
                subgraph_dict[size][subgraph].append(cc)
                break

    if not is_iso:
        subgraph_dict[size][graph].append(cc)
    
    return subgraph_dict

## 将与根节点的链接的边去掉,相当于出度小于2的点都去掉了
def unlinked_subgraph(citation_cascade):
    cc = json.loads(open(citation_cascade).read())
    logging.info('data loaded...')
    # 统计有多少图去掉与根节点直接相连的边只有还有图
    # 剩余边的比例 与前面统计的图 出度大于1的点的比例 是相同的
    # remaining_statistics = defaultdict(list)

    # 剩余的边构成的图中，有多少不相互连通的子图
    remaining_subgraphs_dis = defaultdict(list)

    progress_index = 0
    total = len(cc.keys())

    ### 存储subgraph的字典
    subgraph_dict = defaultdict(lambda:defaultdict(list))

    for pid in cc.keys():
        progress_index+=1

        if progress_index%100==0:
            logging.info('progress report:{:}/{:}'.format(progress_index,total))
        yes_count = 0

        edges = cc[pid]['edges']
        size_of_cascade = float(len(edges))
        citation_count = int(cc[pid]['cnum'])

        # 首先要判断是不是有环
        dig  = nx.DiGraph()
        dig.add_edges_from(edges)

        if not nx.is_directed_acyclic_graph(dig):
            continue

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
        # remaining_statistics[citation_count].append(remaining_edges_size/size_of_cascade)

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
            node_size = len(subgraph.nodes())
            subgraphs.append([edge_size,node_size])

            # 如果边的数量小于于50，画出来
            # 判断是否同质
            if edge_size<20:
                subgraph_dict = iso_cc(subgraph_dict,subgraph,citation_count)

        remaining_subgraphs_dis[citation_count].append(subgraphs)

    # write output
    # open('data/remaining_statistics.json','w').write(json.dumps(remaining_statistics))
    open('data/remaining_subgraphs_dis.json','w').write(json.dumps(remaining_subgraphs_dis))
    open('data/subcascade_dict.json','w').write(json.dumps(subgraph_dict))
    # 将已经同质化过的图形，画出来
    save_subgraphs = {}
    html = ['<html> <head> frequency of sub-cascades</head><body>']
    html.append('<table>')
    for size in sorted(subgraph_dict.keys()):
        subgraphs = subgraph_dict[size].keys()
        for i,graph in enumerate(subgraphs):
            count  = len(subgraph_dict[size][graph])

            cc_dis = Counter(subgraph_dict[size][graph])
            plt.figure()
            xs = []
            ys = []
            for cc in sorted(cc_dis.keys()):
                xs.append(cc)
                ys.append(cc_dis[cc])

            plt.plot(xs,ys)
            plt.tight_layout()
            dis_fig = 'subgraph/{:}_{:}_{:}_dis.png'
            plt.savefig(dis_fig,dpi=200)


            ## 对于某一个size对应的子图，画出来
            # plt.figure()
            # nx.draw(graph)
            # plt.text('{:}'.format(count))
            name = 'subgraph/{:}_{:}_{:}.png'.format(size,i,count)
            # plt.savefig(name,dpi=200)
            save_subgraphs[name] = [e for e in graph.edges()]

            html.append('<tr>')
            html.append('<td>')
            html.append('<img src="{:}">'.format(name))
            html.append('</td>')
            html.append('<td>')
            html.append('{:}'.format(count))
            html.append('</td>')
            html.append('<td>')
            html.append('<img src="{:}">'.format(dis_fig))
            html.append('</td>')
            html.append('</tr>')
    html.append('</table>')
    html.append('</body></html>')

    open('data/subgraphs_mapping.json','w').write(json.dumps(save_subgraphs))
    open('sub-cascade.html','w').write('\n'.join(html))

## unconnected subgraphs plot 
def plot_unconnected_subgraphs():
    logging.info('plot statistics figures of sub-cascades')
    # remaining_statistics = json.loads(open('data/remaining_statistics.json').read()) 
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
    fig,axes = plt.subplots(1,5,figsize=(25,5))
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
    ax0 = axes[2]
    ax01 = axes[3]
    for i in range(13):
        n = i+1
        if n <4:
            plot_size_n(ax1,seven_subcas_dis,n)
        elif n<8:
            plot_size_n(ax0,seven_subcas_dis,n)
        else:
            plot_size_n(ax01,seven_subcas_dis,n)

    ax1.set_title('size N < 4  distribution')
    ax1.set_xlabel('citation count\n(b)')
    ax1.set_ylabel('Percentage of size N')
    ax1.set_xscale('log')
    ax1.legend(loc=2)
    # ax1.set_yscale('log')

    ax0.set_title('4 < N < 7 distribution')
    ax0.set_xlabel('citation count\n(b)')
    ax0.set_ylabel('Percentage of size N')
    ax0.set_xscale('log')
    ax0.legend(loc=1)

    ax01.set_title('8 < N < 13 distribution')
    ax01.set_xlabel('citation count\n(b)')
    ax01.set_ylabel('Percentage of size N')
    ax01.set_xscale('log')
    ax01.legend(loc=1)
    # ax0.set_yscale('log')

    ax3 = axes[4]
    plot_subgraph_pattern(ax3,_20_percent)
    ax3.set_title('pattern distribution')
    ax3.set_xlabel('Ranked patterns\n(c)')
    ax3.set_ylabel('Number of patterns')
    ax3.legend()
    plt.tight_layout()

    plt.savefig('pdf/cascade_remianing_graph_size.pdf',dpi=200)


def plot_subgraph_pattern(ax,_20_percent):

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
        if acc_n/total<0.80/_20_percent and (acc_n+n)/total>0.80/_20_percent:
            x=i
            y=n

        acc_n+=n

        if i==20:
            per_20  = acc_n/total*_20_percent

    # x = np.array(range(len(ns)))+1
    ax.plot(xs,ns)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot([x]*10,np.linspace(10,max_n,10),'--',label='P(X<{:})>80%'.format(x))
    ax.plot([20]*10,np.linspace(10,max_n,10),'--',label='P(X<20)={:.4f}'.format(per_20))
    # ax.plot(np.linspace(10,1000,10),[y]*10,'--',c='r')
    # ax.text(300,1000,"({:},{:})".format(x,y))
    for name in  names[:20]:
        print 'plot sub-cascade using graphviz',name
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
    z = zip(*lowess(ys,np.log(np.array(xs)),frac= 0.1))[1]
    ax.plot(xs,z,label='size = {:}'.format(n),c=color_sequence[n-1])


def stat_subcascade_frequecy(citation_cascade):
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

    top_20_subcascade = {}
    for i,name in enumerate(names[:20]):
        dig  = nx.DiGraph()
        dig.add_edges_from(subcacade_dict[name])
        top_20_subcascade[str(i)] = dig

    #对原来的数据遍历一遍
    cc = json.loads(open(citation_cascade).read())
    logging.info('data loaded...')
    progress_index=0
    total = len(cc.keys())
    total_is_cas_dict = defaultdict(dict)
    for pid in cc.keys():
        progress_index+=1

        if progress_index%1000==0:
            logging.info('progress report:{:}/{:}'.format(progress_index,total))

        edges = cc[pid]['edges']
        size_of_cascade = float(len(edges))
        citation_count = int(cc[pid]['cnum'])


        # 首先要判断是不是有环
        dig  = nx.DiGraph()
        dig.add_edges_from(edges)

        if not nx.is_directed_acyclic_graph(dig):
            continue

        remaining_edges=[]
        for edge in edges:
            source = edge[0]
            target = edge[1]
            
            # 保留非直接连接
            if not int(target)==int(pid):
                remaining_edges.append(edge)

        # 剩下的图形大小
        remaining_edges_size = len(remaining_edges)

        #如果剩余边的数量是0，无子图，原图形状为扇形
        if remaining_edges_size==0:
            continue

        # 根据剩余边创建图
        dig  = nx.DiGraph()
        dig.add_edges_from(remaining_edges)
        #对于某一个图形子图来讲
        is_dict = sub_cascade_dis_in_one(dig,top_20_subcascade)

        total_is_cas_dict[pid]['cas'] = is_dict
        total_is_cas_dict[pid]['count'] = citation_count

    open('data/total_cas_index_dis.json','w').write(json.dumps(total_is_cas_dict))
    

def plot_sub_cascade_dis():
    subcas_dis = json.loads(open('data/total_cas_index_dis.json').read())
    
    cc_counter = defaultdict(int)
    for pid in subcas_dis.keys():
        count = subcas_dis[pid]['count']
        cc_counter[count]+=1

    count_mapping = {}
    last_count = 0
    for cc in sorted(cc_counter.keys()):
        num = cc_counter[cc]
        if num>5:
            count_mapping[cc] = cc
            last_count = cc
        else:
            count_mapping[cc] = last_count

    # print cc_counter
    new_cc_counter = defaultdict(int)
    for cc in cc_counter.keys():
        new_cc_counter[count_mapping[cc]] += cc_counter[cc]

    # print new_cc_counter

    # sub cas 的 字典
    subcas_count_value = defaultdict(dict)
    for pid in subcas_dis.keys():
        is_dict = subcas_dis[pid]['cas']
        count = subcas_dis[pid]['count']
        count = count_mapping[count]
        for i in is_dict.keys():
            percent_list = subcas_count_value[i].get(count,[])
            percent_list.append(is_dict[i])
            subcas_count_value[i][count] = percent_list


    #一共20个图
    fig,axes = plt.subplots(4,5,figsize=(25,18))
    for i in subcas_count_value.keys():
        xs = []
        ys = []
        for cc in sorted(subcas_count_value[i].keys()):
            percent_list = subcas_count_value[i][cc]
            #这里求平均值的等于 平均比例*出现的比例
            avg_per = sum(percent_list)/len(percent_list)
            if len(percent_list) > new_cc_counter[cc]:
                print cc,len(percent_list), new_cc_counter[cc]
            presence_per=len(percent_list)/float(new_cc_counter[cc])
            ys.append(avg_per*presence_per)
            xs.append(cc)

        
        ax = axes[int(i)/5,int(i)%5]
        ax.plot(xs,ys,alpha = 0.6)
        zs = [j for j in zip(*lowess(ys,np.log(xs),frac= 0.4))[1]]
        ax.plot(xs,zs,c='r')
        ax.set_xlabel('citation count')
        ax.set_ylabel('percentage')
        ax.set_xscale('log')
        # ax.set_ylabel('log')
        ax.set_title('{:}th sub_cascade'.format(i))
        ax.set_xlim(0.9,2000)
        # ax.yaxis.get_major_formatter().set_powerlimits((0,2))

    plt.tight_layout()
    plt.savefig('pdf/subcascade_dis.pdf',dpi=200)
    logging.info('sub-cascade distribution saved to pdf/subcascade_dis.pdf')


def sub_cascade_dis_in_one(dig,subcas_dict):
    #根据创建的有向图，获得其所有弱连接的子图
    subgraphs =[] 
    is_dict =defaultdict(int)
    for subgraph in nx.weakly_connected_component_subgraphs(dig):
        # 获得图像子图的边的数量
        edge_size = len(subgraph.edges())
        subgraphs.append(edge_size)

        # 因为前20都是小于6的子图
        if edge_size<7:
            # 判断是否与已有的子图同构
            is_sub, name = is_iso_subcascade(subgraph,subcas_dict)
            # 如果有 则记录下来
            if is_sub:
                is_dict[name]+=1

    # 每一种同构图形所占的比例
    for name in is_dict.keys():
        is_dict[name] = is_dict[name]/float(len(subgraphs))
    #返回同构字典
    return is_dict



def is_iso_subcascade(subgraph,subcas_dict):
    for name in subcas_dict.keys():
        subcas = subcas_dict[name]

        if len(subcas.edges()) == len(subgraph.edges()):
            if nx.is_isomorphic(subcas,subgraph):
                return True,name

    return False,'-1'



if __name__ == '__main__':
    # 生成 subcascade
    unlinked_subgraph(sys.argv[1])
    # # 对上面生成的sub-cascade进行统计
    # plot_unconnected_subgraphs()
    # # 重新对前20的subcascade进行同质化统计
    # stat_subcascade_frequecy(sys.argv[1])
    # 画出前20的分布图
    # plot_sub_cascade_dis()
    
