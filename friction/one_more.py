from para_config import *



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
    return internal_counter,time_internals


def plot_three_level_first_citations(low,medium,high):
    # fig,axes = plt.subplots(1,3,figszie=(15,5))
    logging.info('plot first citations....')

    # ax1 = axes[0]
    logging.info('Low cited papers ...')

    xlabels  = ['Low','Medium','High']
    box_data = []

    internal_dict,time_internals = first_citation(low)
    xs = []
    ys = []
    for i in sorted(internal_dict.keys()):
        xs.append(i)
        ys.append(internal_dict[i])
    ys = np.array(ys)/float(sum(ys))
    plt.plot(xs,ys,label ='low cited papers')
    box_data.append(time_internals)

    logging.info('Medium cited papers ...')
    internal_dict,time_internals = first_citation(medium)
    xs = []
    ys = []
    for i in sorted(internal_dict.keys()):
        xs.append(i)
        ys.append(internal_dict[i])
    ys = np.array(ys)/float(sum(ys))
    plt.plot(xs,ys,label ='medium cited papers')
    box_data.append(time_internals)


    logging.info('High cited papers ...')
    internal_dict,time_internals = first_citation(high)
    xs = []
    ys = []
    for i in sorted(internal_dict.keys()):
        xs.append(i)
        ys.append(internal_dict[i])
    ys = np.array(ys)/float(sum(ys))

    plt.plot(xs,ys,label='high cited papers')
    box_data.append(time_internals)

    plt.legend()
    
    plt.xlim(0,10)
    plt.savefig('pdf/first_citation.pdf',dpi=300)

    logging.info('saved to pdf/first_citation.pdf')

    plt.figure()
    plt.violinplot(box_data,
                   showmeans=True,
                   showmedians=True)
    plt.savefig('pdf/first_citation_box.pdf',dpi=300)
    plt.set_xticks(np.arange(1, len(xlabels) + 1))
    plt.set_xticklabels(xlabels)
    plt.yscale('log')
    
    logging.info('saved to pdf/first_citation_box.pdf')


if __name__ == '__main__':
    plot_three_level_first_citations(sys.argv[1],sys.argv[2],sys.argv[3])


