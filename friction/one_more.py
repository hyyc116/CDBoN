from para_config import *


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

def first_citation(cited_papers_json):
    cited_papers = json.loads(open(cited_papers_json).read())

    time_internals = []
    for k in cited_papers.keys():
        paper_dict  = cited_papers[k]
        pid  = paper_dict['pid']
        year = paper_dict['year']
        citations = [(cit.split(',')[0],int(cit.split(',')[1])) for cit in paper_dict['citations']]
        
        cpid, cyear = sorted(citations,key=lambda x:x[1])[0]
        time_internals.append(cyear-year)

    internal_counter = Counter(time_internals)
    return internal_counter


def plot_three_level_first_citations(low,medium,high):
    # fig,axes = plt.subplots(1,3,figszie=(15,5))

    # ax1 = axes[0]
    internal_dict = first_citation(low)
    xs = []
    ys = []
    for i in sorted(internal_dict.keys()):
        xs.append(i)
        ys.append(internal_dict[i])
    ys = np.array(ys)/float(sum(ys))
    plt.plot(xs,ys,'low cited papers')

    internal_dict = first_citation(medium)
    xs = []
    ys = []
    for i in sorted(internal_dict.keys()):
        xs.append(i)
        ys.append(internal_dict[i])
    ys = np.array(ys)/float(sum(ys))
    plt.plot(xs,ys,'medium cited papers')

    internal_dict = first_citation(high)
    xs = []
    ys = []
    for i in sorted(internal_dict.keys()):
        xs.append(i)
        ys.append(internal_dict[i])
    ys = np.array(ys)/float(sum(ys))
    plt.plot(xs,ys,'high cited papers')

    plt.savefig('pdf/first_citation.pdf',dpi=300)

if __name__ == '__main__':
    plot_three_level_first_citations(sys.argv[1],sys.argv[2],sys.argv[3])


