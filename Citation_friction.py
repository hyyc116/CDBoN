#coding:utf-8
import sys
import json
from collections import defaultdict
def build_citation_network(path):
    ref_dict=defaultdict(dict)
    data = json.loads(open(path).read())
    reflist = data['RECORDS']
    print 'Size of reference', len(reflist)
    count=0
    for ref in reflist:
        count+=1
        if count%1000==1:
            print count
        pid = ref['cpid']
        pid_year = ref['cpid_year']
        cited_pid = ref['pid']
        cited_pid_year = ref['pid_year']

        cited_dict = ref_dict.get(cited_pid,{})
        cited_dict['pid'] = cited_pid
        cited_dict['year'] = cited_pid_year
        citation_list = cited_dict.get('citations',[])
        citation_list.append('{:},{:}'.format(pid,pid_year))
        cited_dict['citations']=citation_list
        ref_dict[cited_pid] = cited_dict

    open('data/aminer_citation_dict.json','w').write(json.dumps(ref_dict))
    print 'done'

def cal_friction(citation_network_path,N):
    data = json.loads(open(citation_network_path).read())
    top_dict = {}
    for k,v in sorted(data.items(),key=x:len(x[1][citations]),reverse=True)[:N]:
        top_dict[k] = v

    open('data/aminer_top_{:}.json'.format(N),'w').write(top_dict)
    

    

if __name__ == '__main__':
    # build_citation_network(sys.argv[1])
    cal_friction(sys.argv[1],int(sys.argv[2]))