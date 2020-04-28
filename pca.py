#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

#计算均值,要求输入数据为numpy的矩阵格式，行表示样本数，列表示特征
def meanX(dataX):
    return np.mean(dataX,axis=0) #axis=0表示依照列来求均值。假设输入list,则axis=1

"""
參数：
    - XMat：传入的是一个numpy的矩阵格式，行表示样本数，列表示特征    
    - k：表示取前k个特征值相应的特征向量
返回值：
    - finalData：參数一指的是返回的低维矩阵，相应于输入參数二
    - reconData：參数二相应的是移动坐标轴后的矩阵
"""
def pca(XMat,k):
    average = meanX(XMat)
    m,n = np.shape(XMat)
    data_adjust = []
    avgs = np.tile(average,(m,1))
    data_adjust = XMat - avgs
    covX = np.cov(data_adjust.T) #计算协方差矩阵
    featValue, featVec = np.linalg.eig(covX ) #求解协方差矩阵的特征值和特征向量
    index = np.argsort(-featValue)
    finalData = []
    if k>n:
        print("k必须小于特征总量")
        return
    else:
        # 注意特征向量时列向量。而numpy的二维矩阵(数组)a[m][n]中，a[1]表示第1行值
        selectVec = np.matrix(featVec.T[index[:k]])  # 所以这里须要进行转置
        finalData = data_adjust * selectVec.T
        reconData = (finalData * selectVec) + average
    print(finalData)
    #print(reconData)
    return finalData, reconData
def plotBestFit(data1, data2):
    dataArr1 = np.array(data1)
    dataArr2 = np.array(data2)

    m = np.shape(dataArr1)[0]
    axis_x1 = []
    axis_y1 = []
    axis_x2 = []
    axis_y2 = []
    for i in range(m):
        axis_x1.append(dataArr1[i,0])
        axis_y1.append(dataArr1[i,1])
        axis_x2.append(dataArr2[i,0])
        axis_y2.append(dataArr2[i,1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(axis_x1, axis_y1, s=50, c='red', marker='s')
    ax.scatter(axis_x2, axis_y2, s=50, c='blue')
    plt.xlabel('x1'); plt.ylabel('x2');
    plt.savefig("outfile.png")
    plt.show()

def main():
    dataX = np.array([[1,1,2],[1,2,4],[1,3,5],[1,4,6]])
    return pca(dataX, 2)

if __name__=="__main__":
    finalData, reconMat = main()
    plotBestFit(finalData, reconMat)