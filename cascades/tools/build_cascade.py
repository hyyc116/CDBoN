#coding:utf-8
'''
@author: hy@tTt
'''
from basic_config import *

#from the aminer_reference.json to build citation network
def build_citation_network(path):
    ref_dict=defaultdict(dict)
    data = json.loads(open(path).read())
    reflist = data['RECORDS']
    ref_size = len(reflist)
    logging.info('loading aminer citation_reference.json, size: {:}'.format(ref_size))
    count=0
    self_citation_count=0
    for ref in reflist:
        count+=1
        if count%10000==1:
            logging.info("progress --  {:}/{:}".format(count,ref_size))
        pid = ref['cpid']
        pid_year = ref['cpid_year']
        cited_pid = ref['pid']
        cited_pid_year = ref['pid_year']

        # 如果是自引，那么不要这一条记录
        if cited_pid == pid:
            self_citation_count+=1
            continue

        if int(pid_year)<1900 or int(cited_pid_year)<1900 or int(pid_year)<int(cited_pid_year):
            continue

        cited_dict = ref_dict.get(cited_pid,{})
        cited_dict['pid'] = cited_pid
        cited_dict['year'] = cited_pid_year
        citation_list = cited_dict.get('citations',{})
        citation_list[pid]=pid_year
        cited_dict['citations']=citation_list
        ref_dict[cited_pid] = cited_dict

    citation_network_path = 'data/aminer_citation_dict.json'
    logging.info('total {:}, self citation count {:}'.format(ref_size,self_citation_count))
    open(citation_network_path,'w').write(json.dumps(ref_dict))
    logging.info('saved to {:}'.format(citation_network_path))
    return citation_network_path

#after building the citation network, we build citation cascade
def build_cascades(citation_network,outpath):
    cn = json.loads(open(citation_network).read())
    logging.info('data loaded...')
    log_count=1
    for pid in cn.keys():
        if log_count%1000==1:
            logging.info('progress:'+str(log_count))

        log_count+=1
        # for a paper, get its dict
        pdict = cn[pid]
        # for its citation dict
        c_dict = pdict['citations']
        citing_pids = c_dict.keys()
        # logging.info('Number of citations:{:}'.format(len(citing_pids)))
        edges = []
        for i,cpid in enumerate(citing_pids):

            if cpid ==pid:
                print 'ERROR'
                continue

            edges.append([cpid,pid])
            #get cpid's citation dict
            if cn.get(cpid,-1)==-1:
                continue
            cp_citing_pid = cn[cpid]['citations'].keys()

            for inter_pid in set(cp_citing_pid) & set(citing_pids):
                edges.append([inter_pid,cpid])
            # j=i+1
            # while j<len(citing_pids):
                
            #     scpid = citing_pids[j]
            #     j+=1
            #     if cp_dict.get(scpid,'-1')=='-1':
            #         continue
            #     else:
                    

        pdict['edges'] = edges
        pdict['cnum'] = len(citing_pids)
        pdict['enum'] = len(edges)

        cn[pid] = pdict

    open(outpath,'w').write(json.dumps(cn))
    logging.info('citation cascade saved to {:}.'.format(outpath))

def main(path):
    citation_network_path = build_citation_network(path)
    build_cascades(citation_network_path)


if __name__ == '__main__':
    if len(sys.argv)==2:
        main(sys.argv[1])
    else:
        print 'ERROR: only one parameter: [path/to/aminer_reference.json]'
    # build_cascades(sys.argv[1],sys.argv[2])