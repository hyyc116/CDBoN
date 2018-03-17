#coding:utf-8
'''
@author: hy@tTt
比较两个数据集 aminer以及mag

'''
from basic_config import *


def compare_datasets(aminer_citation_cascade,aminer_papers_json, mag_cs_papers):
    ## 在aminer中找10篇引用最多的文章，比较title 作者 在mag中是否相同
    logging.info("load aminer citation cascade ...")
    aminer_cc = json.loads(open(aminer_citation_cascade).read())

    logging.info('load aminer paper json ...')
    aminer_papers =  json.loads(open(aminer_papers_json).read())

    logging.info('load paper citations ...')
    pid_citations = {}
    for pid in aminer_cc.keys():
        cc = aminer_cc[pid]['cnum']

        pid_citations[pid] = cc

    logging.info("get top 10 papers ...")
    top_pids = []
    for pid,num in sorted(pid_citations.items(),key = lambda x:x[1], reverse=True)[10]:
        top_pids.append(pid)

    top_titles_id = {}
    ## title转换成小写，去除多余的空格


    # top_titles = set(top_titles)
    logging.info('load mag cs papers .. ')
    progress = 0
    aminer_mag = defaultdict(list)
    for line in open(mag_cs_papers):
        progress+=1
        if progress%10000==0:
            logging.info("progress {:} ...".format(progress))

        line = line.strip()
        paper = json.loads(line)
        tit = paper.get('title',-1).lower().strip()
        if tit!=-1:
            continue

        if top_titles_id.get(tit,-1)!=-1:
            aminer_mag.append(paper)


    open('data/aminer_mag_comparison.json','w').write(json.dumps(aminer_mag))
    for pid in aminer_mag.keys():
        ## 将 aminer的数据打印
            ### 打印对应的mag数据






