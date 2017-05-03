#coding:utf-8

from basic_config import *


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
        citation_list = cited_dict.get('citations',{})
        citation_list[pid]=pid_year
        cited_dict['citations']=citation_list
        ref_dict[cited_pid] = cited_dict

    open('data/aminer_citation_dict.json','w').write(json.dumps(ref_dict))
    print 'done'

#after building the citation network, we build citation cascade
def build_cascades(citation_network):
    cn = json.loads(open(citation_network).read())
    logging.info('data loaded...')
    for pid in cn.keys():
        logging.info('paper id:'+str(pid))
        # for a paper, get its dict
        pdict = cn[pid]
        # for its citation dict
        c_dict = pdict['citations']
        citing_pids = c_dict.keys()
        logging.info('Number of citations:{:}'.format(len(citing_pids)))
        edges = []
        for i,cpid in enumerate(citing_pids):
            edges.append([pid,cpid])
            #get cpid's citation dict
            if cn.get(cpid,-1)==-1:
                continue
            cp_dict = cn[cpid]['citations']
            j=i+1
            while j<len(citing_pids):
                
                scpid = citing_pids[j]
                j+=1
                if cp_dict.get(scpid,'-1')=='-1':
                    continue
                else:
                    edges.append([cpid,scpid])

        pdict['edges'] = edges
        pdict['cnum'] = len(citing_pids)
        pdict['enum'] = len(edges)

        cn[pid] = pdict

    open('data/aminer_citation_cascade.json','w').write(json.dumps(cn))
    logging.info('citation cascade saved to data/aminer_citation_cascade.json.')

def cascade_size_distribution(citation_cascade):
    cc = json.loads(open(citation_cascade).read())
    logging.info('data loaded...')
    cnum_dict=defaultdict(int)
    enum_dict=defaultdict(int)
    cxs=[]
    eys=[]
    for pid in cc.keys():
        cnum_dict[cc[pid]['cnum']]+=1
        cxs.append(cc[pid]['cnum'])
        enum_dict[cc[pid]['cnum']]+=1
        eys.append(cc[pid]['cnum'])

    logging.info('plot data...')
    fig,axes = plt.subplots(1,3,figsize=(15,5))
    ax1 = axes[0]
    xs=[]
    ys=[]
    for num in sorted(cnum_dict.keys()):
        xs.append(num)
        ys.append(cnum_dict[num])
    ax1.plot(xs,ys,'o',fillstyle='none')
    ax1.set_title('Citation Count Distribution')
    ax1.set_xlabel('Citation Count')
    ax1.set_ylabel('Number')
    ax1.set_yscale('log')
    ax1.set_xscale('log')

    ax2 = axes[1]
    for num in sorted(enum_dict.keys()):
        xs.append(num)
        ys.append(enum_dict[num])

    ax2.plot(xs,ys,'o',fillstyle='none')
    ax2.set_title('Cascade Size Distribution')
    ax2.set_xlabel('Cascade Size')
    ax2.set_ylabel('Number')
    ax2.set_yscale('log')
    ax2.set_xscale('log')

    ax3 = axes[2]
    bucket_dict=defaultdict(list)
    for i,x in enumerate(cxs):
        bucket_dict[x].append(eys[i]/x)

    all_data=[]
    sorted_keys = sorted(bucket_dict.keys())
    for d in sorted_keys:
        # print '===',d
        all_data.append(bucket_dict[d])

    # print all_data
    ax3.set_xlabel('Citation Count')
    ax3.set_ylabel('Cascade Size / Citation Count'.format(name,name))
    # ax.set_yscale('log')
    # ax.set_ylim(1,1000)
    # ax.set_xlim(0,11)
    ax3.boxplot(all_data,showfliers=False)
    ax3.set_xticks([i for i in np.arange(len(bucket_dict.keys()),500)])
    ax3.set_xticklabels([sorted_keys(i) for i in np.arange(len(bucket_dict.keys()),500)])
    ax3.set_title('Citation Count vs. Cascade Size')
    ax1.set_xlabel('Citation Count')
    ax1.set_ylabel('Cascade Size')


    plt.tight_layout()
    plt.savefig('pdf/cascade_size_dis.pdf',dpi=300)
    logging.info('figures saved to pdf/cascade_size_dis.pdf.')



if __name__ == '__main__':
    # build_citation_network(sys.argv[1])
    # build_cascades(sys.argv[1])
    label = sys.argv[1]
    if label=='cascade_size':
        cascade_size_distribution(sys.argv[2])



