#coding:utf-8
import sys
import json
from collections import defaultdict
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
    
    fig,axes = plt.subplots(5,2)
    ax_index=0
    for pid in top_dict.keys():
        ax = axes[ax_index/5,ax_index%5-1]
        cited_dict = top_dict[pid]
        pid_year = cited_dict['year']
        citation_year_list = [int(i.split(',')[1]) for i in cited_dict['citations']]
        year_counter = Counter(citation_year_list)
        years=[int(pid_year)]
        counts=[1]
        for year,count in sorted(year_counter.keys()):
            years.append(year)
            counts.append(count)

        ax.plot(years,counts)
        ax.set_title(pid)

        ax_index+=1

    plt.tight_layout()
    plt.savefig('top_10_citation.png',dpi=300)

    

if __name__ == '__main__':
    # build_citation_network(sys.argv[1])
    cal_friction(sys.argv[1],int(sys.argv[2]))