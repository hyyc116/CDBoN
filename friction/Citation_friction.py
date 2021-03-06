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

PREFIX='all'
PROGRAM_ID='friction'
PAGEDIR='pdf'
DATADIR='data'

#from the aminer_refence to build citation network
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



#citation order t_i vs i
# def co_ti_all(citations,year):
#     ti_list = []
#     for cpid, cyear in sorted(citations,key=lambda x:x[1]):
#         ti_list.append(cyear-year+1)
    
#     xs = []
#     ys = []

#     for i, ti in enumerate(ti_list):
#         order = i+1
#         xs.append(order)
#         ys.append(ti)

#     return xs,ys

# git their first i citation
def co_ti_i(citations,year,i='all'):
    if i=='all':
        i=len(citations)
    else:
        i=int(i)

    ti_list = []
    for cpid, cyear in sorted(citations,key=lambda x:x[1])[:i]:
        ti_list.append(cyear-year+1)
    
    xs = []
    ys = []

    for i, ti in enumerate(ti_list):
        order = i+1
        xs.append(order)
        ys.append(ti)

    return xs,ys

def co_delta_ti(citations,year,i='all'):
    if i=='all':
        i = len(citations)
    else:
        i = int(i)

    ti_list = []
    delta_ti_list = []
    for cpid, cyear in sorted(citations,key=lambda x:x[1])[:i]:
        t_i = cyear-year+1
        if len(ti_list)>0:
            delta_ti = t_i - ti_list[-1]
        else:
            delta_ti = t_i

        ti_list.append(t_i)
        delta_ti_list.append(delta_ti)
    
    xs = []
    ys = []

    for i, ti in enumerate(delta_ti_list):
        order = i+1
        xs.append(order)
        ys.append(ti)

    return xs,ys

def co_ti_di(citations,year,i='all'):
    if i=='all':
        i = len(citations)
    else:
        i = int(i)

    ti_list = []
    for cpid, cyear in sorted(citations,key=lambda x:x[1])[:i]:
        ti_list.append(cyear-year+1)
    
    xs = []
    ys = []

    for i, ti in enumerate(ti_list):
        order = i+1
        xs.append(order)
        ys.append(ti/float(order))

    return xs,ys

#citation year
def cy_cyi_yi(citations,year,i='all'):
    yi_list =[]
    for cpid, cyear in sorted(citations,key=lambda x:x[1]):
        yi = cyear-year
        yi_list.append(yi)

    yi_counter = Counter(yi_list)
    
    xs = []
    ys = []
    acc_count=0
    for yi in sorted(yi_counter.keys()):
        xs.append(yi)
        acc_count += yi_counter[yi]
        ys.append(acc_count)

    return xs,ys

#citation year
def cy_delta_cyi_yi(citations,year,i='all'):
    yi_list =[]
    for cpid, cyear in sorted(citations,key=lambda x:x[1]):
        yi = cyear-year
        yi_list.append(yi)

    yi_counter = Counter(yi_list)
    
    xs = []
    ys = []
    for yi in sorted(yi_counter.keys()):
        xs.append(yi)
        ys.append(yi_counter[yi])

    return xs,ys

#citation year
def cy_cyi_dyi(citations,year,i='all'):
    yi_list =[]
    for cpid, cyear in sorted(citations,key=lambda x:x[1]):
        yi = cyear-year+1
        yi_list.append(yi)

    yi_counter = Counter(yi_list)
    
    xs = []
    ys = []
    acc_count=0
    for yi in sorted(yi_counter.keys()):
        xs.append(yi)
        acc_count += yi_counter[yi]
        ys.append(acc_count/float(yi))

    return xs,ys

#citation year
def cy_yi_dcyi(citations,year,i='all'):
    yi_list =[]
    for cpid, cyear in sorted(citations,key=lambda x:x[1]):
        yi = cyear-year+1
        yi_list.append(yi)

    yi_counter = Counter(yi_list)
    
    xs = []
    ys = []
    acc_count=0
    for yi in sorted(yi_counter.keys()):
        xs.append(yi)
        acc_count += yi_counter[yi]
        ys.append(float(yi)/acc_count)

    return xs,ys

#citation year
def cy_delta_yi(citations,year,i='all'):
    yi_list =[]
    for cpid, cyear in sorted(citations,key=lambda x:x[1]):
        yi = cyear-year+1
        yi_list.append(yi)

    yi_counter = Counter(yi_list)
    
    xs = []
    ys = []
    acc_count=0
    last_yi=0
    for i,yi in enumerate(sorted(yi_counter.keys())):
        xs.append(yi)
        ys.append(yi-last_yi)
        last_yi=yi

    return xs,ys

#citation year
def cy_delta_cyi_ddelta_yi(citations,year,i='all'):
    yi_list =[]
    for cpid, cyear in sorted(citations,key=lambda x:x[1]):
        yi = cyear-year+1
        yi_list.append(yi)

    yi_counter = Counter(yi_list)
    
    xs = []
    ys = []
    acc_count=0
    last_yi=0
    for i,yi in enumerate(sorted(yi_counter.keys())):
        xs.append(yi)
        delta_yi = yi-last_yi
        ys.append(yi_counter[yi]/float(delta_yi))
        last_yi=yi

    return xs,ys

#citation year
def cy_delta_yi_ddelta_cyi(citations,year,i='all'):
    yi_list =[]
    for cpid, cyear in sorted(citations,key=lambda x:x[1]):
        yi = cyear-year+1
        yi_list.append(yi)

    yi_counter = Counter(yi_list)
    
    xs = []
    ys = []
    acc_count=0
    last_yi=0
    for i,yi in enumerate(sorted(yi_counter.keys())):
        xs.append(yi)
        delta_yi = yi-last_yi
        ys.append(float(delta_yi)/yi_counter[yi])
        last_yi=yi

    return xs,ys


#from perspective of citation order
def citation_order(cited_papers_json,xyfunc=co_ti_i,i='all'):
    cited_papers = json.loads(open(cited_papers_json).read())
    xs_ys_dict={}
    
    for k in cited_papers.keys():
        paper_dict = cited_papers[k]
        pid = paper_dict['pid']
        year = paper_dict['year']
        citations = [(cit.split(',')[0],int(cit.split(',')[1])) for cit in paper_dict['citations']]
        xs,ys = xyfunc(citations,year,i)
        xs_ys_dict[pid]=(xs,ys)

    return xs_ys_dict


def plot_three_cited_levels(low_json,medium_json,high_json,xyfunc_name='co_ti_i',i='all',is_scale=0,low=0,up=100,isLast=0):

    if xyfunc_name=='co_ti_i':
        xyfunc = co_ti_i
        yls = 'Length of Time'
        xls = '$i^{th}$ citation'
        low = int(low)
        up = int(up)

    elif xyfunc_name=='co_delta_ti':
        xyfunc = co_delta_ti
        yls = 'Length of Time'
        xls = '$i^{th}$ citation'
        low = int(low)
        up = int(up)

    elif xyfunc_name=='co_ti_di':
        xyfunc = co_ti_di
        yls = '$t_i/i$'
        xls = 'citation order $i$'
    elif xyfunc_name=='cy_cyi_yi':
        xyfunc = cy_cyi_yi
        xls='t'
        yls='Number of citations'
        low = -1
        up = -1

    elif xyfunc_name=='cy_cyi_dyi':
        xyfunc = cy_cyi_dyi
        xls='t'
        yls='Average Speed'
        low = int(low)
        up = int(up)

    elif xyfunc_name=='cy_yi_dcyi':
        xyfunc = cy_yi_dcyi
        xls='t'
        yls='$Average time$'
        low = float(low)
        up = float(up)

    elif xyfunc_name=='cy_delta_cyi_yi':
        xyfunc = cy_delta_cyi_yi
        xls='t'
        yls='Number of citation'
        low = -1
        up = -1

    elif xyfunc_name=='cy_delta_yi':
        xyfunc = cy_delta_yi
        xls='citation year $y_i$'
        yls='$\Delta y_i$'
    elif xyfunc_name=='cy_delta_cyi_ddelta_yi':
        xyfunc = cy_delta_cyi_ddelta_yi
        xls='citation year $y_i$'
        yls='$\Delta C_{y_i}/\Delta y_i$'

    elif xyfunc_name=='cy_delta_yi_ddelta_cyi':
        xyfunc = cy_delta_yi_ddelta_cyi
        xls='citation year $y_i$'
        yls='$\Delta y_i/\Delta C_{y_i}$'

    print xyfunc_name,'with i=',i,'low',low,'up',up

    fig,axes = plt.subplots(1,3,figsize=(15,5))
    
    
    print 'low cited papers'
    ax1 = axes[0]
    low_xy_dict = citation_order(low_json,xyfunc,i)
    title = 'low cited papers'
    low_yss = plot_levels(ax1,low_xy_dict,title,xls+"\n(a)",yls,is_scale,low,up)

    ax2= axes[1]
    print 'medium cited papers'
    medium_xy_dict = citation_order(medium_json,xyfunc,i)
    title = 'medium cited papers'
    medium_yss = plot_levels(ax2,medium_xy_dict,title,xls+"\n(b)",yls,is_scale,low,up)

    ax3= axes[2]
    print 'high cited papers'
    high_xy_dict = citation_order(high_json,xyfunc,i)
    title = 'high cited papers'
    high_yss = plot_levels(ax3,high_xy_dict,title,xls+"\n(c)",yls,is_scale,low,up)

    plt.tight_layout()
    namepath = 'pdf/metrics_levels_{:}_{:}.pdf'.format(xyfunc_name,i)
    plt.savefig(namepath,dpi=300)
    print 'Result saved to',namepath

    if isLast==1:
        fig,axes = plt.subplots(1,3,figsize=(15,5))
        ax1 = axes[0]
        hist_levels(ax1,low_yss)
        ax2 = axes[1]
        hist_levels(ax2,medium_yss)
        ax3 = axes[2]
        hist_levels(ax3,high_yss)
        plt.tight_layout()
        namepath = 'pdf/metrics_last_{:}_{:}.pdf'.format(xyfunc_name,i)
        plt.savefig(namepath,dpi=300)
        print 'Result saved to',namepath



def hist_levels(ax,ys):
    ax.hist(ys,10,normed=True)

def plot_levels(ax,xs_ys_dict,title,xls,yls,is_scale=0,low=0,up=60):
    last_ys = []
    for key in xs_ys_dict.keys():
        xs,ys = xs_ys_dict[key]
        ax.plot(xs,ys)
        last_ys.append(ys[-1])
    ax.set_title(title)
    ax.set_xlabel(xls)
    ax.set_ylabel(yls)
    if is_scale==1:
        ax.set_yscale('log')
    if low!=-1:
        ax.set_ylim(low,up)
    # ax.set_xlim(0,50)
    # ax.set_ylim(0,ylims_up)
    return last_ys

def scatter_levels(ax,xs,ys,title,xls,yls,label='low cited papers'):
    
    ax.scatter(xs,ys,marker='.',label=label)

    ax.set_title(title)
    ax.set_xlabel(xls)
    ax.set_ylabel(yls)
    ax.set_yscale('log')

def plot_year_dis(ax,xs,ys,title,xls,yls,label='low cited papers'):
    
    ax.plot(xs,ys,label=label)

    ax.set_title(title)
    ax.set_xlabel(xls)
    ax.set_ylabel(yls)
    # ax.set_yscale('log')

def scatter_three_levels(low_json,medium_json,high_json):
    
    xls = '$y_T$'
    yls = 'C'
    fig,axes = plt.subplots(1,3,figsize=(15,5))
    ax1 = axes[2]
    title = 'citation distribution  over total citation years'
    low_xs,low_ys = citation_num_yt(low_json)
    m_xs,m_ys = citation_num_yt(medium_json)
    h_xs,h_ys = citation_num_yt(high_json)
    
    scatter_levels(ax1,low_xs,low_ys,title,xls,yls,label='low cited papers')
    scatter_levels(ax1,m_xs,m_ys,title,xls,yls,label='medium cited papers')
    scatter_levels(ax1,h_xs,h_ys,title,xls,yls,label='high cited papers')
    ax1.legend()

    ax2= axes[0]
    xls = '$y_0$'
    yls = '$N(y_0)$'
    title = 'Paper distribution over published years'
    low_xs,low_ys = citation_years(low_json)
    m_xs,m_ys = citation_years(medium_json)
    h_xs,h_ys = citation_years(high_json)
    
    plot_year_dis(ax2,low_xs,low_ys,title,xls,yls,label='low cited papers')
    plot_year_dis(ax2,m_xs,m_ys,title,xls,yls,label='medium cited papers')
    plot_year_dis(ax2,h_xs,h_ys,title,xls,yls,label='high cited papers')
    ax2.legend()

    ax3 = axes[1]
    xls = '$y_0$'
    yls = '$C$'
    title = 'Citation distribution over published years'
    low_xs,low_ys = citation_num_year(low_json)
    m_xs,m_ys = citation_num_year(medium_json)
    h_xs,h_ys = citation_num_year(high_json)
    
    scatter_levels(ax3,low_xs,low_ys,title,xls,yls,label='low cited papers')
    scatter_levels(ax3,m_xs,m_ys,title,xls,yls,label='medium cited papers')
    scatter_levels(ax3,h_xs,h_ys,title,xls,yls,label='high cited papers')
    ax3.legend()


    plt.tight_layout()
    namepath = 'pdf/scatter_three_levels.pdf'
    plt.savefig(namepath,dpi=300)
    print 'Result saved to',namepath

#from perspective of citation order
def citation_num_yt(cited_papers_json):
    cited_papers = json.loads(open(cited_papers_json).read())
    xs=[]
    ys=[]    
    for k in cited_papers.keys():
        paper_dict = cited_papers[k]
        pid = paper_dict['pid']
        year = paper_dict['year']
        citations_years = [int(cit.split(',')[1]) for cit in paper_dict['citations']]
        xs.append(np.max(citations_years)-year)
        ys.append(len(citations_years))
    return xs,ys

#from perspective of citation order
def citation_num_year(cited_papers_json):
    cited_papers = json.loads(open(cited_papers_json).read())
    xs=[]
    ys=[]    
    for k in cited_papers.keys():
        paper_dict = cited_papers[k]
        pid = paper_dict['pid']
        year = paper_dict['year']
        citations_years = [int(cit.split(',')[1]) for cit in paper_dict['citations']]
        xs.append(year)
        ys.append(len(citations_years))
    return xs,ys


def citation_years(cited_papers_json):
    cited_papers = json.loads(open(cited_papers_json).read())
    xs=[]
    ys=[]
    years=[]    
    for k in cited_papers.keys():
        paper_dict = cited_papers[k]
        pid = paper_dict['pid']
        year = paper_dict['year']
        years.append(year)
    
    years_counter = Counter(years)
    for year in sorted(years_counter.keys()):
        xs.append(year)
        ys.append(years_counter[year])

    ys = [float(y)/sum(ys) for y in ys]
    return xs,ys


#from perspective of citation order
def citation_ages(citation_network_path):
    cited_papers = json.loads(open(citation_network_path).read())
    age_dict=defaultdict(list)
    
    for k in cited_papers.keys():
        paper_dict = cited_papers[k]
        pid = paper_dict['pid']
        year = paper_dict['year']
        citations = [int(cit.split(',')[1]) for cit in paper_dict['citations']]
        age = np.max(citations)-year
        age_dict[year].append(age)

    fig,axes = plt.subplots(1,2,figsize=(10,5))
    ax1=axes[0]
    xs = []
    ys = []
    for year in sorted(age_dict.keys()):
        xs.append(year)
        ys.append(len(age_dict[year]))

    ax1.plot(xs,ys)
    ax1.set_title('Paper distribution over published year',fontsize=15)
    ax1.set_xlabel('published year',fontsize=10)
    ax1.set_ylabel('Paper count',fontsize=10)
    ax1.set_xlim(1930,2020)
    # ax1.set_yscale('log')

    ax2=axes[1]
    xs = []
    ys = []
    avg = []
    for year in sorted(age_dict.keys()):
        xs.append(year)
        ys.append(sum(age_dict[year])/float(len(age_dict[year])))
        if year>1980:
            avg.append(sum(age_dict[year])/float(len(age_dict[year])))

    a_avg = sum(avg)/float(len(avg))
    ax2.plot(xs,ys)
    ax2.plot(np.linspace(1960,2020,10),[a_avg]*10,'--',label='mean:{:.2f}'.format(a_avg))
    ax2.set_title('Average Citation Age of papers published at year x',fontsize=15)
    ax2.set_xlabel('published year x',fontsize=10)
    ax2.set_ylabel('Average Citation Age',fontsize=10)
    ax2.set_xlim(1930,2020)
    # ax2.set_yscale('log')
    ax2.legend()

    plt.tight_layout()
    plt.savefig('pdf/citation_ages.png',dpi=300)



#divide paper with three point
def divide_paper_level(citation_network_path):
    data = json.loads(open(citation_network_path).read())
    low_citations=defaultdict(list)
    medium_citations=defaultdict(list)
    high_citations=[]

    for k in data.keys():
        citation_num = len(data[k]['citations'])
        if citation_num<5: 
            continue
        elif citation_num<=10:
            low_citations[citation_num].append(k)
        elif citation_num<=1000:
            medium_citations[citation_num].append(k)
        else:
            high_citations.append(k)

    # print low_citations
    # print len(medium_citations)
    print len(high_citations)


    fig,axes = plt.subplots(2,2,figsize=(15,10))
    ax1 = axes[0,0]
    #to randomly select paper, first select citation num with a normal distribution
    citations_nums = [int(n) for n in np.random.normal(100,10,1000)]
    num_counter = Counter(citations_nums)
    medium_selected=[]
    xs=[]
    ys=[]
    for num in sorted(num_counter.keys()):
        num_count = num_counter[num]
        # print num,num_count
        medium_selected.extend(random.sample(medium_citations[num],num_count))
        xs.append(num)
        ys.append(num_count)

    open('data/medium_selected_counter.json','w').write(json.dumps(num_counter))

    ax1.plot(xs,ys)
    ax1.set_xlabel('Citation Count')
    ax1.set_ylabel('Number')
    ax1.set_title('Citation Count Distribution of selected papers')

    # print medium_selected

    # for num in range(5,11):

    low_selected = random.sample(low_citations[10],1000)

    #plot citation dentsity curve low selected paper

    ax2 = axes[0,1]
    ax2.set_title('Low cited paper')
    ax2.set_xlabel('$\Delta t$')
    ax2.set_ylabel('$Difficulty$')
    ax2.set_yscale('log')
    for pid in low_selected:
        cited_dict = data[pid]
        pid_year = cited_dict['year']
        citation_year_list = [int(i.split(',')[1]) for i in cited_dict['citations']]
        year_counter = Counter(citation_year_list)
        
        xs = [] 
        ys = []
        total_citation=0
        for year in sorted(year_counter.keys()):
            delta_y = (year - pid_year)+1
            total_citation+=year_counter[year]
            difficulty = delta_y/float(total_citation)
            xs.append(delta_y)
            ys.append(difficulty)

        xs=[(x-xs[0])+1 for x in xs]
        ax2.plot(xs,ys)

    ax3 = axes[1,0]
    ax3.set_title('Medium cited paper')
    ax3.set_xlabel('$\Delta t$')
    ax3.set_ylabel('$Difficulty$')
    ax3.set_yscale('log')
    for pid in medium_selected:
        cited_dict = data[pid]
        pid_year = cited_dict['year']
        citation_year_list = [int(i.split(',')[1]) for i in cited_dict['citations']]
        year_counter = Counter(citation_year_list)
        
        xs = [] 
        ys = []
        total_citation=0
        for year in sorted(year_counter.keys()):
            delta_y = (year - pid_year)+1
            total_citation+=year_counter[year]
            difficulty = delta_y/float(total_citation)
            xs.append(delta_y)
            ys.append(difficulty)

        xs=[(x-xs[0])+1 for x in xs]
        ax3.plot(xs,ys)

    ax4 = axes[1,1]
    ax4.set_title('High cited paper')
    ax4.set_xlabel('$\Delta t$')
    ax4.set_ylabel('$Difficulty$')
    ax4.set_yscale('log')
    for pid in high_citations:
        cited_dict = data[pid]
        pid_year = cited_dict['year']
        citation_year_list = [int(i.split(',')[1]) for i in cited_dict['citations']]
        year_counter = Counter(citation_year_list)
        
        xs = [] 
        ys = []
        total_citation=0
        for year in sorted(year_counter.keys()):
            delta_y = (year - pid_year)+1
            total_citation+=year_counter[year]
            difficulty = delta_y/float(total_citation)
            xs.append(delta_y)
            ys.append(difficulty)

        xs=[(x-xs[0])+1 for x in xs]
        ax4.plot(xs,ys)

    # low_selected_counter=defaultdict(int)
    # for pid in low_selected:
    #     low_selected_counter[len(data[pid]['citations'])]+=1

    # print low_selected_counter

    # medium_selected = random.sample(medium_citations,1000)
    # medium_selected_counter = defaultdict(int)
    # for pid in medium_selected:
    #     medium_selected_counter[len(data[pid]['citations'])]+=1

    # print medium_selected_counter
    plt.tight_layout()
    plt.savefig('pdf/selected_citation_dis.pdf',dpi=300)

    high_dicts = {}
    for k in high_citations:
        high_dicts[k] = data[k]

    open('data/high_dicts.json','w').write(json.dumps(high_dicts))

    medium_dicts={}
    for k in medium_selected:
        medium_dicts[k] = data[k]
    open('data/medium_dicts.json','w').write(json.dumps(medium_dicts))

    low_dicts={}
    for k in low_selected:
        low_dicts[k] = data[k]
    open('data/low_dicts.json','w').write(json.dumps(low_dicts))


#def first citation distribution
def first_citation_distribution(citation_network_path):
    data = json.loads(open(citation_network_path).read())
    year_dis=defaultdict(int)
    first_citation_dis = defaultdict(int)
    first_citation_year_dis = defaultdict(dict)
    first_citation_zone_dis = defaultdict(dict)
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
            if year < 1981:
                zone = 'A'
            elif year<2001:
                zone = 'B'
            elif year <2011:
                zone = 'C'
            else:
                zone = 'D'

            first_citation_zone_dis[zone][year_delta] = first_citation_zone_dis[zone].get(year_delta,0)+1


    fig,axes = plt.subplots(1,4,figsize=(30,5))
    ax1 = axes[0]
    xs = []
    ys = []
    a_count=0
    b_count=0
    c_count=0
    d_count=0

    for year in sorted(year_dis.keys()):
        xs.append(year)
        ys.append(year_dis[year])
        if year<1981:
            a_count+=year_dis[year]
        elif year<2001:
            b_count+=year_dis[year]
        elif year<2011:
            c_count+=year_dis[year]
        else:
            d_count+=year_dis[year]

    ax1.plot(xs,ys)
    ax1.set_xlabel('year $t$')
    ax1.set_ylabel('Number of published paper at year $t$')
    ax1.set_title('Paper distribution over published years')
    ax1.set_xlim(np.min(xs),2020)
    ax1.plot([1980]*10,np.linspace(0,np.max(ys),10),'--',label='$t = 1980$')
    ax1.plot([2000]*10,np.linspace(0,np.max(ys),10),'--',label='$t = 2000$')
    ax1.plot([2010]*10,np.linspace(0,np.max(ys),10),'--',label='$t = 2010$')
    ax1.text(1960,20000,'A')
    ax1.text(1990,20000,'B')
    ax1.text(2005,20000,'C')
    ax1.text(2015,20000,'D')
    ax1.legend()

    labels=['A','B','C','D']
    counts = [a_count,b_count,c_count,d_count]
    ax2 = axes[1]
    # ax2.bar(np.arange(len(labels)),counts)
    rects = ax2.bar(np.arange(len(labels)),counts,align='center',width=0.3)
    ax2.set_xticks(np.arange(len(labels)))
    ax2.set_xticklabels(labels)
    # autolabel(rects)
    autolabel(rects,ax2)
    ax2.set_title('Distribution of four zone')
    ax2.set_xlabel('Zone Label')
    ax2.set_ylabel('Number of Papers')
    ax2.set_yscale('log')

    ax3 = axes[2]
    xs=[]
    ys=[]
    for year_delta in sorted(first_citation_dis.keys()):
        xs.append(year_delta)
        ys.append(first_citation_dis[year_delta])

    ax3.plot(xs,ys)
    ax3.plot([1]*10,np.linspace(1,np.max(ys),10),'--',label='$\Delta t = 1$')
    for zone in labels:
        zone_citation_dis = first_citation_zone_dis[zone]
        print zone
        print zone_citation_dis
        xs=[]
        ys=[]
        for year_delta in sorted(zone_citation_dis.keys()):
            xs.append(year_delta)
            ys.append(zone_citation_dis[year_delta])

        ax3.plot(xs,ys,label='Zone {:}'.format(zone))

    ax3.set_xlabel('$\Delta t$')
    ax3.set_ylabel('Number of papers')
    ax3.set_yscale('log')
    ax3.set_title('First citation distribution')
    
    ax3.legend()

    ax4=axes[3]
    xs=[]
    ys=[]
    for year in sorted(first_citation_year_dis):
        if year<1981 or year >2010:
            continue
        citation_year_dis = first_citation_year_dis[year]
        xs.append(year)
        avg = cal_avg(citation_year_dis)
        ys.append(avg)

    ax4.plot(xs,ys)
    ax4.set_ylabel('$ Mean of \Delta t_1$')
    ax4.set_xlabel('year $t$')
    # ax4.set_yscale('log')
    ax4.set_title('First citation distribution')
    # ax4.plot([1]*10,np.linspace(1,100000,10),'--',label='$\Delta t = 1$')
    # ax4.legend()  

    plt.tight_layout()
    plt.savefig('pdf/two_dis.pdf',dpi=300)
    open('data/year_first_citation.json','w').write(json.dumps(first_citation_year_dis))

def cal_avg(delta_dis):
    total_count=0
    total_year=0
    for year_delta in delta_dis:
        total_year+=year_delta*delta_dis[year_delta]
        total_count+=delta_dis[year_delta]

    return total_year/float(total_count)

def frictions(top_n_papers,level='top'):
    top_dict = json.loads(open(top_n_papers).read())
    N = len(top_dict)
    print N
    # rows = N/5+1

    #friction accumulative/delta_t
    # result_lines=[]
    # for pid in top_dict.keys():

    #     cited_dict = top_dict[pid]
    #     pid_year = cited_dict['year']
    #     citation_year_list = [int(i.split(',')[1]) for i in cited_dict['citations']]
    #     year_counter = Counter(citation_year_list)
    #     # print year_counter
    #     years=[]
    #     counts=[]
    #     accum_count=0
    #     publish_year = int(pid_year)
    #     for year in sorted(year_counter.keys()):
    #         delta_t = (year-publish_year)+1
    #         count = year_counter[year]
    #         accum_count+=count

    #         years.append(delta_t)
    #         counts.append(accum_count/delta_t)

    #     # ax.plot(years,counts)
    #     result = plot_power_law(years,counts)
    #     result_lines.append(result)

    # num = len(plt.get_fignums())
    # plt.figure(num)
    # fig,axes = plt.subplots(1,5,figsize=(25,5))
    # for index,r in enumerate(sorted(result_lines,key=lambda x:x[3],reverse=True)):
    #     ax_x = index/5
    #     ax_y = index%5

    #     if ax_y==0 and index>0:
    #         plt.tight_layout()
    #         plt.savefig('fig/top_{:}_accum_{:}.png'.format(N,ax_x),dpi=300)
    #         num = len(plt.get_fignums())
    #         plt.figure(num)
    #         fig,axes = plt.subplots(1,5,figsize=(25,5))

    #     ax = axes[ax_y]
    #     xs,ys,fit_y,r2,popt = r[0],r[1],r[2],r[3],r[4]
    #     ax.plot(xs,ys)
    #     ax.plot(xs,fit_y,c='r',label='$R^2={:.5f},\\alpha={:}$'.format(r2,popt[0]))
    #     ax.legend()

    # plt.tight_layout()
    # plt.savefig('fig/top_{:}_accum_{:}.png'.format(N,ax_x),dpi=300)

    #friction delta_t/accumulative
    result_lines=[]    
    for pid in top_dict.keys():
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
            counts.append(delta_t/float(accum_count))

        # ax.plot(years,counts)
        # print years 
        # print counts
        result = plot_power_law(years,counts)
        result_lines.append(result)

    outlist=['num,alpha']
    num = len(plt.get_fignums())
    plt.figure(num)
    fig,axes = plt.subplots(1,5,figsize=(25,5))
    for index,r  in enumerate(sorted(result_lines,key=lambda x:x[3],reverse=True)):
        ax_x = index/5
        ax_y = index%5

        if ax_y==0 and index>0:
            plt.tight_layout()
            plt.savefig('fig/{:}_{:}_delta_{:}.png'.format(level,N,ax_x),dpi=300)
            num = len(plt.get_fignums())
            plt.figure(num)
            fig,axes = plt.subplots(1,5,figsize=(25,5))

        ax = axes[ax_y]
        xs,ys,fit_y,r2,popt = r[0],r[1],r[2],r[3],r[4]
        
        if r2>0.8:
            outlist.append('{:},{:.5f}'.format(ys[-1],popt[0]))

        ax.plot(xs,ys)
        ax.plot(xs,fit_y,c='r',label='$R^2={:.5f},\\alpha={:}$'.format(r2,popt[0]))
        ax.legend()

    plt.tight_layout()
    plt.savefig('fig/{:}_{:}_delta_{:}.png'.format(level,N,ax_x),dpi=300)
    open('{:}_{:}_delta_{:}.csv','w').write('\n'.join(outlist))

    #friction delta_t/count
    # num = len(plt.get_fignums())
    # plt.figure(num)
    # fig,axes = plt.subplots(1,5,figsize=(25,5))
    # ax_index=1

    # for pid in top_dict.keys():

    #     ax_x = (ax_index-1)/5
    #     ax_y = ax_index%5-1
    #     print ax_index,ax_x,ax_y
    #     if ax_y==0 and ax_index>1:
    #         plt.tight_layout()
    #         plt.savefig('fig/top_{:}_count_delta_{:}.png'.format(N,ax_x),dpi=300)
    #         num = len(plt.get_fignums())
    #         plt.figure(num)
    #         fig,axes = plt.subplots(1,5,figsize=(25,5))

    #     ax = axes[ax_y]
    #     cited_dict = top_dict[pid]
    #     pid_year = cited_dict['year']
    #     citation_year_list = [int(i.split(',')[1]) for i in cited_dict['citations']]
    #     year_counter = Counter(citation_year_list)
    #     # print year_counter
    #     publish_year = int(pid_year)
    #     years=[]
    #     counts=[]
    #     # accum_count=0
    #     for year in sorted(year_counter.keys()):
    #         delta_t = (year-publish_year)+1
    #         count = year_counter[year]
    #         # accum_count+=count

    #         years.append(delta_t)
    #         counts.append("{:.5f}".format(delta_t/float(count)))

    #     ax.plot(years,counts)
    #     ax.set_title(pid)

    #     ax_index+=1

    # plt.tight_layout()
    # plt.savefig('fig/top_{:}_count_delta_{:}.png'.format(N,ax_x),dpi=300)

def plot_power_law(xs,ys):
    popt,pcov = curve_fit(power_low_func,xs,ys)
    print 'adoptions:',popt
    fit_y = [power_low_func(xi,*popt) for xi in xs]
    r2 = r2_score(ys,fit_y)
    print 'R2',r2
    return xs,ys,fit_y,r2,popt
    # return popt,r2
    


def power_law(x,alpha):
    return x**(-alpha)

def plot_distributions():

    fig,axes = plt.subplots(1,3,figsize=(20,5))

    #plot power law
    ax1 = axes[0]
    xs = np.linspace(0,10,100)
    ys = [power_law(x,3) for x in xs]
    ax1.plot(xs,ys)

    #plot     


def main():
    label = sys.argv[1]
    if label=='citation_network':
        build_citation_network(sys.argv[2])
    elif label == 'citation_num':
        citation_count_json(sys.argv[2])
    elif label=='co':
        citation_order(sys.argv[2])
    elif label=='co_three_levels':
        plot_three_cited_levels(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],int(sys.argv[7]),float(sys.argv[8]),float(sys.argv[9]),float(sys.argv[10]))
    elif label=='scatter_levels':
        scatter_three_levels(sys.argv[2],sys.argv[3],sys.argv[4])
    elif label=='citation_ages':
        citation_ages(sys.argv[2])
    elif label =='plot_top':
        plot_top_N(sys.argv[2],int(sys.argv[3]))
    elif label =='friction':
        frictions(sys.argv[2],sys.argv[3])
    elif label=='paper_level':
        # divide_paper_level(sys.argv[2])
        get_three_levels_paper(sys.argv[2])
    elif label=='first_citation':
        first_citation_distribution(sys.argv[2])
    else:
        print 'No such label'
    
if __name__ == '__main__':
    # plot_citation_num()
    main()
    