import markov_clustering as mc
import networkx as nx
import random
import numpy
from matplotlib.pylab import show, cm, axis
import scipy.sparse as sp

"""
library needed:
!pip install markov_clustering[drawing]

more details about the mc library on https://github.com/GuyAllard/markov_clustering
"""

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

# test data
test_data = [[0,662,877,0,412,966],[662,0,295,468,268,0],[877,295,0,754,564,0],
[0,468,754,0,219,869],[412,268,564,219,0,0],[996,0,0,869,0,0]]

# test run
csrmatrix = sp.csr_matrix(test_data)
result = mc.run_mcl(csrmatrix)           # run MCL with default parameters
clusters = mc.get_clusters(result)    # get clusters
print(clusters)
draw_graph(csrmatrix, clusters, node_size=50, with_labels=False, edge_color="silver")
