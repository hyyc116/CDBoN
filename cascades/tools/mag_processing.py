#coding:utf-8
from basic_config import *

def build_reference_network(dirpath):

    citation_network=defaultdict(list)
    paper_year = defaultdict(int)
    file_index = 0
    line_index = 0
    for file in os.listdir(dirpath):
        file_index+=1
        filepath = path[:-1] if path.endswith('/') else path+"/"+file
        for line in open(filepath):
            line_index+=1

            if line_index%10000==0:
                logging.info('The {:} th File:{:}, total progress:{:}'.format(file_index,filepath,line_index))


            if line_index%1000000==100000:
                open('data/mag_citation_network.json','w').write(json.dumps(citation_network))
                open('data/mag_paper_year.json','w').write(json.dumps(paper_year))
                logging.info('save json, file index: {:}, line_index:{:}'.format(file_index,line_index))

            line = line.strip()
            paper = json.loads(line)

            pid = paper['id']
            year = paper['year']
            paper_year[pid] = year

            if 'references' in paper.keys():
                for cpid in paper['references']:
                    citation_network[cpid].append(pid)

    open('data/mag_citation_network.json','w').write(json.dumps(citation_network))
    open('data/mag_paper_year.json','w').write(json.dumps(paper_year))
    logging.info('save json, file index: {:}, line_index:{:}'.format(file_index,line_index))


if __name__ == '__main__':
    build_reference_network(sys.argv[1])

