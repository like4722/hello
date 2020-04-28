#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
import sys
import xlrd
import xlwt

def connect_mysql(sql):
    # 连接database
    conn = pymysql.connect(host="localhost", user="root", password="root", database="dss", charset="utf8")
    # 得到一个可以执行SQL语句的光标对象
    print("connect successful")
    cursor = conn.cursor()
    #sql = 'select * from dss_leg'
    cursor.execute(sql.encode('utf-8'))
    data = cursor.fetchall()
    conn.close()

    return data

def connect_mysqlnew(sql):
    # 连接database
    conn = pymysql.connect(host="10.243.26.240",user="like",password="229398",database="sales",charset="utf8")
    # 得到一个可以执行SQL语句的光标对象
    print("connect successful")
    cursor = conn.cursor()
    #sql = 'select * from dss_leg'
    cursor.execute(sql.encode('utf-8'))
    data = cursor.fetchall()
    conn.close()
    return data
#数据库连接
def connect_mysql_input():
    # 连接database
    conn = pymysql.connect(host="localhost",user="root",password="root",database="dss",charset="utf8")
    # 得到一个可以执行SQL语句的光标对象
    print("connect successful")
    cursor = conn.cursor()
    # 定义要执行的SQL语句
    book = xlrd.open_workbook(r"D:\test.xlsx")
    sheet = book.sheet_by_name("sheet1")
    columnName = ["飞行年","飞行月","合并承运人",'航线中文','始发单位','始发机场','起飞时间','承运人','航段','航班号','航段中文','航线性质','飞行日期','座位数','登机数','收入(快报)','座公里(航节)','叠加客公里','收入(快报捆绑)','座公里(快报捆绑)','全票价收入','飞行小时','团体人数','修正座位数','班次','叠加登机数','公务舱登机数','公务舱座公里(航节)','豪华头等舱登机数','豪华头等舱座公里(航节)','头等舱登机数','头等舱座公里(航节)','公务舱预测收入','头等舱预测收入','豪华头等舱预测收入','公务舱座位数','豪华头等舱座位数','头等舱座位数','补贴收入']
    for r in range(1,sheet.nrows):
        values = []
        for i in range(len(columnName)):
            if (getColumnIndex(sheet, columnName[i])==1):
                if(columnName[i]=="飞行日期"):
                    date = xlrd.xldate_as_tuple(sheet.cell(r, i).value, 0)[0:3]
                    date = str(date[0])+'-'+str(date[1])+'-'+str(date[2])
                    #print(date)
                    values.append(date)
                else:
                    values.append(sheet.cell(r,i).value)
            else:
                values.append("")
        sql =  "insert into dss_leg(飞行年,飞行月,合并承运人,航线中文,始发单位,始发机场,起飞时间,承运人,航段,航班号,航段中文,航线性质,飞行日期,座位数,登机数,`收入(快报)`,`座公里(航节)`,叠加客公里,`收入(快报捆绑)`,`座公里(快报捆绑)`,全票价收入,飞行小时,团体人数,修正座位数,班次,叠加登机数,公务舱登机数,`公务舱座公里(航节)`,豪华头等舱登机数,`豪华头等舱座公里(航节)`,头等舱登机数,`头等舱座公里(航节)`,公务舱预测收入,头等舱预测收入,豪华头等舱预测收入,公务舱座位数,豪华头等舱座位数,头等舱座位数,补贴收入) values (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql,tuple(values))
    # 关闭光标对象
    cursor.close()
    conn.commit()
    # 关闭数据库连接
    conn.close()
    print("connect closed")
    columes = str(sheet.ncols)
    rows = str(sheet.nrows)
    print("导入"+columes+"列"+rows+"行数据到MySQL数据库！")
def connect_mysql_output():
    # 连接database
    conn = pymysql.connect(host="localhost",user="root",password="root",database="dss",charset="utf8")
    # 得到一个可以执行SQL语句的光标对象
    print("connect successful")
    cursor = conn.cursor()
    # 新建excel写入
    book = xlwt.Workbook() #创建一个book
    sheet = book.add_sheet('sheet1') #创建一个sheet表
    sheet = book.sheet_by_name("sheet1")
    columnName = ["飞行年","飞行月","合并承运人",'航线中文','始发单位','始发机场','起飞时间','承运人','航段','航班号','航段中文','航线性质','飞行日期','座位数','登机数','收入(快报)','座公里(杭节)','叠加客公里','收入(快报捆绑)','座公里(快报捆绑)','全票价收入','飞行小时','团体人数','修正座位数','班次','叠加登机数','公务舱登机数','公务舱座公里(航节)','豪华头等舱登机数','豪华头等舱座公里(航节)','头等舱登机数','头等舱座公里(航节)','公务舱预测收入','头等舱预测收入','豪华头等舱预测收入','公务舱座位数','豪华头等舱座位数','头等舱座位数','补贴收入']
    for r in range(1,sheet.nrows):
        values = []
        for i in range(len(columnName)):
            if (getColumnIndex(sheet, columnName[i])==1):
                if(columnName[i]=="飞行日期"):
                    date = xlrd.xldate_as_tuple(sheet.cell(r, i).value, 0)[0:3]
                    date = str(date[0])+'-'+str(date[1])+'-'+str(date[2])
                    print(date)
                    values.append(date)
                else:
                    values.append(sheet.cell(r,i).value)
            else:
                values.append("")

        sql =  "insert into dss_leg(飞行年,飞行月,合并承运人,航线中文,始发单位,始发机场,起飞时间,承运人,航段,航班号,航段中文,航线性质,飞行日期,座位数,登机数,`收入(快报)`,`座公里(航节)`,叠加客公里,`收入(快报捆绑)`,`座公里(快报捆绑)`,全票价收入,飞行小时,团体人数,修正座位数,班次,叠加登机数,公务舱登机数,`公务舱座公里(航节)`,豪华头等舱登机数,`豪华头等舱座公里(航节)`,头等舱登机数,`头等舱座公里(航节)`,公务舱预测收入,头等舱预测收入,豪华头等舱预测收入,公务舱座位数,豪华头等舱座位数,头等舱座位数,补贴收入) values (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql,tuple(values))
    # 执行SQL语句
    #cursor.execute(sql)
    # 关闭光标对象
    cursor.close()
    conn.commit()
    # 关闭数据库连接
    conn.close()
    print("connect closed")
    columes = str(sheet.ncols)
    rows = str(sheet.nrows)
    print("导入"+columes+"列"+rows+"行数据到MySQL数据库！")

def getColumnIndex(table, columnName):
    columnIndex = None
    # print table
    for i in range(table.ncols):
        # print columnName
        # print table.cell_value(0, i)
        if (table.cell_value(0, i) == columnName):
            columnIndex = i
            break
    return 1
# 筛选条件
#def filter(start,end,route):
def filter(argv):
    print(argv[1])
    print(argv[2])
    print(argv[3])

#def main():
#    connect_mysql_output()
    #filter(sys.argv)


#if __name__ == '__main__':
 #   main()
