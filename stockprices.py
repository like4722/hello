import pandas as pd
import numpy as np
import xlrd
import glob,os
from datetime import date
import matplotlib.pyplot as plt
import math
from scipy.stats import norm
#import scipy.stats as st

def read_csv():
    #data = xlrd.open_workbook(r"D:\data.xlsx")
    path = r"D:"
    file = glob.glob(os.path.join(path,"data.csv"))
    print(file)
    df = []
    for f in file:
        df.append(pd.read_csv(f, index_col=None))
    df = pd.concat(df)
    df.dropna(axis=0, how='any', inplace=True)
    print(df)
    return(df)

#sortino ratio
def ortino_ratio(daily_return):
    for i in daily_return:
        if(i<0):
            a = i
            break
    list_return = [a]
    print(list_return)
    for j in daily_return:
        if((j<0)):
            list_return.append(j)
    print(list_return)
    return_pd = pd.DataFrame(list_return)
    return(return_pd.std())

def MaxDrawdown(return_list):
    '''最大回撤率'''
    i = np.argmax((np.maximum.accumulate(return_list) - return_list) / np.maximum.accumulate(return_list))  # 结束位置
    if i == 0:
        return 0
    j = np.argmax(return_list[:i])  # 开始位置
    return (return_list[j] - return_list[i]) / (return_list[j])


if __name__ == '__main__':
   StockPrices = read_csv()
   StockPrices_data = StockPrices
   #归一化收盘价格
   #print(type(StockPrices))
   #for stock in ['Portfolio A']:
    #   stock['normalized_price A'] = stock['Adj. Close']/stock['Adj. Close'].iloc[0]
   #StockPrices['Total'] = StockPrices.sum(axis=1)
   #print(StockPrices)
   #plt.style.use('ggplot')
   #StockPrices['Total'].plot(label='Total')
   #plt.legend(loc='best')
   #plt.title('Total Portfolio Value')

   #StockPrices.drop('Total', axis=1).plot(figsize=(8, 4))
   #plt.show()
   # 日收益率
   StockPrices['daily return A']=StockPrices['Portfolio A'].pct_change(1)
   StockPrices['daily return B'] = StockPrices['Portfolio B'].pct_change(1)

   print("日收益率",StockPrices)
   # 累积回报率
   cumulative_return_A = StockPrices['Portfolio A'].iloc[-1] / StockPrices['Portfolio A'].iloc[0] - 1
   cumulative_return_B = StockPrices['Portfolio B'].iloc[-1] / StockPrices['Portfolio B'].iloc[0] - 1
   print("累积回报率",cumulative_return_A,cumulative_return_B)

   #平均日回报率
   average_return_A = StockPrices['daily return A'].mean()
   average_return_B = StockPrices['daily return B'].mean()
   print("平均日回报率",average_return_A, average_return_B)

   #日回报率的标准差
   print("日回报率的标准差",StockPrices['daily return A'].std(),StockPrices['daily return B'].std())



   #normalized annual return
   annualreturn_A = StockPrices['Portfolio A'].iloc[-1] / StockPrices['Portfolio A'][0] / 520 * 365
   annualreturn_B = StockPrices['Portfolio B'].iloc[-1]  / StockPrices['Portfolio B'][0] / 520 * 365
   print("normalized annual return", annualreturn_A, annualreturn_B)

   # 对数收益率
   logreturns_A = np.diff(StockPrices['Portfolio A'])
   logreturns_B = np.diff(StockPrices['Portfolio B'])
   print("对数收益率", logreturns_A, logreturns_B)

   # 波动率
   annualVolatility = logreturns_A.std() / logreturns_A.mean()
   annualVolatility = annualVolatility / np.sqrt(1 / 252)
   print("A年波动率：", annualVolatility)

   annualVolatility = logreturns_B.std() / logreturns_B.mean()
   annualVolatility = annualVolatility / np.sqrt(1 / 252)
   print("B年波动率：", annualVolatility)


   # 夏普比率
   SR_A = StockPrices['daily return A'].mean() / StockPrices['daily return A'].std()
   SR_B = StockPrices['daily return B'].mean() / StockPrices['daily return B'].std()
   print("夏普比率",SR_A,SR_B)

   # 最大回撤率
   print("A最大回撤率",MaxDrawdown(StockPrices['Portfolio A'].tolist()))
   print("B最大回撤率", MaxDrawdown(StockPrices['Portfolio B'].tolist()))

   # 索提诺比率
   OR_A = StockPrices['daily return A'].mean() / ortino_ratio(StockPrices['daily return A'].tolist()) * np.sqrt(252)
   OR_B = StockPrices['daily return B'].mean() / ortino_ratio(StockPrices['daily return B'].tolist()) * np.sqrt(252)
   print("索提诺比率", OR_A, OR_B)

   # 协方差矩阵法
   A_var = norm.ppf(0.05,StockPrices['Portfolio A'].pct_change(1).mean(),
                     StockPrices['Portfolio A'].pct_change(1).std()) / 100
   B_var = norm.ppf(0.05, StockPrices['Portfolio B'].pct_change(1).mean(),
                     StockPrices['Portfolio B'].pct_change(1).std()) / 100
   print("VaR",A_var,B_var )

   # 历史模拟法
   A_var =StockPrices['Portfolio A'].pct_change(1).quantile(0.05) / 100
   B_var = StockPrices['Portfolio B'].pct_change(1).quantile(0.05) / 100
   print("VaR", A_var, B_var)

   # -------------------------------------------------------------------------
   #两只股票的相关性

   # 计算相关矩阵
   correlation_matrix = StockPrices[['daily return A', 'daily return B']].corr()
   # 输出相关矩阵
   print(correlation_matrix)

   # 计算协方差矩阵
   cov_matrix = StockPrices[['daily return A', 'daily return B']].cov()
   # 年化协方差矩阵
   cov_matrix_annual = cov_matrix * 252
   # 输出协方差矩阵
   print(cov_matrix_annual)

   # 标准差
   print("标准差", StockPrices['daily return A'].std(), StockPrices['daily return B'].std())
   print("均值", StockPrices['daily return A'].mean(), StockPrices['daily return B'].mean())


