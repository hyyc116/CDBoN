#coding:utf-8

from basic_config import *


## 对每一个citation cascade中的connector的属性只进行分析
def mag_indicators_for_connectors():

    pid_citation = defaultdict(int)
    ## 对所有可能存在的id的citation数量进行读取
    for line in open('data/mag/mag_all_nodes_paper_objs.txt'):
        line = line.strip()
        read_index+=1
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
            for cpid in ca[pid].keys():
                obj= ca[pid][cpid]

                depth = obj['depth']
                od = obj['od']
                ind = obj['id']

                if ind>0:

                    nc = int(pid_citation[cpid])

                    if nc!=-1:

                        nc_depth.append([nc,depth])

                        cr = float(ind)/nc

                        cr_depth.append([cr,depth])


    out_json ={}
    out_json['nc'] = nc_depth
    out_json['cr'] = cr_depth

    open('data/mag/mag_connector.json','w').write(json.dumps(out_json)+"\n")


if __name__ == '__main__':
    mag_indicators_for_connectors()






















