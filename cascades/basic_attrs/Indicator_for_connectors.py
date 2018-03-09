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


    depth_cr=defaultdict(list)
    level_cat_list =defaultdict(lambda:defaultdict(list))
    for cr,depth,n_citation,pid in nc_list:
        # if n_citation>260:
        depth_cr[depth].append(cr)

        level_cat_list['ALL']['cr'].append(cr)
        level_cat_list['ALL']['depth'].append(depth)

        if n_citation<22:
            level_cat_list['LOW']['cr'].append(cr)
            level_cat_list['LOW']['depth'].append(depth)
        elif n_citation<260:
            level_cat_list['MEDIUM']['cr'].append(cr)
            level_cat_list['MEDIUM']['depth'].append(depth)
        else:
            level_cat_list['HIGH']['cr'].append(cr)
            level_cat_list['HIGH']['depth'].append(depth) 

    data=[]
    xlabels=[]
    for depth in sorted(depth_cr.keys()):
        xlabels.append(depth)
        data.append(depth_cr[depth])

    fig,ax = plt.subplots(figsize=(10,5))
    ax.boxplot(data)
    ax.set_xlabel('Depth')
    ax.set_ylabel('Conversion Rate')

    plt.tight_layout()
    plt.savefig('pdf/mag_connector_cr.png',dpi=200)

    logging.info('Saved to pdf/mag_connector_cr.png.')

    for level in level_cat_list.keys():
        cl = level_cat_list[level]['cr']
        dl = level_cat_list[level]['depth']
        score,p = pearsonr(cl,dl)

        print level,score,p



if __name__ == '__main__':
    # mag_indicators_for_connectors()
    draw_box(sys.argv[1])






















