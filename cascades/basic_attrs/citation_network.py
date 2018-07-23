#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *


def build_cc(path):
    ref_dict=defaultdict(dict)
    data = json.loads(open(path).read())
    reflist = data['RECORDS']
    ref_size = len(reflist)
    logging.info('loading aminer citation_reference.json, size: {:}'.format(ref_size))
    count=0
    self_citation_count=0

    edge_dict = defaultdict(list)
    node_dict = defaultdict(int)

    for ref in reflist:
        count+=1
        if count%10000==1:
            logging.info("progress --  {:}/{:}".format(count,ref_size))
        pid = ref['cpid']
        pid_year = ref['cpid_year']
        citing_pid = ref['pid']
        citing_pid_year = ref['pid_year']

        # 如果是自引，那么不要这一条记录
        if citing_pid == pid:
            self_citation_count+=1
            continue

        ## ∏
        # edge_list.append([citing_pid,pid])
        edge_dict[citing_pid].append(pid)

        node_dict[citing_pid] = len(node_dict.keys())

        node_dict[pid] = len(node_dict.keys())

    # node_dict.append(pid)
    out_maxtrix(edge_dict,node_dict,2000)
    out_maxtrix(edge_dict,node_dict,20000)

    out_maxtrix(edge_dict,node_dict,100000)


    logging.info('done')


def out_maxtrix(edge_dict,node_dict,N):
    # size = len(node_dict.keys())
    lines = []
    logging.info('node size:{:}'.format(N))
    for node in sortd(edge_dict.keys())[:N]:
        ## 每一个node输出一行
        line = [0]*len(size)

        for n2 in edge_dict.get(node,[]):

            pos = node_dict[n2]

            if pos >=N:
                continue

            line[pos] = 1

        lines.append(','.join([str(i) for i in line]))

    open('cc_{:}.txt'.format(N),'w').write('\n'.join(lines))



if __name__ == '__main__':
    
    build_cc(sys.argv[1],sys.argv[2])






