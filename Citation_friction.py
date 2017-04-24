#coding:utf-8
import sys
import json
from collections import defaultdict
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import math
import numpy as np
import random

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

def citation_count_json(citation_network_path):
    data = json.loads(open(citation_network_path).read())
    citation_num_list = [] 
    for k in data.keys():
        citation_num_list.append(len(data[k]['citations']))

    num_counter = Counter(citation_num_list)

    open('data/aminer_citation_num_dict.json','w').write(json.dumps(num_counter))

def plot_citation_num():
    data = json.loads(open('aminer_citation_num_dict.json').read())
    xs=[]
    ys=[]
    total_count=0
    low_citation_count=0
    high_citation_count=0
    low_count=0
    for count in sorted([int(count) for count in data.keys()]):
        # if count<10:
        #     continue
        xs.append(count)
        total_count+=data[str(count)]
        ys.append(data[str(count)])

        if count <=10:
            low_count +=data[str(count)]
        if count<=10:
            low_citation_count+=data[str(count)]
        if count>1000:
            high_citation_count+=data[str(count)]


    # print xs
    # print ys
    print low_citation_count,low_citation_count/float(total_count)
    print high_citation_count, high_citation_count/float(total_count)
    print total_count
    length=len(xs)
    print length
    popt,pcov = curve_fit(power_low_func,xs[30:400],ys[30:400])

    print popt
    fig,axes = plt.subplots(1,2,figsize=(12,5))
    ax = axes[0]
    ax.plot(xs,ys,'o',fillstyle='none')
    ax.plot(np.linspace(10, 1000, 10), power_low_func(np.linspace(10, 1000, 10), *popt),c='r',label='$\\alpha={:.2f}$'.format(popt[0]))
    # plt.plot([760]*10,np.linspace(np.min(ys), power_low_func(760,*popt), 10),'--',c='r')
    # plt.plot([100]*10,np.linspace(np.min(ys), power_low_func(100,*popt), 10),'--',c='r')
    ax.plot([10]*10,np.linspace(10**3, 10**5, 10),'--',c='r')
    # plt.text()
    ax.plot(xs,xs,'--',label='$y=x$')

    ax.text(20,5*10**4,'$x_{low}$')
    ax.text(100,2*10**2,'$x_{medium}$')
    ax.text(2000,5*10**0,'$x_{high}$')


    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('$x$\n(a)')
    ax.set_ylabel('$N(x)$')
    ax.legend()

    medium_count = total_count-high_citation_count-low_count
    ax2 = axes[1]
    xs=['Low','Medium','High']
    ys=[low_citation_count,medium_count,high_citation_count]
    x_pos = x_pos = np.arange(len(xs))
    rects = ax2.bar(x_pos,ys,align='center',width=0.3)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(xs)
    ax2.set_xlabel('Levels\n(b)')
    ax2.set_ylabel('Number of papers')
    ax2.set_yscale('log')
    ax2.set_ylim(1,10**6.5)
    autolabel(rects,ax2,total_count)

    # plot_margin = 0.25

    # x0, x1, y0, y1 = plt.axis()
    # plt.axis((x0 - plot_margin,
    #     x1 + plot_margin,
    #     y0 - plot_margin,
    #     y1 + plot_margin))

    plt.tight_layout()
    plt.savefig('citation_dis.png',dpi=300)

def autolabel(rects,ax,total_count,step=1,):
    """
    Attach a text label above each bar displaying its height
    """
    for index in np.arange(len(rects),step=step):
        rect = rects[index]
        height = rect.get_height()
        # print height
        ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                '{:}\n({:.6f})'.format(int(height),height/float(total_count)),
                ha='center', va='bottom')

def power_low_func(x,a,b):
    return b*(x**(-a))

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

#divide paper with three point
def divide_paper_level(citation_network_path):
    data = json.loads(open(citation_network_path).read())
    low_citations=[]
    medium_citations=[]
    high_citations=[]

    for k in data.keys():
        citation_num = len(data[k]['citations'])
        if citation_num<5: 
            continue
        elif citation_num<=10:
            low_citations.append(k)
        elif citation_num<=1000:
            medium_citations.append(k)
        else:
            high_citations.append(k)

    print len(low_citations)
    print len(medium_citations)
    print len(high_citations)

    low_selected = random.sample(low_citations,1000)
    low_selected_counter=defaultdict(int)
    for pid in low_selected:
        low_selected_counter[len(data[pid]['citations'])]+=1

    print low_selected_counter

    medium_selected = random.sample(medium_citations,1000)
    medium_selected_counter = defaultdict(int)
    for pid in medium_selected:
        medium_selected_counter[len(data[pid]['citations'])]+=1

    print medium_selected_counter



#def first citation distribution
def first_citation_distribution(citation_network_path):
    data = json.loads(open(citation_network_path).read())
    year_dis=defaultdict(int)
    first_citation_dis = defaultdict(int)
    first_citation_year_dis = defaultdict(dict)
    for pid in data.keys():
        one_dict = data[pid]
        #year
        year = one_dict['year']
        year_dis[year]+=1
        #first citation delta
        citations = one_dict['citations']

        first_citation = sorted(citations,key=lambda x:int(x.split(',')[1]))[0]
        year_delta =  int(first_citation.split(',')[1]) - year
        if not year_delta<0:
            first_citation_dis[year_delta]+=1
            first_citation_year_dis[year][year_delta]=first_citation_year_dis[year].get(year_delta,0)+1

    fig,axes = plt.subplots(1,2,figsize=(15,5))
    ax1 = axes[0]
    xs = []
    ys = []
    for year in sorted(year_dis.keys()):
        xs.append(year)
        ys.append(year_dis[year])

    ax1.plot(xs,ys)
    ax1.set_xlabel('year $t$')
    ax1.set_ylabel('Number of published paper at year $t$')
    ax1.set_title('Paper distribution over published years')

    ax2 = axes[1]
    xs=[]
    ys=[]
    for year_delta in sorted(first_citation_dis.keys()):
        xs.append(year_delta)
        ys.append(first_citation_dis[year_delta])

    ax2.plot(xs,ys)
    ax2.set_xlabel('$\delta t$')
    ax2.set_ylabel('Number of papers')
    ax2.set_yscale('log')
    ax2.set_title('First citation distribution')

    plt.savefig('two_dis.pdf',dpi=300)
    open('data/year_first_citation.json','w').write(json.dumps(first_citation_year_dis))



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
            delta_t = (year-publish_year)+1
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
            delta_t = (year-publish_year)+1
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
            delta_t = (year-publish_year)+1
            count = year_counter[year]
            # accum_count+=count

            years.append(delta_t)
            counts.append("{:.5f}".format(delta_t/float(count)))

        ax.plot(years,counts)
        ax.set_title(pid)

        ax_index+=1

    plt.tight_layout()
    plt.savefig('top_{:}_count_delta.png'.format(N),dpi=300)

def main():
    label = sys.argv[1]
    if label=='citation_network':
        build_citation_network(sys.argv[2])
    elif label == 'citation_num':
        citation_count_json(sys.argv[2])
    elif label =='plot_top':
        plot_top_N(sys.argv[2],int(sys.argv[3]))
    elif label =='friction':
        frictions(sys.argv[2])
    elif label=='paper_level':
        divide_paper_level(sys.argv[2])
    elif label=='first_citation':
        first_citation_distribution(sys.argv[2])
    else:
        print 'No such label'
    
if __name__ == '__main__':
    # plot_citation_num()
    main()
    