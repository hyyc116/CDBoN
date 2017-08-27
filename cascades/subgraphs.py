#coding:utf-8
'''
the algorithm of get all connected graph refers to https://stackoverflow.com/questions/18837026/an-algorithm-to-get-all-connected-subgraphs-from-graph-is-it-correct

'''
from collections import defaultdict
from basic_config import *
import time

def read_cascade(cascade_path):
    cc = json.loads(open(cascade_path).read())

    j = {}
    logi=0
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

def get_subgraphs():
    edges = json.loads(open('graph_500.json').read())['e']
    print 'length',len(edges)
    subgraphs = []

    D=defaultdict(list)

    def addedge(a,b):
        D[a].append(b)
        D[b].append(a)

    for e in edges:
        addedge(e[0],e[1])

    V=D.keys()
    k=4

    def F(X,Y):
        if len(X)==k:
            return
        if X:
            T = set(a for x in X for a in D[x] if a not in Y and a not in X)
        else:
            T = V
        Y1=set(Y)
        for v in T:
            X.add(v)
            if len(X)>2:

                if len(subgraphs) %1000 ==0:
                    print len(subgraphs)
                subgraphs.append(X)

            F(X,Y1)
            X.remove(v)
            Y1.add(v)
    start = time.time()
    F(set(),set())
    end = time.time()
    print 'total time:',end-start


def plot_subgraph():
    ns = []
    for line in open('graph.size.txt'):
        line = line.strip().split('.')[0].split('_')
        size,i,n = line[0],line[1],int(line[2])
        ns.append(n)

    ns = sorted(ns,reverse=True)
    total = float(sum(ns))
    xs = []
    acc_n = 0
    x =0
    y=0
    max_n = ns[0]
    for i,n in enumerate(ns):
        xs.append(i+1)
        if acc_n/total<0.9 and (acc_n+n)/total>0.9:
            x=i
            y=n

        acc_n+=n


    # x = np.array(range(len(ns)))+1
    plt.plot(xs,ns)
    plt.xscale('log')
    plt.yscale('log')
    plt.plot([x]*10,np.linspace(10,max_n,10),'--',c='r')
    plt.plot(np.linspace(10,1000,10),[y]*10,'--',c='r')
    plt.text(300,1000,"({:},{:})".format(x,y))
    plt.savefig('a.png',dpi=200)


def weakly_components():
    dig = nx.DiGraph()
    dig.add_edges_from([(1,2),(2,3),(1,4),(1,5),(4,5),(3,5),(7,8),(8,9)])
    for sub in nx.weakly_connected_component_subgraphs(dig):
        print sub.edges()


if __name__ == '__main__':
    # read_cascade(sys.argv[1])
    # plot_subgraph()
    weakly_components()




