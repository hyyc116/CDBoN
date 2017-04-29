#coding:utf-8
from para_config import *
from friction_plots import *

def paper_distribution(loaded_papers_json,ax=None,index=None):
    year_dict=defaultdict(int)
    for k in loaded_papers_json.keys():
        paper_dict = loaded_papers_json[k]
        pid = paper_dict['pid']
        year = paper_dict['year']
        year_dict[year]+=1
    
    if ax is None:
        num = len(plt.get_fignums())
        plt.figure(num)
        fig,ax = plt.subplots(figsize=(5,5))

    xs = []
    ys = []
    for year in sorted(year_dict.keys()):
        xs.append(year)
        ys.append(year_dict[year])
    
    logging.info('paper distribution...')

    title = 'Paper distribution over published year'
    xls = 'published year'
    if index is not None:
        xls += '\n{:}'.format(index)
    yls = 'Number of papers'
    subplot_line(ax,xs,ys,title,xls,yls)
    ax.set_xlim(1930,2020)
    logging.info('plot done...')
    if ax is None:
        plt.tight_layout()
        fig_path = '{:}/{:}_{:}_citation_dis.pdf'.format(FIGDIR,PROGRAM_ID,PREFIX)
        plt.savefig(fig_path,dpi=300)


#calculate the period of citation age
def citation_ages(loaded_papers_json,ax=None,index=None):
    logging.info('citation age with index {:}'.format(index))
    age_dict=defaultdict(list)
    for k in loaded_papers_json.keys():
        paper_dict = loaded_papers_json[k]
        pid = paper_dict['pid']
        year = paper_dict['year']
        citations = [int(cit.split(',')[1]) for cit in paper_dict['citations']]
        age = np.max(citations)-year
        age_dict[year].append(age)

    if ax is None:
        num = len(plt.get_fignums())
        plt.figure(num)
        fig,ax = plt.subplots(figsize=(5,5))
    
    xs = []
    ys = []
    avg = []
    for year in sorted(age_dict.keys()):
        xs.append(year)
        ys.append(sum(age_dict[year])/float(len(age_dict[year])))
        if year>1980:
            avg.append(sum(age_dict[year])/float(len(age_dict[year])))

    a_avg = sum(avg)/float(len(avg))
    title = 'Average Citation Age of papers published at year x'
    xls = 'published year x'
    if index is not None:
        xls += '\n{:}'.format(index)
    yls = 'Average Citation Age'
    subplot_line(ax,xs,ys,title,xls,yls)
    ax.plot(np.linspace(1980,2020,10),[a_avg]*10,'--',label='mean:{:.2f}'.format(a_avg))
    ax.set_xlim(1930,2020)
    ax.legend()
    logging.info('plot done...')
    if ax is None:
        plt.tight_layout()
        fig_path = '{:}/{:}_{:}_citation_ages.pdf'.format(FIGDIR,PROGRAM_ID,PREFIX)
        plt.savefig(fig_path,dpi=300)


def citation_dis_age(citation_network_path):
    logging.info('plot paper distribution and citation ages dis...')
    cited_papers = json.loads(open(citation_network_path).read())
    num = len(plt.get_fignums())
    plt.figure(num)
    fig,axes = plt.subplots(1,2,figsize=(10,5))
    ax1 = axes[0]
    index = '(a)'
    # citation distribution
    paper_distribution(cited_papers,ax1,index=index)
    ax2 = axes[1]
    index = '(b)'
    citation_ages(cited_papers,ax2,index=index)

    plt.tight_layout()
    fig_path = '{:}/{:}_{:}_citation_dis_ages.pdf'.format(FIGDIR,PROGRAM_ID,PREFIX)
    logging.info('fig saved to {:}'.format(fig_path))
    plt.savefig(fig_path,dpi=300)

if __name__ == '__main__':
    citation_dis_age(sys.argv[1])
