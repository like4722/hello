#!/usr/bin/python
# -*- coding: UTF-8 -*-
import getopt
import sys
from math import log
import operator

#TREE
def createDataSet():      #创造示例数据
    dataSet = [['长', '粗', '男'],
               ['短', '粗', '男'],
               ['短', '粗', '男'],
               ['长', '细', '女'],
               ['短', '细', '女'],
               ['短', '粗', '女'],
               ['长', '粗', '女'],
               ['长', '粗', '女']]
    labels = ['头发','声音']  #两个特征
    return dataSet,labels

def calcEntropy(dataSet):     # 计算数据的熵(entropy)总熵
    num = len(dataSet)
    labelCounts={}
    for i in dataSet:
        currentLabel = i[-1] # 每行数据的最后一个字（类别）
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1 # 统计有多少个类以及每个类的数量
        shannonEnt = 0
    for key in labelCounts:
        prob = labelCounts[key]/num     #计算类别概率
        shannonEnt -= prob*log(prob,2)   #累加每个类熵值
    return shannonEnt
def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):  #选择最优的分类特征
    numFeatures = len(dataSet[0])-1 #特征个数
    baseEntropy = calcEntropy(dataSet)   #原始的熵
    bestInfoGain = 0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet] #读取列
        uniqueVals = set(featList)
        newEntropy = 0
        for value in uniqueVals:
            subDataSet =splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob*calcEntropy(subDataSet)# 按特征分类后的熵
        infoGain = baseEntropy - newEntropy # 原始熵与按特征分类后的熵的差值
        if(infoGain>bestInfoGain):  # 若按某特征划分后，熵值减少的最大，则次特征为最优分类特征
            bestInfoGain=infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):#按分类后类别数量排序，比如：最后分类为2男1女，则判定为男；
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]
    if classList.count(classList[0]) ==len(classList):
        return classList[0]
    if len(dataSet[0])==1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet) #选择最优特征
    bestFeatLabel = labels[bestFeat]
    myTree={bestFeatLabel:{}}   #分类结果以字典形式保存
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet \
                (dataSet, bestFeat, value), subLabels)
    return myTree
def main():
    dataSet, labels=createDataSet()  # 创造示列数据
    print(createTree(dataSet, labels))  # 输出决策树模型结果

if __name__=="__main__":
    main()