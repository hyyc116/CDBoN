#coding:utf-8
from basic_config import *

def build_citation_network(dirpath,field_path):

    # load 
    paper_pids = set([paperid.strip() for paperid in open(field_path)])
    
    file_index = 0
    line_index = 0

    new_lines = []
    already_in  = set([])

    n_count_papers = 0
    all_paper_count=0
    
    citation_network=defaultdict(list)
    for file in os.listdir(dirpath):
        file_index+=1
        filepath = dirpath[:-1] if dirpath.endswith('/') else dirpath
        filepath=filepath+"/"+file

        paper_year = defaultdict(int)
        for line in open(filepath):
            line_index+=1

            if line_index%100000==0:
                logging.info('The {:} th File, total progress:{:}, length of already_in {:}, size of citation count >1 : {:}/{:}, length of citation network:{:}'.format(file_index,line_index,len(already_in),n_count_papers,all_paper_count,len(citation_network.keys())))
                new_lines = []
            
            line = line.strip()
            paper = json.loads(line)

            pid = paper['id']
            year = paper['year']
            paper_year[pid] = year

            #如果这篇论文是cs,并且没有被记录过
            if pid in paper_pids and pid not in already_in:
                new_lines.append(line)
                already_in.add(pid)
                all_paper_count+=1

                ## 计数 cs引文数量大于1的文章数量
                if paper.get('n_citation',0)>0:
                    n_count_papers+=1

            ## 参考文献
            if 'references' in paper.keys():

                for cpid in paper['references']:
                    # 如果这篇被引文献是CS
                    if cpid in paper_pids:
                        citation_network[cpid].append(pid)
                        ## 记录这篇文章，如果没有记录过
                        if pid not in already_in:
                            already_in.add(pid)
                            new_lines.append(line)

        open('data/mag/mag_cs_papers.txt','a').write('\n'.join(new_lines))
        
    # open('data/mag/mag_cs_papers.txt','a').write('\n'.join(new_lines))
    open('data/mag/mag_citation_network.json','w').write(json.dumps(citation_network))
    open('data/mag/mag_paper_year.json','w').write(json.dumps(paper_year))
    logging.info('save json, file index: {:}, line_index:{:}'.format(file_index,line_index))



def merger_dict(dirpath,prefix,t='list'):
    file_index = 0
    if t =='list':
        merger_dict = defaultdict(list)
    else:
        merger_dict = defaultdict(int)

    for file in os.listdir(dirpath):
        if not file.startswith(prefix):
            continue
        filepath = dirpath[:-1] if dirpath.endswith('/') else dirpath
        filepath=filepath+"/"+file

        file_index+=1

        logging.info('file index : {:}'.format(file_index))

        data = json.loads(open(filepath).read())

        for key in data.keys():
            if t=='list':
                for v in data[key]:
                    merger_dict[key].append(v)
            else:
                merger_dict[key] = data[key]
    if t=='list':
        outpath = 'data/mag_citation_network.json'
    else:
        outpath = 'data/mag_paper_year.json'

    open('outpath','w').write(merger_dict)

    logging.info('writing to {:}'.format(outpath))

def cs_papers(dirpath):
    file_index = 0
    line_index = 0
    paper_ids = []
    for file in os.listdir(dirpath):
        file_index+=1
        filepath = dirpath[:-1] if dirpath.endswith('/') else dirpath
        filepath=filepath+"/"+file
        if not filepath.endswith('txt'):
            continue

        citation_network=defaultdict(list)
        paper_year = defaultdict(int)
        for line in open(filepath):
            line_index+=1

            if line_index%10000==0:
                logging.info('The {:} th File:{:}, total progress:{:}, {:} papers in CS'.format(file_index,filepath,line_index,len(paper_ids)))

            line = line.strip()
            paper = json.loads(line) 
            if paper.get('lang','-1')!='en':
                continue

            fos = paper.get('fos',-1)
            if fos!=-1:
                fos = ','.join(fos).lower()
                if 'computer science' in fos:
                    paper_ids.append(paper['id'])

    open('data/cs_papers.txt','w').write('\n'.join(paper_ids))

### 统计citation network中所有涉及到的所有论文的id
def all_nodes_in_citation_network(citation_network):
    cn = json.loads(open(citation_network).read())
    total = len(cn.keys())
    logging.info('total number of papers:{:}'.format(total))

    all_nodes = []
    for pid in cn.keys():
        all_nodes.append(pid)
        all_nodes.extend(cn[pid])

    all_nodes  = list(set(all_nodes))
    logging.info('total nodes:{:}'.format(len(all_nodes)))

    open('data/mag/all_nodes.txt','w').write('\n'.join(all_nodes))

def build_cc_of_all_nodes(dirpath,all_nodes):

    # load 
    paper_pids = set([paperid.strip() for paperid in open(all_nodes)])
    file_index = 0
    line_index = 0
    citation_network=defaultdict(list)

    for file in os.listdir(dirpath):
        file_index+=1
        filepath = dirpath[:-1] if dirpath.endswith('/') else dirpath
        filepath=filepath+"/"+file

        paper_year = defaultdict(int)
        for line in open(filepath):
            line_index+=1

            if line_index%100000==0:
                logging.info('The {:} th File, total progress:{:}, length of citation network:{:}'.format(file_index,line_index,len(citation_network.keys())))
            
            line = line.strip()
            paper = json.loads(line)

            pid = paper['id']

            if 'references' in paper.keys():
                for cpid in paper['references']:
                    if cpid in paper_pids:
                        citation_network[cpid].append(pid)

    open('data/mag/mag_all_nodes_citation_network.json','w').write(json.dumps(citation_network))



## 根据citation network构建cascade
def build_mag_cascade(citation_network,cs_papers):

    cs_pids = [line.strip() for line in open(cs_papers)]

    cn = json.loads(open(citation_network).read())
    total = len(cs_pids)
    logging.info('total number of papers:{:}'.format(total))
    ## progress index
    progress_index = 0
    ## num of edges
    num_of_edges = 0
    ## cascade
    citation_cascade = defaultdict(dict)

    for pid in cs_pids:
        if progress_index%100000==1:
            logging.info('progress of building cascade:{:}/{:}, number of edges:{:}'.format(progress_index,total,num_of_edges))
            open('data/mag/mag_cs_citation_cascade.json','a').write(json.dumps(citation_cascade)+"\n") 

            citation_cascade = defaultdict(list)

        progress_index+=1

        citing_pids = cn.get(pid,[])

        if len(citing_pids)==0:
            continue

        ## for each paper
        edges = []
        for citing_pid in citing_pids:
            # if errors
            if citing_pid == pid:
                continue

            edges.append([citing_pid,pid])
            num_of_edges+=1

            ## for every citing papers
            citing_citing_pids = cn.get(citing_pid,[])

            inter_citing_pids = set(citing_citing_pids)&set(citing_pids)  
            
            for inter_citing_pid in inter_citing_pids:
                if inter_citing_pid == citing_pid:
                    continue
                
                edges.append([inter_citing_pid,citing_pid])
                num_of_edges+=1

        pid_dict = {}
        pid_dict['cc']=len(citing_pids)
        pid_dict['cs']=len(edges)
        pid_dict['edges'] = edges

        citation_cascade[pid] = pid_dict


    open('data/mag/mag_cs_citation_cascade.json','a').write(json.dumps(citation_cascade)+"\n") 
    logging.info('Done, total edges:{:}'.format(num_of_edges))

## 根据citation network构建cascade
def stats_edges(citation_network,cs_papers):

    cs_pids = [line.strip() for line in open(cs_papers)]

    cn = json.loads(open(citation_network).read())
    total = len(cs_pids)
    logging.info('total number of papers:{:}'.format(total))
    ## progress index
    progress_index = 0
    ## num of edges
    num_of_edges = 0
    ## cascade

    for pid in cs_pids:
        if progress_index%100000==1:
            logging.info('progress of building cascade:{:}/{:}, number of edges:{:}'.format(progress_index,total,num_of_edges))


        progress_index+=1

        citing_pids = cn.get(pid,[])

        if len(citing_pids)==0:
            continue

        ## for each paper
        edges = []
        for citing_pid in citing_pids:
            # if errors
            if citing_pid == pid:
                continue

            edges.append([citing_pid,pid])
            num_of_edges+=1

    logging.info('Done, total edges:{:}'.format(num_of_edges))



if __name__ == '__main__':
    # build_reference_network(sys.argv[1],sys.argv[2])

    # all_nodes_in_citation_network(sys.argv[1])
    # build_cc_of_all_nodes(sys.argv[1],sys.argv[2])
    # build_mag_cascade(sys.argv[1],sys.argv[2])
    stats_edges(sys.argv[1],sys.argv[2])
