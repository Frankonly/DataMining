class Config():
    colors = []
    labels = None

# produce edges.dat
def export_edge_list(sim, labels = Config.labels, filename, delim = ",", header = True):
    f = open(filename, 'w')
    if header:
        f.write("Source,Target\n")
    for i in range(sim.shape[0]):
        for j in range(i+1, sim.shape[1]):
            if sim[i,j] != 0:
                if labels == None:
                    f.write(str(i) + delim + str(j) + "\n")
                else:
                    f.write("\"" + labels[i] + "\"" + delim + "\"" + labels[j] + "\"\n")                          
    f.close()
    files.download(filename)

#produce community.dat
def export_community_list(communities, labels=Config.labels, filename):

    f = open("pals-community.dat", 'w')

    indices_in_community = []   

    cur_com = 1

    for c in communities:
        indices = [i for i, x in enumerate(Config.labels) if x in c]
        indices_in_community.extend(indices)
        for i in indices:
            f.write("\"" + Config.labels[i] + "\" " + str(cur_com) + "\r\n")
        cur_com += 1

    f.close()

    files.download(filename)

export_edge_list(adjmat,labels = Config.labels, filename = 'pals-edges.dat', delim = " ")

export_community_list(adjmat,labels = Config.labels, filename = 'pals-communities.dat')  
