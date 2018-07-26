data = [[0,662,877,255,412,966],[662,0,295,468,268,400],[877,295,0,754,564,138],[255,468,754,0,219,869],[412,268,564,219,0,669],[996,400,138,869,669,0]]
copy = data.copy()
length = len(data)

cluster = [[i] for i in range(length)]
def cal_ave(i,j,cluster):
    return sum(data[a][b] for a in cluster[i] for b in cluster[j])/(len(cluster[i])*len(cluster[j]))
def find_min(M):
    minvalue = 1000
    x = 0;y = 0
    for i in range(len(M)):
        for j in range(len(M[i])):
            if i !=j and M[i][j] < minvalue:
                minvalue = M[i][j];x = i;y = j
    return (x,y,minvalue)
for i in range(1,length):
    x,y,minvalue = find_min(copy)
    cluster[min(x,y)].extend(cluster[y])
    cluster.remove(cluster[y])
    copy = [[] for i in range(5)]
    for i in range(len(cluster)):
        for j in range(len(cluster)):
            copy[i].extend([cal_ave(i,j,cluster)])
    print(cluster)
