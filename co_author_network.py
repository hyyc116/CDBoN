#coding:utf-8
"""generating co-author network based on published year"""
import json
import sys
from collections import defaultdict
from collections import Counter
import logging
#logging file
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.DEBUG)

def split_paper_by_year(json_path):
    """Four pre-defined internal"""
    #-80,81-90,91-00,01-10

    data = json.loads(open(json_path).read(),strict=False)['RECORDS']
    paper_zone_dict={}
    count=0
    for paper in data:
        count+=1
        if count%10000:
            logging.info(count)
        pid = paper['pid']
        year = paper['p_year']
        zone = time_zone(year)
        paper_zone_dict[pid]=zone

    open('data/paper_zone_dict.json','w').write(json.dumps(paper_zone_dict))


def time_zone(year):
    if int(year)<1981:
        return 0
    elif int(year) <1991:
        return 1
    elif int(year) <2001:
        return 2
    elif int(year) <2011:
        return 3
    else:
        return 4


def gen_co_author_network(json_path):
    """based on the time zone, generate co-author-network"""
    paper_zone_dict = json.loads(open('data/paper_zone_dict.json').read(),strict=False)
    data = json.loads(open(json_path).read(),strict=False)['RECORDS']
    paper_authors=defaultdict(list)
    for record in data:
        # print record
        aid=str(record.get('aid','-1'))
        pid=str(record.get('pid','-1'))
        if pid=='-1' or aid=='-1':
            continue
        paper_authors[pid].append(int(aid))

    logging.info('generating coauthor network')

    zone_coauthor_network = defaultdict(list)
    zone_authors=defaultdict(list)
    zone_papers=defaultdict(int)
    zone_all_papers= defaultdict(int)
    for pid in paper_authors.keys():
        alist = paper_authors[pid]
        zone = paper_zone_dict.get(pid,'-1')
        if zone=='-1':
            continue
        zone_all_papers[zone]+=1
        if len(alist)<2:
            continue
        zone_authors[zone].extend(alist)
        zone_papers[zone]+=1
        for e in generate_coauthor_edge(alist):
            if len(e.split(" "))!=2:
                print e
                continue
            zone_coauthor_network[zone].append(e)

    #write edges to file
    logging.info('saving')
    for zone in zone_coauthor_network.keys():
        lines = []
        #write vetex
        lines.append('*Vertices {:}'.format(len(set(zone_authors[zone]))))
        for author in sorted(list(set(zone_authors[zone]))):
            lines.append('{:} "{:}'.format(author,author))

        ## generate author count 
        # generate_id_author_name(set(zone_authors[zone]))

        
        lines.append('*Arcs')
        for k,v in sorted(Counter(zone_coauthor_network[zone]).items(),key=lambda x:x[1],reverse=True):
            lines.append("{:} {:}".format(k,v))
        logging.info('====Zone {:}===='.format(zone))
        logging.info('{:} edges between {:} unique authors in {:} papers. Average number of users is {:.2f}.'.format(len(lines),len(set(zone_authors[zone])),zone_papers[zone],len(zone_authors[zone])/float(zone_papers[zone])))
        logging.info('{:} papers with at least two authors in all {:} papers, occupy {:.4f}.'.format(zone_papers[zone],zone_all_papers[zone],float(zone_papers[zone])/zone_all_papers[zone]))
        
        open('data/zone-{:}.net'.format(zone),'w').write('\n'.join(lines))


def generate_coauthor_edge(alist):
    for i in range(len(alist)):
        j=i+1
        while j<len(alist):

            if alist[i]>alist[j]:
                yield '{:} {:}'.format(alist[j],alist[i])
            else:
                yield '{:} {:}'.format(alist[i],alist[j])
            j+=1


if __name__=="__main__":
    # split_paper_by_year('data/aminer_paper.json')
    # logging.info('Done')
    gen_co_author_network('data/aminer_author2paper.json')




