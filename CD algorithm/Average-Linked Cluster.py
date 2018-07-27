data = adjmat.copy()
length = len(data)
copy = data.copy()
#计算各聚簇之间距离的平均值
def cal_ave(i,j,cluster):
    sum = 0
    for a in cluster[i]:
      for b in cluster[j]:
          if data[a][b] != 0:
            sum = sum + data[a][b]
    return sum/(len(cluster[i])*len(cluster[j]))
#计算各聚簇之间距离的最大值
def cal_max(i,j,cluster):
    maxvalue = 0
    for a in cluster[i]:
        for b in cluster[j]:
            if data[a][b] != 0:
              maxvalue = max(data[a][b],maxvalue)
    return maxvalue
#计算各聚簇之间距离的最小值
def cal_min(i,j,cluster):
  minvalue = 0x7fffffff
  for a in cluster[i]:
    for b in cluster[j]:
      if data[a][b] != 0:
        minvalue = min(data[a][b],minvalue)
  return minvalue
#在新的距离矩阵之间寻找最小的值及这个值对应的下标
def find_min(M):
    minvalue = 1000
    x = 0;y = 0
    for i in range(len(M)):
        for j in range(len(M[i])):
            if i !=j and M[i][j] < minvalue and M[i][j] != 0:
                minvalue = M[i][j];x = i;y = j
    return (x,y,minvalue)
#将聚类功能进行了函数封装，k代表聚簇次数，alg代表聚类算法，cal_ave,cal_min,cal_max分别代表平均聚类，单链聚类和完全聚类
def linked_cluster(alg = cal_ave,k = length,copy = copy):
    cluster = [[i] for i in range(length)]
    print(cluster)
    for i in range(1,k):
        x,y,minvalue= find_min(copy)
        if minvalue != 1000: 
          cluster[x].extend(cluster[y])
          cluster.remove(cluster[y])
          copy = [[] for i in range(len(cluster))]
          for i in range(len(cluster)):
              for j in range(len(cluster)):
                copy[i].extend([alg(i,j,cluster)])
          print(cluster)
linked_cluster(alg = cal_max,k = length)
