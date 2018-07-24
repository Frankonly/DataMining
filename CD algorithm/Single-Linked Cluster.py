# test data
data = [[0,662,877,255,412,966],[662,0,295,468,268,400],[877,295,0,754,564,138],
[255,468,754,0,219,869],[412,268,564,219,0,669],[996,400,138,869,669,0]]

# distmatrix是距离矩阵(二维数组)，k为最后的聚类数量
def SLCluster(distmatrix,k):
    clusters = [[i] for i in range(len(distmatrix))]
    abandon = [False for i in range(len(distmatrix))]
    newDist = distmatrix
    for _ in range(len(clusters) - k):
        minDist = 1000 #根据情况改参数
        x = 0
        y = 0
        for i in range(len(newDist)):
            if not abandon[i]:
               for j in range(i+1,len(newDist[i])):
                    if not abandon[j] and newDist[i][j] < minDist:
                        minDist,x,y=newDist[i][j],i,j
        if len(clusters[x]) < len(clusters[y]):
            x,y = y,x
        abandon[y] = True
        for i in range(len(newDist[x])):
            if not abandon[i] and i != x:
                newDist[x][i] = newDist[i][x] = min(newDist[x][i],newDist[y][i])
        clusters[x].extend(clusters[y])
    finalClusters = [clusters[i] for i in range(len(clusters)) if not abandon[i]]
    return finalClusters

# test running
print(SLCluster(data,1))
