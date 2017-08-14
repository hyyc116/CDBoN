#coding:utf-8

from basic_config import *
import gc
from multiprocessing.dummy import Pool as ThreadPool
from networkx.algorithms import isomorphism

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


# def statistics_all(citation_cascade):
    # cc = json.loads(open(citation_cascade).read())


def gen_statistics_data(citation_cascade):
    cc = json.loads(open(citation_cascade).read())
    logging.info('data loaded...')
    cnum_dict=defaultdict(int)
    enum_dict=defaultdict(int)
    size_depth_dict=defaultdict(list)
    depth_dict=defaultdict(int)
    od_dict = defaultdict(int)
    in_dict = defaultdict(int)
    logi = 0
        
    cxs=[]
    eys=[]
    dys=[]
    for pid in cc.keys():
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
        #degree
        outdegree_dict = diG.out_degree()
        for nid in outdegree_dict.keys():
            od = outdegree_dict[nid]
            od_dict[od]+=1
            if od >0:
                ind = len(diG.in_edges(nid))
                in_dict[ind]+=1

    open('data/nodes_size.json','w').write(json.dumps(cnum_dict))
    open('data/cascade_size.json','w').write(json.dumps(enum_dict))
    open('data/depth.json','w').write(json.dumps(depth_dict))
    open('data/out_degree.json','w').write(json.dumps(od_dict))
    open('data/in_degree.json','w').write(json.dumps(in_dict))

    ###plot the comparison figure

    num = len(plt.get_fignums())
    # plt.figure(num)
    fig,axes = plt.subplots(1,3,figsize=(15,5))

    print 'length of xs and ys', len(cxs),len(eys),len(dys)

    # cascade size vs citation count
    ax1 = axes[0]
    ax1.scatter(cxs,eys)
    ax1.set_xlabel('Citation Count')
    ax1.set_ylabel('Cascade Size')

    ## ratio of cascade size/ ciattion count vs citation count
    ax2 = axes[1]
    rys = [eys[i]/cxs[i] for i in range(cxs)]
    ax2.scatter(cxs,rys)
    ax2.set_xlabel('Citation Count')
    ax2.set_ylabel('Ratio of cascade size and citation count')

    ### depth distribution over citation count
    ax3=axes[2]
    ax3.scatter(cxs,dys)
    ax3.set_xlabel('Citation Count')
    ax3.set_ylabel('Depth of citation cascade')

    plt.tight_layout()
    plt.savefig('pdf/compare.pdf',dpi=200)
    print 'figure saved to pdf/compare.pdf'



def stats_plot():
    logging.info('plot data ...')

    num = len(plt.get_fignums())
    # plt.figure(num)
    fig,axes = plt.subplots(1,5,figsize=(25,5))
    #### node size 
    logging.info('plot node size ...')
    cnum_dict = json.loads(open('data/nodes_size.json').read())
    ax1 = axes[0]
    xs=[]
    ys=[]
    for num in sorted(cnum_dict.keys()):
        xs.append(num)
        ys.append(cnum_dict[num])
    ax1.plot(xs,ys,'o',fillstyle='none')
    ax1.set_title('Citation Count Distribution')
    ax1.set_xlabel('Citation Count')
    ax1.set_ylabel('Number')
    ax1.set_yscale('log')
    ax1.set_xscale('log')

    #### cascade size
    logging.info('plotting cascade size ...')
    ax2 = axes[1]
    enum_dict = json.loads(open('data/cascade_size.json').read())
    for num in sorted(enum_dict.keys()):
        xs.append(num)
        ys.append(enum_dict[num])

    ax2.plot(xs,ys,'o',fillstyle='none')
    ax2.set_title('Cascade Size Distribution')
    ax2.set_xlabel('Cascade Size')
    ax2.set_ylabel('Number')
    ax2.set_yscale('log')
    ax2.set_xscale('log')


    ####depth
    logging.info('plotting cascade depth ...')
    depth_dict = json.loads(open('data/depth.json').read())
    ax3=axes[2]
    xs=[]
    ys=[]
    for depth in sorted([int(i) for i in depth_dict.keys()]):
        xs.append(int(depth))
        ys.append(depth_dict[str(depth)])

    print xs 
    print ys
    ax3.plot(xs,ys,marker = '.',fillstyle='none')
    ax3.set_xlabel('Cascade depth')
    ax3.set_ylabel('Count')
    ax3.set_title('Cascade depth distribution')
    ax3.set_yscale('log')

    #### In and out degree
    logging.info('plotting degree ...')
    in_degree_dict=json.loads(open('data/in_degree.json').read())
    out_degree_dict=json.loads(open('data/out_degree.json').read())
    ax4 = axes[3]
    xs=[]
    ys=[]
    for ind in sorted(in_degree_dict.keys()):
        xs.append(ind)
        ys.append(in_degree_dict[ind])

    ax4.plot(xs,ys,'.')
    ax4.set_xlabel('In Degree')
    ax4.set_ylabel('Count')
    ax4.set_title('In Degree distribution')
    ax4.set_yscale('log')
    ax4.set_xscale('log')

    # ax2=axes[1]
    # ax2.scatter(cascade_sizes,cascade_depths,marker='.')

    ax5=axes[4]
    xs=[]
    ys=[]
    for od in sorted(out_degree_dict.keys()):
        xs.append(od)
        ys.append(out_degree_dict[od])

    ax5.plot(xs,ys,'.')
    ax5.set_title('Out Degree distribution')
    ax5.set_xlabel('Out Degree')
    ax5.set_ylabel('Count')
    ax5.set_xscale('log')
    ax5.set_yscale('log')

    plt.tight_layout()
    plt.savefig('pdf/statistics.pdf',dpi=300)
    logging.info('figures saved to pdf/statistics.pdf.')

def cascade_depth_distribution(citation_cascade):
    cc = json.loads(open(citation_cascade).read())
    logging.info('data loaded...')
    # cascade_depths=[]
    # cascade_sizes=[]
    size_depth_dict=defaultdict(list)
    depth_dict=defaultdict(int)
    logi = 0
    for pid in cc.keys():
        logi+=1
        if logi%10000==1:
            logging.info('progress {:}'.format(logi))
        diG = nx.DiGraph()
        edges = cc[pid]['edges']
        diG.add_edges_from(edges)
        if nx.is_directed_acyclic_graph(diG):
            depth=nx.dag_longest_path_length(diG)
            # cascade_depths.append(depth)
            depth_dict[depth]+=1
            # cascade_sizes.append(len(edges))
            size_depth_dict[len(edges)].append(depth)

    logging.info('plot data...')
    fig,axes = plt.subplots(1,2,figsize=(10,5))
    ax1 = axes[0]
    xs=[]
    ys=[]
    for depth in sorted(depth_dict.keys()):
        xs.append(depth)
        ys.append(depth_dict[depth])

    ax1.plot(xs,ys,'.',fillstyle='none')
    ax1.set_xlabel('Cascade depth')
    ax1.set_ylabel('Count')
    ax1.set_title('Cascade depth distribution')
    ax1.set_yscale('log')
    # ax1.set_xscale('log')

    # ax2=axes[1]
    # ax2.scatter(cascade_sizes,cascade_depths,marker='.')

    ax2=axes[1]
    xs=[]
    ys=[]
    for size in sorted(size_depth_dict.keys()):
        xs.append(size)
        ys.append(np.mean(size_depth_dict[size]))

    ax2.plot(xs,ys,'.')
    ax2.set_title('Depth vs. Cascade Size')
    ax2.set_xlabel('Cascade Size')
    ax2.set_ylabel('Mean of Cascade depth')
    # ax2.set_yscale('log')
    # ax2.set_xscale('log')

    plt.tight_layout()
    plt.savefig('pdf/cascade_depth.pdf',dpi=300)
    logging.info('figure saved to pdf/cascade_depth.pdf.')


def cascade_degree_distribution(citation_cascade):
    cc = json.loads(open(citation_cascade).read())
    logging.info('data loaded...')
    # cascade_depths=[]
    # cascade_sizes=[]
    size_depth_dict=defaultdict(list)
    depth_dict=defaultdict(int)
    logi = 0
    od_dict = defaultdict(int)
    in_dict = defaultdict(int)

    for pid in cc.keys():
        logi+=1
        if logi%10000==1:
            logging.info('progress {:}'.format(logi))
        diG = nx.DiGraph()
        edges = cc[pid]['edges']
        diG.add_edges_from(edges)
        outdegree_dict = diG.out_degree()
        for nid in outdegree_dict.keys():
            od = outdegree_dict[nid]
            od_dict[od]+=1
            if od >0:
                ind = len(diG.in_edges(nid))
                in_dict[ind]+=1

    open('data/out_degree.json','w').write(json.dumps(od_dict))
    open('data/in_degree.json','w').write(json.dumps(in_dict))

    logging.info('Done')

        # if nx.is_directed_acyclic_graph(diG):
        #     depth=nx.dag_longest_path_length(diG)
        #     # cascade_depths.append(depth)
        #     depth_dict[depth]+=1
        #     # cascade_sizes.append(len(edges))
        #     size_depth_dict[len(edges)].append(depth)

    # logging.info('plot data...')

###three levels of 
def three_levels_dis():
    high_cited_papers = [i for i in json.loads(open('../friction/data/high_selected_papers.json').read()).keys()]
    medium_cited_papers = [i for i in json.loads(open('../friction/data/medium_selected_papers.json').read()).keys()]
    low_cited_papers = [i for i in json.loads(open('../friction/data/low_selected_papers.json').read()).keys()]

    print high_cited_papers,len(high_cited_papers)
    print medium_cited_papers,len(medium_cited_papers)
    print low_cited_papers,len(low_cited_papers)

    ### low medium high



def draw_degree_plot():
    in_degree_dict=json.loads(open('data/in_degree.json').read())
    out_degree_dict=json.loads(open('data/out_degree.json').read())
    fig,axes = plt.subplots(1,2,figsize=(10,5))
    ax1 = axes[0]
    xs=[]
    ys=[]
    for ind in sorted(in_degree_dict.keys()):
        xs.append(ind)
        ys.append(in_degree_dict[ind])

    ax1.plot(xs,ys,'.')
    ax1.set_xlabel('In Degree')
    ax1.set_ylabel('Count')
    ax1.set_title('In Degree distribution')
    ax1.set_yscale('log')
    ax1.set_xscale('log')

    # ax2=axes[1]
    # ax2.scatter(cascade_sizes,cascade_depths,marker='.')

    ax2=axes[1]
    xs=[]
    ys=[]
    for od in sorted(out_degree_dict.keys()):
        xs.append(od)
        ys.append(out_degree_dict[od])

    ax2.plot(xs,ys,'.')
    ax2.set_title('Out Degree distribution')
    ax2.set_xlabel('Out Degree')
    ax2.set_ylabel('Count')
    ax2.set_xscale('log')
    ax2.set_yscale('log')

    plt.tight_layout()
    plt.savefig('pdf/cascade_degree.pdf',dpi=300)
    logging.info('figure saved to pdf/cascade_degree.pdf.')

#cascade subgraph
def cascade_subgraph(graph):
    ungraph = graph.to_undirected()
    nodes = ungraph.nodes()
    logging.info('Size of graph:{:}'.format(len(nodes)))
    subgraphs=[]
    paths=[]
    for i,target in enumerate(nodes):
        # logging.info('target {:}'.format(i))
        j=i+1
        while j < len(nodes):
            source = nodes[j]
            for path in nx.all_simple_paths(ungraph,target,source,10):
                paths.append(set(path))

            # for path in nx.all_simple_paths(ungraph,source,target):
            #     paths.append(set(path))

            j+=1

    logging.info('Size of paths:{:}'.format(len(paths)))
    size_two = 0
    for i,path in enumerate(paths):
        subgraphs.append(','.join(sorted(list(path))))
        j = i+1
        while j < len(paths):
            # print j
            spath = paths[j]
            if len(path&spath)>0:
                newpath = sorted(list(path| paths[j]))
                subgraphs.append(','.join(newpath))
            j+=1   

    paths=[]
    gc.collect()
    subgraphs = list(set(subgraphs))
    logging.info('number of subgraphs:{:}'.format(len(subgraphs)))
    logging.info('Size two:{:}'.format(size_two))
    logging.info('subgraph extraction ...')

    return subgraphs


def subgraph_statistics(citation_cascade,start,end):
    logging.info('from {:} to {:}...'.format(start,end))
    cc = json.loads(open(citation_cascade).read())
    logging.info('{:} data loaded...'.format(len(cc.keys())))

    step=5000
    if end>10:
        step = 1000
    
    if end>100:
        step = 50
    
    if end>500:
        step=5

    logging.info('Steps:{:}'.format(step))

    # return None

    new_cascade = {}
    # pid_subgraph=defaultdict(dict)
    for pid in cc.keys():
        cnum = cc[pid]['cnum']
        if cnum<start:
            continue
        elif cnum>=end:
            continue

        new_cascade[pid] = cc[pid]

    length = len(new_cascade)
    logging.info('Number of papers in this zone:{:}'.format(length))

    del cc 
    gc.collect()

    logi = 0
    for pid in new_cascade.keys():
        logi+=1
        logging.info('progress {:}/{:}'.format(logi,length))

        diG = nx.DiGraph()
        edges = new_cascade[pid]['edges']
        # if len(edges)<1000:
        #     continue
        diG.add_edges_from(edges)
        subgraphs = cascade_subgraph(diG)
        for subgraph in subgraphs:
            print str(pid)+"\t"+str(subgraph)

        subgraphs=[]
        gc.collect()

    logging.info('DONE')


def isomorohic():
    name_clusters=defaultdict(list)
    names = subgraphs.keys()
    for i,name in enumerate(names):
        g1=subgraphs[name]
        j=i+1
        while j < len(names):
            g2 = subgraphs[names[j]]
            if nx.is_isomorphic(g1,g2):
                print name,names[j]
            j+=1
    

def create_subgraph(G,sub_G,start_node):
    for n in G.successors_iter(start_node):
        sub_G.add_path([start_node,n])
        create_subgraph(G,sub_G,n)


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
    elif label == 'degree':
        cascade_degree_distribution(sys.argv[2])
    elif label =='degree_plot':
        draw_degree_plot()
    elif label =='subgraphs':
        subgraph_statistics(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
    elif label == 'gen_sub':
        generate_subgraphs_(int(sys.argv[2]))

def test_subgrah():
    # graph = nx.DiGraph()
    # edges = [('2','1'),('3','1'),('3','2'),('4','2'),('4','3'),('4','1'),('5','1'),('5','4'),('6','3'),('7','4'),('8','7')]
    # graph.add_edges_from(edges)
    # print graph.out_degree('1')
    # print graph.in_edges('1')
    # for edges in cascade_subgraph(graph):
        # print edges
    pass

def generate_subgraphs_(N):
    pool = ThreadPool(8)
    diG = nx.complete_graph(N).to_directed()
    edges = diG.edges()
    minL = N-1
    maxL = len(edges)/2
    subgraphs = []
    logging.info('edges:{:}'.format(maxL))
    progress=0
    sub_index=0

    for num in range(minL,maxL+1):
        incere_index=0
        logging.info('Number of edges:{:}.'.format(num))
        last_number=0
        for sub_edges in iter_tools(edges,num):
            progress+=1
            # print sub_edges
            subDG=nx.DiGraph()
            subDG.add_edges_from(sub_edges)
            # is connected
            if len(subDG.nodes())==N and nx.is_connected(subDG.to_undirected()) and nx.is_directed_acyclic_graph(subDG):
                sub_index+=1
                if not isIso_matcher(subgraphs,subDG,pool):
                    subgraphs.append(subDG)
                    ses = ""
                    for e in sub_edges:
                        ses+='{:}_{:} '.format(e[0],e[1])

                    print ses.strip()
                
                number_of_subgraphs = len(subgraphs)
                
                if sub_index%500==1:
                    if number_of_subgraphs==last_number:
                        incere_index+=1
                    else:
                        incere_index=0

                last_number=number_of_subgraphs



            if progress%5000==1:
                logging.info('progress:{:},sub_index:{:},size of subgraphs:{:},duplicate times:{:}.'.format(progress,sub_index,number_of_subgraphs,incere_index))
                

            if incere_index>19:
                logging.info('progress:{:},sub_index:{:},size of subs:{:},duplicate times:{:},EDGES:{:},BREAKING........'.format(progress,sub_index,len(subgraphs),incere_index,N))
                incere_index=0
                break

    logging.info('progress:{:},size of subs:{:}.DONE'.format(progress,len(subgraphs)))


def isIso(gset,subg,pool):
    isISO=False
    for g in gset:
        if nx.is_isomorphic(g,subg):
            isISO=True
            break

    return isISO

def isIso_matcher(gset,subg,pool):
    isISO=False
    for g in gset:
        if isomorphism.GraphMatcher(g,subg).is_isomorphic():
            isISO=True
            break

    return isISO

def isIso_multi(glist,subg,pool):
    paralist = [(subg,g) for g in glist]
    results = pool.map(iso_multi, paralist)
    # if the the subg has a isomorphic graph in list return true
    if sum(results)==0:
        return False
    else:
        return True

def iso_multi(para):
    subg,g = para
    if nx.is_isomorphic(subg,g):
        return 1
    else:
        return 0



def iter_tools(edges,n):
    for es in itertools.combinations(edges,n):
        yield list(es)

if __name__ == '__main__':
    # generate_subgraphs_(5)
    main()
    # three_levels_dis()

    



