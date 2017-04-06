import numpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import math
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser()

parser.add_argument('-input', default = '', help = 'input file')
parser.add_argument('-label', default = '', help = 'label file')
parser.add_argument('-index', default = '', help = 'index file')
parser.add_argument('-words', default = '', help = 'words file')
parser.add_argument('-output', default = '', help = 'output file')
parser.add_argument('-range', default = '', help = 'axis range')
parser.add_argument('-size', default = '', help = 'minimum cluster size used')

args = parser.parse_args()


#load the frequency dic
words_path = args.words 
if words_path =="":
    sys.stderr.write("no words file!")
    sys.exit(0) 

index_author = {}
index_pc={}

for line in open(words_path):
    line = line.strip()
    splits=line.split("\t")
    aid = splits[0]
    author = splits[1]
    count = int(splits[2])
    index_author[aid] = author
    index_pc[aid]=count

label = []
if args.label != '':
    for line in open(args.label):
        label.append(line.strip())

indexes = []
if args.index !='':
    indexes=[index.strip() for index in open(args.index)]

N = M = 0
all_data = {}
for i, line in enumerate(open(args.input)):
    vec = line.strip().split(' ')
    if i == 0:
        N = int(vec[0])
        M = int(vec[1])
    elif i <= N:
        if args.label == '':
            label.append(0)
        all_data.setdefault(label[i-1], []).append((float(vec[-2]), float(vec[-1]),indexes[i-1]))

labels=[]
mini_size= (1 if args.size=="" else int(args.size))

#filter out small clusters
for ll in all_data.keys():
    if len(all_data[ll])> int(mini_size):
        labels.append(ll)

clusters_count = len(labels) - (1 if -1 in labels else 0)
colors = plt.cm.rainbow(numpy.linspace(0, 1, clusters_count))

for color, ll in zip(colors, sorted(labels)):

    if ll == "-1":
        color="k"

    for t in all_data[ll]:
        x = t[0]
        y = t[1]
        index = t[2]
        if index_pc.get(index,-1)==-1:
            count=1
            author='NONE'
        else:
            count = index_pc[index]
            author = index_author[index]
        if int(count)>10:
            plt.plot(x, y, '.', color = color, markersize = math.log(int(count)/10+1)+1)
        # plot the corresponding word at this position
            if count>300:
                plt.text(x, y, author, fontsize=math.log(int(count)/10)+1)

plt.title('Estimated number of clusters: %d' % len(labels))

if args.range != '':
    l = abs(float(args.range))
    plt.xlim(-l, l)
    plt.ylim(-l, l)
plt.savefig(args.output, dpi = 300)



