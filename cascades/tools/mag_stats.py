#coding:utf-8
from basic_config import *
'''
    generate distribution data and correlation data
'''


def gen_statistics_data(citation_cascade,paper_year_path):

    ## 每一篇文章的年限
    pid_year = json.loads(open(paper_year_path).read())
    logging.info('Size of papers with year:{:}'.format(len(pid_year.keys())))

    # general indicators
    cc_dict=defaultdict(int)
    cs_dict=defaultdict(int)
    size_depth_dict=defaultdict(list)
    depth_dict=defaultdict(int)
    od_dict = defaultdict(int)
    in_dict = defaultdict(int)

    ##
    plot_dict = {}
    cxs=[]
    eys=[]
    dys=[]
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

    line_index = 0
    for line in open(citation_cascade):
        line = line.strip()
        line_index+=1
        cc = json.loads(line)
        total = len(cc.keys())

        logging.info('line {:} loaded, total: {:}'.format(line_index,total))
        logi = 0

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
                logging.info('progress {:}/{:}, line_index:{:}'.format(logi,total,line_index))
        

            diG = nx.DiGraph()
            edges = cc[pid]['edges']
            diG.add_edges_from(edges)

            # if citation cascade is not acyclic graph
            if not nx.is_directed_acyclic_graph(diG):
                continue

            depth=nx.dag_longest_path_length(diG)
            # cascade_depths.append(depth)
            depth_dict[depth]+=1
            # cascade_sizes.append(len(edges))
            size_depth_dict[len(edges)].append(depth)

            #number of nodes
            cc_dict[cc[pid]['cc']]+=1
            cxs.append(cc[pid]['cc'])
            #number of edges
            cs_dict[cc[pid]['cs']]+=1
            eys.append(cc[pid]['cs'])
        
            dys.append(depth)

            ## year 
            year = pid_year.get(pid,-1)
            print '--------',year
            


            #degree
            outdegree_dict = diG.out_degree()
            # print outdegree_dict
            citing_years = []
            for nid,od in outdegree_dict:
                # od = outdegree_dict[nid]

                if od==0:
                    zero_od_count+=1

                if od>0:

                    print nid,pid_year.get(nid,-1)
                    citing_years.append(pid_year.get(nid,-1))


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
                    direct_count+=1

            if year!=-1:
                citing_age = np.max(citing_years)-year
                citation_ages.append(citing_age)


            od_ys.append(od_count/float(cc[pid]['cc']))
            id_ys.append(id_count/float(cc[pid]['cc']))
            n_owner_years.append(year)
            n_direct_citations.append(direct_count/float(cc[pid]['cc']))
            n_indirect_citations.append(od_count/float(cc[pid]['cc']))

    print 'zero od count:',zero_od_count
    open('data/mag/stats/citation_count.json','w').write(json.dumps(cc_dict))
    open('data/mag/stats/cascade_size.json','w').write(json.dumps(cs_dict))
    open('data/mag/stats/depth.json','w').write(json.dumps(depth_dict))
    open('data/mag/stats/out_degree.json','w').write(json.dumps(od_dict))
    open('data/mag/stats/in_degree.json','w').write(json.dumps(in_dict))

    
    plot_dict['cxs'] = cxs;
    plot_dict['eys'] = eys;
    plot_dict['dys'] = dys;
    plot_dict['od_ys'] = od_ys
    plot_dict['id_ys'] = id_ys
    plot_dict['age'] = citation_ages
    plot_dict['direct'] = n_direct_citations
    plot_dict['indirect'] = n_indirect_citations
    plot_dict['year'] = n_owner_years

    open('data/mag/stats/plot_dict.json','w').write(json.dumps(plot_dict))





if __name__ == '__main__':
    ## data/mag/mag_cs_citation_cascade.json, data/mag/mag_paper_year.json
    gen_statistics_data(sys.argv[1],sys.argv[2])



