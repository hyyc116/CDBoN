#coding:utf-8

from basic_config import *


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
def build_cascades(citation_network):
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
        logging.info('Number of citations:{:}'.format(len(citing_pids)))
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

    open('data/aminer_citation_cascade.json','w').write(json.dumps(cn))
    logging.info('citation cascade saved to data/aminer_citation_cascade.json.')

def cascade_size_distribution(citation_cascade):
    cc = json.loads(open(citation_cascade).read())
    logging.info('data loaded...')
    cnum_dict=defaultdict(int)
    enum_dict=defaultdict(int)
    cxs=[]
    eys=[]
    for pid in cc.keys():
        cnum_dict[cc[pid]['cnum']]+=1
        cxs.append(cc[pid]['cnum'])
        enum_dict[cc[pid]['enum']]+=1
        eys.append(cc[pid]['enum'])

    logging.info('plot data...')
    num = len(plt.get_fignums())
    plt.figure(num)
    fig,axes = plt.subplots(1,3,figsize=(15,5))
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

    ax2 = axes[1]
    for num in sorted(enum_dict.keys()):
        xs.append(num)
        ys.append(enum_dict[num])

    ax2.plot(xs,ys,'o',fillstyle='none')
    ax2.set_title('Cascade Size Distribution')
    ax2.set_xlabel('Cascade Size')
    ax2.set_ylabel('Number')
    ax2.set_yscale('log')
    ax2.set_xscale('log')

    # plt.tight_layout()
    # plt.savefig('pdf/cascade_size_dis.pdf',dpi=300)
    # logging.info('figures saved to pdf/cascade_size_dis.pdf.')

    # num = len(plt.get_fignums())
    # plt.figure(num)

    # fig,ax3 = plt.subplots(figsize=(5,5))
    ax3=axes[2]
    bucket_dict=defaultdict(list)
    for i,x in enumerate(cxs):
        bucket_dict[x].append(eys[i]/float(x))

    xs = []
    ys = []
    all_data=[]
    sorted_keys = sorted(bucket_dict.keys())
    for d in sorted_keys:
        # print '===',d
        xs.append(d)
        ys.append(np.mean(bucket_dict[d]))
        all_data.append(bucket_dict[d])

    logging.info('Number of boxes: {:}'.format(len(sorted_keys)))
    # print all_data
    ax3.set_xlabel('Citation Count')
    ax3.set_ylabel('Mean of Cascade Size / Citation Count')
    ax3.set_xscale('log')
    # ax.set_ylim(1,1000)
    # ax.set_xlim(0,11)
    ax3.scatter(xs,ys,marker='.')
    # ax3.boxplot(all_data,showfliers=False)
    # ax3.set_xticks([i+1 for i in np.arange(len(bucket_dict.keys()),500)])
    # ax3.set_xticklabels([sorted_keys[i] for i in np.arange(len(bucket_dict.keys()),500)])
    ax3.set_title('Cascade Size vs. Citation Count')


    plt.tight_layout()
    plt.savefig('pdf/cascade_size_dis.pdf',dpi=300)
    logging.info('figures saved to pdf/cascade_size_dis.pdf.')

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

    ax1.plot(xs,ys,marker='o',fillstyle='none')
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
    ax2.set_xscale('log')

    plt.tight_layout()
    plt.savefig('pdf/cascade_depth.pdf',dpi=300)
    logging.info('figure saved to pdf/cascade_depth.pdf.')

#cascade subgraph
def cascade_subgraph(graph,n_max):
    all_nodes = graph.nodes()
    if len(all_nodes)<n_max:
        n_max = len(all_nodes)

    for N in range(2,n_max+1):
        print N
        nodes_list = []
        for node_set in combinations(all_nodes,N):
            # print node_set
            nodes_list.append([n for n in node_set])

        for i,nodes in enumerate(nodes_list):
            h = graph.subgraph(nodes)
            connected = nx.is_weakly_connected(h)
            if connected:
                yield N,h.edges()
            # plt.savefig('{:}.png'.format(name))

def subgraph_statistics(citation_cascade):
    cc = json.loads(open(citation_cascade).read())
    logging.info('data loaded...')
    logi = 0
    pid_subgraph=defaultdict(dict)
    for pid in cc.keys():
        logi+=1
        if logi%10000==1:
            logging.info('progress {:}'.format(logi))
        diG = nx.DiGraph()
        edges = cc[pid]['edges']
        diG.add_edges_from(edges)
        for n,subgraph in cascade_subgraph(diG,10):
            sub_list = pid_subgraph[pid].get(n,[])
            sub_list.append(subgraph)
            pid_subgraph[pid][n]=sub_list


    open('data/subgraphs.json','w').write(json.dumps(pid_subgraph))



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
    



def main():
    # build_citation_network(sys.argv[1])
    # build_cascades(sys.argv[1])
    label = sys.argv[1]
    if label=='cascade_size':
        cascade_size_distribution(sys.argv[2])
    elif label == 'cascade_depth':
        cascade_depth_distribution(sys.argv[2])
    elif label =='build_cascade':
        build_cascade(sys.argv[2])
    elif label =='subgraphs':
        subgraph_statistics(sys.argv[2])


if __name__ == '__main__':
    # graph = nx.DiGraph()
    # edges = [(2,1),(3,1),(3,2),(4,2),(4,3),(4,1),(5,1),(5,4),(6,3),(7,4),(8,7)]
    # graph.add_edges_from(edges)

    # for i in cascade_subgraph(graph,10):
    #     print i

    main()

    



