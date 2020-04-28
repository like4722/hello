#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import pandas as pd
import glob
#合并多个CSV文件

def combine():
    csv_list = glob.glob('D:\\combine\\*')
    print(u'共发现%s个CSV文件'% len(csv_list))
    print(u'正在处理......')
    for i in csv_list:
        fr = open(i,'rb').read()
        with open('D:\\combine\\result.csv','ab') as f:  #将结果保存为result.csv
            f.write(fr)
        print(u'合并完毕！')

#去重
def duplicate():
    df = pd.read_csv('D:\\combine\\result.csv',encoding="gbk",header=0)
    df.info()
    datalist = df.drop_duplicates()
    datalist.to_csv('D:\\combine\\result.csv',encoding="gbk",index=0)


def main():
    combine()
    #duplicate()
if __name__ == '__main__':
    main()