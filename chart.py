#!/usr/bin/python
# -*- coding: UTF-8 -*-



from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts import options as opts #引入配置项入口
from module import open_csv
from module import open_excel
from module import write_excel
from module import csv_to_xlsx_pd
import pandas as pd

#bar = Bar()
#bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
#bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
#bar.render('D:\my_first_chart.html')
#line = Line()
#line.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
#line.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
#line.render('D:\my_first_chart.html')
def data_process(df):
    #执管航班
    for i in range(df.iloc[:, 0].size):
        df.loc[i,'航班号'] = df.loc[i,'承运人']+ df.loc[i,'航班号']
    #print(df.iloc[:,0].size)
    write_excel(r'D:\策略小组\数据\20200224日报\数据源(国内)\chart.xlsx', df)

    df_zhiguan = pd.DataFrame(columns=['航线中文', '航班号', '客运收入(万)',
                                  '同比', '座位数', '同比', '座收',
                                  '同比', '客座率', '同比', '折扣率', '同比'])
    print(df_zhiguan)



def main():
    csv_to_xlsx_pd(r'D:\策略小组\数据\20200224日报\数据源(国内)\dss.csv',r'D:\策略小组\数据\20200224日报\数据源(国内)\chart.xlsx')
    df_read = open_excel(r'D:\策略小组\数据\20200224日报\数据源(国内)\chart.xlsx',"Sheet1")
    data_process(df_read)


if __name__ == '__main__':
    main()
