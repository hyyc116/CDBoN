#coding:utf-8
from basic_config import *

def build_citation_network(dirpath):

    # index of mag dataset
    file_index = 0
    line_index = 0

    ## record all publication year of papers
    paper_year = defaultdict(int)


    for file in os.listdir(dirpath):
        file_index+=1
        filepath = dirpath[:-1] if dirpath.endswith('/') else dirpath
        filepath=filepath+"/"+file

        for line in open(filepath):
            line_index+=1

            if line_index%100000==0:
                logging.info('==== The {:} th File, total progress:{:}, length of paper years {:} ====').format(file_index,line_index,len(paper_year.keys()))
                new_lines = []
            
            line = line.strip()
            paper = json.loads(line)

            pid = paper['id']
            year = paper['year']
            paper_year[pid] = year

    open('data/mag/mag_paper_year.json'.format(fieldname),'w').write(json.dumps(paper_year))

    print len(paper_year.keys())

if __name__ == '__main__':
    build_citation_network(sys.argv[1])