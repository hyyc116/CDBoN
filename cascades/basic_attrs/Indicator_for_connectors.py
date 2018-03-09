#coding:utf-8

from basic_config import *


## 对每一个citation cascade中的connector的属性只进行分析
def mag_indicators_for_connectors():

    pid_citation = defaultdict(int)
    read_index=0
    ## 对所有可能存在的id的citation数量进行读取
    for line in open('data/mag/mag_all_nodes_paper_objs.txt'):
        line = line.strip()
        read_index+=1
        if read_index%100==1:
            logging.info('loading paper obj {:} th ...'.format(read_index))
        d = json.loads(line)
        for pid in d.keys():
            pid_citation[pid] = d[pid]['n_citation']

    logging.info('Number of all papers:{:}.'.format(len(pid_citation.keys())))


    ## 从mag_cs_cascade_attrs.txt中读取每个pid的citation的depth, od, id
    ## id大于0的就表示该node为connector
    nc_depth = []
    cr_depth = []
    read_index=0
    for line in open('data/mag/mag_cs_cascade_attrs.txt'):
        read_index+=1
        line = line.strip()
        ca = json.loads(line)
        if read_index%10==1:
            logging.info('loading cascade attrs {:} th ...'.format(read_index))

        for pid in ca.keys():
            n_citation = len(ca[pid].keys())
            for cpid in ca[pid].keys():
                obj= ca[pid][cpid]

                depth = obj['depth']
                od = obj['od']
                ind = obj['id']

                if ind>0:

                    nc = int(pid_citation[cpid])
                    if nc!=-1:
                        nc_depth.append([nc,depth,n_citation,pid])

                        cr = float(ind)/nc
                        cr_depth.append([cr,depth,n_citation,pid])

    out_json ={}
    out_json['nc'] = nc_depth
    out_json['cr'] = cr_depth
    open('data/mag/mag_connector.json','w').write(json.dumps(out_json)+"\n")


def draw_box(mag_connector):
    logging.info('loading data ... ')
    mag_connector_obj = json.loads(open(mag_connector).read())
    nc_list = mag_connector_obj['nc']
    cr_list = mag_connector_obj['cr']

    logging.info('plotting CR ... ')


    cc_pid_crs =defaultdict(lambda:defaultdict(list))
    for cr,depth,n_citation,pid in cr_list:
        cc_pid_crs[n_citation][pid].append(cr)

    cxs=[]
    acr=[]
    for cc in cc_pid_crs.keys():
        for pid in cc_pid_crs[cc].keys():
            cxs.append(cc)
            acr.append(np.mean(cc_pid_crs[cc][pid]))

    fig,ax = plt.subplots(figsize=(5,5))
    plot_heat_scatter(cxs,acr,ax,fig)

    ax.set_xscale('log')
    ax.set_xlabel('citation count')
    ax.set_ylabel('ACR')
    ax.set_title('Average Conversion Rate')

    plt.tight_layout()
    plt.savefig('pdf/mag_acr.png',dpi=200)


if __name__ == '__main__':
    # mag_indicators_for_connectors()
    draw_box(sys.argv[1])






















