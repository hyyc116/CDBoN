#coding:utf-8

from basic_config import *


def importance():   
    fig,ax = plt.subplots(figsize=(6,5))

    plot_dict = json.loads(open('data/plot_dict.json').read())
    ###plot the comparison figure
    cxs= plot_dict['cxs']
    eys= plot_dict['eys']
    dys= plot_dict['dys']
    dcxs=plot_dict['dcx']
    od_ys = plot_dict['od_ys']
    id_ys = plot_dict['id_ys']

    print 'length of cxs:{:},eys:{:},dcxs:{:},dys:{:},od_ys:{:},id_ys:{:}'.format(len(cxs),len(eys),len(dcxs),len(dys),len(od_ys),len(id_ys))

    # max_dict = defaultdict(int)
    equal_dict=defaultdict(list)
    aminer_percentages = defaultdict(list)
    aminer_einorm = []
    for i in range(len(cxs)):
        sx = cxs[i]
        if eys[i]==cxs[i]:
            equal_dict[sx].append(1)
        else:
            equal_dict[sx].append(0)

            ### 将没有indirect links的文章去掉
            aminer_einorm.append((eys[i]-cxs[i])/float(cys[i]))

            if sx<10:
                aminer_percentages[0].append((eys[i]-cxs[i])/float(cxs[i]))
            elif sx<165:
                aminer_percentages[1].append((eys[i]-cxs[i])/float(cxs[i]))
            else:
                aminer_percentages[2].append((eys[i]-cxs[i])/float(cxs[i]))




    # percentage of  cascade size = ciattion count vs citation count
    print 'percentage of cascade size = edge count'
    e_xs = []
    e_ys = []
    for cc in sorted(equal_dict.keys()):
        e_xs.append(cc)
        y = equal_dict[cc]
        e_ys.append(1- sum(y)/float(len(y)))

    ax.plot(e_xs,e_ys,label='ArnetMiner')
    ax.set_xscale('log')
    # ax0.set_yscale('log')
    # ax.set_title('$P(e=n-1)$')
    ax.set_xlabel('$N(C=n)$')
    ax.set_ylabel('$P(e>n|C=n)$')

    plot_dict = json.loads(open('data/mag/stats/plot_dict.json').read())
    ###plot the comparison figure
    cxs= plot_dict['cxs']
    eys= plot_dict['eys']
    dys= plot_dict['dys']
    dcxs=plot_dict['cxs']
    od_ys = plot_dict['od_ys']
    id_ys = plot_dict['id_ys']

    print 'length of cxs:{:},eys:{:},dcxs:{:},dys:{:},od_ys:{:},id_ys:{:}'.format(len(cxs),len(eys),len(dcxs),len(dys),len(od_ys),len(id_ys))
    # max_dict = defaultdict(int)
    equal_dict=defaultdict(list)
    mag_percentages = defaultdict(list)
    mag_einorm = []
    for i in range(len(cxs)):
        sx = cxs[i]

        if eys[i]==cxs[i]:
            equal_dict[sx].append(1)
        else:
            equal_dict[sx].append(0)

            mag_einorm.append((eys[i]-cxs[i])/float(cxs[i]))

            if sx<22:   
                mag_percentages[0].append((eys[i]-cxs[i])/float(cxs[i]))
            elif sx<260:
                mag_percentages[1].append((eys[i]-cxs[i])/float(cxs[i]))
            else:
                mag_percentages[2].append((eys[i]-cxs[i])/float(cxs[i]))


    # percentage of  cascade size = ciattion count vs citation count
    print 'percentage of cascade size = edge size'
    e_xs = []
    e_ys = []
    _10_y=0
    for cc in sorted(equal_dict.keys()):
        e_xs.append(cc)
        

        y = equal_dict[cc]

        if cc==10:
            _10_y=sum(y)/float(len(y))

        e_ys.append(1- sum(y)/float(len(y)))

    ax.plot(e_xs,e_ys,label='MAG-CS')

    print 1-_10_y
    ax.plot(np.linspace(0.6,10,10),[1-_10_y]*10,'--',c='r')
    ax.plot([10]*10,np.linspace(-0.5,1-_10_y,10),'--',c='r')
    ax.set_xlim(0.9,e_xs[-1])
    ax.set_ylim(-0.01,1.01)

    ax.text(12,0.85,'$({:},{:.4f})$'.format(10,1-_10_y))
    ax.legend()
    plt.tight_layout()
    plt.savefig('pdf/importance.pdf',dpi=200)



    ## 两条累积曲线 
    ## aminer_einorm mag_einorm
    plt.figure(figsize=(6.5,4))
    length = float(len(aminer_einorm))

    einorm_counter = Counter(aminer_einorm)

    xs = []
    ys = []
    small = 0
    for einorm in sorted(einorm_counter.keys()):
        xs.append(einorm)
        v = length-small
        ys.append(v/length)

        small+=einorm_counter[einorm]

    plt.plot(xs,ys,label='ArtnetMiner')
    plt.xlabel('$e_{i-norm}$')
    plt.ylabel('$P(X>e_{i-norm})$')
    plt.tight_layout()
    plt.savefig('pdf/ccdf_aminer.pdf',dpi=200)


    ## aminer_einorm mag_einorm
    plt.figure(figsize=(6.5,4))
    length = float(len(mag_einorm))

    einorm_counter = Counter(mag_einorm)

    xs = []
    ys = []
    small = 0
    for einorm in sorted(einorm_counter.keys()):
        xs.append(einorm)
        v = length-small
        ys.append(v/length)

        small+=einorm_counter[einorm]

    plt.plot(xs,ys,label='ArtnetMiner')
    plt.xlabel('$e_{i-norm}$')
    plt.ylabel('$P(X>e_{i-norm})$')
    plt.tight_layout()
    plt.savefig('pdf/ccdf_aminer.pdf',dpi=200)




    fig,axes = plt.subplots(1,2,figsize=(12,5))
    xs,ys = AD_percentage(aminer_percentages)
    ax = axes[0]
    ax.set_title('ArnetMiner')
    rect = ax.bar(xs,ys,width=0.4)
    autolabel(rect,ax)
    ax.set_xticks(xs)
    ax.set_xticklabels(['Low-impact','Medium-impact','High-impact'])

    xs,ys = AD_percentage(mag_percentages)
    ax = axes[1]
    ax.set_title('MAG-CS')
    rect = ax.bar(xs,ys,width=0.4)
    autolabel(rect,ax)

    ax.set_xticks(xs)
    ax.set_xticklabels(['Low-impact','Medium-impact','High-impact'])

    plt.tight_layout()
    plt.savefig('pdf/freq.pdf',dpi=200)



def AD_percentage(pc):
    
    # num = len(percentage)
    xs = []
    ys = []
    a_count=0
    for i in sorted(pc.keys()):
        xs.append(i)
        ys.append(np.mean(pc[i]))

    return xs,ys



if __name__ == '__main__':
    importance()











    
