#coding:utf-8

from basic_config import *

def build_cascade_from_pid_refs(pid_ref_path):

    logging.info("build cascade from {:} .".format(pid_ref_path))

    pid_citations = defaultdict(list)
    progress = 0
    for line in open(pid_ref_path):

        progress+=1

        if progress%10000000==0:
            logging.info('reading %d citation relations....' % progress)

        line = line.strip()
        citing_id,pid = line.split(",")

        pid_citations[pid].append(citing_id)

    pids = pid_citations.keys()

    ## 记录每篇论文的引用次数用于分高中低
    citnum_list = []

    length = len(pids)
    logging.info('{:} papers has citations with {} citation relations, start to build cascade ...'.format(length,progress))
    progress = 0
    saved_path = 'data/mag_cascade.txt'
    os.remove(saved_path) if os.path.exists(saved_path) else None

    outfile = open(saved_path,'w+')
    citation_cascade = defaultdict(list)
    total_num = 0
    for pid in pids:
        progress+=1

        if progress%1000000==0:
            total_num += len(citation_cascade.keys())
            outfile.write(json.dumps(citation_cascade)+'\n')
            logging.info('Building progress {:}/{:}, {:} citation cascades saved to {:}...'.format(progress,length,total_num,saved_path))
            citation_cascade = defaultdict(list)

        citing_list = set(pid_citations.get(pid,[]))

        if len(citing_list)==0:
            continue

        citnum_list.append(str(len(citing_list)))

        for cit in citing_list:

            if pid == cit:
                continue

            citation_cascade[pid].append([cit,pid])

            ## if cit has no citation
            cit_citation_list = set(pid_citations.get(cit,[]))

            if len(cit_citation_list)==0:
                continue

            for inter_pid in (citing_list & cit_citation_list):
                citation_cascade[pid].append([inter_pid,cit])

    outfile.write(json.dumps(citation_cascade)+"\n")

    total_num+=len(citation_cascade)
    logging.info("{:} citation cascade has been build, and saved to {:}".format(total_num,saved_path))

    open('data/citnum_list.txt','w').write('\n'.join(citnum_list))


if __name__ == '__main__':
    build_cascade_from_pid_refs(sys.argv[1])
