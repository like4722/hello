#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import pandas as pd
from pandas import DataFrame,Series
from mysql import connect_mysql
from mysql import connect_mysql_input
import sys
import xlrd
import xlutils.copy
from decimal import *
import re
import openpyxl
import xlsxwriter

#def csv_handle():
#    data = connect_mysql()
def tuple_float(p):#
    if(str(p[0][0]) == 'None'):
        return 0
    else:
        float1 = p[0][0]
        return float1
def tuple_str(p):#
    pattern = re.compile("'(.*)'")
    str1 = pattern.findall(str(p[0]))[0]
    return str1
def tuple_precent(p):
    per = "%.2f%%" % (p * 100)
    return per
def occupy(cap,p):
    print((cap))
    if(str(cap[0])[1:5] == 'None'):
        print("无"+sys.argv[1]+"航线，请核实！")
        sys.exit(0)
    else:
        if(str(p[0])[1:5] == 'None'):
            print("该航司无此航线，请核实！")
            return '{:.2%}'.format(0)
        else:
            return tuple_precent(tuple_float(connect_mysql(p))/cap)

def round_up(value):
    # 替换内置round函数,实现保留2位小数的精确四舍五入
    return round(value * 100) / 100.0
def chart_pie(ws,rows,columns):
    chart = ws.add_chart({"type":"pie"})
    chart.add_series({
        # "name":"饼形图",
        "categories": rows,
        "values": columns
    })
    chart.set_title({"name": "饼图成绩单"})
    chart.set_style(3)
    # 插入图表
    ws.insert_chart("W4", chart)
    # 关闭EXCEL文件
    ws.close()
def write_csv():
    book = xlrd.open_workbook(r"D:\FFDT.xlsx")
    wb = xlutils.copy.copy(book)  # 创建一个可写入的副本
    ws = wb.get_sheet(0)
    ws.write(4, 0, sys.argv[1])
    list_comp = ['南航','东上航','国深航','海航','川航','山东航','厦航','天津航','首都航','祥鹏航','吉祥航']
    list_comp1 = []
    cap = "select sum(座位数) from dss_leg where 航线中文='" + sys.argv[1] + "'" + " and 飞行年='" + '2018年' + "'"
    if(str(cap[0][0]) == 'None'):
        print("无"+sys.argv[1]+"航线，请核实！")
        sys.exit(0)
    cap = tuple_float(connect_mysql(cap))
    cap2 = 1
    for i in range(len(list_comp)):
        cap1 = "select sum(座位数) from dss_leg where 航线中文='"+sys.argv[1]+"'"+" and 合并承运人='"+list_comp[i]+"'"+" and 飞行年='"+'2018年'+"'"
        list_comp1.append(tuple_float(connect_mysql(cap1))/ cap)
        cap1 = tuple_precent(tuple_float(connect_mysql(cap1)) / cap)
        ws.write(4, i+1, cap1)
        cap2 = cap2 - list_comp1[i]
    cap2 =  round_up(cap2) #四舍五入
    ws.write(4,12,tuple_precent(cap2))
    wb.save(r"D:\FFDT1.xls")
    print(sys.argv[1])
    work = xlsxwriter.Workbook(r"D:\FFDT1.xls")
    worksheet = work.get_sheet(0)
    chart_pie(worksheet, list_comp, list_comp1)



def main():
    #connect_mysql_input()
    write_csv()
    #connect_mysql_input()

if __name__ == '__main__':
    main()