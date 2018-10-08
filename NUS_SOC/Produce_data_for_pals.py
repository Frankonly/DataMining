'''
class Config():
    colors = []
    labels = ['0','1','2','3','4','5']
'''
# produce edges.dat
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
    backup(filename)
    return
#produce community.dat
def export_community_list(communities, filename, labels=Config.labels):
    f = open(filename, 'w')
    indices_in_community = []   
    cur_com = 1
    for c in communities:
        indices = [i for i, x in enumerate(Config.labels) if x in c]
        indices_in_community.extend(indices)
        for i in indices:
            f.write("\"" + Config.labels[i] + "\" " + str(cur_com) + "\n")
        cur_com += 1
    f.close()
    backup(filename)
    return
adjmat = [['1'], ['2','5'], ['3','4','0']]
export_edge_list(adjmat,labels = Config.labels, filename = 'pals-edges.dat', delim = " ")
export_community_list(adjmat,labels = Config.labels, filename = 'pals-communities.dat')  
