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


if __name__ == '__main__':
    build_reference_network(sys.argv[1])

