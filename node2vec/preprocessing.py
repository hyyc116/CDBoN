#coding:utf-8
'''
Preprocessing the result of node2vec 
'''

import sys
import numpy as np
from sklearn.cluster import DBSCAN
import json
from collections import defaultdict

# parameter path: the path of files
def transform(path):
    for line in open(path):
        line = line.strip()
        splits = line.split(" ")
        if len(splits)!=2:
            sys.stderr.write(splits[0]+"\n")
            print " ".join(splits[1:])
        else:
            print line


# parameter path: the path of files
def transform_graph(path):
    for line in open(path):
        line = line.strip()
        splits = line.split(" ")
        if len(splits)==3:
            sys.stderr.write(splits[0]+"\n")
            print " ".join(splits[1:])
        else:
            print line

#clustering the 2D result of largevis by DBSCAN from scikit-learn
def dbscan_clustering(path):
    data = [line.strip().split(" ") for line in open(path)][1:]
    data = np.array(data)
    # print len(data)
    #implement dbscan
    db = DBSCAN(eps=0.75, min_samples=5, n_jobs=8).fit(data)
    #labels of X 
    labels = db.labels_
    #core labels
    # core_index = db.core_sample_indices_

    for label in labels:
        print label
    #for core in core_index:
    #    sys.stderr.write(core+"\n")    


def filter_edges(path,N):
    for line in open(path):
        line = line.strip()
        splits = line.split()
        count = int(splits[2])
        if count > N:
            print line 


def undirected_edges(path):
    for line in open(path):
        line = line.strip().replace('\t',' ')
        print line
        splits = line.split(" ")
        print splits[1]+" "+splits[0]+" "+splits[2]

# generate the authorid, papercount, authorname
def generate_id_author_name(index_path):
    author_list = json.loads(open('data/aminer_author.json').read())['RECORDS']
    aids = set([int(aid.strip()) for aid in open(index_path)])
    for author in author_list:
        aid = author['aid']
        name = author['name']
        pc = author['paper_count']
        if aid in aids:
            print str(aid)+"\t"+name.encode('utf-8')+"\t"+str(pc)
    
def generate_id_task(data_path,index_path):
    task_dict=defaultdict(int)
    for line in open(data_path):
        splits = line.split('\t')
        id1 = splits[0]
        id2 = splits[1]
        num = int(splits[2])
        task_dict[id1]+=num
        task_dict[id2]+=num

    for line in open(index_path):
        splits = line.split('\t')
        name = splits[0]
        id1 = splits[1]

        if aid in aids:
            print id1+"\t"+name.encode('utf-8')+"\t"+task_dict[id1]


if __name__=="__main__":
    label = sys.argv[1]
    path = sys.argv[2]
    if label=="transform":
        transform(path)
    elif label=='tg':
        transform_graph(path)
    elif label=="clustering":
        dbscan_clustering(path)
    elif label == "undirected":
        undirected_edges(path)
    elif label == 'ac':
        generate_id_author_name(path)
    elif label =='filtered':
        filter_edges(path,int(sys.argv[3]))
    elif label == 'task':
        generate_id_task(path,sys.argv[3])



