# -*- coding: utf-8 -*-
"""“community_detection.ipynb”的副本

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S72-lj1TYiFDwE4Upt5y87rL1RtzJ588

# Community Detection
In this session we shall use a community detection algorithm to discover large community of similar nodes in the graph we constructed in the earlier session "Finding pairwise dissimilarity from Siamese Network".

##Test case name
Please set the variable "name" below to a name of your choice. <br>
Use any name, but please choose one that does not conflict with others' choices, e.g. your name.<br>
**For the initial lab session, do not change this -- just leave this as "trial".**
"""

name="Frankonly"

"""## Imports"""

# Install GCP modules

!apt-get install -y -qq software-properties-common python-software-properties module-init-tools

# Install NetworkX module

!pip3 install networkx

# %matplotlib inline
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import PIL.ImageOps    
from PIL import Image
import numpy as np
import itertools
import math
import os
from google.colab import files, auth

"""## Helper functions"""

def hierarchicalCluster(distmatrix,n,method):
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
        print(finalClusters)
    return finalClusters
  
def imshow(img):
    npimg = img.numpy()
    plt.axis("off")
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()    

def show_plot(iteration, loss):
    plt.plot(iteration, loss)
    plt.show()
    
# Set use_gcp to False to download a file to your local harddisk
def backup(filename, use_gcp=True):
    if name == "trial" and use_gcp: # No backup for the trial
        print("File \"" + filename + "\" not backed up since this is a trial run")
        return
    if use_gcp:
        project_id = 'customer-project-on-google'
        auth.authenticate_user()
        os.system("gcloud config set project customer-project-on-google")
        os.system("gsutil copy " + filename + " gs://harddisk-1/" + name + "/")
    else:
        files.download(filename)

# Set use_gcp to False to upload a file from your local harddisk
def restore(filename, use_gcp=True):
    if use_gcp:
        project_id = 'customer-project-on-google'
        auth.authenticate_user()
        os.system("gcloud config set project customer-project-on-google")
        os.system("gsutil copy gs://harddisk-1/" + name + "/" + filename + " .")
    else:
        if os.path.exists(filename):
            os.remove(filename)
        uploaded = files.upload()
    !ls -l {filename}

# Creates a NetworkX graph object
def make_graph(sim, labels=None):
    G = nx.Graph()
    for i in range(sim.shape[0]):
        for j in range(sim.shape[1]):
            if i != j and sim[i,j] != 0:
                if labels == None:
                    G.add_edge(i, j, weight=sim[i,j])
                else:
                    G.add_edge(labels[i], labels[j], weight=sim[i,j])
    return G

# Save graph for use in Gephi or pals
def export_edge_list(sim, filename, delim = ",", header = True, labels = Config.labels):
    f = open(filename, 'w')
    if header:
        f.write("Source,Target\n")
    for i in range(len(sim[0])):
        for j in range(i+1, len(sim[1])):
            if sim[i,j] != 0:
                if labels == None:
                    f.write(str(i) + delim + str(j) + "\n")
                else:
                    f.write("\"" + labels[i] + "\"" + delim + "\"" + labels[j] + "\"\n")                          
    f.close()
    backup(filename,False)
    return
def downloadClusters(clusters,labels):
    comm = []
    for i in range(len(clusters)):
        for x in clusters[i]:
            comm.append((labels[int(x)],i+1))
    f = open("community.dat", 'w')
    for c in comm:
        f.write("\"" + c[0] + "\" " + str(c[1]) + "\r\n")
    f.close()
    files.download("community.dat")

"""##Configuration"""

class Config():
    colors = ['aquamarine', 'bisque', 'blanchedalmond', 'blueviolet', 'brown',
              'burlywood', 'cadetblue', 'chartreuse','chocolate', 'coral',
              'cornflowerblue', 'cornsilk', 'crimson', 'darkblue', 'darkcyan',
              'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki',
              'darkmagenta', 'darkolivegreen', 'darkorange', 'darkslateblue',
              'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
              'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet',
              'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue',
              'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
              'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow',
              'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory']
    labels = None

"""## Build graph
Construct an adjacency matrix from the dissimilarity matrix, then use the adjacency matrix to build a networkx graph
"""

# Load a saved copy of the dissimilarity matrix

restore("_sim.txt",False)
# backup("_sim.txt")

# Loads the dissimilarity matrix (and node labels)

sim = np.loadtxt('_sim.txt')
print("Restored {}x{} matrix".format(sim.shape[0], sim.shape[1]))

# Restore labels from saved "_labels.csv" file

restore("_labels.csv")

Config.labels = []
with open('_labels.csv') as f:
    for line in f:
        _, label = line.rstrip().split(",")
        Config.labels.append(label)

print("Loaded labels (" + str(len(Config.labels)) + " classes): ", end='')
print(Config.labels)

# Analyze distribution of dissimilarity score

d = np.diagonal(sim)
print('diagonal avg={0:.2f} min={1:.2f} max={2:.2f}'.format(np.mean(d), np.min(d), np.max(d)))
simflat = sim.reshape((-1,))
_ = plt.hist(simflat, bins=200)

# Select a suitable threshold and set dissimilarity scores larger than that threshold to zero

threshold = 208
adjmat = sim.reshape((-1,)).copy()
sadjmat = adjmat.copy()
ssadjmat = adjmat.copy()
sadjmat[sadjmat > threshold] = -1
ssadjmat[ssadjmat > threshold] = 1000
adjmat[adjmat > threshold] = 0
# adjmat[adjmat > 0] = 1
print("{} out of {} values set to zero".format(len(adjmat[adjmat == 0]), len(adjmat)))
adjmat = adjmat.reshape(sim.shape)
sadjmat = sadjmat.reshape(sim.shape)
ssadjmat = ssadjmat.reshape(sim.shape)
# print(sadjmat)

# Construct a networkx graph from the adjacency matrix
# (Singleton nodes are excluded from the graph)

G = make_graph(adjmat, labels=Config.labels)
nx.draw_spring(G, with_labels=True)
# new_labels = []
# for i in range(len(adjmat)):
#   for j in range(len(adjmat)):
#     if adjmat[i][j] > 0:
#       new_labels.append(Config.labels[i])
#       break
# print(new_labels)

"""##Community detection using Girvan-Newman"""

from networkx.algorithms.community.centrality import girvan_newman

comp = girvan_newman(G)

max_shown = 10
shown_count = 1
possibilities = []
for communities in itertools.islice(comp, max_shown):
    print("Possibility", shown_count, ": ", end='')
    print(communities)
    possibilities.append(communities)
    color_map = ["" for x in range(len(G))]
    color = 0
    for c in communities:
        indices = [i for i, x in enumerate(G.nodes) if x in c]
        for i in indices:
            color_map[i] = Config.colors[color]
        color += 1
    shown_count += 1
    nx.draw(G, node_color=color_map, with_labels=True)
    plt.show()

"""##Visualization"""

!pip install scipy
!pip install matplotlib
!pip install markov_clustering[drawing]

H = hierarchicalCluster(sadjmat,11,"single")
F = ([[Config.labels[j] for j in i] for i in H])
F
downloadClusters(H,Config.labels)

from scipy.cluster import hierarchy  #用于进行层次聚类，话层次聚类图的工具包
from scipy import cluster
import matplotlib.pyplot as plt
# print(ssadjmat)
def f(i,j):
    return ssadjmat[int(i[0])][int(j[0])]
usr = [[i] for i in range(len(ssadjmat))]
Z = hierarchy.linkage(usr, method ='single',metric = f)
# hierarchy.dendrogram(Z,labels = Config.labels)
print(Z)
hierarchy.dendrogram(Z,labels = [i for i in range(24)],color_threshold = 217)
# print(Config.labels[8])
plt.show()
print(Config.labels[14],Config.labels[15],Config.labels[16],Config.labels[17])

import markov_clustering as mc
import networkx as nx
import random
import numpy
from matplotlib.pylab import show, cm, axis
import scipy.sparse as sp


def draw_graph(matrix, clusters, **kwargs):

    """
    Visualize the clustering
    
    :param matrix: The unprocessed adjacency matrix
    :param clusters: list of tuples containing clusters as returned
                     by 'get_clusters'
    :param kwargs: Additional keyword arguments to be passed to
                   networkx.draw_networkx
    """
    # make a networkx graph from the adjacency matrix
    graph = nx.Graph(matrix)
    
    # map node to cluster id for colors
    cluster_map = {node: i for i, cluster in enumerate(clusters) for node in cluster}
    colors = [cluster_map[i] for i in range(len(graph.nodes()))]
    
    # if colormap not specified in kwargs, use a default
    if not kwargs.get("cmap", False):
        kwargs["cmap"] = cm.tab20
    
    # draw
    nx.draw_networkx(graph, node_color=colors, **kwargs)
    axis("off")
    show(block=True)

csrmatrix = sp.csr_matrix(adjmat)
result = mc.run_mcl(csrmatrix, expansion=2, inflation=2, loop_value=1,iterations=200, pruning_threshold=0.01, pruning_frequency=0.1,convergence_check_frequency=1, verbose=False)           # run MCL with default parameters
clusters = mc.get_clusters(result)    # get clusters
print(clusters)
draw_graph(csrmatrix, clusters, node_size=50, with_labels=False, edge_color="silver")
print(Config.labels)

"""###Gephi
Gephi Download - https://gephi.org/users/download/<br>
Gephi HOWTO    - https://gephi.wordpress.com/2017/09/26/gephi-0-9-2-a-new-csv-importer/<br>
*(It is possible to colorize communities in Gephi - read here: https://github.com/kalngyk/repoman/raw/master/gephi_communities.pdf)*
"""

# Generate and download edges for Gephi

export_edge_list(adjmat, labels=Config.labels, filename='gephi-edges.csv')
backup('gephi-edges.csv', False)

"""###pals
pals HOWTO - https://github.com/kalngyk/repoman/raw/master/usepals.pdf
"""

# Generate the community file for pals system

# which_possibility = 7

# communities = possibilities[which_possibility-1]

# indices_in_community = []   # For obtaining submatrix of adjmat

# f = open("pals-community.dat", 'w')
# cur_com = 1
# for c in communities:
#     f.write("\"" + Config.labels[i] + "\" " + str(cur_com) + "\r\n")
# f.close()

# backup("pals-community.dat", False)


# Generate the graph file for pals system

# Obtain the submatrix of adjmat with only elements that appear in communities
# indices_in_community = sorted(indices_in_community)
# adjmat_in_community = adjmat[indices_in_community,:][:,indices_in_community]

# Obtain sublist of labels of only elements that appear in communities
# labels = np.array(Config.labels)[indices_in_community].tolist()
# print(communities)
export_edge_list(adjmat, labels=Config.labels, filename='pals-edges.dat', delim=" ", header=True)

# backup('pals-edges.dat', False)

