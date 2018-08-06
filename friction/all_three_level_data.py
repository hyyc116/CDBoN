#coding:utf-8

'''
三个level的所有论文
'''

import json

def three_cited_papers():
    data_path = 'data/aminer_citation_dict.json'

    data = json.loads(open(data_path).read())

    high_cited_papers = {}
    medium_cited_papers = {}
    low_cited_papers = {}

    for k in data.keys():
        if data[k]['year']>2005:
            continue

        citation_num = len(data[k]['citations'])
        citation_num_list[citation_num].append(k)

        if citation_num>1000:
            # high_selected.append(k)
            # high_citation_nums.append(citation_num)
            high_cited_papers[k] = data[k]

        elif citation_num > 14:
            medium_cited_papers[k] = data[k]

        else:

            low_cited_papers[k] = data[k]



    open('data/all_low_cited_papers.json','w').write(json.dumps(low_cited_papers))
    open('data/all_medium_cited_papers.json','w').write(json.dumps(medium_cited_papers))
    open('data/all_high_cited_papers.json','w').write(json.dumps(high_cited_papers))


if __name__ == '__main__':
    three_cited_papers()