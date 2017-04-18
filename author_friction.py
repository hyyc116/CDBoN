#coding:utf-8
import sys
import json

def get_top_authors(path):
    authors = json.loads(open(path).read())['RECORDS']

    top_100_authors=[]
    for author in sorted(authors,key=lambda x:x['h_index'],reverse=True)[:100]:
        top_100_authors.append(author)

    open('data/top_100_authors.json','w').write(json.dumps(top_100_authors))

if __name__ == '__main__':
    get_top_authors(sys.argv[1])
