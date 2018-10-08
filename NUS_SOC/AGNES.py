from scipy.cluster import hierarchy  #用于进行层次聚类，话层次聚类图的工具包
from scipy import cluster
import matplotlib.pyplot as plt

# test data
data = [[10000,662,877,255,412,966],[662,10000,295,468,268,400],[877,295,10000,754,564,138],
[255,468,754,10000,219,869],[412,268,564,219,10000,669],[996,400,138,869,669,10000]]
index = [i for i in range(len(data))]

# distance function
def f(i,j):
    return data[int(i[0])][int(j[0])]
    
# test running
test = [[0],[1],[2],[3],[4],[5]]
Z = hierarchy.linkage(test, method ='single',metric = f)
# print(Z)
label = cluster.hierarchy.cut_tree(Z,height=220)
label = label.reshape(label.size,)
print(label)
hierarchy.dendrogram(Z,labels = [i for i in range(len(data))],color_threshold = 266)
plt.show()
