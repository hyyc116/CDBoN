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
        if count%10000==1:
            print count
        pid = ref['cpid']
        pid_year = ref['cpid_year']
        cited_pid = ref['pid']
        cited_pid_year = ref['pid_year']

        if int(pid_year)<1900 or int(cited_pid_year)<1900 or int(pid_year)<int(cited_pid_year):
            continue

        cited_dict = ref_dict.get(cited_pid,{})
        cited_dict['pid'] = cited_pid
        cited_dict['year'] = cited_pid_year
        citation_list = cited_dict.get('citations',[])
        citation_list.append('{:},{:}'.format(pid,pid_year))
        cited_dict['citations']=citation_list
        ref_dict[cited_pid] = cited_dict

    open('data/aminer_citation_dict.json','w').write(json.dumps(ref_dict))
    print 'done'

def plot_top_N(citation_network_path,N):
    data = json.loads(open(citation_network_path).read())
    top_dict = {}
    for k,v in sorted(data.items(),key= lambda x:len(x[1]['citations']),reverse=True)[:N]:
        top_dict[k] = v

    open('data/aminer_top_{:}.json'.format(N),'w').write(json.dumps(top_dict))
    
    rows = N/5
    fig,axes = plt.subplots(rows,5,figsize=(25,rows*5))
    ax_index=0
    for pid in top_dict.keys():
        ax = axes[ax_index/5,ax_index%5-1]
        cited_dict = top_dict[pid]
        pid_year = cited_dict['year']
        citation_year_list = [int(i.split(',')[1]) for i in cited_dict['citations']]
        year_counter = Counter(citation_year_list)
        # print year_counter
        publish_year = int(pid_year)
        years=[publish_year]
        counts=[1]
        for year in sorted(year_counter.keys()):
            if year<1900:
                continue
            count = year_counter[year]
            years.append(year)
            counts.append(count)

        ax.plot(years,counts)
        ax.set_title(pid)

        ax_index+=1

    plt.tight_layout()
    plt.savefig('top_{:}_citation.png'.format(N),dpi=300)


def frictions(top_n_papers):
    top_dict = json.loads(open(top_n_papers).read())
    N = len(top_dict)
    rows = N/5

    #friction accumulative/delta_t
    num = len(plt.get_fignums())
    plt.figure(num)
    fig,axes = plt.subplots(rows,5,figsize=(25,rows*5))
    ax_index=0
    
    for pid in top_dict.keys():
        ax = axes[ax_index/5,ax_index%5-1]
        cited_dict = top_dict[pid]
        pid_year = cited_dict['year']
        citation_year_list = [int(i.split(',')[1]) for i in cited_dict['citations']]
        year_counter = Counter(citation_year_list)
        # print year_counter
        years=[]
        counts=[]
        accum_count=0
        publish_year = int(pid_year)
        for year in sorted(year_counter.keys()):
            delta_t = (year-publish_year)+0.5
            count = year_counter[year]
            accum_count+=count

            years.append(delta_t)
            counts.append(accum_count/delta_t)

        ax.plot(years,counts)
        ax.set_title(pid)

        ax_index+=1

    plt.tight_layout()
    plt.savefig('top_{:}_accum.png'.format(N),dpi=300)

    #friction delta_t/accumulative
    num = len(plt.get_fignums())
    plt.figure(num)
    fig,axes = plt.subplots(rows,5,figsize=(25,rows*5))
    ax_index=0
    

    for pid in top_dict.keys():
        ax = axes[ax_index/5,ax_index%5-1]
        cited_dict = top_dict[pid]
        pid_year = cited_dict['year']
        citation_year_list = [int(i.split(',')[1]) for i in cited_dict['citations']]
        year_counter = Counter(citation_year_list)
        # print year_counter
        publish_year = int(pid_year)
        years=[]
        counts=[]
        accum_count=0
        for year in sorted(year_counter.keys()):
            delta_t = (year-publish_year)
            count = year_counter[year]
            accum_count+=count

            years.append(delta_t)
            counts.append("{:.5f}".format(delta_t/float(accum_count)))

        ax.plot(years,counts)
        ax.set_title(pid)

        ax_index+=1

    plt.tight_layout()
    plt.savefig('top_{:}_delta.png'.format(N),dpi=300)

    #friction delta_t/count
    num = len(plt.get_fignums())
    plt.figure(num)
    fig,axes = plt.subplots(rows,5,figsize=(25,rows*5))
    ax_index=0
    

    for pid in top_dict.keys():
        ax = axes[ax_index/5,ax_index%5-1]
        cited_dict = top_dict[pid]
        pid_year = cited_dict['year']
        citation_year_list = [int(i.split(',')[1]) for i in cited_dict['citations']]
        year_counter = Counter(citation_year_list)
        # print year_counter
        publish_year = int(pid_year)
        years=[]
        counts=[]
        # accum_count=0
        for year in sorted(year_counter.keys()):
            delta_t = (year-publish_year)
            count = year_counter[year]
            # accum_count+=count

            years.append(delta_t)
            counts.append("{:.5f}".format(delta_t/float(count)))

        ax.plot(years,counts)
        ax.set_title(pid)

        ax_index+=1

    plt.tight_layout()
    plt.savefig('top_{:}_count_delta.png'.format(N),dpi=300)

    
if __name__ == '__main__':
    label = sys.argv[1]
    if label=='citation_network':
        build_citation_network(sys.argv[2])
    elif label =='plot_top':
        plot_top_N(sys.argv[2],int(sys.argv[3]))
    elif label =='friction':
        frictions(sys.argv[2])
    else:
        print 'No such label'