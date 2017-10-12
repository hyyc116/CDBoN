#coding:utf-8

import sys
import json
import networkx as nx

cascade_dict={}
for line in open(sys.argv[1]):
    line = line.strip()
    data = json.loads(line)

    cascade_dict.update(data)


selected_pid = '-1'
selected_obj = None
for pid in cascade_dict.keys():
    if cascade_dict[pid]['cc']>1000:
        selected_pid = pid
        selected_obj = cascade_dict[pid]

        break

edges = selected_obj['edges']

## 在图中获得每个node的最大距离
dig  = nx.DiGraph()

dig.add_edges_from(edges)

for node in dig.nodes():
    pass

