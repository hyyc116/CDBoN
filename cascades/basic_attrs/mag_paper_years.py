#coding:utf-8
from basic_config import *
import beautifulsoup as bs

def build_citation_network(dirpath):

    # index of mag dataset
    file_index = 0
    line_index = 0

    ## record all publication year of papers
    paper_year = defaultdict(int)

    year_filepath = 'data/mag/mag_paper_year.txt'
    if os.path.exists(year_filepath):
        os.remove(year_filepath)

    for file in os.listdir(dirpath):
        file_index+=1
        filepath = dirpath[:-1] if dirpath.endswith('/') else dirpath
        filepath=filepath+"/"+file

        for line in open(filepath):
            line_index+=1

            if line_index%100000==0:
                logging.info('==== The {:} th File, total progress:{:}, length of paper years {:} ===='.format(file_index,line_index,len(paper_year.keys())))
                open(year_filepath,'a').write(json.dumps(paper_year)+'\n')
                paper_year = defaultdict(int)

            
            line = line.strip()
            paper = json.loads(line)

            pid = paper['id']
            year = paper['year']
            paper_year[pid] = year

    open(year_filepath,'a').write(json.dumps(paper_year)+'\n')

    print len(paper_year.keys())

if __name__ == '__main__':
    build_citation_network(sys.argv[1])