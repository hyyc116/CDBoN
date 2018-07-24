#coding:utf-8

from basic_config import *
# from mpl_toolkits.axes_grid.inset_locator import inset_axes

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
            aminer_einorm.append((eys[i]-cxs[i])/float(cxs[i]))

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

    # ax.plot(e_xs,e_ys,label='ArnetMiner')
    ax.set_xscale('log')
    # ax0.set_yscale('log')
    # ax.set_title('$P(e=n-1)$')
    ax.set_xlabel('$C=n$')
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
            print 10,sum(y),len(y)
            _10_y=sum(y)/float(len(y))

        # if cc==2:
        #     print 2,sum(y),len(y)

        e_ys.append(1- sum(y)/float(len(y)))

    ax.plot(e_xs,e_ys,label='MAG-CS')

    print 1-_10_y
    ax.plot(np.linspace(0.6,10,10),[1-_10_y]*10,'--',c='r')
    ax.plot([10]*10,np.linspace(-0.5,1-_10_y,10),'--',c='r')
    ax.set_xlim(0.9,e_xs[-1])
    ax.set_ylim(-0.01,1.01)

    ax.text(12,0.85,'$({:},{:.4f})$'.format(10,1-_10_y))
    # ax.()
    plt.tight_layout()
    plt.savefig('pdf/importance.pdf',dpi=200)


    change_xs=[]
    change_ys =[]
    last_x= -1
    last_y = -1
    for i,x in enumerate(e_xs):
        y = e_ys[i]

        if i>0:
            change_xs.append(i)
            change_ys.append(float(y-last_y)/(x-last_x))

        last_x = x 
        last_y = y


    plt.figure(figsize=(6,5))
    plt.plot(change_xs,change_ys)
    plt.xlabel('$C=n$')
    plt.ylabel('Change Rate')
    plt.xscale('log')
    plt.savefig('pdf/change_rate.pdf',dpi=200)


    ## 两条累积曲线 
    ## aminer_einorm mag_einorm
    plt.figure(figsize=(6.5,5))
    # length = float(len(aminer_einorm))

    # einorm_counter = Counter(aminer_einorm)

    # xs = []
    # ys = []
    # small = 0
    # for einorm in sorted(einorm_counter.keys()):
    #     xs.append(einorm)
    #     v = length-small
    #     ys.append(v/length)

    #     small+=einorm_counter[einorm]

    # plt.plot(xs,ys,label='ArtnetMiner')
    plt.xlabel('$e_{i-norm}$')
    plt.ylabel('$P(X>e_{i-norm})$')
    # plt.tight_layout()
    # plt.savefig('pdf/ccdf_aminer.pdf',dpi=200)

    ## aminer_einorm mag_einorm
    # plt.figure(figsize=(6.5,4))
    length = float(len(mag_einorm))

    einorm_counter = Counter(mag_einorm)

    xs = []
    ys = []
    small = 0
    sub_xs = []
    sub_ys = []
    for einorm in sorted(einorm_counter.keys()):
        xs.append(einorm)
        v = length-small
        ys.append(v/length)

        if einorm > 0.05 and einorm<=5:
            sub_xs.append(einorm)
            sub_ys.append(v/length)


        small+=einorm_counter[einorm]

    plt.plot(xs,ys,label='MAG-CS')
    # plt.xlabel('$e_{i-norm}$')
    # plt.ylabel('$P(X>e_{i-norm})$')
    plt.xscale('log')
    plt.title('Probability')

    # plt.()

    ### add sub plot
    a = plt.axes([.6, .55, .25, .25], facecolor='w')
    plt.plot(sub_xs, sub_ys)
    # plt.xticks([])
    # plt.yticks([])

    # plt.tight_layout()
    plt.savefig('pdf/ccdf_mag.pdf',dpi=200)




    fig,axes = plt.subplots(1,1,figsize=(6,5))
    ax = axes
    # xs,ys,lower_errors,upper_errors = AD_percentage(mag_percentages)
    # asymmetric_error = [lower_errors, upper_errors]
    # ax.errorbar(xs, ys, yerr=asymmetric_error, fmt='-o',capsize=2,label='MAG-CS')

    # for i,x in enumerate(xs):
        # ax.text(x,ys[i],'({:.2f})'.format(ys[i]))
    data = []
    for i in sorted(mag_percentages.keys()):
        # xs.append(i)
        # mean = np.mean(mag_percentages[i])
        data.append(mag_percentages[i])
        # ys.append(mean)

    data = [[row[i] for row in data] for i in range(len(data[0]))]

    ax.boxplot(data,labels=['low-impact','medium-impact','high-impact'],showfliers=False)
    # ax.set_xticks(xs)
    # ax.set_xticklabels()
    ax.set_xlabel('Paper Impact Level')
    ax.set_ylabel('$e_{i-norm}$')
    # ax.()
    plt.tight_layout()
    plt.savefig('pdf/boxplot_mag.pdf',dpi=200)



def AD_percentage(pc):
    
    # num = len(percentage)
    xs = []
    ys = []
    a_count=0
    lower_errors = []
    upper_errors = []
    for i in sorted(pc.keys()):
        xs.append(i)
        mean = np.mean(pc[i])
        ys.append(mean)
        lower_errors.append(mean-np.min(pc[i]))
        upper_errors.append(np.max(pc[i])-mean)
    return xs,ys,lower_errors,upper_errors



if __name__ == '__main__':
    importance()











    
