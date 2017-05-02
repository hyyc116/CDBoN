#coding:utf-8

from basic_config import *


#from the aminer_refence to build citation network
def build_citation_network(path):
    ref_dict=defaultdict(dict)
    data = json.loads(open(path).read())
    reflist = data['RECORDS']
    print 'Size of reference', len(reflist)
    count=0
    for ref in reflist:
        count+=1
        if count%10000==1:
            print count
        pid = ref['cpid']
        pid_year = ref['cpid_year']
        cited_pid = ref['pid']
        cited_pid_year = ref['pid_year']

        if int(pid_year)<1900 or int(cited_pid_year)<1900 or int(pid_year)<int(cited_pid_year):
            continue

        cited_dict = ref_dict.get(cited_pid,{})
        cited_dict['pid'] = cited_pid
        cited_dict['year'] = cited_pid_year
        citation_list = cited_dict.get('citations',{})
        citation_list[pid]=pid_year
        cited_dict['citations']=citation_list
        ref_dict[cited_pid] = cited_dict

    open('data/aminer_citation_dict.json','w').write(json.dumps(ref_dict))
    print 'done'

#after building the citation network, we build citation cascade
def build_cascades(citation_network):
    cn = json.loads(open(citation_network).read())
    logging.info('data loaded...')
    for pid in cn.keys():
        logging.info('paper id:'+str(pid))
        # for a paper, get its dict
        pdict = cn[pid]
        # for its citation dict
        c_dict = pdict['citations']
        citing_pids = c_dict.keys()
        edges = []
        for i,cpid in enumerate(citing_pids):
            edges.append([pid,cpid])
            #get cpid's citation dict
            if cn.get(cpid,-1)==-1:
                continue
            cp_dict = cn[cpid]['citations']
            j=i+1
            while j<len(citing_pids):
                scpid = citing_pids[j]
                if cp_dict.get(scpid,'-1')=='-1':
                    continue
                else:
                    edges.append([cpid,scipd])

                j+=1

        pdict['edges'] = edges
        pdict['cnum'] = len(citing_pids)
        pdict['enum'] = len(edges)

        cn[pid] = pdict

    open('data/aminer_citation_cascade.json','w').write(json.dumps(cn))
    logging.info('citation cascade saved to data/aminer_citation_cascade.json.')


if __name__ == '__main__':
    # build_citation_network(sys.argv[1])
    build_cascades(sys.argv[1])


