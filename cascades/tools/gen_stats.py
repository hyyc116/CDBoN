#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *

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
    kcores=[]

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
        

        diG = nx.DiGraph()
        edges = cc[pid]['edges']
        diG.add_edges_from(edges)

        # if citation cascade is not acyclic graph
        if not nx.is_directed_acyclic_graph(diG):
            continue
        ## DEPTH
        depth=nx.dag_longest_path_length(diG)

        ## k_CORE
        k_core = core_number(diG)
        print k_core


        # cascade_depths.append(depth)
        depth_dict[depth]+=1
        # cascade_sizes.append(len(edges))
        size_depth_dict[len(edges)].append(depth)

        #number of nodes
        cnum_dict[cc[pid]['cnum']]+=1
        cxs.append(cc[pid]['cnum'])
        #number of edges
        enum_dict[cc[pid]['enum']]+=1
        eys.append(cc[pid]['enum'])
        
        dys.append(depth)
        dcxs.append(cc[pid]['cnum'])

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

    
    plot_dict['cxs'] = cxs;
    plot_dict['eys'] = eys;
    plot_dict['dys'] = dys;
    plot_dict['dcx'] = dcxs;
    plot_dict['od_ys'] = od_ys
    plot_dict['id_ys'] = id_ys

    open('data/plot_dict.json','w').write(json.dumps(plot_dict))

if __name__ == '__main__':
    gen_statistics_data(sys.argv[1])