from math import log
import treePlotter
import sys

##### 计算信息熵 #####
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)  # 样本数
    labelCounts = {}   # 创建一个数据字典：key是最后一列的数值（即标签，也就是目标分类的类别），value是属于该类别的样本个数
    for featVec in dataSet: # 遍历整个数据集，每次取一行
        currentLabel = featVec[-1]  #取该行最后一列的值
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0  # 初始化信息熵
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2) #log base 2  计算信息熵
    return shannonEnt

##### 计算基尼系数 #####
def calcGiniCoe(dataSet):
    numEntries = len(dataSet)  # 样本数
    labelCounts = {}   # 创建一个数据字典：key是最后一列的数值（即标签，也就是目标分类的类别），value是属于该类别的样本个数
    for featVec in dataSet: # 遍历整个数据集，每次取一行
        currentLabel = featVec[-1]  #取该行最后一列的值
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    giniCoe = 1.0  # 初始化基尼系数
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        giniCoe -= prob * prob #计算基尼系数
    return giniCoe

##### 按给定的特征划分数据 #####
def splitDataSet(dataSet, axis, value): #axis是dataSet数据集下要进行特征划分的列号例如outlook是0列，value是该列下某个特征值，0列中的sunny
    retDataSet = []
    for featVec in dataSet: #遍历数据集，并抽取按axis的当前value特征进划分的数据集(不包括axis列的值)
        if featVec[axis] == value: #
            reducedFeatVec = featVec[:axis]     #chop out axis used for splitting
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

##### 选取当前数据集下，用于划分数据集的最优特征 #####
def chooseBestFeatureToSplit(dataSet,alg):
    numFeatures = len(dataSet[0]) - 1      #获取当前数据集的特征个数，最后一列是分类标签
    bestInfo = 0.0; bestFeature = -1   #初始化最优信息增益和最优的特征
    if alg < 2:
        baseEntropy = calcShannonEnt(dataSet)  #计算当前数据集的信息熵
    elif alg == 2: bestInfo = 1.0
    for i in range(numFeatures):        #遍历每个特征iterate over all the features
        featList = [example[i] for example in dataSet]#获取数据集中当前特征下的所有值
        uniqueVals = set(featList)       # 获取当前特征值，例如outlook下有sunny、overcast、rainy
        if alg < 2:                 #ID3决策树或C4.5决策树
            newEntropy = 0.0
            iv = 0.0
            for value in uniqueVals: #计算每种划分结果的信息熵
                subDataSet = splitDataSet(dataSet, i, value)
                prob = len(subDataSet) / float(len(dataSet))
                iv -= prob * log(prob,2) #log base 2 计算划分的信息熵，作为增益率计算的除数
                newEntropy += prob * calcShannonEnt(subDataSet)
            infoGain = baseEntropy - newEntropy     #计算信息增益
            infoRatio = infoGain / iv
            if alg == 0:            #ID3决策树
                if (infoGain > bestInfo):       #比较每个特征的信息增益，只要最好的信息增益
                    bestInfo = infoGain
                    bestFeature = i
            else:                   #C4.5决策树
                if(infoRatio > bestInfo):
                    bestInfo = infoRatio
                    bestFeature = i
        elif alg == 2:              #CART决策树
            GiniIndex = 0.0         #初始化基尼指数
            for value in uniqueVals: #计算每种划分结果的基尼系数
                subDataSet = splitDataSet(dataSet, i, value)
                prob = len(subDataSet) / float(len(dataSet))
                GiniIndex += prob * calcGiniCoe(subDataSet)   #计算基尼指数
            if(GiniIndex < bestInfo):
                bestInfo = GiniIndex
                bestFeature = i
    return bestFeature                      #returns an integer

##### 生成决策树主方法 #####
def createTree(dataSet,labels,alg = '0'):
    classList = [example[-1] for example in dataSet] # 返回当前数据集下标签列所有值
    if classList.count(classList[0]) == len(classList):
        return classList[0]#当类别完全相同时则停止继续划分，直接返回该类的标签
    if len(dataSet[0]) == 1: ##遍历完所有的特征时，仍然不能将数据集划分成仅包含唯一类别的分组 dataSet
        return set([a[0] for a in dataSet])
    bestFeat = chooseBestFeatureToSplit(dataSet, int(alg)) # 获取最好的分类特征索引
    bestFeatLabel = labels[bestFeat] #获取该特征的名字

    # 这里直接使用字典变量来存储树信息，这对于绘制树形图很重要。
    myTree = {bestFeatLabel:{}} #当前数据集选取最好的特征存储在bestFeat中
    del(labels[bestFeat]) #删除已经在选取的特征
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:] #如果直接传labels给creatTree在递归中会因为改动发生错误，所以这里进行复制
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels,alg)
    return myTree

def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict): 
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: classLabel = valueOfFeat
    return classLabel

def storeTree(inputTree,filename):
    import pickle
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)


if __name__ == '__main__':
    fr = open(sys.argv[1])        #传入的第一个参数为存储DataSet的txt文件
    lenses =[inst.strip().split(' ') for inst in fr.readlines()]
    fr.close()
    fr = open(sys.argv[2])        #传入的第二个参数为存储labels的txt文件
    lensesLabels = fr.readlines()[0].strip().split(' ')
    if len(sys.argv) > 3:         #第三个参数为决策数类型，如果不设置默认为ID3
        lensesTree = createTree(lenses,lensesLabels,sys.argv[3])
    else:
        lensesTree = createTree(lenses,lensesLabels)
    treePlotter.createPlot(lensesTree)  #将树画出来
