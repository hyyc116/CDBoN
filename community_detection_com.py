#coding:utf-8
import hdbscan
import numpy as np
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.DEBUG)

def read_emb(path):
    pids=[]
    data=[]
    for line in open(path):
        splits=line.strip().split()
        if len(splits)==2:
            logging.info('{:} with {:} dimensions.'.format(splits[0],splits[1]))
            continue
        pids.append(splits[0])
        data.append([float(i) for i in splits[1:]])

    return pids,np.array(data)

def cluster(path,save):
    pids,data = read_emb(path)
    logging.info('length of papers {:}'.format(len(pids)))
    # print data[0]
    clusterer = hdbscan.HDBSCAN(min_cluster_size=15,min_samples=30).fit(data)
    labels = clusterer.labels_
    if len(labels)!=len(pids):
        sys.stderr.write('Wrong labels')
        return

    logging.info('Clustering result get {:} labels'.format(len(set(labels))))
    # print len(set(labels))

    lines=[]
    for i,pid in enumerate(pids):
        lines.append('{:} {:}'.format(pid,labels[i])) 

    logging.info('result length: {:}'.format(len(lines)))
    open(save,'w').write('\n'.join(lines))


if __name__ == '__main__':
    cluster('data/embs/zone-0.emd','data/results/zone-0-emd.txt')