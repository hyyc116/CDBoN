#coding:utf-8
'''
@author: hyyc116
'''

from basic_config import *
import gc
from multiprocessing.dummy import Pool as ThreadPool
from networkx.algorithms import isomorphism
from matplotlib import cm as CM
from collections import Counter
from viz_graph import plot_a_subcascade

#from the aminer_refence to build citation network
def build_citation_network(path):
    ref_dict=defaultdict(dict)
    data = json.loads(open(path).read())
    reflist = data['RECORDS']
    print 'Size of reference', len(reflist)
    count=0
    for ref in reflist:
        count+=1
        if count%10000==1:
            print count
        pid = ref['cpid']
        pid_year = ref['cpid_year']
        cited_pid = ref['pid']
        cited_pid_year = ref['pid_year']

        if int(pid_year)<1900 or int(cited_pid_year)<1900 or int(pid_year)<int(cited_pid_year):
            continue

        cited_dict = ref_dict.get(cited_pid,{})
        cited_dict['pid'] = cited_pid
        cited_dict['year'] = cited_pid_year
        citation_list = cited_dict.get('citations',{})
        citation_list[pid]=pid_year
        cited_dict['citations']=citation_list
        ref_dict[cited_pid] = cited_dict

    open('data/aminer_citation_dict.json','w').write(json.dumps(ref_dict))
    print 'done'

#after building the citation network, we build citation cascade
def build_cascades(citation_network,outpath):
    cn = json.loads(open(citation_network).read())
    logging.info('data loaded...')
    log_count=1
    for pid in cn.keys():
        if log_count%1000==1:
            logging.info('progress:'+str(log_count))

        log_count+=1
        # for a paper, get its dict
        pdict = cn[pid]
        # for its citation dict
        c_dict = pdict['citations']
        citing_pids = c_dict.keys()
        # logging.info('Number of citations:{:}'.format(len(citing_pids)))
        edges = []
        for i,cpid in enumerate(citing_pids):
            edges.append([cpid,pid])
            #get cpid's citation dict
            if cn.get(cpid,-1)==-1:
                continue
            cp_dict = cn[cpid]['citations']
            j=i+1
            while j<len(citing_pids):
                
                scpid = citing_pids[j]
                j+=1
                if cp_dict.get(scpid,'-1')=='-1':
                    continue
                else:
                    edges.append([scpid,cpid])

        pdict['edges'] = edges
        pdict['cnum'] = len(citing_pids)
        pdict['enum'] = len(edges)

        cn[pid] = pdict

    open(outpath,'w').write(json.dumps(cn))
    logging.info('citation cascade saved to {:}.'.format(outpath))

def gen_statistics_data(citation_cascade):
    cc = json.loads(open(citation_cascade).read())
    logging.info('data loaded...')
    # general indicators
    cnum_dict=defaultdict(int)
    enum_dict=defaultdict(int)
    size_depth_dict=defaultdict(list)
    depth_dict=defaultdict(int)
    od_dict = defaultdict(int)
    in_dict = defaultdict(int)
    ## centrality dict
    centrality_dict=defaultdict(list)
    ## Assortativity
    ass_dict = defaultdict(list)

    logi = 0

    plot_dict = {}
        
    cxs=[]
    eys=[]
    dys=[]
    dcxs=[]
    od_ys = []
    id_ys = []

    zero_od_count=0
    for pid in cc.keys():

        #out-degree count
        od_count=0
        #in-degree count
        id_count=0

        #progress 
        logi+=1
        if logi%10000==1:
            logging.info('progress {:}'.format(logi))
        #number of nodes
        cnum_dict[cc[pid]['cnum']]+=1
        cxs.append(cc[pid]['cnum'])
        #number of edges
        enum_dict[cc[pid]['enum']]+=1
        eys.append(cc[pid]['enum'])

        diG = nx.DiGraph()
        edges = cc[pid]['edges']
        diG.add_edges_from(edges)
        #depth of graph
        if nx.is_directed_acyclic_graph(diG):
            depth=nx.dag_longest_path_length(diG)
            # cascade_depths.append(depth)
            depth_dict[depth]+=1
            # cascade_sizes.append(len(edges))
            size_depth_dict[len(edges)].append(depth)
            dys.append(depth)
            dcxs.append(cc[pid]['cnum'])
        else:
            continue

        #degree
        outdegree_dict = diG.out_degree()
        # print outdegree_dict
        for nid,od in outdegree_dict:
            # od = outdegree_dict[nid]

            if od==0:
                zero_od_count+=1

            if od>0:
                # out degree
                od_dict[od]+=1
                # in degree
                ind = diG.in_degree(nid)
                in_dict[ind]+=1

                if ind>0:
                    id_count+=1

            ##od 
            if od > 1:
                od_count+=1

        od_ys.append(od_count/float(cc[pid]['cnum']))
        id_ys.append(id_count/float(cc[pid]['cnum']))

        #centrality
        # degree centrality
        centrality_dict['indegree'].extend(nx.in_degree_centrality(diG).values())
        centrality_dict['outdegree'].extend(nx.out_degree_centrality(diG).values())
        centrality_dict['closeness'].extend(nx.closeness_centrality(diG).values())
        centrality_dict['betweenness'].extend(nx.betweenness_centrality(diG).values())
        # centrality_dict['eigenvector'].extend(nx.eigenvector_centrality(diG).values())
        centrality_dict['katz'].extend(nx.katz_centrality(diG).values())
        centrality_dict['assortativity'].append(nx.degree_assortativity_coefficient(diG))




    print 'zero od count:',zero_od_count
    open('data/nodes_size.json','w').write(json.dumps(cnum_dict))
    open('data/cascade_size.json','w').write(json.dumps(enum_dict))
    open('data/depth.json','w').write(json.dumps(depth_dict))
    open('data/out_degree.json','w').write(json.dumps(od_dict))
    open('data/in_degree.json','w').write(json.dumps(in_dict))

    open('data/centrality.json','w').write(json.dumps(centrality_dict))

    
    plot_dict['cxs'] = cxs;
    plot_dict['eys'] = eys;
    plot_dict['dys'] = dys;
    plot_dict['dcx'] = dcxs;
    plot_dict['od_ys'] = od_ys
    plot_dict['id_ys'] = id_ys

    open('data/plot_dict.json','w').write(json.dumps(plot_dict))

def plot_heatmap(x,y,ax,bins,fig,gridsize=30):
    hb = ax.hexbin(x, y, gridsize=gridsize, cmap=CM.Blues, bins='log',xscale=bins[0] ,yscale=bins[1])

# 统计指标的分布图
def stats_plot():
    logging.info('plot data ...')

    # add 80% percent x

    num = len(plt.get_fignums())
    # plt.figure(num)
    fig,axes = plt.subplots(1,5,figsize=(25,5))
    #### node size 
    logging.info('plot node size ...')
    cnum_dict = json.loads(open('data/nodes_size.json').read())
    ax1 = axes[0]
    xs=[]
    ys=[]
    total = sum(cnum_dict.values()) 
    _80_total = float(0)
    _80_x = 0
    _80_y = 0
    _max_y = 0
    for num in sorted([int(num) for num in cnum_dict.keys()]):
        v = cnum_dict[str(num)]
        xs.append(num)
        ys.append(v)

        if _80_total/total<0.8 and (_80_total+v)/total>0.8:
            _80_x = num
            _80_y = v

        _80_total+= v

        if v>_max_y:
            _max_y = v

    popt,pcov = curve_fit(power_low_func,xs[30:400],ys[30:400])


    ax1.plot(xs,ys,'o',fillstyle='none')
    ax1.plot(np.linspace(30, 500, 10), power_low_func(np.linspace(30, 500, 10), *popt)*10,label='$\\alpha={:.2f}$'.format(popt[0]))
    ax1.set_title('citation count distribution')
    ax1.set_xlabel('$x=$citation count\n(a)')
    ax1.set_ylabel('$N(x)$')
    ax1.set_yscale('log')
    ax1.set_xscale('log')
    # plot the 80%
    ax1.plot([_80_x]*10,np.linspace(100,_max_y,10),'--',label='$x={:}$'.format(_80_x))
    # ax1.text(_80_x-5,_80_y,'({:},{:})'.format(_80_x,_80_y))
    ax1.legend()

    #### cascade size
    logging.info('plotting cascade size ...')
    enum_dict = json.loads(open('data/cascade_size.json').read())
    ax2 = axes[1]
    total = sum(enum_dict.values()) 
    _80_total = float(0)
    _80_x = 0
    _80_y = 0
    _max_y = 0
    
    for num in sorted([int(num) for num in enum_dict.keys()]):
        xs.append(num)
        v = enum_dict[str(num)]
        ys.append(v)

        if _80_total/total<0.8 and (_80_total+v)/total>0.8:
            _80_x = num
            _80_y = v

        _80_total+= v

        if v>_max_y:
            _max_y = v


    ax2.plot(xs,ys,'o',fillstyle='none')

    popt,pcov = curve_fit(power_low_func,xs[20:400],ys[20:400])
    ax2.plot(np.linspace(30, 500, 10), power_low_func(np.linspace(30, 500, 10), *popt)*10,label='$\\alpha={:.2f}$'.format(popt[0]))
    ax2.plot([_80_x]*10,np.linspace(100,_max_y,10),'--',label='$x={:}$'.format(_80_x))
    ax2.set_title('cascade size distribution')
    ax2.set_xlabel('$x=$cascade size\n(b)')
    ax2.set_ylabel('$N(x)$')
    ax2.set_yscale('log')
    ax2.set_xscale('log') 
    ax2.legend()


    ####depth
    logging.info('plotting cascade depth ...')
    depth_dict = json.loads(open('data/depth.json').read())
    ax3=axes[2]
    xs=[]
    ys=[]
    total = sum(depth_dict.values()) 
    _80_total = float(0)
    _80_x = 0
    _80_y = 0
    _max_y = 0
    for depth in sorted([int(i) for i in depth_dict.keys()]):
        xs.append(int(depth))
        v = depth_dict[str(depth)]
        ys.append(v)

        if _80_total/total<0.8 and (_80_total+v)/total>0.8:
            _80_x = depth
            _80_y = v

        _80_total+= v

        if v>_max_y:
            _max_y = v

    # use exponential func to fit the distribution

    popt,pcov = curve_fit(exponential_func,xs,ys)

    print xs
    print ys
    ax3.plot(xs,ys,'o',fillstyle='none')
    mean  = 1/popt[0]
    ax3.plot(np.linspace(1, 12, 12), exponential_func(np.linspace(1, 12, 12), *popt),label='$\\lambda={:.2f}$'.format(popt[0]))
    ax3.set_xlabel('$x=$cascade depth\n(c)')
    ax3.set_ylabel('$N(x)$')
    ax3.plot([_80_x]*10,np.linspace(100,1000000,10),'--',label='x={:}'.format(_80_x))
    # ax3.plot([mean]*10,np.linspace(10,100000,10),'--',label='mean={:.2f}'.format(mean))
   
    ax3.set_title('cascade depth distribution')
    ax3.set_yscale('log')
    ax3.set_xlim(0,13)
    ax3.set_xticks(range(14),[str(i) for i in range(14)])
    ax3.legend()

    #### In and out degree
    logging.info('plotting degree ...')
    in_degree_dict=json.loads(open('data/in_degree.json').read())
    out_degree_dict=json.loads(open('data/out_degree.json').read())
    ax4 = axes[3]
    xs=[]
    ys=[]
    total = sum(in_degree_dict.values()) 
    _80_total = float(0)
    _80_x = 0
    _80_y = 0
    _max_y = 0
    for ind in sorted([int(i) for i in in_degree_dict.keys()]):
            
        xs.append(ind+1)
        v = in_degree_dict[str(ind)]
        ys.append(v)

        if _80_total/total<0.8 and (_80_total+v)/total>0.8:
            _80_x = ind+1
            _80_y = v

        _80_total+= v

        if v>_max_y:
            _max_y = v

    popt,pcov = curve_fit(power_low_func,xs[:100],ys[:100])
    ax4.plot(xs,ys,'o',fillstyle='none')
    ax4.set_xlabel('$x = deg^{-}(v)+1$\n(d)')
    ax4.set_ylabel('$N(x)$')
    
    ax4.plot(np.linspace(3, 100, 10), power_low_func(np.linspace(3, 100, 10), *popt)*10,label='$\\alpha={:.2f}$'.format(popt[0]))
    ax4.plot([_80_x]*10,np.linspace(100,_max_y*2,10),'--',label='$x={:}$'.format(_80_x))

    ax4.set_title('in degree distribution')
    ax4.set_yscale('log')
    ax4.set_xscale('log')
    ax4.legend()

    # ax2=axes[1]
    # ax2.scatter(cascade_sizes,cascade_depths,marker='.')

    ax5=axes[4]
    xs=[]
    ys=[]
    total = sum(out_degree_dict.values()) 
    _80_total = float(0)
    _80_x = 0
    _80_y = 0
    _max_y = 0
    for od in sorted([int(i) for i in out_degree_dict.keys()]):
        xs.append(od)
        v = out_degree_dict[str(od)]
        ys.append(v)

        if _80_total/total<0.8 and (_80_total+v)/total>0.8:
            _80_x = od
            _80_y = v

        _80_total+= v

        if v>_max_y:
            _max_y = v

    popt,pcov = curve_fit(power_low_func,xs[10:40],ys[10:40]) 
    ax5.plot(xs,ys,'o',fillstyle='none')


    ax5.plot(np.linspace(10, 30, 10), power_low_func(np.linspace(10, 30, 10), *popt)*10,label='$\\alpha={:.2f}$'.format(popt[0]))
    ax5.plot([_80_x]*10,np.linspace(100,_max_y*2,10),'--',label='$x={:}$'.format(_80_x))

    ax5.set_title('out degree distribution')
    ax5.set_xlabel('$x = deg^{+}(v)$\n(e)')
    ax5.set_ylabel('$N(x)$')
    ax5.set_xscale('log')
    ax5.set_yscale('log')
    ax5.legend()

    plt.tight_layout()
    plt.savefig('pdf/statistics.pdf',dpi=300)
    logging.info('figures saved to pdf/statistics.pdf.')

### centrality
def plot_centrality():
    num = len(plt.get_fignums())
    # plt.figure(num)
    fig,axes = plt.subplots(1,5,figsize=(25,5))
    #### node size 
    # logging.info('plot node size ...')sz 
    centrality_dict = json.loads(open('data/centrality.json').read())

    # degree 
    indegree_list = centrality_dict['indegree']
    ax1 = axes[0]
    plot_cumulative_dis(ax1,indegree_list,'in degree centrality','$x$','$P_x$',False,False)

    outdegree_list = centrality_dict['outdegree']
    ax2 = axes[1]
    plot_cumulative_dis(ax2,outdegree_list,'out degree centrality','$x$','$P_x$',False,True)
    # closeness 
    closeness_list = centrality_dict['closeness']
    ax3 = axes[2]
    plot_cumulative_dis(ax3,closeness_list,'closeness','$x$','$P_x$',False,False)
    # betweenness
    betweenness_list = centrality_dict['betweenness']
    ax4 = axes[3]
    plot_cumulative_dis(ax4,betweenness_list,'betweenness','$x$','$P_x$',False,False)
    # katz
    katz_list = centrality_dict['katz']
    ax5= axes[4]
    plot_cumulative_dis(ax5,katz_list,'katz','$x$','$P_x$',False,False)


    plt.tight_layout()
    plt.savefig('pdf/centrality.pdf',dpi=200)


# plot one kind of centrality
def plot_cumulative_dis(ax,alist,title,xlabel,ylabel,isxlog=True,isylog=True):
    acounter = Counter(alist)
    total = float(len(alist))
    last_num = len(alist)
    xs = []
    ys = []
    for a in sorted(acounter.keys()):
        xs.append(a)
        ys.append(last_num/total)
        last_num = last_num-acounter[a]

    # xs = np.array(xs)+0.000001
    ax.plot(xs,ys)
    if isxlog:
        ax.set_xscale('log')
    if isylog:
        ax.set_yscale('log')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


# 随着citation count的增加，各个指标的变化
def plot_dict():

    plot_dict = json.loads(open('data/plot_dict.json').read())
    ###plot the comparison figure

    cxs= plot_dict['cxs']
    eys= plot_dict['eys']
    dys= plot_dict['dys']
    dcxs=plot_dict['dcx']
    od_ys = plot_dict['od_ys']
    id_ys = plot_dict['id_ys']

    for ii,indgree in enumerate(id_ys):
        if indgree==1:
            print cxs[ii],indgree

    num = len(plt.get_fignums())
    # plt.figure(num)
    fig,axes = plt.subplots(1,5,figsize=(25,5))

    print 'length of xs and ys', len(cxs),len(eys),len(dcxs),len(dys),len(od_ys),len(id_ys)

    # cascade size vs citation count
    ax1 = axes[0]
    ax1.scatter(cxs,eys)
    ax1.plot(cxs,cxs,'--',label='y=x',c='r')
    ax1.set_xlabel('Citation Count\n(a)')
    ax1.set_ylabel('Cascade Size')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_title('Cascade Size Dis')
    
    # ax11 = axes[1,0]
    # plot_heatmap(cxs,eys,ax11,['log','log'],fig)
    # ax11.set_xlabel('Citation Count')
    # ax11.set_ylabel('Cascade Size')
    # ax11.set_title('Cascade Size Dis')

    ## ratio of cascade size/ ciattion count vs citation count
    ax2 = axes[1]
    rys=[]
    max_dict = defaultdict(int)
    for i in range(len(cxs)):
        y  = eys[i]/float(cxs[i])-1
        rys.append(y)
        if y> max_dict[cxs[i]]:
            max_dict[cxs[i]] = y

    fit_x = []
    fit_y = []
    for key in sorted(max_dict.keys()):
        fit_x.append(key)
        fit_y.append(max_dict[key])

    ax2.scatter(cxs,rys)

    ax2.plot(fit_x,fit_y,c=color_sequence[3],alpha=0.8)
    #把数据前面的点加多 
    fit_z = [i for i in zip(*lowess(fit_y[:10],fit_x[:10],frac= 0.9))[1]]
    # ax2.plot(fit_x[:10],fit_z,c='r')
    fit_z_2 = [i for i in zip(*lowess(fit_y[10:],fit_x[10:],frac= 0.9))[1]]
    fit_z.extend(fit_z_2)
    ax2.plot(fit_x,fit_z,c='r')

    # popt,pcov = curve_fit(square_x,new_fit_x,new_fit_y) 

    # ax2.plot(np.linspace(1,8000,100), square_x(np.linspace(1,8000,100), *popt),c='r')
    
    ax2.set_xlabel('Citation Count\n(b)')
    ax2.set_ylabel('Average Marginal Value')
    ax2.set_xscale('log')
    ax2.set_title('Average Marginal Value')
    # ax12 = axes[1,1]
    # plot_heatmap(cxs,rys,ax12,['log','linear'],fig)
    # ax12.set_xlabel('Citation Count')
    # ax12.set_ylabel('Cascade size/citation count')
    # ax12.set_title('Cascade size/citation count')


    ### depth distribution over citation count
    ax3=axes[2]
    ax3.scatter(dcxs,dys)
    ax3.set_xlabel('Citation Count\n(c)')
    ax3.set_ylabel('Cascade Depth')
    ax3.set_xscale('log')
    ax3.set_title('Depth Distribution')

    # ax13 = axes[1,2]
    # plot_heatmap(dcxs,dys,ax13,['log','linear'],fig,(8,8))
    # ax13.set_xlabel('Citation Count')
    # ax13.set_ylabel('Depth of citation cascade')
    # ax13.set_title('Cascade Depth Distribution')

    #### in degree over citation count
    ax5 = axes[3]
    ax5.scatter(dcxs,id_ys)
    ax5.set_xlabel('Citation Count\n(d)')
    ax5.set_ylabel('$P(v=connector)$')
    ax5.set_xscale('log')
    ax5.set_title('Percentage of connectors')
    sdxcs = np.array([float(i) for i in sorted(dcxs) if i>1])
    ax5.plot(sdxcs,1/sdxcs,c='r')
    ax5.plot(sdxcs,1-1/sdxcs,c='r')
    # ax15 = axes[1,4]
    # plot_heatmap(dcxs,id_ys,ax15,['log','linear'],fig)
    # ax15.set_xlabel('Citation Count')
    # ax15.set_ylabel('Percentage')
    # ax15.set_title('In degree(>0) Distribution')

    ### out degree over citation count
    ax4 = axes[4]
    ax4.scatter(dcxs,od_ys)
    ax4.set_xlabel('Citation Count\n(e)')
    ax4.set_ylabel('$P(deg^+(v)>1)$')
    ax4.set_xscale('log')
    ax4.set_title('Out degree > 1')
    ax4.plot(sdxcs,1/sdxcs,c='r')
    ax4.plot(sdxcs,1-1/sdxcs,c='r')

    # ax14 = axes[1,3]
    # plot_heatmap(dcxs,od_ys,ax14,['log','linear'],fig)
    # ax14.set_xlabel('Citation Count')
    # ax14.set_ylabel('Percentage')
    # ax14.set_title('Out degree(>1) Distribution')

    

    plt.tight_layout()
    plt.savefig('pdf/compare.png',dpi=200)
    print 'figure saved to pdf/compare.png'


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

    # 首先画 剩余图形中 边的数量的比例分布图,散点图
    # 横坐标为citation count 
    # xs = []
    # ys = []
    # for k in sorted([int(k) for k in remaining_statistics.keys()]):
    #     citation_count = str(k)
    #     # print 'citation_count:',citation_count
    #     for percent in remaining_statistics[citation_count]:
    #         xs.append(citation_count)
    #         ys.append(percent)

    # fig,axes = plt.subplots(1,3,figsize=(15,5))
    # ax1 = axes[0]
    # ax1.scatter(xs,ys)
    # ax1.set_xscale('log')

    # 在有剩余图的里面，找到的联通子图的分布

    total_dis = 0
    remain_edges_size = defaultdict(int)

    citation_counts_dict = defaultdict(list)
    lastk = 0
    for k in sorted([int(k) for k in remaining_subgraphs_dis.keys()]):
        k_count = len(remaining_subgraphs_dis[str(k)])
        for subgraphs in remaining_subgraphs_dis[str(k)]:
            ##  如果这个k对应的文章数量小于10，遇上一个k合并
            if k_count<10:
                citation_counts_dict[lastk].extend(subgraphs)
            else:
                citation_counts_dict[k].extend(subgraphs)
                lastk = k
                
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
        plot_size_n(ax1,citation_counts_dict,n)

    ax1.set_title('scize N distribution')
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
            per_20  = acc_n/total

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
        # size list
        size_list = size_dict[cc]
        total_num = len(size_list)
        # counter    
        counter = Counter(size_list)
        # number of size n 
        xs.append(cc)
        ys.append(counter[n]/float(total_num))

    ax.plot(xs,ys,c=color_sequence[n-1],label='N={:}'.format(n))
    # z = zip(*lowess(ys,xs,frac= 0.9))[1]
    # ax.plot(xs,z,label='size = {:}'.format(n),c=color_sequence[n-1])






###three levels of 
def three_levels_dis():
    high_cited_papers = [i for i in json.loads(open('../friction/data/high_selected_papers.json').read()).keys()]
    medium_cited_papers = [i for i in json.loads(open('../friction/data/medium_selected_papers.json').read()).keys()]
    low_cited_papers = [i for i in json.loads(open('../friction/data/low_selected_papers.json').read()).keys()]

    print high_cited_papers,len(high_cited_papers)
    print medium_cited_papers,len(medium_cited_papers)
    print low_cited_papers,len(low_cited_papers)

    ### low medium high

def main():
    # build_citation_network(sys.argv[1])
    # build_cascades(sys.argv[1])
    label = sys.argv[1]
    if label== 'gen_stat':
        gen_statistics_data(sys.argv[2])
    elif label == 'stat_plot':
        stats_plot()
    elif label == 'build_cascade':
        build_cascades(sys.argv[2])
    elif label =='compare_plot':
        plot_dict()
    elif label=='unlinked_subgraph':
        unlinked_subgraph(sys.argv[2])
    elif label == 'plot_subgraph':
        plot_unconnected_subgraphs()
    elif label == 'plot_centrality':
        plot_centrality()


if __name__ == '__main__':
    main()
    # a=[(1,2),(4,2)]
    # b = [(2,3),(5,3)]
    # ag = nx.DiGraph()
    # ag.add_edges_from(a)
    # bg = nx.DiGraph()
    # bg.add_edges_from(b)
    # print nx.is_isomorphic(ag,bg)

    



