#coding:utf-8
from para_config import *

#given the citation network json file, return the citation number distribution json file before year n
def citation_count_json(citation_network_path,N):
    logging.info('stat numbers of citation before year {:}'.format(N))
    data = json.loads(open(citation_network_path).read())
    citation_num_list = [] 
    for k in data.keys():
        if data[k]['year']>N:
            continue
        citation_num_list.append(len(data[k]['citations']))

    num_counter = Counter(citation_num_list)

    filename = '{:}/{:}_{:}_citation_num_dict_b{:}.json'.format(DATADIR,PROGRAM_ID,PREFIX,N)

    open(filename,'w').write(json.dumps(num_counter))

    logging.info('citation distribution statistics file saved to {:}'.format(filename))

    return num_counter

#plot the citation distribution, and the statistics of three cited levels
def plot_citation_num(num_counter):

    logging.info('plot citation distribution and paper distribution over cited levels')

    data = num_counter
    xs=[]
    ys=[]
    total_count=0
    low_citation_count=0
    high_citation_count=0
    for count in sorted(data.keys()):
        # if count<10:
        #     continue
        xs.append(count)
        total_count+=data[count]
        ys.append(data[count])

        if count<=10:
            low_citation_count+=data[count]
        if count>1000:
            high_citation_count+=data[count]

    medium_count = total_count-high_citation_count-low_citation_count
    logging.info('total number of papers:{:}'.format(total_count))
    logging.info('total number of low cited papers:{:}'.format(low_citation_count))
    logging.info('total number of medium cited papers:{:}'.format(medium_count))
    logging.info('total number of high cited papers:{:}'.format(high_citation_count))

    popt,pcov = curve_fit(power_low_func,xs[30:400],ys[30:400])
    logging.info('the alpha value of power law is {:.2f}'.format(popt[0]))

    logging.info('plot citation distribution...')
    fig,axes = plt.subplots(1,2,figsize=(10,5))
    ax = axes[0]
    ax.plot(xs,ys,'o',fillstyle='none')
    ax.plot(np.linspace(10, 1000, 10), power_low_func(np.linspace(10, 1000, 10), *popt),c='r',label='$\\alpha={:.2f}$'.format(popt[0]))
    ax.plot([10]*10,np.linspace(10**3, 10**5, 10),'--',c='r')
    ax.plot(xs,xs,'--',label='$y=x$')

    ax.text(20,5*10**4,'$x_{low}$')
    ax.text(100,2*10**2,'$x_{medium}$')
    ax.text(2000,5*10**0,'$x_{high}$')
    ax.set_title('Citation distribution',fontsize=15)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('$x$\n(c)',fontsize=10)
    ax.set_ylabel('$N(x)$',fontsize=10)
    ax.legend()

    logging.info('plot paper distribution...')
    ax2 = axes[1]
    xs=['$x<=x_{low}$','$x_{low}<x<x_{high}$','$x>=x_{high}$']
    ys=[low_citation_count,medium_count,high_citation_count]
    x_pos = x_pos = np.arange(len(xs))
    rects = ax2.bar(x_pos,ys,align='center',width=0.3)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(xs)
    ax2.set_xlabel('Levels\n(d)',fontsize=10)
    ax2.set_ylabel('Number of papers',fontsize=10)
    ax2.set_title('Paper distribution',fontsize=15)
    ax2.set_yscale('log')
    ax2.set_ylim(1,10**6.5)
    autolabel(rects,ax2,total_count)

    plt.tight_layout()
    fig_path = '{:}/{:}_{:}_citation_distribution.pdf'.format(FIGDIR,PROGRAM_ID,PREFIX)
    plt.savefig(fig_path,dpi=300)
    logging.info('fig saved to {:}'.format(fig_path))

def main():
    num_counter = citation_count_json(sys.argv[1],int(sys.argv[2]))
    plot_citation_num(num_counter)


if __name__ == '__main__':
    main()
