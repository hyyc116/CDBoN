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
        removed_links = []
        for pid in cc.keys():
            diG = nx.DiGraph()
            edges = cc[pid]['edges']
            diG.add_edges_from(edges)

            logi+=1
            if logi%10000==1:
                logging.info('progress {:}/{:}...'.format(logi,total))

            # if citation cascade is not acyclic graph
            if not nx.is_directed_acyclic_graph(diG):
                continue

            print '==== PRE NUM OF EDGES:',len(edges)

            outdegree_dict = diG.out_degree()

            ## 对于每一个节点来讲
            for nid,od in outdegree_dict:

                ## 出度为0的为owner
                if od==0:
                    continue

                #如果出度是大于1的，那么将直接citation link给去掉
                if od >1:
                    removed_links.append((nid,pid))

                ## 入度
                ind = diG.in_degree(nid)
                pid_cpid_obj[pid][nid]['od'] = od
                pid_cpid_obj[pid][nid]['id'] = ind

            ## 将直接连接删除，那么这个图边的相对较小
            if len(removed_links)>0:
                diG.remove_edges_from(removed_links)
            print 'REMOVED LINKS LEN:',len(removed_links)
            print '==== LATER NUM OF EDGES:',len(edges)
            for nid in diG.nodes():
                print nid
                depth = np.mean([len(l)-1 for l in nx.all_simple_paths(diG,nid,pid)])
                pid_cpid_obj[pid][nid]['depth'] = depth

        open(field_path,'a').write(json.dumps(pid_cpid_obj)+'\n')

if __name__ == '__main__':
    ## /public/data/Aminer_MAG/MAG/txt/ , data/mag/all_nodes.txt
    # gen_all_nodes_objs(sys.argv[1],sys.argv[2])

    # generate the cascade attrs' data
    cascade_attrs(sys.argv[1])

    # dig =nx.DiGraph()
    # dig.add_edges_from([(2,1),(3,1),(2,3),(4,2),(4,3),(5,4),(4,1)])
    # for l in nx.shortest_simple_paths(dig,5,1):
        # print l

