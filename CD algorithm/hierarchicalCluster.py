def hierarchicalCluster(distmatrix,n,method):
    """Get hierarchical clusters from similarity matrix.

    Using hierarchical cluster algorithm to get clusters from similarity matrix.
    now support three methods: single-linked, complete-linked, average-linked.

    The function is coded by 'FrankOnly'. More details in "https://github.com/Frankonly/DataMining/tree/master/CD%20algorithm"

    Args:
        distmatrix: A similarity matrix. If vertix i and vertix j are not connected, set distmatrix[i][j] = distmatrix[j][i] = -1 .
        n: The number of clusters after clustering.
        method: A cluster algorithm used. "single", "complete" or "average".

    Returns:
        A 2-d list presents clusters. Each list contains indices of vertices.
        For example:

        [[0, 3, 4], [1], [2, 5]]

    Raises:
        ValueError: An error occurred with wrong parameter
        RuntimeError: An error occurred when no clustes can be merged.

    """
    if method not in ["single", "complete", "average"]:
        raise ValueError("no such method: {}".format(method))
    clusters = [[i] for i in range(len(distmatrix))]
    abandon = [False for i in range(len(distmatrix))]
    newDist = distmatrix.copy()
    for _ in range(len(clusters) - n):
        minDist = 0x7fffffff #the max number of int32.
        x,y = 0,0
        for i in range(len(newDist)):
            if not abandon[i]:
               for j in range(i+1,len(newDist[i])):
                    if not abandon[j] and newDist[i][j] < minDist and newDist[i][j] != -1:
                        minDist,x,y=newDist[i][j],i,j
        if minDist == 0x7fffffff:
            raise RuntimeError("single vertices are more than n")
        # The function run faster if merge the smaller one into the larger one. 
        if len(clusters[x]) < len(clusters[y]):
            x,y = y,x
        abandon[y] = True
        for i in range(len(newDist[x])):
            if not abandon[i] and i != x:
                if newDist[x][i] == -1:
                    newDist[x][i] = newDist[i][x] = newDist[y][i]
                elif newDist[y][i] == -1:
                    newDist[x][i] = newDist[i][x] = newDist[x][i]
                else:
                    if method == "single":
                        newDist[x][i] = newDist[i][x] = min(newDist[x][i],newDist[y][i])
                    elif method == "complete":
                        newDist[x][i] = newDist[i][x] = max(newDist[x][i],newDist[y][i])
                    else:
                        newDist[x][i] = newDist[i][x] = (newDist[x][i] * len(clusters[x]) + newDist[y][i] * len(clusters[y])) \
                        / (len(clusters[x]) + len(clusters[y]))
        clusters[x].extend(clusters[y])
    finalClusters = [clusters[i] for i in range(len(clusters)) if not abandon[i]]
    return finalClusters

# test data
test_data = [[0,662,877,255,412,966],[662,0,295,468,268,400],[877,295,0,754,564,138],
[255,468,754,0,219,869],[412,268,564,219,0,669],[996,400,138,869,669,0]]

# test run
print(hierarchicalCluster(test_data, 3, "average"))
