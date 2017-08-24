#coding:utf-8
'''
@author: hyyc116
'''

from basic_config import *
import gc
from multiprocessing.dummy import Pool as ThreadPool
from networkx.algorithms import isomorphism
from matplotlib import cm as CM

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
def build_cascades(citation_network,outpath):
    cn = json.loads(open(citation_network).read())
    logging.info('data loaded...')
    log_count=1
    for pid in cn.keys():
        if log_count%1000==1:
            logging.info('progress:'+str(log_count))

        log_count+=1
        # for a paper, get its dict
        pdict = cn[pid]
        # for its citation dict
        c_dict = pdict['citations']
        citing_pids = c_dict.keys()
        # logging.info('Number of citations:{:}'.format(len(citing_pids)))
        edges = []
        for i,cpid in enumerate(citing_pids):
            edges.append([cpid,pid])
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
                    edges.append([scpid,cpid])

        pdict['edges'] = edges
        pdict['cnum'] = len(citing_pids)
        pdict['enum'] = len(edges)

        cn[pid] = pdict

    open(outpath,'w').write(json.dumps(cn))
    logging.info('citation cascade saved to {:}.'.format(outpath))

def gen_statistics_data(citation_cascade):
    cc = json.loads(open(citation_cascade).read())
    logging.info('data loaded...')
    cnum_dict=defaultdict(int)
    enum_dict=defaultdict(int)
    size_depth_dict=defaultdict(list)
    depth_dict=defaultdict(int)
    od_dict = defaultdict(int)
    in_dict = defaultdict(int)
    logi = 0

    plot_dict = {}
        
    cxs=[]
    eys=[]
    dys=[]
    dcxs=[]
    od_ys = []
    id_ys = []

    zero_od_count=0
    for pid in cc.keys():

        #out-degree count
        od_count=0
        #in-degree count
        id_count=0

        #progress 
        logi+=1
        if logi%10000==1:
            logging.info('progress {:}'.format(logi))
        #number of nodes
        cnum_dict[cc[pid]['cnum']]+=1
        cxs.append(cc[pid]['cnum'])
        #number of edges
        enum_dict[cc[pid]['enum']]+=1
        eys.append(cc[pid]['enum'])

        diG = nx.DiGraph()
        edges = cc[pid]['edges']
        diG.add_edges_from(edges)
        #depth of graph
        if nx.is_directed_acyclic_graph(diG):
            depth=nx.dag_longest_path_length(diG)
            # cascade_depths.append(depth)
            depth_dict[depth]+=1
            # cascade_sizes.append(len(edges))
            size_depth_dict[len(edges)].append(depth)
            dys.append(depth)
            dcxs.append(cc[pid]['cnum'])
        else:
            continue
        #degree
        outdegree_dict = diG.out_degree()
        for nid in outdegree_dict.keys():
            od = outdegree_dict[nid]

            if od==0:
                zero_od_count+=1

            if od>0:
                # out degree
                od_dict[od]+=1
                # in degree
                ind = diG.in_degree(nid)
                in_dict[ind]+=1

                if ind>0:
                    id_count+=1

            ##od 
            if od > 1:
                od_count+=1

        od_ys.append(od_count/float(cc[pid]['cnum']))
        id_ys.append(id_count/float(cc[pid]['cnum']))


    print 'zero od count:',zero_od_count
    open('data/nodes_size.json','w').write(json.dumps(cnum_dict))
    open('data/cascade_size.json','w').write(json.dumps(enum_dict))
    open('data/depth.json','w').write(json.dumps(depth_dict))
    open('data/out_degree.json','w').write(json.dumps(od_dict))
    open('data/in_degree.json','w').write(json.dumps(in_dict))

    
    plot_dict['cxs'] = cxs;
    plot_dict['eys'] = eys;
    plot_dict['dys'] = dys;
    plot_dict['dcx'] = dcxs;
    plot_dict['od_ys'] = od_ys
    plot_dict['id_ys'] = id_ys

    open('data/plot_dict.json','w').write(json.dumps(plot_dict))

def plot_heatmap(x,y,ax,bins,fig,gridsize=30):
    hb = ax.hexbin(x, y, gridsize=gridsize, cmap=CM.Blues, bins='log',xscale=bins[0] ,yscale=bins[1])

# 统计指标的分布图
def stats_plot():
    logging.info('plot data ...')

    num = len(plt.get_fignums())
    # plt.figure(num)
    fig,axes = plt.subplots(1,5,figsize=(25,5))
    #### node size 
    logging.info('plot node size ...')
    cnum_dict = json.loads(open('data/nodes_size.json').read())
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

    #### cascade size
    logging.info('plotting cascade size ...')
    ax2 = axes[1]
    enum_dict = json.loads(open('data/cascade_size.json').read())
    for num in sorted(enum_dict.keys()):
        xs.append(num)
        ys.append(enum_dict[num])

    ax2.plot(xs,ys,'o',fillstyle='none')
    ax2.set_title('Cascade Size Distribution')
    ax2.set_xlabel('Cascade Size')
    ax2.set_ylabel('Number')
    ax2.set_yscale('log')
    ax2.set_xscale('log')


    ####depth
    logging.info('plotting cascade depth ...')
    depth_dict = json.loads(open('data/depth.json').read())
    ax3=axes[2]
    xs=[]
    ys=[]
    for depth in sorted([int(i) for i in depth_dict.keys()]):
        xs.append(int(depth))
        ys.append(depth_dict[str(depth)])

    print xs 
    print ys
    ax3.plot(xs,ys,marker = '.',fillstyle='none')
    ax3.set_xlabel('Cascade depth')
    ax3.set_ylabel('Count')
    ax3.set_title('Cascade depth distribution')
    ax3.set_yscale('log')

    #### In and out degree
    logging.info('plotting degree ...')
    in_degree_dict=json.loads(open('data/in_degree.json').read())
    out_degree_dict=json.loads(open('data/out_degree.json').read())
    ax4 = axes[3]
    xs=[]
    ys=[]
    for ind in sorted(in_degree_dict.keys()):
        xs.append(ind)
        ys.append(in_degree_dict[ind])

    ax4.plot(xs,ys,'.')
    ax4.set_xlabel('In Degree')
    ax4.set_ylabel('Count')
    ax4.set_title('In Degree distribution')
    ax4.set_yscale('log')
    ax4.set_xscale('log')

    # ax2=axes[1]
    # ax2.scatter(cascade_sizes,cascade_depths,marker='.')

    ax5=axes[4]
    xs=[]
    ys=[]
    for od in sorted(out_degree_dict.keys()):
        xs.append(od)
        ys.append(out_degree_dict[od])

    ax5.plot(xs,ys,'.')
    ax5.set_title('Out Degree distribution')
    ax5.set_xlabel('Out Degree')
    ax5.set_ylabel('Count')
    ax5.set_xscale('log')
    ax5.set_yscale('log')

    plt.tight_layout()
    plt.savefig('pdf/statistics.pdf',dpi=300)
    logging.info('figures saved to pdf/statistics.pdf.')

# 随着citation count的增加，各个指标的变化
def plot_dict():

    plot_dict = json.loads(open('data/plot_dict.json').read())
    ###plot the comparison figure

    cxs= plot_dict['cxs']
    eys= plot_dict['eys']
    dys= plot_dict['dys']
    dcxs=plot_dict['dcx']
    od_ys = plot_dict['od_ys']
    id_ys = plot_dict['id_ys']

    for ii,indgree in enumerate(id_ys):
        if indgree==1:
            print cxs[ii],indgree

    num = len(plt.get_fignums())
    # plt.figure(num)
    fig,axes = plt.subplots(2,5,figsize=(25,10))

    print 'length of xs and ys', len(cxs),len(eys),len(dcxs),len(dys),len(od_ys),len(id_ys)

    # cascade size vs citation count
    ax1 = axes[0,0]
    ax1.scatter(cxs,eys)
    ax1.set_xlabel('Citation Count')
    ax1.set_ylabel('Cascade Size')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_title('Cascade Size Dis')
    
    ax11 = axes[1,0]
    plot_heatmap(cxs,eys,ax11,['log','log'],fig)
    ax11.set_xlabel('Citation Count')
    ax11.set_ylabel('Cascade Size')
    ax11.set_title('Cascade Size Dis')

    ## ratio of cascade size/ ciattion count vs citation count
    ax2 = axes[0,1]
    rys = [eys[i]/float(cxs[i]) for i in range(len(cxs))]
    ax2.scatter(cxs,rys)
    ax2.set_xlabel('Citation Count')
    ax2.set_ylabel('Cascade size/citation count')
    ax2.set_xscale('log')
    ax2.set_title('Cascade size/citation count')
    ax12 = axes[1,1]
    plot_heatmap(cxs,rys,ax12,['log','linear'],fig)
    ax12.set_xlabel('Citation Count')
    ax12.set_ylabel('Cascade size/citation count')
    ax12.set_title('Cascade size/citation count')


    ### depth distribution over citation count
    ax3=axes[0,2]
    ax3.scatter(dcxs,dys)
    ax3.set_xlabel('Citation Count')
    ax3.set_ylabel('Depth of citation cascade')
    ax3.set_xscale('log')
    ax3.set_title('Depth Distribution')

    ax13 = axes[1,2]
    plot_heatmap(dcxs,dys,ax13,['log','linear'],fig,(8,8))
    ax13.set_xlabel('Citation Count')
    ax13.set_ylabel('Depth of citation cascade')
    ax13.set_title('Cascade Depth Distribution')

    ### out degree over citation count
    ax4 = axes[0,3]
    ax4.scatter(dcxs,od_ys)
    ax4.set_xlabel('Citation Count')
    ax4.set_ylabel('Percentage')
    ax4.set_xscale('log')
    ax4.set_title('Out degree')

    ax14 = axes[1,3]
    plot_heatmap(dcxs,od_ys,ax14,['log','linear'],fig)
    ax14.set_xlabel('Citation Count')
    ax14.set_ylabel('Percentage')
    ax14.set_title('Out degree(>1) Distribution')

    #### in degree over citation count
    ax5 = axes[0,4]
    ax5.scatter(dcxs,id_ys)
    ax5.set_xlabel('Citation Count')
    ax5.set_ylabel('Percentage')
    ax5.set_xscale('log')
    ax5.set_title('In degree')
    ax15 = axes[1,4]
    plot_heatmap(dcxs,id_ys,ax15,['log','linear'],fig)
    ax15.set_xlabel('Citation Count')
    ax15.set_ylabel('Percentage')
    ax15.set_title('In degree(>0) Distribution')

    plt.tight_layout()
    plt.savefig('pdf/compare.png',dpi=200)
    print 'figure saved to pdf/compare.png'


## 将与根节点的链接的边去掉
def unlinked_subgraph(citation_cascade):
    cc = json.loads(open(citation_cascade).read())
    logging.info('data loaded...')
    for pid in cc.keys():
        yes_count = 0
        edges = cc[pid]['edges']
        # print 'size of cascade:',len(edges)
        new_edges=[]
        for edge in edges:
            source = edge[0]
            target = edge[1]
            
            if int(target)==int(pid):
                yes_count+=1
            else:
                new_edges.append(edge)

        print yes_count
        dig  = nx.DiGraph()
        dig.add_edges_from(new_edges)
        print list(nx.weakly_connected_component_subgraphs(dig))        


###three levels of 
def three_levels_dis():
    high_cited_papers = [i for i in json.loads(open('../friction/data/high_selected_papers.json').read()).keys()]
    medium_cited_papers = [i for i in json.loads(open('../friction/data/medium_selected_papers.json').read()).keys()]
    low_cited_papers = [i for i in json.loads(open('../friction/data/low_selected_papers.json').read()).keys()]

    print high_cited_papers,len(high_cited_papers)
    print medium_cited_papers,len(medium_cited_papers)
    print low_cited_papers,len(low_cited_papers)

    ### low medium high

def main():
    # build_citation_network(sys.argv[1])
    # build_cascades(sys.argv[1])
    label = sys.argv[1]
    if label== 'gen_stat':
        gen_statistics_data(sys.argv[2])
    elif label == 'stat_plot':
        stats_plot()
    elif label == 'build_cascade':
        build_cascades(sys.argv[2])
    elif label =='compare_plot':
        plot_dict()
    elif label=='unlinked_subgraph':
        unlinked_subgraph(sys.argv[2])


if __name__ == '__main__':
    main()

    



