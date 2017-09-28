#coding:utf-8
from basic_config import *

def build_reference_network(dirpath,field_path):

    # load 
    paper_pids = set([paperid.strip() for paperid in open(field_path)])
    
    file_index = 0
    line_index = 0

    new_lines = []
    already_in  = set([])

    n_count_papers = 0

    for file in os.listdir(dirpath):
        file_index+=1
        filepath = dirpath[:-1] if dirpath.endswith('/') else dirpath
        filepath=filepath+"/"+file

        citation_network=defaultdict(list)
        paper_year = defaultdict(int)
        for line in open(filepath):
            line_index+=1

            if line_index%100000==0:
                logging.info('The {:} th File:{:}, total progress:{:}, length of already_in {:}, size of citation count >1 : {:}'.format(file_index,filepath,line_index,len(already_in),n_count_papers))
                
                new_lines = []
            
            line = line.strip()
            paper = json.loads(line)

            pid = paper['id']
            year = paper['year']
            paper_year[pid] = year
            if paper.get('n_citation',0)>0:
                n_count_papers+=1



            if pid in paper_pids and pid not in already_in:
                new_lines.append(line)
                already_in.add(pid)


            if 'references' in paper.keys():
                for cpid in paper['references']:
                    if cpid in paper_pids and cpid not in already_in:
                        citation_network[cpid].append(pid)
                        already_in.add(cpid)
                        new_lines.append(line)

        open('data/mag/mag_cs_papers.txt','a').write('\n'.join(new_lines))
        
    logging.info('The {:} th File:{:}, total progress:{:}, length of lines {:}'.format(file_index,filepath,line_index,len(new_lines)))
    open('data/mag/mag_cs_papers.txt','a').write('\n'.join(new_lines))
    open('data/mag/mag_citation_network.json','w').write(json.dumps(citation_network))
    open('data/mag/mag_paper_year.json','w').write(json.dumps(paper_year))
    logging.info('save json, file index: {:}, line_index:{:}'.format(file_index,line_index))


def count_citation(path):
    for line in open(path):
        line = line.strip()




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

if __name__ == '__main__':
    build_reference_network(sys.argv[1],sys.argv[2])
    # merger_dict(sys.argv[1],sys.argv[2],sys.argv[3])
    # cs_papers(sys.argv[1])

