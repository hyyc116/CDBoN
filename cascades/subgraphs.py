#coding:utf-8

from collections import defaultdict
from basic_config import *


def read_cascade(cascade_path):
    cc = json.loads(open(cascade_path).read())

    j = {}
    for pid in cc.keys():

        logi+=1
        if logi%10000==1:
            logging.info('progress {:}'.format(logi))
        citation_count = cc[pid]['cnum']

        if citation_count == 500:
            edges = cc[pid]['edges']
            j['e'] = edges
            break

    open('graph_500.json','w').write(json.dumps(j))

if __name__ == '__main__':
    read_cascade(sys.argv[1])



# D=defaultdict(list)


# def addedge(a,b):
#     D[a].append(b)
#     D[b].append(a)

# addedge(1,2)
# addedge(2,3)
# addedge(3,4)
# addedge(3,5)
# addedge(3,6)
# addedge(3,7)
# addedge(6,8)
# addedge(5,9)
# addedge(4,10)
# addedge(3,11)
# addedge(7,12)
# addedge(10,13)
# V=D.keys()
# k=5

# def F(X,Y):
#     if len(X)==k:
#         return
#     if X:
#         T = set(a for x in X for a in D[x] if a not in Y and a not in X)
#     else:
#         T = V
#     Y1=set(Y)
#     for v in T:
#         X.add(v)
#         print X
#         F(X,Y1)
#         X.remove(v)
#         Y1.add(v)

# F(set(),set())
