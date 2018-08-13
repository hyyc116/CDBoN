#coding:utf-8
from basic_config import *

# fetch paper ids of specific field
def field_papers(dirpath,field,keywords):
    file_index = 0
    line_index = 0
    paper_ids = []
    for file in os.listdir(dirpath):
        file_index+=1
        filepath = dirpath[:-1] if dirpath.endswith('/') else dirpath
        filepath=filepath+"/"+file
        if not filepath.endswith('txt'):
            continue

        # citation_network=defaultdict(list)
        # paper_year = defaultdict(int)
        for line in open(filepath):
            line_index+=1

            if line_index%10000==0:
                logging.info('The {:} th File:{:}, total progress:{:}, {:} papers in CS'.format(file_index,filepath,line_index,len(paper_ids)))

            line = line.strip()
            paper = json.loads(line) 
            if paper.get('lang','-1')!='en':
                continue

            year = paper.get('year',-1)

            if year==-1:
                continue

            if year>2016 or year<1970:
                continue

            fos = paper.get('fos',-1)
            if fos!=-1:
                fos = ','.join(fos).lower()
                if keywords in fos:
                    paper_ids.append(paper['id'])

    open('data/{:}_papers.txt'.format(field),'w').write('\n'.join(paper_ids))

    logging.info('----total number of cs papers: {:} ..'.format(len(paper_ids)))
    # delete variables
    del paper_ids

    return 'data/{:}_papers.txt'.format(field)


## build citation network related to specific fields
def build_citation_network(dirpath,field_path,fieldname):

    # load pids of field
    paper_pids = set([paperid.strip() for paperid in open(field_path)])
    
    # index of mag dataset
    file_index = 0
    line_index = 0

    ## save the data related to this field
    new_lines = []

    # recording the pids saved
    already_in  = set([])

    ## num of paper of which citation is bigger than 0.
    n_count_papers = 0

    ## total number in this field
    all_paper_count=0

    ## num_of_edges
    num_of_edges = 0
    
    ## citation network finally saved
    citation_network=defaultdict(list)

    ## record all publication year of papers
    paper_year = defaultdict(int)


    for file in os.listdir(dirpath):
        file_index+=1
        filepath = dirpath[:-1] if dirpath.endswith('/') else dirpath
        filepath=filepath+"/"+file

        for line in open(filepath):
            line_index+=1

            if line_index%100000==0:
                logging.info('==== The {:} th File, total progress:{:} ===='.format(file_index,line_index))
                logging.info('---- length of already_in {:}, size of citation count >0 : {:}/{:}, length of citation network:{:}, number of edges:{:} ----'.format(len(already_in),n_count_papers,all_paper_count,len(citation_network.keys()),num_of_edges))
                new_lines = []
            
            line = line.strip()
            paper = json.loads(line)

            pid = paper['id']
            year = paper['year']
            paper_year[pid] = year

            # one paper is belong to this field and has not been recorded
            if pid in paper_pids and pid not in already_in:
                new_lines.append(line)
                already_in.add(pid)

                all_paper_count+=1

                ## record n_citatin>0
                if paper.get('n_citation',0)>0:
                    n_count_papers+=1

            ## references
            if 'references' in paper.keys():

                for cited_pid in paper['references']:
                    # If this paper is in paper_ids
                    if cited_pid in paper_pids:
                        # update the citation network if cited_pid
                        citation_network[cited_pid].append(pid)

                        num_of_edges+=1

                        ##  if this paper not recorded, record whatever its filed is
                        if pid not in already_in:
                            already_in.add(pid)
                            new_lines.append(line)

        open('data/mag/mag_{:}_papers.txt'.format(fieldname),'a').write('\n'.join(new_lines))
        
    open('data/mag/mag_{:}_citation_network.json'.format(fieldname),'w').write(json.dumps(citation_network))
    open('data/mag/mag_{:}_paper_year.json'.format(fieldname),'w').write(json.dumps(paper_year))
    logging.info('save json, file index: {:}, line_index:{:}'.format(file_index,line_index))
    logging.info('---- length of already_in {:}, size of citation count >0 : {:}/{:}, length of citation network:{:}, number of edges:{:} ----'.format(len(already_in),n_count_papers,all_paper_count,len(citation_network.keys()),num_of_edges))

    #delete variable
    del citation_network
    del paper_year
    del new_lines

    return 'data/mag/mag_{:}_citation_network.json'.format(fieldname)

### stats all nodes in already built citation network
def all_nodes_in_citation_network(citation_network,fieldname):

    cn = json.loads(open(citation_network).read())
    total = len(cn.keys())
    logging.info('total number of papers:{:}'.format(total))

    all_nodes = []
    for pid in cn.keys():
        all_nodes.append(pid)
        all_nodes.extend(cn[pid])

    all_nodes  = list(set(all_nodes))
    logging.info('total nodes:{:}'.format(len(all_nodes)))

    open('data/mag/{:}_all_nodes.txt'.format(fieldname),'w').write('\n'.join(all_nodes))

    del all_nodes

    return 'data/mag/{:}_all_nodes.txt'.format(fieldname)

## to build the citation cascade, the citations of papers that not in a filed is also useful.
def build_cc_of_all_nodes(dirpath,all_nodes,fieldname):

    # load 
    paper_pids = set([paperid.strip() for paperid in open(all_nodes)])
    file_index = 0
    line_index = 0
    citation_network=defaultdict(list)

    for file in os.listdir(dirpath):
        file_index+=1
        filepath = dirpath[:-1] if dirpath.endswith('/') else dirpath
        filepath=filepath+"/"+file

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

    open('data/mag/mag_{:}_all_citation_network.json'.format(fieldname),'w').write(json.dumps(citation_network))

    del all_nodes

    return 'data/mag/mag_{:}_all_citation_network.json'.format(fieldname)


## 根据citation network构建cascade
def build_mag_cascade(citation_network,cs_papers,fieldname):

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
            open('data/mag/mag_{:}_citation_cascade.json'.format(fieldname),'a').write(json.dumps(citation_cascade)+"\n") 

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

    open('data/mag/mag_{:}_citation_cascade.json'.format(fieldname),'a').write(json.dumps(citation_cascade)+"\n")

    del citation_cascade

    logging.info('Done, total edges:{:}'.format(num_of_edges))


def build_cascade_of_a_filed(dirpath,keywords='computer science',fieldname='cs'):


    ## filter out paper ids in specific field
    field_path = field_papers(dirpath,fieldname,keywords)
    # first around build basic citation network
    citation_network = build_citation_network(dirpath,field_path,fieldname)
    ## get all nodes in citation network
    all_nodes  = all_nodes_in_citation_network(citation_network,fieldname)
    ## citation citation network of all nodes
    all_nodes_citation_network = build_cc_of_all_nodes(dirpath,all_nodes,fieldname)
    ## build citation cascade
    build_mag_cascade(all_nodes_citation_network,field_path,fieldname)




if __name__ == '__main__':
    build_cascade_of_a_filed(sys.argv[1])
