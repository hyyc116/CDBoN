#coding:utf-8
from para_config import *

#given the citation network json file, return the citation number distribution json file before year n
def citation_count_json(citation_network_path,N):
    data = json.loads(open(citation_network_path).read())
    citation_num_list = [] 
    for k in data.keys():
        if data[k]['year']>N:
            continue
        citation_num_list.append(len(data[k]['citations']))

    num_counter = Counter(citation_num_list)

    filename = '{:}/{:}_{:}_citation_num_dict_b{:}.json'.format(DATADIR,PROGRAM_ID,PREFIX,N)

    open(filename,'w').write(json.dumps(num_counter))

    print 'save citation num before {:} to {:}'.format(N,filename)