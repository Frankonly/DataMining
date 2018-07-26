# test data
data = [[0,662,877,255,412,966],[662,0,295,468,268,400],[877,295,0,754,564,138],
[255,468,754,0,219,869],[412,268,564,219,0,669],[996,400,138,869,669,0]]

# distmatrix是距离矩阵(二维数组)，k为最后的cluster数量,如果单点过多会被迫停止
def SLCluster(distmatrix,k):
    clusters = [[i] for i in range(len(distmatrix))]
    abandon = [False for i in range(len(distmatrix))]
    newDist = distmatrix
    for _ in range(len(clusters) - k):
        minDist = 1000 #根据情况改参数
        x,y = 0,0
        for i in range(len(newDist)):
            if not abandon[i]:
               for j in range(i+1,len(newDist[i])):
                    if not abandon[j] and newDist[i][j] < minDist and newDist[i][j] != 0: # newDist[i][j] == 0 means there is no edge between the two vertices.
                        minDist,x,y=newDist[i][j],i,j
        if minDist == 1000:
            print("can't merge anymore")
            break
        if len(clusters[x]) < len(clusters[y]): # Faster: merge the smaller one into the larger one. 
            x,y = y,x
        abandon[y] = True
        for i in range(len(newDist[x])):
            if not abandon[i] and i != x: # newDist[i][j] == 0 means no edge between the two vertices.
                if newDist[x][i] == 0:
                    newDist[x][i] = newDist[i][x] = newDist[y][i]
                elif newDist[y][i] == 0:
                    newDist[x][i] = newDist[i][x] = newDist[x][i]
                else:
                    newDist[x][i] = newDist[i][x] = min(newDist[x][i],newDist[y][i])
        clusters[x].extend(clusters[y])
        # test
        # finalClusters = [clusters[i] for i in range(len(clusters)) if not abandon[i]]
        # print(finalClusters)
    finalClusters = [clusters[i] for i in range(len(clusters)) if not abandon[i]]
    return finalClusters

# test running
print(SLCluster(data,1))
