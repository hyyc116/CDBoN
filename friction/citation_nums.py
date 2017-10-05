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

        if count<=14:
            low_citation_count+=data[count]
        if count>1000:
            high_citation_count+=data[count]

    medium_count = total_count-high_citation_count-low_citation_count
    logging.info('total number of papers:{:}'.format(total_count))
    logging.info('total number of low cited papers:{:}'.format(low_citation_count))
    logging.info('total number of medium cited papers:{:}'.format(medium_count))
    logging.info('total number of high cited papers:{:}'.format(high_citation_count))

    popt,pcov = curve_fit(power_low_func,xs[24:700],ys[24:700])
    logging.info('the alpha value of power law is {:.2f}'.format(popt[0]))

    logging.info('plot citation distribution...')
    fig,axes = plt.subplots(1,2,figsize=(10,5))
    ax = axes[0]
    ax.plot(xs,ys,'o',fillstyle='none')
    ax.plot(np.linspace(15, 1000, 10), power_low_func(np.linspace(15, 1000, 10), *popt),c='r',label='$\\alpha={:.2f}$'.format(popt[0]))
    ax.plot([14]*10,np.linspace(10**3, 10**4.5, 10),'--',c='r')
    ax.plot([1000]*10,np.linspace(0.9, 10**2, 10),'--',c='r')
    ax.plot(xs,xs,'--',label='$y=x$')

    ax.text(2,10**3.5,'$x_{low}=14$')
    ax.text(100,2*10**2,'$x_{medium}=100$')
    ax.text(1050,5*10**0,'$x_{high}=1000$')
    ax.set_title('Citation distribution',fontsize=15)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Citation count $x$\n(c)',fontsize=10)
    ax.set_ylabel('$N(x)$',fontsize=10)
    ax.legend()

    para_xs= xs
    para_ys = ys 

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

    paras_square(para_xs,para_ys)



def main():
    num_counter = citation_count_json(sys.argv[1],int(sys.argv[2]))
    plot_citation_num(num_counter)


def paras_square(xs,ys):

    rxs=[]
    rys=[]
    rzs=[]

    fig,axes = plt.subplots(12,8,figsize=(40,60))
    for i,start in enumerate([5,10,15,20,21,22,23,24,25,30,40,50]):
        for j,end in enumerate([200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000]):


            for xi,v in enumerate(x):
                if v>j:
                    end = xi-1
                    break

            x = xs[start:end]
            y = ys[start:end]

            popt,pcov = curve_fit(power_low_func,x,y)
            fit_y = power_low_func(x, *popt)
            r2 = r2_score(np.log(y),np.log(fit_y))*len(x)/float(len(xs))

            print start,end,r2,popt[0],x[-1],len(x)/float(len(xs))

            ax = axes[i,j]

            ax.plot(xs,ys,'o',fillstyle='none')
            ax.plot(x,fit_y,label='$\\alpha={:4f}$,\n $Global R^2={:.10f}$'.format(popt[0],r2))
            ax.legend()

            rxs.append(start)
            rys.append(end)
            rzs.append(r2)

            ax.set_yscale('log')
            ax.set_xscale('log')
            ax.set_title('{:}-{:}'.format(x[0],x[-1]))

    plt.tight_layout()
    plt.savefig('fitting_lines.png',dpi=200)
    
    fig=plt.figure()
    ax = Axes3D(fig)
    ax.plot_wireframe(rxs,rys,rzs)
    plt.savefig('para_space.pdf',dpi=200)


if __name__ == '__main__':
    main()

