#coding:utf-8
from para_config import *
from scipy.stats import norm



def plot_diffusion_inno_sim():
    mu=25
    sigma=10
    # bins = np.linspace(0,20,1000)
    s = [int(i)+1 for i in np.random.normal(mu, sigma, 10)]
    print s
    # print s
    count, bins, ignored = plt.hist(s, 50,normed=True)
    print bins
    plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
               np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
         linewidth=2)
    # plt.show()
    plt.savefig('sim.pdf',dpi=300)


def plot_sim(mean,var,count,path):
    fig,axes = plt.subplots(2,3,figsize=(15,10))

    ax1 = axes[0,0]
    sample_x = [0]
    r_count = 0
    while sample_x[0]<=0:
        r_count+=1
        print r_count
        if r_count>1000:
            break
        sample_x = sorted([int(i)+1 for i in np.random.normal(mean, var, count)])

    sample_x = [sx for sx in sample_x if sx >=0 and sx <=50]
    ax1.hist(sample_x,50,alpha=0.5,label='sampling from N({:},{:})'.format(mean,var))

    dist = norm(mean,var)
    sim_x = np.linspace(0,50,50)
    pdf_y = dist.pdf(sim_x)*count
    cdf_y = dist.cdf(sim_x)*count

    ax1.plot(sim_x,pdf_y,'--',c='r',label='N({:},{:})'.format(mean,var))
    ax1.set_xlabel('t\n(a)')
    ax1.set_ylabel('Number of citations')
    ax1.set_title('Citation Curve')
    ax1.legend()

    ax2 = axes[0,1]
    ax2.plot(sim_x,cdf_y,'--',c='r',label='Simulation')
    counter = Counter(sample_x)
    xs=[]
    ys=[]
    all_count=0
    for year in sorted(counter.keys()):
        xs.append(year)
        all_count+=float(counter[year])
        ys.append(all_count)

    ax2.plot(xs,ys,label='Sampling',alpha=0.7)
    ax2.set_xlabel('t\n(b)')
    ax2.set_ylabel('Number of citations')
    ax2.set_title('Accumulative Citation Curve')
    ax2.legend()

    #average speed
    ax3=axes[0,2]
    ax3.plot(xs,np.array(ys)/(np.array(xs)+1),label='Sampling')
    ax3.plot(sim_x,cdf_y/(np.array(sim_x)+1),'--',c='r',label='Simulation')
    ax3.set_xlabel('t\n(c)')
    ax3.set_ylabel('Number of citations')
    ax3.set_title('Average Speed')
    ax3.legend()


    ax6 = axes[1,0]
    xs = []
    ys = []
    for i in range(50):
        yc = 0
        for sx  in sample_x:
            if sx > i+1:
                break
            yc+=1
        if yc >0:
            ys.append(float(yc))
            xs.append(float(i))

    print xs
    print ys
    ax6.plot(xs,(np.array(xs)+1)/np.array(ys),label='sampling')
    ax6.plot(sim_x,(sim_x+1)/cdf_y,'--',c='r',alpha=0.8,label='simulation')
    ax6.set_xlabel('t\n(d)')
    ax6.set_ylabel('Average time')
    ax6.set_title('Average Time of receiving one citation')
    ax6.legend()

    ax4 = axes[1,1]
    xs = []
    ys=[]
    for i,y in enumerate(sample_x):
        ys.append(y)
        xs.append(i)

    ax4.plot(xs,ys,label='sampling')

    xs = []
    ys = []
    pi = 0
    for i,y in enumerate(pdf_y):
        for j in range(int(y)):
            pi+=1
            xs.append(pi)
            ys.append(sim_x[i])
    ax4.plot(xs,ys,'--',c='r',label='simulation')
    ax4.set_xlabel('$i^{th}$ citation\n(e)')
    ax4.set_ylabel('Length of time')
    ax4.set_title('Time required to receive certain citations')
    ax4.legend()

    ax5 = axes[1,2]
    last_i=0
    # xs = range(0,count)
    ys = []
    for i,y in enumerate(sample_x):
        ys.append(y-last_i)
        last_i=y
    xs = range(1,len(ys)+1)
    ax5.plot(xs,ys)
    ax5.set_xlabel('$i^{th}$ citation\n(f)')
    ax5.set_ylabel('Length of time')
    ax5.set_title('Time required to receive one more citation')

    

    plt.tight_layout()
    plt.savefig(path,dpi=300)


def another(mean,var,count,path):
    fig,axes = plt.subplots(1,4,figsize=(20,5))
    ax1=axes[0]

    real_x = [0]
    rcount=0
    while real_x[0]<=0:
        rcount+=1
        print 'repeat',rcount
        if rcount>1000:
            break
        real_x = sorted([int(i)+1 for i in np.random.normal(mean, var, count)])

    real_x = [rx for rx in real_x if rx>=0 and rx<=50]

    ax1.hist(real_x,50,alpha=0.5)

    dist  = norm(mean,var)
    x = np.linspace(0,50,50)
    pdf_y = dist.pdf(x)*count
    cdf_y = dist.cdf(x)*count
    ax4 = ax1.twinx()
    # print var
    # print cdf_y
    ax4.plot(x,pdf_y,'--',label='pdf',c='r')
    ax4.plot(x,cdf_y,label='cdf')

    print sum(dist.pdf(x))
    ax2 = axes[1]
    # ax2.plot(x,(x+1)/cdf_y,'--',c='r')
    xs = []
    ys = []
    for i in range(50):
        yc = 0
        for rx  in real_x:
            if rx > i+1:
                break
            yc+=1
        if yc >0:
            ys.append(float(yc))
            xs.append(float(i))

    print xs
    print ys
    ax2.plot(xs,(np.array(xs)+1)/np.array(ys))
    ax5=ax2.twinx()
    ax5.plot(x,(x+1)/cdf_y,'--',c='r',alpha=0.8)



    last_i=0
    # xs = range(0,count)
    ys = []
    for i,y in enumerate(real_x):
        ys.append(y-last_i)
        last_i=y
    xs = range(1,len(ys)+1)
    ax3 = axes[2]
    ax3.plot(xs,ys)

    ax6 = axes[3]

    xs = []
    ys=[]
    for i,y in enumerate(real_x):
        ys.append(y)
        xs.append(i)

    ax6.plot(xs,ys)

    plt.tight_layout()
    plt.savefig(path,dpi=300)




if __name__ == '__main__':
    # plot_diffusion_inno_sim()
    # for sigma in [1,5,10,15,20,25]:
    #     for count in [10,100,1000]:
    #         pdfname = 'sim_{:}_{:}.pdf'.format(count,sigma)
    #         another(25,sigma,count,pdfname) 
    plot_sim(25,10,100,'sim.pdf')
    # another(25,15,1000,'sim_1000_15.pdf')
    # another(25,5,10,'sim_10_5.pdf')

