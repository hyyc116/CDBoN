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


def test_motif(citation_cascade):
    cc = json.loads(open(citation_cascade).read())
    for pid in cc.keys():

        count = cc[pid]['cnum']

        if count>100:
            edges = cc[pid]['edges']
            for e in edges:
                print e[0],e[1]

            break


def iter_tools(edges,n):
    for es in itertools.combinations(edges,n):
        yield list(es)