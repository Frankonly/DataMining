from google.colab import files
def downloadClusters(clusters,labels):
    comm = []
    for i in range(len(clusters)):
        for x in clusters[i]:
            comm.append((labels[x],i+1))
    f = open("community.dat", 'w')
    for c in comm:
        f.write("\"" + c[0] + "\" " + str(c[1]) + "\r\n")
    f.close()
    files.download("community.dat", False)
