#data是不相似度矩阵
data = [[0,662,877,255,412,966],[662,0,295,468,268,400],[877,295,0,754,564,138],[255,468,754,0,219,869],[412,268,564,219,0,669],[996,400,138,869,669,0]]
copy = data.copy()
length = len(data)

cluster = [[i] for i in range(length)]
#计算各聚簇之间距离的平均值
def cal_ave(i,j,cluster):
    return sum(data[a][b] for a in cluster[i] for b in cluster[j])/(len(cluster[i])*len(cluster[j]))
#计算各聚簇之间距离的最大值
def cal_max(i,j,cluster):
    return max(data[a][b] for a in cluster[i] for b in cluster[j])
#计算各聚簇之间距离的最小值
def cal_min(i,j,cluster):
    return min(data[a][b] for a in cluster[i] for b in cluster[j])
#在新的距离矩阵之间寻找最小的值及这个值对应的下标
def find_min(M):
    minvalue = 1000
    x = 0;y = 0
    for i in range(len(M)):
        for j in range(len(M[i])):
            if i !=j and M[i][j] < minvalue:
                minvalue = M[i][j];x = i;y = j
    return (x,y,minvalue)
#将聚类功能进行了函数封装，k代表聚簇次数，alg代表聚类算法，cal_ave,cal_min,cal_max分别代表平均聚类，单链聚类和完全聚类,输出的是聚簇后的结果，用一个二维list表示
def linked_cluster(k = length,alg = cal_ave,copy = copy):
    for i in range(1,k):
        x,y,minvalue = find_min(copy)
        cluster[min(x,y)].extend(cluster[y])
        cluster.remove(cluster[y])
        copy = [[] for i in range(5)]
        for i in range(len(cluster)):
            for j in range(len(cluster)):
                copy[i].extend([alg(i,j,cluster)])
    return cluster
print(linked_cluster())
