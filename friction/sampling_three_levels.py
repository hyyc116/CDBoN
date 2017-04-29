#coding:utf-8
from para_config import *
from friction_plots.py import *

#get three levels of papers
def get_three_levels_paper(citation_network_path,N):
    data = json.loads(open(citation_network_path).read())
    citation_num_list = defaultdict(list)
    high_selected=[]
    high_citation_nums = []
    for k in data.keys():
        if data[k]['year']>N:
            continue
        citation_num = len(data[k]['citations'])
        citation_num_list[citation_num].append(k)

        if citation_num>1000:
            high_selected.append(k)
            high_citation_nums.append(citation_num)

    

    # to randomly select low cited paper with a normal distribution
    low_citations_nums = [int(n) for n in np.random.normal(10,1,1000)]
    low_counter = Counter(low_citations_nums)
    logging.info('low Cited nums: {:}'.format(len(low_citations_nums)))

    # to randomly select medium cited nums
    mediumn_citations_nums = [int(n) for n in np.random.normal(100,10,1000)]
    medium_counter = Counter(mediumn_citations_nums)
    logging.info('Medium Cited nums: {:}'.format(len(mediumn_citations_nums)))

    #number of high cited papers
    logging.info('number of high cited papers: {:}'.format(len(high_selected)))
    high_counter = Counter(high_citation_nums)

    #plot the citation num distribution of three cited levels
    fig,axes = plt.subplots(1,4,figsize=(20,5))
    ax1 = axes[0]
    xs=[]
    ys=[]
    low_selected=[]
    for num in sorted(low_counter.keys()):
        num_count = low_counter[num]
        # print num,num_count
        low_selected.extend(random.sample(citation_num_list[num],num_count))
        xs.append(num)
        ys.append(num_count)

    low_selected_papers = {}
    for pid in low_selected:
        low_selected_papers[pid] = data[pid]

    open('data/low_selected_papers.json','w').write(json.dumps(low_selected_papers))
    logging.info('low cited papers saved to data/low_selected_papers.json')

    xls = 'Citation Count $x$\n(a)'
    yls = '$N(x)$'
    title = 'low cited papers'
    subplot_line(ax1,xs,ys,title,xls,yls)

    ax2 = axes[1]
    xs=[]
    ys=[]
    medium_selected=[]
    for num in sorted(medium_counter.keys()):
        num_count = medium_counter[num]
        # print num,num_count
        medium_selected.extend(random.sample(citation_num_list[num],num_count))
        xs.append(num)
        ys.append(num_count)

    medium_selected_papers = {}
    for pid in medium_selected:
        medium_selected_papers[pid] = data[pid]

    open('data/medium_selected_papers.json','w').write(json.dumps(medium_selected_papers))
    logging.info('medium cited papers saved to data/medium_selected_papers.json')

    
    xls = 'Citation Count $x$\n(b)'
    yls = '$N(x)$'
    title = 'medium cited papers'
    subplot_line(ax2,xs,ys,title,xls,yls)

    ax3 = axes[2]
    xs=[]
    ys=[]
    for num in sorted(high_counter.keys()):
        num_count = high_counter[num]
        xs.append(num)
        ys.append(num_count)

    high_selected_papers = {}
    for pid in high_selected:
        high_selected_papers[pid] = data[pid]

    open('data/high_selected_papers.json','w').write(json.dumps(high_selected_papers))
    logging.info('high cited papers saved to data/high_selected_papers.json')

    xls = 'Citation Count $x$\n(c)'
    yls = '$N(x)$'
    title = 'high cited papers'
    subplot_scatter(ax3,xs,ys,title,xls,yls)

    ax4= axes[3]
    xls = '$year x\n(d)$'
    yls = '$N(x)$'
    title = 'Selected paper distribution'
    low_xs,low_ys = citation_years(low_selected_papers)
    m_xs,m_ys = citation_years(medium_selected_papers)
    h_xs,h_ys = citation_years(high_selected_papers)
    
    plot_year_dis(ax4,low_xs,low_ys,title,xls,yls,label='low cited papers')
    plot_year_dis(ax4,m_xs,m_ys,title,xls,yls,label='medium cited papers')
    plot_year_dis(ax4,h_xs,h_ys,title,xls,yls,label='high cited papers')
    ax4.legend()

    plt.tight_layout()
    fig_path = '{:}/{:}_{:}_three_levels_papers.pdf'.format(FIGDIR,PROGRAM_ID,PREFIX)
    plt.savefig(fig_path,dpi=300)
    logging.info('fig saved to {:}'.format(fig_path))

def citation_years(cited_papers):
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

if __name__ == '__main__':
    get_three_levels_paper(sys.argv[1],int(sys.argv[2]))




