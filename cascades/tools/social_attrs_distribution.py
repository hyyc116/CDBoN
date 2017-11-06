#coding:utf-8
'''
@author: hy@tTt
对于node的社会属性例如field， topic similarity, node importance的分布进行计算

'''
from basic_config import *

def filed_distribution():
    ## field的分布
    ## 读取cascade attrs， data/mag/mag_all_nodes_paper_objs.txt
    paper_fos={}
    num_list = []
    read_index=0
    for line in open('data/mag/mag_all_nodes_paper_objs.txt'):
        line = line.strip()
        read_index+=1
        d = json.loads(line)
        for pid in d.keys():
            n_fos = d[pid]['n_fos']
            if n_fos!="-1":
                ## 一级类别
                fos = list(set([f[0] for f in n_fos]))
                paper_fos[pid]=fos
                num_list.append(len(fos))
        if read_index%100==1:
            logging.info('reading paper obj , the {:}th line ... '.format(read_index))

    logging.info('Number of existing all nodes having fos:{:}'.format(len(paper_fos.keys())))
    logging.info('Average number of field of papers:{:.2f}'.format(np.average(num_list)))

    ## 读取 mag_cs_cascade_attrs 看分布
    cascade_social_attr = {}
    read_index=0
    for line in open('data/mag/mag_cs_cascade_attrs.txt'):
        read_index+=1


        line = line.strip()
        ca = json.loads(line)
        cascade_social_attr.update(ca)

        if read_index%10==1:
            logging.info('loading cascade attrs {:} th ...'.format(read_index))

    ## 对于cascade中每一篇文章，对应的citing papers的分析

    cc_depth_fos_list=[]
    logging.info('processing the depth and field ...')
    read_index=0
    for pid in cascade_social_attr.keys():
        read_index+=1
        ## 引文数量
        cc = len(cascade_social_attr[pid].keys())
        # 对于每一个节点的属性
        for cpid in cascade_social_attr[pid].keys():
            obj = cascade_social_attr[pid][cpid]
            depth = obj['depth']
            ## field of this paper
            fos = paper_fos.get(cpid,'-1')
            if fos!='-1':
                for f in fos:
                    cc_depth_fos_list.append([cc,depth,f])

        if read_index%200000==1:
            logging.info('process the depth, process {:} ...'.format(read_index))

    ### 对于现在的list,画出整体的分布图
    field_list = []
    field_depth = defaultdict(list)
    for cc,depth,f in cc_depth_fos_list:
        field_list.append(f)
        field_depth[f].append(depth)

    total = float(len(field_list))
    fc = Counter(field_list)
    logging.info('field dict {:}'.format(fc))

    open('data/mag/mag_field_dis.json','w').write(json.dumps(fc))
    open('data/mag/mag_field_depth.json','w').write(json.dumps(field_depth))

    logging.info('filed data saved!')

def plot_field_dis():
    fc = json.loads(open('data/mag/mag_field_dis.json').read())
    field_depth = json.loads(open('data/mag/mag_field_depth.json'.read()))

    xs = []
    ys = []

    for x in sorted(fc.keys()):
        xs.append(x)
        ys.append(fc[x]/total)

    plt.figure()
    plt.bar(range(len(xs)),ys)
    # plt.xticks(range(len(xs)),xs, rotation='vertical')
    plt.xlabel('Fields')
    plt.ylabel('Number')
    plt.yscale('log')
    plt.title('General Distribution')
    plt.tight_layout()
    plt.savefig('pdf/mag_field_dis.pdf',dpi=200)
    logging.info('saved to pdf/mag_field_dis.pdf')


    xs=[]
    ys=[]
    for x in sorted(field_depth.keys()):
        xs.append(x)
        ys.append(np.mean(field_depth[x]))

    plt.figure()
    plt.bar(range(len(xs)),ys)
    # plt.xticks(range(len(xs)),xs, rotation='vertical')
    plt.xlabel('Fields')
    plt.ylabel('Average Depth')
    plt.title('Filed Depth')
    plt.tight_layout()
    plt.savefig('pdf/mag_field_depth.pdf',dpi=200)
    logging.info('saved to pdf/mag_field_depth.pdf')

    logging.info('Done')





if __name__ == '__main__':
    filed_distribution()

















