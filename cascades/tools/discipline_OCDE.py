#coding:utf-8
'''
@author: hy@tTt

处理OCDE的discipline，从fos_html.txt中生成字典文件

'''
from basic_config import *
import re


def process_fos():

    top_level = '-1'
    second_level = '-1'
    des = ''

    is_content = False

    lines = ''

    for line in open('fos_html.txt'):
        line  = line.strip()

        if line.startswith('<h3>'):
            top_level = re.sub(r'<.*?>','',line)
            # print top_level

        if line.startswith('<p>'):
            second_level = re.sub(r'<.*?>','',line)

            # print top_level,second_level

        if line.startswith('<ul>'):
            is_content=True

        if line.endswith('</ul>'):
            is_content=False

            print '==',top_level
            print '---',second_level
            print '****',des
            lines+=top_level+'\t'+second_level+'\t'+des.strip()+'\n'

            des=''

        if is_content:
            des+=re.sub(r'<.*?>','',line)+' '

    open('OCDE_fos.txt','w').write(lines)



if __name__ == '__main__':
    process_fos()




