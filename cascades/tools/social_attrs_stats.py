#coding:utf-8
'''
@author: hy@tTt
对于node的社会属性例如field， topic similarity, node importance的分布进行计算

'''
from basic_config import *

def gen_all_nodes_objs(dirpath,all_nodes_path):

    ## load the fos mapping
    fos_dict = defaultdict(list)
    for line in open('tools/OCDE_fos.txt'):
        line= line.strip()
        top,second,content = line.split('\t')

        fos_dict[top].append([second,content])

    ## load the datas related
    all_nodes = set([i.strip() for i in open(all_nodes_path)])

    # index of mag dataset
    file_index = 0
    line_index = 0

    ## record all publication year of papers
    paper_obj = defaultdict(dict)

    field_path = 'data/mag/mag_all_nodes_paper_objs.txt'
    if os.path.exists(field_path):
        os.remove(field_path)

    for file in os.listdir(dirpath):
        file_index+=1
        filepath = dirpath[:-1] if dirpath.endswith('/') else dirpath
        filepath=filepath+"/"+file

        for line in open(filepath):
            line_index+=1

            if line_index%100000==0:
                logging.info('==== The {:} th File, total progress:{:}, length of paper years {:} ===='.format(file_index,line_index,len(paper_obj.keys())))
                open(field_path,'a').write(json.dumps(paper_obj)+'\n')
                paper_obj = defaultdict(dict)

            
            line = line.strip()
            paper = json.loads(line)

            pid = paper['id']
            # 如果不在 就省略
            if pid not in all_nodes:
                continue

            pyear = paper.get('year','-1')
            doctype = paper.get('doc_type','-1')
            fos = paper.get('fos','-1')
            n_citation = paper.get('n_citation','-1')

            normed_fos = '-1'
            if fos!='-1':
                normed_fos=[]
                for f in fos:
                    for t in fos_dict.keys():
                        for s in fos_dict[t]:
                            if f.lower() in s[1].lower():
                                normed_fos.append([t,s[0]])

                if len(normed_fos)==0:
                    normed_fos='-1'

            obj={}
            obj['id']=pid
            obj['year'] = pyear
            obj['dt'] = doctype
            obj['fos'] = fos
            obj['n_fos'] = normed_fos
            obj['n_citation'] = n_citation

            paper_obj[pid] = obj

    open(field_path,'a').write(json.dumps(paper_obj)+'\n')

    print len(paper_obj.keys())

## 对每一个citation cascade中的每一个节点的距离，以及属性进行整合
def cascade_attrs(citation_cascade):

    field_path = 'data/mag/mag_cs_cascade_attrs.txt'
    if os.path.exists(field_path):
        os.remove(field_path)
    line_index=0
    for line in open(citation_cascade):
        line = line.strip()
        line_index+=1
        cc = json.loads(line)
        total = len(cc.keys())
        logging.info('line {:} loaded, total: {:}'.format(line_index,total))
        logi = 0
        pid_cpid_obj=defaultdict(lambda: defaultdict(dict))
        for pid in cc.keys():
            diG = nx.DiGraph()
            edges = cc[pid]['edges']
            diG.add_edges_from(edges)
            # edge_dict = _edge_dict(edges)
            logi+=1

            if logi%1000==1:
                logging.info('progress {:}/{:}...'.format(logi,total))

            # if citation cascade is not acyclic graph
            if not nx.is_directed_acyclic_graph(diG):
                continue

            # print '==== PRE NUM OF EDGES:',len(edges)
            # print '==== PRE NODES SIZE:', len(diG.nodes())

            outdegree_dict = diG.out_degree()
            # removed_links = []

            read_index=0
            ## 对于每一个节点来讲
            for nid,od in outdegree_dict:
                read_index+=1
                if len(edges)>100:
                    if read_index%10==1:
                        logging.info('edges of {:} is {:}, {:}/{:}'.format(pid,len(edges),read_index,len(edges)))

                ## 出度为0的为owner
                if od==0:
                    continue

                #如果出度是大于1的，那么将直接citation link给去掉
                # if od >1:
                    # removed_links.append([nid,pid])

                ## 入度
                ind = diG.in_degree(nid)
                pid_cpid_obj[pid][nid]['od'] = od
                pid_cpid_obj[pid][nid]['id'] = ind

                depth = _depth_of_node(nid,diG,edges)
                
                pid_cpid_obj[pid][nid]['depth'] = depth

            # print len(edges-removed_links)
            ## 将直接连接删除，那么这个图边的相对较小
            # if len(removed_links)>0:
                # print removed_links
                # diG.remove_edges_from(removed_links)

            # print 'REMOVED LINKS LEN:',len(removed_links)
            # print '==== LATER NUM OF EDGES:',len(diG.edges())
            # print '==== LATER NODES SIZE:',len(diG.nodes())
            # later_edge_size = len(diG.edges())
            # for nid in diG.nodes():
                # if nid==pid:
                    # continue
                # depth = nx.shortest_path_length(diG,nid,pid)
                # pid_cpid_obj[pid][nid]['depth'] = depth

        open(field_path,'a').write(json.dumps(pid_cpid_obj)+'\n')

def _edge_dict(edges):
    edge_dict = defaultdict(list)
    for edge in edges:
        edge_dict[edge[0]].append(edge[1])

    return edge_dict

def _depth_of_node(nid,dig,edges):
    nodes = set([e for e in nx.dfs_preorder_nodes(dig,nid)])
    edge_list = []
    for e in edges:
        if e[0] in nodes and e[1] in nodes:
            edge_list.append(e)

    new_dig = nx.DiGraph()
    new_dig.add_edges_from(edge_list)
    depth = nx.dag_longest_path_length(new_dig)
    return depth


if __name__ == '__main__':
    ## /public/data/Aminer_MAG/MAG/txt/ , data/mag/all_nodes.txt
    # gen_all_nodes_objs(sys.argv[1],sys.argv[2])

    # generate the cascade attrs' data
    cascade_attrs(sys.argv[1])
    # edges = [(2,1),(3,1),(2,3),(4,2),(4,3),(5,4),(4,1),(5,1),(5,3),(6,5),(6,4),(6,1)]
    # edge_dict = defaultdict(list)
    # for edge in edges:
    #     edge_dict[edge[0]].append(edge[1])

    # dig =nx.DiGraph()
    # dig.add_edges_from(edges)
    # print nx.dfs_predecessors(dig,6)
    # print nx.dfs_successors(dig,6)
    # print [e for e in nx.dfs_preorder_nodes(dig,6)]
    # print [e for e in nx.dfs_postorder_nodes(dig,6)]
    # print [e for e in nx.bfs_edges(dig,6)]
    # print nx.bfs_edges(dig,4)
    # print nx.bfs_edges(dig,3)

    # for node in dig.nodes():
    #     if node!=1:
    #         node_edge_list = []
    #         pre(node,edge_dict,node_edge_list)
    #         node_edge_list = list(set(node_edge_list))
    #         new_dig = nx.DiGraph(node_edge_list)
    #         depth = nx.dag_longest_path_length(new_dig)
    #         print node,'==',node_edge_list,'==',depth

    # print dig
    # dig.remove_edges_from([(2,1)])
    # print dig.edges()
    # for l in nx.shortest_simple_paths(dig,5,1):
    #     print l

