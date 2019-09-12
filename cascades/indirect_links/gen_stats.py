#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *

def gen_statistics_data(citation_cascade,paper_year_path):

    cc = {}

    for line in open(citation_cascade):
        cc.update(json.loads(line.strip()))


    pid_year = json.loads(open(paper_year_path).read())

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
    ## 时间长度
    citation_ages = []
    ## 直接引文的数量
    n_direct_citations = []
    ## 间接引文数量
    n_indirect_citations = []
    # owner发布时间, aminer citation cascade中有year , mag 需要mag_paper_year.json
    n_owner_years = []

    zero_od_count=0
    for pid in cc.keys():

        #out-degree count
        od_count=0
        #in-degree count
        id_count=0
        ## direct count 
        direct_count = 0

        #progress 
        logi+=1
        if logi%10000==1:
            logging.info('progress {:}'.format(logi))
        

        diG = nx.DiGraph()
        edges = cc[pid]
        diG.add_edges_from(edges)

        nodes = list(diG.nodes)

        # if citation cascade is not acyclic graph
        if not nx.is_directed_acyclic_graph(diG):
            continue

        ## DEPTH
        depth=nx.dag_longest_path_length(diG)

        year = int(pid_year[pid])

        n_owner_years.append(year) 

        ## citing age
        citing_age = np.max([int(pid_year[p]) for p in nodes])-year

        # print year,citing_age    
        citation_ages.append(citing_age)   

        # cascade_depths.append(depth)
        depth_dict[depth]+=1
        # cascade_sizes.append(len(edges))
        size_depth_dict[len(edges)].append(depth)

        #number of nodes
        cnum_dict[len(nodes)-1]+=1
        cxs.append(len(nodes)-1)
        #number of edges
        enum_dict[len(edges)]+=1
        eys.append(len(edges))
        
        dys.append(depth)
        dcxs.append(len(nodes)-1)

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
            elif od ==1:
                ##如果出度等于1， 就是直接引文
                direct_count +=1

        od_ys.append(od_count/float(len(nodes)-1))
        id_ys.append(id_count/float(len(nodes)-1))

        ## od 就是indirect  
        n_direct_citations.append(direct_count/float(len(nodes)-1))
        n_indirect_citations.append(od_count/float(len(nodes)-1))




        #centrality
        # degree centrality
        # centrality_dict['indegree'].extend(nx.in_degree_centrality(diG).values())
        # centrality_dict['outdegree'].extend(nx.out_degree_centrality(diG).values())
        # centrality_dict['closeness'].extend(nx.closeness_centrality(diG).values())
        # centrality_dict['betweenness'].extend(nx.betweenness_centrality(diG).values())
        # # centrality_dict['eigenvector'].extend(nx.eigenvector_centrality(diG).values())
        # centrality_dict['katz'].extend(nx.katz_centrality(diG).values())
        # centrality_dict['assortativity'].append(nx.degree_assortativity_coefficient(diG))




    print 'zero od count:',zero_od_count
    open('data/nodes_size.json','w').write(json.dumps(cnum_dict))
    open('data/cascade_size.json','w').write(json.dumps(enum_dict))
    open('data/depth.json','w').write(json.dumps(depth_dict))
    open('data/out_degree.json','w').write(json.dumps(od_dict))
    open('data/in_degree.json','w').write(json.dumps(in_dict))
    open('data/centrality.json','w').write(json.dumps(centrality_dict))

    
    plot_dict['cxs'] = cxs
    plot_dict['eys'] = eys
    plot_dict['dys'] = dys
    plot_dict['dcx'] = dcxs
    plot_dict['od_ys'] = od_ys
    plot_dict['id_ys'] = id_ys
    plot_dict['age'] = citation_ages
    plot_dict['direct'] = n_direct_citations
    plot_dict['indirect'] = n_indirect_citations
    plot_dict['year'] = n_owner_years

    open('data/plot_dict.json','w').write(json.dumps(plot_dict))

if __name__ == '__main__':
    gen_statistics_data(sys.argv[1])