#coding:utf-8
from basic_config import *

def build_reference_network(dirpath):

    
    file_index = 0
    line_index = 0
    for file in os.listdir(dirpath):
        file_index+=1
        filepath = dirpath[:-1] if dirpath.endswith('/') else dirpath
        filepath=filepath+"/"+file

        citation_network=defaultdict(list)
        paper_year = defaultdict(int)
        for line in open(filepath):
            line_index+=1

            if line_index%10000==0:
                logging.info('The {:} th File:{:}, total progress:{:}'.format(file_index,filepath,line_index))

            line = line.strip()
            paper = json.loads(line)

            pid = paper['id']
            year = paper['year']
            paper_year[pid] = year

            if 'references' in paper.keys():
                for cpid in paper['references']:
                    citation_network[cpid].append(pid)

        open('data/mag/mag_citation_network_{:}.json'.format(file_index),'w').write(json.dumps(citation_network))
        open('data/mag/mag_paper_year_{:}.json'.format(file_index),'w').write(json.dumps(paper_year))
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





if __name__ == '__main__':
    # build_reference_network(sys.argv[1])
    merger_dict(sys.argv[1],sys.argv[2],sys.argv[3])

